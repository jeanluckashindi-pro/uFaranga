"""
Throttles (Rate Limiting) pour l'API publique
"""
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from apps.developpeurs.models import QuotaUtilisation
from datetime import date
import logging

logger = logging.getLogger(__name__)


class APIKeyRateThrottle(BaseThrottle):
    """
    Rate limiting basé sur la clé API
    Utilise les limites configurées pour chaque clé/compte
    """
    
    def allow_request(self, request, view):
        # Ignorer si pas de clé API
        if not hasattr(request, 'auth') or request.auth is None:
            return True
        
        cle_api = request.auth
        compte_dev = cle_api.compte_developpeur
        
        # Vérifier le rate limit par minute
        return self._check_rate_limit(cle_api, compte_dev)
    
    def _check_rate_limit(self, cle_api, compte_dev):
        """Vérifie le rate limit par minute"""
        # Utiliser la limite de la clé si définie, sinon celle du compte
        limite = cle_api.limite_requetes_minute or compte_dev.limite_taux_par_minute
        
        # Clé de cache unique
        cache_key = f"throttle:api_key:{cle_api.id}:minute"
        
        # Récupérer le compteur actuel
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limite:
            # Rate limit dépassé
            self.wait = self._get_wait_time(cache_key)
            return False
        
        # Incrémenter le compteur (expire après 60 secondes)
        cache.set(cache_key, current_count + 1, 60)
        
        return True
    
    def _get_wait_time(self, cache_key):
        """Récupère le temps d'attente avant la prochaine requête"""
        ttl = cache.ttl(cache_key)
        return ttl if ttl > 0 else 60
    
    def wait(self):
        """Retourne le temps d'attente en secondes"""
        return getattr(self, 'wait', None)


class DailyQuotaThrottle(BaseThrottle):
    """
    Throttle basé sur le quota journalier
    """
    
    def allow_request(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return True
        
        cle_api = request.auth
        compte_dev = cle_api.compte_developpeur
        
        # Récupérer la limite
        limite = cle_api.limite_requetes_jour or compte_dev.quota_requetes_jour
        
        # Récupérer le quota du jour
        today = date.today()
        try:
            quota = QuotaUtilisation.objects.get(
                compte_developpeur=compte_dev,
                cle_api=cle_api,
                date_periode=today,
                type_periode='JOUR'
            )
            
            if quota.nombre_requetes >= limite:
                return False
        except QuotaUtilisation.DoesNotExist:
            # Pas encore de quota pour aujourd'hui, autoriser
            pass
        
        return True
    
    def wait(self):
        """Temps d'attente jusqu'à minuit"""
        from datetime import datetime, timedelta
        now = datetime.now()
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return int((midnight - now).total_seconds())


class MonthlyQuotaThrottle(BaseThrottle):
    """
    Throttle basé sur le quota mensuel
    """
    
    def allow_request(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return True
        
        cle_api = request.auth
        compte_dev = cle_api.compte_developpeur
        
        # Récupérer la limite
        limite = compte_dev.quota_requetes_mois
        
        # Premier jour du mois
        today = date.today()
        first_day = today.replace(day=1)
        
        try:
            quota = QuotaUtilisation.objects.get(
                compte_developpeur=compte_dev,
                cle_api=cle_api,
                date_periode=first_day,
                type_periode='MOIS'
            )
            
            if quota.nombre_requetes >= limite:
                return False
        except QuotaUtilisation.DoesNotExist:
            # Pas encore de quota pour ce mois, autoriser
            pass
        
        return True
    
    def wait(self):
        """Temps d'attente jusqu'au début du mois prochain"""
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        now = datetime.now()
        next_month = (now + relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return int((next_month - now).total_seconds())


class BurstRateThrottle(BaseThrottle):
    """
    Throttle pour limiter les rafales de requêtes
    Permet un burst court mais limite sur une fenêtre plus longue
    """
    
    BURST_LIMIT = 10  # 10 requêtes
    BURST_WINDOW = 10  # en 10 secondes
    
    def allow_request(self, request, view):
        if not hasattr(request, 'auth') or request.auth is None:
            return True
        
        cle_api = request.auth
        
        # Clé de cache pour le burst
        cache_key = f"throttle:burst:{cle_api.id}"
        
        # Récupérer le compteur
        current_count = cache.get(cache_key, 0)
        
        if current_count >= self.BURST_LIMIT:
            self.wait = self._get_wait_time(cache_key)
            return False
        
        # Incrémenter
        cache.set(cache_key, current_count + 1, self.BURST_WINDOW)
        
        return True
    
    def _get_wait_time(self, cache_key):
        """Récupère le temps d'attente"""
        ttl = cache.ttl(cache_key)
        return ttl if ttl > 0 else self.BURST_WINDOW
    
    def wait(self):
        return getattr(self, 'wait', None)
