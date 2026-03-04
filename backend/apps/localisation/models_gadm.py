"""
Modèles GADM pour le schéma localisation
Structure: ADM0 (Pays) → ADM1 (Provinces) → ADM2 (Territoires) → ADM3 (Secteurs) → ADM4 (Groupements) → ADM5 (Villages)
"""
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import uuid


class Pays(models.Model):
    """ADM0 - Niveau Pays"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_iso_2 = models.CharField(max_length=2, unique=True, db_index=True)
    code_iso_3 = models.CharField(max_length=3, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    nom_anglais = models.CharField(max_length=100, blank=True)
    
    # Géographie
    continent = models.CharField(max_length=50, blank=True, db_index=True)
    sous_region = models.CharField(max_length=100, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Téléphonie
    code_telephonique = models.CharField(max_length=10, blank=True)
    format_telephone = models.CharField(max_length=50, blank=True)
    langue_principale = models.CharField(max_length=50, blank=True)
    langues_secondaires = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    
    # Système bancaire
    systeme_bancaire = models.CharField(max_length=50, blank=True)
    autorise_mobile_money = models.BooleanField(default=True)
    autorise_crypto = models.BooleanField(default=False)
    
    # Statistiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    pib_par_habitant = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)
    fuseau_horaire_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'localisation"."pays'
        verbose_name = 'Pays (ADM0)'
        verbose_name_plural = 'Pays (ADM0)'
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.code_iso_2})"


class DivisionAdmin1(models.Model):
    """ADM1 - Provinces/Régions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='divisions_admin_1', db_column='pays_id')
    code = models.CharField(max_length=20, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_division = models.CharField(max_length=50, default='Province', help_text='Province, État, Région, etc.')
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Statistiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."divisions_admin_1'
        verbose_name = 'Division Administrative Niveau 1 (Province)'
        verbose_name_plural = 'Divisions Administratives Niveau 1 (Provinces)'
        unique_together = [('pays', 'code')]
        ordering = ['pays__nom', 'nom']
        indexes = [
            models.Index(fields=['pays', 'est_actif']),
            models.Index(fields=['type_division']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.type_division})"


class DivisionAdmin2(models.Model):
    """ADM2 - Territoires/Districts/Communes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division_admin_1 = models.ForeignKey(DivisionAdmin1, on_delete=models.CASCADE, related_name='divisions_admin_2', db_column='division_admin_1_id')
    code = models.CharField(max_length=20, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_division = models.CharField(max_length=50, default='Territoire', help_text='Territoire, District, Commune, etc.')
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Statistiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."divisions_admin_2'
        verbose_name = 'Division Administrative Niveau 2 (Territoire)'
        verbose_name_plural = 'Divisions Administratives Niveau 2 (Territoires)'
        ordering = ['division_admin_1__nom', 'nom']
        indexes = [
            models.Index(fields=['division_admin_1', 'est_actif']),
            models.Index(fields=['type_division']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.type_division})"


class DivisionAdmin3(models.Model):
    """ADM3 - Secteurs/Chefferies"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division_admin_2 = models.ForeignKey(DivisionAdmin2, on_delete=models.CASCADE, related_name='divisions_admin_3', db_column='division_admin_2_id')
    code = models.CharField(max_length=20, blank=True, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_division = models.CharField(max_length=50, default='Secteur', help_text='Secteur, Chefferie, Commune, etc.')
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Statistiques
    population_estimee = models.IntegerField(null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."divisions_admin_3'
        verbose_name = 'Division Administrative Niveau 3 (Secteur/Chefferie)'
        verbose_name_plural = 'Divisions Administratives Niveau 3 (Secteurs/Chefferies)'
        ordering = ['division_admin_2__nom', 'nom']
        indexes = [
            models.Index(fields=['division_admin_2', 'est_actif']),
            models.Index(fields=['type_division']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.type_division})"


class DivisionAdmin4(models.Model):
    """ADM4 - Groupements"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division_admin_3 = models.ForeignKey(DivisionAdmin3, on_delete=models.CASCADE, related_name='divisions_admin_4', db_column='division_admin_3_id')
    division_admin_2 = models.ForeignKey(DivisionAdmin2, on_delete=models.CASCADE, null=True, blank=True, db_column='division_admin_2_id')
    code = models.CharField(max_length=20, blank=True, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_division = models.CharField(max_length=50, default='Groupement', help_text='Groupement, Quartier, etc.')
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."divisions_admin_4'
        verbose_name = 'Division Administrative Niveau 4 (Groupement)'
        verbose_name_plural = 'Divisions Administratives Niveau 4 (Groupements)'
        ordering = ['division_admin_3__nom', 'nom']
        indexes = [
            models.Index(fields=['division_admin_3', 'est_actif']),
            models.Index(fields=['type_division']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.type_division})"


class DivisionAdmin5(models.Model):
    """ADM5 - Villages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division_admin_4 = models.ForeignKey(DivisionAdmin4, on_delete=models.CASCADE, related_name='divisions_admin_5', db_column='division_admin_4_id', null=True, blank=True)
    division_admin_3 = models.ForeignKey(DivisionAdmin3, on_delete=models.CASCADE, null=True, blank=True, db_column='division_admin_3_id')
    code = models.CharField(max_length=20, blank=True, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_division = models.CharField(max_length=50, default='Village', help_text='Village, Localité, etc.')
    
    # Géométrie PostGIS
    centre_geo = models.PointField(srid=4326, null=True, blank=True, geography=False)
    geometrie = models.MultiPolygonField(srid=4326, null=True, blank=True, geography=False)
    
    # Coordonnées (legacy)
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."divisions_admin_5'
        verbose_name = 'Division Administrative Niveau 5 (Village)'
        verbose_name_plural = 'Divisions Administratives Niveau 5 (Villages)'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['division_admin_4', 'est_actif']),
            models.Index(fields=['type_division']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.type_division})"


# Alias pour compatibilité
Province = DivisionAdmin1
District = DivisionAdmin2
Territoire = DivisionAdmin2
Commune = DivisionAdmin3
Secteur = DivisionAdmin3
Chefferie = DivisionAdmin3
Groupement = DivisionAdmin4
Quartier = DivisionAdmin4
Village = DivisionAdmin5
