"""
Views GeoJSON pour affichage dynamique sur carte.
Endpoints optimisés pour charger les données géospatiales niveau par niveau.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Pays, Province, District, Commune, Secteur, Quartier, Zone, Colline, PointDeService
from .serializers_geo import (
    PaysGeoSerializer, ProvinceGeoSerializer, DistrictGeoSerializer,
    CommuneGeoSerializer, SecteurGeoSerializer, QuartierGeoSerializer,
    ZoneGeoSerializer, CollineGeoSerializer, PointDeServiceGeoSerializer,
    GeoJSONFeatureSerializer
)


class GeoLocalisationViewSet(viewsets.ViewSet):
    """
    ViewSet pour charger les données géospatiales de manière dynamique.
    
    Workflow:
    1. Charger tous les pays avec leurs coordonnées
    2. Cliquer sur un pays → charger ses provinces avec coordonnées de découpage
    3. Cliquer sur une province → charger ses districts
    4. Et ainsi de suite jusqu'aux points de service
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='pays')
    def pays(self, request):
        """
        GET /api/v1/localisation/geo/pays/
        
        Retourne tous les pays avec leurs coordonnées centrales et bounding boxes.
        """
        queryset = Pays.objects.filter(est_actif=True).order_by('nom')
        serializer = PaysGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='pays/geojson')
    def pays_geojson(self, request):
        """
        GET /api/v1/localisation/geo/pays/geojson/
        
        Retourne tous les pays au format GeoJSON FeatureCollection.
        """
        queryset = Pays.objects.filter(est_actif=True).order_by('nom')
        data = {'data': queryset, 'niveau': 'pays'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='provinces')
    def provinces(self, request):
        """
        GET /api/v1/localisation/geo/provinces/?pays_id={uuid}
        
        Retourne les provinces d'un pays avec coordonnées et géométries de découpage.
        """
        pays_id = request.query_params.get('pays_id')
        if not pays_id:
            return Response({"error": "pays_id requis"}, status=400)
        
        queryset = Province.objects.filter(
            pays_id=pays_id,
            est_actif=True
        ).select_related('pays').order_by('nom')
        
        serializer = ProvinceGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='provinces/geojson')
    def provinces_geojson(self, request):
        """
        GET /api/v1/localisation/geo/provinces/geojson/?pays_id={uuid}
        
        Retourne les provinces au format GeoJSON FeatureCollection.
        """
        pays_id = request.query_params.get('pays_id')
        if not pays_id:
            return Response({"error": "pays_id requis"}, status=400)
        
        queryset = Province.objects.filter(
            pays_id=pays_id,
            est_actif=True
        ).select_related('pays').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'provinces'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='districts')
    def districts(self, request):
        """
        GET /api/v1/localisation/geo/districts/?province_id={uuid}
        
        Retourne les districts d'une province avec coordonnées et géométries.
        """
        province_id = request.query_params.get('province_id')
        if not province_id:
            return Response({"error": "province_id requis"}, status=400)
        
        queryset = District.objects.filter(
            province_id=province_id,
            est_actif=True
        ).select_related('province', 'province__pays').order_by('nom')
        
        serializer = DistrictGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='districts/geojson')
    def districts_geojson(self, request):
        """
        GET /api/v1/localisation/geo/districts/geojson/?province_id={uuid}
        
        Retourne les districts au format GeoJSON FeatureCollection.
        """
        province_id = request.query_params.get('province_id')
        if not province_id:
            return Response({"error": "province_id requis"}, status=400)
        
        queryset = District.objects.filter(
            province_id=province_id,
            est_actif=True
        ).select_related('province', 'province__pays').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'districts'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='communes')
    def communes(self, request):
        """
        GET /api/v1/localisation/geo/communes/?district_id={uuid}
        
        Retourne les communes d'un district avec coordonnées.
        """
        district_id = request.query_params.get('district_id')
        if not district_id:
            return Response({"error": "district_id requis"}, status=400)
        
        queryset = Commune.objects.filter(
            district_id=district_id,
            est_actif=True
        ).select_related('district').order_by('nom')
        
        serializer = CommuneGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='communes/geojson')
    def communes_geojson(self, request):
        """
        GET /api/v1/localisation/geo/communes/geojson/?district_id={uuid}
        
        Retourne les communes au format GeoJSON FeatureCollection.
        """
        district_id = request.query_params.get('district_id')
        if not district_id:
            return Response({"error": "district_id requis"}, status=400)
        
        queryset = Commune.objects.filter(
            district_id=district_id,
            est_actif=True
        ).select_related('district').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'communes'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='secteurs')
    def secteurs(self, request):
        """
        GET /api/v1/localisation/geo/secteurs/?commune_id={uuid}
        
        Retourne les secteurs d'une commune avec coordonnées.
        """
        commune_id = request.query_params.get('commune_id')
        if not commune_id:
            return Response({"error": "commune_id requis"}, status=400)
        
        queryset = Secteur.objects.filter(
            commune_id=commune_id,
            est_actif=True
        ).select_related('commune').order_by('nom')
        
        serializer = SecteurGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='secteurs/geojson')
    def secteurs_geojson(self, request):
        """
        GET /api/v1/localisation/geo/secteurs/geojson/?commune_id={uuid}
        
        Retourne les secteurs au format GeoJSON FeatureCollection.
        """
        commune_id = request.query_params.get('commune_id')
        if not commune_id:
            return Response({"error": "commune_id requis"}, status=400)
        
        queryset = Secteur.objects.filter(
            commune_id=commune_id,
            est_actif=True
        ).select_related('commune').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'secteurs'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='quartiers')
    def quartiers(self, request):
        """
        GET /api/v1/localisation/geo/quartiers/?district_id={uuid}
        
        Retourne les quartiers d'un district avec coordonnées.
        """
        district_id = request.query_params.get('district_id')
        if not district_id:
            return Response({"error": "district_id requis"}, status=400)
        
        queryset = Quartier.objects.filter(
            district_id=district_id,
            est_actif=True
        ).select_related('district').order_by('nom')
        
        serializer = QuartierGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='quartiers/geojson')
    def quartiers_geojson(self, request):
        """
        GET /api/v1/localisation/geo/quartiers/geojson/?district_id={uuid}
        
        Retourne les quartiers au format GeoJSON FeatureCollection.
        """
        district_id = request.query_params.get('district_id')
        if not district_id:
            return Response({"error": "district_id requis"}, status=400)
        
        queryset = Quartier.objects.filter(
            district_id=district_id,
            est_actif=True
        ).select_related('district').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'quartiers'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='zones')
    def zones(self, request):
        """
        GET /api/v1/localisation/geo/zones/?quartier_id={uuid}
        
        Retourne les zones d'un quartier avec coordonnées.
        """
        quartier_id = request.query_params.get('quartier_id')
        if not quartier_id:
            return Response({"error": "quartier_id requis"}, status=400)
        
        queryset = Zone.objects.filter(
            quartier_id=quartier_id,
            est_actif=True
        ).select_related('quartier').order_by('nom')
        
        serializer = ZoneGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='zones/geojson')
    def zones_geojson(self, request):
        """
        GET /api/v1/localisation/geo/zones/geojson/?quartier_id={uuid}
        
        Retourne les zones au format GeoJSON FeatureCollection.
        """
        quartier_id = request.query_params.get('quartier_id')
        if not quartier_id:
            return Response({"error": "quartier_id requis"}, status=400)
        
        queryset = Zone.objects.filter(
            quartier_id=quartier_id,
            est_actif=True
        ).select_related('quartier').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'zones'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='collines')
    def collines(self, request):
        """
        GET /api/v1/localisation/geo/collines/?zone_id={uuid}
        
        Retourne les collines d'une zone avec coordonnées.
        """
        zone_id = request.query_params.get('zone_id')
        if not zone_id:
            return Response({"error": "zone_id requis"}, status=400)
        
        queryset = Colline.objects.filter(
            zone_id=zone_id,
            est_actif=True
        ).select_related('zone').order_by('nom')
        
        serializer = CollineGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='collines/geojson')
    def collines_geojson(self, request):
        """
        GET /api/v1/localisation/geo/collines/geojson/?zone_id={uuid}
        
        Retourne les collines au format GeoJSON FeatureCollection.
        """
        zone_id = request.query_params.get('zone_id')
        if not zone_id:
            return Response({"error": "zone_id requis"}, status=400)
        
        queryset = Colline.objects.filter(
            zone_id=zone_id,
            est_actif=True
        ).select_related('zone').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'collines'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='points-de-service')
    def points_de_service(self, request):
        """
        GET /api/v1/localisation/geo/points-de-service/?quartier_id={uuid}
        
        Retourne les points de service d'un quartier avec coordonnées exactes.
        """
        quartier_id = request.query_params.get('quartier_id')
        if not quartier_id:
            return Response({"error": "quartier_id requis"}, status=400)
        
        queryset = PointDeService.objects.filter(
            quartier_id=quartier_id,
            est_actif=True
        ).select_related('quartier').order_by('nom')
        
        serializer = PointDeServiceGeoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='points-de-service/geojson')
    def points_de_service_geojson(self, request):
        """
        GET /api/v1/localisation/geo/points-de-service/geojson/?quartier_id={uuid}
        
        Retourne les points de service au format GeoJSON FeatureCollection.
        """
        quartier_id = request.query_params.get('quartier_id')
        if not quartier_id:
            return Response({"error": "quartier_id requis"}, status=400)
        
        queryset = PointDeService.objects.filter(
            quartier_id=quartier_id,
            est_actif=True
        ).select_related('quartier').order_by('nom')
        
        data = {'data': queryset, 'niveau': 'points_de_service'}
        serializer = GeoJSONFeatureSerializer(data)
        return Response(serializer.data)
