from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, UserSession

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le profil utilisateur."""

    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'language', 'currency', 'timezone',
            'email_notifications', 'sms_notifications', 'push_notifications',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur principal pour l'utilisateur."""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth',
            'country', 'city', 'address',
            'is_phone_verified', 'is_email_verified', 'kyc_level',
            'profile', 'created_at', 'updated_at', 'last_login',
        ]
        read_only_fields = [
            'id', 'email', 'is_phone_verified', 'is_email_verified',
            'kyc_level', 'created_at', 'updated_at', 'last_login',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour du profil utilisateur."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'date_of_birth', 'country', 'city', 'address',
        ]

    def validate_phone_number(self, value):
        user = self.instance
        if value and User.objects.filter(phone_number=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('Ce numéro de téléphone est déjà utilisé.')
        return value


class UserListSerializer(serializers.ModelSerializer):
    """Sérialiseur léger pour les listes d'utilisateurs."""
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'kyc_level', 'is_active', 'created_at',
        ]
        read_only_fields = fields


class UserSessionSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les sessions utilisateur."""

    class Meta:
        model = UserSession
        fields = [
            'id', 'session_key', 'ip_address', 'user_agent',
            'device_info', 'created_at', 'last_activity', 'is_active',
        ]
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour du profil étendu."""

    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'language', 'currency', 'timezone',
            'email_notifications', 'sms_notifications', 'push_notifications',
        ]
