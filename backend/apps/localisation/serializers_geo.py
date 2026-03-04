"""
Serializers GeoJSON pour affichage sur carte dynamique.
Retourne les coordonnées et géométries pour chaque niveau hiérarchique.
"""
from rest_framework import serializers
from .models import Pays, Province, District, PointDeService, DivisionNiveau0, DivisionNiveau1, DivisionNiveau2


# ============================================================================
# SERIALIZERS GEO POUR CARTE (avec coordonnées et géométries)
# ============================================================================

class PaysGeoSerializer(serializers.ModelSerializer):
    """Pays avec coordonnées pour affichage carte"""
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Pays
        fields = [
            'id', 'code_iso_2', 'code_iso_3', 'nom', 
            'centre_latitude', 'centre_longitude',
            'bbox_nord', 'bbox_sud', 'bbox_est', 'bbox_ouest',
            'geometry', 'est_actif'
        ]
    
    def get_geometry(self, obj):
        """Retourne la géométrie GeoJSON si disponible"""
        if obj.geometrie_geojson:
            return obj.geometrie_geojson
        # Sinon créer un Point avec les coordonnées du centre
        if obj.centre_latitude and obj.centre_longitude:
            return {
                "type": "Point",
                "coordinates": [float(obj.centre_longitude), float(obj.centre_latitude)]
            }
        return None


class ProvinceGeoSerializer(serializers.ModelSerializer):
    """Province (Division Niveau 1) avec coordonnées pour affichage carte"""
    
    class Meta:
        model = DivisionNiveau1
        fields = [
            'division_id', 'gid_0', 'pays', 'gid_1', 'nom_1', 
            'type_1', 'code_1', 'code_iso', 'nom_pays', 'est_actif'
        ]


class DistrictGeoSerializer(serializers.ModelSerializer):
    """District (Division Niveau 2) avec coordonnées pour affichage carte"""
    
    class Meta:
        model = DivisionNiveau2
        fields = [
            'division_id', 'gid_0', 'pays', 'gid_1', 'nom_1',
            'gid_2', 'nom_2', 'type_2', 'code_2', 
            'code_iso', 'nom_pays', 'est_actif'
        ]


# Serializers vides pour compatibilité (modèles non existants)
class CommuneGeoSerializer(serializers.Serializer):
    """Placeholder - Commune n'existe pas dans la structure actuelle"""
    pass


class SecteurGeoSerializer(serializers.Serializer):
    """Placeholder - Secteur n'existe pas dans la structure actuelle"""
    pass


class QuartierGeoSerializer(serializers.Serializer):
    """Placeholder - Quartier n'existe pas dans la structure actuelle"""
    pass


class ZoneGeoSerializer(serializers.Serializer):
    """Placeholder - Zone n'existe pas dans la structure actuelle"""
    pass


class CollineGeoSerializer(serializers.Serializer):
    """Placeholder - Colline n'existe pas dans la structure actuelle"""
    pass


class PointDeServiceGeoSerializer(serializers.ModelSerializer):
    """Point de service avec coordonnées exactes pour affichage carte"""
    
    class Meta:
        model = PointDeService
        fields = [
            'id', 'code', 'nom', 'type_point', 'quartier_id',
            'latitude', 'longitude', 'altitude_m',
            'adresse_complementaire', 'est_actif'
        ]


# ============================================================================
# SERIALIZER GEOJSON FEATURE COLLECTION
# ============================================================================

class GeoJSONFeatureSerializer(serializers.Serializer):
    """
    Serializer pour format GeoJSON FeatureCollection.
    Compatible avec Leaflet, Mapbox, OpenLayers, etc.
    """
    type = serializers.CharField(default='FeatureCollection')
    features = serializers.ListField()
    
    def to_representation(self, instance):
        """
        Convertit les données en format GeoJSON FeatureCollection
        """
        features = []
        
        for item in instance.get('data', []):
            # Extraire les coordonnées
            if hasattr(item, 'centre_latitude') and item.centre_latitude:
                coordinates = [float(item.centre_longitude), float(item.centre_latitude)]
            elif hasattr(item, 'latitude') and item.latitude:
                coordinates = [float(item.longitude), float(item.latitude)]
            else:
                continue
            
            # Créer la feature GeoJSON
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": coordinates
                },
                "properties": {
                    "id": str(item.id) if hasattr(item, 'id') else str(item.division_id),
                    "code": item.code if hasattr(item, 'code') else '',
                    "nom": item.nom if hasattr(item, 'nom') else (item.nom_pays if hasattr(item, 'nom_pays') else ''),
                    "est_actif": item.est_actif if hasattr(item, 'est_actif') else True,
                }
            }
            
            # Ajouter des propriétés spécifiques selon le type
            if hasattr(item, 'population_estimee') and item.population_estimee:
                feature['properties']['population'] = item.population_estimee
            if hasattr(item, 'zone_urbaine'):
                feature['properties']['zone_urbaine'] = item.zone_urbaine
            if hasattr(item, 'type_point'):
                feature['properties']['type'] = item.type_point
            if hasattr(item, 'altitude_m') and item.altitude_m:
                feature['properties']['altitude'] = float(item.altitude_m)
            
            # Ajouter bbox si disponible
            if hasattr(item, 'bbox_nord') and item.bbox_nord:
                feature['properties']['bbox'] = [
                    float(item.bbox_ouest),
                    float(item.bbox_sud),
                    float(item.bbox_est),
                    float(item.bbox_nord)
                ]
            
            # Ajouter géométrie complète si disponible
            if hasattr(item, 'geometrie_geojson') and item.geometrie_geojson:
                feature['geometry'] = item.geometrie_geojson
            
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "count": len(features),
                "niveau": instance.get('niveau', 'unknown')
            }
        }
