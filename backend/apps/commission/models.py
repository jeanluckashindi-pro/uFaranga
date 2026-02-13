"""
Modèles pour le schéma COMMISSION
Système de commissions et rémunérations
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class GrilleCommission(models.Model):
    """Grille des commissions - commission.grilles_commissions"""
    
    TYPE_COMMISSION_CHOICES = [
        ('FIXE', 'Fixe'),
        ('POURCENTAGE', 'Pourcentage'),
        ('MIXTE', 'Mixte'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Applicabilité
    type_transaction = models.CharField(max_length=30, db_index=True)
    type_utilisateur = models.CharField(max_length=20, blank=True)
    niveau_kyc = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Montant de transaction
    montant_min = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    montant_max = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Commission
    type_commission = models.CharField(
        max_length=20,
        choices=TYPE_COMMISSION_CHOICES
    )
    montant_fixe = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    pourcentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )
    commission_min = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    commission_max = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Priorité
    priorite = models.IntegerField(default=0)
    
    # Période de validité
    date_debut_validite = models.DateField(default=timezone.now, db_index=True)
    date_fin_validite = models.DateField(null=True, blank=True)
    
    # Statut
    est_active = models.BooleanField(default=True, db_index=True)
    
    # Métadonnées
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'commission"."grilles_commissions'
        verbose_name = 'Grille Commission'
        verbose_name_plural = 'Grilles Commissions'
        indexes = [
            models.Index(fields=['type_transaction']),
            models.Index(fields=['date_debut_validite', 'date_fin_validite']),
        ]
    
    def __str__(self):
        return f"{self.type_transaction} - {self.type_commission}"


class Commission(models.Model):
    """Commissions calculées - commission.commissions"""
    
    TYPE_BENEFICIAIRE_CHOICES = [
        ('AGENT', 'Agent'),
        ('MARCHAND', 'Marchand'),
        ('PARRAIN', 'Parrain'),
        ('PLATEFORME', 'Plateforme'),
    ]
    
    STATUT_PAIEMENT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('PAYEE', 'Payée'),
        ('SUSPENDUE', 'Suspendue'),
        ('ANNULEE', 'Annulée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Transaction liée
    transaction_id = models.UUIDField(unique=True, db_index=True)
    
    # Bénéficiaire
    beneficiaire_id = models.UUIDField(null=True, blank=True, db_index=True)
    type_beneficiaire = models.CharField(
        max_length=20,
        choices=TYPE_BENEFICIAIRE_CHOICES,
        blank=True
    )
    
    # Grille appliquée
    grille_commission_id = models.UUIDField(null=True, blank=True)
    
    # Type et montant
    type_commission = models.CharField(max_length=50)
    montant_commission = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    devise = models.CharField(max_length=3, default='BIF')
    
    # Détails du calcul
    base_calcul = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    pourcentage_applique = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    montant_fixe_applique = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Statut de paiement
    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_PAIEMENT_CHOICES,
        default='EN_ATTENTE',
        db_index=True
    )
    date_paiement = models.DateTimeField(null=True, blank=True)
    reference_paiement = models.CharField(max_length=100, blank=True)
    
    # Horodatage
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'commission"."commissions'
        verbose_name = 'Commission'
        verbose_name_plural = 'Commissions'
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['beneficiaire_id']),
            models.Index(fields=['statut_paiement']),
            models.Index(fields=['-date_creation']),
        ]
    
    def __str__(self):
        return f"Commission {self.montant_commission} {self.devise} - {self.type_beneficiaire}"
