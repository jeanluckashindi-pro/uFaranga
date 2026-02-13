"""
Permissions pour l'API publique
Vérifie les scopes, quotas, pays autorisés, etc.
"""
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, Throttled
from django.utils import timezone
from django.core.cache import cache
from apps.developpeurs.models import QuotaUtilisation, LogUtilisationAPI
from datetime import date, timedelta
import logging

logger = logging.getLogger(__name__)


class HasAPIKeyPermission(permissions.BasePermission):
    """
    Permission de base: vérifie qu'une clé API valide est fournie
    """
    message = "Une clé API valide est requise pour accéder à cet endpoint"
    
    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est authentifié via API Key
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        # request.auth contient l'objet CleAPI
        cle_api = request.auth
        
        # Vérifier que la clé est valide
        if not cle_api.est_valide():
            self.message = "Votre clé API n'est plus valide"
            return False
        
        return True


class HasScopePermission(permissions.BasePermission):
    """
    Vérifie que la clé API a le scope requis
    Usage dans la vue: required_scopes = ['public:read', 'fees:read']
    """
    
    def has_permission(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        cle_api = request.auth
        required_scopes = getattr(view, 'required_scopes', [])
        
        # Si aucun scope requis, autoriser
        if not required_scopes:
            return True
        
        # Vérifier si la clé a le scope wildcard
        if '*' in cle_api.scopes:
            return True
        
        # Vérifier si la clé a au moins un des scopes requis
        for scope in required_scopes:
            if scope in cle_api.scopes:
                return True
        
        self.message = f"Scope requis: {', '.join(required_scopes)}"
        return False


class CheckQuotaPermission(permissions.BasePermission):
    """
    Vérifie que le développeur n'a pas dépassé ses quotas
    """
    
    def has_permission(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        cle_api = request.auth
        compte_dev = cle_api.compte_developpeur
        
        # Vérifier quota par minute (via cache)
        quota_minute = self._check_quota_minute(cle_api, compte_dev)
        if not quota_minute['allowed']:
            raise Throttled(
                detail=f"Quota par minute dépassé. Limite: {quota_minute['limit']}/minute",
                wait=quota_minute['wait']
            )
        
        # Vérifier quota par jour
        quota_jour = self._check_quota_jour(cle_api, compte_dev)
        if not quota_jour['allowed']:
            raise Throttled(
                detail=f"Quota journalier dépassé. Limite: {quota_jour['limit']}/jour"
            )
        
        # Vérifier quota par mois
        quota_mois = self._check_quota_mois(cle_api, compte_dev)
        if not quota_mois['allowed']:
            raise Throttled(
                detail=f"Quota mensuel dépassé. Limite: {quota_mois['limit']}/mois"
            )
        
        # Ajouter les infos de quota dans la requête pour les headers de réponse
        request.quota_info = {
            'minute': quota_minute,
            'jour': quota_jour,
            'mois': quota_mois
        }
        
        return True
    
    def _check_quota_minute(self, cle_api, compte_dev):
        """Vérifie le quota par minute (via Redis/cache)"""
        # Utiliser la limite de la clé si définie, sinon celle du compte
        limite = cle_api.limite_requetes_minute or compte_dev.limite_taux_par_minute
        
        # Clé de cache unique par clé API
        cache_key = f"api_quota_minute:{cle_api.id}"
        
        # Récupérer le compteur actuel
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limite:
            # Quota dépassé
            ttl = cache.ttl(cache_key) or 60
            return {
                'allowed': False,
                'limit': limite,
                'remaining': 0,
                'wait': ttl
            }
        
        # Incrémenter le compteur (expire après 60 secondes)
        cache.set(cache_key, current_count + 1, 60)
        
        return {
            'allowed': True,
            'limit': limite,
            'remaining': limite - current_count - 1,
            'wait': 0
        }
    
    def _check_quota_jour(self, cle_api, compte_dev):
        """Vérifie le quota par jour"""
        limite = cle_api.limite_requetes_jour or compte_dev.quota_requetes_jour
        
        # Récupérer ou créer le quota du jour
        today = date.today()
        quota, created = QuotaUtilisation.objects.get_or_create(
            compte_developpeur=compte_dev,
            cle_api=cle_api,
            date_periode=today,
            type_periode='JOUR',
            defaults={'nombre_requetes': 0}
        )
        
        if quota.nombre_requetes >= limite:
            return {
                'allowed': False,
                'limit': limite,
                'remaining': 0
            }
        
        return {
            'allowed': True,
            'limit': limite,
            'remaining': limite - quota.nombre_requetes
        }
    
    def _check_quota_mois(self, cle_api, compte_dev):
        """Vérifie le quota par mois"""
        limite = compte_dev.quota_requetes_mois
        
        # Premier jour du mois
        today = date.today()
        first_day = today.replace(day=1)
        
        # Récupérer ou créer le quota du mois
        quota, created = QuotaUtilisation.objects.get_or_create(
            compte_developpeur=compte_dev,
            cle_api=cle_api,
            date_periode=first_day,
            type_periode='MOIS',
            defaults={'nombre_requetes': 0}
        )
        
        if quota.nombre_requetes >= limite:
            return {
                'allowed': False,
                'limit': limite,
                'remaining': 0
            }
        
        return {
            'allowed': True,
            'limit': limite,
            'remaining': limite - quota.nombre_requetes
        }


class CheckCountryPermission(permissions.BasePermission):
    """
    Vérifie que la requête provient d'un pays autorisé
    """
    # Liste des pays autorisés (codes ISO 3166-1 alpha-2)
    ALLOWED_COUNTRIES = [
        'BI',  # Burundi
        'RW',  # Rwanda
        'CD',  # RD Congo
        'TZ',  # Tanzanie
        'UG',  # Ouganda
        'KE',  # Kenya
        # Ajouter d'autres pays selon les besoins
    ]
    
    def has_permission(self, request, view):
        # Récupérer le pays depuis les métadonnées de la requête
        # (peut être défini par un middleware de géolocalisation)
        country_code = getattr(request, 'country_code', None)
        
        # Si le pays n'est pas détecté, on peut soit:
        # 1. Autoriser (mode permissif)
        # 2. Refuser (mode strict)
        # Pour l'instant, mode permissif
        if not country_code:
            logger.warning(f"Pays non détecté pour la requête depuis {request.META.get('REMOTE_ADDR')}")
            return True
        
        # Vérifier si le pays est autorisé
        if country_code not in self.ALLOWED_COUNTRIES:
            self.message = f"Accès non autorisé depuis le pays: {country_code}"
            logger.warning(
                f"Tentative d'accès depuis pays non autorisé: {country_code} "
                f"(IP: {request.META.get('REMOTE_ADDR')})"
            )
            return False
        
        return True


class CheckEnvironmentPermission(permissions.BasePermission):
    """
    Vérifie que la clé API correspond à l'environnement requis
    Usage: required_environment = 'PRODUCTION'
    """
    
    def has_permission(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        cle_api = request.auth
        required_env = getattr(view, 'required_environment', None)
        
        # Si aucun environnement requis, autoriser
        if not required_env:
            return True
        
        # Vérifier l'environnement
        if cle_api.environnement != required_env:
            self.message = f"Cet endpoint nécessite une clé {required_env}"
            return False
        
        return True


class IsProductionKeyPermission(permissions.BasePermission):
    """
    Vérifie que la clé API est une clé de production
    """
    message = "Cet endpoint nécessite une clé de production"
    
    def has_permission(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        cle_api = request.auth
        return cle_api.environnement == 'PRODUCTION'


class IsSandboxKeyPermission(permissions.BasePermission):
    """
    Vérifie que la clé API est une clé sandbox
    """
    message = "Cet endpoint nécessite une clé sandbox"
    
    def has_permission(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return False
        
        cle_api = request.auth
        return cle_api.environnement == 'SANDBOX'


# Combinaisons de permissions courantes
class PublicAPIPermission(permissions.BasePermission):
    """
    Permission complète pour l'API publique:
    - Clé API valide
    - Quotas respectés
    - Pays autorisé
    """
    
    def has_permission(self, request, view):
        # Vérifier toutes les permissions
        checks = [
            HasAPIKeyPermission(),
            CheckQuotaPermission(),
            CheckCountryPermission(),
        ]
        
        for check in checks:
            if not check.has_permission(request, view):
                self.message = check.message
                return False
        
        return True
