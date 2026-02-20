"""
Sérialiseurs pour le schéma IDENTITE (identite.utilisateurs, identite.profils_utilisateurs).
"""
import re
from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import (
    Utilisateur, ProfilUtilisateur, 
    TypeUtilisateur, NiveauKYC, StatutUtilisateur,
    NumeroTelephone, HistoriqueNumeroTelephone
)

PHONE_REGEX = re.compile(r'^\+?[1-9]\d{8,14}$')


# =============================================================================
# SERIALIZERS POUR LES TABLES DE RÉFÉRENCE
# =============================================================================

class TypeUtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les types d'utilisateurs"""
    
    class Meta:
        model = TypeUtilisateur
        fields = [
            'code', 'libelle', 'description', 
            'ordre_affichage', 'est_actif'
        ]


class NiveauKYCSerializer(serializers.ModelSerializer):
    """Serializer pour les niveaux KYC"""
    
    class Meta:
        model = NiveauKYC
        fields = [
            'niveau', 'libelle', 'description',
            'limite_transaction_journaliere', 'limite_solde_maximum',
            'documents_requis', 'est_actif'
        ]


class StatutUtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les statuts utilisateurs"""
    
    class Meta:
        model = StatutUtilisateur
        fields = [
            'code', 'libelle', 'description', 'couleur',
            'permet_connexion', 'permet_transactions',
            'ordre_affichage', 'est_actif'
        ]


# =============================================================================
# SERIALIZERS POUR LES NUMÉROS DE TÉLÉPHONE
# =============================================================================

class NumeroTelephoneSerializer(serializers.ModelSerializer):
    """Serializer pour les numéros de téléphone"""
    pays_nom = serializers.SerializerMethodField()
    
    class Meta:
        model = NumeroTelephone
        fields = [
            'id', 'pays_code_iso_2', 'pays_nom', 'code_pays',
            'numero_national', 'numero_complet', 'numero_formate',
            'type_numero', 'usage', 'est_principal', 'est_verifie',
            'date_verification', 'methode_verification',
            'statut', 'raison_statut', 'operateur', 'type_ligne',
            'nombre_connexions_reussies', 'derniere_connexion',
            'date_creation', 'date_modification'
        ]
        read_only_fields = [
            'id', 'numero_formate', 'date_creation', 
            'date_modification', 'nombre_connexions_reussies'
        ]
    
    def get_pays_nom(self, obj):
        """Récupère le nom du pays depuis les métadonnées"""
        from apps.localisation.models import Pays
        try:
            pays = Pays.objects.get(code_iso_2=obj.pays_code_iso_2)
            return pays.nom
        except Pays.DoesNotExist:
            return obj.pays_code_iso_2


class HistoriqueNumeroTelephoneSerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des numéros"""
    
    class Meta:
        model = HistoriqueNumeroTelephone
        fields = [
            'id', 'action', 'ancien_statut', 'nouveau_statut',
            'raison', 'details', 'date_action', 'adresse_ip'
        ]
        read_only_fields = fields


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


class CreerUtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer un nouvel utilisateur CLIENT standard
    Utilise des IDs pour les relations
    """
    mot_de_passe = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Mot de passe (min 8 caractères)'
    )
    mot_de_passe_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text='Confirmation du mot de passe'
    )
    
    # Relations par ID
    type_utilisateur_id = serializers.CharField(
        write_only=True,
        required=False,
        help_text='ID du type utilisateur (par défaut: CLIENT)'
    )
    niveau_kyc_id = serializers.IntegerField(
        write_only=True,
        required=False,
        default=0,
        help_text='ID du niveau KYC (par défaut: 0)'
    )
    statut_id = serializers.CharField(
        write_only=True,
        required=False,
        help_text='ID du statut (par défaut: ACTIF)'
    )
    
    # Localisation par ID
    pays_id = serializers.UUIDField(
        write_only=True,
        required=False,
        help_text='UUID du pays'
    )
    province_id = serializers.UUIDField(
        write_only=True,
        required=False,
        help_text='UUID de la province'
    )
    district_id = serializers.UUIDField(
        write_only=True,
        required=False,
        help_text='UUID du district'
    )
    quartier_id = serializers.UUIDField(
        write_only=True,
        required=False,
        help_text='UUID du quartier'
    )

    class Meta:
        model = Utilisateur
        fields = [
            # Authentification
            'courriel',
            'numero_telephone',
            'mot_de_passe',
            'mot_de_passe_confirmation',
            
            # Informations personnelles
            'prenom',
            'nom_famille',
            'date_naissance',
            'lieu_naissance',
            'nationalite',
            
            # Adresse
            'pays_residence',
            'province',
            'ville',
            'commune',
            'quartier',
            'avenue',
            'numero_maison',
            'code_postal',
            
            # Relations (IDs)
            'type_utilisateur_id',
            'niveau_kyc_id',
            'statut_id',
            'pays_id',
            'province_id',
            'district_id',
            'quartier_id',
            
            # Métadonnées
            'metadonnees',
        ]
        extra_kwargs = {
            'courriel': {'required': True},
            'numero_telephone': {'required': True},
            'prenom': {'required': True},
            'nom_famille': {'required': True},
            'date_naissance': {'required': True},
        }
    
    def validate(self, attrs):
        """Validation globale"""
        # Vérifier que les mots de passe correspondent
        if attrs.get('mot_de_passe') != attrs.get('mot_de_passe_confirmation'):
            raise serializers.ValidationError({
                'mot_de_passe_confirmation': 'Les mots de passe ne correspondent pas.'
            })
        
        # Vérifier que l'email n'existe pas déjà
        courriel = attrs.get('courriel', '').lower().strip()
        if Utilisateur.objects.filter(courriel=courriel).exists():
            raise serializers.ValidationError({
                'courriel': 'Cette adresse e-mail est déjà utilisée.'
            })
        
        # Vérifier que le téléphone n'existe pas déjà
        numero_telephone = attrs.get('numero_telephone', '').strip()
        if Utilisateur.objects.filter(numero_telephone=numero_telephone).exists():
            raise serializers.ValidationError({
                'numero_telephone': 'Ce numéro de téléphone est déjà utilisé.'
            })
        
        return attrs
    
    def validate_mot_de_passe(self, value):
        """Valider le mot de passe"""
        if len(value) < 8:
            raise serializers.ValidationError(
                'Le mot de passe doit contenir au moins 8 caractères.'
            )
        return value
    
    def validate_courriel(self, value):
        """Normaliser l'email"""
        return value.lower().strip()
    
    def validate_numero_telephone(self, value):
        """Valider le format du téléphone"""
        import re
        value = value.strip()
        if not re.match(r'^\+?[1-9]\d{8,14}$', value):
            raise serializers.ValidationError(
                'Format de numéro invalide. Utilisez le format international (ex: +25762046725)'
            )
        return value
    
    def create(self, validated_data):
        """Créer l'utilisateur CLIENT standard"""
        # Extraire les champs spéciaux
        mot_de_passe = validated_data.pop('mot_de_passe')
        validated_data.pop('mot_de_passe_confirmation')
        
        type_utilisateur_id = validated_data.pop('type_utilisateur_id', None)
        niveau_kyc_id = validated_data.pop('niveau_kyc_id', 0)
        statut_id = validated_data.pop('statut_id', None)
        
        pays_id = validated_data.pop('pays_id', None)
        province_id = validated_data.pop('province_id', None)
        district_id = validated_data.pop('district_id', None)
        quartier_id = validated_data.pop('quartier_id', None)
        
        # Récupérer les objets de référence
        # Type: toujours CLIENT pour inscription publique
        type_utilisateur = TypeUtilisateur.objects.get(code='CLIENT')
        
        # Niveau KYC
        try:
            niveau_kyc = NiveauKYC.objects.get(niveau=niveau_kyc_id)
        except NiveauKYC.DoesNotExist:
            niveau_kyc = NiveauKYC.objects.get(niveau=0)
        
        # Statut: toujours ACTIF par défaut
        statut = StatutUtilisateur.objects.get(code='ACTIF')
        
        # Récupérer les objets de localisation
        from apps.localisation.models import Pays, Province, District, Quartier
        
        pays = None
        if pays_id:
            try:
                pays = Pays.objects.get(id=pays_id)
            except Pays.DoesNotExist:
                pass
        
        province_geo = None
        if province_id:
            try:
                province_geo = Province.objects.get(id=province_id)
            except Province.DoesNotExist:
                pass
        
        district = None
        if district_id:
            try:
                district = District.objects.get(id=district_id)
            except District.DoesNotExist:
                pass
        
        quartier_geo = None
        if quartier_id:
            try:
                quartier_geo = Quartier.objects.get(id=quartier_id)
            except Quartier.DoesNotExist:
                pass
        
        # Créer l'utilisateur
        utilisateur = Utilisateur(
            **validated_data,
            type_utilisateur=type_utilisateur,
            niveau_kyc=niveau_kyc,
            statut=statut,
            pays=pays,
            province_geo=province_geo,
            district=district,
            quartier_geo=quartier_geo,
            telephone_verifie=False,
            courriel_verifie=False,
        )
        
        # Définir le mot de passe (hashé)
        utilisateur.set_password(mot_de_passe)
        utilisateur.save()
        
        # Créer le profil automatiquement
        from apps.identite.models import ProfilUtilisateur
        ProfilUtilisateur.objects.create(utilisateur=utilisateur)
        
        return utilisateur


class CreerAdminSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer un ADMIN/AGENT/MARCHAND
    Réservé aux administrateurs authentifiés
    """
    mot_de_passe = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    mot_de_passe_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    # Relations par ID
    type_utilisateur_id = serializers.CharField(
        required=True,
        help_text='Code du type: AGENT, MARCHAND, ADMIN, SUPER_ADMIN'
    )
    niveau_kyc_id = serializers.IntegerField(
        required=True,
        help_text='Niveau KYC: 0, 1, 2, 3'
    )
    statut_id = serializers.CharField(
        required=True,
        help_text='Code du statut'
    )
    
    # Localisation par ID
    pays_id = serializers.UUIDField(required=False)
    province_id = serializers.UUIDField(required=False)
    district_id = serializers.UUIDField(required=False)
    quartier_id = serializers.UUIDField(required=False)
    
    # Vérifications
    telephone_verifie = serializers.BooleanField(default=False)
    courriel_verifie = serializers.BooleanField(default=False)

    class Meta:
        model = Utilisateur
        fields = [
            'courriel',
            'numero_telephone',
            'mot_de_passe',
            'mot_de_passe_confirmation',
            'prenom',
            'nom_famille',
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
            'code_postal',
            'type_utilisateur_id',
            'niveau_kyc_id',
            'statut_id',
            'pays_id',
            'province_id',
            'district_id',
            'quartier_id',
            'telephone_verifie',
            'courriel_verifie',
            'metadonnees',
        ]
        extra_kwargs = {
            'courriel': {'required': True},
            'numero_telephone': {'required': True},
            'prenom': {'required': True},
            'nom_famille': {'required': True},
            'date_naissance': {'required': True},
        }
    
    def validate(self, attrs):
        """Validation globale"""
        if attrs.get('mot_de_passe') != attrs.get('mot_de_passe_confirmation'):
            raise serializers.ValidationError({
                'mot_de_passe_confirmation': 'Les mots de passe ne correspondent pas.'
            })
        
        courriel = attrs.get('courriel', '').lower().strip()
        if Utilisateur.objects.filter(courriel=courriel).exists():
            raise serializers.ValidationError({
                'courriel': 'Cette adresse e-mail est déjà utilisée.'
            })
        
        numero_telephone = attrs.get('numero_telephone', '').strip()
        if Utilisateur.objects.filter(numero_telephone=numero_telephone).exists():
            raise serializers.ValidationError({
                'numero_telephone': 'Ce numéro de téléphone est déjà utilisé.'
            })
        
        # Vérifier que le type n'est pas CLIENT
        type_code = attrs.get('type_utilisateur_id')
        if type_code == 'CLIENT':
            raise serializers.ValidationError({
                'type_utilisateur_id': 'Utilisez l\'endpoint d\'inscription pour créer un CLIENT.'
            })
        
        return attrs
    
    def validate_mot_de_passe(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'Le mot de passe doit contenir au moins 8 caractères.'
            )
        return value
    
    def validate_courriel(self, value):
        return value.lower().strip()
    
    def validate_numero_telephone(self, value):
        import re
        value = value.strip()
        if not re.match(r'^\+?[1-9]\d{8,14}$', value):
            raise serializers.ValidationError(
                'Format de numéro invalide.'
            )
        return value
    
    def create(self, validated_data):
        """Créer l'utilisateur ADMIN/AGENT/MARCHAND"""
        mot_de_passe = validated_data.pop('mot_de_passe')
        validated_data.pop('mot_de_passe_confirmation')
        
        type_utilisateur_id = validated_data.pop('type_utilisateur_id')
        niveau_kyc_id = validated_data.pop('niveau_kyc_id')
        statut_id = validated_data.pop('statut_id')
        
        pays_id = validated_data.pop('pays_id', None)
        province_id = validated_data.pop('province_id', None)
        district_id = validated_data.pop('district_id', None)
        quartier_id = validated_data.pop('quartier_id', None)
        
        # Récupérer les objets
        try:
            type_utilisateur = TypeUtilisateur.objects.get(code=type_utilisateur_id)
        except TypeUtilisateur.DoesNotExist:
            raise serializers.ValidationError({
                'type_utilisateur_id': f'Type "{type_utilisateur_id}" introuvable.'
            })
        
        try:
            niveau_kyc = NiveauKYC.objects.get(niveau=niveau_kyc_id)
        except NiveauKYC.DoesNotExist:
            raise serializers.ValidationError({
                'niveau_kyc_id': f'Niveau KYC "{niveau_kyc_id}" introuvable.'
            })
        
        try:
            statut = StatutUtilisateur.objects.get(code=statut_id)
        except StatutUtilisateur.DoesNotExist:
            raise serializers.ValidationError({
                'statut_id': f'Statut "{statut_id}" introuvable.'
            })
        
        # Localisation
        from apps.localisation.models import Pays, Province, District, Quartier
        
        pays = Pays.objects.filter(id=pays_id).first() if pays_id else None
        province_geo = Province.objects.filter(id=province_id).first() if province_id else None
        district = District.objects.filter(id=district_id).first() if district_id else None
        quartier_geo = Quartier.objects.filter(id=quartier_id).first() if quartier_id else None
        
        # Créer l'utilisateur
        utilisateur = Utilisateur(
            **validated_data,
            type_utilisateur=type_utilisateur,
            niveau_kyc=niveau_kyc,
            statut=statut,
            pays=pays,
            province_geo=province_geo,
            district=district,
            quartier_geo=quartier_geo,
        )
        
        utilisateur.set_password(mot_de_passe)
        utilisateur.save()
        
        # Créer le profil
        from apps.identite.models import ProfilUtilisateur
        ProfilUtilisateur.objects.create(utilisateur=utilisateur)
        
        return utilisateur


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
    
    AVEC EXPANDS: type_utilisateur_details, niveau_kyc_details, statut_details, numeros_telephone
    """
    profil = ProfilUtilisateurIdentiteSerializer(read_only=True)
    nom_complet = serializers.CharField(read_only=True)
    derniere_connexion = serializers.DateTimeField(source='last_login', read_only=True)
    
    # Expands - Détails complets des relations
    type_utilisateur_details = TypeUtilisateurSerializer(source='type_utilisateur', read_only=True)
    niveau_kyc_details = NiveauKYCSerializer(source='niveau_kyc', read_only=True)
    statut_details = StatutUtilisateurSerializer(source='statut', read_only=True)
    numeros_telephone = NumeroTelephoneSerializer(many=True, read_only=True)
    
    # Informations de localisation
    pays_details = serializers.SerializerMethodField()
    province_details = serializers.SerializerMethodField()
    district_details = serializers.SerializerMethodField()
    quartier_details = serializers.SerializerMethodField()
    
    # Informations de nationalité (basé sur le code pays)
    nationalite_details = serializers.SerializerMethodField()
    pays_residence_details = serializers.SerializerMethodField()

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
            'nationalite_details',  # EXPAND - Détails du pays de nationalité
            'pays_residence',
            'pays_residence_details',  # EXPAND - Détails du pays de résidence
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
            'niveau_kyc_details',  # EXPAND
            'date_validation_kyc',
            'validateur_kyc_id',
            'type_utilisateur',
            'type_utilisateur_details',  # EXPAND
            'statut',
            'statut_details',  # EXPAND
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
            'numeros_telephone',  # EXPAND - Liste des numéros
            'pays_details',  # EXPAND - Localisation hiérarchique (si définie)
            'province_details',  # EXPAND
            'district_details',  # EXPAND
            'quartier_details',  # EXPAND
            'metadonnees',
        ]
        read_only_fields = fields
    
    def get_nationalite_details(self, obj):
        """Détails du pays de nationalité basé sur le code ISO"""
        if obj.nationalite:
            from apps.localisation.models import Pays
            try:
                pays = Pays.objects.get(code_iso_2=obj.nationalite)
                return {
                    'id': str(pays.id),
                    'code_iso_2': pays.code_iso_2,
                    'code_iso_3': pays.code_iso_3,
                    'nom': pays.nom,
                    'nom_anglais': pays.nom_anglais,
                    'continent': pays.continent,
                    'sous_region': pays.sous_region,
                    'metadonnees': pays.metadonnees,
                }
            except Pays.DoesNotExist:
                return {
                    'code_iso_2': obj.nationalite,
                    'nom': obj.nationalite,
                    'note': 'Pays non trouvé dans la base de données'
                }
        return None
    
    def get_pays_residence_details(self, obj):
        """Détails du pays de résidence basé sur le code ISO"""
        if obj.pays_residence:
            from apps.localisation.models import Pays
            try:
                pays = Pays.objects.get(code_iso_2=obj.pays_residence)
                return {
                    'id': str(pays.id),
                    'code_iso_2': pays.code_iso_2,
                    'code_iso_3': pays.code_iso_3,
                    'nom': pays.nom,
                    'nom_anglais': pays.nom_anglais,
                    'continent': pays.continent,
                    'sous_region': pays.sous_region,
                    'metadonnees': pays.metadonnees,
                }
            except Pays.DoesNotExist:
                return {
                    'code_iso_2': obj.pays_residence,
                    'nom': obj.pays_residence,
                    'note': 'Pays non trouvé dans la base de données'
                }
        return None
    
    def get_pays_details(self, obj):
        """Détails complets du pays de localisation"""
        if obj.pays:
            return {
                'id': str(obj.pays.id),
                'code_iso_2': obj.pays.code_iso_2,
                'code_iso_3': obj.pays.code_iso_3,
                'nom': obj.pays.nom,
                'nom_anglais': obj.pays.nom_anglais,
                'continent': obj.pays.continent,
                'sous_region': obj.pays.sous_region,
                'latitude_centre': float(obj.pays.latitude_centre) if obj.pays.latitude_centre else None,
                'longitude_centre': float(obj.pays.longitude_centre) if obj.pays.longitude_centre else None,
                'autorise_systeme': obj.pays.autorise_systeme,
                'est_actif': obj.pays.est_actif,
                'metadonnees': obj.pays.metadonnees,
            }
        return None
    
    def get_province_details(self, obj):
        """Détails complets de la province"""
        if obj.province_geo:
            return {
                'id': str(obj.province_geo.id),
                'code': obj.province_geo.code,
                'nom': obj.province_geo.nom,
                'pays': {
                    'id': str(obj.province_geo.pays.id),
                    'code_iso_2': obj.province_geo.pays.code_iso_2,
                    'nom': obj.province_geo.pays.nom,
                },
                'latitude_centre': float(obj.province_geo.latitude_centre) if obj.province_geo.latitude_centre else None,
                'longitude_centre': float(obj.province_geo.longitude_centre) if obj.province_geo.longitude_centre else None,
                'autorise_systeme': obj.province_geo.autorise_systeme,
                'est_actif': obj.province_geo.est_actif,
                'metadonnees': obj.province_geo.metadonnees,
            }
        return None
    
    def get_district_details(self, obj):
        """Détails complets du district"""
        if obj.district:
            return {
                'id': str(obj.district.id),
                'code': obj.district.code,
                'nom': obj.district.nom,
                'province': {
                    'id': str(obj.district.province.id),
                    'code': obj.district.province.code,
                    'nom': obj.district.province.nom,
                    'pays': {
                        'code_iso_2': obj.district.province.pays.code_iso_2,
                        'nom': obj.district.province.pays.nom,
                    }
                },
                'latitude_centre': float(obj.district.latitude_centre) if obj.district.latitude_centre else None,
                'longitude_centre': float(obj.district.longitude_centre) if obj.district.longitude_centre else None,
                'autorise_systeme': obj.district.autorise_systeme,
                'est_actif': obj.district.est_actif,
                'metadonnees': obj.district.metadonnees,
            }
        return None
    
    def get_quartier_details(self, obj):
        """Détails complets du quartier"""
        if obj.quartier_geo:
            return {
                'id': str(obj.quartier_geo.id),
                'code': obj.quartier_geo.code,
                'nom': obj.quartier_geo.nom,
                'district': {
                    'id': str(obj.quartier_geo.district.id),
                    'code': obj.quartier_geo.district.code,
                    'nom': obj.quartier_geo.district.nom,
                    'province': {
                        'code': obj.quartier_geo.district.province.code,
                        'nom': obj.quartier_geo.district.province.nom,
                    }
                },
                'latitude_centre': float(obj.quartier_geo.latitude_centre) if obj.quartier_geo.latitude_centre else None,
                'longitude_centre': float(obj.quartier_geo.longitude_centre) if obj.quartier_geo.longitude_centre else None,
                'autorise_systeme': obj.quartier_geo.autorise_systeme,
                'est_actif': obj.quartier_geo.est_actif,
                'metadonnees': obj.quartier_geo.metadonnees,
            }
        return None
