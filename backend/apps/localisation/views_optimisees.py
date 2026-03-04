"""
Vues optimisées pour la structure GADM avec pagination et filtres.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Pays, Province, District, PointDeService, DivisionNiveau0, DivisionNiveau1, DivisionNiveau2
from .serializers_optimises import *
from .permissions import IsSystemeOrSuperAdmin


# ============================================================================
# PAGINATION
# ============================================================================

class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class LargePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


# ============================================================================
# VIEWSETS POUR PAYS (Table de référence)
# ============================================================================

class PaysOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Pays (table de référence)"""
    queryset = Pays.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code_iso_2', 'continent', 'sous_region', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'nom_anglais', 'code_iso_2', 'code_iso_3']
    ordering_fields = ['nom', 'code_iso_2', 'continent', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PaysDetailSerializer
        return PaysListSerializer


# ============================================================================
# VIEWSETS POUR DIVISIONS GADM (lecture seule)
# ============================================================================

class DivisionNiveau0ViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour Niveau 0 - Pays GADM"""
    queryset = DivisionNiveau0.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code_iso', 'continent_code', 'region_code', 'est_actif']
    search_fields = ['nom_pays', 'code_iso', 'gid_0']
    ordering_fields = ['nom_pays', 'code_iso']
    ordering = ['nom_pays']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DivisionNiveau0DetailSerializer
        return DivisionNiveau0ListSerializer


class DivisionNiveau1ViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour Niveau 1 - Provinces GADM"""
    queryset = DivisionNiveau1.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LargePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pays_division_id', 'code_iso', 'type_1', 'est_actif']
    search_fields = ['nom_1', 'nom_variante_1', 'nom_local_1', 'code_1']
    ordering_fields = ['nom_1', 'code_1', 'nom_pays']
    ordering = ['nom_pays', 'nom_1']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DivisionNiveau1DetailSerializer
        return DivisionNiveau1ListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        pays_division_id = self.request.query_params.get('pays_division_id')
        code_iso = self.request.query_params.get('code_iso')
        
        if pays_division_id:
            qs = qs.filter(pays_division_id=pays_division_id)
        elif code_iso:
            qs = qs.filter(code_iso=code_iso)
        
        return qs


class DivisionNiveau2ViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour Niveau 2 - Districts GADM"""
    queryset = DivisionNiveau2.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LargePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pays_division_id', 'parent_division_id', 'code_iso', 'type_2', 'est_actif']
    search_fields = ['nom_2', 'nom_variante_2', 'nom_local_2', 'code_2', 'nom_1']
    ordering_fields = ['nom_2', 'code_2', 'nom_pays', 'nom_1']
    ordering = ['nom_pays', 'nom_1', 'nom_2']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DivisionNiveau2DetailSerializer
        return DivisionNiveau2ListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        pays_division_id = self.request.query_params.get('pays_division_id')
        parent_division_id = self.request.query_params.get('parent_division_id')
        code_iso = self.request.query_params.get('code_iso')
        
        if parent_division_id:
            qs = qs.filter(parent_division_id=parent_division_id)
        elif pays_division_id:
            qs = qs.filter(pays_division_id=pays_division_id)
        elif code_iso:
            qs = qs.filter(code_iso=code_iso)
        
        return qs


# ============================================================================
# VIEWSETS POUR POINTS DE SERVICE
# ============================================================================

class PointDeServiceOptimiseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet optimisé pour Points de Service"""
    queryset = PointDeService.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['quartier_id', 'type_point', 'est_actif', 'autorise_systeme']
    search_fields = ['nom', 'code', 'adresse_complementaire']
    ordering_fields = ['nom', 'code', 'type_point', 'date_creation']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PointDeServiceDetailSerializer
        return PointDeServiceListSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        quartier_id = self.request.query_params.get('quartier_id')
        
        if quartier_id:
            qs = qs.filter(quartier_id=quartier_id)
        
        return qs


# ============================================================================
# ALIAS POUR COMPATIBILITÉ
# ============================================================================

# Alias pour faciliter l'utilisation
ProvinceOptimiseViewSet = DivisionNiveau1ViewSet
DistrictOptimiseViewSet = DivisionNiveau2ViewSet


# ============================================================================
# VUES STATISTIQUES
# ============================================================================

class LocalisationStatistiquesViewSet(viewsets.ViewSet):
    """Statistiques globales sur la localisation"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def resume(self, request):
        """Résumé des statistiques de localisation"""
        return Response({
            'pays_reference': {
                'total': Pays.objects.count(),
                'actifs': Pays.objects.filter(est_actif=True).count(),
            },
            'divisions_niveau0': {
                'total': DivisionNiveau0.objects.count(),
                'actifs': DivisionNiveau0.objects.filter(est_actif=True).count(),
            },
            'divisions_niveau1': {
                'total': DivisionNiveau1.objects.count(),
                'actifs': DivisionNiveau1.objects.filter(est_actif=True).count(),
            },
            'divisions_niveau2': {
                'total': DivisionNiveau2.objects.count(),
                'actifs': DivisionNiveau2.objects.filter(est_actif=True).count(),
            },
            'points_de_service': {
                'total': PointDeService.objects.count(),
                'actifs': PointDeService.objects.filter(est_actif=True).count(),
            },
        })
    
    @action(detail=False, methods=['get'])
    def hierarchie(self, request):
        """Récupère la hiérarchie selon le niveau demandé"""
        niveau = request.query_params.get('niveau')
        pays_division_id = request.query_params.get('pays_division_id')
        parent_division_id = request.query_params.get('parent_division_id')
        code_iso = request.query_params.get('code_iso')
        
        # Construire la requête selon le niveau
        if niveau == 'pays':
            qs = Pays.objects.filter(est_actif=True)
            serializer = PaysListSerializer(qs, many=True)
        elif niveau == 'niveau0':
            qs = DivisionNiveau0.objects.filter(est_actif=True)
            if code_iso:
                qs = qs.filter(code_iso=code_iso)
            serializer = DivisionNiveau0ListSerializer(qs, many=True)
        elif niveau == 'niveau1' or niveau == 'provinces':
            qs = DivisionNiveau1.objects.filter(est_actif=True)
            if pays_division_id:
                qs = qs.filter(pays_division_id=pays_division_id)
            elif code_iso:
                qs = qs.filter(code_iso=code_iso)
            serializer = DivisionNiveau1ListSerializer(qs, many=True)
        elif niveau == 'niveau2' or niveau == 'districts':
            qs = DivisionNiveau2.objects.filter(est_actif=True)
            if parent_division_id:
                qs = qs.filter(parent_division_id=parent_division_id)
            elif pays_division_id:
                qs = qs.filter(pays_division_id=pays_division_id)
            elif code_iso:
                qs = qs.filter(code_iso=code_iso)
            serializer = DivisionNiveau2ListSerializer(qs, many=True)
        else:
            return Response(
                {'error': 'Niveau invalide. Utilisez: pays, niveau0, niveau1, niveau2, provinces, districts'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'niveau': niveau,
            'total': qs.count(),
            'donnees': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def recherche_globale(self, request):
        """Recherche globale dans toutes les divisions"""
        query = request.query_params.get('q', '')
        
        if len(query) < 2:
            return Response(
                {'error': 'La recherche doit contenir au moins 2 caractères'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Recherche dans toutes les tables
        pays_qs = Pays.objects.filter(
            Q(nom__icontains=query) | Q(code_iso_2__icontains=query)
        ).filter(est_actif=True)[:10]
        
        niveau1_qs = DivisionNiveau1.objects.filter(
            Q(nom_1__icontains=query) | Q(code_1__icontains=query)
        ).filter(est_actif=True)[:20]
        
        niveau2_qs = DivisionNiveau2.objects.filter(
            Q(nom_2__icontains=query) | Q(code_2__icontains=query)
        ).filter(est_actif=True)[:20]
        
        return Response({
            'query': query,
            'resultats': {
                'pays': PaysListSerializer(pays_qs, many=True).data,
                'provinces': DivisionNiveau1ListSerializer(niveau1_qs, many=True).data,
                'districts': DivisionNiveau2ListSerializer(niveau2_qs, many=True).data,
            }
        })
