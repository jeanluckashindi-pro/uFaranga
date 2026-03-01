"""
Serializers optimisés pour gérer 232K+ entités avec pagination et filtres.
"""
from rest_framework import serializers
from .models import Pays, Province, District, Commune, Secteur, Quartier, Zone, Colline, PointDeService


# ============================================================================
# SERIALIZERS MINIMAUX (pour listes paginées)
# ============================================================================

class PaysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'code_iso_2', 'code_iso_3', 'nom', 'continent', 'est_actif']


class ProvinceListSerializer(serializers.ModelSerializer):
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    
    class Meta:
        model = Province
        fields = ['id', 'code', 'nom', 'pays_nom', 'est_actif']


class DistrictListSerializer(serializers.ModelSerializer):
    province_nom = serializers.CharField(source='province.nom', read_only=True)
    pays_nom = serializers.CharField(source='province.pays.nom', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'code', 'nom', 'province_nom', 'pays_nom', 'est_actif']


class CommuneListSerializer(serializers.ModelSerializer):
    district_nom = serializers.CharField(source='district.nom', read_only=True)
    
    class Meta:
        model = Commune
        fields = ['id', 'code', 'nom', 'type_commune', 'district_nom', 'zone_urbaine', 'est_actif']


class SecteurListSerializer(serializers.ModelSerializer):
    commune_nom = serializers.CharField(source='commune.nom', read_only=True)
    
    class Meta:
        model = Secteur
        fields = ['id', 'code', 'nom', 'type_secteur', 'commune_nom', 'est_actif']


class QuartierListSerializer(serializers.ModelSerializer):
    district_nom = serializers.CharField(source='district.nom', read_only=True)
    
    class Meta:
        model = Quartier
        fields = ['id', 'code', 'nom', 'district_nom', 'est_actif']


class ZoneListSerializer(serializers.ModelSerializer):
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    
    class Meta:
        model = Zone
        fields = ['id', 'code', 'nom', 'type_zone', 'quartier_nom', 'est_actif']


class CollineListSerializer(serializers.ModelSerializer):
    zone_nom = serializers.CharField(source='zone.nom', read_only=True)
    
    class Meta:
        model = Colline
        fields = ['id', 'code', 'nom', 'type_colline', 'zone_nom', 'altitude_m', 'est_actif']


class PointDeServiceListSerializer(serializers.ModelSerializer):
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    
    class Meta:
        model = PointDeService
        fields = ['id', 'code', 'nom', 'type_point', 'quartier_nom', 'est_actif']


# ============================================================================
# SERIALIZERS COMPLETS (pour détails)
# ============================================================================

class PaysDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'


class ProvinceDetailSerializer(serializers.ModelSerializer):
    pays = PaysListSerializer(read_only=True)
    
    class Meta:
        model = Province
        fields = '__all__'


class DistrictDetailSerializer(serializers.ModelSerializer):
    province = ProvinceListSerializer(read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class CommuneDetailSerializer(serializers.ModelSerializer):
    district = DistrictListSerializer(read_only=True)
    
    class Meta:
        model = Commune
        fields = '__all__'


class SecteurDetailSerializer(serializers.ModelSerializer):
    commune = CommuneListSerializer(read_only=True)
    
    class Meta:
        model = Secteur
        fields = '__all__'


class QuartierDetailSerializer(serializers.ModelSerializer):
    district = DistrictListSerializer(read_only=True)
    secteur = SecteurListSerializer(read_only=True)
    
    class Meta:
        model = Quartier
        fields = '__all__'


class ZoneDetailSerializer(serializers.ModelSerializer):
    quartier = QuartierListSerializer(read_only=True)
    
    class Meta:
        model = Zone
        fields = '__all__'


class CollineDetailSerializer(serializers.ModelSerializer):
    zone = ZoneListSerializer(read_only=True)
    
    class Meta:
        model = Colline
        fields = '__all__'


class PointDeServiceDetailSerializer(serializers.ModelSerializer):
    quartier = QuartierListSerializer(read_only=True)
    
    class Meta:
        model = PointDeService
        fields = '__all__'


# ============================================================================
# SERIALIZERS HIÉRARCHIQUES (avec filtres)
# ============================================================================

class HierarchieOptimiseeSerializer(serializers.Serializer):
    """Serializer pour hiérarchie avec statistiques"""
    niveau = serializers.CharField()
    total = serializers.IntegerField()
    actifs = serializers.IntegerField()
    inactifs = serializers.IntegerField()
    donnees = serializers.ListField()
