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
    EnvoyerCodeConfirmationSerializer,
    VerifierCodeConfirmationSerializer,
    ReinitialiserMotDePasseSMSSerializer,
)
from apps.users.serializers import UserSerializer
from apps.identite.models import Utilisateur as UtilisateurIdentite
from apps.identite.serializers import UtilisateurIdentiteSerializer, UtilisateurIdentiteUpdateSerializer
from .services_sessions import get_sessions_actives_info
from .auth_security import reinitialiser_valeurs_deconnexion
from .services_sms import (
    envoyer_code_confirmation, 
    verifier_code_confirmation,
    enregistrer_changement_mot_de_passe,
    obtenir_historique_changements_mdp,
    compter_changements_mdp
)

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

        # Sauvegarder l'ancien hash
        ancien_hash = request.user.password

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

            # Enregistrer dans l'historique
            adresse_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            enregistrer_changement_mot_de_passe(
                utilisateur=utilisateur_identite,
                ancien_hash=ancien_hash,
                nouveau_hash=utilisateur_identite.password,
                type_changement='MODIFICATION',
                adresse_ip=adresse_ip,
                user_agent=user_agent,
                raison='Modification par l\'utilisateur'
            )

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


# =============================================================================
# ENVOYER CODE CONFIRMATION — Envoyer un code de confirmation par SMS
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Envoyer un code de confirmation par SMS',
    description=(
        'Génère un code de confirmation à 5 chiffres au format UF-CCF-PSW-XXXXX '
        'et l\'envoie par SMS au numéro de téléphone spécifié. '
        'Le code est valide pendant 5 minutes.'
    ),
    request=EnvoyerCodeConfirmationSerializer,
    responses={
        200: {
            'description': 'Code envoyé avec succès',
            'content': {
                'application/json': {
                    'example': {
                        'success': True,
                        'message': 'Code de confirmation envoyé avec succès',
                        'code_formate': 'UF-CCF-PSW-12345',
                        'telephone': '62046725'
                    }
                }
            }
        },
        400: {'description': 'Données invalides'},
        500: {'description': 'Erreur lors de l\'envoi du SMS'},
    },
)
class EnvoyerCodeConfirmationView(APIView):
    """
    Envoie un code de confirmation par SMS.
    
    Le code généré est au format UF-CCF-PSW-XXXXX où XXXXX est un code à 5 chiffres.
    Le code est stocké dans Redis et valide pendant 5 minutes.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EnvoyerCodeConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        telephone = serializer.validated_data['telephone']
        prenom = serializer.validated_data.get('prenom')
        
        # Récupérer les informations de l'utilisateur si disponibles
        utilisateur = UtilisateurIdentite.objects.filter(
            numero_telephone=telephone
        ).first()
        
        utilisateur_id = utilisateur.id if utilisateur else None
        courriel = utilisateur.courriel if utilisateur else ''
        prenom = prenom or (utilisateur.prenom if utilisateur else None)
        
        # Récupérer l'adresse IP et user agent
        adresse_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Envoyer le code de confirmation
        resultat = envoyer_code_confirmation(
            telephone=telephone,
            prenom=prenom,
            type_code='VERIFICATION_TELEPHONE',
            utilisateur_id=utilisateur_id,
            courriel=courriel,
            adresse_ip=adresse_ip,
            user_agent=user_agent
        )
        
        if resultat['success']:
            logger.info(f"Code de confirmation envoyé à {telephone}")
            return Response({
                'success': True,
                'message': 'Code de confirmation envoyé avec succès',
                'code_formate': resultat['code_formate'],
                'telephone': telephone,
                'date_expiration': resultat['date_expiration'],
                'duree_validite_minutes': 15,
            }, status=status.HTTP_200_OK)
        else:
            logger.error(f"Échec de l'envoi du code à {telephone}: {resultat['message']}")
            return Response({
                'success': False,
                'message': resultat['message'],
                'error': resultat.get('error'),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =============================================================================
# VERIFIER CODE CONFIRMATION — Vérifier un code de confirmation
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Vérifier un code de confirmation',
    description=(
        'Vérifie si le code de confirmation à 5 chiffres est valide pour le numéro de téléphone. '
        'Le code est supprimé après vérification réussie.'
    ),
    request=VerifierCodeConfirmationSerializer,
    responses={
        200: {
            'description': 'Code valide',
            'content': {
                'application/json': {
                    'example': {
                        'success': True,
                        'message': 'Code de confirmation valide',
                        'telephone': '62046725'
                    }
                }
            }
        },
        400: {
            'description': 'Code invalide ou expiré',
            'content': {
                'application/json': {
                    'example': {
                        'success': False,
                        'message': 'Code de confirmation invalide ou expiré'
                    }
                }
            }
        },
    },
)
class VerifierCodeConfirmationView(APIView):
    """
    Vérifie un code de confirmation.
    
    Le code doit être un nombre à 5 chiffres (sans le préfixe UF-CCF-PSW-).
    Après vérification réussie, le code est automatiquement supprimé.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifierCodeConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        telephone = serializer.validated_data['telephone']
        code = serializer.validated_data['code']
        
        # Vérifier le code
        resultat = verifier_code_confirmation(telephone, code)
        
        if resultat['valide']:
            logger.info(f"Code de confirmation vérifié avec succès pour {telephone}")
            
            # Récupérer les informations du code
            code_obj = resultat['code_obj']
            
            return Response({
                'success': True,
                'message': 'Code de confirmation valide',
                'telephone': telephone,
                'type_code': code_obj.type_code if code_obj else None,
                'utilisateur_id': str(code_obj.utilisateur_id) if code_obj and code_obj.utilisateur_id else None,
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Code de confirmation invalide pour {telephone}: {resultat['message']}")
            return Response({
                'success': False,
                'message': resultat['message'],
            }, status=status.HTTP_400_BAD_REQUEST)



# =============================================================================
# REINITIALISER MOT DE PASSE SMS — Réinitialiser le mot de passe avec code SMS
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Réinitialiser le mot de passe avec code SMS',
    description=(
        'Réinitialise le mot de passe en utilisant un code de confirmation SMS. '
        'Le code doit être valide et non expiré (15 minutes). '
        'L\'historique des changements de mot de passe est enregistré.'
    ),
    request=ReinitialiserMotDePasseSMSSerializer,
    responses={
        200: {
            'description': 'Mot de passe réinitialisé avec succès',
            'content': {
                'application/json': {
                    'example': {
                        'success': True,
                        'message': 'Mot de passe réinitialisé avec succès',
                        'nombre_changements_total': 3
                    }
                }
            }
        },
        400: {'description': 'Code invalide ou données incorrectes'},
        404: {'description': 'Utilisateur introuvable'},
    },
)
class ReinitialiserMotDePasseSMSView(APIView):
    """
    Réinitialise le mot de passe avec un code SMS.
    
    Processus :
    1. Vérifie le code SMS
    2. Trouve l'utilisateur par numéro de téléphone
    3. Change le mot de passe
    4. Enregistre dans l'historique
    5. Met à jour la date de dernière modification
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ReinitialiserMotDePasseSMSSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        telephone = serializer.validated_data['telephone']
        code = serializer.validated_data['code']
        nouveau_mdp = serializer.validated_data['nouveau_mot_de_passe']
        
        # Vérifier le code
        resultat = verifier_code_confirmation(telephone, code)
        
        if not resultat['valide']:
            return Response({
                'success': False,
                'message': resultat['message'],
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Trouver l'utilisateur
        utilisateur = UtilisateurIdentite.objects.filter(
            numero_telephone=telephone
        ).first()
        
        if not utilisateur:
            logger.error(f"Utilisateur introuvable pour le téléphone {telephone}")
            return Response({
                'success': False,
                'message': 'Utilisateur introuvable',
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Sauvegarder l'ancien hash
        ancien_hash = utilisateur.password
        
        # Changer le mot de passe
        utilisateur.set_password(nouveau_mdp)
        utilisateur.derniere_modification_mdp = timezone.now()
        utilisateur.save(update_fields=['password', 'derniere_modification_mdp'])
        
        # Synchroniser avec users.User si existe
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.filter(email=utilisateur.courriel).first()
            if user:
                user.set_password(nouveau_mdp)
                user.save(update_fields=['password'])
        except Exception as e:
            logger.warning(f"Erreur lors de la synchronisation avec users.User: {str(e)}")
        
        # Enregistrer dans l'historique
        adresse_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        enregistrer_changement_mot_de_passe(
            utilisateur=utilisateur,
            ancien_hash=ancien_hash,
            nouveau_hash=utilisateur.password,
            type_changement='REINITIALISATION',
            code_utilise=code,
            adresse_ip=adresse_ip,
            user_agent=user_agent,
            raison='Réinitialisation par code SMS'
        )
        
        # Compter le nombre total de changements
        nombre_changements = compter_changements_mdp(utilisateur_id=utilisateur.id)
        
        logger.info(
            f"Mot de passe réinitialisé avec succès pour {utilisateur.courriel} "
            f"(changement #{nombre_changements})"
        )
        
        return Response({
            'success': True,
            'message': 'Mot de passe réinitialisé avec succès',
            'nombre_changements_total': nombre_changements,
        }, status=status.HTTP_200_OK)


# =============================================================================
# HISTORIQUE MOT DE PASSE — Consulter l'historique des changements
# =============================================================================
@extend_schema(
    tags=['Authentication'],
    summary='Historique des changements de mot de passe',
    description=(
        'Consulte l\'historique des changements de mot de passe de l\'utilisateur connecté. '
        'Affiche les 10 derniers changements avec les détails.'
    ),
    responses={
        200: {
            'description': 'Historique récupéré avec succès',
            'content': {
                'application/json': {
                    'example': {
                        'nombre_total': 5,
                        'historique': [
                            {
                                'id': 'uuid',
                                'type_changement': 'REINITIALISATION',
                                'date_changement': '2024-01-15T10:30:00Z',
                                'adresse_ip': '192.168.1.1',
                                'code_utilise': '12345'
                            }
                        ]
                    }
                }
            }
        },
    },
)
class HistoriqueMotDePasseView(APIView):
    """
    Consulte l'historique des changements de mot de passe.
    
    Retourne les 10 derniers changements avec :
    - Type de changement
    - Date et heure
    - Adresse IP
    - Code SMS utilisé (si applicable)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Récupérer l'utilisateur identite
        utilisateur = UtilisateurIdentite.objects.filter(
            courriel=request.user.email
        ).first()
        
        if not utilisateur:
            return Response({
                'nombre_total': 0,
                'historique': []
            })
        
        # Récupérer l'historique
        historique = obtenir_historique_changements_mdp(
            utilisateur_id=utilisateur.id,
            limite=10
        )
        
        # Compter le total
        nombre_total = compter_changements_mdp(utilisateur_id=utilisateur.id)
        
        # Formater les données
        historique_data = []
        for h in historique:
            historique_data.append({
                'id': str(h.id),
                'type_changement': h.type_changement,
                'type_changement_display': h.get_type_changement_display(),
                'date_changement': h.date_changement.isoformat(),
                'adresse_ip': h.adresse_ip,
                'code_utilise': h.code_confirmation_utilise,
                'raison': h.raison,
            })
        
        return Response({
            'nombre_total': nombre_total,
            'historique': historique_data,
        }, status=status.HTTP_200_OK)
