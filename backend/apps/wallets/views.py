import logging
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.db import transaction

from .models import Wallet, WalletTransaction, Currency, ExchangeRate
from .serializers import (
    WalletSerializer, WalletCreateSerializer, WalletTransactionSerializer,
    BalanceUpdateSerializer, TransferSerializer, CurrencySerializer,
    ExchangeRateSerializer, CurrencyConversionSerializer
)
from .services import WalletService, CurrencyService, WalletLimitService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(tags=['Wallets'], description='Lister mes wallets'),
    retrieve=extend_schema(tags=['Wallets'], description='Détails d\'un wallet'),
    create=extend_schema(tags=['Wallets'], description='Créer un nouveau wallet'),
)
class WalletViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des portefeuilles.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # L'utilisateur ne voit que ses propres wallets
        if getattr(self, 'swagger_fake_view', False):
            return Wallet.objects.none()
        return WalletService.get_user_wallets(self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return WalletCreateSerializer
        return WalletSerializer
    
    def perform_create(self, serializer):
        # Utiliser le service pour la création
        WalletService.create_wallet(
            user_id=self.request.user.id,
            currency_code=serializer.validated_data['currency'].code,
            wallet_type=serializer.validated_data.get('wallet_type', 'PERSONAL'),
            name=serializer.validated_data.get('name', ''),
            description=serializer.validated_data.get('description', '')
        )

    # --- Transactions d'un wallet ---
    @extend_schema(tags=['Wallets'], description='Historique des transactions d\'un wallet')
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        wallet = self.get_object()
        transactions = WalletTransaction.objects.filter(wallet=wallet).order_by('-created_at')
        
        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = WalletTransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    # --- Transfert entre wallets ---
    @extend_schema(tags=['Transactions'], request=TransferSerializer)
    @action(detail=False, methods=['post'], url_path='transfer')
    def transfer(self, request):
        """Transférer des fonds entre deux wallets."""
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Vérifier que le wallet source appartient bien à l'utilisateur
        try:
            source_wallet = Wallet.objects.get(id=data['from_wallet_id'], user_id=request.user.id)
        except Wallet.DoesNotExist:
            return Response(
                {'error': 'Wallet source introuvable ou ne vous appartient pas.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Vérifier les limites avant le transfert
            limit_check = WalletLimitService.check_limits(
                wallet_id=source_wallet.id,
                amount=data['amount'],
                operation='DEBIT'
            )
            
            if not limit_check['can_proceed']:
                return Response(
                    {'error': 'Limite dépassée', 'details': limit_check['violations']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Exécuter le transfert
            result = WalletService.transfer_between_wallets(
                from_wallet_id=data['from_wallet_id'],
                to_wallet_id=data['to_wallet_id'],
                amount=data['amount'],
                description=data.get('description', ''),
                reference=data.get('reference')
            )
            
            # Mettre à jour les limites consommées
            WalletLimitService.update_limit_usage(
                wallet_id=source_wallet.id,
                amount=data['amount'],
                operation='DEBIT'
            )
            
            return Response({
                'message': 'Transfert réussi',
                'debit_transaction': str(result['debit_transaction'].id),
                'credit_transaction': str(result['credit_transaction'].id)
            })
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Transfer error: {e}")
            return Response({'error': 'Erreur interne lors du transfert.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['Currencies'])
class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les devises.
    """
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(description='Convertir un montant entre deux devises')
    @action(detail=False, methods=['post'], url_path='convert')
    def convert(self, request):
        serializer = CurrencyConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        try:
            result = CurrencyService.convert_currency(
                amount=data['amount'],
                from_currency=data['from_currency'],
                to_currency=data['to_currency']
            )
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --- Endpoint interne pour mise à jour de solde (Admin / System) ---
@extend_schema(tags=['Internal'])
class BalanceUpdateView(generics.GenericAPIView):
    """
    Endpoint pour créditer/débiter un wallet.
    Réservé aux admins ou appels systèmes.
    """
    serializer_class = BalanceUpdateSerializer
    permission_classes = [IsAdminUser] # Devrait être IsServiceAccount en prod

    def post(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        try:
            WalletService.update_balance(
                wallet_id=pk,
                amount=data['amount'],
                operation=data['operation'],
                reference=data['reference'],
                description=data.get('description', ''),
                external_transaction_id=data['external_transaction_id']
            )
            return Response({'message': 'Solde mis à jour avec succès.'})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
