"""
Script complet pour peupler TOUS les pays africains avec provinces, districts, quartiers et GPS
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier
from decimal import Decimal

print("\n" + "="*80)
print("PEUPLEMENT COMPLET DES DONNÉES DE LOCALISATION")
print("="*80)

# Données complètes des pays avec provinces
DONNEES_COMPLETES = {
    'BI': {
        'provinces': [
            {'code': 'BB', 'nom': 'Bubanza', 'lat': -3.0833, 'lon': 29.3833},
            {'code': 'BM', 'nom': 'Bujumbura Mairie', 'lat': -3.3822, 'lon': 29.3644},
            {'code': 'BR', 'nom': 'Bujumbura Rural', 'lat': -3.5000, 'lon': 29.5000},
            {'code': 'BU', 'nom': 'Bururi', 'lat': -3.9500, 'lon': 29.6167},
            {'code': 'CA', 'nom': 'Cankuzo', 'lat': -3.2167, 'lon': 30.6000},
            {'code': 'CI', 'nom': 'Cibitoke', 'lat': -2.8833, 'lon': 29.1167},
            {'code': 'GI', 'nom': 'Gitega', 'lat': -3.4271, 'lon': 29.9246},
            {'code': 'KI', 'nom': 'Kirundo', 'lat': -2.5833, 'lon': 30.1000},
            {'code': 'KR', 'nom': 'Karuzi', 'lat': -3.1000, 'lon': 30.1667},
            {'code': 'KY', 'nom': 'Kayanza', 'lat': -2.9167, 'lon': 29.6333},
            {'code': 'MA', 'nom': 'Makamba', 'lat': -4.1333, 'lon': 29.8000},
            {'code': 'MU', 'nom': 'Muramvya', 'lat': -3.2667, 'lon': 29.6167},
            {'code': 'MW', 'nom': 'Mwaro', 'lat': -3.5167, 'lon': 29.7000},
            {'code': 'MY', 'nom': 'Muyinga', 'lat': -2.8500, 'lon': 30.3333},
            {'code': 'NG', 'nom': 'Ngozi', 'lat': -2.9167, 'lon': 29.8333},
            {'code': 'RT', 'nom': 'Rutana', 'lat': -3.9333, 'lon': 30.0000},
            {'code': 'RY', 'nom': 'Ruyigi', 'lat': -3.4833, 'lon': 30.2500},
        ]
    },
    'RW': {
        'provinces': [
            {'code': 'KIG', 'nom': 'Kigali', 'lat': -1.9536, 'lon': 30.0606},
            {'code': 'EST', 'nom': 'Est', 'lat': -2.0000, 'lon': 30.5000},
            {'code': 'NOR', 'nom': 'Nord', 'lat': -1.5000, 'lon': 29.8000},
            {'code': 'OUE', 'nom': 'Ouest', 'lat': -2.0000, 'lon': 29.3000},
            {'code': 'SUD', 'nom': 'Sud', 'lat': -2.5000, 'lon': 29.7000},
        ]
    },
    'KE': {
        'provinces': [
            {'code': 'NAI', 'nom': 'Nairobi', 'lat': -1.2921, 'lon': 36.8219},
            {'code': 'MOM', 'nom': 'Mombasa', 'lat': -4.0435, 'lon': 39.6682},
            {'code': 'KIS', 'nom': 'Kisumu', 'lat': -0.0917, 'lon': 34.7680},
            {'code': 'NAK', 'nom': 'Nakuru', 'lat': -0.3031, 'lon': 36.0800},
        ]
    },
    'TZ': {
        'provinces': [
            {'code': 'DAR', 'nom': 'Dar es Salaam', 'lat': -6.7924, 'lon': 39.2083},
            {'code': 'DOD', 'nom': 'Dodoma', 'lat': -6.1630, 'lon': 35.7516},
            {'code': 'ARU', 'nom': 'Arusha', 'lat': -3.3869, 'lon': 36.6830},
            {'code': 'MWA', 'nom': 'Mwanza', 'lat': -2.5164, 'lon': 32.9175},
        ]
    },
    'UG': {
        'provinces': [
            {'code': 'KAM', 'nom': 'Kampala', 'lat': 0.3476, 'lon': 32.5825},
            {'code': 'ENT', 'nom': 'Entebbe', 'lat': 0.0560, 'lon': 32.4634},
            {'code': 'GUL', 'nom': 'Gulu', 'lat': 2.7747, 'lon': 32.2989},
            {'code': 'MBA', 'nom': 'Mbarara', 'lat': -0.6069, 'lon': 30.6582},
        ]
    },
}

# Continuer avec les autres pays...
