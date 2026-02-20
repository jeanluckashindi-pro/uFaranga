"""
Modèles pour le schéma IDENTITE
Gestion des utilisateurs, profils et authentification
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
import uuid


# =============================================================================
# TABLES DE RÉFÉRENCE
# =============================================================================

class TypeUtilisateur(models.Model):
    """Types d'utilisateurs - identite.types_utilisateurs"""
    
    code = models.CharField(max_length=20, primary_key=True, unique=True)
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    ordre_affichage = models.IntegerField(default=0)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'identite"."types_utilisateurs'
        verbose_name = 'Type Utilisateur'
        verbose_name_plural = 'Types Utilisateurs'
        ordering = ['ordre_affichage', 'libelle']
    
    def __str__(self):
        return self.libelle


class NiveauKYC(models.Model):
    """Niveaux KYC - identite.niveaux_kyc"""
    
    niveau = models.IntegerField(primary_key=True, unique=True)
    libelle = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')
    limite_transaction_journaliere = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Limite de transaction journalière en devise locale'
    )
    limite_solde_maximum = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text='Solde maximum autorisé'
    )
    documents_requis = models.JSONField(
        default=list, 
        blank=True,
        help_text='Liste des documents requis pour ce niveau'
    )
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'identite"."niveaux_kyc'
        verbose_name = 'Niveau KYC'
        verbose_name_plural = 'Niveaux KYC'
        ordering = ['niveau']
    
    def __str__(self):
        return f"Niveau {self.niveau} - {self.libelle}"


class StatutUtilisateur(models.Model):
    """Statuts utilisateurs - identite.statuts_utilisateurs"""
    
    code = models.CharField(max_length=20, primary_key=True, unique=True)
    libelle = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    couleur = models.CharField(
        max_length=7, 
        default='#000000',
        help_text='Couleur hexadécimale pour l\'affichage (ex: #FF0000)'
    )
    permet_connexion = models.BooleanField(
        default=True,
        help_text='Si False, l\'utilisateur ne peut pas se connecter'
    )
    permet_transactions = models.BooleanField(
        default=True,
        help_text='Si False, l\'utilisateur ne peut pas effectuer de transactions'
    )
    ordre_affichage = models.IntegerField(default=0)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'identite"."statuts_utilisateurs'
        verbose_name = 'Statut Utilisateur'
        verbose_name_plural = 'Statuts Utilisateurs'
        ordering = ['ordre_affichage', 'libelle']
    
    def __str__(self):
        return self.libelle


class UtilisateurManager(BaseUserManager):
    """Manager personnalisé pour le modèle Utilisateur"""
    
    def create_user(self, courriel, numero_telephone, mot_de_passe=None, **extra_fields):
        if not courriel:
            raise ValueError('L\'adresse courriel est obligatoire')
        if not numero_telephone:
            raise ValueError('Le numéro de téléphone est obligatoire')
        
        courriel = self.normalize_email(courriel)
        
        # Définir les valeurs par défaut pour les ForeignKeys
        if 'type_utilisateur' not in extra_fields:
            extra_fields['type_utilisateur'] = TypeUtilisateur.objects.get(code='CLIENT')
        if 'niveau_kyc' not in extra_fields:
            extra_fields['niveau_kyc'] = NiveauKYC.objects.get(niveau=0)
        if 'statut' not in extra_fields:
            extra_fields['statut'] = StatutUtilisateur.objects.get(code='ACTIF')
        
        user = self.model(courriel=courriel, numero_telephone=numero_telephone, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, courriel, numero_telephone, mot_de_passe=None, **extra_fields):
        extra_fields['type_utilisateur'] = TypeUtilisateur.objects.get(code='SUPER_ADMIN')
        extra_fields['niveau_kyc'] = NiveauKYC.objects.get(niveau=3)
        extra_fields['statut'] = StatutUtilisateur.objects.get(code='ACTIF')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(courriel, numero_telephone, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """Table principale des utilisateurs - identite.utilisateurs"""
    
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
    # Mot de passe : colonne en base = hash_mot_de_passe (AbstractBaseUser utilise "password")
    password = models.CharField(max_length=255, db_column='hash_mot_de_passe')
    # Dernière connexion : colonne en base = derniere_connexion (AbstractBaseUser utilise "last_login")
    last_login = models.DateTimeField(blank=True, null=True, db_column='derniere_connexion')

    # Informations personnelles
    prenom = models.CharField(max_length=100, default='')
    nom_famille = models.CharField(max_length=100, default='')
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, blank=True, default='')
    nationalite = models.CharField(max_length=2, default='BI')
    
    # Adresse
    pays_residence = models.CharField(max_length=2, default='BI')
    province = models.CharField(max_length=100, blank=True, default='')
    ville = models.CharField(max_length=100, blank=True, default='')
    commune = models.CharField(max_length=100, blank=True, default='')
    quartier = models.CharField(max_length=100, blank=True, default='')
    avenue = models.CharField(max_length=100, blank=True, default='')
    numero_maison = models.CharField(max_length=50, blank=True, default='')
    adresse_complete = models.TextField(blank=True, default='')
    code_postal = models.CharField(max_length=20, blank=True, default='')
    
    # Localisation (hiérarchie géo : Pays → Province → District → Quartier → Point de service)
    pays = models.ForeignKey('localisation.Pays', on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs_identite')
    province_geo = models.ForeignKey('localisation.Province', on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs_identite', db_column='province_id')
    district = models.ForeignKey('localisation.District', on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs_identite')
    quartier_geo = models.ForeignKey('localisation.Quartier', on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs_identite', db_column='quartier_id')
    point_de_service = models.ForeignKey('localisation.PointDeService', on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs_identite')
    
    # Vérifications
    telephone_verifie = models.BooleanField(default=False)
    telephone_verifie_le = models.DateTimeField(null=True, blank=True)
    courriel_verifie = models.BooleanField(default=False)
    courriel_verifie_le = models.DateTimeField(null=True, blank=True)
    
    # Relations vers tables de référence (REFACTORED)
    type_utilisateur = models.ForeignKey(
        TypeUtilisateur,
        on_delete=models.PROTECT,
        related_name='utilisateurs',
        db_column='type_utilisateur'
    )
    niveau_kyc = models.ForeignKey(
        NiveauKYC,
        on_delete=models.PROTECT,
        related_name='utilisateurs',
        db_column='niveau_kyc'
    )
    statut = models.ForeignKey(
        StatutUtilisateur,
        on_delete=models.PROTECT,
        related_name='utilisateurs',
        db_column='statut'
    )
    
    date_validation_kyc = models.DateTimeField(null=True, blank=True)
    validateur_kyc_id = models.UUIDField(null=True, blank=True)
    raison_statut = models.TextField(blank=True, default='')
    
    # Sécurité
    nombre_tentatives_connexion = models.IntegerField(default=0)
    bloque_jusqua = models.DateTimeField(null=True, blank=True)
    double_auth_activee = models.BooleanField(default=False)
    secret_2fa = models.CharField(max_length=255, blank=True, default='')
    
    # Métadonnées
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now, db_index=True)
    date_modification = models.DateTimeField(auto_now=True)
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
            self.statut.permet_transactions and
            self.telephone_verifie and
            self.niveau_kyc.niveau >= 1
        )


# =============================================================================
# GESTION DES NUMÉROS DE TÉLÉPHONE
# =============================================================================

class NumeroTelephone(models.Model):
    """Numéros de téléphone des utilisateurs - identite.numeros_telephone"""
    
    TYPE_NUMERO_CHOICES = [
        ('MOBILE', 'Mobile'),
        ('FIXE', 'Fixe'),
        ('VOIP', 'VoIP'),
    ]
    
    USAGE_CHOICES = [
        ('PERSONNEL', 'Personnel'),
        ('PROFESSIONNEL', 'Professionnel'),
        ('URGENCE', 'Urgence'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('SUSPENDU', 'Suspendu'),
        ('BLOQUE', 'Bloqué'),
        ('SUPPRIME', 'Supprimé'),
    ]
    
    TYPE_LIGNE_CHOICES = [
        ('PREPAYE', 'Prépayé'),
        ('POSTPAYE', 'Postpayé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Utilisateur
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='numeros_telephone'
    )
    
    # Pays (code ISO au lieu de FK)
    pays_code_iso_2 = models.CharField(max_length=2, db_index=True)
    code_pays = models.CharField(max_length=10)
    
    # Numéro
    numero_national = models.CharField(max_length=20)
    numero_complet = models.CharField(max_length=30, unique=True, db_index=True)
    numero_formate = models.CharField(max_length=30, blank=True)
    
    # Type et usage
    type_numero = models.CharField(max_length=20, choices=TYPE_NUMERO_CHOICES, default='MOBILE')
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, default='PERSONNEL')
    est_principal = models.BooleanField(default=False, db_index=True)
    
    # Vérification
    est_verifie = models.BooleanField(default=False, db_index=True)
    date_verification = models.DateTimeField(null=True, blank=True)
    methode_verification = models.CharField(max_length=50, blank=True)
    code_verification_hash = models.CharField(max_length=255, blank=True)
    tentatives_verification = models.IntegerField(default=0)
    derniere_tentative_verification = models.DateTimeField(null=True, blank=True)
    
    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF', db_index=True)
    raison_statut = models.TextField(blank=True)
    date_changement_statut = models.DateTimeField(null=True, blank=True)
    
    # Sécurité
    nombre_connexions_reussies = models.IntegerField(default=0)
    nombre_connexions_echouees = models.IntegerField(default=0)
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    derniere_connexion_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Opérateur
    operateur = models.CharField(max_length=100, blank=True)
    type_ligne = models.CharField(max_length=20, choices=TYPE_LIGNE_CHOICES, null=True, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    date_suppression = models.DateTimeField(null=True, blank=True)
    cree_par = models.UUIDField(null=True, blank=True)
    modifie_par = models.UUIDField(null=True, blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'identite"."numeros_telephone'
        verbose_name = 'Numéro de Téléphone'
        verbose_name_plural = 'Numéros de Téléphone'
        indexes = [
            models.Index(fields=['utilisateur']),
            models.Index(fields=['pays_code_iso_2']),
            models.Index(fields=['numero_complet']),
            models.Index(fields=['statut']),
            models.Index(fields=['est_verifie']),
        ]
    
    def __str__(self):
        return f"{self.numero_complet} ({self.utilisateur.nom_complet})"
    
    def formater_numero(self):
        """Formate le numéro selon le pays"""
        # Récupérer le format depuis les métadonnées du pays
        from apps.localisation.models import Pays
        try:
            pays = Pays.objects.get(code_iso_2=self.pays_code_iso_2)
            format_national = pays.metadonnees.get('telephonie', {}).get('format_numero_national', '')
            if format_national:
                # Logique de formatage basique
                numero_sans_code = self.numero_national
                return f"{self.code_pays} {numero_sans_code}"
        except:
            pass
        return self.numero_complet


class HistoriqueNumeroTelephone(models.Model):
    """Historique des changements sur les numéros - identite.historique_numeros_telephone"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    numero_telephone = models.ForeignKey(
        NumeroTelephone,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='historique_numeros'
    )
    
    action = models.CharField(max_length=50)
    ancien_statut = models.CharField(max_length=20, blank=True)
    nouveau_statut = models.CharField(max_length=20, blank=True)
    
    raison = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    date_action = models.DateTimeField(default=timezone.now, db_index=True)
    effectue_par = models.UUIDField(null=True, blank=True)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'identite"."historique_numeros_telephone'
        verbose_name = 'Historique Numéro Téléphone'
        verbose_name_plural = 'Historiques Numéros Téléphone'
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['numero_telephone']),
            models.Index(fields=['utilisateur']),
            models.Index(fields=['-date_action']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.numero_telephone.numero_complet} - {self.date_action}"


class LimiteNumerosParPays(models.Model):
    """Limites de numéros par pays et type d'utilisateur - identite.limites_numeros_par_pays"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    pays_code_iso_2 = models.CharField(max_length=2)
    type_utilisateur = models.ForeignKey(
        TypeUtilisateur,
        on_delete=models.CASCADE,
        related_name='limites_numeros'
    )
    
    nombre_max_numeros = models.IntegerField(default=3)
    nombre_max_numeros_verifies = models.IntegerField(default=2)
    
    autorise_numeros_etrangers = models.BooleanField(default=False)
    pays_autorises_codes = models.JSONField(default=list, blank=True)
    
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'identite"."limites_numeros_par_pays'
        verbose_name = 'Limite Numéros par Pays'
        verbose_name_plural = 'Limites Numéros par Pays'
        unique_together = [('pays_code_iso_2', 'type_utilisateur')]
    
    def __str__(self):
        return f"{self.pays_code_iso_2} - {self.type_utilisateur.code} - Max: {self.nombre_max_numeros}"


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
