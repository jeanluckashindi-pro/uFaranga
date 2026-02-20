#!/usr/bin/env python
"""
Script pour générer automatiquement des métadonnées pour provinces, districts et quartiers
"""
import os
import sys
import django
from decimal import Decimal
import random

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier

# Données de référence
ECONOMIES_PAR_TYPE = {
    'capitale': ['Services', 'Administration', 'Finance', 'Commerce', 'Technologie'],
    'port': ['Port', 'Commerce maritime', 'Pêche', 'Logistique'],
    'agricole': ['Agriculture', 'Élevage', 'Agro-industrie'],
    'minier': ['Mines', 'Extraction', 'Industrie'],
    'touristique': ['Tourisme', 'Hôtellerie', 'Artisanat'],
    'urbain': ['Commerce', 'Services', 'Industrie'],
    'rural': ['Agriculture', 'Élevage', 'Artisanat'],
}

def detecter_type_province(nom, est_capitale=False):
    """Détecter le type de province basé sur son nom"""
    nom_lower = nom.lower()
    
    if est_capitale or 'capital' in nom_lower or 'ville' in nom_lower:
        return 'capitale'
    elif 'port' in nom_lower or 'maritime' in nom_lower or 'littoral' in nom_lower:
        return 'port'
    elif 'mine' in nom_lower or 'katanga' in nom_lower:
        return 'minier'
    elif 'parc' in nom_lower or 'reserve' in nom_lower:
        return 'touristique'
    elif 'nord' in nom_lower or 'sud' in nom_lower or 'est' in nom_lower or 'ouest' in nom_lower:
        return 'rural'
    else:
        return 'urbain'

def estimer_population(type_zone, est_capitale=False):
    """Estimer la population selon le type de zone"""
    if est_capitale:
        return random.randint(1000000, 5000000)
    elif type_zone == 'capitale':
        return random.randint(500000, 2000000)
    elif type_zone == 'port':
        return random.randint(300000, 1500000)
    elif type_zone == 'urbain':
        return random.randint(200000, 800000)
    elif type_zone == 'minier':
        return random.randint(150000, 600000)
    elif type_zone == 'touristique':
        return random.randint(100000, 400000)
    else:  # rural
        return random.randint(50000, 300000)

def generer_metadonnees_province(province, pays):
    """Générer des métadonnées pour une province"""
    # Vérifier si c'est la capitale
    capitale = pays.metadonnees.get('capitale', '')
    est_capitale = capitale.lower() in province.nom.lower()
    
    # Détecter le type
    type_zone = detecter_type_province(province.nom, est_capitale)
    
    # Générer les métadonnées
    metadonnees = {
        'population_estimee': estimer_population(type_zone, est_capitale),
        'superficie_km2': random.randint(1000, 50000),
        'chef_lieu': province.nom,
        'fuseau_horaire': pays.metadonnees.get('fuseau_horaire', 'UTC+0'),
        'langues_principales': pays.metadonnees.get('langues', ['Français']),
        'economie_principale': ECONOMIES_PAR_TYPE.get(type_zone, ['Agriculture', 'Commerce']),
        'type_zone': type_zone,
        'densite_population': 'élevée' if type_zone in ['capitale', 'port', 'urbain'] else 'moyenne',
        'niveau_developpement': 'élevé' if est_capitale else 'moyen',
        'derniere_mise_a_jour': '2026-02-20'
    }
    
    if est_capitale:
        metadonnees['est_capitale'] = True
        metadonnees['services_disponibles'] = [
            'Hôpitaux', 'Universités', 'Aéroport', 'Banques', 'Centres commerciaux'
        ]
    
    return metadonnees

def generer_metadonnees_district(district, province):
    """Générer des métadonnées pour un district"""
    type_zone = detecter_type_province(district.nom)
    
    metadonnees = {
        'population_estimee': estimer_population(type_zone) // 5,  # Plus petit que province
        'superficie_km2': random.randint(100, 5000),
        'chef_lieu': district.nom,
        'economie_principale': ECONOMIES_PAR_TYPE.get(type_zone, ['Agriculture', 'Commerce'])[:3],
        'type_zone': type_zone,
        'services_disponibles': ['Hôpital', 'Écoles', 'Marché', 'Poste'],
        'infrastructures': {
            'routes_pavees': random.choice([True, False]),
            'electricite': random.choice(['permanente', 'intermittente', 'limitée']),
            'eau_potable': random.choice(['réseau', 'puits', 'mixte']),
            'internet': random.choice(['4G', '3G', 'limité'])
        },
        'derniere_mise_a_jour': '2026-02-20'
    }
    
    return metadonnees

def generer_metadonnees_quartier(quartier, district):
    """Générer des métadonnées pour un quartier"""
    type_zone = detecter_type_province(quartier.nom)
    
    metadonnees = {
        'population_estimee': random.randint(5000, 50000),
        'superficie_km2': random.randint(1, 100),
        'type_quartier': random.choice(['résidentiel', 'commercial', 'mixte', 'industriel']),
        'economie_principale': random.sample(['Commerce', 'Artisanat', 'Services', 'Agriculture'], 2),
        'services_disponibles': random.sample([
            'École primaire', 'Centre de santé', 'Marché', 'Poste de police',
            'Église', 'Mosquée', 'Terrain de sport'
        ], random.randint(3, 5)),
        'infrastructures': {
            'routes': random.choice(['pavées', 'terre', 'mixte']),
            'electricite': random.choice(['oui', 'partiel', 'non']),
            'eau_potable': random.choice(['réseau', 'puits', 'fontaine']),
            'transport_public': random.choice(['oui', 'non'])
        },
        'securite': random.choice(['bonne', 'moyenne', 'à améliorer']),
        'derniere_mise_a_jour': '2026-02-20'
    }
    
    return metadonnees

def main():
    print("=" * 70)
    print("GÉNÉRATION DES MÉTADONNÉES POUR LOCALISATION")
    print("=" * 70)
    
    # Statistiques
    stats = {
        'provinces_mises_a_jour': 0,
        'districts_mis_a_jour': 0,
        'quartiers_mis_a_jour': 0
    }
    
    # Traiter les provinces
    print("\n📍 Traitement des PROVINCES...")
    provinces = Province.objects.select_related('pays').filter(
        pays__continent='Afrique'
    )
    
    for province in provinces:
        if not province.metadonnees or province.metadonnees == {}:
            province.metadonnees = generer_metadonnees_province(province, province.pays)
            province.save()
            stats['provinces_mises_a_jour'] += 1
            
            if stats['provinces_mises_a_jour'] % 50 == 0:
                print(f"   ✅ {stats['provinces_mises_a_jour']} provinces traitées...")
    
    print(f"   ✅ Total: {stats['provinces_mises_a_jour']} provinces mises à jour")
    
    # Traiter les districts
    print("\n📍 Traitement des DISTRICTS...")
    districts = District.objects.select_related('province__pays').all()
    
    for district in districts:
        if not district.metadonnees or district.metadonnees == {}:
            district.metadonnees = generer_metadonnees_district(district, district.province)
            district.save()
            stats['districts_mis_a_jour'] += 1
            
            if stats['districts_mis_a_jour'] % 50 == 0:
                print(f"   ✅ {stats['districts_mis_a_jour']} districts traités...")
    
    print(f"   ✅ Total: {stats['districts_mis_a_jour']} districts mis à jour")
    
    # Traiter les quartiers
    print("\n📍 Traitement des QUARTIERS...")
    quartiers = Quartier.objects.select_related('district__province__pays').all()
    
    for quartier in quartiers:
        if not quartier.metadonnees or quartier.metadonnees == {}:
            quartier.metadonnees = generer_metadonnees_quartier(quartier, quartier.district)
            quartier.save()
            stats['quartiers_mis_a_jour'] += 1
            
            if stats['quartiers_mis_a_jour'] % 50 == 0:
                print(f"   ✅ {stats['quartiers_mis_a_jour']} quartiers traités...")
    
    print(f"   ✅ Total: {stats['quartiers_mis_a_jour']} quartiers mis à jour")
    
    # Résumé final
    print("\n" + "=" * 70)
    print("✅ GÉNÉRATION TERMINÉE")
    print("=" * 70)
    print(f"Provinces mises à jour: {stats['provinces_mises_a_jour']}")
    print(f"Districts mis à jour: {stats['districts_mis_a_jour']}")
    print(f"Quartiers mis à jour: {stats['quartiers_mis_a_jour']}")
    print(f"TOTAL: {sum(stats.values())} entités mises à jour")
    print("=" * 70)

if __name__ == '__main__':
    main()
