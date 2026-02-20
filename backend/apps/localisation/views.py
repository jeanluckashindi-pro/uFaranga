"""
CRUD localisation (Pays, Province, District, Quartier, Point de service).

Permissions:
- GET (list, retrieve): Accès public (AllowAny)
- POST, PUT, PATCH, DELETE: Réservé aux utilisateurs SYSTEME et SUPER_ADMIN
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from .models import Pays, Province, District, Quartier, PointDeService
from .filters import PaysFilterSet
from .serializers import (
    PaysSerializer,
    PaysDetailSerializer,
    CouverturePaysSerializer,
    ProvinceSerializer,
    DistrictSerializer,
    QuartierSerializer,
    PointDeServiceSerializer,
)
from .permissions import IsSystemeOrSuperAdmin


@extend_schema_view(
    list=extend_schema(summary='Liste des pays (Public)', tags=['Localisation']),
    create=extend_schema(summary='Créer un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(
        summary='Détail d\'un pays (Public)',
        tags=['Localisation'],
    ),
    update=extend_schema(summary='Modifier un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un pays', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [IsSystemeOrSuperAdmin]  # Default, overridden by get_permissions()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PaysFilterSet
    search_fields = ['code_iso_2', 'code_iso_3', 'nom', 'nom_anglais']
    ordering_fields = ['nom', 'code_iso_2', 'date_creation', 'date_modification']
    ordering = ['nom']
    
    def get_permissions(self):
        """
        Permissions publiques pour GET (list, retrieve, couverture).
        Permissions admin pour POST/PUT/PATCH/DELETE.
        """
        if self.action in ['list', 'retrieve', 'couverture']:
            return [AllowAny()]
        return [IsSystemeOrSuperAdmin()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PaysDetailSerializer
        return PaysSerializer

    def get_queryset(self):
        qs = Pays.objects.all()
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                'provinces',
                'provinces__districts',
                'provinces__districts__quartiers',
                'provinces__districts__quartiers__points_de_service',
            )
        return qs

    @extend_schema(
        summary='Couverture mondiale : pays, provinces, districts, quartiers, points de vente',
        description='Hiérarchie complète des pays couverts avec coordonnées, statistiques (actifs/inactifs) à chaque niveau. '
                    'Chaque pays contient ses provinces → districts → quartiers → points de service.',
        tags=['Localisation (SYSTEME/SUPER_ADMIN)'],
        parameters=[
            OpenApiParameter(name='pays_id', type=str, description='Filtrer par UUID d’un pays (un seul pays retourné)'),
            OpenApiParameter(name='code_iso_2', type=str, description='Filtrer par code ISO 2 (ex. BI, RW)'),
            OpenApiParameter(name='nom', type=str, description='Filtrer par nom du pays (contient)'),
            OpenApiParameter(name='autorise_systeme', type=bool, description='Filtrer par autorise_systeme (true/false). Si absent : tous les pays.'),
            OpenApiParameter(name='est_actif', type=bool, description='Filtrer par est_actif (true/false). Si absent : tous les pays.'),
        ],
    )
    @action(detail=False, url_path='couverture', methods=['get'])
    def couverture(self, request):
        params = request.query_params
        qs = Pays.objects.all()

        # Filtres (appliqués seulement si le paramètre est fourni)
        if params.get('pays_id'):
            qs = qs.filter(id=params['pays_id'])
        if params.get('code_iso_2'):
            qs = qs.filter(code_iso_2__iexact=params['code_iso_2'].strip())
        if params.get('nom'):
            qs = qs.filter(nom__icontains=params['nom'].strip())
        if 'autorise_systeme' in params:
            val = params.get('autorise_systeme', '').lower()
            if val in ('true', '1', 'yes'):
                qs = qs.filter(autorise_systeme=True)
            elif val in ('false', '0', 'no'):
                qs = qs.filter(autorise_systeme=False)
        if 'est_actif' in params:
            val = params.get('est_actif', '').lower()
            if val in ('true', '1', 'yes'):
                qs = qs.filter(est_actif=True)
            elif val in ('false', '0', 'no'):
                qs = qs.filter(est_actif=False)

        qs = qs.prefetch_related(
            'provinces',
            'provinces__districts',
            'provinces__districts__quartiers',
            'provinces__districts__quartiers__points_de_service',
        ).order_by('nom')
        serializer = CouverturePaysSerializer(qs, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary='Liste des provinces (Public)', tags=['Localisation']),
    create=extend_schema(summary='Créer une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'une province (Public)', tags=['Localisation']),
    update=extend_schema(summary='Modifier une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer une province', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.select_related('pays').all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsSystemeOrSuperAdmin]  # Default, overridden by get_permissions()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'pays__code_iso_2', 'pays__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['pays__nom', 'nom']
    
    def get_permissions(self):
        """
        Permissions publiques pour GET (list, retrieve).
        Permissions admin pour POST/PUT/PATCH/DELETE.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsSystemeOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        pays_id = self.request.query_params.get('pays_id')
        if pays_id:
            qs = qs.filter(pays_id=pays_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des districts (Public)', tags=['Localisation']),
    create=extend_schema(summary='Créer un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un district (Public)', tags=['Localisation']),
    update=extend_schema(summary='Modifier un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un district', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.select_related('province', 'province__pays').all()
    serializer_class = DistrictSerializer
    permission_classes = [IsSystemeOrSuperAdmin]  # Default, overridden by get_permissions()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'province__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['province__nom', 'nom']
    
    def get_permissions(self):
        """
        Permissions publiques pour GET (list, retrieve).
        Permissions admin pour POST/PUT/PATCH/DELETE.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsSystemeOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        province_id = self.request.query_params.get('province_id')
        if province_id:
            qs = qs.filter(province_id=province_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des quartiers (Public)', tags=['Localisation']),
    create=extend_schema(summary='Créer un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un quartier (Public)', tags=['Localisation']),
    update=extend_schema(summary='Modifier un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un quartier', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class QuartierViewSet(viewsets.ModelViewSet):
    queryset = Quartier.objects.select_related('district', 'district__province').all()
    serializer_class = QuartierSerializer
    permission_classes = [IsSystemeOrSuperAdmin]  # Default, overridden by get_permissions()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'district__nom']
    ordering_fields = ['nom', 'code', 'date_creation']
    ordering = ['district__nom', 'nom']
    
    def get_permissions(self):
        """
        Permissions publiques pour GET (list, retrieve).
        Permissions admin pour POST/PUT/PATCH/DELETE.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsSystemeOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        district_id = self.request.query_params.get('district_id')
        if district_id:
            qs = qs.filter(district_id=district_id)
        return qs


@extend_schema_view(
    list=extend_schema(summary='Liste des points de service (Public)', tags=['Localisation']),
    create=extend_schema(summary='Créer un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    retrieve=extend_schema(summary='Détail d\'un point de service (Public)', tags=['Localisation']),
    update=extend_schema(summary='Modifier un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    partial_update=extend_schema(summary='Modifier partiellement un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
    destroy=extend_schema(summary='Supprimer un point de service', tags=['Localisation (SYSTEME/SUPER_ADMIN)']),
)
class PointDeServiceViewSet(viewsets.ModelViewSet):
    queryset = PointDeService.objects.select_related('quartier', 'quartier__district', 'agent_utilisateur').all()
    serializer_class = PointDeServiceSerializer
    permission_classes = [IsSystemeOrSuperAdmin]  # Default, overridden by get_permissions()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'nom', 'quartier__nom']
    ordering_fields = ['nom', 'code', 'type_point', 'date_creation']
    ordering = ['quartier__nom', 'nom']
    
    def get_permissions(self):
        """
        Permissions publiques pour GET (list, retrieve).
        Permissions admin pour POST/PUT/PATCH/DELETE.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsSystemeOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        quartier_id = self.request.query_params.get('quartier_id')
        if quartier_id:
            qs = qs.filter(quartier_id=quartier_id)
        return qs
