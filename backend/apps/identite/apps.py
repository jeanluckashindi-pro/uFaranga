from django.apps import AppConfig


class IdentiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.identite'
    verbose_name = 'Identité et Authentification'
    
    def ready(self):
        import apps.identite.signals
