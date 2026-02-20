import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings as jwt_api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator
from apps.users.models import UserProfile
from apps.identite.models import Utilisateur as UtilisateurIdentite
from apps.notification.models import Notification
from .services_sessions import get_sessions_actives_info
from .auth_security import (
    verifier_compte_non_bloque,
    verifier_2fa_si_requise,
    appliquer_echec_connexion,
    appliquer_succes_connexion,
)

User = get_user_model()

# Format téléphone : 9 à 15 chiffres, optionnellement préfixé par +
PHONE_REGEX = re.compile(r'^\+?\d{9,15}$')

email_validator = EmailValidator(message='Saisissez une adresse e-mail valide.')


def is_valid_email(value):
    """Vérifie si la valeur est une adresse e-mail valide."""
    if not value or not value.strip():
        return False
    try:
        email_validator(value.strip())
        return True
    except DjangoValidationError:
        return False


def is_valid_phone(value):
    """Vérifie si la valeur est un numéro de téléphone valide (9-15 chiffres, + optionnel)."""
    if not value or not value.strip():
        return False
    # Supprimer espaces et tirets pour la vérification
    cleaned = re.sub(r'[\s\-]', '', value.strip())
    return bool(PHONE_REGEX.match(cleaned))


def validate_email_or_phone(value):
    """
    Vérifie que la valeur est soit une adresse e-mail valide, soit un numéro de téléphone valide.
    Sinon lève serializers.ValidationError.
    """
    if not value or not value.strip():
        raise serializers.ValidationError(
            'Saisissez votre adresse e-mail ou votre numéro de téléphone.'
        )
    value = value.strip()
    if is_valid_email(value):
        return value
    if is_valid_phone(value):
        # Normaliser le numéro (garder tel quel pour la recherche en base)
        return re.sub(r'[\s\-]', '', value)
    raise serializers.ValidationError(
        'Saisissez une adresse e-mail valide ou un numéro de téléphone valide (9 à 15 chiffres).'
    )


def get_utilisateur_identite_by_email_or_phone(value):
    """Retourne l'utilisateur identite.Utilisateur (identite.utilisateurs) par courriel ou téléphone."""
    if not value or not value.strip():
        return None
    value = value.strip()
    if '@' in value:
        return UtilisateurIdentite.objects.filter(courriel__iexact=value).first()
    phone_clean = re.sub(r'[\s\-]', '', value)
    user = UtilisateurIdentite.objects.filter(numero_telephone=phone_clean).first()
    if not user and not phone_clean.startswith('+'):
        user = UtilisateurIdentite.objects.filter(numero_telephone='+' + phone_clean).first()
    return user


def sync_identite_to_user(utilisateur_identite, password):
    """
    Crée ou met à jour un users.User à partir de identite.Utilisateur
    pour que le JWT soit émis sur le même modèle que le reste de l'app.
    """
    email = utilisateur_identite.courriel
    
    # Extraire le niveau KYC (integer) depuis la relation ForeignKey
    niveau_kyc_value = 0
    if hasattr(utilisateur_identite, 'niveau_kyc') and utilisateur_identite.niveau_kyc:
        # Si c'est un objet NiveauKYC, extraire l'attribut 'niveau'
        if hasattr(utilisateur_identite.niveau_kyc, 'niveau'):
            niveau_kyc_value = utilisateur_identite.niveau_kyc.niveau
        else:
            # Sinon c'est déjà un integer
            niveau_kyc_value = utilisateur_identite.niveau_kyc
    
    user, created = User.objects.update_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0] if '@' in email else email,
            'first_name': utilisateur_identite.prenom or '',
            'last_name': utilisateur_identite.nom_famille or '',
            'phone_number': utilisateur_identite.numero_telephone or None,
            'is_staff': utilisateur_identite.is_staff,
            'is_superuser': getattr(utilisateur_identite, 'is_superuser', False),
            'is_active': utilisateur_identite.est_actif,
            'kyc_level': niveau_kyc_value,
            'is_phone_verified': getattr(utilisateur_identite, 'telephone_verifie', False),
            'is_email_verified': getattr(utilisateur_identite, 'courriel_verifie', False),
        },
    )
    user.set_password(password)
    user.save(update_fields=['password'])
    UserProfile.objects.get_or_create(user=user)
    return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Sérialiseur JWT personnalisé.
    Accepte l'adresse e-mail OU le numéro de téléphone pour se connecter.
    Accepte "email" ou "username" dans le body (pour compatibilité frontend).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Libellé pour le champ : adresse e-mail ou numéro de téléphone
        self.fields[self.username_field].label = 'Adresse e-mail ou numéro de téléphone'
        self.fields[self.username_field].help_text = 'Saisissez votre e-mail ou votre numéro de téléphone'
        # Accepter aussi "username" pour compatibilité frontend (optionnel)
        self.fields[self.username_field].required = False
        self.fields['username'] = serializers.CharField(write_only=True, required=False, label='Identifiant (email ou username)')
        self.fields['remember_me'] = serializers.BooleanField(required=False, default=False, label='Se souvenir de moi')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims personnalisés dans le JWT
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['kyc_level'] = user.kyc_level
        token['is_staff'] = user.is_staff
        return token

    def validate(self, attrs):
        """
        Connexion : toute la couche sécurité est vérifiée avant d'émettre un token.
        Ordre : identifiants → compte actif → compte non bloqué → mot de passe
        → mise à jour tentatives/succès → 2FA si requise → émission token → réponse.
        """
        # Accepter "username" ou "email" (le front peut envoyer l'un ou l'autre)
        credential = attrs.get(self.username_field) or attrs.get('username') or ''
        if not credential:
            raise serializers.ValidationError({
                self.username_field: 'Saisissez votre adresse e-mail, numéro de téléphone ou identifiant.'
            })
        # Vérifier que la valeur est une adresse e-mail ou un numéro de téléphone valide
        credential = validate_email_or_phone(credential)
        # Authentification contre identite.utilisateurs (source de vérité)
        utilisateur_identite = get_utilisateur_identite_by_email_or_phone(credential)
        if not utilisateur_identite:
            raise AuthenticationFailed(
                detail='Aucun compte actif avec ces identifiants.',
                code='no_active_account',
            )
        if not utilisateur_identite.est_actif:
            raise AuthenticationFailed(
                detail='Ce compte est désactivé.',
                code='no_active_account',
            )
        # --- Couche sécurité : vérifications avant toute émission de token ---
        verifier_compte_non_bloque(utilisateur_identite)
        if not utilisateur_identite.check_password(attrs['password']):
            appliquer_echec_connexion(utilisateur_identite)
            raise AuthenticationFailed(
                detail='Aucun compte actif avec ces identifiants.',
                code='no_active_account',
            )
        appliquer_succes_connexion(utilisateur_identite)
        verifier_2fa_si_requise(utilisateur_identite, attrs.get('code_2fa'))
        # --- Fin couche sécurité : on peut émettre le token ---
        # Synchroniser vers users.User pour émettre le JWT (reste de l'app utilise users)
        user = sync_identite_to_user(utilisateur_identite, attrs['password'])
        attrs[self.username_field] = user.email
        self.user = user
        # Création du token (durée dynamique selon remember_me)
        refresh = self.get_token(self.user)
        if attrs.get('remember_me'):
            from config.constants import REFRESH_TOKEN_LIFETIME_REMEMBER_ME
            refresh.set_exp(lifetime=REFRESH_TOKEN_LIFETIME_REMEMBER_ME)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        if jwt_api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        # Sessions actives (après génération du token : on sait si le compte est utilisé à plusieurs endroits)
        sessions_info = get_sessions_actives_info(self.user)
        data['sessions_actives'] = sessions_info
        # Si plus de 2 sessions actives : enregistrer une notification pour la personne (notification.notifications)
        if sessions_info['nombre_sessions_actives'] > 2:
            Notification.objects.create(
                utilisateur_id=utilisateur_identite.id,
                type_notification='IN_APP',
                canal='in_app',
                destinataire=self.user.email or utilisateur_identite.numero_telephone or str(utilisateur_identite.id),
                sujet='Connexion multiple détectée',
                message=(
                    f"Votre compte est actuellement utilisé sur {sessions_info['nombre_sessions_actives']} "
                    "session(s). Si ce n'est pas vous, changez votre mot de passe."
                ),
                priorite='NORMALE',
                statut_envoi='EN_ATTENTE',
                metadonnees={'nombre_sessions_actives': sessions_info['nombre_sessions_actives'], 'connexion': 'connexion'},
            )
        data['remember_me'] = bool(attrs.get('remember_me', False))
        # Ajouter les infos utilisateur dans la réponse
        data['user'] = {
            'id': str(self.user.id),
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone_number': self.user.phone_number,
            'kyc_level': self.user.kyc_level,
            'is_phone_verified': self.user.is_phone_verified,
            'is_email_verified': self.user.is_email_verified,
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'inscription d'un nouvel utilisateur.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number',
            'country', 'city',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Les mots de passe ne correspondent pas.'
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('Un utilisateur avec cet email existe déjà.')
        return value.lower()

    def validate_phone_number(self, value):
        if value and User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Ce numéro de téléphone est déjà utilisé.')
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Créer le profil automatiquement
        UserProfile.objects.create(user=user)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Changement de mot de passe avec vérification stricte :
    - Mot de passe actuel requis et vérifié (identite puis users).
    - Nouveau mot de passe avec confirmation et règles de complexité.
    """
    mot_de_passe_actuel = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label='Mot de passe actuel',
    )
    nouveau_mot_de_passe = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        label='Nouveau mot de passe',
    )
    nouveau_mot_de_passe_confirmation = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label='Confirmer le nouveau mot de passe',
    )

    def validate(self, attrs):
        if attrs['nouveau_mot_de_passe'] != attrs['nouveau_mot_de_passe_confirmation']:
            raise serializers.ValidationError({
                'nouveau_mot_de_passe_confirmation': 'Les deux mots de passe ne correspondent pas.'
            })
        return attrs

    def validate_mot_de_passe_actuel(self, value):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError('Utilisateur non authentifié.')
        # Vérifier d'abord sur identite (source de vérité) si la personne y existe
        utilisateur_identite = UtilisateurIdentite.objects.filter(
            courriel=request.user.email
        ).first()
        if utilisateur_identite:
            if not utilisateur_identite.check_password(value):
                raise serializers.ValidationError('Mot de passe actuel incorrect.')
            return value
        # Sinon vérifier sur users.User
        if not request.user.check_password(value):
            raise serializers.ValidationError('Mot de passe actuel incorrect.')
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Demande de réinitialisation de mot de passe."""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Confirmation de réinitialisation de mot de passe."""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Les mots de passe ne correspondent pas.'
            })
        return attrs


class EnvoyerCodeConfirmationSerializer(serializers.Serializer):
    """Envoi d'un code de confirmation par SMS."""
    telephone = serializers.CharField(
        required=True,
        max_length=15,
        help_text='Numéro de téléphone (ex: 62046725 ou +25762046725)'
    )
    prenom = serializers.CharField(
        required=False,
        max_length=100,
        help_text='Prénom de l\'utilisateur (optionnel)'
    )

    def validate_telephone(self, value):
        """Valide et normalise le numéro de téléphone."""
        if not value or not value.strip():
            raise serializers.ValidationError('Le numéro de téléphone est requis.')
        
        # Nettoyer le numéro (supprimer espaces et tirets)
        cleaned = re.sub(r'[\s\-]', '', value.strip())
        
        # Vérifier le format
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError(
                'Format de numéro invalide. Utilisez 8 à 15 chiffres, avec ou sans le préfixe +'
            )
        
        return cleaned


class VerifierCodeConfirmationSerializer(serializers.Serializer):
    """Vérification d'un code de confirmation."""
    telephone = serializers.CharField(
        required=True,
        max_length=15,
        help_text='Numéro de téléphone'
    )
    code = serializers.CharField(
        required=True,
        min_length=5,
        max_length=5,
        help_text='Code à 5 chiffres'
    )

    def validate_telephone(self, value):
        """Valide et normalise le numéro de téléphone."""
        if not value or not value.strip():
            raise serializers.ValidationError('Le numéro de téléphone est requis.')
        
        cleaned = re.sub(r'[\s\-]', '', value.strip())
        
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError('Format de numéro invalide.')
        
        return cleaned

    def validate_code(self, value):
        """Valide le format du code."""
        if not value or not value.strip():
            raise serializers.ValidationError('Le code est requis.')
        
        cleaned = value.strip()
        
        if not re.match(r'^\d{5}$', cleaned):
            raise serializers.ValidationError('Le code doit contenir exactement 5 chiffres.')
        
        return cleaned


class ReinitialiserMotDePasseSMSSerializer(serializers.Serializer):
    """Réinitialisation de mot de passe avec code SMS."""
    telephone = serializers.CharField(
        required=True,
        max_length=15,
        help_text='Numéro de téléphone'
    )
    code = serializers.CharField(
        required=True,
        min_length=5,
        max_length=5,
        help_text='Code de confirmation à 5 chiffres'
    )
    nouveau_mot_de_passe = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text='Nouveau mot de passe'
    )
    nouveau_mot_de_passe_confirmation = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text='Confirmation du nouveau mot de passe'
    )

    def validate_telephone(self, value):
        """Valide et normalise le numéro de téléphone."""
        if not value or not value.strip():
            raise serializers.ValidationError('Le numéro de téléphone est requis.')
        
        cleaned = re.sub(r'[\s\-]', '', value.strip())
        
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError('Format de numéro invalide.')
        
        return cleaned

    def validate_code(self, value):
        """Valide le format du code."""
        if not value or not value.strip():
            raise serializers.ValidationError('Le code est requis.')
        
        cleaned = value.strip()
        
        if not re.match(r'^\d{5}$', cleaned):
            raise serializers.ValidationError('Le code doit contenir exactement 5 chiffres.')
        
        return cleaned

    def validate(self, attrs):
        """Valide que les deux mots de passe correspondent."""
        if attrs['nouveau_mot_de_passe'] != attrs['nouveau_mot_de_passe_confirmation']:
            raise serializers.ValidationError({
                'nouveau_mot_de_passe_confirmation': 'Les deux mots de passe ne correspondent pas.'
            })
        return attrs
