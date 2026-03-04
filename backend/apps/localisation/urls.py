from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_optimisees import *
from .views_geo import GeoLocalisationViewSet

app_name = 'localisation'

router = DefaultRouter()

# Endpoints optimisés avec pagination
router.register(r'pays', PaysOptimiseViewSet, basename='pays')
router.register(r'niveau0', DivisionNiveau0ViewSet, basename='niveau0')
router.register(r'niveau1', DivisionNiveau1ViewSet, basename='niveau1')
router.register(r'niveau2', DivisionNiveau2ViewSet, basename='niveau2')

# Alias pour compatibilité
router.register(r'provinces', ProvinceOptimiseViewSet, basename='provinces')
router.register(r'districts', DistrictOptimiseViewSet, basename='districts')

# Points de service
router.register(r'points-de-service', PointDeServiceOptimiseViewSet, basename='points-de-service')

# Statistiques
router.register(r'statistiques', LocalisationStatistiquesViewSet, basename='statistiques')

# Endpoints géospatiaux pour carte dynamique
router.register(r'geo', GeoLocalisationViewSet, basename='geo')

urlpatterns = [
    path('', include(router.urls)),
]
