"""
Modèles COMPLETS pour le schéma localisation.
Hiérarchie à 9 niveaux: Pays → Provinces → Districts → Communes → Secteurs → Quartiers → Zones → Collines → Sous-localités
"""
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import uuid


class Pays(models.Model):
    """Niveau 1: Pays"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_iso_2 = models.CharField(max_length=2, unique=True, db_index=True)
    code_iso_3 = models.CharField(max_length=3, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    nom_anglais = models.CharField(max_length=100, blank=True)
    
    # Géographie
    continent = models.CharField(max_length=50, blank=True, db_index=True)
    sous_region = models.CharField(max_length=100, blank=True, db_index=True)
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
        db_table = 'localisation"."pays'
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['est_actif', 'autorise_systeme']),
            models.Index(fields=['continent', 'sous_region']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.code_iso_2})"


class Province(models.Model):
    """Niveau 2: Provinces/Régions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='provinces', db_index=True)
    code = models.CharField(max_length=20, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Statistiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    densite_population = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    zone_urbaine = models.BooleanField(default=False)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Infrastructure bancaire
    code_bancaire = models.CharField(max_length=20, blank=True)
    nombre_banques = models.IntegerField(default=0)
    nombre_agences_bancaires = models.IntegerField(default=0)
    nombre_distributeurs = models.IntegerField(default=0)
    
    # Couverture réseau
    couverture_reseau_mobile = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    couverture_internet = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Géométrie
    geometrie_geojson = models.JSONField(null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."provinces'
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        unique_together = [('pays', 'code')]
        ordering = ['pays__nom', 'nom']
        indexes = [
            models.Index(fields=['pays', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.pays.code_iso_2})"


class District(models.Model):
    """Niveau 3: Districts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts', db_index=True)
    code = models.CharField(max_length=20, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Statistiques
    population_estimee = models.BigIntegerField(null=True, blank=True)
    zone_urbaine = models.BooleanField(default=False)
    niveau_activite_economique = models.CharField(max_length=20, blank=True)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Infrastructure
    code_postal = models.CharField(max_length=20, blank=True)
    code_bancaire = models.CharField(max_length=20, blank=True)
    nombre_agences_bancaires = models.IntegerField(default=0)
    nombre_distributeurs = models.IntegerField(default=0)
    nombre_agents_mobile_money = models.IntegerField(default=0)
    couverture_reseau_mobile = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Géométrie
    geometrie_geojson = models.JSONField(null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."districts'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        unique_together = [('province', 'code')]
        ordering = ['province__nom', 'nom']
        indexes = [
            models.Index(fields=['province', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.province.nom})"


class Commune(models.Model):
    """Niveau 4: Communes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='communes', db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    nom = models.CharField(max_length=200, db_index=True)
    type_commune = models.CharField(max_length=50, default='COMMUNE')
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Démographie
    population_totale = models.BigIntegerField(null=True, blank=True)
    zone_urbaine = models.BooleanField(default=False, db_index=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."communes'
        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'
        unique_together = [('district', 'code')]
        ordering = ['district__nom', 'nom']
        indexes = [
            models.Index(fields=['district', 'est_actif']),
            models.Index(fields=['zone_urbaine', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom}"


class Secteur(models.Model):
    """Niveau 5: Secteurs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='secteurs', db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    nom = models.CharField(max_length=200, db_index=True)
    type_secteur = models.CharField(max_length=50, default='SECTEUR')
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    population_estimee = models.BigIntegerField(null=True, blank=True)
    zone_urbaine = models.BooleanField(default=False, db_index=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."secteurs'
        verbose_name = 'Secteur'
        verbose_name_plural = 'Secteurs'
        unique_together = [('commune', 'code')]
        ordering = ['commune__nom', 'nom']
        indexes = [
            models.Index(fields=['commune', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom}"


class Quartier(models.Model):
    """Niveau 6: Quartiers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='quartiers', db_index=True)
    secteur = models.ForeignKey(Secteur, on_delete=models.SET_NULL, null=True, blank=True, related_name='quartiers')
    code = models.CharField(max_length=20, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_nord = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_sud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_est = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    bbox_ouest = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    superficie_km2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Statistiques
    type_zone = models.CharField(max_length=50, blank=True)
    nombre_habitants = models.IntegerField(null=True, blank=True)
    nombre_commerces = models.IntegerField(default=0)
    nombre_agents = models.IntegerField(default=0)
    nombre_utilisateurs = models.IntegerField(default=0)
    nombre_agents_actifs = models.IntegerField(default=0)
    nombre_utilisateurs_actifs = models.IntegerField(default=0)
    
    # Infrastructure
    code_postal = models.CharField(max_length=20, blank=True)
    
    # Géométrie
    geometrie_geojson = models.JSONField(null=True, blank=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."quartiers'
        verbose_name = 'Quartier'
        verbose_name_plural = 'Quartiers'
        unique_together = [('district', 'code')]
        ordering = ['district__nom', 'nom']
        indexes = [
            models.Index(fields=['district', 'est_actif']),
            models.Index(fields=['secteur']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.district.nom})"


class Zone(models.Model):
    """Niveau 7: Zones"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='zones', db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    nom = models.CharField(max_length=200, db_index=True)
    type_zone = models.CharField(max_length=50, default='ZONE')
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    population_estimee = models.IntegerField(null=True, blank=True)
    
    # Classification
    zone_commerciale = models.BooleanField(default=False, db_index=True)
    zone_residentielle = models.BooleanField(default=False, db_index=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."zones'
        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'
        unique_together = [('quartier', 'code')]
        ordering = ['quartier__nom', 'nom']
        indexes = [
            models.Index(fields=['quartier', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom}"


class Colline(models.Model):
    """Niveau 8: Collines"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='collines', db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    nom = models.CharField(max_length=200, db_index=True)
    type_colline = models.CharField(max_length=50, default='COLLINE')
    
    # Géographie
    centre_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    centre_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    altitude_m = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    population_estimee = models.IntegerField(null=True, blank=True)
    zone_rurale = models.BooleanField(default=True, db_index=True)
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."collines'
        verbose_name = 'Colline'
        verbose_name_plural = 'Collines'
        unique_together = [('zone', 'code')]
        ordering = ['zone__nom', 'nom']
        indexes = [
            models.Index(fields=['zone', 'est_actif']),
        ]

    def __str__(self):
        return f"{self.nom}"


class PointDeService(models.Model):
    """Points de service"""
    TYPE_POINT_CHOICES = [
        ('AGENT', 'Agent'),
        ('GUICHET', 'Guichet'),
        ('PARTENAIRE', 'Partenaire'),
        ('AUTRE', 'Autre'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='points_de_service', db_index=True)
    code = models.CharField(max_length=30, db_index=True)
    nom = models.CharField(max_length=100, db_index=True)
    type_point = models.CharField(max_length=20, choices=TYPE_POINT_CHOICES, default='AGENT')
    
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
    
    # Gestion
    autorise_systeme = models.BooleanField(default=True, db_index=True)
    est_actif = models.BooleanField(default=True, db_index=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."points_de_service'
        verbose_name = 'Point de service'
        verbose_name_plural = 'Points de service'
        unique_together = [('quartier', 'code')]
        ordering = ['quartier__nom', 'nom']
        indexes = [
            models.Index(fields=['quartier', 'est_actif']),
            models.Index(fields=['type_point']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.quartier.nom})"
