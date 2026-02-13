"""
Services pour la gestion des portefeuilles
"""
from django.db import transaction
from django.utils import timezone
import random
import string
import logging

from .models import PortefeuilleVirtuel

logger = logging.getLogger(__name__)


class PortefeuilleService:
    """Service de gestion des portefeuilles virtuels"""
    
    @staticmethod
    def generer_numero_portefeuille():
        """
        Génère un numéro de portefeuille unique au format UFAR-BI-XXXXXXXX
        """
        while True:
            # Générer 8 caractères alphanumériques
            code = ''.join(random.choices(string.digits + string.ascii_uppercase, k=8))
            numero = f"UFAR-BI-{code}"
            
            # Vérifier l'unicité
            if not PortefeuilleVirtuel.objects.filter(numero_portefeuille=numero).exists():
                return numero
    
    @staticmethod
    @transaction.atomic
    def creer_portefeuille(
        utilisateur_id,
        compte_bancaire_reel_id,
        type_portefeuille='PERSONNEL',
        nom_portefeuille=None,
        devise='BIF',
        est_principal=False
    ):
        """
        Crée un nouveau portefeuille virtuel lié à un compte bancaire réel
        """
        try:
            # Si c'est le portefeuille principal, désactiver les autres
            if est_principal:
                PortefeuilleVirtuel.objects.filter(
                    utilisateur_id=utilisateur_id,
                    est_portefeuille_principal=True
                ).update(est_portefeuille_principal=False)
            
            # Créer le portefeuille
            portefeuille = PortefeuilleVirtuel.objects.create(
                utilisateur_id=utilisateur_id,
                compte_bancaire_reel_id=compte_bancaire_reel_id,
                numero_portefeuille=PortefeuilleService.generer_numero_portefeuille(),
                type_portefeuille=type_portefeuille,
                nom_portefeuille=nom_portefeuille or f"Portefeuille {type_portefeuille}",
                devise=devise,
                est_portefeuille_principal=est_principal,
                statut='ACTIF'
            )
            
            logger.info(f"Portefeuille créé: {portefeuille.numero_portefeuille}")
            return portefeuille
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du portefeuille: {str(e)}")
            raise
    
    @staticmethod
    @transaction.atomic
    def synchroniser_solde_avec_banque(portefeuille_id):
        """
        Synchronise le solde du portefeuille avec le compte bancaire réel
        """
        from apps.bancaire.models import CompteBancaireReel
        
        try:
            portefeuille = PortefeuilleVirtuel.objects.select_for_update().get(id=portefeuille_id)
            
            # Marquer comme en cours de synchronisation
            portefeuille.en_cours_synchronisation = True
            portefeuille.save()
            
            # Récupérer le solde du compte bancaire réel
            compte_bancaire = CompteBancaireReel.objects.get(
                id=portefeuille.compte_bancaire_reel_id
            )
            
            # TODO: Appeler l'API de la banque pour obtenir le solde en temps réel
            # Pour l'instant, on utilise le solde stocké
            solde_reel = compte_bancaire.solde_reel
            
            # Mettre à jour le portefeuille
            portefeuille.solde_disponible = solde_reel
            portefeuille.solde_affiche = (
                portefeuille.solde_disponible +
                portefeuille.solde_en_attente +
                portefeuille.solde_bloque
            )
            portefeuille.derniere_synchronisation = timezone.now()
            portefeuille.en_cours_synchronisation = False
            portefeuille.save()
            
            logger.info(f"Portefeuille {portefeuille.numero_portefeuille} synchronisé")
            return portefeuille
            
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation: {str(e)}")
            # Marquer comme non en cours
            if 'portefeuille' in locals():
                portefeuille.en_cours_synchronisation = False
                portefeuille.save()
            raise
