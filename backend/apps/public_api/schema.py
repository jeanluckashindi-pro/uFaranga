"""
Configuration OpenAPI/Swagger pour l'API publique
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class APIKeyScheme(OpenApiAuthenticationExtension):
    """
    Extension pour documenter l'authentification par API Key
    """
    target_class = 'apps.developpeurs.authentication.APIKeyAuthentication'
    name = 'ApiKeyAuth'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'API Key authentication. Format: `ApiKey your_api_key_here`'
        }


# Schémas personnalisés pour l'API publique
class PublicAPISchema(AutoSchema):
    """
    Schéma personnalisé pour l'API publique
    Ajoute automatiquement les tags et la documentation
    """
    
    def get_tags(self):
        """Définit les tags basés sur le chemin"""
        path = self.path
        
        if '/sante' in path or '/statut' in path or '/version' in path:
            return ['Système']
        elif '/frais' in path or '/taux-change' in path:
            return ['Tarification']
        elif '/pays' in path or '/devises' in path or '/types-transaction' in path:
            return ['Informations']
        elif '/valider' in path:
            return ['Validation']
        elif '/agents' in path:
            return ['Agents']
        elif '/inscription' in path:
            return ['Inscription']
        elif '/contact' in path or '/faq' in path:
            return ['Support']
        
        return ['Public API']
    
    def get_operation_id(self):
        """Génère un operation_id lisible"""
        method = self.method.lower()
        path_parts = [p for p in self.path.split('/') if p and p != 'api' and p != 'public']
        
        # Remplacer les paramètres UUID par un nom générique
        path_parts = [p if not '<' in p else 'by_id' for p in path_parts]
        
        return f"{method}_{'_'.join(path_parts)}"
