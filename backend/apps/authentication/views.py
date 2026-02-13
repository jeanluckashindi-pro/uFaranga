import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from apps.users.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger('apps')


# =============================================================================
# LOGIN — Obtention de token JWT
# =============================================================================
@extend_schema(tags=['Authentication'])
class LoginView(TokenObtainPairView):
    """
    Connexion utilisateur.
    
    Retourne un access token et un refresh token JWT.
    L'access token expire après 60 minutes.
    Le refresh token expire après 7 jours.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# =============================================================================
# REGISTER — Inscription
# =============================================================================
@extend_schema(tags=['Authentication'])
class RegisterView(generics.CreateAPIView):
    """
    Inscription d'un nouvel utilisateur.
    
    Crée un compte utilisateur avec un profil par défaut.
    Retourne les tokens JWT pour connexion automatique.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Générer les tokens JWT pour connexion automatique
        refresh = RefreshToken.for_user(user)

        logger.info(f"Nouvel utilisateur inscrit: {user.email}")

        return Response({
            'message': 'Inscription réussie',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


# =============================================================================
# TOKEN REFRESH — Rafraîchir le token
# =============================================================================
@extend_schema(tags=['Authentication'])
class RefreshTokenView(TokenRefreshView):
    """
    Rafraîchir le token d'accès.
    
    Utilise le refresh token pour obtenir un nouveau access token.
    L'ancien refresh token est blacklisté et un nouveau est généré.
    """
    pass


# =============================================================================
# LOGOUT — Déconnexion
# =============================================================================
@extend_schema(tags=['Authentication'])
class LogoutView(APIView):
    """
    Déconnexion utilisateur.
    
    Blackliste le refresh token pour empêcher sa réutilisation.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Le refresh token est requis.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(f"Utilisateur déconnecté: {request.user.email}")

            return Response(
                {'message': 'Déconnexion réussie'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.warning(f"Erreur lors de la déconnexion: {str(e)}")
            return Response(
                {'error': 'Token invalide.'},
                status=status.HTTP_400_BAD_REQUEST
            )


# =============================================================================
# LOGOUT ALL — Déconnecter toutes les sessions
# =============================================================================
@extend_schema(tags=['Authentication'])
class LogoutAllView(APIView):
    """
    Déconnecter toutes les sessions.
    
    Blackliste tous les refresh tokens de l'utilisateur.
    Utile en cas de compromission du compte.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            logger.info(f"Toutes les sessions invalidées pour: {request.user.email}")

            return Response(
                {'message': 'Toutes les sessions ont été fermées.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Erreur logout all: {str(e)}")
            return Response(
                {'error': 'Erreur interne.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =============================================================================
# CHANGE PASSWORD — Changer le mot de passe
# =============================================================================
@extend_schema(tags=['Authentication'])
class ChangePasswordView(APIView):
    """
    Changer le mot de passe de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        logger.info(f"Mot de passe changé pour: {request.user.email}")

        return Response(
            {'message': 'Mot de passe modifié avec succès.'},
            status=status.HTTP_200_OK
        )


# =============================================================================
# ME — Profil de l'utilisateur connecté
# =============================================================================
@extend_schema(tags=['Authentication'])
class MeView(APIView):
    """
    Récupérer le profil de l'utilisateur connecté.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
