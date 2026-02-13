"""
Modèles pour le schéma TRANSACTION
Transactions financières et grand livre comptable
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid


class Transaction(models.Model):
    """Transactions financières - transaction.transactions"""
    
    TYPE_TRANSACTION_CHOICES = [
        ('P2P', 'Peer to Peer'),
        ('DEPOT', 'Dépôt d\'espèces'),
        ('RETRAIT', 'Retrait d\'espèces'),
        ('PAIEMENT_MARCHAND', 'Paiement à un marchand'),
        ('PAIEMENT_FACTURE', 'Paiement de facture'),
        ('RECHARGE_TELEPHONIQUE', 'Recharge téléphone'),
        ('VIREMENT_BANCAIRE', 'Virement vers autre banque'),
        ('TRANSFERT_INTERNATIONAL', 'Transfert international'),
        ('COMMISSION', 'Commission'),
        ('FRAIS', 'Frais de service'),
        ('REMBOURSEMENT', 'Remboursement'),
        ('AJUSTEMENT', 'Ajustement comptable'),
        ('INTEREST', 'Intérêts'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDATION', 'En cours de validation'),
        ('TRAITEMENT', 'En cours de traitement'),
        ('COMPLETE', 'Transaction réussie'),
        ('ECHEC', 'Transaction échouée'),
        ('ANNULEE', 'Transaction annulée'),
        ('REMBOURSEE', 'Transaction remboursée'),
        ('SUSPENDUE', 'Transaction suspendue'),
    ]
    
    TYPE_APPAREIL_CHOICES = [
        ('MOBILE', 'Mobile'),
        ('WEB', 'Web'),
        ('TABLETTE', 'Tablette'),
        ('USSD', 'USSD'),
        ('API', 'API'),
    ]
    
    CANAL_CHOICES = [
        ('APP_MOBILE', 'Application Mobile'),
        ('APP_WEB', 'Application Web'),
        ('USSD', 'USSD'),
        ('API', 'API'),
        ('AGENT', 'Agent'),
        ('GUICHET', 'Guichet'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Référence unique
    reference_transaction = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Type de transaction
    type_transaction = models.CharField(
        max_length=30,
        choices=TYPE_TRANSACTION_CHOICES,
        db_index=True
    )
    
    # Portefeuilles impliqués
    portefeuille_source_id = models.UUIDField(null=True, blank=True, db_index=True)
    portefeuille_destination_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Utilisateurs impliqués
    utilisateur_source_id = models.UUIDField(null=True, blank=True, db_index=True)
    utilisateur_destination_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Comptes bancaires RÉELS impliqués
    compte_bancaire_source_id = models.UUIDField(null=True, blank=True)
    compte_bancaire_dest_id = models.UUIDField(null=True, blank=True)
    
    # Montants
    montant = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    devise = models.CharField(max_length=3, default='BIF')
    montant_frais = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    montant_commission = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    montant_total = models.DecimalField(max_digits=18, decimal_places=2)
    
    # Taux de change (si applicable)
    taux_change = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True
    )
    devise_destination = models.CharField(max_length=3, blank=True)
    montant_destination = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Description
    description = models.TextField()
    description_detaillee = models.TextField(blank=True)
    motif = models.CharField(max_length=200, blank=True)
    
    # Statut du traitement
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        db_index=True
    )
    
    # Flux de traitement
    date_initiation = models.DateTimeField(default=timezone.now, db_index=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    date_debut_traitement = models.DateTimeField(null=True, blank=True)
    date_completion = models.DateTimeField(null=True, blank=True, db_index=True)
    date_echec = models.DateTimeField(null=True, blank=True)
    date_annulation = models.DateTimeField(null=True, blank=True)
    
    # Durée de traitement
    duree_traitement_ms = models.IntegerField(null=True, blank=True)
    
    # Raisons d'échec/annulation
    code_erreur = models.CharField(max_length=50, blank=True)
    raison_echec = models.TextField(blank=True)
    raison_annulation = models.TextField(blank=True)
    annulee_par = models.UUIDField(null=True, blank=True)
    
    # Détection de fraude
    score_fraude = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    raison_score_fraude = models.TextField(blank=True)
    flagged_fraude = models.BooleanField(default=False, db_index=True)
    date_flag_fraude = models.DateTimeField(null=True, blank=True)
    
    # Référence bancaire
    reference_banque = models.CharField(max_length=100, blank=True)
    reference_externe = models.CharField(max_length=100, blank=True)
    
    # Localisation
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True
    )
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    pays_origine = models.CharField(max_length=2, blank=True)
    ville_origine = models.CharField(max_length=100, blank=True)
    
    # Appareil utilisé
    id_appareil = models.CharField(max_length=255, blank=True)
    type_appareil = models.CharField(
        max_length=20,
        choices=TYPE_APPAREIL_CHOICES,
        blank=True
    )
    agent_utilisateur = models.TextField(blank=True)
    
    # Canal de transaction
    canal = models.CharField(
        max_length=30,
        choices=CANAL_CHOICES,
        default='APP_MOBILE'
    )
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    # Audit
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    
    class Meta:
        db_table = 'transaction"."transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        indexes = [
            models.Index(fields=['reference_transaction']),
            models.Index(fields=['type_transaction']),
            models.Index(fields=['statut']),
            models.Index(fields=['portefeuille_source_id']),
            models.Index(fields=['portefeuille_destination_id']),
            models.Index(fields=['utilisateur_source_id']),
            models.Index(fields=['utilisateur_destination_id']),
            models.Index(fields=['-date_initiation']),
            models.Index(fields=['-date_completion']),
            models.Index(fields=['utilisateur_source_id', '-date_initiation']),
            models.Index(fields=['portefeuille_source_id', '-date_initiation']),
            models.Index(fields=['statut', '-date_initiation']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    montant_total=models.F('montant') + 
                    models.F('montant_frais') + 
                    models.F('montant_commission')
                ),
                name='chk_montant_total'
            ),
        ]
    
    def __str__(self):
        return f"{self.reference_transaction} - {self.type_transaction} - {self.montant} {self.devise}"


class GrandLivreComptable(models.Model):
    """Grand livre comptable - Double Entry Bookkeeping - TABLE IMMUABLE"""
    
    TYPE_ECRITURE_CHOICES = [
        ('DEBIT', 'Débit'),
        ('CREDIT', 'Crédit'),
    ]
    
    TYPE_COMPTE_CHOICES = [
        ('PORTEFEUILLE', 'Portefeuille'),
        ('COMPTE_BANCAIRE', 'Compte Bancaire'),
        ('AUTRE', 'Autre'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    
    # Transaction liée
    transaction_id = models.UUIDField(db_index=True)
    
    # Compte affecté
    portefeuille_id = models.UUIDField(null=True, blank=True)
    compte_bancaire_id = models.UUIDField(null=True, blank=True)
    
    # Type d'écriture
    type_ecriture = models.CharField(max_length=10, choices=TYPE_ECRITURE_CHOICES, db_index=True)
    
    # Montants
    montant = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    devise = models.CharField(max_length=3, default='BIF')
    
    # Soldes
    solde_avant = models.DecimalField(max_digits=18, decimal_places=2)
    solde_apres = models.DecimalField(max_digits=18, decimal_places=2)
    
    # Description
    libelle = models.TextField()
    reference = models.CharField(max_length=100, blank=True)
    
    # Compte de contrepartie
    compte_contrepartie_id = models.UUIDField(null=True, blank=True)
    type_compte_contrepartie = models.CharField(
        max_length=20,
        choices=TYPE_COMPTE_CHOICES,
        blank=True
    )
    
    # Horodatage (IMMUABLE)
    date_ecriture = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'transaction"."grand_livre_comptable'
        verbose_name = 'Écriture Comptable'
        verbose_name_plural = 'Grand Livre Comptable'
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['portefeuille_id']),
            models.Index(fields=['compte_bancaire_id']),
            models.Index(fields=['-date_ecriture']),
            models.Index(fields=['type_ecriture']),
        ]
        # TABLE IMMUABLE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_grandlivre', 'Can view grand livre comptable'),
            ('add_grandlivre', 'Can add grand livre comptable'),
        ]
    
    def __str__(self):
        return f"{self.type_ecriture} - {self.montant} {self.devise} - {self.date_ecriture}"
    
    def save(self, *args, **kwargs):
        # Empêcher la modification après création
        if self.pk is not None:
            raise ValueError("Le grand livre comptable ne peut pas être modifié (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Le grand livre comptable ne peut pas être supprimé (TABLE IMMUABLE)")
