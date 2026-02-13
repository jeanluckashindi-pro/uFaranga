from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'wallets'

router = DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet, basename='currency')
router.register(r'', views.WalletViewSet, basename='wallet')

urlpatterns = [
    # Route spécifique pour l'update de solde (hors router pour plus de contrôle)
    path('<uuid:pk>/balance/', views.BalanceUpdateView.as_view(), name='balance-update'),
    
    path('', include(router.urls)),
]
