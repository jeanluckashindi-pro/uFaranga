"""
Serializers GeoJSON pour affichage sur carte dynamique.
Retourne les coordonnées et géométries pour chaque niveau hiérarchique.
"""
from rest_framework import serializers
from .models import Pays, Province, District, Commune, Secteur, Quartier, Zone, Colline, PointDeService


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
    """Province avec coordonnées pour affichage carte"""
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    pays_code = serializers.CharField(source='pays.code_iso_2', read_only=True)
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Province
        fields = [
            'id', 'code', 'nom', 'pays_nom', 'pays_code',
            'centre_latitude', 'centre_longitude',
            'bbox_nord', 'bbox_sud', 'bbox_est', 'bbox_ouest',
            'superficie_km2', 'population_estimee',
            'geometry', 'est_actif'
        ]
    
    def get_geometry(self, obj):
        if obj.geometrie_geojson:
            return obj.geometrie_geojson
        if obj.centre_latitude and obj.centre_longitude:
            return {
                "type": "Point",
                "coordinates": [float(obj.centre_longitude), float(obj.centre_latitude)]
            }
        return None


class DistrictGeoSerializer(serializers.ModelSerializer):
    """District avec coordonnées pour affichage carte"""
    province_nom = serializers.CharField(source='province.nom', read_only=True)
    pays_nom = serializers.CharField(source='province.pays.nom', read_only=True)
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = District
        fields = [
            'id', 'code', 'nom', 'province_nom', 'pays_nom',
            'centre_latitude', 'centre_longitude',
            'bbox_nord', 'bbox_sud', 'bbox_est', 'bbox_ouest',
            'superficie_km2', 'population_estimee', 'zone_urbaine',
            'geometry', 'est_actif'
        ]
    
    def get_geometry(self, obj):
        if obj.geometrie_geojson:
            return obj.geometrie_geojson
        if obj.centre_latitude and obj.centre_longitude:
            return {
                "type": "Point",
                "coordinates": [float(obj.centre_longitude), float(obj.centre_latitude)]
            }
        return None


class CommuneGeoSerializer(serializers.ModelSerializer):
    """Commune avec coordonnées pour affichage carte"""
    district_nom = serializers.CharField(source='district.nom', read_only=True)
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Commune
        fields = [
            'id', 'code', 'nom', 'type_commune', 'district_nom',
            'centre_latitude', 'centre_longitude',
            'bbox_nord', 'bbox_sud', 'bbox_est', 'bbox_ouest',
            'superficie_km2', 'population_totale', 'zone_urbaine',
            'geometry', 'est_actif'
        ]
    
    def get_geometry(self, obj):
        if obj.centre_latitude and obj.centre_longitude:
            return {
                "type": "Point",
                "coordinates": [float(obj.centre_longitude), float(obj.centre_latitude)]
            }
        return None


class SecteurGeoSerializer(serializers.ModelSerializer):
    """Secteur avec coordonnées pour affichage carte"""
    commune_nom = serializers.CharField(source='commune.nom', read_only=True)
    
    class Meta:
        model = Secteur
        fields = [
            'id', 'code', 'nom', 'type_secteur', 'commune_nom',
            'centre_latitude', 'centre_longitude',
            'population_estimee', 'zone_urbaine', 'est_actif'
        ]


class QuartierGeoSerializer(serializers.ModelSerializer):
    """Quartier avec coordonnées pour affichage carte"""
    district_nom = serializers.CharField(source='district.nom', read_only=True)
    geometry = serializers.SerializerMethodField()
    
    class Meta:
        model = Quartier
        fields = [
            'id', 'code', 'nom', 'type_zone', 'district_nom',
            'centre_latitude', 'centre_longitude',
            'bbox_nord', 'bbox_sud', 'bbox_est', 'bbox_ouest',
            'nombre_habitants', 'geometry', 'est_actif'
        ]
    
    def get_geometry(self, obj):
        if obj.geometrie_geojson:
            return obj.geometrie_geojson
        if obj.centre_latitude and obj.centre_longitude:
            return {
                "type": "Point",
                "coordinates": [float(obj.centre_longitude), float(obj.centre_latitude)]
            }
        return None


class ZoneGeoSerializer(serializers.ModelSerializer):
    """Zone avec coordonnées pour affichage carte"""
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    
    class Meta:
        model = Zone
        fields = [
            'id', 'code', 'nom', 'type_zone', 'quartier_nom',
            'centre_latitude', 'centre_longitude',
            'population_estimee', 'zone_commerciale', 'zone_residentielle',
            'est_actif'
        ]


class CollineGeoSerializer(serializers.ModelSerializer):
    """Colline avec coordonnées pour affichage carte"""
    zone_nom = serializers.CharField(source='zone.nom', read_only=True)
    
    class Meta:
        model = Colline
        fields = [
            'id', 'code', 'nom', 'type_colline', 'zone_nom',
            'centre_latitude', 'centre_longitude', 'altitude_m',
            'population_estimee', 'zone_rurale', 'est_actif'
        ]


class PointDeServiceGeoSerializer(serializers.ModelSerializer):
    """Point de service avec coordonnées exactes pour affichage carte"""
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    
    class Meta:
        model = PointDeService
        fields = [
            'id', 'code', 'nom', 'type_point', 'quartier_nom',
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
                    "id": str(item.id),
                    "code": item.code,
                    "nom": item.nom,
                    "est_actif": item.est_actif,
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
