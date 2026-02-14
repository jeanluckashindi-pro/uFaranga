import logging
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserSessionSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from .models import UserProfile, UserSession
from .permissions import IsOwnerOrAdmin

User = get_user_model()
logger = logging.getLogger('apps')


# =============================================================================
# USER VIEWSET — CRUD Utilisateurs
# =============================================================================
@extend_schema_view(
    list=extend_schema(tags=['Users'], description='Lister tous les utilisateurs (admin uniquement)'),
    retrieve=extend_schema(tags=['Users'], description='Détails d\'un utilisateur'),
    update=extend_schema(tags=['Users'], description='Mettre à jour un utilisateur'),
    partial_update=extend_schema(tags=['Users'], description='Mise à jour partielle'),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs.
    
    - Liste (GET /api/v1/utilisateurs/) — Admin uniquement
    - Détail (GET /api/v1/utilisateurs/{id}/) — Propriétaire ou Admin
    - Mise à jour (PUT/PATCH /api/v1/utilisateurs/{id}/) — Propriétaire ou Admin
    """
    queryset = User.objects.select_related('profile').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        if self.action in ('retrieve', 'update', 'partial_update'):
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    # --- Profil étendu ---
    @extend_schema(tags=['Users'])
    @action(detail=True, methods=['get', 'put', 'patch'], url_path='profile')
    def profile(self, request, pk=None):
        """GET/PUT/PATCH le profil étendu d'un utilisateur."""
        user = self.get_object()
        profile, _ = UserProfile.objects.get_or_create(user=user)

        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)

        serializer = UserProfileUpdateSerializer(
            profile, data=request.data, partial=(request.method == 'PATCH')
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # --- Sessions actives ---
    @extend_schema(tags=['Sessions'])
    @action(detail=True, methods=['get'], url_path='sessions')
    def sessions(self, request, pk=None):
        """Lister les sessions actives d'un utilisateur."""
        user = self.get_object()
        sessions = UserSession.objects.filter(user=user, is_active=True)
        serializer = UserSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    # --- Rechercher un utilisateur par téléphone ---
    @extend_schema(tags=['Users'])
    @action(detail=False, methods=['get'], url_path='search-by-phone')
    def search_by_phone(self, request):
        """
        Rechercher un utilisateur par numéro de téléphone.
        Utilisé par les autres services pour vérifier un bénéficiaire.
        """
        phone = request.query_params.get('phone')
        if not phone:
            return Response(
                {'error': 'Le paramètre "phone" est requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(phone_number=phone, is_active=True)
            return Response({
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'kyc_level': user.kyc_level,
                'can_transact': user.can_transact(),
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )

    # --- Rechercher par email ---
    @extend_schema(tags=['Users'])
    @action(detail=False, methods=['get'], url_path='search-by-email')
    def search_by_email(self, request):
        """Rechercher un utilisateur par email."""
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Le paramètre "email" est requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email.lower(), is_active=True)
            return Response({
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'kyc_level': user.kyc_level,
                'can_transact': user.can_transact(),
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )

    # --- Vérifier si un utilisateur peut effectuer des transactions ---
    @extend_schema(tags=['Users'])
    @action(detail=True, methods=['get'], url_path='can-transact')
    def can_transact(self, request, pk=None):
        """Vérifier si un utilisateur peut effectuer des transactions (inter-service)."""
        user = self.get_object()
        return Response({
            'user_id': str(user.id),
            'can_transact': user.can_transact(),
            'kyc_level': user.kyc_level,
            'is_phone_verified': user.is_phone_verified,
            'is_active': user.is_active,
        })
