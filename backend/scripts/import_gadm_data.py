#!/usr/bin/env python
"""
Script pour importer les données géospatiales GADM (Global Administrative Areas)
dans la base de données uFaranga.

GADM fournit les découpages administratifs officiels pour tous les pays.
"""
import os
import sys
import django
import requests
import json
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Commune


def telecharger_gadm_data(code_iso3, niveau=2):
    """
    Télécharge les données GADM pour un pays donné.
    
    Args:
        code_iso3: Code ISO3 du pays (ex: 'BDI' pour Burundi)
        niveau: Niveau administratif (0=pays, 1=provinces, 2=districts, etc.)
    """
    url = f"https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{code_iso3}_{niveau}.json"
    print(f"Téléchargement depuis: {url}")
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement: {e}")
        return None


def importer_pays_gadm(code_iso3="BDI"):
    """Importe les données du pays depuis GADM niveau 0"""
    print(f"\n=== Import du pays {code_iso3} ===")
    
    data = telecharger_gadm_data(code_iso3, niveau=0)
    if not data:
        return None
    
    features = data.get('features', [])
    if not features:
        print("Aucune donnée trouvée")
        return None
    
    feature = features[0]
    props = feature['properties']
    geom = feature['geometry']
    
    # Calculer le centre et bbox depuis la géométrie
    coords = geom['coordinates']
    
    pays, created = Pays.objects.update_or_create(
        code_iso_3=props['GID_0'],
        defaults={
            'code_iso_2': props['GID_0'][:2],
            'nom': props['COUNTRY'],
            'nom_anglais': props['COUNTRY'],
            'geometrie_geojson': geom,
            'est_actif': True,
            'autorise_systeme': True,
        }
    )
    
    action = "créé" if created else "mis à jour"
    print(f"Pays {pays.nom} {action}")
    return pays


def importer_provinces_gadm(code_iso3="BDI"):
    """Importe les provinces depuis GADM niveau 1"""
    print(f"\n=== Import des provinces {code_iso3} ===")
    
    pays = Pays.objects.filter(code_iso_3=code_iso3).first()
    if not pays:
        print(f"Pays {code_iso3} non trouvé. Importez d'abord le pays.")
        return
    
    data = telecharger_gadm_data(code_iso3, niveau=1)
    if not data:
        return
    
    features = data.get('features', [])
    print(f"Trouvé {len(features)} provinces")
    
    for feature in features:
        props = feature['properties']
        geom = feature['geometry']
        
        province, created = Province.objects.update_or_create(
            pays=pays,
            code=props['GID_1'],
            defaults={
                'nom': props['NAME_1'],
                'geometrie_geojson': geom,
                'est_actif': True,
            }
        )
        
        action = "créée" if created else "mise à jour"
        print(f"  - Province {province.nom} {action}")


def importer_districts_gadm(code_iso3="BDI"):
    """Importe les districts depuis GADM niveau 2"""
    print(f"\n=== Import des districts {code_iso3} ===")
    
    data = telecharger_gadm_data(code_iso3, niveau=2)
    if not data:
        return
    
    features = data.get('features', [])
    print(f"Trouvé {len(features)} districts")
    
    for feature in features:
        props = feature['properties']
        geom = feature['geometry']
        
        # Trouver la province parente
        province = Province.objects.filter(code=props['GID_1']).first()
        if not province:
            print(f"  ! Province {props['GID_1']} non trouvée pour {props['NAME_2']}")
            continue
        
        district, created = District.objects.update_or_create(
            province=province,
            code=props['GID_2'],
            defaults={
                'nom': props['NAME_2'],
                'geometrie_geojson': geom,
                'est_actif': True,
            }
        )
        
        action = "créé" if created else "mis à jour"
        print(f"  - District {district.nom} ({province.nom}) {action}")


def importer_communes_gadm(code_iso3="BDI"):
    """Importe les communes depuis GADM niveau 3"""
    print(f"\n=== Import des communes {code_iso3} ===")
    
    data = telecharger_gadm_data(code_iso3, niveau=3)
    if not data:
        print("Niveau 3 non disponible pour ce pays")
        return
    
    features = data.get('features', [])
    print(f"Trouvé {len(features)} communes")
    
    count = 0
    for feature in features:
        props = feature['properties']
        geom = feature['geometry']
        
        # Trouver le district parent
        district = District.objects.filter(code=props['GID_2']).first()
        if not district:
            print(f"  ! District {props['GID_2']} non trouvé pour {props.get('NAME_3', 'N/A')}")
            continue
        
        # Calculer le centre approximatif depuis la géométrie
        # Pour simplifier, on utilise les coordonnées du premier point
        coords = geom['coordinates']
        centre_lat, centre_lon = 0, 0
        
        try:
            if geom['type'] == 'Polygon':
                centre_lon = sum(c[0] for c in coords[0]) / len(coords[0])
                centre_lat = sum(c[1] for c in coords[0]) / len(coords[0])
            elif geom['type'] == 'MultiPolygon':
                all_coords = [c for poly in coords for c in poly[0]]
                centre_lon = sum(c[0] for c in all_coords) / len(all_coords)
                centre_lat = sum(c[1] for c in all_coords) / len(all_coords)
        except:
            centre_lat, centre_lon = 0, 0
        
        commune, created = Commune.objects.update_or_create(
            district=district,
            code=props['GID_3'],
            defaults={
                'nom': props.get('NAME_3', 'Sans nom'),
                'centre_latitude': centre_lat if centre_lat != 0 else None,
                'centre_longitude': centre_lon if centre_lon != 0 else None,
                'est_actif': True,
                'metadonnees': {'geometrie': geom}  # Stocker la géométrie dans metadonnees
            }
        )
        
        count += 1
        if count % 100 == 0:
            print(f"  - {count} communes importées...")
    
    print(f"  Total: {count} communes importées")


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importer les données GADM')
    parser.add_argument('--pays', default='BDI', help='Code ISO3 du pays (défaut: BDI pour Burundi)')
    parser.add_argument('--niveau', type=int, choices=[0, 1, 2, 3], help='Niveau spécifique à importer')
    parser.add_argument('--tout', action='store_true', help='Importer tous les niveaux')
    
    args = parser.parse_args()
    
    print(f"Import des données GADM pour {args.pays}")
    print("=" * 60)
    
    if args.tout or args.niveau == 0:
        importer_pays_gadm(args.pays)
    
    if args.tout or args.niveau == 1:
        importer_provinces_gadm(args.pays)
    
    if args.tout or args.niveau == 2:
        importer_districts_gadm(args.pays)
    
    if args.tout or args.niveau == 3:
        importer_communes_gadm(args.pays)
    
    print("\n" + "=" * 60)
    print("Import terminé!")


if __name__ == '__main__':
    main()
