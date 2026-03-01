"""
Views optimisées avec pagination, filtres et cache pour gérer 232K+ entités.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Pays, Province, District, Commune, Secteur, Quartier, Zone, Colline, PointDeService
from .serializers_optimises import *
from .permissions import IsSystemeOrSuperAdmin


# ============================================================================
# PAGINATION OPTIMISÉE
# ============================================================================

class StandardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LargePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


# ============================================================================
# VIEWSETS OPTIMISÉS
# ============================================================================

class PaysOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Pays"""
    queryset = Pays.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['continent', 'sous_region', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code_iso_2', 'code_iso_3']
    ordering_fields = ['nom', 'code_iso_2', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PaysDetailSerializer
        return PaysListSerializer


class ProvinceOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Provinces"""
    queryset = Province.objects.select_related('pays').all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pays', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProvinceDetailSerializer
        return ProvinceListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        pays_id = self.request.query_params.get('pays_id')
        if pays_id:
            qs = qs.filter(pays_id=pays_id)
        return qs


class DistrictOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Districts"""
    queryset = District.objects.select_related('province', 'province__pays').all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['province', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistrictDetailSerializer
        return DistrictListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        province_id = self.request.query_params.get('province_id')
        pays_id = self.request.query_params.get('pays_id')
        
        if province_id:
            qs = qs.filter(province_id=province_id)
        elif pays_id:
            qs = qs.filter(province__pays_id=pays_id)
        
        return qs


class CommuneOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Communes (20K+ entités)"""
    queryset = Commune.objects.select_related('district', 'district__province').all()
    permission_classes = [AllowAny]
    pagination_class = LargePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district', 'type_commune', 'zone_urbaine', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'population_totale', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CommuneDetailSerializer
        return CommuneListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        district_id = self.request.query_params.get('district_id')
        province_id = self.request.query_params.get('province_id')
        pays_id = self.request.query_params.get('pays_id')
        
        if district_id:
            qs = qs.filter(district_id=district_id)
        elif province_id:
            qs = qs.filter(district__province_id=province_id)
        elif pays_id:
            qs = qs.filter(district__province__pays_id=pays_id)
        
        return qs


class SecteurOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Secteurs (114K+ entités)"""
    queryset = Secteur.objects.select_related('commune', 'commune__district').all()
    permission_classes = [AllowAny]
    pagination_class = LargePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['commune', 'type_secteur', 'zone_urbaine', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SecteurDetailSerializer
        return SecteurListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        commune_id = self.request.query_params.get('commune_id')
        district_id = self.request.query_params.get('district_id')
        
        if commune_id:
            qs = qs.filter(commune_id=commune_id)
        elif district_id:
            qs = qs.filter(commune__district_id=district_id)
        
        return qs


class QuartierOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Quartiers"""
    queryset = Quartier.objects.select_related('district', 'secteur').all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district', 'secteur', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuartierDetailSerializer
        return QuartierListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        district_id = self.request.query_params.get('district_id')
        secteur_id = self.request.query_params.get('secteur_id')
        
        if district_id:
            qs = qs.filter(district_id=district_id)
        if secteur_id:
            qs = qs.filter(secteur_id=secteur_id)
        
        return qs


class ZoneOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Zones (60K+ entités)"""
    queryset = Zone.objects.select_related('quartier', 'quartier__district').all()
    permission_classes = [AllowAny]
    pagination_class = LargePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quartier', 'type_zone', 'zone_commerciale', 'zone_residentielle', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ZoneDetailSerializer
        return ZoneListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        quartier_id = self.request.query_params.get('quartier_id')
        district_id = self.request.query_params.get('district_id')
        
        if quartier_id:
            qs = qs.filter(quartier_id=quartier_id)
        elif district_id:
            qs = qs.filter(quartier__district_id=district_id)
        
        return qs


class CollineOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Collines (16K+ entités)"""
    queryset = Colline.objects.select_related('zone', 'zone__quartier').all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['zone', 'type_colline', 'zone_rurale', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'altitude_m', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CollineDetailSerializer
        return CollineListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        zone_id = self.request.query_params.get('zone_id')
        quartier_id = self.request.query_params.get('quartier_id')
        
        if zone_id:
            qs = qs.filter(zone_id=zone_id)
        elif quartier_id:
            qs = qs.filter(zone__quartier_id=quartier_id)
        
        return qs


class PointDeServiceOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Points de Service"""
    queryset = PointDeService.objects.select_related('quartier', 'quartier__district').all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quartier', 'type_point', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code']
    ordering_fields = ['nom', 'code', 'type_point', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PointDeServiceDetailSerializer
        return PointDeServiceListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        quartier_id = self.request.query_params.get('quartier_id')
        district_id = self.request.query_params.get('district_id')
        
        if quartier_id:
            qs = qs.filter(quartier_id=quartier_id)
        elif district_id:
            qs = qs.filter(quartier__district_id=district_id)
        
        return qs


# ============================================================================
# ENDPOINT HIÉRARCHIE OPTIMISÉE
# ============================================================================

class HierarchieOptimiseeViewSet(viewsets.ViewSet):
    """Endpoint optimisé pour récupérer la hiérarchie avec filtres"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Statistiques globales de la hiérarchie"""
        stats = {
            'pays': {
                'total': Pays.objects.count(),
                'actifs': Pays.objects.filter(est_actif=True).count(),
            },
            'provinces': {
                'total': Province.objects.count(),
                'actifs': Province.objects.filter(est_actif=True).count(),
            },
            'districts': {
                'total': District.objects.count(),
                'actifs': District.objects.filter(est_actif=True).count(),
            },
            'communes': {
                'total': Commune.objects.count(),
                'actifs': Commune.objects.filter(est_actif=True).count(),
            },
            'secteurs': {
                'total': Secteur.objects.count(),
                'actifs': Secteur.objects.filter(est_actif=True).count(),
            },
            'quartiers': {
                'total': Quartier.objects.count(),
                'actifs': Quartier.objects.filter(est_actif=True).count(),
            },
            'zones': {
                'total': Zone.objects.count(),
                'actifs': Zone.objects.filter(est_actif=True).count(),
            },
            'collines': {
                'total': Colline.objects.count(),
                'actifs': Colline.objects.filter(est_actif=True).count(),
            },
            'points_de_service': {
                'total': PointDeService.objects.count(),
                'actifs': PointDeService.objects.filter(est_actif=True).count(),
            },
        }
        return Response(stats)
    
    def list(self, request):
        """Récupère la hiérarchie filtrée par niveau"""
        niveau = request.query_params.get('niveau', 'pays')
        pays_id = request.query_params.get('pays_id')
        province_id = request.query_params.get('province_id')
        district_id = request.query_params.get('district_id')
        commune_id = request.query_params.get('commune_id')
        secteur_id = request.query_params.get('secteur_id')
        quartier_id = request.query_params.get('quartier_id')
        zone_id = request.query_params.get('zone_id')
        
        # Construire la requête selon le niveau
        if niveau == 'provinces' and pays_id:
            qs = Province.objects.filter(pays_id=pays_id, est_actif=True)
            serializer = ProvinceListSerializer(qs, many=True)
        elif niveau == 'districts' and province_id:
            qs = District.objects.filter(province_id=province_id, est_actif=True)
            serializer = DistrictListSerializer(qs, many=True)
        elif niveau == 'communes' and district_id:
            qs = Commune.objects.filter(district_id=district_id, est_actif=True)
            serializer = CommuneListSerializer(qs, many=True)
        elif niveau == 'secteurs' and commune_id:
            qs = Secteur.objects.filter(commune_id=commune_id, est_actif=True)
            serializer = SecteurListSerializer(qs, many=True)
        elif niveau == 'quartiers' and district_id:
            qs = Quartier.objects.filter(district_id=district_id, est_actif=True)
            serializer = QuartierListSerializer(qs, many=True)
        elif niveau == 'zones' and quartier_id:
            qs = Zone.objects.filter(quartier_id=quartier_id, est_actif=True)
            serializer = ZoneListSerializer(qs, many=True)
        elif niveau == 'collines' and zone_id:
            qs = Colline.objects.filter(zone_id=zone_id, est_actif=True)
            serializer = CollineListSerializer(qs, many=True)
        elif niveau == 'points_de_service' and quartier_id:
            qs = PointDeService.objects.filter(quartier_id=quartier_id, est_actif=True)
            serializer = PointDeServiceListSerializer(qs, many=True)
        else:
            qs = Pays.objects.filter(est_actif=True)
            serializer = PaysListSerializer(qs, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='complete')
    def complete(self, request):
        """
        Hiérarchie complète avec filtres généalogiques.
        Retourne tous les niveaux filtrés selon les paramètres.
        """
        params = request.query_params
        
        # Initialiser les querysets
        provinces_qs = Province.objects.select_related('pays').all()
        districts_qs = District.objects.select_related('province', 'province__pays').all()
        communes_qs = Commune.objects.select_related('district', 'district__province').all()
        secteurs_qs = Secteur.objects.select_related('commune', 'commune__district').all()
        quartiers_qs = Quartier.objects.select_related('district', 'secteur').all()
        zones_qs = Zone.objects.select_related('quartier', 'quartier__district').all()
        collines_qs = Colline.objects.select_related('zone', 'zone__quartier').all()
        points_qs = PointDeService.objects.select_related('quartier', 'quartier__district').all()
        
        # Filtres par pays
        if params.get('pays_id'):
            pays_id = params['pays_id']
            provinces_qs = provinces_qs.filter(pays_id=pays_id)
            districts_qs = districts_qs.filter(province__pays_id=pays_id)
            communes_qs = communes_qs.filter(district__province__pays_id=pays_id)
            secteurs_qs = secteurs_qs.filter(commune__district__province__pays_id=pays_id)
            quartiers_qs = quartiers_qs.filter(district__province__pays_id=pays_id)
            zones_qs = zones_qs.filter(quartier__district__province__pays_id=pays_id)
            collines_qs = collines_qs.filter(zone__quartier__district__province__pays_id=pays_id)
            points_qs = points_qs.filter(quartier__district__province__pays_id=pays_id)
        
        # Filtres par province
        if params.get('province_id'):
            province_id = params['province_id']
            provinces_qs = provinces_qs.filter(id=province_id)
            districts_qs = districts_qs.filter(province_id=province_id)
            communes_qs = communes_qs.filter(district__province_id=province_id)
            secteurs_qs = secteurs_qs.filter(commune__district__province_id=province_id)
            quartiers_qs = quartiers_qs.filter(district__province_id=province_id)
            zones_qs = zones_qs.filter(quartier__district__province_id=province_id)
            collines_qs = collines_qs.filter(zone__quartier__district__province_id=province_id)
            points_qs = points_qs.filter(quartier__district__province_id=province_id)
        
        # Filtres par district
        if params.get('district_id'):
            district_id = params['district_id']
            districts_qs = districts_qs.filter(id=district_id)
            communes_qs = communes_qs.filter(district_id=district_id)
            secteurs_qs = secteurs_qs.filter(commune__district_id=district_id)
            quartiers_qs = quartiers_qs.filter(district_id=district_id)
            zones_qs = zones_qs.filter(quartier__district_id=district_id)
            collines_qs = collines_qs.filter(zone__quartier__district_id=district_id)
            points_qs = points_qs.filter(quartier__district_id=district_id)
        
        # Filtres par commune
        if params.get('commune_id'):
            commune_id = params['commune_id']
            communes_qs = communes_qs.filter(id=commune_id)
            secteurs_qs = secteurs_qs.filter(commune_id=commune_id)
        
        # Filtres par quartier
        if params.get('quartier_id'):
            quartier_id = params['quartier_id']
            quartiers_qs = quartiers_qs.filter(id=quartier_id)
            zones_qs = zones_qs.filter(quartier_id=quartier_id)
            collines_qs = collines_qs.filter(zone__quartier_id=quartier_id)
            points_qs = points_qs.filter(quartier_id=quartier_id)
        
        # Filtres par zone
        if params.get('zone_id'):
            zone_id = params['zone_id']
            zones_qs = zones_qs.filter(id=zone_id)
            collines_qs = collines_qs.filter(zone_id=zone_id)
        
        # Filtres par statut actif
        if 'est_actif' in params:
            val = params.get('est_actif', '').lower()
            est_actif = val in ('true', '1', 'yes')
            provinces_qs = provinces_qs.filter(est_actif=est_actif)
            districts_qs = districts_qs.filter(est_actif=est_actif)
            communes_qs = communes_qs.filter(est_actif=est_actif)
            secteurs_qs = secteurs_qs.filter(est_actif=est_actif)
            quartiers_qs = quartiers_qs.filter(est_actif=est_actif)
            zones_qs = zones_qs.filter(est_actif=est_actif)
            collines_qs = collines_qs.filter(est_actif=est_actif)
            points_qs = points_qs.filter(est_actif=est_actif)
        
        # Filtres par autorisation système
        if 'autorise_systeme' in params:
            val = params.get('autorise_systeme', '').lower()
            autorise = val in ('true', '1', 'yes')
            provinces_qs = provinces_qs.filter(autorise_systeme=autorise)
            districts_qs = districts_qs.filter(autorise_systeme=autorise)
            communes_qs = communes_qs.filter(autorise_systeme=autorise)
            secteurs_qs = secteurs_qs.filter(autorise_systeme=autorise)
            quartiers_qs = quartiers_qs.filter(autorise_systeme=autorise)
            zones_qs = zones_qs.filter(autorise_systeme=autorise)
            collines_qs = collines_qs.filter(autorise_systeme=autorise)
            points_qs = points_qs.filter(autorise_systeme=autorise)
        
        # Ordonner les résultats
        provinces_qs = provinces_qs.order_by('pays__nom', 'nom')
        districts_qs = districts_qs.order_by('province__nom', 'nom')
        communes_qs = communes_qs.order_by('district__nom', 'nom')
        secteurs_qs = secteurs_qs.order_by('commune__nom', 'nom')
        quartiers_qs = quartiers_qs.order_by('district__nom', 'nom')
        zones_qs = zones_qs.order_by('quartier__nom', 'nom')
        collines_qs = collines_qs.order_by('zone__nom', 'nom')
        points_qs = points_qs.order_by('quartier__nom', 'nom')
        
        # Préparer les données
        data = {
            'provinces': ProvinceListSerializer(provinces_qs, many=True).data,
            'districts': DistrictListSerializer(districts_qs, many=True).data,
            'communes': CommuneListSerializer(communes_qs, many=True).data,
            'secteurs': SecteurListSerializer(secteurs_qs, many=True).data,
            'quartiers': QuartierListSerializer(quartiers_qs, many=True).data,
            'zones': ZoneListSerializer(zones_qs, many=True).data,
            'collines': CollineListSerializer(collines_qs, many=True).data,
            'points_de_service': PointDeServiceListSerializer(points_qs, many=True).data,
            'statistiques': {
                'total_provinces': provinces_qs.count(),
                'total_districts': districts_qs.count(),
                'total_communes': communes_qs.count(),
                'total_secteurs': secteurs_qs.count(),
                'total_quartiers': quartiers_qs.count(),
                'total_zones': zones_qs.count(),
                'total_collines': collines_qs.count(),
                'total_points_de_service': points_qs.count(),
            }
        }
        
        return Response(data)
