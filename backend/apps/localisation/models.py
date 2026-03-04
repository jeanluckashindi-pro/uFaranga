"""
Modèles pour le schéma localisation.
Hiérarchie GADM: Pays (niveau0) → Provinces (niveau1) → Districts (niveau2) → Communes (niveau3) → Secteurs (niveau4) → Villages (niveau5)
+ Points de service
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import uuid


# =============================================================================
# TABLE DE RÉFÉRENCE PAYS (utilisée pour les ForeignKeys)
# =============================================================================

class Pays(models.Model):
    """Table de référence des pays avec UUID - utilisée pour les relations ForeignKey"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_iso_2 = models.CharField(max_length=2, unique=True, db_index=True)
    code_iso_3 = models.CharField(max_length=3, blank=True)
    nom = models.CharField(max_length=100)
    nom_anglais = models.CharField(max_length=100, blank=True)
    
    # Géographie
    continent = models.CharField(max_length=50, blank=True)
    sous_region = models.CharField(max_length=100, blank=True)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Téléphonie et langues
    code_telephonique = models.CharField(max_length=10, blank=True)
    format_telephone = models.CharField(max_length=50, blank=True)
    langue_principale = models.CharField(max_length=50, blank=True)
    langues_secondaires = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    
    # Système bancaire
    systeme_bancaire = models.CharField(max_length=50, blank=True)
    code_swift_pays = models.CharField(max_length=2, blank=True)
    autorise_mobile_money = models.BooleanField(default=True)
    autorise_crypto = models.BooleanField(default=False)
    niveau_bancarisation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Statistiques démographiques et économiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    pib_par_habitant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    taux_penetration_mobile = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    taux_penetration_internet = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    score_facilite_affaires = models.IntegerField(null=True, blank=True)
    indice_corruption = models.IntegerField(null=True, blank=True)
    
    # Gestion des risques et limites
    niveau_risque_pays = models.CharField(max_length=20, blank=True)
    exige_kyc_renforce = models.BooleanField(default=False)
    limite_transaction_journaliere = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    limite_transaction_mensuelle = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    # Statistiques agents/utilisateurs
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Géométrie GeoJSON
    geometrie_geojson = models.JSONField(null=True, blank=True)
    fuseau_horaire_id = models.UUIDField(null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = '"localisation"."pays_reference"'
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']
        managed = False

    def __str__(self):
        return f"{self.nom} ({self.code_iso_2})"


# =============================================================================
# DIVISIONS ADMINISTRATIVES GADM (lecture seule)
# =============================================================================

class DivisionNiveau0(models.Model):
    """Niveau 0 GADM - Pays (lecture seule, données géographiques)"""
    division_id = models.CharField(max_length=50, primary_key=True)
    gid_0 = models.TextField(blank=True)
    pays = models.TextField(blank=True)
    code_iso = models.TextField(blank=True)
    nom_pays = models.TextField(blank=True)
    niveau_admin = models.BigIntegerField(null=True, blank=True)
    est_autorise = models.BooleanField(default=False)
    affiche_par_defaut = models.BooleanField(default=False)
    continent_code = models.CharField(max_length=3, blank=True)
    region_code = models.CharField(max_length=3, blank=True)
    est_actif = models.BooleanField(default=False)

    class Meta:
        db_table = '"localisation"."divisions_administratives_niveau0"'
        verbose_name = 'Division Niveau 0 (Pays GADM)'
        verbose_name_plural = 'Divisions Niveau 0 (Pays GADM)'
        ordering = ['nom_pays']
        managed = False

    def __str__(self):
        return f"{self.nom_pays} ({self.code_iso})"


class DivisionNiveau1(models.Model):
    """Niveau 1 GADM - Provinces/États"""
    division_id = models.CharField(max_length=50, primary_key=True)
    pays_division_id = models.CharField(max_length=50, db_index=True)
    gid_0 = models.TextField(blank=True)
    pays = models.TextField(blank=True)
    gid_1 = models.TextField(blank=True)
    nom_1 = models.TextField(blank=True)
    nom_variante_1 = models.TextField(blank=True)
    nom_local_1 = models.TextField(blank=True)
    type_1 = models.TextField(blank=True)
    type_anglais_1 = models.TextField(blank=True)
    code_1 = models.TextField(blank=True)
    hasc_1 = models.TextField(blank=True)
    iso_1 = models.TextField(blank=True)
    code_iso = models.TextField(blank=True)
    nom_pays = models.TextField(blank=True)
    niveau_admin = models.BigIntegerField(null=True, blank=True)
    est_autorise = models.BooleanField(default=False)
    affiche_par_defaut = models.BooleanField(default=False)
    est_actif = models.BooleanField(default=False)

    class Meta:
        db_table = '"localisation"."divisions_administratives_niveau1"'
        verbose_name = 'Division Niveau 1 (Province)'
        verbose_name_plural = 'Divisions Niveau 1 (Provinces)'
        ordering = ['nom_pays', 'nom_1']
        managed = False

    def __str__(self):
        return f"{self.nom_1} ({self.pays})"


class DivisionNiveau2(models.Model):
    """Niveau 2 GADM - Districts/Territoires"""
    division_id = models.CharField(max_length=50, primary_key=True)
    pays_division_id = models.CharField(max_length=50, db_index=True)
    parent_division_id = models.CharField(max_length=50, db_index=True)
    gid_0 = models.TextField(blank=True)
    pays = models.TextField(blank=True)
    gid_1 = models.TextField(blank=True)
    nom_1 = models.TextField(blank=True)
    nom_local_1 = models.TextField(blank=True)
    gid_2 = models.TextField(blank=True)
    nom_2 = models.TextField(blank=True)
    nom_variante_2 = models.TextField(blank=True)
    nom_local_2 = models.TextField(blank=True)
    type_2 = models.TextField(blank=True)
    type_anglais_2 = models.TextField(blank=True)
    code_2 = models.TextField(blank=True)
    hasc_2 = models.TextField(blank=True)
    code_iso = models.TextField(blank=True)
    nom_pays = models.TextField(blank=True)
    niveau_admin = models.BigIntegerField(null=True, blank=True)
    est_autorise = models.BooleanField(default=False)
    affiche_par_defaut = models.BooleanField(default=False)
    est_actif = models.BooleanField(default=False)

    class Meta:
        db_table = '"localisation"."divisions_administratives_niveau2"'
        verbose_name = 'Division Niveau 2 (District)'
        verbose_name_plural = 'Divisions Niveau 2 (Districts)'
        ordering = ['nom_pays', 'nom_1', 'nom_2']
        managed = False

    def __str__(self):
        return f"{self.nom_2} ({self.nom_1}, {self.pays})"


# =============================================================================
# ALIAS POUR COMPATIBILITÉ
# =============================================================================

# Alias pour faciliter l'utilisation
Province = DivisionNiveau1
District = DivisionNiveau2
Commune = DivisionNiveau2  # Peut être niveau 2 ou 3 selon le pays
Secteur = DivisionNiveau2
Quartier = DivisionNiveau2


# =============================================================================
# POINTS DE SERVICE
# =============================================================================

class PointDeService(models.Model):
    """Points de service (agents, guichets, partenaires)"""
    TYPE_POINT_CHOICES = [
        ('AGENT', 'Agent'),
        ('GUICHET', 'Guichet'),
        ('PARTENAIRE', 'Partenaire'),
        ('AUTRE', 'Autre'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quartier_id = models.UUIDField(null=True, blank=True, db_index=True)
    code = models.CharField(max_length=30, blank=True)
    nom = models.CharField(max_length=100, blank=True)
    type_point = models.CharField(max_length=20, blank=True)
    
    # Localisation
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    altitude_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    precision_gps_m = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    adresse_complementaire = models.TextField(blank=True)
    
    # Relations
    agent_utilisateur_id = models.UUIDField(null=True, blank=True)
    
    # Statistiques
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Géométrie
    zone_couverture_geojson = models.JSONField(null=True, blank=True)
    rayon_couverture_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = '"localisation"."points_service"'
        verbose_name = 'Point de service'
        verbose_name_plural = 'Points de service'
        ordering = ['nom']
        managed = False

    def __str__(self):
        return f"{self.nom} ({self.type_point})"



# =============================================================================
# TABLES DE GESTION GÉOGRAPHIQUE
# =============================================================================

class FuseauHoraire(models.Model):
    """Fuseaux horaires"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    offset_utc = models.CharField(max_length=10)
    offset_minutes = models.IntegerField()
    description = models.TextField(blank=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"localisation"."fuseaux_horaires"'
        verbose_name = 'Fuseau horaire'
        verbose_name_plural = 'Fuseaux horaires'
        ordering = ['offset_minutes']
        managed = False

    def __str__(self):
        return f"{self.nom} ({self.offset_utc})"


class ZoneRisque(models.Model):
    """Zones à risque pour la conformité et la sécurité"""
    NIVEAU_RISQUE_CHOICES = [
        ('FAIBLE', 'Faible'),
        ('MOYEN', 'Moyen'),
        ('ELEVE', 'Élevé'),
        ('TRES_ELEVE', 'Très élevé'),
        ('CRITIQUE', 'Critique'),
    ]
    
    TYPE_RISQUE_CHOICES = [
        ('FRAUDE', 'Fraude'),
        ('BLANCHIMENT', 'Blanchiment'),
        ('TERRORISME', 'Terrorisme'),
        ('CRIMINALITE', 'Criminalité'),
        ('INSTABILITE', 'Instabilité'),
        ('AUTRE', 'Autre'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='zones_risque')
    province_id = models.UUIDField(null=True, blank=True)
    district_id = models.UUIDField(null=True, blank=True)
    quartier_id = models.UUIDField(null=True, blank=True)
    
    niveau_risque = models.CharField(max_length=20, choices=NIVEAU_RISQUE_CHOICES)
    type_risque = models.CharField(max_length=50, choices=TYPE_RISQUE_CHOICES)
    score_risque = models.IntegerField(help_text='Score de 0 à 100')
    description = models.TextField(blank=True)
    mesures_mitigation = models.TextField(blank=True)
    
    verification_renforcee = models.BooleanField(default=False)
    limite_transaction = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    date_evaluation = models.DateField()
    date_prochaine_evaluation = models.DateField(null=True, blank=True)
    
    est_actif = models.BooleanField(default=True, db_index=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"localisation"."zones_risque"'
        verbose_name = 'Zone à risque'
        verbose_name_plural = 'Zones à risque'
        ordering = ['-score_risque', 'niveau_risque']
        managed = False

    def __str__(self):
        return f"{self.pays.nom} - {self.niveau_risque} ({self.type_risque})"


class RestrictionGeographique(models.Model):
    """Restrictions géographiques pour les transactions"""
    NIVEAU_RESTRICTION_CHOICES = [
        ('FAIBLE', 'Faible'),
        ('MOYEN', 'Moyen'),
        ('ELEVE', 'Élevé'),
        ('TOTAL', 'Total'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='restrictions')
    
    type_restriction = models.CharField(max_length=50)
    niveau_restriction = models.CharField(max_length=20, choices=NIVEAU_RESTRICTION_CHOICES)
    description = models.TextField(blank=True)
    
    autorise_transactions = models.BooleanField(default=True)
    autorise_transferts_entrants = models.BooleanField(default=True)
    autorise_transferts_sortants = models.BooleanField(default=True)
    montant_max_journalier = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    montant_max_mensuel = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    
    est_actif = models.BooleanField(default=True, db_index=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"localisation"."restrictions_geographiques"'
        verbose_name = 'Restriction géographique'
        verbose_name_plural = 'Restrictions géographiques'
        ordering = ['-date_debut']
        managed = False

    def __str__(self):
        return f"{self.pays.nom} - {self.type_restriction} ({self.niveau_restriction})"
    
    def est_en_vigueur(self):
        """Vérifie si la restriction est actuellement en vigueur"""
        from datetime import date
        aujourd_hui = date.today()
        if not self.est_actif:
            return False
        if self.date_debut > aujourd_hui:
            return False
        if self.date_fin and self.date_fin < aujourd_hui:
            return False
        return True


class CorridorPaiement(models.Model):
    """Corridors de paiement entre pays"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    
    pays_origine = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='corridors_sortants', db_column='pays_origine_id')
    pays_destination = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='corridors_entrants', db_column='pays_destination_id')
    
    volume_transactions_mensuel = models.BigIntegerField(default=0)
    montant_moyen = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    delai_moyen_heures = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    taux_commission = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    est_prioritaire = models.BooleanField(default=False)
    est_actif = models.BooleanField(default=True, db_index=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"localisation"."corridors_paiement"'
        verbose_name = 'Corridor de paiement'
        verbose_name_plural = 'Corridors de paiement'
        ordering = ['-volume_transactions_mensuel']
        managed = False

    def __str__(self):
        return f"{self.pays_origine.code_iso_2} → {self.pays_destination.code_iso_2}"
