"""
Modèles pour le schéma LOCALISATION.
Hiérarchie : Pays → Province → District → Quartier → Point de service / Agent.
Coordonnées pour repérage sur carte, flag autorise_systeme par niveau.
"""
from django.db import models
from django.utils import timezone
import uuid


class Pays(models.Model):
    """Pays - localisation.pays"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_iso_2 = models.CharField(max_length=2, unique=True, db_index=True)
    code_iso_3 = models.CharField(max_length=3, blank=True)
    nom = models.CharField(max_length=100)
    nom_anglais = models.CharField(max_length=100, blank=True)
    
    # Groupements géographiques
    continent = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        help_text='Continent du pays (ex: Afrique, Europe, Asie)'
    )
    sous_region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text='Sous-région géographique (ex: Afrique de l\'Est, Afrique Centrale)'
    )
    
    latitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    autorise_systeme = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."pays'
        verbose_name = 'Pays'
        verbose_name_plural = 'Pays'
        indexes = [
            models.Index(fields=['continent']),
            models.Index(fields=['sous_region']),
            models.Index(fields=['code_iso_2']),
        ]

    def __str__(self):
        return f"{self.nom} ({self.code_iso_2})"


class Province(models.Model):
    """Région / Province - localisation.provinces"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='provinces')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    latitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    autorise_systeme = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."provinces'
        verbose_name = 'Province / Région'
        verbose_name_plural = 'Provinces / Régions'
        unique_together = [('pays', 'code')]

    def __str__(self):
        return f"{self.nom} ({self.pays.code_iso_2})"


class District(models.Model):
    """Ville / District - localisation.districts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    latitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    autorise_systeme = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."districts'
        verbose_name = 'District / Ville'
        verbose_name_plural = 'Districts / Villes'
        unique_together = [('province', 'code')]

    def __str__(self):
        return f"{self.nom} ({self.province.nom})"


class Quartier(models.Model):
    """Quartier / Zone - localisation.quartiers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='quartiers')
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    latitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude_centre = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    autorise_systeme = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."quartiers'
        verbose_name = 'Quartier / Zone'
        verbose_name_plural = 'Quartiers / Zones'
        unique_together = [('district', 'code')]

    def __str__(self):
        return f"{self.nom} ({self.district.nom})"


class PointDeService(models.Model):
    """Point de service / Agent - localisation.points_de_service"""
    TYPE_POINT_CHOICES = [
        ('AGENT', 'Agent'),
        ('GUICHET', 'Guichet'),
        ('PARTENAIRE', 'Partenaire'),
        ('AUTRE', 'Autre'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE, related_name='points_de_service')
    code = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    type_point = models.CharField(max_length=20, choices=TYPE_POINT_CHOICES, default='AGENT')
    agent_utilisateur = models.ForeignKey(
        'identite.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='points_de_service_agent',
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    adresse_complementaire = models.TextField(blank=True)
    autorise_systeme = models.BooleanField(default=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'localisation"."points_de_service'
        verbose_name = 'Point de service / Agent'
        verbose_name_plural = 'Points de service / Agents'
        unique_together = [('quartier', 'code')]

    def __str__(self):
        return f"{self.nom} ({self.quartier.nom})"
