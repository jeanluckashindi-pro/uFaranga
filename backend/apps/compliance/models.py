"""
Modèles pour le schéma COMPLIANCE
KYC, AML, et conformité réglementaire
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class DocumentKYC(models.Model):
    """Documents KYC - compliance.documents_kyc"""
    
    TYPE_DOCUMENT_CHOICES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('PASSEPORT', 'Passeport'),
        ('PERMIS_CONDUIRE', 'Permis de Conduire'),
        ('CARTE_ELECTEUR', 'Carte d\'Électeur'),
        ('SELFIE', 'Photo du visage'),
        ('SELFIE_AVEC_DOCUMENT', 'Selfie tenant le document'),
        ('JUSTIFICATIF_DOMICILE', 'Justificatif de domicile'),
        ('ATTESTATION_RESIDENCE', 'Attestation de résidence'),
        ('EXTRAIT_NAISSANCE', 'Extrait de naissance'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_VERIFICATION_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
        ('EXPIRE', 'Expiré'),
        ('SUSPENDU', 'Suspendu'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Type de document
    type_document = models.CharField(
        max_length=50,
        choices=TYPE_DOCUMENT_CHOICES,
        db_index=True
    )
    
    # Informations du document
    numero_document = models.CharField(max_length=100, blank=True)
    date_emission = models.DateField(null=True, blank=True)
    date_expiration = models.DateField(null=True, blank=True, db_index=True)
    autorite_emission = models.CharField(max_length=200, blank=True)
    pays_emission = models.CharField(max_length=2)
    
    # Fichiers
    url_fichier_recto = models.URLField(max_length=500)
    url_fichier_verso = models.URLField(max_length=500, blank=True)
    url_fichier_selfie = models.URLField(max_length=500, blank=True)
    hash_fichier_recto = models.CharField(max_length=255, blank=True)
    hash_fichier_verso = models.CharField(max_length=255, blank=True)
    
    # Statut de vérification
    statut_verification = models.CharField(
        max_length=20,
        choices=STATUT_VERIFICATION_CHOICES,
        default='EN_ATTENTE',
        db_index=True
    )
    
    # Vérification
    verifie_par = models.UUIDField(null=True, blank=True)
    date_verification = models.DateTimeField(null=True, blank=True)
    methode_verification = models.CharField(max_length=50, blank=True)
    score_confiance = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Données extraites (OCR)
    donnees_extraites = models.JSONField(default=dict, blank=True)
    
    # Raisons
    raison_rejet = models.TextField(blank=True)
    commentaire_verificateur = models.TextField(blank=True)
    
    # Expiration
    alerte_expiration_envoyee = models.BooleanField(default=False)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'compliance"."documents_kyc'
        verbose_name = 'Document KYC'
        verbose_name_plural = 'Documents KYC'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['type_document']),
            models.Index(fields=['statut_verification']),
        ]
    
    def __str__(self):
        return f"{self.type_document} - {self.utilisateur_id}"


class VerificationKYC(models.Model):
    """Vérifications KYC effectuées - TABLE IMMUABLE"""
    
    TYPE_VERIFICATION_CHOICES = [
        ('IDENTITE', 'Identité'),
        ('ADRESSE', 'Adresse'),
        ('TELEPHONE', 'Téléphone'),
        ('EMAIL', 'Email'),
        ('BIOMETRIE_FACIALE', 'Biométrie Faciale'),
        ('BIOMETRIE_EMPREINTE', 'Biométrie Empreinte'),
        ('LIVENESS_CHECK', 'Liveness Check'),
        ('VERIFICATION_BANCAIRE', 'Vérification Bancaire'),
        ('VERIFICATION_CREDIT', 'Vérification Crédit'),
        ('AML_SCREENING', 'AML Screening'),
    ]
    
    RESULTAT_CHOICES = [
        ('SUCCES', 'Succès'),
        ('ECHEC', 'Échec'),
        ('PARTIEL', 'Partiel'),
        ('EN_ATTENTE', 'En attente'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Type de vérification
    type_verification = models.CharField(
        max_length=50,
        choices=TYPE_VERIFICATION_CHOICES,
        db_index=True
    )
    
    # Résultat
    resultat = models.CharField(
        max_length=20,
        choices=RESULTAT_CHOICES,
        db_index=True
    )
    score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Détails
    fournisseur_verification = models.CharField(max_length=100, blank=True)
    reference_externe = models.CharField(max_length=100, blank=True)
    donnees_verification = models.JSONField(default=dict, blank=True)
    
    # Raisons
    raison_echec = models.TextField(blank=True)
    recommandations = models.TextField(blank=True)
    
    # Horodatage (IMMUABLE)
    date_verification = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'compliance"."verifications_kyc'
        verbose_name = 'Vérification KYC'
        verbose_name_plural = 'Vérifications KYC'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['type_verification']),
            models.Index(fields=['resultat']),
            models.Index(fields=['-date_verification']),
        ]
        # TABLE IMMUABLE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_verification', 'Can view vérification KYC'),
            ('add_verification', 'Can add vérification KYC'),
        ]
    
    def __str__(self):
        return f"{self.type_verification} - {self.resultat} - {self.date_verification}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Les vérifications KYC ne peuvent pas être modifiées (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Les vérifications KYC ne peuvent pas être supprimées (TABLE IMMUABLE)")


class ScreeningAML(models.Model):
    """Screening Anti-Money Laundering - TABLE IMMUABLE"""
    
    TYPE_SCREENING_CHOICES = [
        ('SANCTIONS', 'Sanctions'),
        ('PEP', 'Politically Exposed Person'),
        ('ADVERSE_MEDIA', 'Adverse Media'),
        ('WATCHLIST', 'Watchlist'),
        ('COMPLET', 'Complet'),
    ]
    
    RESULTAT_CHOICES = [
        ('CLEAN', 'Clean'),
        ('MATCH_POSSIBLE', 'Match Possible'),
        ('MATCH_CONFIRME', 'Match Confirmé'),
        ('ERREUR', 'Erreur'),
    ]
    
    NIVEAU_RISQUE_CHOICES = [
        ('FAIBLE', 'Faible'),
        ('MOYEN', 'Moyen'),
        ('ELEVE', 'Élevé'),
        ('CRITIQUE', 'Critique'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Type de screening
    type_screening = models.CharField(
        max_length=50,
        choices=TYPE_SCREENING_CHOICES
    )
    
    # Résultat
    resultat = models.CharField(
        max_length=20,
        choices=RESULTAT_CHOICES,
        db_index=True
    )
    score_risque = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    niveau_risque = models.CharField(
        max_length=20,
        choices=NIVEAU_RISQUE_CHOICES,
        blank=True,
        db_index=True
    )
    
    # Détails du match
    donnees_match = models.JSONField(default=dict, blank=True)
    listes_matchees = models.JSONField(default=list, blank=True)
    
    # Actions
    action_requise = models.BooleanField(default=False, db_index=True)
    action_prise = models.TextField(blank=True)
    prise_en_charge_par = models.UUIDField(null=True, blank=True)
    date_prise_en_charge = models.DateTimeField(null=True, blank=True)
    
    # Fournisseur
    fournisseur_screening = models.CharField(max_length=100, blank=True)
    reference_externe = models.CharField(max_length=100, blank=True)
    
    # Horodatage (IMMUABLE)
    date_screening = models.DateTimeField(default=timezone.now, db_index=True)
    
    # Métadonnées
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'compliance"."screening_aml'
        verbose_name = 'Screening AML'
        verbose_name_plural = 'Screenings AML'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['resultat']),
            models.Index(fields=['niveau_risque']),
            models.Index(fields=['-date_screening']),
        ]
        # TABLE IMMUABLE
        default_permissions = ()  # Désactive les permissions par défaut
        permissions = [
            ('view_screening', 'Can view screening AML'),
            ('add_screening', 'Can add screening AML'),
        ]
    
    def __str__(self):
        return f"{self.type_screening} - {self.resultat} - {self.date_screening}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Les screenings AML ne peuvent pas être modifiés (TABLE IMMUABLE)")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise ValueError("Les screenings AML ne peuvent pas être supprimés (TABLE IMMUABLE)")
