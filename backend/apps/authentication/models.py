"""
Modèles pour l'authentification et la sécurité
"""
from django.db import models
from django.utils import timezone
import uuid


class HistoriqueMotDePasse(models.Model):
    """
    Historique des changements de mot de passe.
    Permet de tracer tous les changements de mot de passe d'un utilisateur.
    """
    
    TYPE_CHANGEMENT_CHOICES = [
        ('CREATION', 'Création du compte'),
        ('MODIFICATION', 'Modification par l\'utilisateur'),
        ('REINITIALISATION', 'Réinitialisation par SMS'),
        ('REINITIALISATION_EMAIL', 'Réinitialisation par email'),
        ('FORCE_ADMIN', 'Forcé par un administrateur'),
        ('EXPIRATION', 'Changement suite à expiration'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Référence à l'utilisateur (identite.utilisateurs)
    utilisateur_id = models.UUIDField(db_index=True)
    courriel = models.EmailField(db_index=True)
    numero_telephone = models.CharField(max_length=20, db_index=True)
    
    # Détails du changement
    type_changement = models.CharField(
        max_length=30,
        choices=TYPE_CHANGEMENT_CHOICES,
        default='MODIFICATION'
    )
    ancien_hash = models.CharField(max_length=255, blank=True)  # Hash de l'ancien mot de passe
    nouveau_hash = models.CharField(max_length=255)  # Hash du nouveau mot de passe
    
    # Contexte
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    code_confirmation_utilise = models.CharField(max_length=5, blank=True)  # Code SMS utilisé
    
    # Métadonnées
    date_changement = models.DateTimeField(default=timezone.now, db_index=True)
    raison = models.TextField(blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'authentification"."historique_mot_de_passe'
        verbose_name = 'Historique Mot de Passe'
        verbose_name_plural = 'Historiques Mots de Passe'
        ordering = ['-date_changement']
        indexes = [
            models.Index(fields=['utilisateur_id', '-date_changement']),
            models.Index(fields=['courriel', '-date_changement']),
            models.Index(fields=['numero_telephone', '-date_changement']),
            models.Index(fields=['type_changement']),
        ]
    
    def __str__(self):
        return f"{self.courriel} - {self.type_changement} - {self.date_changement}"


class CodeConfirmationSMS(models.Model):
    """
    Codes de confirmation SMS actifs.
    Stocke les codes envoyés avec leur validité et permet de vérifier leur utilisation.
    """
    
    TYPE_CODE_CHOICES = [
        ('VERIFICATION_TELEPHONE', 'Vérification de téléphone'),
        ('REINITIALISATION_MDP', 'Réinitialisation mot de passe'),
        ('DOUBLE_AUTH', 'Double authentification'),
        ('CONFIRMATION_TRANSACTION', 'Confirmation de transaction'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('UTILISE', 'Utilisé'),
        ('EXPIRE', 'Expiré'),
        ('REMPLACE', 'Remplacé par un nouveau code'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Destinataire
    utilisateur_id = models.UUIDField(null=True, blank=True, db_index=True)
    numero_telephone = models.CharField(max_length=20, db_index=True)
    courriel = models.EmailField(blank=True, db_index=True)
    prenom = models.CharField(max_length=100, blank=True)
    
    # Code
    code = models.CharField(max_length=5, db_index=True)  # Code à 5 chiffres
    code_formate = models.CharField(max_length=50)  # Format: UF-CCF-PSW-XXXXX
    type_code = models.CharField(
        max_length=30,
        choices=TYPE_CODE_CHOICES,
        default='VERIFICATION_TELEPHONE'
    )
    
    # Validité
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    date_expiration = models.DateTimeField(db_index=True)
    duree_validite_minutes = models.IntegerField(default=15)
    
    # Statut
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='ACTIF',
        db_index=True
    )
    date_utilisation = models.DateTimeField(null=True, blank=True)
    nombre_tentatives = models.IntegerField(default=0)
    
    # Contexte d'envoi
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Métadonnées
    message_envoye = models.TextField(blank=True)
    reponse_service_sms = models.JSONField(default=dict, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'authentification"."codes_confirmation_sms'
        verbose_name = 'Code Confirmation SMS'
        verbose_name_plural = 'Codes Confirmation SMS'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['numero_telephone', 'statut', '-date_creation']),
            models.Index(fields=['code', 'statut']),
            models.Index(fields=['utilisateur_id', '-date_creation']),
            models.Index(fields=['date_expiration', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.numero_telephone} - {self.code_formate} - {self.statut}"
    
    def est_valide(self):
        """Vérifie si le code est encore valide"""
        return (
            self.statut == 'ACTIF' and
            timezone.now() <= self.date_expiration
        )
    
    def marquer_comme_utilise(self):
        """Marque le code comme utilisé"""
        self.statut = 'UTILISE'
        self.date_utilisation = timezone.now()
        self.save(update_fields=['statut', 'date_utilisation'])
    
    def marquer_comme_expire(self):
        """Marque le code comme expiré"""
        self.statut = 'EXPIRE'
        self.save(update_fields=['statut'])
    
    def marquer_comme_remplace(self):
        """Marque le code comme remplacé"""
        self.statut = 'REMPLACE'
        self.save(update_fields=['statut'])
    
    def incrementer_tentatives(self):
        """Incrémente le nombre de tentatives"""
        self.nombre_tentatives += 1
        self.save(update_fields=['nombre_tentatives'])
