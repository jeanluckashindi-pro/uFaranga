"""
Modèles pour le schéma PORTEFEUILLE
Portefeuilles virtuels uFaranga (interface au-dessus des comptes bancaires)
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class PortefeuilleVirtuel(models.Model):
    """Portefeuilles virtuels - portefeuille.portefeuilles_virtuels"""
    
    TYPE_PORTEFEUILLE_CHOICES = [
        ('PERSONNEL', 'Personnel'),
        ('PROFESSIONNEL', 'Professionnel'),
        ('MARCHAND', 'Marchand'),
        ('AGENT', 'Agent'),
        ('EPARGNE', 'Épargne'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('GELE', 'Gelé'),
        ('SUSPENDU', 'Suspendu'),
        ('FERME', 'Fermé'),
        ('EN_VERIFICATION', 'En vérification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Liaison utilisateur
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Liaison au compte bancaire RÉEL
    compte_bancaire_reel_id = models.UUIDField(db_index=True)
    
    # Numéro de portefeuille uFaranga
    numero_portefeuille = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Type de portefeuille
    type_portefeuille = models.CharField(
        max_length=20,
        choices=TYPE_PORTEFEUILLE_CHOICES,
        db_index=True
    )
    
    # Alias et personnalisation
    nom_portefeuille = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    couleur_interface = models.CharField(max_length=7, blank=True)  # Code hex
    icone = models.CharField(max_length=50, blank=True)
    
    # Solde VIRTUEL (miroir du compte bancaire)
    solde_affiche = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    devise = models.CharField(max_length=3, default='BIF')
    
    # Décomposition du solde
    solde_disponible = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    solde_en_attente = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    solde_bloque = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Spécifique agents
    solde_float = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    solde_especes = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Limites
    limite_quotidienne = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    limite_mensuelle = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    limite_par_transaction = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Synchronisation avec le compte bancaire
    derniere_synchronisation = models.DateTimeField(null=True, blank=True)
    en_cours_synchronisation = models.BooleanField(default=False)
    
    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF', db_index=True)
    raison_statut = models.TextField(blank=True)
    
    # Métadonnées
    est_portefeuille_principal = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'portefeuille"."portefeuilles_virtuels'
        verbose_name = 'Portefeuille Virtuel'
        verbose_name_plural = 'Portefeuilles Virtuels'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['numero_portefeuille']),
            models.Index(fields=['compte_bancaire_reel_id']),
            models.Index(fields=['type_portefeuille']),
            models.Index(fields=['statut']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    solde_affiche=models.F('solde_disponible') + 
                    models.F('solde_en_attente') + 
                    models.F('solde_bloque')
                ),
                name='chk_solde_coherent'
            ),
        ]
    
    def __str__(self):
        return f"{self.numero_portefeuille} - {self.nom_portefeuille or 'Sans nom'}"
    
    def peut_debiter(self, montant):
        """Vérifie si le portefeuille peut être débité"""
        return (
            self.statut == 'ACTIF' and
            self.solde_disponible >= montant and
            montant > 0
        )
    
    def peut_crediter(self, montant):
        """Vérifie si le portefeuille peut être crédité"""
        return self.statut == 'ACTIF' and montant > 0
