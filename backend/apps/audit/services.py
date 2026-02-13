"""
Services pour l'audit et la traçabilité
"""
from django.utils import timezone
import uuid
import logging

from .models import JournalEvenement

logger = logging.getLogger(__name__)


class AuditService:
    """Service centralisé pour l'audit et la traçabilité"""
    
    @staticmethod
    def log_evenement(
        categorie,
        action,
        description,
        resultat='SUCCES',
        utilisateur_id=None,
        session_id=None,
        type_ressource=None,
        id_ressource=None,
        metadonnees=None,
        code_erreur=None,
        message_erreur=None,
        trace_erreur=None,
        temps_execution_ms=None,
        adresse_ip=None,
        agent_utilisateur=None
    ):
        """
        Enregistre un événement dans le journal d'audit
        """
        try:
            evenement = JournalEvenement.objects.create(
                id_requete=uuid.uuid4(),
                utilisateur_id=utilisateur_id,
                session_id=session_id,
                categorie_evenement=categorie,
                action=action,
                type_ressource=type_ressource,
                id_ressource=id_ressource,
                description=description,
                resultat=resultat,
                temps_execution_ms=temps_execution_ms,
                adresse_ip=adresse_ip,
                agent_utilisateur=agent_utilisateur,
                code_erreur=code_erreur,
                message_erreur=message_erreur,
                trace_erreur=trace_erreur,
                metadonnees=metadonnees or {},
                date_evenement=timezone.now()
            )
            
            return evenement
            
        except Exception as e:
            # Ne pas lever d'exception pour ne pas bloquer le flux principal
            logger.error(f"Erreur lors de l'enregistrement de l'événement d'audit: {str(e)}")
            return None
    
    @staticmethod
    def log_modification(
        nom_table,
        nom_schema,
        id_enregistrement,
        operation,
        utilisateur_id=None,
        donnees_avant=None,
        donnees_apres=None,
        champs_modifies=None,
        raison_modification=None
    ):
        """
        Enregistre une modification de données dans l'historique
        """
        from .models import HistoriqueModification
        
        try:
            historique = HistoriqueModification.objects.create(
                nom_table=nom_table,
                nom_schema=nom_schema,
                id_enregistrement=str(id_enregistrement),
                operation=operation,
                utilisateur_id=utilisateur_id,
                donnees_avant=donnees_avant,
                donnees_apres=donnees_apres,
                champs_modifies=champs_modifies or [],
                raison_modification=raison_modification,
                id_requete=uuid.uuid4(),
                date_modification=timezone.now()
            )
            
            return historique
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement de l'historique: {str(e)}")
            return None
