"""
Modèles pour le schéma DEVELOPPEURS
Gestion des comptes développeurs et clés API
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import uuid
import secrets
import hashlib


class CompteDeveloppeur(models.Model):
    """Comptes développeurs - developpeurs.comptes_developpeurs"""
    
    TYPE_COMPTE_CHOICES = [
        ('SANDBOX', 'Sandbox (Test)'),
        ('PRODUCTION', 'Production'),
        ('PARTENAIRE', 'Partenaire Stratégique'),
        ('INTERNE', 'Équipe Interne'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente d\'approbation'),
        ('ACTIF', 'Actif'),
        ('SUSPENDU', 'Suspendu'),
        ('BLOQUE', 'Bloqué'),
        ('FERME', 'Fermé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Utilisateur lié (optionnel)
    utilisateur_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Informations du compte
    nom_entreprise = models.CharField(max_length=200)
    nom_contact = models.CharField(max_length=200)
    prenom_contact = models.CharField(max_length=200, blank=True)
    courriel_contact = models.EmailField(unique=True, db_index=True)
    telephone_contact = models.CharField(max_length=20, blank=True)
    
    # Adresse
    pays = models.CharField(max_length=2, default='BI')
    ville = models.CharField(max_length=100, blank=True)
    adresse_complete = models.TextField(blank=True)
    
    # Type et statut
    type_compte = models.CharField(
        max_length=30,
        choices=TYPE_COMPTE_CHOICES,
        default='SANDBOX',
        db_index=True
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        db_index=True
    )
    raison_statut = models.TextField(blank=True)
    
    # Vérification
    courriel_verifie = models.BooleanField(default=False)
    date_verification_courriel = models.DateTimeField(null=True, blank=True)
    
    # Approbation
    approuve_par = models.UUIDField(null=True, blank=True)
    date_approbation = models.DateTimeField(null=True, blank=True)
    
    # Limites et quotas
    quota_requetes_jour = models.IntegerField(
        default=1000,
        validators=[MinValueValidator(0)]
    )
    quota_requetes_mois = models.IntegerField(
        default=30000,
        validators=[MinValueValidator(0)]
    )
    limite_taux_par_minute = models.IntegerField(
        default=60,
        validators=[MinValueValidator(1)]
    )
    
    # Webhooks
    url_webhook = models.URLField(max_length=500, blank=True)
    secret_webhook = models.CharField(max_length=255, blank=True)
    
    # Notifications
    notifications_email = models.BooleanField(default=True)
    notifications_sms = models.BooleanField(default=False)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    
    class Meta:
        db_table = 'developpeurs"."comptes_developpeurs'
        verbose_name = 'Compte Développeur'
        verbose_name_plural = 'Comptes Développeurs'
        indexes = [
            models.Index(fields=['courriel_contact']),
            models.Index(fields=['statut']),
            models.Index(fields=['type_compte']),
        ]
    
    def __str__(self):
        return f"{self.nom_entreprise} ({self.courriel_contact})"
    
    def est_actif(self):
        return self.statut == 'ACTIF' and self.courriel_verifie


class CleAPI(models.Model):
    """Clés API - developpeurs.cles_api"""
    
    ENVIRONNEMENT_CHOICES = [
        ('SANDBOX', 'Sandbox (Test)'),
        ('PRODUCTION', 'Production'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Compte développeur
    compte_developpeur = models.ForeignKey(
        CompteDeveloppeur,
        on_delete=models.CASCADE,
        related_name='cles_api'
    )
    
    # Clé API
    cle_api = models.CharField(max_length=64, unique=True, db_index=True)
    prefixe_cle = models.CharField(max_length=20)
    hash_cle = models.TextField()
    
    # Nom et description
    nom_cle = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Environnement
    environnement = models.CharField(
        max_length=20,
        choices=ENVIRONNEMENT_CHOICES,
        default='SANDBOX',
        db_index=True
    )
    
    # Permissions (scopes)
    scopes = models.JSONField(default=list)
    
    # Restrictions
    adresses_ip_autorisees = models.JSONField(default=list, blank=True)
    domaines_autorises = models.JSONField(default=list, blank=True)
    
    # Limites spécifiques
    limite_requetes_minute = models.IntegerField(null=True, blank=True)
    limite_requetes_jour = models.IntegerField(null=True, blank=True)
    
    # Statut
    est_active = models.BooleanField(default=True, db_index=True)
    date_expiration = models.DateTimeField(null=True, blank=True)
    
    # Utilisation
    derniere_utilisation = models.DateTimeField(null=True, blank=True)
    nombre_utilisations = models.BigIntegerField(default=0)
    
    # Révocation
    est_revoquee = models.BooleanField(default=False)
    date_revocation = models.DateTimeField(null=True, blank=True)
    revoquee_par = models.UUIDField(null=True, blank=True)
    raison_revocation = models.TextField(blank=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'developpeurs"."cles_api'
        verbose_name = 'Clé API'
        verbose_name_plural = 'Clés API'
        indexes = [
            models.Index(fields=['compte_developpeur']),
            models.Index(fields=['cle_api']),
            models.Index(fields=['prefixe_cle']),
            models.Index(fields=['environnement']),
        ]
    
    def __str__(self):
        return f"{self.nom_cle} ({self.prefixe_cle}***)"
    
    @staticmethod
    def generer_cle(environnement='SANDBOX'):
        """Génère une nouvelle clé API"""
        prefixe = 'ufar_live_' if environnement == 'PRODUCTION' else 'ufar_test_'
        random_part = secrets.token_urlsafe(32)[:32]
        return f"{prefixe}{random_part}", prefixe
    
    @staticmethod
    def hasher_cle(cle_complete):
        """Hash une clé API pour stockage sécurisé"""
        return hashlib.sha256(cle_complete.encode()).hexdigest()
    
    def verifier_cle(self, cle_fournie):
        """Vérifie si une clé fournie correspond à cette clé API"""
        return self.hash_cle == self.hasher_cle(cle_fournie)
    
    def est_valide(self):
        """Vérifie si la clé est valide et utilisable"""
        if not self.est_active or self.est_revoquee:
            return False
        if self.date_expiration and self.date_expiration < timezone.now():
            return False
        return self.compte_developpeur.est_actif()


class LogUtilisationAPI(models.Model):
    """Logs d'utilisation API - TABLE IMMUABLE"""
    
    id = models.BigAutoField(primary_key=True)
    
    # Clé API utilisée
    cle_api = models.ForeignKey(
        CleAPI,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    compte_developpeur = models.ForeignKey(
        CompteDeveloppeur,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    
    # Requête
    methode_http = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=500, db_index=True)
    chemin_complet = models.TextField(blank=True)
    parametres_query = models.JSONField(default=dict, blank=True)
    
    # Réponse
    statut_http = models.IntegerField(db_index=True)
    temps_reponse_ms = models.IntegerField(null=True, blank=True)
    taille_reponse_bytes = models.IntegerField(null=True, blank=True)
    
    # Erreurs
    code_erreur = models.CharField(max_length=50, blank=True)
    message_erreur = models.TextField(blank=True)
    
    # Contexte
    adresse_ip = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(blank=True)
    referer = models.TextField(blank=True)
    pays = models.CharField(max_length=2, blank=True)
    
    # Horodatage (IMMUABLE)
    date_requete = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'developpeurs"."logs_utilisation_api'
        verbose_name = 'Log Utilisation API'
        verbose_name_plural = 'Logs Utilisation API'
        indexes = [
            models.Index(fields=['cle_api']),
            models.Index(fields=['compte_developpeur']),
            models.Index(fields=['-date_requete']),
            models.Index(fields=['endpoint']),
            models.Index(fields=['statut_http']),
            models.Index(fields=['adresse_ip']),
        ]
        default_permissions = ()
        permissions = [
            ('view_log', 'Can view log utilisation API'),
            ('add_log', 'Can add log utilisation API'),
        ]
    
    def __str__(self):
        return f"{self.methode_http} {self.endpoint} - {self.statut_http}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Les logs d'utilisation API ne peuvent pas être modifiés (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Les logs d'utilisation API ne peuvent pas être supprimés (TABLE IMMUABLE)")


class QuotaUtilisation(models.Model):
    """Quotas et statistiques d'utilisation"""
    
    TYPE_PERIODE_CHOICES = [
        ('JOUR', 'Jour'),
        ('MOIS', 'Mois'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Compte et clé
    compte_developpeur = models.ForeignKey(
        CompteDeveloppeur,
        on_delete=models.CASCADE,
        related_name='quotas'
    )
    cle_api = models.ForeignKey(
        CleAPI,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='quotas'
    )
    
    # Période
    date_periode = models.DateField(db_index=True)
    type_periode = models.CharField(max_length=10, choices=TYPE_PERIODE_CHOICES)
    
    # Compteurs
    nombre_requetes = models.IntegerField(default=0)
    nombre_requetes_succes = models.IntegerField(default=0)
    nombre_requetes_erreur = models.IntegerField(default=0)
    
    # Par statut HTTP
    requetes_2xx = models.IntegerField(default=0)
    requetes_4xx = models.IntegerField(default=0)
    requetes_5xx = models.IntegerField(default=0)
    
    # Performance
    temps_reponse_moyen_ms = models.IntegerField(null=True, blank=True)
    temps_reponse_max_ms = models.IntegerField(null=True, blank=True)
    
    # Bande passante
    bande_passante_bytes = models.BigIntegerField(default=0)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'developpeurs"."quotas_utilisation'
        verbose_name = 'Quota Utilisation'
        verbose_name_plural = 'Quotas Utilisation'
        unique_together = [['compte_developpeur', 'cle_api', 'date_periode', 'type_periode']]
        indexes = [
            models.Index(fields=['compte_developpeur']),
            models.Index(fields=['cle_api']),
            models.Index(fields=['-date_periode']),
        ]
    
    def __str__(self):
        return f"{self.compte_developpeur.nom_entreprise} - {self.date_periode} ({self.type_periode})"


class Application(models.Model):
    """Applications enregistrées par les développeurs"""
    
    TYPE_APPLICATION_CHOICES = [
        ('WEB', 'Application Web'),
        ('MOBILE_IOS', 'Application Mobile iOS'),
        ('MOBILE_ANDROID', 'Application Mobile Android'),
        ('BACKEND', 'Backend/API'),
        ('PLUGIN', 'Plugin/Extension'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('EN_REVISION', 'En révision'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
        ('SUSPENDU', 'Suspendu'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Compte développeur
    compte_developpeur = models.ForeignKey(
        CompteDeveloppeur,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    # Informations
    nom_application = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url_application = models.URLField(max_length=500, blank=True)
    url_logo = models.URLField(max_length=500, blank=True)
    
    # Type
    type_application = models.CharField(
        max_length=30,
        choices=TYPE_APPLICATION_CHOICES,
        blank=True
    )
    
    # URLs
    urls_callback = models.JSONField(default=list, blank=True)
    urls_webhook = models.JSONField(default=list, blank=True)
    
    # Statut
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='BROUILLON',
        db_index=True
    )
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'developpeurs"."applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        indexes = [
            models.Index(fields=['compte_developpeur']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.nom_application} ({self.type_application})"
