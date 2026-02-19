"""
Tâches Celery pour l'authentification
"""
from celery import shared_task
import logging
from .services_sms import nettoyer_codes_expires

logger = logging.getLogger('apps')


@shared_task(name='authentication.nettoyer_codes_expires')
def nettoyer_codes_expires_task():
    """
    Tâche périodique pour nettoyer les codes SMS expirés.
    À exécuter toutes les heures.
    """
    try:
        count = nettoyer_codes_expires()
        logger.info(f"Tâche de nettoyage terminée: {count} code(s) expiré(s)")
        return {
            'success': True,
            'codes_expires': count
        }
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des codes: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
