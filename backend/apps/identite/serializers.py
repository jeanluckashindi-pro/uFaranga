"""
Sérialiseurs pour le schéma IDENTITE (identite.utilisateurs, identite.profils_utilisateurs).
"""
import re
from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import Utilisateur, ProfilUtilisateur

PHONE_REGEX = re.compile(r'^\+?[1-9]\d{8,14}$')


class ProfilUtilisateurIdentiteSerializer(serializers.ModelSerializer):
    """Profil identite (préférences, notifications, etc.)."""

    class Meta:
        model = ProfilUtilisateur
        fields = [
            'id', 'url_avatar', 'url_photo_couverture', 'biographie',
            'langue', 'devise_preferee', 'fuseau_horaire', 'format_date', 'format_heure',
            'notifications_courriel', 'notifications_sms', 'notifications_push',
            'notifications_transactions', 'notifications_marketing',
            'profil_public', 'afficher_telephone', 'afficher_courriel',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = fields


class ProfilUtilisateurUpdateSerializer(serializers.ModelSerializer):
    """Champs du profil identite modifiables par la personne."""

    class Meta:
        model = ProfilUtilisateur
        fields = [
            'url_avatar', 'url_photo_couverture', 'biographie',
            'langue', 'devise_preferee', 'fuseau_horaire', 'format_date', 'format_heure',
            'notifications_courriel', 'notifications_sms', 'notifications_push',
            'notifications_transactions', 'notifications_marketing',
            'profil_public', 'afficher_telephone', 'afficher_courriel',
            'metadonnees',
        ]


class UtilisateurIdentiteUpdateSerializer(serializers.ModelSerializer):
    """
    Mise à jour des informations complètes de la personne (identite.utilisateurs).
    Champs modifiables uniquement ; type_utilisateur, statut, KYC, etc. restent en lecture.
    """
    profil = ProfilUtilisateurUpdateSerializer(required=False)
    courriel = serializers.EmailField(required=False)
    numero_telephone = serializers.CharField(required=False, max_length=20)

    class Meta:
        model = Utilisateur
        fields = [
            'courriel', 'numero_telephone',
            'prenom', 'nom_famille', 'date_naissance', 'lieu_naissance', 'nationalite',
            'pays_residence', 'province', 'ville', 'commune', 'quartier', 'avenue',
            'numero_maison', 'adresse_complete', 'code_postal',
            'profil',
        ]

    def validate_courriel(self, value):
        if not value:
            return value
        value = value.lower().strip()
        instance = self.instance
        if Utilisateur.objects.filter(courriel=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Cette adresse e-mail est déjà utilisée.')
        return value

    def validate_numero_telephone(self, value):
        if not value:
            return value
        value = re.sub(r'[\s\-]', '', value.strip())
        if not PHONE_REGEX.match(value):
            raise serializers.ValidationError('Numéro de téléphone invalide (format international, ex. +257...).')
        instance = self.instance
        if Utilisateur.objects.filter(numero_telephone=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError('Ce numéro de téléphone est déjà utilisé.')
        return value

    def update(self, instance, validated_data):
        profil_data = validated_data.pop('profil', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profil_data:
            profil, _ = ProfilUtilisateur.objects.get_or_create(utilisateur=instance)
            for attr, value in profil_data.items():
                setattr(profil, attr, value)
            profil.save()
        return instance


class UtilisateurIdentiteSerializer(serializers.ModelSerializer):
    """
    Toutes les infos de la personne depuis identite.utilisateurs
    (y compris type_utilisateur) + profil identite.
    On n'expose pas password ni secret_2fa.
    """
    profil = ProfilUtilisateurIdentiteSerializer(read_only=True)
    nom_complet = serializers.CharField(read_only=True)
    # Modèle : last_login (db_column='derniere_connexion') → exposé en API sous derniere_connexion
    derniere_connexion = serializers.DateTimeField(source='last_login', read_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'courriel',
            'numero_telephone',
            'prenom',
            'nom_famille',
            'nom_complet',
            'date_naissance',
            'lieu_naissance',
            'nationalite',
            'pays_residence',
            'province',
            'ville',
            'commune',
            'quartier',
            'avenue',
            'numero_maison',
            'adresse_complete',
            'code_postal',
            'telephone_verifie',
            'telephone_verifie_le',
            'courriel_verifie',
            'courriel_verifie_le',
            'niveau_kyc',
            'date_validation_kyc',
            'validateur_kyc_id',
            'type_utilisateur',
            'statut',
            'raison_statut',
            'nombre_tentatives_connexion',
            'bloque_jusqua',
            'double_auth_activee',
            'est_actif',
            'date_creation',
            'date_modification',
            'derniere_connexion',
            'derniere_modification_mdp',
            'is_staff',
            'is_superuser',
            'profil',
            'metadonnees',
        ]
        read_only_fields = fields
