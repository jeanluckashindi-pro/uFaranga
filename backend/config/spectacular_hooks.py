"""
Hooks drf-spectacular pour filtrer le schéma OpenAPI.
Par défaut, la doc Swagger n'affiche que les APIs v1 (pas l'API publique).
"""

# Préfixe des paths à conserver dans le schéma par défaut (Swagger principal)
V1_PATH_PREFIX = '/api/v1/'


def postprocess_filter_v1_only(result, generator, request=None, public=None, **kwargs):
    """
    Garde uniquement les paths sous /api/v1/ dans le schéma.
    Ainsi /api/docs/ et la racine n'affichent que l'API v1.
    """
    if 'paths' not in result:
        return result
    result['paths'] = {
        path: methods
        for path, methods in result['paths'].items()
        if path.startswith(V1_PATH_PREFIX)
    }
    return result
