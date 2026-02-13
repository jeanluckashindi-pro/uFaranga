"""
Modèles pour le schéma BANCAIRE
Intégration avec le système bancaire réel
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class BanquePartenaire(models.Model):
    """Banques partenaires - bancaire.banques_partenaires"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Identification
    code_banque = models.CharField(max_length=20, unique=True, db_index=True)
    nom_banque = models.CharField(max_length=200)
    code_swift = models.CharField(max_length=11, unique=True, blank=True)
    code_bic = models.CharField(max_length=11, blank=True)
    pays = models.CharField(max_length=2, default='BI')
    
    # Contact
    adresse_siege = models.TextField(blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    site_web = models.URLField(blank=True)
    
    # Intégration technique
    api_endpoint = models.URLField(max_length=500, blank=True)
    api_version = models.CharField(max_length=20, blank=True)
    cle_api_chiffree = models.TextField(blank=True)  # Stockée chiffrée
    certificat_ssl = models.TextField(blank=True)
    
    # Configuration
    supporte_temps_reel = models.BooleanField(default=False)
    delai_traitement_heures = models.IntegerField(default=24)
    frais_integration = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Statut
    est_active = models.BooleanField(default=True, db_index=True)
    date_partenariat = models.DateField()
    date_fin_partenariat = models.DateField(null=True, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'bancaire"."banques_partenaires'
        verbose_name = 'Banque Partenaire'
        verbose_name_plural = 'Banques Partenaires'
        indexes = [
            models.Index(fields=['code_banque']),
            models.Index(fields=['code_swift']),
        ]
    
    def __str__(self):
        return f"{self.nom_banque} ({self.code_banque})"


class CompteBancaireReel(models.Model):
    """Comptes bancaires RÉELS - bancaire.comptes_bancaires_reels"""
    
    TYPE_COMPTE_CHOICES = [
        ('COMPTE_COURANT', 'Compte Courant'),
        ('COMPTE_EPARGNE', 'Compte Épargne'),
        ('COMPTE_DEPOT', 'Compte Dépôt'),
        ('COMPTE_PROFESSIONNEL', 'Compte Professionnel'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('SUSPENDU', 'Suspendu'),
        ('FERME', 'Fermé'),
        ('EN_VERIFICATION', 'En vérification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Liaison utilisateur
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Banque
    banque = models.ForeignKey(
        BanquePartenaire,
        on_delete=models.RESTRICT,
        related_name='comptes'
    )
    
    # Informations du compte bancaire RÉEL
    numero_compte_bancaire = models.CharField(max_length=50, unique=True, db_index=True)
    rib = models.CharField(max_length=50, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    swift_bic = models.CharField(max_length=11, blank=True)
    
    # Type de compte
    type_compte = models.CharField(max_length=30, choices=TYPE_COMPTE_CHOICES)
    
    # Titulaire
    nom_titulaire = models.CharField(max_length=200)
    prenom_titulaire = models.CharField(max_length=200, blank=True)
    
    # Solde RÉEL (synchronisé depuis la banque)
    solde_reel = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    devise = models.CharField(max_length=3, default='BIF')
    
    # Synchronisation
    derniere_synchronisation = models.DateTimeField(null=True, blank=True)
    frequence_synchronisation_minutes = models.IntegerField(default=5)
    erreur_derniere_sync = models.TextField(blank=True)
    
    # Statut
    est_compte_principal = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF')
    
    # Validation
    compte_verifie = models.BooleanField(default=False)
    date_verification = models.DateTimeField(null=True, blank=True)
    methode_verification = models.CharField(max_length=50, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'bancaire"."comptes_bancaires_reels'
        verbose_name = 'Compte Bancaire Réel'
        verbose_name_plural = 'Comptes Bancaires Réels'
        unique_together = [['utilisateur_id', 'numero_compte_bancaire']]
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['numero_compte_bancaire']),
            models.Index(fields=['banque']),
        ]
    
    def __str__(self):
        return f"{self.numero_compte_bancaire} - {self.banque.nom_banque}"


class MouvementBancaireReel(models.Model):
    """Mouvements bancaires RÉELS - TABLE IMMUABLE"""
    
    TYPE_MOUVEMENT_CHOICES = [
        ('CREDIT', 'Crédit'),
        ('DEBIT', 'Débit'),
        ('FRAIS', 'Frais'),
        ('INTERET', 'Intérêt'),
        ('VIREMENT', 'Virement'),
        ('PRELEVEMENT', 'Prélèvement'),
        ('CHEQUE', 'Chèque'),
        ('CARTE', 'Carte'),
    ]
    
    STATUT_CHOICES = [
        ('COMPLETE', 'Complète'),
        ('EN_ATTENTE', 'En attente'),
        ('ANNULE', 'Annulée'),
        ('REJETE', 'Rejetée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Compte bancaire concerné
    compte_bancaire = models.ForeignKey(
        CompteBancaireReel,
        on_delete=models.RESTRICT,
        related_name='mouvements'
    )
    
    # Référence bancaire
    reference_banque = models.CharField(max_length=100, unique=True, db_index=True)
    reference_externe = models.CharField(max_length=100, blank=True)
    
    # Type de mouvement
    type_mouvement = models.CharField(max_length=30, choices=TYPE_MOUVEMENT_CHOICES, db_index=True)
    
    # Montant
    montant = models.DecimalField(max_digits=18, decimal_places=2)
    devise = models.CharField(max_length=3, default='BIF')
    
    # Soldes
    solde_avant = models.DecimalField(max_digits=18, decimal_places=2)
    solde_apres = models.DecimalField(max_digits=18, decimal_places=2)
    
    # Description
    libelle = models.TextField()
    description_detaillee = models.TextField(blank=True)
    
    # Contrepartie
    compte_contrepartie = models.CharField(max_length=50, blank=True)
    nom_contrepartie = models.CharField(max_length=200, blank=True)
    banque_contrepartie = models.CharField(max_length=100, blank=True)
    
    # Dates
    date_operation = models.DateField(db_index=True)
    date_valeur = models.DateField()
    heure_operation = models.TimeField(null=True, blank=True)
    
    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='COMPLETE')
    
    # Synchronisation
    date_importation = models.DateTimeField(default=timezone.now, db_index=True)
    importe_par = models.CharField(max_length=50, default='SYSTEME')
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'bancaire"."mouvements_bancaires_reels'
        verbose_name = 'Mouvement Bancaire Réel'
        verbose_name_plural = 'Mouvements Bancaires Réels'
        indexes = [
            models.Index(fields=['compte_bancaire']),
            models.Index(fields=['reference_banque']),
            models.Index(fields=['-date_operation']),
            models.Index(fields=['-date_importation']),
            models.Index(fields=['type_mouvement']),
        ]
        # TABLE IMMUABLE - Pas de UPDATE/DELETE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_mouvement', 'Can view mouvement bancaire réel'),
            ('add_mouvement', 'Can add mouvement bancaire réel'),
        ]
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.montant} {self.devise} - {self.date_operation}"
    
    def save(self, *args, **kwargs):
        # Empêcher la modification après création
        if self.pk is not None:
            raise ValueError("Les mouvements bancaires réels ne peuvent pas être modifiés (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Les mouvements bancaires réels ne peuvent pas être supprimés (TABLE IMMUABLE)")
