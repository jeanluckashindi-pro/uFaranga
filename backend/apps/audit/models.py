"""
Modèles pour le schéma AUDIT
Traçabilité complète - TOUTES LES TABLES SONT IMMUABLES
"""
from django.db import models
from django.utils import timezone
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
import uuid


class SessionUtilisateur(models.Model):
    """Sessions utilisateurs - audit.sessions_utilisateurs"""
    
    TYPE_APPAREIL_CHOICES = [
        ('MOBILE', 'Mobile'),
        ('WEB', 'Web'),
        ('TABLETTE', 'Tablette'),
        ('API', 'API'),
    ]
    
    RAISON_DECONNEXION_CHOICES = [
        ('UTILISATEUR', 'Utilisateur'),
        ('EXPIRATION', 'Expiration'),
        ('SYSTEME', 'Système'),
        ('SECURITE', 'Sécurité'),
        ('FORCEE', 'Forcée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Session
    cle_session = models.CharField(max_length=255, unique=True)
    jeton_rafraichissement = models.TextField(blank=True)
    
    # Informations de connexion
    adresse_ip = models.GenericIPAddressField(db_index=True)
    agent_utilisateur = models.TextField(blank=True)
    type_appareil = models.CharField(
        max_length=20,
        choices=TYPE_APPAREIL_CHOICES,
        blank=True
    )
    id_appareil = models.CharField(max_length=255, blank=True)
    empreinte_appareil = models.CharField(max_length=255, blank=True)
    
    # Localisation
    pays_connexion = models.CharField(max_length=2, blank=True)
    ville_connexion = models.CharField(max_length=100, blank=True)
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
    fournisseur_internet = models.CharField(max_length=100, blank=True)
    
    # Statut de la session
    est_active = models.BooleanField(default=True, db_index=True)
    
    # Dates
    date_connexion = models.DateTimeField(default=timezone.now, db_index=True)
    date_deconnexion = models.DateTimeField(null=True, blank=True)
    derniere_activite = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField()
    
    # Durée
    duree_session_secondes = models.IntegerField(null=True, blank=True)
    
    # Raison de déconnexion
    raison_deconnexion = models.CharField(
        max_length=50,
        choices=RAISON_DECONNEXION_CHOICES,
        blank=True
    )
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'audit"."sessions_utilisateurs'
        verbose_name = 'Session Utilisateur'
        verbose_name_plural = 'Sessions Utilisateurs'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['-date_connexion']),
            models.Index(fields=['adresse_ip']),
        ]
    
    def __str__(self):
        return f"Session {self.utilisateur_id} - {self.date_connexion}"


class JournalEvenement(models.Model):
    """Journal COMPLET de tous les événements - TABLE IMMUABLE"""
    
    CATEGORIE_EVENEMENT_CHOICES = [
        ('AUTHENTIFICATION', 'Authentification'),
        ('AUTORISATION', 'Autorisation'),
        ('TRANSACTION_FINANCIERE', 'Transaction Financière'),
        ('MODIFICATION_DONNEES', 'Modification Données'),
        ('CONSULTATION_DONNEES', 'Consultation Données'),
        ('CONFIGURATION_SYSTEME', 'Configuration Système'),
        ('SECURITE', 'Sécurité'),
        ('ERREUR', 'Erreur'),
        ('ALERTE', 'Alerte'),
        ('SYNCHRONISATION_BANCAIRE', 'Synchronisation Bancaire'),
        ('NOTIFICATION', 'Notification'),
        ('KYC_COMPLIANCE', 'KYC Compliance'),
    ]
    
    RESULTAT_CHOICES = [
        ('SUCCES', 'Succès'),
        ('ECHEC', 'Échec'),
        ('PARTIEL', 'Partiel'),
        ('EN_COURS', 'En cours'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    
    # Corrélation
    id_requete = models.UUIDField(db_index=True)
    id_correlation = models.UUIDField(null=True, blank=True)
    
    # Utilisateur et session
    utilisateur_id = models.UUIDField(null=True, blank=True, db_index=True)
    session_id = models.UUIDField(null=True, blank=True)
    
    # Type d'événement
    categorie_evenement = models.CharField(
        max_length=50,
        choices=CATEGORIE_EVENEMENT_CHOICES,
        db_index=True
    )
    action = models.CharField(max_length=100, db_index=True)
    
    # Ressource affectée
    type_ressource = models.CharField(max_length=50, blank=True)
    id_ressource = models.CharField(max_length=100, blank=True)
    
    # Détails de l'action
    description = models.TextField()
    resultat = models.CharField(max_length=20, choices=RESULTAT_CHOICES)
    
    # Contexte technique
    nom_service = models.CharField(max_length=50, blank=True)
    nom_module = models.CharField(max_length=100, blank=True)
    nom_fonction = models.CharField(max_length=100, blank=True)
    point_terminaison = models.CharField(max_length=255, blank=True)
    methode_http = models.CharField(max_length=10, blank=True)
    statut_http = models.IntegerField(null=True, blank=True)
    
    # Performance
    temps_execution_ms = models.IntegerField(null=True, blank=True)
    
    # Informations réseau
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    agent_utilisateur = models.TextField(blank=True)
    id_appareil = models.CharField(max_length=255, blank=True)
    
    # Localisation
    pays = models.CharField(max_length=2, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    
    # Données de la requête/réponse (sanitized)
    corps_requete = models.JSONField(null=True, blank=True)
    corps_reponse = models.JSONField(null=True, blank=True)
    
    # Erreurs
    code_erreur = models.CharField(max_length=50, blank=True)
    message_erreur = models.TextField(blank=True)
    trace_erreur = models.TextField(blank=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    # Horodatage (IMMUABLE)
    date_evenement = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Index de recherche full-text
    recherche_texte = SearchVectorField(null=True)
    
    class Meta:
        db_table = 'audit"."journaux_evenements'
        verbose_name = 'Journal Événement'
        verbose_name_plural = 'Journaux Événements'
        indexes = [
            models.Index(fields=['id_requete']),
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['session_id']),
            models.Index(fields=['categorie_evenement']),
            models.Index(fields=['action']),
            models.Index(fields=['-date_evenement']),
            models.Index(fields=['resultat']),
            models.Index(fields=['adresse_ip']),
            models.Index(fields=['utilisateur_id', '-date_evenement']),
            models.Index(fields=['categorie_evenement', '-date_evenement']),
            GinIndex(fields=['metadonnees']),
            GinIndex(fields=['corps_requete']),
            GinIndex(fields=['corps_reponse']),
        ]
        # TABLE IMMUABLE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_journal', 'Can view journal événement'),
            ('add_journal', 'Can add journal événement'),
        ]
    
    def __str__(self):
        return f"{self.categorie_evenement} - {self.action} - {self.date_evenement}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Les journaux d'événements ne peuvent pas être modifiés (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Les journaux d'événements ne peuvent pas être supprimés (TABLE IMMUABLE)")


class HistoriqueModification(models.Model):
    """Historique des modifications de données critiques - TABLE IMMUABLE"""
    
    OPERATION_CHOICES = [
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    
    # Table et enregistrement modifiés
    nom_table = models.CharField(max_length=100, db_index=True)
    nom_schema = models.CharField(max_length=50)
    id_enregistrement = models.CharField(max_length=100, db_index=True)
    
    # Type d'opération
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES, db_index=True)
    
    # Utilisateur
    utilisateur_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Données avant/après
    donnees_avant = models.JSONField(null=True, blank=True)
    donnees_apres = models.JSONField(null=True, blank=True)
    champs_modifies = models.JSONField(default=list, blank=True)
    
    # Contexte
    raison_modification = models.TextField(blank=True)
    id_requete = models.UUIDField(null=True, blank=True)
    
    # Horodatage
    date_modification = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'audit"."historique_modifications'
        verbose_name = 'Historique Modification'
        verbose_name_plural = 'Historique Modifications'
        indexes = [
            models.Index(fields=['nom_schema', 'nom_table']),
            models.Index(fields=['id_enregistrement']),
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['-date_modification']),
            models.Index(fields=['operation']),
        ]
        # TABLE IMMUABLE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_historique', 'Can view historique modification'),
            ('add_historique', 'Can add historique modification'),
        ]
    
    def __str__(self):
        return f"{self.operation} - {self.nom_table} - {self.date_modification}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("L'historique des modifications ne peut pas être modifié (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("L'historique des modifications ne peut pas être supprimé (TABLE IMMUABLE)")
