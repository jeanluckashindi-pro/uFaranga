"""
Configuration centralisée des services pour Django
Utilise le gestionnaire de configuration centralisé
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire config au path pour importer le gestionnaire
config_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'config'
sys.path.insert(0, str(config_path))

try:
    from config_manager import ConfigManager
    config_manager = ConfigManager()
except ImportError:
    # Fallback si le gestionnaire n'est pas disponible
    config_manager = None

def get_service_url(category, service_name, fallback_url):
    """Obtenir l'URL d'un service avec fallback"""
    if config_manager:
        url = config_manager.get_service_url(category, service_name)
        if url:
            return url
    
    # Fallback vers les variables d'environnement ou valeur par défaut
    env_name = f"{service_name.upper().replace('-', '_')}_URL"
    return os.getenv(env_name, fallback_url)

def get_service_port(category, service_name, fallback_port):
    """Obtenir le port d'un service avec fallback"""
    if config_manager:
        port = config_manager.get_service_port(category, service_name)
        if port:
            return port
    
    # Fallback vers les variables d'environnement ou valeur par défaut
    env_name = f"{service_name.upper().replace('-', '_')}_PORT"
    return int(os.getenv(env_name, fallback_port))

# Configuration des URLs de services
SERVICE_URLS = {
    'API_GATEWAY': get_service_url('backend.node-services', 'api-gateway', 'http://localhost:3000'),
    'WALLET_SERVICE': get_service_url('backend.django-services', 'wallet-service', 'http://localhost:8001'),
    'TRANSACTION_SERVICE': get_service_url('backend.spring-services', 'transaction-service', 'http://localhost:9000'),
    'KYC_SERVICE': get_service_url('backend.django-services', 'kyc-service', 'http://localhost:8002'),
    'NOTIFICATION_SERVICE': get_service_url('backend.node-services', 'notification-service', 'http://localhost:3001'),
    'FRAUD_DETECTION_SERVICE': get_service_url('backend.spring-services', 'fraud-detection-service', 'http://localhost:9001'),
    'WEBSOCKET_SERVICE': get_service_url('backend.node-services', 'websocket-service', 'http://localhost:3002'),
}

# Configuration des ports
SERVICE_PORTS = {
    'USER_SERVICE': get_service_port('backend.django-services', 'user-service', 8000),
    'WALLET_SERVICE': get_service_port('backend.django-services', 'wallet-service', 8001),
    'KYC_SERVICE': get_service_port('backend.django-services', 'kyc-service', 8002),
    'ADMIN_SERVICE': get_service_port('backend.django-services', 'admin-service', 8003),
}

# Configuration de la base de données
def get_database_config(service_name):
    """Obtenir la configuration de base de données pour un service"""
    if config_manager:
        # Mapper le nom du service vers le nom de la base
        db_mapping = {
            'user-service': 'ufaranga_users',
            'wallet-service': 'ufaranga_wallets',
            'kyc-service': 'ufaranga_kyc',
            'admin-service': 'ufaranga_admin',
        }
        
        db_name = db_mapping.get(service_name, 'ufaranga')
        
        # Obtenir la configuration depuis le gestionnaire
        settings = config_manager.generate_django_settings(service_name)
        if 'DATABASES' in settings:
            return settings['DATABASES']
    
    # Configuration par défaut
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'ufaranga'),
            'USER': os.getenv('DB_USER', 'admin'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'secret123'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Configuration Redis
def get_redis_config(db_index=0):
    """Obtenir la configuration Redis"""
    if config_manager:
        redis_url = config_manager.get_redis_url(db_index)
        if redis_url:
            return redis_url
    
    # Fallback
    return os.getenv('REDIS_URL', f'redis://localhost:6379/{db_index}')

# Configuration Kafka
def get_kafka_config():
    """Obtenir la configuration Kafka"""
    if config_manager:
        brokers = config_manager.get_kafka_brokers()
        if brokers:
            return brokers
    
    # Fallback
    return os.getenv('KAFKA_BROKERS', 'localhost:9092')

# Timeouts et limites
SERVICE_TIMEOUTS = {
    'DEFAULT': 5000,  # 5 secondes
    'TRANSACTION': 10000,  # 10 secondes
    'FRAUD_CHECK': 3000,  # 3 secondes
    'UPLOAD': 30000,  # 30 secondes
}

# Configuration des topics Kafka
KAFKA_TOPICS = {
    'TRANSACTION_INITIATED': 'transaction.initiated',
    'TRANSACTION_COMPLETED': 'transaction.completed',
    'TRANSACTION_FAILED': 'transaction.failed',
    'USER_REGISTERED': 'user.registered',
    'USER_KYC_UPDATED': 'user.kyc.updated',
    'NOTIFICATION_SEND': 'notification.send',
    'FRAUD_DETECTED': 'fraud.detected',
}

# Configuration CORS pour les environnements
def get_cors_origins():
    """Obtenir les origines CORS autorisées"""
    if config_manager:
        environment = config_manager.get_environment()
        
        if environment == 'production':
            return [
                'https://app.ufaranga.com',
                'https://admin.ufaranga.com',
            ]
        elif environment == 'staging':
            return [
                'https://app-staging.ufaranga.com',
                'https://admin-staging.ufaranga.com',
            ]
    
    # Développement - autoriser tout
    return [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://localhost:3002',
    ]

CORS_ALLOWED_ORIGINS = get_cors_origins()

# Configuration JWT
JWT_SETTINGS = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_LIFETIME_MINUTES': 60,
    'REFRESH_TOKEN_LIFETIME_DAYS': 7,
    'ISSUER': 'ufaranga-user-service',
}

# Limites par défaut
DEFAULT_LIMITS = {
    'MAX_UPLOAD_SIZE': 10 * 1024 * 1024,  # 10MB
    'MAX_REQUESTS_PER_MINUTE': 100,
    'MAX_DAILY_TRANSACTIONS': 50,
    'MAX_TRANSACTION_AMOUNT': 10000,
}