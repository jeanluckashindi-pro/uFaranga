"""
Services pour la gestion des transactions
Logique métier critique avec sécurité et traçabilité
"""
from django.db import transaction as db_transaction
from django.utils import timezone
from decimal import Decimal
import uuid
import logging

from .models import Transaction, GrandLivreComptable
from apps.portefeuille.models import PortefeuilleVirtuel
from apps.audit.services import AuditService

logger = logging.getLogger(__name__)


class TransactionService:
    """Service de gestion des transactions financières"""
    
    @staticmethod
    def generer_reference_transaction():
        """Génère une référence unique pour une transaction"""
        date_str = timezone.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"TXN-{date_str}-{unique_id}"
    
    @staticmethod
    @db_transaction.atomic
    def creer_transaction_p2p(
        portefeuille_source_id,
        portefeuille_destination_id,
        montant,
        description,
        utilisateur_source_id,
        utilisateur_destination_id,
        metadonnees=None
    ):
        """
        Crée une transaction Peer-to-Peer avec comptabilité en partie double
        """
        try:
            # Validation des portefeuilles
            portefeuille_source = PortefeuilleVirtuel.objects.select_for_update().get(
                id=portefeuille_source_id
            )
            portefeuille_dest = PortefeuilleVirtuel.objects.select_for_update().get(
                id=portefeuille_destination_id
            )
            
            # Vérifications
            if not portefeuille_source.peut_debiter(montant):
                raise ValueError("Solde insuffisant ou portefeuille inactif")
            
            if not portefeuille_dest.peut_crediter(montant):
                raise ValueError("Portefeuille destination ne peut pas recevoir de fonds")
            
            # Calcul des frais (à implémenter selon la grille de commissions)
            montant_frais = Decimal('0.00')  # TODO: Calculer selon grille
            montant_commission = Decimal('0.00')  # TODO: Calculer selon grille
            montant_total = montant + montant_frais + montant_commission
            
            # Créer la transaction
            txn = Transaction.objects.create(
                reference_transaction=TransactionService.generer_reference_transaction(),
                type_transaction='P2P',
                portefeuille_source_id=portefeuille_source_id,
                portefeuille_destination_id=portefeuille_destination_id,
                utilisateur_source_id=utilisateur_source_id,
                utilisateur_destination_id=utilisateur_destination_id,
                montant=montant,
                devise=portefeuille_source.devise,
                montant_frais=montant_frais,
                montant_commission=montant_commission,
                montant_total=montant_total,
                description=description,
                statut='VALIDATION',
                metadonnees=metadonnees or {}
            )
            
            # Débiter le portefeuille source
            solde_avant_source = portefeuille_source.solde_disponible
            portefeuille_source.solde_disponible -= montant_total
            portefeuille_source.solde_affiche = (
                portefeuille_source.solde_disponible +
                portefeuille_source.solde_en_attente +
                portefeuille_source.solde_bloque
            )
            portefeuille_source.save()
            
            # Écriture comptable - Débit
            GrandLivreComptable.objects.create(
                transaction_id=txn.id,
                portefeuille_id=portefeuille_source_id,
                type_ecriture='DEBIT',
                montant=montant_total,
                devise=portefeuille_source.devise,
                solde_avant=solde_avant_source,
                solde_apres=portefeuille_source.solde_disponible,
                libelle=f"Transfert P2P vers {portefeuille_destination_id}",
                reference=txn.reference_transaction
            )
            
            # Créditer le portefeuille destination
            solde_avant_dest = portefeuille_dest.solde_disponible
            portefeuille_dest.solde_disponible += montant
            portefeuille_dest.solde_affiche = (
                portefeuille_dest.solde_disponible +
                portefeuille_dest.solde_en_attente +
                portefeuille_dest.solde_bloque
            )
            portefeuille_dest.save()
            
            # Écriture comptable - Crédit
            GrandLivreComptable.objects.create(
                transaction_id=txn.id,
                portefeuille_id=portefeuille_destination_id,
                type_ecriture='CREDIT',
                montant=montant,
                devise=portefeuille_dest.devise,
                solde_avant=solde_avant_dest,
                solde_apres=portefeuille_dest.solde_disponible,
                libelle=f"Réception P2P de {portefeuille_source_id}",
                reference=txn.reference_transaction
            )
            
            # Marquer la transaction comme complète
            txn.statut = 'COMPLETE'
            txn.date_validation = timezone.now()
            txn.date_debut_traitement = timezone.now()
            txn.date_completion = timezone.now()
            txn.duree_traitement_ms = 0  # TODO: Calculer la durée réelle
            txn.save()
            
            # Audit
            AuditService.log_evenement(
                categorie='TRANSACTION_FINANCIERE',
                action='CREATION_TRANSACTION_P2P',
                utilisateur_id=utilisateur_source_id,
                description=f"Transaction P2P créée: {txn.reference_transaction}",
                resultat='SUCCES',
                metadonnees={
                    'transaction_id': str(txn.id),
                    'montant': str(montant),
                    'devise': portefeuille_source.devise
                }
            )
            
            logger.info(f"Transaction P2P créée avec succès: {txn.reference_transaction}")
            return txn
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la transaction P2P: {str(e)}")
            
            # Audit de l'échec
            AuditService.log_evenement(
                categorie='TRANSACTION_FINANCIERE',
                action='CREATION_TRANSACTION_P2P',
                utilisateur_id=utilisateur_source_id,
                description=f"Échec de création de transaction P2P",
                resultat='ECHEC',
                message_erreur=str(e)
            )
            
            raise
    
    @staticmethod
    def verifier_limites_transaction(utilisateur_id, type_transaction, montant, niveau_kyc):
        """
        Vérifie si une transaction respecte les limites configurées
        """
        from apps.configuration.models import LimiteTransaction
        from django.db.models import Sum
        from datetime import datetime, timedelta
        
        # Récupérer les limites applicables
        limites = LimiteTransaction.objects.filter(
            niveau_kyc=niveau_kyc,
            type_transaction=type_transaction,
            est_active=True,
            date_debut_validite__lte=timezone.now().date()
        ).first()
        
        if not limites:
            return True, "Aucune limite configurée"
        
        # Vérifier le montant unitaire
        if montant > limites.montant_max_unitaire:
            return False, f"Montant supérieur à la limite unitaire ({limites.montant_max_unitaire})"
        
        # Vérifier les limites quotidiennes
        debut_jour = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        total_jour = Transaction.objects.filter(
            utilisateur_source_id=utilisateur_id,
            type_transaction=type_transaction,
            statut='COMPLETE',
            date_completion__gte=debut_jour
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')
        
        if total_jour + montant > limites.montant_max_quotidien:
            return False, f"Limite quotidienne dépassée ({limites.montant_max_quotidien})"
        
        # Vérifier les limites mensuelles
        debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total_mois = Transaction.objects.filter(
            utilisateur_source_id=utilisateur_id,
            type_transaction=type_transaction,
            statut='COMPLETE',
            date_completion__gte=debut_mois
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')
        
        if total_mois + montant > limites.montant_max_mensuel:
            return False, f"Limite mensuelle dépassée ({limites.montant_max_mensuel})"
        
        return True, "Limites respectées"
    
    @staticmethod
    def calculer_score_fraude(transaction_data):
        """
        Calcule un score de fraude pour une transaction
        Score de 0 (pas de risque) à 100 (risque élevé)
        """
        score = 0
        raisons = []
        
        # TODO: Implémenter la logique de détection de fraude
        # - Montant inhabituel
        # - Localisation inhabituelle
        # - Fréquence des transactions
        # - Appareil inconnu
        # - Heure inhabituelle
        # - etc.
        
        return score, raisons
