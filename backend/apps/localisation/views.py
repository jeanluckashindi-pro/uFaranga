"""
CRUD localisation (Pays, Province, District, Quartier, Point de service).
Réservé aux utilisateurs SYSTEME et SUPER_ADMIN.
"""
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Pays, Province, District, Quartier, PointDeService
from .serializers import (
    PaysSerializer,
    ProvinceSerializer,
    DistrictSerializer,
    QuartierSerializer,
    PointDeServiceSerializer,
)
from .permissions import IsSystemeOrSuperAdmin


@extend_schema_view(
    list=extend_schema(summary='Liste des pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    create=extend_schema(summary='Créer un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    update=extend_schema(summary='Modifier un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [IsSystemeOrSuperAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code_iso_2', 'code_iso_3', 'nom', 'nom_anglais']
    ordering_fields = ['nom', 'code_iso_2', 'date_creation']
    ordering = ['nom']


@extend_schema_view(
    list=extend_schema(summary='Liste des provinces', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    create=extend_schema(summary='Créer une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    update=extend_schema(summary='Modifier une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.select_related('pays').all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsSystemeOrSuperAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'pays__code_iso_2', 'pays__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['pays__nom', 'nom']

    def get_queryset(self):
        qs = super().get_queryset()
        pays_id = self.request.query_params.get('pays_id')
        if pays_id:
            qs = qs.filter(pays_id=pays_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des districts', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    create=extend_schema(summary='Créer un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    update=extend_schema(summary='Modifier un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.select_related('province', 'province__pays').all()
    serializer_class = DistrictSerializer
    permission_classes = [IsSystemeOrSuperAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'province__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['province__nom', 'nom']

    def get_queryset(self):
        qs = super().get_queryset()
        province_id = self.request.query_params.get('province_id')
        if province_id:
            qs = qs.filter(province_id=province_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des quartiers', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    create=extend_schema(summary='Créer un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    update=extend_schema(summary='Modifier un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class QuartierViewSet(viewsets.ModelViewSet):
    queryset = Quartier.objects.select_related('district', 'district__province').all()
    serializer_class = QuartierSerializer
    permission_classes = [IsSystemeOrSuperAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'district__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['district__nom', 'nom']

    def get_queryset(self):
        qs = super().get_queryset()
        district_id = self.request.query_params.get('district_id')
        if district_id:
            qs = qs.filter(district_id=district_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des points de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    create=extend_schema(summary='Créer un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    update=extend_schema(summary='Modifier un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class PointDeServiceViewSet(viewsets.ModelViewSet):
    queryset = PointDeService.objects.select_related('quartier', 'quartier__district', 'agent_utilisateur').all()
    serializer_class = PointDeServiceSerializer
    permission_classes = [IsSystemeOrSuperAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'quartier__nom']
    ordering_fields = ['nom', 'code', 'type_point', 'date_creation']
    ordering = ['quartier__nom', 'nom']

    def get_queryset(self):
        qs = super().get_queryset()
        quartier_id = self.request.query_params.get('quartier_id')
        if quartier_id:
            qs = qs.filter(quartier_id=quartier_id)
        return qs
