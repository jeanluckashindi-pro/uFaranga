"""
Vues OAuth 2.0 personnalisées
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.views import TokenView
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_oauth_client(request):
    """
    Enregistrer une nouvelle application OAuth 2.0
    
    POST /api/oauth2/register/
    {
        "name": "Mon Application",
        "client_type": "confidential",  # ou "public"
        "authorization_grant_type": "authorization-code",  # ou "password", "client-credentials"
        "redirect_uris": "https://mon-app.com/callback"
    }
    """
    try:
        name = request.data.get('name')
        client_type = request.data.get('client_type', 'confidential')
        authorization_grant_type = request.data.get('authorization_grant_type', 'authorization-code')
        redirect_uris = request.data.get('redirect_uris', '')
        
        if not name:
            return Response(
                {'error': 'Le nom de l\'application est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer l'application OAuth 2.0
        application = Application.objects.create(
            name=name,
            user=request.user if request.user.is_authenticated else None,
            client_type=client_type,
            authorization_grant_type=authorization_grant_type,
            redirect_uris=redirect_uris,
            skip_authorization=False,  # Demander l'autorisation à l'utilisateur
        )
        
        logger.info(f"Application OAuth 2.0 créée: {application.name} (ID: {application.client_id})")
        
        return Response({
            'client_id': application.client_id,
            'client_secret': application.client_secret,
            'name': application.name,
            'client_type': application.client_type,
            'authorization_grant_type': application.authorization_grant_type,
            'redirect_uris': application.redirect_uris,
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'application OAuth 2.0: {str(e)}")
        return Response(
            {'error': 'Erreur lors de la création de l\'application'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    """
    Révoquer un access token ou refresh token
    
    POST /api/oauth2/revoke/
    {
        "token": "votre_token",
        "token_type_hint": "access_token"  # ou "refresh_token"
    }
    """
    try:
        token = request.data.get('token')
        token_type_hint = request.data.get('token_type_hint', 'access_token')
        
        if not token:
            return Response(
                {'error': 'Le token est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Révoquer le token
        if token_type_hint == 'access_token':
            try:
                access_token = AccessToken.objects.get(token=token)
                access_token.delete()
                logger.info(f"Access token révoqué: {token[:10]}...")
            except AccessToken.DoesNotExist:
                pass
        
        elif token_type_hint == 'refresh_token':
            try:
                refresh_token = RefreshToken.objects.get(token=token)
                # Révoquer aussi l'access token associé
                if refresh_token.access_token:
                    refresh_token.access_token.delete()
                refresh_token.delete()
                logger.info(f"Refresh token révoqué: {token[:10]}...")
            except RefreshToken.DoesNotExist:
                pass
        
        return Response(
            {'message': 'Token révoqué avec succès'},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la révocation du token: {str(e)}")
        return Response(
            {'error': 'Erreur lors de la révocation du token'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def introspect_token(request):
    """
    Vérifier la validité d'un token
    
    GET /api/oauth2/introspect/
    Authorization: Bearer <token>
    """
    try:
        # Le token est déjà validé par OAuth2Authentication
        user = request.user
        token = request.auth
        
        if not token:
            return Response({
                'active': False
            }, status=status.HTTP_200_OK)
        
        # Vérifier si le token est expiré
        is_active = token.expires > timezone.now()
        
        response_data = {
            'active': is_active,
        }
        
        if is_active:
            response_data.update({
                'scope': token.scope,
                'client_id': token.application.client_id,
                'username': user.username if user else None,
                'user_id': str(user.id) if user else None,
                'exp': int(token.expires.timestamp()),
                'iat': int(token.created.timestamp()),
            })
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'introspection du token: {str(e)}")
        return Response({
            'active': False
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_my_tokens(request):
    """
    Lister tous les tokens actifs de l'utilisateur connecté
    
    GET /api/oauth2/tokens/
    """
    try:
        user = request.user
        
        # Récupérer tous les access tokens actifs
        access_tokens = AccessToken.objects.filter(
            user=user,
            expires__gt=timezone.now()
        ).select_related('application')
        
        tokens_data = []
        for token in access_tokens:
            tokens_data.append({
                'token': token.token[:10] + '...',  # Masquer le token complet
                'application': token.application.name,
                'scope': token.scope,
                'expires': token.expires,
                'created': token.created,
            })
        
        return Response({
            'count': len(tokens_data),
            'tokens': tokens_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des tokens: {str(e)}")
        return Response(
            {'error': 'Erreur lors de la récupération des tokens'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
