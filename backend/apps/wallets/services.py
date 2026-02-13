from django.db import transaction, models
from django.utils import timezone
from decimal import Decimal
from typing import Optional, Dict, Any
import uuid
import logging

from .models import Wallet, WalletTransaction, Currency, ExchangeRate, WalletLimit

logger = logging.getLogger(__name__)


class WalletService:
    """Service pour la gestion des wallets"""
    
    @staticmethod
    def create_wallet(user_id: uuid.UUID, currency_code: str, wallet_type: str = 'PERSONAL', 
                     name: str = '', description: str = '') -> Wallet:
        """Créer un nouveau wallet pour un utilisateur"""
        try:
            currency = Currency.objects.get(code=currency_code, is_active=True)
            
            wallet = Wallet.objects.create(
                user_id=user_id,
                currency=currency,
                wallet_type=wallet_type,
                name=name or f"{wallet_type.title()} Wallet",
                description=description
            )
            
            logger.info(f"Wallet created: {wallet.id} for user {user_id}")
            return wallet
            
        except Currency.DoesNotExist:
            raise ValueError(f"Currency {currency_code} not found or inactive")
    
    @staticmethod
    def get_user_wallets(user_id: uuid.UUID, currency_code: str = None) -> models.QuerySet:
        """Récupérer les wallets d'un utilisateur"""
        queryset = Wallet.objects.filter(user_id=user_id).select_related('currency')
        
        if currency_code:
            queryset = queryset.filter(currency__code=currency_code)
        
        return queryset.order_by('-created_at')
    
    @staticmethod
    def get_wallet_balance(wallet_id: uuid.UUID) -> Dict[str, Any]:
        """Récupérer le solde d'un wallet"""
        try:
            wallet = Wallet.objects.select_related('currency').get(id=wallet_id)
            return {
                'wallet_id': wallet.id,
                'balance': wallet.balance,
                'currency': wallet.currency.code,
                'currency_symbol': wallet.currency.symbol,
                'formatted_balance': f"{wallet.currency.symbol}{wallet.balance}",
                'last_updated': wallet.updated_at
            }
        except Wallet.DoesNotExist:
            raise ValueError(f"Wallet {wallet_id} not found")
    
    @staticmethod
    @transaction.atomic
    def update_balance(wallet_id: uuid.UUID, amount: Decimal, operation: str,
                      reference: str, description: str = '', 
                      external_transaction_id: uuid.UUID = None) -> WalletTransaction:
        """Mettre à jour le solde d'un wallet"""
        
        if operation not in ['CREDIT', 'DEBIT']:
            raise ValueError("Operation must be CREDIT or DEBIT")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        try:
            wallet = Wallet.objects.select_for_update().get(id=wallet_id)
            
            if not wallet.is_active:
                raise ValueError("Wallet is not active")
            
            balance_before = wallet.balance
            
            if operation == 'CREDIT':
                if not wallet.can_credit(amount):
                    raise ValueError("Cannot credit this wallet")
                wallet.balance += amount
            else:  # DEBIT
                if not wallet.can_debit(amount):
                    raise ValueError("Insufficient balance or wallet cannot be debited")
                wallet.balance -= amount
            
            balance_after = wallet.balance
            wallet.last_transaction_at = timezone.now()
            wallet.save()
            
            # Créer l'enregistrement de transaction
            wallet_transaction = WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type=operation,
                amount=amount,
                balance_before=balance_before,
                balance_after=balance_after,
                external_transaction_id=external_transaction_id or uuid.uuid4(),
                reference=reference,
                description=description
            )
            
            logger.info(f"Balance updated: {wallet.id} - {operation} {amount} - New balance: {balance_after}")
            return wallet_transaction
            
        except Wallet.DoesNotExist:
            raise ValueError(f"Wallet {wallet_id} not found")
    
    @staticmethod
    @transaction.atomic
    def transfer_between_wallets(from_wallet_id: uuid.UUID, to_wallet_id: uuid.UUID,
                                amount: Decimal, description: str = '', 
                                reference: str = None) -> Dict[str, WalletTransaction]:
        """Transférer des fonds entre deux wallets"""
        
        if from_wallet_id == to_wallet_id:
            raise ValueError("Source and destination wallets must be different")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        reference = reference or f"TRANSFER-{uuid.uuid4().hex[:8].upper()}"
        external_transaction_id = uuid.uuid4()
        
        try:
            # Débiter le wallet source
            debit_transaction = WalletService.update_balance(
                wallet_id=from_wallet_id,
                amount=amount,
                operation='DEBIT',
                reference=reference,
                description=f"Transfer to {to_wallet_id}: {description}",
                external_transaction_id=external_transaction_id
            )
            
            # Créditer le wallet destination
            credit_transaction = WalletService.update_balance(
                wallet_id=to_wallet_id,
                amount=amount,
                operation='CREDIT',
                reference=reference,
                description=f"Transfer from {from_wallet_id}: {description}",
                external_transaction_id=external_transaction_id
            )
            
            logger.info(f"Transfer completed: {from_wallet_id} -> {to_wallet_id} - Amount: {amount}")
            
            return {
                'debit_transaction': debit_transaction,
                'credit_transaction': credit_transaction
            }
            
        except Exception as e:
            logger.error(f"Transfer failed: {from_wallet_id} -> {to_wallet_id} - Error: {str(e)}")
            raise


class CurrencyService:
    """Service pour la gestion des devises"""
    
    @staticmethod
    def get_active_currencies() -> models.QuerySet:
        """Récupérer toutes les devises actives"""
        return Currency.objects.filter(is_active=True).order_by('code')
    
    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[ExchangeRate]:
        """Récupérer le taux de change entre deux devises"""
        if from_currency == to_currency:
            return None
        
        now = timezone.now()
        return ExchangeRate.objects.filter(
            from_currency__code=from_currency,
            to_currency__code=to_currency,
            is_active=True,
            valid_from__lte=now
        ).filter(
            models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=now)
        ).first()
    
    @staticmethod
    def convert_currency(amount: Decimal, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Convertir un montant d'une devise à une autre"""
        if from_currency == to_currency:
            return {
                'original_amount': amount,
                'converted_amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'exchange_rate': Decimal('1.0'),
                'conversion_date': timezone.now()
            }
        
        exchange_rate = CurrencyService.get_exchange_rate(from_currency, to_currency)
        
        if not exchange_rate:
            raise ValueError(f"Exchange rate not found: {from_currency} -> {to_currency}")
        
        converted_amount = exchange_rate.convert_amount(amount)
        
        return {
            'original_amount': amount,
            'converted_amount': converted_amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': exchange_rate.rate,
            'conversion_date': timezone.now()
        }


class WalletLimitService:
    """Service pour la gestion des limites de wallet"""
    
    @staticmethod
    def check_limits(wallet_id: uuid.UUID, amount: Decimal, operation: str = 'DEBIT') -> Dict[str, Any]:
        """Vérifier si une opération respecte les limites du wallet"""
        
        if operation != 'DEBIT':
            return {'can_proceed': True, 'message': 'No limits for credit operations'}
        
        now = timezone.now()
        active_limits = WalletLimit.objects.filter(
            wallet_id=wallet_id,
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )
        
        violations = []
        
        for limit in active_limits:
            if limit.used_amount + amount > limit.amount:
                violations.append({
                    'limit_type': limit.limit_type,
                    'limit_amount': limit.amount,
                    'used_amount': limit.used_amount,
                    'requested_amount': amount,
                    'remaining_amount': limit.remaining_amount
                })
        
        return {
            'can_proceed': len(violations) == 0,
            'violations': violations,
            'message': 'Limit exceeded' if violations else 'Within limits'
        }
    
    @staticmethod
    @transaction.atomic
    def update_limit_usage(wallet_id: uuid.UUID, amount: Decimal, operation: str = 'DEBIT'):
        """Mettre à jour l'utilisation des limites après une transaction"""
        
        if operation != 'DEBIT':
            return
        
        now = timezone.now()
        active_limits = WalletLimit.objects.filter(
            wallet_id=wallet_id,
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )
        
        for limit in active_limits:
            limit.used_amount += amount
            limit.save()
        
        logger.info(f"Limit usage updated for wallet {wallet_id} - Amount: {amount}")
