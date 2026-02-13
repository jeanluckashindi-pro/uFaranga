"""
Authentification par clé API pour les développeurs
"""
from rest_framework import authentication, exceptions
from django.utils import timezone
from .models import CleAPI, LogUtilisationAPI
import logging

logger = logging.getLogger(__name__)


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Authentification par clé API dans le header:
    Authorization: ApiKey ufar_test_xxxxxxxxxxxxx
    ou
    X-API-Key: ufar_test_xxxxxxxxxxxxx
    """
    
    keyword = 'ApiKey'
    
    def authenticate(self, request):
        # Essayer d'abord le header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith(f'{self.keyword} '):
            api_key = auth_header[len(self.keyword) + 1:]
        else:
            # Essayer le header X-API-Key
            api_key = request.META.get('HTTP_X_API_KEY', '')
        
        if not api_key:
            return None  # Pas de clé API fournie, passer à l'authentification suivante
        
        return self.authenticate_credentials(api_key, request)
    
    def authenticate_credentials(self, key, request):
        """Valide la clé API"""
        try:
            # Récupérer la clé par son hash
            cle_hash = CleAPI.hasher_cle(key)
            cle_api = CleAPI.objects.select_related('compte_developpeur').get(
                hash_cle=cle_hash
            )
        except CleAPI.DoesNotExist:
            raise exceptions.AuthenticationFailed('Clé API invalide')
        
        # Vérifier si la clé est valide
        if not cle_api.est_valide():
            raison = []
            if not cle_api.est_active:
                raison.append('clé désactivée')
            if cle_api.est_revoquee:
                raison.append('clé révoquée')
            if cle_api.date_expiration and cle_api.date_expiration < timezone.now():
                raison.append('clé expirée')
            if not cle_api.compte_developpeur.est_actif():
                raison.append('compte développeur inactif')
            
            raise exceptions.AuthenticationFailed(
                f'Clé API non valide: {", ".join(raison)}'
            )
        
        # Vérifier les restrictions IP si configurées
        if cle_api.adresses_ip_autorisees:
            ip_client = self.get_client_ip(request)
            if ip_client not in cle_api.adresses_ip_autorisees:
                logger.warning(
                    f'Tentative d\'accès depuis IP non autorisée: {ip_client} '
                    f'pour la clé {cle_api.prefixe_cle}***'
                )
                raise exceptions.AuthenticationFailed(
                    'Votre adresse IP n\'est pas autorisée pour cette clé API'
                )
        
        # Mettre à jour la dernière utilisation
        cle_api.derniere_utilisation = timezone.now()
        cle_api.nombre_utilisations += 1
        cle_api.save(update_fields=['derniere_utilisation', 'nombre_utilisations'])
        
        # Retourner un objet user-like avec les infos du développeur
        return (DeveloperUser(cle_api), cle_api)
    
    def authenticate_header(self, request):
        return self.keyword
    
    @staticmethod
    def get_client_ip(request):
        """Récupère l'IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DeveloperUser:
    """
    Objet user-like pour représenter un développeur authentifié par API key
    """
    
    def __init__(self, cle_api):
        self.cle_api = cle_api
        self.compte_developpeur = cle_api.compte_developpeur
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
    
    @property
    def id(self):
        return self.compte_developpeur.id
    
    @property
    def username(self):
        return self.compte_developpeur.courriel_contact
    
    @property
    def email(self):
        return self.compte_developpeur.courriel_contact
    
    def has_perm(self, perm, obj=None):
        """Vérifie si le développeur a une permission (scope)"""
        # Vérifier si le scope est dans la liste des scopes de la clé
        return perm in self.cle_api.scopes or '*' in self.cle_api.scopes
    
    def has_perms(self, perm_list, obj=None):
        """Vérifie plusieurs permissions"""
        return all(self.has_perm(perm, obj) for perm in perm_list)
    
    def has_module_perms(self, app_label):
        """Vérifie les permissions pour un module"""
        return any(scope.startswith(f'{app_label}:') for scope in self.cle_api.scopes)
    
    def __str__(self):
        return f"Developer: {self.compte_developpeur.nom_entreprise}"
