from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'wallets'

router = DefaultRouter()
router.register(r'devises', views.CurrencyViewSet, basename='currency')
router.register(r'', views.WalletViewSet, basename='wallet')

urlpatterns = [
    # Mise à jour du solde (hors router pour plus de contrôle)
    path('<uuid:pk>/solde/', views.BalanceUpdateView.as_view(), name='balance-update'),
    
    path('', include(router.urls)),
]
