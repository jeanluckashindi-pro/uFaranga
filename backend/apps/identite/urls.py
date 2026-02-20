"""
URLs pour le module IDENTITE
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CreerUtilisateurView,
    CreerAdminView,
    TypeUtilisateurViewSet,
    NiveauKYCViewSet,
    StatutUtilisateurViewSet,
    NumeroTelephoneViewSet,
)

app_name = 'identite'

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'types-utilisateurs', TypeUtilisateurViewSet, basename='type-utilisateur')
router.register(r'niveaux-kyc', NiveauKYCViewSet, basename='niveau-kyc')
router.register(r'statuts-utilisateurs', StatutUtilisateurViewSet, basename='statut-utilisateur')
router.register(r'numeros-telephone', NumeroTelephoneViewSet, basename='numero-telephone')

urlpatterns = [
    # Inscription publique (CLIENT)
    path('inscription/', CreerUtilisateurView.as_view(), name='inscription'),
    
    # Créer un ADMIN/AGENT/MARCHAND (réservé aux admins)
    path('admin/creer-utilisateur/', CreerAdminView.as_view(), name='creer-admin'),
    
    # Router URLs
    path('', include(router.urls)),
]
