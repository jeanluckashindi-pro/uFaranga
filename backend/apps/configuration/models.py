"""
Modèles pour le schéma CONFIGURATION
Paramètres système et référentiels
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class ParametreSysteme(models.Model):
    """Paramètres système - configuration.parametres_systeme"""
    
    TYPE_VALEUR_CHOICES = [
        ('STRING', 'String'),
        ('INTEGER', 'Integer'),
        ('DECIMAL', 'Decimal'),
        ('BOOLEAN', 'Boolean'),
        ('JSON', 'JSON'),
        ('ARRAY', 'Array'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    cle = models.CharField(max_length=100, unique=True, db_index=True)
    valeur = models.TextField()
    type_valeur = models.CharField(
        max_length=20,
        choices=TYPE_VALEUR_CHOICES,
        default='STRING'
    )
    
    # Métadonnées
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=50, blank=True, db_index=True)
    est_sensible = models.BooleanField(default=False)
    est_modifiable = models.BooleanField(default=True)
    
    # Audit
    modifie_par = models.UUIDField(null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'configuration"."parametres_systeme'
        verbose_name = 'Paramètre Système'
        verbose_name_plural = 'Paramètres Système'
        indexes = [
            models.Index(fields=['cle']),
            models.Index(fields=['categorie']),
        ]
    
    def __str__(self):
        return f"{self.cle} = {self.valeur}"


class LimiteTransaction(models.Model):
    """Limites de transactions - configuration.limites_transactions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Règle
    niveau_kyc = models.IntegerField(validators=[MinValueValidator(0)])
    type_utilisateur = models.CharField(max_length=20)
    type_transaction = models.CharField(max_length=30)
    
    # Limites
    montant_min = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    montant_max_unitaire = models.DecimalField(max_digits=18, decimal_places=2)
    montant_max_quotidien = models.DecimalField(max_digits=18, decimal_places=2)
    montant_max_hebdomadaire = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    montant_max_mensuel = models.DecimalField(max_digits=18, decimal_places=2)
    montant_max_annuel = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Nombre
    nombre_max_quotidien = models.IntegerField(null=True, blank=True)
    nombre_max_hebdomadaire = models.IntegerField(null=True, blank=True)
    nombre_max_mensuel = models.IntegerField(null=True, blank=True)
    
    # Validité
    est_active = models.BooleanField(default=True, db_index=True)
    date_debut_validite = models.DateField(default=timezone.now)
    date_fin_validite = models.DateField(null=True, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'configuration"."limites_transactions'
        verbose_name = 'Limite Transaction'
        verbose_name_plural = 'Limites Transactions'
        unique_together = [
            ['niveau_kyc', 'type_utilisateur', 'type_transaction', 'date_debut_validite']
        ]
        indexes = [
            models.Index(fields=['niveau_kyc']),
            models.Index(fields=['type_utilisateur']),
        ]
    
    def __str__(self):
        return f"Limite {self.type_transaction} - KYC {self.niveau_kyc}"


class TauxChange(models.Model):
    """Taux de change - configuration.taux_change"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    devise_source = models.CharField(max_length=3)
    devise_cible = models.CharField(max_length=3)
    taux = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000001'))]
    )
    
    # Source du taux
    source = models.CharField(max_length=50, blank=True)
    
    # Validité
    date_debut_validite = models.DateTimeField(default=timezone.now)
    date_fin_validite = models.DateTimeField(null=True, blank=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'configuration"."taux_change'
        verbose_name = 'Taux de Change'
        verbose_name_plural = 'Taux de Change'
        unique_together = [['devise_source', 'devise_cible', 'date_debut_validite']]
        indexes = [
            models.Index(fields=['devise_source', 'devise_cible']),
            models.Index(fields=['est_actif', '-date_debut_validite']),
        ]
    
    def __str__(self):
        return f"{self.devise_source}/{self.devise_cible}: {self.taux}"


class Blacklist(models.Model):
    """Liste noire - configuration.blacklist"""
    
    TYPE_ENTREE_CHOICES = [
        ('UTILISATEUR', 'Utilisateur'),
        ('TELEPHONE', 'Téléphone'),
        ('EMAIL', 'Email'),
        ('IP', 'IP'),
        ('DEVICE', 'Device'),
        ('COMPTE_BANCAIRE', 'Compte Bancaire'),
    ]
    
    GRAVITE_CHOICES = [
        ('FAIBLE', 'Faible'),
        ('MOYENNE', 'Moyenne'),
        ('ELEVEE', 'Élevée'),
        ('CRITIQUE', 'Critique'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    type_entree = models.CharField(max_length=20, choices=TYPE_ENTREE_CHOICES, db_index=True)
    valeur = models.CharField(max_length=255, db_index=True)
    
    # Raison
    raison = models.TextField()
    categorie = models.CharField(max_length=50, blank=True)
    gravite = models.CharField(
        max_length=20,
        choices=GRAVITE_CHOICES,
        blank=True,
        db_index=True
    )
    
    # Qui a ajouté
    ajoute_par = models.UUIDField()
    
    # Période
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(null=True, blank=True)
    est_permanent = models.BooleanField(default=False)
    est_actif = models.BooleanField(default=True, db_index=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'configuration"."blacklist'
        verbose_name = 'Blacklist'
        verbose_name_plural = 'Blacklist'
        unique_together = [['type_entree', 'valeur']]
        indexes = [
            models.Index(fields=['type_entree']),
            models.Index(fields=['valeur']),
            models.Index(fields=['gravite']),
        ]
    
    def __str__(self):
        return f"{self.type_entree}: {self.valeur}"
