"""
Serializers OAuth 2.0
"""
from rest_framework import serializers
from oauth2_provider.models import Application, AccessToken, RefreshToken


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer pour les applications OAuth 2.0"""
    
    class Meta:
        model = Application
        fields = [
            'id',
            'client_id',
            'client_secret',
            'name',
            'client_type',
            'authorization_grant_type',
            'redirect_uris',
            'skip_authorization',
            'created',
            'updated',
        ]
        read_only_fields = ['id', 'client_id', 'client_secret', 'created', 'updated']
        extra_kwargs = {
            'client_secret': {'write_only': True}
        }


class ApplicationCreateSerializer(serializers.Serializer):
    """Serializer pour créer une application OAuth 2.0"""
    
    name = serializers.CharField(max_length=255, required=True)
    client_type = serializers.ChoiceField(
        choices=['confidential', 'public'],
        default='confidential'
    )
    authorization_grant_type = serializers.ChoiceField(
        choices=[
            'authorization-code',
            'implicit',
            'password',
            'client-credentials',
            'openid-hybrid'
        ],
        default='authorization-code'
    )
    redirect_uris = serializers.CharField(required=False, allow_blank=True)
    skip_authorization = serializers.BooleanField(default=False)


class AccessTokenSerializer(serializers.ModelSerializer):
    """Serializer pour les access tokens"""
    
    application_name = serializers.CharField(source='application.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = AccessToken
        fields = [
            'id',
            'token',
            'application',
            'application_name',
            'user',
            'user_email',
            'expires',
            'scope',
            'created',
            'updated',
            'is_expired',
        ]
        read_only_fields = ['id', 'token', 'created', 'updated']
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expires < timezone.now()


class TokenIntrospectionSerializer(serializers.Serializer):
    """Serializer pour l'introspection de token"""
    
    active = serializers.BooleanField()
    scope = serializers.CharField(required=False)
    client_id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    exp = serializers.IntegerField(required=False)
    iat = serializers.IntegerField(required=False)


class TokenRevokeSerializer(serializers.Serializer):
    """Serializer pour révoquer un token"""
    
    token = serializers.CharField(required=True)
    token_type_hint = serializers.ChoiceField(
        choices=['access_token', 'refresh_token'],
        default='access_token'
    )


class OAuth2TokenResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse d'obtention de token"""
    
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')
    expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField(required=False)
    scope = serializers.CharField(required=False)
