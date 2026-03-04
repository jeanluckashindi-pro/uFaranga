"""
Serializers optimisés pour la structure GADM.
"""
from rest_framework import serializers
from .models import Pays, Province, District, PointDeService, DivisionNiveau0, DivisionNiveau1, DivisionNiveau2


# ============================================================================
# SERIALIZERS POUR PAYS (Table de référence)
# ============================================================================

class PaysListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'code_iso_2', 'code_iso_3', 'nom', 'nom_anglais', 'continent', 'sous_region', 'est_actif', 'autorise_systeme']


class PaysDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'


# ============================================================================
# SERIALIZERS POUR DIVISIONS GADM (lecture seule)
# ============================================================================

class DivisionNiveau0ListSerializer(serializers.ModelSerializer):
    """Niveau 0 - Pays GADM"""
    class Meta:
        model = DivisionNiveau0
        fields = ['division_id', 'gid_0', 'code_iso', 'nom_pays', 'continent_code', 'region_code', 'est_actif']


class DivisionNiveau0DetailSerializer(serializers.ModelSerializer):
    """Niveau 0 - Pays GADM (détails)"""
    class Meta:
        model = DivisionNiveau0
        fields = '__all__'


class DivisionNiveau1ListSerializer(serializers.ModelSerializer):
    """Niveau 1 - Provinces GADM"""
    class Meta:
        model = DivisionNiveau1
        fields = [
            'division_id', 'pays_division_id', 'gid_0', 'pays', 'gid_1', 'nom_1', 
            'type_1', 'code_1', 'code_iso', 'nom_pays', 'est_actif'
        ]


class DivisionNiveau1DetailSerializer(serializers.ModelSerializer):
    """Niveau 1 - Provinces GADM (détails)"""
    class Meta:
        model = DivisionNiveau1
        fields = '__all__'


class DivisionNiveau2ListSerializer(serializers.ModelSerializer):
    """Niveau 2 - Districts GADM"""
    class Meta:
        model = DivisionNiveau2
        fields = [
            'division_id', 'pays_division_id', 'parent_division_id', 'gid_0', 'pays',
            'gid_1', 'nom_1', 'gid_2', 'nom_2', 'type_2', 'code_2', 
            'code_iso', 'nom_pays', 'est_actif'
        ]


class DivisionNiveau2DetailSerializer(serializers.ModelSerializer):
    """Niveau 2 - Districts GADM (détails)"""
    class Meta:
        model = DivisionNiveau2
        fields = '__all__'


# ============================================================================
# SERIALIZERS POUR POINTS DE SERVICE
# ============================================================================

class PointDeServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointDeService
        fields = [
            'id', 'code', 'nom', 'type_point', 'quartier_id',
            'latitude', 'longitude', 'est_actif', 'autorise_systeme'
        ]


class PointDeServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointDeService
        fields = '__all__'


# ============================================================================
# ALIAS POUR COMPATIBILITÉ
# ============================================================================

# Alias pour faciliter l'utilisation
ProvinceListSerializer = DivisionNiveau1ListSerializer
ProvinceDetailSerializer = DivisionNiveau1DetailSerializer
DistrictListSerializer = DivisionNiveau2ListSerializer
DistrictDetailSerializer = DivisionNiveau2DetailSerializer

# Serializers vides pour compatibilité (à supprimer si non utilisés)
class CommuneListSerializer(serializers.Serializer):
    """Placeholder - Commune n'existe pas dans la structure actuelle"""
    pass

class SecteurListSerializer(serializers.Serializer):
    """Placeholder - Secteur n'existe pas dans la structure actuelle"""
    pass

class QuartierListSerializer(serializers.Serializer):
    """Placeholder - Quartier n'existe pas dans la structure actuelle"""
    pass


# ============================================================================
# SERIALIZERS HIÉRARCHIQUES
# ============================================================================

class HierarchieOptimiseeSerializer(serializers.Serializer):
    """Serializer pour hiérarchie avec statistiques"""
    niveau = serializers.CharField()
    total = serializers.IntegerField()
    actifs = serializers.IntegerField()
    inactifs = serializers.IntegerField()
    donnees = serializers.ListField()
