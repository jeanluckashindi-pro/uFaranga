"""
Modèles pour le schéma IDENTITE
Gestion des utilisateurs, profils et authentification
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
import uuid


class UtilisateurManager(BaseUserManager):
    """Manager personnalisé pour le modèle Utilisateur"""
    
    def create_user(self, courriel, numero_telephone, mot_de_passe=None, **extra_fields):
        if not courriel:
            raise ValueError('L\'adresse courriel est obligatoire')
        if not numero_telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        courriel = self.normalize_email(courriel)
        user = self.model(courriel=courriel, numero_telephone=numero_telephone, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, courriel, numero_telephone, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('type_utilisateur', 'SUPER_ADMIN')
        extra_fields.setdefault('niveau_kyc', 3)
        extra_fields.setdefault('statut', 'ACTIF')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(courriel, numero_telephone, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Table principale des utilisateurs - identite.utilisateurs"""
    
    TYPE_UTILISATEUR_CHOICES = [
        ('CLIENT', 'Client'),
        ('AGENT', 'Agent'),
        ('MARCHAND', 'Marchand'),
        ('ADMIN', 'Administrateur'),
        ('SUPER_ADMIN', 'Super Administrateur'),
        ('SYSTEME', 'Système'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('SUSPENDU', 'Suspendu'),
        ('BLOQUE', 'Bloqué'),
        ('FERME', 'Fermé'),
        ('EN_VERIFICATION', 'En vérification'),
    ]
    
    # Identifiant unique
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Authentification
    courriel = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        db_index=True
    )
    numero_telephone = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^\+?[1-9]\d{1,14}$')],
        db_index=True
    )
    hash_mot_de_passe = models.CharField(max_length=255)
    
    # Informations personnelles
    prenom = models.CharField(max_length=100)
    nom_famille = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, blank=True)
    nationalite = models.CharField(max_length=2, default='BI')
    
    # Adresse
    pays_residence = models.CharField(max_length=2, default='BI')
    province = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    commune = models.CharField(max_length=100, blank=True)
    quartier = models.CharField(max_length=100, blank=True)
    avenue = models.CharField(max_length=100, blank=True)
    numero_maison = models.CharField(max_length=50, blank=True)
    adresse_complete = models.TextField(blank=True)
    code_postal = models.CharField(max_length=20, blank=True)
    
    # Vérifications
    telephone_verifie = models.BooleanField(default=False)
    telephone_verifie_le = models.DateTimeField(null=True, blank=True)
    courriel_verifie = models.BooleanField(default=False)
    courriel_verifie_le = models.DateTimeField(null=True, blank=True)
    
    # KYC
    niveau_kyc = models.IntegerField(
        default=0,
        choices=[(0, 'Non vérifié'), (1, 'Basique'), (2, 'Complet'), (3, 'Premium')]
    )
    date_validation_kyc = models.DateTimeField(null=True, blank=True)
    validateur_kyc_id = models.UUIDField(null=True, blank=True)
    
    # Type et statut
    type_utilisateur = models.CharField(max_length=20, choices=TYPE_UTILISATEUR_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF', db_index=True)
    raison_statut = models.TextField(blank=True)
    
    # Sécurité
    nombre_tentatives_connexion = models.IntegerField(default=0)
    bloque_jusqua = models.DateTimeField(null=True, blank=True)
    double_auth_activee = models.BooleanField(default=False)
    secret_2fa = models.CharField(max_length=255, blank=True)
    
    # Métadonnées
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    date_modification = models.DateTimeField(auto_now=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    derniere_modification_mdp = models.DateTimeField(null=True, blank=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    # Django admin
    is_staff = models.BooleanField(default=False)
    
    # Fix pour éviter les conflits avec users.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='identite_utilisateurs',
        related_query_name='identite_utilisateur',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='identite_utilisateurs',
        related_query_name='identite_utilisateur',
    )
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'courriel'
    REQUIRED_FIELDS = ['numero_telephone', 'prenom', 'nom_famille', 'date_naissance']
    
    class Meta:
        db_table = 'identite"."utilisateurs'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        indexes = [
            models.Index(fields=['courriel']),
            models.Index(fields=['numero_telephone']),
            models.Index(fields=['type_utilisateur']),
            models.Index(fields=['statut']),
            models.Index(fields=['niveau_kyc']),
            models.Index(fields=['-date_creation']),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom_famille} ({self.courriel})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom_famille}"
    
    def peut_effectuer_transactions(self):
        """Vérifie si l'utilisateur peut effectuer des transactions"""
        return (
            self.statut == 'ACTIF' and
            self.telephone_verifie and
            self.niveau_kyc >= 1
        )


class ProfilUtilisateur(models.Model):
    """Profils et préférences - identite.profils_utilisateurs"""
    
    LANGUE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        ('sw', 'Kiswahili'),
        ('rn', 'Kirundi'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='profil'
    )
    
    # Profil visuel
    url_avatar = models.URLField(max_length=500, blank=True)
    url_photo_couverture = models.URLField(max_length=500, blank=True)
    biographie = models.TextField(blank=True)
    
    # Préférences
    langue = models.CharField(max_length=5, choices=LANGUE_CHOICES, default='fr')
    devise_preferee = models.CharField(max_length=3, default='BIF')
    fuseau_horaire = models.CharField(max_length=50, default='Africa/Bujumbura')
    format_date = models.CharField(max_length=20, default='DD/MM/YYYY')
    format_heure = models.CharField(max_length=10, default='24h')
    
    # Notifications
    notifications_courriel = models.BooleanField(default=True)
    notifications_sms = models.BooleanField(default=True)
    notifications_push = models.BooleanField(default=True)
    notifications_transactions = models.BooleanField(default=True)
    notifications_marketing = models.BooleanField(default=False)
    
    # Confidentialité
    profil_public = models.BooleanField(default=False)
    afficher_telephone = models.BooleanField(default=False)
    afficher_courriel = models.BooleanField(default=False)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'identite"."profils_utilisateurs'
        verbose_name = 'Profil Utilisateur'
        verbose_name_plural = 'Profils Utilisateurs'
    
    def __str__(self):
        return f"Profil de {self.utilisateur.nom_complet}"
