import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from django.utils import timezone
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
from apps.identite.models import Utilisateur as UtilisateurIdentite
from apps.identite.serializers import UtilisateurIdentiteSerializer, UtilisateurIdentiteUpdateSerializer
from .services_sessions import get_sessions_actives_info
from .auth_security import reinitialiser_valeurs_deconnexion

User = get_user_model()
logger = logging.getLogger('apps')


# =============================================================================
# LOGIN — Obtention de token JWT
# =============================================================================
@extend_schema(tags=['Authentication'])
class LoginView(TokenObtainPairView):
    """
    Connexion utilisateur.
    
    Body optionnel : `remember_me` (booléen). Si true, le refresh token dure 30 jours ;
    sinon 7 jours. L'access token reste 60 minutes.
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
    
    Blackliste le refresh token puis réinitialise en base (identite.utilisateurs)
    les valeurs clés : nombre_tentatives_connexion, bloque_jusqua.
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

            reinitialiser_valeurs_deconnexion(request.user)

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
    
    Blackliste tous les refresh tokens de l'utilisateur puis réinitialise
    en base (identite) les valeurs clés (tentatives, blocage).
    Utile en cas de compromission du compte.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            reinitialiser_valeurs_deconnexion(request.user)

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
# LOGOUT OTHER SESSIONS — Déconnecter les autres sessions (garder la session actuelle)
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Déconnecter les autres sessions',
    description=(
        'Quand la personne est notifiée que son compte a plus de 2 connexions, '
        'elle peut invalider toutes les autres sessions en gardant uniquement celle en cours. '
        'Body : {"refresh": "<votre_refresh_token_actuel>"}.'
    ),
    request={'application/json': {'schema': {'type': 'object', 'properties': {'refresh': {'type': 'string'}}, 'required': ['refresh']}}},
    responses={
        200: {'description': 'Les autres sessions ont été fermées.'},
        400: {'description': 'Refresh token requis ou invalide.'},
    },
)
class LogoutOtherSessionsView(APIView):
    """
    Déconnecte toutes les sessions sauf celle correspondant au refresh token envoyé.
    À utiliser après notification "connexion multiple" pour garder uniquement cette session.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Le refresh token est requis pour identifier la session à conserver.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
        except Exception:
            return Response(
                {'error': 'Refresh token invalide ou expiré.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id_claim = jwt_settings.USER_ID_CLAIM
        jti_claim = jwt_settings.JTI_CLAIM
        if str(token.get(user_id_claim)) != str(request.user.id):
            return Response(
                {'error': 'Ce token ne correspond pas à votre compte.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        current_jti = token.get(jti_claim)
        if not current_jti:
            return Response(
                {'error': 'Refresh token invalide.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        now = timezone.now()
        # Tous les tokens de l'utilisateur non expirés, non blacklistés, sauf le jti actuel
        others = OutstandingToken.objects.filter(
            user_id=request.user.id,
            expires_at__gt=now,
        ).exclude(jti=current_jti)
        # Exclure ceux déjà blacklistés
        others = others.filter(blacklistedtoken__isnull=True)
        count = 0
        for ot in others:
            BlacklistedToken.objects.get_or_create(token=ot)
            count += 1
        logger.info(f"Déconnexion de {count} autre(s) session(s) pour {request.user.email}, session actuelle conservée.")
        return Response({
            'message': f'Les autres sessions ont été fermées ({count} session(s) déconnectée(s)). Vous restez connecté sur cette session.',
            'sessions_deconnectees': count,
        }, status=status.HTTP_200_OK)


# =============================================================================
# CHANGE PASSWORD — Changer le mot de passe (vérification + identite + users)
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Modifier le mot de passe',
    description=(
        'Modification sécurisée : mot de passe actuel requis, confirmation du nouveau, '
        'mise à jour dans identite et users. Body : mot_de_passe_actuel, nouveau_mot_de_passe, nouveau_mot_de_passe_confirmation.'
    ),
)
class ChangePasswordView(APIView):
    """
    Changer le mot de passe avec vérification stricte.
    Met à jour identite.utilisateurs (source de vérité) et users.User.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['nouveau_mot_de_passe']

        # Mise à jour users.User
        request.user.set_password(new_password)
        request.user.save(update_fields=['password'])

        # Mise à jour identite (source de vérité) : hash + derniere_modification_mdp
        utilisateur_identite = UtilisateurIdentite.objects.filter(
            courriel=request.user.email
        ).first()
        if utilisateur_identite:
            utilisateur_identite.set_password(new_password)
            utilisateur_identite.derniere_modification_mdp = timezone.now()
            utilisateur_identite.save(update_fields=['password', 'derniere_modification_mdp'])

        logger.info("Mot de passe modifié avec succès pour %s", request.user.email)

        return Response(
            {'message': 'Mot de passe modifié avec succès.'},
            status=status.HTTP_200_OK
        )


# =============================================================================
# ME — Profil de l'utilisateur connecté (GET) et modification (PUT/PATCH)
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Profil (moi)',
    description='GET : infos complètes. PUT/PATCH : modifier les informations de la personne (identite + profil).',
)
class MeView(APIView):
    """
    GET : toutes les infos de la personne (identite + sessions_actives).
    PUT / PATCH : modifier les infos complètes (coordonnées, adresse, profil).
    Seul le compte connecté peut modifier ses propres données.
    """
    permission_classes = [IsAuthenticated]

    def _get_utilisateur_identite(self, request):
        return UtilisateurIdentite.objects.filter(
            courriel=request.user.email
        ).select_related('profil').first()

    def get(self, request):
        sessions_info = get_sessions_actives_info(request.user)
        utilisateur_identite = self._get_utilisateur_identite(request)
        if utilisateur_identite:
            serializer = UtilisateurIdentiteSerializer(utilisateur_identite)
            data = dict(serializer.data)
            data['sessions_actives'] = sessions_info
            return Response(data)
        data = UserSerializer(request.user).data
        data['type_utilisateur'] = None
        data['statut'] = None
        data['sessions_actives'] = sessions_info
        return Response(data)

    def put(self, request):
        """Mise à jour complète (tous les champs envoyés)."""
        return self._update_me(request, partial=False)

    def patch(self, request):
        """Mise à jour partielle (seuls les champs envoyés)."""
        return self._update_me(request, partial=True)

    def _update_me(self, request, partial=False):
        utilisateur_identite = self._get_utilisateur_identite(request)
        if not utilisateur_identite:
            return Response(
                {'error': 'Profil identite introuvable pour ce compte.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UtilisateurIdentiteUpdateSerializer(
            instance=utilisateur_identite,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Synchroniser users.User pour cohérence (courriel, nom, téléphone)
        u = request.user
        u.email = utilisateur_identite.courriel
        u.first_name = utilisateur_identite.prenom or ''
        u.last_name = utilisateur_identite.nom_famille or ''
        u.phone_number = utilisateur_identite.numero_telephone or None
        u.username = (utilisateur_identite.courriel or '').split('@')[0] if '@' in (utilisateur_identite.courriel or '') else (utilisateur_identite.courriel or str(u.pk))
        u.save(update_fields=['email', 'first_name', 'last_name', 'phone_number', 'username'])
        # Réponse : profil complet comme en GET
        sessions_info = get_sessions_actives_info(request.user)
        response_serializer = UtilisateurIdentiteSerializer(utilisateur_identite)
        data = dict(response_serializer.data)
        data['sessions_actives'] = sessions_info
        return Response(data, status=status.HTTP_200_OK)


# =============================================================================
# SESSIONS ACTIVES — Savoir si le compte est utilisé à plusieurs endroits
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Sessions actives',
    description=(
        'Nombre de sessions actives (jetons JWT non révoqués) pour le compte connecté. '
        'Si > 1 : le même compte est utilisé par plusieurs personnes ou appareils en même temps.'
    ),
    responses={200: {'description': 'Nombre de sessions et indicateur de connexion multiple'}},
)
class SessionsActivesView(APIView):
    """
    Retourne le nombre de sessions actives et un indicateur de connexion multiple.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        info = get_sessions_actives_info(request.user)
        return Response(info)
