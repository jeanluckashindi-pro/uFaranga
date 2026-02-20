#!/usr/bin/env python
"""
Script pour peupler automatiquement les districts et quartiers
pour toutes les provinces du système
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

# Noms génériques pour districts
NOMS_DISTRICTS = [
    'Centre', 'Nord', 'Sud', 'Est', 'Ouest',
    'Centre-Ville', 'Périphérie', 'Zone Industrielle',
    'Zone Commerciale', 'Zone Résidentielle',
    'Commune 1', 'Commune 2', 'Commune 3',
    'Secteur A', 'Secteur B', 'Secteur C'
]

# Noms génériques pour quartiers
NOMS_QUARTIERS = [
    'Centre', 'Marché', 'Gare', 'Port', 'Aéroport',
    'Résidentiel', 'Commercial', 'Industriel',
    'Quartier 1', 'Quartier 2', 'Quartier 3', 'Quartier 4',
    'Zone A', 'Zone B', 'Zone C', 'Zone D',
    'Secteur 1', 'Secteur 2', 'Secteur 3',
    'Cité', 'Village', 'Plateau', 'Colline', 'Vallée'
]

def generer_coordonnees_proches(lat_centre, lon_centre, rayon_km=20):
    """Générer des coordonnées GPS proches d'un centre"""
    if not lat_centre or not lon_centre:
        return None, None
    
    # 1 degré ≈ 111 km
    delta_lat = (random.uniform(-rayon_km, rayon_km) / 111)
    delta_lon = (random.uniform(-rayon_km, rayon_km) / 111)
    
    return (
        float(lat_centre) + delta_lat,
        float(lon_centre) + delta_lon
    )

def determiner_nombre_districts(province):
    """Déterminer le nombre de districts selon le type de province"""
    metadonnees = province.metadonnees or {}
    population = metadonnees.get('population_estimee', 200000)
    type_zone = metadonnees.get('type_zone', 'rural')
    
    if type_zone == 'capitale' or population > 2000000:
        return random.randint(5, 8)
    elif type_zone in ['port', 'urbain'] or population > 1000000:
        return random.randint(4, 6)
    elif population > 500000:
        return random.randint(3, 5)
    else:
        return random.randint(2, 4)

def determiner_nombre_quartiers(district):
    """Déterminer le nombre de quartiers selon le type de district"""
    metadonnees = district.metadonnees or {}
    population = metadonnees.get('population_estimee', 50000)
    type_zone = metadonnees.get('type_zone', 'rural')
    
    if type_zone == 'capitale' or population > 500000:
        return random.randint(6, 10)
    elif type_zone in ['port', 'urbain'] or population > 200000:
        return random.randint(4, 7)
    elif population > 100000:
        return random.randint(3, 5)
    else:
        return random.randint(2, 4)

def creer_districts_pour_province(province):
    """Créer des districts pour une province"""
    nb_districts = determiner_nombre_districts(province)
    districts_crees = []
    
    # Vérifier si des districts existent déjà
    districts_existants = District.objects.filter(province=province).count()
    if districts_existants > 0:
        return []  # Ne pas créer si déjà existants
    
    for i in range(nb_districts):
        # Choisir un nom de district
        if i < len(NOMS_DISTRICTS):
            nom = f"{NOMS_DISTRICTS[i]}"
        else:
            nom = f"District {i+1}"
        
        # Générer coordonnées
        lat, lon = generer_coordonnees_proches(
            province.latitude_centre,
            province.longitude_centre,
            rayon_km=30
        )
        
        if lat and lon:
            # Créer le district
            district = District(
                province=province,
                code=f"D{i+1:02d}",
                nom=nom,
                latitude_centre=Decimal(str(round(lat, 7))),
                longitude_centre=Decimal(str(round(lon, 7))),
                autorise_systeme=True,
                est_actif=True,
                metadonnees={
                    'population_estimee': random.randint(50000, 500000),
                    'superficie_km2': random.randint(100, 5000),
                    'chef_lieu': nom,
                    'type_zone': random.choice(['urbain', 'rural', 'mixte']),
                    'economie_principale': random.sample([
                        'Agriculture', 'Commerce', 'Artisanat', 'Services', 'Industrie'
                    ], 2),
                    'services_disponibles': random.sample([
                        'Hôpital', 'Écoles', 'Marché', 'Poste', 'Banque'
                    ], random.randint(2, 4)),
                    'infrastructures': {
                        'routes_pavees': random.choice([True, False]),
                        'electricite': random.choice(['permanente', 'intermittente', 'limitée']),
                        'eau_potable': random.choice(['réseau', 'puits', 'mixte']),
                        'internet': random.choice(['4G', '3G', 'limité', 'non'])
                    }
                }
            )
            district.save()
            districts_crees.append(district)
    
    return districts_crees

def creer_quartiers_pour_district(district):
    """Créer des quartiers pour un district"""
    nb_quartiers = determiner_nombre_quartiers(district)
    quartiers_crees = []
    
    # Vérifier si des quartiers existent déjà
    quartiers_existants = Quartier.objects.filter(district=district).count()
    if quartiers_existants > 0:
        return []  # Ne pas créer si déjà existants
    
    for i in range(nb_quartiers):
        # Choisir un nom de quartier
        if i < len(NOMS_QUARTIERS):
            nom = f"{NOMS_QUARTIERS[i]}"
        else:
            nom = f"Quartier {i+1}"
        
        # Générer coordonnées
        lat, lon = generer_coordonnees_proches(
            district.latitude_centre,
            district.longitude_centre,
            rayon_km=5
        )
        
        if lat and lon:
            # Créer le quartier
            quartier = Quartier(
                district=district,
                code=f"Q{i+1:02d}",
                nom=nom,
                latitude_centre=Decimal(str(round(lat, 7))),
                longitude_centre=Decimal(str(round(lon, 7))),
                autorise_systeme=True,
                est_actif=True,
                metadonnees={
                    'population_estimee': random.randint(5000, 50000),
                    'superficie_km2': random.randint(1, 100),
                    'type_quartier': random.choice(['résidentiel', 'commercial', 'mixte', 'industriel']),
                    'economie_principale': random.sample([
                        'Commerce', 'Artisanat', 'Services', 'Agriculture', 'Industrie'
                    ], 2),
                    'services_disponibles': random.sample([
                        'École primaire', 'Centre de santé', 'Marché',
                        'Poste de police', 'Église', 'Mosquée', 'Terrain de sport'
                    ], random.randint(3, 5)),
                    'infrastructures': {
                        'routes': random.choice(['pavées', 'terre', 'mixte']),
                        'electricite': random.choice(['oui', 'partiel', 'non']),
                        'eau_potable': random.choice(['réseau', 'puits', 'fontaine']),
                        'transport_public': random.choice(['oui', 'non'])
                    },
                    'securite': random.choice(['bonne', 'moyenne', 'à améliorer'])
                }
            )
            quartier.save()
            quartiers_crees.append(quartier)
    
    return quartiers_crees

def main():
    print("=" * 80)
    print("PEUPLEMENT AUTOMATIQUE DES DISTRICTS ET QUARTIERS")
    print("=" * 80)
    
    # Statistiques
    stats = {
        'provinces_traitees': 0,
        'districts_crees': 0,
        'quartiers_crees': 0,
        'erreurs': 0
    }
    
    # Récupérer toutes les provinces africaines
    provinces = Province.objects.select_related('pays').filter(
        pays__continent='Afrique'
    ).order_by('pays__nom', 'nom')
    
    total_provinces = provinces.count()
    print(f"\n📊 Total de provinces à traiter: {total_provinces}")
    print("=" * 80)
    
    pays_actuel = None
    
    for province in provinces:
        try:
            # Afficher le pays si changement
            if pays_actuel != province.pays.nom:
                pays_actuel = province.pays.nom
                print(f"\n🌍 {pays_actuel}")
                print("-" * 80)
            
            # Créer les districts
            districts = creer_districts_pour_province(province)
            
            if districts:
                stats['districts_crees'] += len(districts)
                print(f"   📍 {province.nom}: {len(districts)} districts créés", end='')
                
                # Créer les quartiers pour chaque district
                total_quartiers = 0
                for district in districts:
                    quartiers = creer_quartiers_pour_district(district)
                    total_quartiers += len(quartiers)
                    stats['quartiers_crees'] += len(quartiers)
                
                print(f" → {total_quartiers} quartiers")
            else:
                print(f"   ⚠️  {province.nom}: Districts déjà existants")
            
            stats['provinces_traitees'] += 1
            
            # Afficher progression tous les 50
            if stats['provinces_traitees'] % 50 == 0:
                print(f"\n   ✅ Progression: {stats['provinces_traitees']}/{total_provinces} provinces")
        
        except Exception as e:
            stats['erreurs'] += 1
            print(f"   ❌ Erreur pour {province.nom}: {e}")
            continue
    
    # Résumé final
    print("\n" + "=" * 80)
    print("✅ PEUPLEMENT TERMINÉ")
    print("=" * 80)
    print(f"Provinces traitées: {stats['provinces_traitees']}/{total_provinces}")
    print(f"Districts créés: {stats['districts_crees']}")
    print(f"Quartiers créés: {stats['quartiers_crees']}")
    print(f"Erreurs: {stats['erreurs']}")
    print("=" * 80)
    
    # Statistiques finales par pays
    print("\n📊 STATISTIQUES PAR PAYS:")
    print("=" * 80)
    
    pays_list = Pays.objects.filter(continent='Afrique').order_by('nom')
    
    for pays in pays_list:
        nb_provinces = Province.objects.filter(pays=pays).count()
        nb_districts = District.objects.filter(province__pays=pays).count()
        nb_quartiers = Quartier.objects.filter(district__province__pays=pays).count()
        
        if nb_provinces > 0:
            print(f"{pays.nom:35} | P:{nb_provinces:3} | D:{nb_districts:4} | Q:{nb_quartiers:5}")
    
    print("=" * 80)
    
    # Total global
    total_provinces = Province.objects.filter(pays__continent='Afrique').count()
    total_districts = District.objects.filter(province__pays__continent='Afrique').count()
    total_quartiers = Quartier.objects.filter(district__province__pays__continent='Afrique').count()
    
    print(f"\n🎯 TOTAL GLOBAL:")
    print(f"   Provinces: {total_provinces}")
    print(f"   Districts: {total_districts}")
    print(f"   Quartiers: {total_quartiers}")
    print(f"   TOTAL: {total_provinces + total_districts + total_quartiers} entités")
    print("=" * 80)

if __name__ == '__main__':
    main()
