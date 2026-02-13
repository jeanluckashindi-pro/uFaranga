from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour DRF.
    Formate toutes les erreurs de manière cohérente.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'success': False,
            'status_code': response.status_code,
            'errors': response.data,
        }

        # Log les erreurs serveur
        if response.status_code >= 500:
            logger.error(f"Erreur serveur: {exc}", exc_info=True)

        response.data = custom_response_data

    return response
