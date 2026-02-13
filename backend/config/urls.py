"""
URL configuration for user-service.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Health Check
    path('health/', include('apps.users.health')),

    # OAuth 2.0 Authentication
    path('api/v1/oauth2/', include('apps.oauth2.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Authentication (login, register, token refresh, logout)
    path('api/v1/auth/', include('apps.authentication.urls')),

    # Users (CRUD, profiles, sessions)
    path('api/v1/users/', include('apps.users.urls')),

    # Wallets (Currencies, Wallets, Transactions)
    path('api/v1/wallets/', include('apps.wallets.urls')),

    # API Publique (nécessite clé API)
    path('api/public/', include('apps.public_api.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Redirect root to docs
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='root'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
