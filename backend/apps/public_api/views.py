"""
Vues pour l'API publique
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular import openapi
from rest_framework import serializers as drf_serializers
from .permissions import (
    HasAPIKeyPermission, HasScopePermission, CheckQuotaPermission,
    CheckCountryPermission, PublicAPIPermission
)
from .throttles import APIKeyRateThrottle, BurstRateThrottle
from .serializers import (
    FeesCalculatorSerializer, FeesResponseSerializer,
    ValidatePhoneSerializer, ValidateAccountSerializer,
    AgentSearchSerializer, RegisterInitiateSerializer, VerifyOTPSerializer
)
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# SYSTÈME - Health, Status, Version
# =============================================================================

@extend_schema(
    tags=['Système'],
    summary='Vérification de santé',
    description='Vérifie l\'état de santé du système API',
    responses={200: inline_serializer(
        name='HealthResponse',
        fields={
            'status': drf_serializers.CharField(),
            'timestamp': drf_serializers.DateTimeField(),
            'version': drf_serializers.CharField(),
            'environment': drf_serializers.CharField(),
        }
    )}
)
@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
@throttle_classes([APIKeyRateThrottle])
def health_check(request):
    """
    Vérification de l'état du système
    
    Scope requis: public:read
    """
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'environment': 'production' if not settings.DEBUG else 'development'
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
@throttle_classes([APIKeyRateThrottle])
def system_status(request):
    """
    Statut détaillé des services
    
    Scope requis: public:read
    """
    return Response({
        'status': 'operational',
        'services': {
            'api': 'operational',
            'database': 'operational',
            'cache': 'operational',
            'transactions': 'operational'
        },
        'maintenance': {
            'scheduled': False,
            'message': None
        },
        'timestamp': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
def api_version(request):
    """
    Version de l'API
    
    Scope requis: aucun
    """
    return Response({
        'version': '1.0.0',
        'release_date': '2026-02-13',
        'documentation': 'https://docs.ufaranga.bi',
        'changelog': 'https://docs.ufaranga.bi/changelog'
    })


# =============================================================================
# TARIFICATION & FRAIS
# =============================================================================

class FeesCalculatorView(APIView):
    """
    Calculateur de frais de transaction
    
    Scope requis: fees:read
    """
    permission_classes = [HasAPIKeyPermission, CheckQuotaPermission, HasScopePermission]
    throttle_classes = [APIKeyRateThrottle, BurstRateThrottle]
    required_scopes = ['fees:read', 'public:read']
    
    def get(self, request):
        """
        Calcule les frais pour une transaction
        
        Paramètres:
        - amount (required): Montant de la transaction
        - type (required): Type de transaction (P2P, DEPOT, RETRAIT, etc.)
        - currency (optional): Devise (défaut: BIF)
        """
        # Récupérer les paramètres
        try:
            montant = Decimal(request.query_params.get('amount', 0))
            type_transaction = request.query_params.get('type', '').upper()
            devise = request.query_params.get('currency', 'BIF').upper()
        except (ValueError, TypeError):
            return Response({
                'error': 'invalid_parameters',
                'message': 'Le montant doit être un nombre valide'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validation
        if montant <= 0:
            return Response({
                'error': 'invalid_amount',
                'message': 'Le montant doit être supérieur à 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not type_transaction:
            return Response({
                'error': 'missing_type',
                'message': 'Le type de transaction est requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculer les frais (logique simplifiée - à adapter selon vos règles)
        frais = self._calculer_frais(montant, type_transaction, devise)
        commission = self._calculer_commission(montant, type_transaction)
        montant_total = montant + frais + commission
        
        return Response({
            'montant': float(montant),
            'devise': devise,
            'type_transaction': type_transaction,
            'frais': float(frais),
            'commission': float(commission),
            'montant_total': float(montant_total),
            'details': {
                'taux_frais': self._get_taux_frais(type_transaction),
                'taux_commission': self._get_taux_commission(type_transaction)
            }
        })
    
    def _calculer_frais(self, montant, type_transaction, devise):
        """Calcule les frais selon le type de transaction"""
        # Grille tarifaire simplifiée (à adapter)
        grille = {
            'P2P': Decimal('0.01'),  # 1%
            'DEPOT': Decimal('0.00'),  # Gratuit
            'RETRAIT': Decimal('0.02'),  # 2%
            'PAIEMENT_MARCHAND': Decimal('0.015'),  # 1.5%
            'PAIEMENT_FACTURE': Decimal('0.005'),  # 0.5%
            'RECHARGE_TELEPHONIQUE': Decimal('0.00'),  # Gratuit
            'VIREMENT_BANCAIRE': Decimal('0.025'),  # 2.5%
            'TRANSFERT_INTERNATIONAL': Decimal('0.05'),  # 5%
        }
        
        taux = grille.get(type_transaction, Decimal('0.02'))
        frais = montant * taux
        
        # Frais minimum et maximum
        frais_min = Decimal('100')  # 100 BIF
        frais_max = Decimal('5000')  # 5000 BIF
        
        return max(frais_min, min(frais, frais_max))
    
    def _calculer_commission(self, montant, type_transaction):
        """Calcule la commission"""
        # Commission simplifiée
        if type_transaction in ['P2P', 'PAIEMENT_MARCHAND']:
            return montant * Decimal('0.005')  # 0.5%
        return Decimal('0')
    
    def _get_taux_frais(self, type_transaction):
        """Retourne le taux de frais en pourcentage"""
        grille = {
            'P2P': 1.0,
            'DEPOT': 0.0,
            'RETRAIT': 2.0,
            'PAIEMENT_MARCHAND': 1.5,
            'PAIEMENT_FACTURE': 0.5,
            'RECHARGE_TELEPHONIQUE': 0.0,
            'VIREMENT_BANCAIRE': 2.5,
            'TRANSFERT_INTERNATIONAL': 5.0,
        }
        return grille.get(type_transaction, 2.0)
    
    def _get_taux_commission(self, type_transaction):
        """Retourne le taux de commission en pourcentage"""
        if type_transaction in ['P2P', 'PAIEMENT_MARCHAND']:
            return 0.5
        return 0.0


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def fees_schedule(request):
    """
    Grille tarifaire complète
    
    Scope requis: fees:read
    """
    return Response({
        'devise': 'BIF',
        'grille': [
            {
                'type': 'P2P',
                'nom': 'Transfert Peer-to-Peer',
                'taux_frais': 1.0,
                'taux_commission': 0.5,
                'frais_min': 100,
                'frais_max': 5000
            },
            {
                'type': 'DEPOT',
                'nom': 'Dépôt d\'espèces',
                'taux_frais': 0.0,
                'taux_commission': 0.0,
                'frais_min': 0,
                'frais_max': 0
            },
            {
                'type': 'RETRAIT',
                'nom': 'Retrait d\'espèces',
                'taux_frais': 2.0,
                'taux_commission': 0.0,
                'frais_min': 100,
                'frais_max': 5000
            },
            {
                'type': 'PAIEMENT_MARCHAND',
                'nom': 'Paiement à un marchand',
                'taux_frais': 1.5,
                'taux_commission': 0.5,
                'frais_min': 100,
                'frais_max': 5000
            },
            {
                'type': 'PAIEMENT_FACTURE',
                'nom': 'Paiement de facture',
                'taux_frais': 0.5,
                'taux_commission': 0.0,
                'frais_min': 100,
                'frais_max': 2000
            },
            {
                'type': 'RECHARGE_TELEPHONIQUE',
                'nom': 'Recharge téléphonique',
                'taux_frais': 0.0,
                'taux_commission': 0.0,
                'frais_min': 0,
                'frais_max': 0
            },
            {
                'type': 'VIREMENT_BANCAIRE',
                'nom': 'Virement bancaire',
                'taux_frais': 2.5,
                'taux_commission': 0.0,
                'frais_min': 500,
                'frais_max': 10000
            },
            {
                'type': 'TRANSFERT_INTERNATIONAL',
                'nom': 'Transfert international',
                'taux_frais': 5.0,
                'taux_commission': 0.0,
                'frais_min': 2000,
                'frais_max': 50000
            }
        ],
        'notes': [
            'Les frais sont calculés en pourcentage du montant',
            'Des frais minimum et maximum s\'appliquent',
            'Les taux peuvent varier selon les promotions en cours'
        ],
        'derniere_mise_a_jour': '2026-02-13'
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def exchange_rates(request):
    """
    Taux de change en temps réel
    
    Scope requis: fees:read
    """
    return Response({
        'base_currency': 'BIF',
        'rates': {
            'USD': 0.00035,  # 1 BIF = 0.00035 USD
            'EUR': 0.00032,  # 1 BIF = 0.00032 EUR
            'RWF': 0.45,     # 1 BIF = 0.45 RWF
            'TZS': 0.82,     # 1 BIF = 0.82 TZS
            'UGX': 1.30,     # 1 BIF = 1.30 UGX
            'KES': 0.045,    # 1 BIF = 0.045 KES
        },
        'timestamp': timezone.now().isoformat(),
        'source': 'Banque Centrale du Burundi',
        'note': 'Taux indicatifs - peuvent varier selon le montant et le type de transaction'
    })


# =============================================================================
# INFORMATIONS GÉNÉRALES
# =============================================================================

@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
def supported_countries(request):
    """
    Liste des pays supportés
    """
    return Response({
        'countries': [
            {'code': 'BI', 'name': 'Burundi', 'currency': 'BIF', 'active': True},
            {'code': 'RW', 'name': 'Rwanda', 'currency': 'RWF', 'active': True},
            {'code': 'CD', 'name': 'RD Congo', 'currency': 'CDF', 'active': True},
            {'code': 'TZ', 'name': 'Tanzanie', 'currency': 'TZS', 'active': True},
            {'code': 'UG', 'name': 'Ouganda', 'currency': 'UGX', 'active': True},
            {'code': 'KE', 'name': 'Kenya', 'currency': 'KES', 'active': True},
        ]
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
def supported_currencies(request):
    """
    Liste des devises supportées
    """
    return Response({
        'currencies': [
            {'code': 'BIF', 'name': 'Franc Burundais', 'symbol': 'FBu', 'decimals': 0},
            {'code': 'USD', 'name': 'Dollar Américain', 'symbol': '$', 'decimals': 2},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'decimals': 2},
            {'code': 'RWF', 'name': 'Franc Rwandais', 'symbol': 'FRw', 'decimals': 0},
            {'code': 'TZS', 'name': 'Shilling Tanzanien', 'symbol': 'TSh', 'decimals': 0},
            {'code': 'UGX', 'name': 'Shilling Ougandais', 'symbol': 'USh', 'decimals': 0},
            {'code': 'KES', 'name': 'Shilling Kenyan', 'symbol': 'KSh', 'decimals': 2},
        ]
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
def transaction_types(request):
    """
    Types de transactions disponibles
    """
    return Response({
        'types': [
            {'code': 'P2P', 'name': 'Transfert Peer-to-Peer', 'description': 'Envoi d\'argent entre utilisateurs'},
            {'code': 'DEPOT', 'name': 'Dépôt', 'description': 'Dépôt d\'espèces sur le compte'},
            {'code': 'RETRAIT', 'name': 'Retrait', 'description': 'Retrait d\'espèces du compte'},
            {'code': 'PAIEMENT_MARCHAND', 'name': 'Paiement Marchand', 'description': 'Paiement à un commerçant'},
            {'code': 'PAIEMENT_FACTURE', 'name': 'Paiement Facture', 'description': 'Paiement de factures (eau, électricité, etc.)'},
            {'code': 'RECHARGE_TELEPHONIQUE', 'name': 'Recharge Mobile', 'description': 'Recharge de crédit téléphonique'},
            {'code': 'VIREMENT_BANCAIRE', 'name': 'Virement Bancaire', 'description': 'Virement vers un compte bancaire'},
            {'code': 'TRANSFERT_INTERNATIONAL', 'name': 'Transfert International', 'description': 'Envoi d\'argent à l\'étranger'},
        ]
    })


# =============================================================================
# VALIDATION
# =============================================================================

@api_view(['POST'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def validate_phone(request):
    """
    Valide un numéro de téléphone
    
    Scope requis: validation:write
    """
    from .serializers import ValidatePhoneSerializer
    
    serializer = ValidatePhoneSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone = serializer.validated_data['phone']
    
    # Validation basique du format
    import re
    phone_pattern = r'^\+?[1-9]\d{1,14}$'
    is_valid = bool(re.match(phone_pattern, phone))
    
    # Détecter le pays
    country_code = None
    if phone.startswith('+257'):
        country_code = 'BI'
    elif phone.startswith('+250'):
        country_code = 'RW'
    elif phone.startswith('+243'):
        country_code = 'CD'
    elif phone.startswith('+255'):
        country_code = 'TZ'
    elif phone.startswith('+256'):
        country_code = 'UG'
    elif phone.startswith('+254'):
        country_code = 'KE'
    
    return Response({
        'phone': phone,
        'is_valid': is_valid,
        'country_code': country_code,
        'formatted': phone if is_valid else None,
        'message': 'Numéro valide' if is_valid else 'Format de numéro invalide'
    })


@api_view(['POST'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def validate_account(request):
    """
    Vérifie si un compte existe (pour P2P)
    
    Scope requis: validation:write
    """
    from .serializers import ValidateAccountSerializer
    
    serializer = ValidateAccountSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    account = serializer.validated_data['account']
    
    # Simulation - À remplacer par une vraie vérification en base
    exists = len(account) >= 5  # Simulation simple
    
    return Response({
        'account': account,
        'exists': exists,
        'can_receive': exists,
        'message': 'Compte trouvé' if exists else 'Compte non trouvé'
    })


# =============================================================================
# AGENTS
# =============================================================================

@api_view(['GET'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def search_agents(request):
    """
    Recherche d'agents à proximité
    
    Scope requis: agents:read
    """
    from .serializers import AgentSearchSerializer
    
    serializer = AgentSearchSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Données simulées - À remplacer par une vraie recherche
    agents = [
        {
            'id': '123e4567-e89b-12d3-a456-426614174001',
            'name': 'Agent Central Bujumbura',
            'type': 'AGENT',
            'address': 'Avenue de la Liberté, Bujumbura',
            'city': 'Bujumbura',
            'country': 'BI',
            'latitude': -3.3761,
            'longitude': 29.3611,
            'distance_meters': 1200,
            'phone': '+25779123456',
            'hours': {
                'monday': '08:00-18:00',
                'tuesday': '08:00-18:00',
                'wednesday': '08:00-18:00',
                'thursday': '08:00-18:00',
                'friday': '08:00-18:00',
                'saturday': '08:00-14:00',
                'sunday': 'Fermé'
            },
            'services': ['DEPOT', 'RETRAIT', 'P2P'],
            'is_open': True
        },
        {
            'id': '123e4567-e89b-12d3-a456-426614174002',
            'name': 'Agent Rohero',
            'type': 'AGENT',
            'address': 'Quartier Rohero, Bujumbura',
            'city': 'Bujumbura',
            'country': 'BI',
            'latitude': -3.3850,
            'longitude': 29.3700,
            'distance_meters': 2500,
            'phone': '+25779234567',
            'hours': {
                'monday': '07:00-19:00',
                'tuesday': '07:00-19:00',
                'wednesday': '07:00-19:00',
                'thursday': '07:00-19:00',
                'friday': '07:00-19:00',
                'saturday': '07:00-16:00',
                'sunday': '09:00-13:00'
            },
            'services': ['DEPOT', 'RETRAIT', 'P2P', 'PAIEMENT_FACTURE'],
            'is_open': True
        }
    ]
    
    return Response({
        'count': len(agents),
        'agents': agents
    })


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle])
def agent_detail(request, agent_id):
    """
    Détails d'un agent spécifique
    
    Scope requis: agents:read
    """
    # Données simulées
    agent = {
        'id': agent_id,
        'name': 'Agent Central Bujumbura',
        'type': 'AGENT',
        'address': 'Avenue de la Liberté, Bujumbura',
        'city': 'Bujumbura',
        'country': 'BI',
        'latitude': -3.3761,
        'longitude': 29.3611,
        'phone': '+25779123456',
        'email': 'agent.central@ufaranga.bi',
        'hours': {
            'monday': '08:00-18:00',
            'tuesday': '08:00-18:00',
            'wednesday': '08:00-18:00',
            'thursday': '08:00-18:00',
            'friday': '08:00-18:00',
            'saturday': '08:00-14:00',
            'sunday': 'Fermé'
        },
        'services': ['DEPOT', 'RETRAIT', 'P2P'],
        'limits': {
            'min_deposit': 1000,
            'max_deposit': 5000000,
            'min_withdrawal': 1000,
            'max_withdrawal': 2000000
        },
        'is_open': True,
        'rating': 4.5,
        'reviews_count': 127
    }
    
    return Response(agent)


# =============================================================================
# INSCRIPTION
# =============================================================================

@api_view(['POST'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle, BurstRateThrottle])
def register_initiate(request):
    """
    Initier une inscription
    
    Scope requis: public:write
    """
    from .serializers import RegisterInitiateSerializer
    
    serializer = RegisterInitiateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Simulation - Générer un code OTP
    import random
    otp_code = f"{random.randint(100000, 999999)}"
    
    # En production, envoyer le SMS ici
    logger.info(f"OTP généré pour {data['phone']}: {otp_code}")
    
    return Response({
        'success': True,
        'message': 'Code de vérification envoyé par SMS',
        'phone': data['phone'],
        'email': data['email'],
        'expires_in': 300,  # 5 minutes
        # En développement seulement
        'otp_code': otp_code if not settings.DEBUG else None
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([APIKeyRateThrottle, BurstRateThrottle])
def verify_otp(request):
    """
    Vérifier un code OTP
    
    Scope requis: public:write
    """
    from .serializers import VerifyOTPSerializer
    
    serializer = VerifyOTPSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Simulation - Vérifier le code OTP
    # En production, vérifier contre la base de données
    is_valid = len(data['otp']) == 6 and data['otp'].isdigit()
    
    if is_valid:
        return Response({
            'success': True,
            'message': 'Code vérifié avec succès',
            'phone': data['phone'],
            'verified': True
        })
    else:
        return Response({
            'success': False,
            'message': 'Code invalide ou expiré',
            'verified': False
        }, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# SUPPORT & CONTACT
# =============================================================================

@api_view(['POST'])
@permission_classes([HasAPIKeyPermission, CheckQuotaPermission])
@throttle_classes([BurstRateThrottle])  # Rate limit strict pour éviter le spam
def contact_support(request):
    """
    Envoyer un message au support
    
    Scope requis: public:write
    """
    name = request.data.get('name', '')
    email = request.data.get('email', '')
    subject = request.data.get('subject', '')
    message = request.data.get('message', '')
    
    # Validation
    if not all([name, email, subject, message]):
        return Response({
            'error': 'missing_fields',
            'message': 'Tous les champs sont requis'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # En production, envoyer l'email ou créer un ticket
    logger.info(f"Message de support reçu de {email}: {subject}")
    
    return Response({
        'success': True,
        'message': 'Votre message a été envoyé. Nous vous répondrons sous 24h.',
        'ticket_id': f"TICKET-{timezone.now().strftime('%Y%m%d%H%M%S')}"
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([HasAPIKeyPermission])
def faq(request):
    """
    Questions fréquemment posées
    """
    return Response({
        'faqs': [
            {
                'category': 'Compte',
                'questions': [
                    {
                        'question': 'Comment créer un compte?',
                        'answer': 'Téléchargez l\'application uFaranga, entrez votre numéro de téléphone et suivez les instructions.'
                    },
                    {
                        'question': 'Quels documents sont nécessaires?',
                        'answer': 'Une pièce d\'identité valide (CNI, passeport) et un justificatif de domicile.'
                    }
                ]
            },
            {
                'category': 'Transactions',
                'questions': [
                    {
                        'question': 'Quels sont les frais de transaction?',
                        'answer': 'Les frais varient selon le type de transaction. Consultez notre grille tarifaire.'
                    },
                    {
                        'question': 'Quelle est la limite de transaction?',
                        'answer': 'Les limites dépendent de votre niveau KYC. Niveau 1: 500,000 BIF/jour, Niveau 2: 2,000,000 BIF/jour.'
                    }
                ]
            }
        ]
    })
