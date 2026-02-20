from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'localisation'

router = DefaultRouter()
router.register(r'pays', views.PaysViewSet, basename='pays')
router.register(r'provinces', views.ProvinceViewSet, basename='provinces')
router.register(r'districts', views.DistrictViewSet, basename='districts')
router.register(r'quartiers', views.QuartierViewSet, basename='quartiers')
router.register(r'points-de-service', views.PointDeServiceViewSet, basename='points-de-service')
router.register(r'complete', views.LocalisationCompleteViewSet, basename='localisation-complete')

urlpatterns = [
    path('', include(router.urls)),
]
