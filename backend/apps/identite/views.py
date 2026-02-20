"""
Views pour le module IDENTITE
Gestion des utilisateurs et profils
"""
import logging
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import (
    Utilisateur, ProfilUtilisateur,
    TypeUtilisateur, NiveauKYC, StatutUtilisateur,
    NumeroTelephone
)
from .serializers import (
    CreerUtilisateurSerializer,
    CreerAdminSerializer,
    UtilisateurIdentiteSerializer,
    TypeUtilisateurSerializer,
    NiveauKYCSerializer,
    StatutUtilisateurSerializer,
    NumeroTelephoneSerializer,
)

logger = logging.getLogger('apps')


# =============================================================================
# CRÉER UN UTILISATEUR CLIENT (Inscription Publique)
# =============================================================================
@extend_schema(
    tags=['Identité - Utilisateurs'],
    summary='Inscription - Créer un compte CLIENT',
    description=(
        'Inscription publique pour créer un compte CLIENT standard. '
        'Le compte est créé avec KYC niveau 0, statut ACTIF, '
        'email et téléphone NON vérifiés. '
        'Retourne les tokens JWT pour connexion automatique.'
    ),
)
class CreerUtilisateurView(generics.CreateAPIView):
    """
    Inscription publique - Crée un utilisateur CLIENT.
    
    - Type: CLIENT (automatique)
    - KYC: Niveau 0 (automatique)
    - Statut: ACTIF (automatique)
    - Email vérifié: NON
    - Téléphone vérifié: NON
    """
    serializer_class = CreerUtilisateurSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utilisateur = serializer.save()
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(utilisateur)
        
        logger.info(
            f"Nouvel utilisateur CLIENT créé: {utilisateur.courriel} "
            f"(KYC: {utilisateur.niveau_kyc.niveau})"
        )
        
        # Retourner les détails complets
        response_serializer = UtilisateurIdentiteSerializer(utilisateur)
        
        return Response({
            'message': 'Inscription réussie',
            'utilisateur': response_serializer.data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


# =============================================================================
# CRÉER UN ADMIN/AGENT/MARCHAND (Réservé aux Admins)
# =============================================================================
@extend_schema(
    tags=['Identité - Administration'],
    summary='Admin - Créer un AGENT/MARCHAND/ADMIN',
    description=(
        'Endpoint réservé aux administrateurs pour créer des comptes '
        'AGENT, MARCHAND, ADMIN ou SUPER_ADMIN. '
        'Vérifie que l\'utilisateur connecté est bien un administrateur. '
        'Permet de définir le type, KYC, statut et vérifications.'
    ),
)
class CreerAdminView(generics.CreateAPIView):
    """
    Créer un AGENT/MARCHAND/ADMIN.
    
    Réservé aux administrateurs authentifiés.
    Vérifie que l'utilisateur connecté a les droits d'administration.
    """
    serializer_class = CreerAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        # Vérifier que l'utilisateur connecté est bien un admin
        utilisateur_connecte = request.user
        
        # Récupérer l'utilisateur identite
        try:
            admin_identite = Utilisateur.objects.get(courriel=utilisateur_connecte.email)
        except Utilisateur.DoesNotExist:
            return Response(
                {'error': 'Profil identite introuvable'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifier le type d'utilisateur
        if admin_identite.type_utilisateur.code not in ['ADMIN', 'SUPER_ADMIN']:
            logger.warning(
                f"Tentative de création d'admin par un non-admin: {utilisateur_connecte.email} "
                f"(Type: {admin_identite.type_utilisateur.code})"
            )
            return Response(
                {
                    'error': 'Accès refusé',
                    'message': 'Seuls les administrateurs peuvent créer des comptes AGENT/MARCHAND/ADMIN',
                    'votre_type': admin_identite.type_utilisateur.code
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Créer l'utilisateur
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        utilisateur = serializer.save()
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(utilisateur)
        
        logger.info(
            f"Nouvel utilisateur {utilisateur.type_utilisateur.code} créé par {admin_identite.courriel}: "
            f"{utilisateur.courriel} (KYC: {utilisateur.niveau_kyc.niveau})"
        )
        
        # Retourner les détails complets
        response_serializer = UtilisateurIdentiteSerializer(utilisateur)
        
        return Response({
            'message': f'Utilisateur {utilisateur.type_utilisateur.libelle} créé avec succès',
            'utilisateur': response_serializer.data,
            'cree_par': {
                'courriel': admin_identite.courriel,
                'nom_complet': admin_identite.nom_complet,
                'type': admin_identite.type_utilisateur.code
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


# =============================================================================
# TABLES DE RÉFÉRENCE
# =============================================================================
@extend_schema(tags=['Identité - Référence'])
class TypeUtilisateurViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des types d'utilisateurs disponibles.
    
    Types: CLIENT, AGENT, MARCHAND, ADMIN, SUPER_ADMIN, SYSTEME
    """
    queryset = TypeUtilisateur.objects.filter(est_actif=True).order_by('ordre_affichage')
    serializer_class = TypeUtilisateurSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Identité - Référence'])
class NiveauKYCViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des niveaux KYC disponibles.
    
    Niveaux: 0 (Non vérifié), 1 (Basique), 2 (Complet), 3 (Premium)
    """
    queryset = NiveauKYC.objects.filter(est_actif=True).order_by('niveau')
    serializer_class = NiveauKYCSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['Identité - Référence'])
class StatutUtilisateurViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des statuts utilisateurs disponibles.
    
    Statuts: ACTIF, EN_VERIFICATION, SUSPENDU, BLOQUE, FERME
    """
    queryset = StatutUtilisateur.objects.filter(est_actif=True).order_by('ordre_affichage')
    serializer_class = StatutUtilisateurSerializer
    permission_classes = [AllowAny]


# =============================================================================
# GESTION DES NUMÉROS DE TÉLÉPHONE
# =============================================================================
@extend_schema(tags=['Identité - Numéros'])
class NumeroTelephoneViewSet(viewsets.ModelViewSet):
    """
    Gestion des numéros de téléphone des utilisateurs.
    
    - Liste des numéros de l'utilisateur connecté
    - Ajouter un nouveau numéro
    - Vérifier un numéro par SMS
    - Définir un numéro comme principal
    - Supprimer un numéro
    """
    serializer_class = NumeroTelephoneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les numéros de l'utilisateur connecté"""
        return NumeroTelephone.objects.filter(
            utilisateur=self.request.user,
            statut__in=['ACTIF', 'SUSPENDU']
        ).order_by('-est_principal', '-date_creation')
    
    @action(detail=False, methods=['post'])
    def ajouter_numero(self, request):
        """
        Ajoute un nouveau numéro à l'utilisateur.
        
        Vérifie la limite de numéros autorisés selon le pays et le type d'utilisateur.
        """
        from .models import LimiteNumerosParPays
        
        utilisateur = request.user
        pays_code = request.data.get('pays_code_iso_2')
        
        # Vérifier la limite
        nb_numeros_actuels = NumeroTelephone.objects.filter(
            utilisateur=utilisateur,
            statut='ACTIF'
        ).count()
        
        try:
            limite = LimiteNumerosParPays.objects.get(
                pays_code_iso_2=pays_code,
                type_utilisateur=utilisateur.type_utilisateur
            )
            if nb_numeros_actuels >= limite.nombre_max_numeros:
                return Response(
                    {
                        'error': f'Limite de {limite.nombre_max_numeros} numéros atteinte',
                        'limite': limite.nombre_max_numeros,
                        'actuels': nb_numeros_actuels
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except LimiteNumerosParPays.DoesNotExist:
            # Utiliser limite par défaut
            if nb_numeros_actuels >= 3:
                return Response(
                    {
                        'error': 'Limite de 3 numéros atteinte',
                        'limite': 3,
                        'actuels': nb_numeros_actuels
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Créer le numéro
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        numero = serializer.save(utilisateur=utilisateur)
        
        logger.info(f"Nouveau numéro ajouté pour {utilisateur.courriel}: {numero.numero_complet}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def envoyer_code_verification(self, request, pk=None):
        """
        Envoie un code de vérification par SMS.
        
        Génère un code à 6 chiffres et l'envoie au numéro.
        """
        numero = self.get_object()
        
        if numero.est_verifie:
            return Response(
                {'message': 'Numéro déjà vérifié'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Intégrer avec le service SMS
        # from apps.authentication.services_sms import envoyer_code_confirmation
        
        import random
        import hashlib
        from django.utils import timezone
        
        # Générer un code à 6 chiffres
        code = str(random.randint(100000, 999999))
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        # Sauvegarder le hash
        numero.code_verification_hash = code_hash
        numero.tentatives_verification += 1
        numero.derniere_tentative_verification = timezone.now()
        numero.save()
        
        logger.info(f"Code de vérification envoyé à {numero.numero_complet}")
        
        return Response({
            'message': 'Code de vérification envoyé',
            'code': code,  # À retirer en production!
            'numero': numero.numero_complet
        })
    
    @action(detail=True, methods=['post'])
    def verifier_code(self, request, pk=None):
        """
        Vérifie le code reçu par SMS.
        
        Si le code est correct, marque le numéro comme vérifié.
        """
        numero = self.get_object()
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'Code requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        import hashlib
        from django.utils import timezone
        
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        
        if code_hash == numero.code_verification_hash:
            numero.est_verifie = True
            numero.date_verification = timezone.now()
            numero.methode_verification = 'SMS'
            numero.save()
            
            logger.info(f"Numéro vérifié: {numero.numero_complet}")
            
            return Response({
                'message': 'Numéro vérifié avec succès',
                'numero': NumeroTelephoneSerializer(numero).data
            })
        else:
            return Response(
                {'error': 'Code invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def definir_principal(self, request, pk=None):
        """
        Définit ce numéro comme principal.
        
        Le numéro doit être vérifié pour devenir principal.
        """
        numero = self.get_object()
        
        if not numero.est_verifie:
            return Response(
                {'error': 'Le numéro doit être vérifié pour devenir principal'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Retirer le flag principal des autres numéros
        NumeroTelephone.objects.filter(
            utilisateur=numero.utilisateur,
            est_principal=True
        ).update(est_principal=False)
        
        # Définir ce numéro comme principal
        numero.est_principal = True
        numero.save()
        
        logger.info(f"Numéro principal défini: {numero.numero_complet}")
        
        return Response({
            'message': 'Numéro principal défini',
            'numero': NumeroTelephoneSerializer(numero).data
        })
    
    @action(detail=False, methods=['get'])
    def numeros_restants(self, request):
        """
        Retourne le nombre de numéros que l'utilisateur peut encore ajouter.
        """
        from .models import LimiteNumerosParPays
        
        utilisateur = request.user
        pays_code = request.query_params.get('pays_code_iso_2', 'BI')
        
        nb_actuels = NumeroTelephone.objects.filter(
            utilisateur=utilisateur,
            statut='ACTIF'
        ).count()
        
        try:
            limite = LimiteNumerosParPays.objects.get(
                pays_code_iso_2=pays_code,
                type_utilisateur=utilisateur.type_utilisateur
            )
            max_numeros = limite.nombre_max_numeros
        except LimiteNumerosParPays.DoesNotExist:
            max_numeros = 3
        
        return Response({
            'numeros_actuels': nb_actuels,
            'limite_max': max_numeros,
            'numeros_restants': max_numeros - nb_actuels,
            'pays_code': pays_code,
            'type_utilisateur': utilisateur.type_utilisateur.code
        })
