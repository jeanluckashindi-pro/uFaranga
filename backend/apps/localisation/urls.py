from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_optimisees import *
from .views_geo import GeoLocalisationViewSet

app_name = 'localisation'

router = DefaultRouter()

# Endpoints optimisés avec pagination
router.register(r'pays', PaysOptimiseViewSet, basename='pays')
router.register(r'provinces', ProvinceOptimiseViewSet, basename='provinces')
router.register(r'districts', DistrictOptimiseViewSet, basename='districts')
router.register(r'communes', CommuneOptimiseViewSet, basename='communes')
router.register(r'secteurs', SecteurOptimiseViewSet, basename='secteurs')
router.register(r'quartiers', QuartierOptimiseViewSet, basename='quartiers')
router.register(r'zones', ZoneOptimiseViewSet, basename='zones')
router.register(r'collines', CollineOptimiseViewSet, basename='collines')
router.register(r'points-de-service', PointDeServiceOptimiseViewSet, basename='points-de-service')
router.register(r'hierarchie', HierarchieOptimiseeViewSet, basename='hierarchie')

# Endpoints géospatiaux pour carte dynamique
router.register(r'geo', GeoLocalisationViewSet, basename='geo')

urlpatterns = [
    path('', include(router.urls)),
]
