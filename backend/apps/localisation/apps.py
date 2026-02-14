from django.apps import AppConfig


class LocalisationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.localisation'
    verbose_name = 'Localisation (Pays, Province, District, Quartier, Point de service)'
