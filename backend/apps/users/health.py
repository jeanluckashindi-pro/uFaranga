"""Health check endpoint for user-service."""
from django.urls import path
from django.http import JsonResponse
from django.db import connection
import time


def health_check(request):
    """
    Health check endpoint.
    Vérifie la connexion à la base de données.
    Utilisé par Docker, Kubernetes, et le monitoring.
    """
    health = {
        'status': 'OK',
        'service': 'user-service',
        'timestamp': time.time(),
        'checks': {}
    }

    # Check PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health['checks']['database'] = 'OK'
    except Exception as e:
        health['status'] = 'DEGRADED'
        health['checks']['database'] = f'ERROR: {str(e)}'

    status_code = 200 if health['status'] == 'OK' else 503
    return JsonResponse(health, status=status_code)


urlpatterns = [
    path('', health_check, name='health-check'),
]
