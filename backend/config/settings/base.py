import os
from pathlib import Path

# Compatibility patch for PostgreSQL 10 (Django 4.2 requires 12+)
import config.pg_compat  # noqa: F401

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# SECURITY
# =============================================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ufaranga-dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# =============================================================================
# APPLICATIONS
# =============================================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'oauth2_provider',  # Django OAuth Toolkit
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]

LOCAL_APPS = [
    # Modules existants
    'apps.users',
    'apps.authentication',
    'apps.wallets',
    'apps.oauth2',  # OAuth 2.0
    # Nouveaux modules uFaranga
    'apps.identite',
    'apps.bancaire',
    'apps.portefeuille',
    'apps.transaction',
    'apps.audit',
    'apps.compliance',
    'apps.commission',
    'apps.notification',
    'apps.configuration',
    'apps.localisation',  # Hiérarchie géo : Pays → Province → District → Quartier → Point de service
    'apps.developpeurs',  # Comptes développeurs et API keys
    'apps.public_api',  # API publique
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URL & TEMPLATE CONFIG
# =============================================================================
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# =============================================================================
# DATABASE — PostgreSQL Local
# =============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'ufaranga'),
        'USER': os.environ.get('DB_USER', 'ufaranga'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '12345'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c search_path=public,identite,bancaire,portefeuille,transaction,audit,compliance,commission,notification,configuration,localisation',
        },
    }
}

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Bujumbura'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.developpeurs.authentication.APIKeyAuthentication',  # API Key (pour développeurs)
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # OAuth 2.0
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT (fallback)
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '100/minute',
    },
    'EXCEPTION_HANDLER': 'apps.users.exceptions.custom_exception_handler',
}

# =============================================================================
# SIMPLE JWT (durées définies dans config.constants)
# =============================================================================
from config.constants import (
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME_REMEMBER_ME,
)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME_REMEMBER_ME': REFRESH_TOKEN_LIFETIME_REMEMBER_ME,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_OBTAIN_SERIALIZER': 'apps.authentication.serializers.CustomTokenObtainPairSerializer',
}

# =============================================================================
# CORS
# =============================================================================
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if not DEBUG else []
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# REDIS
# =============================================================================
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# =============================================================================
# DRF SPECTACULAR (API Documentation)
# =============================================================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'uFaranga User Service API',
    'DESCRIPTION': 'Service de gestion des utilisateurs et authentification pour la plateforme uFaranga',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'Authentication', 'description': 'Inscription, connexion, tokens JWT'},
        {'name': 'Users', 'description': 'Gestion des utilisateurs et profils'},
        {'name': 'Sessions', 'description': 'Gestion des sessions utilisateur'},
    ],
    # Par défaut, Swagger (/api/docs/ et /) n'affiche que les APIs v1 (pas l'API publique)
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
        'config.spectacular_hooks.postprocess_filter_v1_only',
    ],
}

# =============================================================================
# LOGGING
# =============================================================================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'user-service.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}


# =============================================================================
# OAUTH 2.0 CONFIGURATION (Django OAuth Toolkit)
# =============================================================================
OAUTH2_PROVIDER = {
    # Durées de vie des tokens
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 heure
    'REFRESH_TOKEN_EXPIRE_SECONDS': 604800,  # 7 jours
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,  # 10 minutes
    
    # Types de grants supportés
    'SCOPES': {
        'read': 'Lecture des données',
        'write': 'Écriture des données',
        'transactions': 'Gestion des transactions',
        'wallets': 'Gestion des portefeuilles',
        'profile': 'Accès au profil utilisateur',
        'admin': 'Accès administrateur',
    },
    
    # Scopes par défaut
    'DEFAULT_SCOPES': ['read', 'profile'],
    
    # Rotation des refresh tokens
    'ROTATE_REFRESH_TOKEN': True,
    
    # Algorithme de hachage pour les tokens
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    
    # Validation des redirects URIs
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https'],
    
    # Paramètres de sécurité
    'PKCE_REQUIRED': True,  # Proof Key for Code Exchange (recommandé pour mobile)
    'REFRESH_TOKEN_GRACE_PERIOD_SECONDS': 120,  # 2 minutes de grâce
    
    # Applications
    'APPLICATION_MODEL': 'oauth2_provider.Application',
    'ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
    'GRANT_MODEL': 'oauth2_provider.Grant',
    
    # Paramètres d'erreur
    'ERROR_RESPONSE_WITH_SCOPES': True,
    
    # Introspection
    'RESOURCE_SERVER_INTROSPECTION_URL': None,
    'RESOURCE_SERVER_AUTH_TOKEN': None,
    
    # OIDC (OpenID Connect) - Optionnel
    'OIDC_ENABLED': False,
    'OIDC_RSA_PRIVATE_KEY': os.environ.get('OIDC_RSA_PRIVATE_KEY', ''),
}

# Configuration des scopes requis par endpoint
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

# Middleware OAuth2 (optionnel, pour l'introspection)
# MIDDLEWARE += ['oauth2_provider.middleware.OAuth2TokenMiddleware']
