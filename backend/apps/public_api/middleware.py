"""
Middleware pour l'API publique
Logging, géolocalisation, headers de réponse, etc.
"""
from django.utils import timezone
from django.core.cache import cache
from apps.developpeurs.models import LogUtilisationAPI, QuotaUtilisation
from datetime import date
import time
import logging
import geoip2.database
import geoip2.errors
from django.conf import settings

logger = logging.getLogger(__name__)


class APILoggingMiddleware:
    """
    Middleware pour logger toutes les requêtes API
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Ignorer les requêtes non-API
        if not request.path.startswith('/api/public/'):
            return self.get_response(request)
        
        # Enregistrer le temps de début
        start_time = time.time()
        
        # Traiter la requête
        response = self.get_response(request)
        
        # Calculer le temps de réponse
        temps_reponse_ms = int((time.time() - start_time) * 1000)
        
        # Logger la requête si authentifiée par API Key
        if hasattr(request, 'auth') and request.auth is not None:
            self._log_api_request(request, response, temps_reponse_ms)
            self._update_quotas(request, response, temps_reponse_ms)
        
        # Ajouter les headers de quota
        if hasattr(request, 'quota_info'):
            self._add_quota_headers(response, request.quota_info)
        
        return response
    
    def _log_api_request(self, request, response, temps_reponse_ms):
        """Enregistre la requête dans les logs"""
        try:
            cle_api = request.auth
            compte_dev = cle_api.compte_developpeur
            
            # Récupérer les paramètres de query (sanitisés)
            parametres_query = dict(request.GET.items())
            
            # Récupérer l'IP du client
            ip_client = self._get_client_ip(request)
            
            # Créer le log
            LogUtilisationAPI.objects.create(
                cle_api=cle_api,
                compte_developpeur=compte_dev,
                methode_http=request.method,
                endpoint=request.path,
                chemin_complet=request.get_full_path(),
                parametres_query=parametres_query,
                statut_http=response.status_code,
                temps_reponse_ms=temps_reponse_ms,
                taille_reponse_bytes=len(response.content) if hasattr(response, 'content') else 0,
                adresse_ip=ip_client,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500],
                pays=getattr(request, 'country_code', ''),
                metadonnees={
                    'content_type': response.get('Content-Type', ''),
                    'accept': request.META.get('HTTP_ACCEPT', ''),
                }
            )
        except Exception as e:
            logger.error(f"Erreur lors du logging de la requête API: {e}")
    
    def _update_quotas(self, request, response, temps_reponse_ms):
        """Met à jour les quotas et statistiques"""
        try:
            cle_api = request.auth
            compte_dev = cle_api.compte_developpeur
            
            # Mettre à jour le quota du jour
            self._update_quota_periode(
                compte_dev, cle_api, 'JOUR', date.today(),
                response.status_code, temps_reponse_ms,
                len(response.content) if hasattr(response, 'content') else 0
            )
            
            # Mettre à jour le quota du mois
            first_day = date.today().replace(day=1)
            self._update_quota_periode(
                compte_dev, cle_api, 'MOIS', first_day,
                response.status_code, temps_reponse_ms,
                len(response.content) if hasattr(response, 'content') else 0
            )
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des quotas: {e}")
    
    def _update_quota_periode(self, compte_dev, cle_api, type_periode, date_periode, 
                             statut_http, temps_reponse_ms, taille_bytes):
        """Met à jour un quota pour une période donnée"""
        quota, created = QuotaUtilisation.objects.get_or_create(
            compte_developpeur=compte_dev,
            cle_api=cle_api,
            date_periode=date_periode,
            type_periode=type_periode,
            defaults={
                'nombre_requetes': 0,
                'nombre_requetes_succes': 0,
                'nombre_requetes_erreur': 0,
                'requetes_2xx': 0,
                'requetes_4xx': 0,
                'requetes_5xx': 0,
                'temps_reponse_moyen_ms': 0,
                'temps_reponse_max_ms': 0,
                'bande_passante_bytes': 0,
            }
        )
        
        # Incrémenter les compteurs
        quota.nombre_requetes += 1
        
        if 200 <= statut_http < 300:
            quota.nombre_requetes_succes += 1
            quota.requetes_2xx += 1
        elif 400 <= statut_http < 500:
            quota.nombre_requetes_erreur += 1
            quota.requetes_4xx += 1
        elif 500 <= statut_http < 600:
            quota.nombre_requetes_erreur += 1
            quota.requetes_5xx += 1
        
        # Mettre à jour les métriques de performance
        if quota.temps_reponse_moyen_ms == 0:
            quota.temps_reponse_moyen_ms = temps_reponse_ms
        else:
            # Moyenne mobile
            quota.temps_reponse_moyen_ms = int(
                (quota.temps_reponse_moyen_ms * (quota.nombre_requetes - 1) + temps_reponse_ms) 
                / quota.nombre_requetes
            )
        
        if temps_reponse_ms > quota.temps_reponse_max_ms:
            quota.temps_reponse_max_ms = temps_reponse_ms
        
        quota.bande_passante_bytes += taille_bytes
        
        quota.save()
    
    def _add_quota_headers(self, response, quota_info):
        """Ajoute les headers de quota à la réponse"""
        minute_info = quota_info.get('minute', {})
        jour_info = quota_info.get('jour', {})
        
        response['X-RateLimit-Limit-Minute'] = minute_info.get('limit', 0)
        response['X-RateLimit-Remaining-Minute'] = minute_info.get('remaining', 0)
        response['X-RateLimit-Limit-Day'] = jour_info.get('limit', 0)
        response['X-RateLimit-Remaining-Day'] = jour_info.get('remaining', 0)
        
        if not minute_info.get('allowed', True):
            response['Retry-After'] = minute_info.get('wait', 60)
    
    @staticmethod
    def _get_client_ip(request):
        """Récupère l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class GeoLocationMiddleware:
    """
    Middleware pour détecter le pays d'origine de la requête
    Utilise GeoIP2 (nécessite la base de données GeoLite2)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.reader = None
        
        # Charger la base de données GeoIP2 si disponible
        try:
            geoip_db_path = getattr(settings, 'GEOIP_PATH', None)
            if geoip_db_path:
                self.reader = geoip2.database.Reader(geoip_db_path)
        except Exception as e:
            logger.warning(f"GeoIP2 database non disponible: {e}")
    
    def __call__(self, request):
        # Ignorer les requêtes non-API
        if not request.path.startswith('/api/public/'):
            return self.get_response(request)
        
        # Détecter le pays
        if self.reader:
            ip_client = self._get_client_ip(request)
            try:
                response_geo = self.reader.country(ip_client)
                request.country_code = response_geo.country.iso_code
                request.country_name = response_geo.country.name
            except geoip2.errors.AddressNotFoundError:
                request.country_code = None
                request.country_name = None
            except Exception as e:
                logger.error(f"Erreur GeoIP2: {e}")
                request.country_code = None
                request.country_name = None
        else:
            request.country_code = None
            request.country_name = None
        
        return self.get_response(request)
    
    @staticmethod
    def _get_client_ip(request):
        """Récupère l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def __del__(self):
        """Fermer le reader GeoIP2"""
        if self.reader:
            self.reader.close()


class CORSMiddleware:
    """
    Middleware CORS personnalisé pour l'API publique
    Vérifie les domaines autorisés par la clé API
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Ignorer les requêtes non-API
        if not request.path.startswith('/api/public/'):
            return self.get_response(request)
        
        # Traiter la requête
        response = self.get_response(request)
        
        # Ajouter les headers CORS si la clé API a des domaines autorisés
        if hasattr(request, 'auth') and request.auth is not None:
            cle_api = request.auth
            
            if cle_api.domaines_autorises:
                origin = request.META.get('HTTP_ORIGIN', '')
                
                if origin in cle_api.domaines_autorises or '*' in cle_api.domaines_autorises:
                    response['Access-Control-Allow-Origin'] = origin
                    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
                    response['Access-Control-Allow-Headers'] = 'Authorization, X-API-Key, Content-Type'
                    response['Access-Control-Max-Age'] = '3600'
        
        return response
