#!/usr/bin/env python3
"""
Script pour charger les divisions administratives GADM pour les pays africains activés
(Burundi, Congo, RD Congo)
"""

import os
import requests
import psycopg2
from psycopg2.extras import execute_values
import geopandas as gpd
from pathlib import Path

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
}

# Pays à charger
PAYS_A_CHARGER = {
    'BDI': 'Burundi',
    'COG': 'Congo',
    'COD': 'Democratic Republic of the Congo'
}

GADM_BASE_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg"
DOWNLOAD_DIR = Path("gadm_data_africa")

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def download_gadm_data(country_code):
    """Télécharger les données GADM pour un pays"""
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    filename = f"gadm41_{country_code}.gpkg"
    filepath = DOWNLOAD_DIR / filename
    
    if filepath.exists():
        print(f"  ✓ Fichier déjà téléchargé: {filename}")
        return filepath
    
    url = f"{GADM_BASE_URL}/{filename}"
    print(f"  📥 Téléchargement depuis: {url}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  📊 Progression: {percent:.1f}%", end='', flush=True)
        
        print(f"\n  ✓ Téléchargement terminé: {filename}")
        return filepath
        
    except Exception as e:
        print(f"\n  ❌ Erreur lors du téléchargement: {e}")
        if filepath.exists():
            filepath.unlink()
        return None

def get_pays_mapping(conn, country_code):
    """Récupérer le mapping d'un pays"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT continent_code, region_code, sequence_number
        FROM localisation.pays_mapping
        WHERE code_iso3 = %s
    """, (country_code,))
    
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        return {
            'continent': result[0],
            'region': result[1],
            'sequence': result[2]
        }
    return None

def generate_division_id(code_iso3, continent, region, sequence):
    """Générer un division_id"""
    return f"UF-{code_iso3}-{continent}-{region}-{sequence:03d}"

def load_niveau1(conn, gpkg_file, country_code, mapping):
    """Charger les divisions de niveau 1"""
    cursor = conn.cursor()
    
    print(f"\n  📂 Chargement niveau 1 (Provinces/États)...")
    
    try:
        # Lire les données niveau 1
        gdf = gpd.read_file(gpkg_file, layer=f"ADM_ADM_1")
        
        if gdf.empty:
            print(f"  ⚠️  Aucune donnée niveau 1 trouvée")
            return 0
        
        print(f"  📊 {len(gdf)} divisions trouvées")
        
        # Récupérer le division_id du pays
        cursor.execute("""
            SELECT division_id 
            FROM localisation.divisions_administratives_niveau0
            WHERE gid_0 = %s
        """, (country_code,))
        
        result = cursor.fetchone()
        if not result:
            print(f"  ❌ Pays {country_code} non trouvé dans niveau0")
            return 0
            
        pays_division_id = result[0]
        
        # Préparer les données
        records = []
        for idx, row in gdf.iterrows():
            division_id = generate_division_id(
                country_code,
                mapping['continent'],
                mapping['region'],
                idx + 1
            )
            
            record = (
                row.get('GID_1'),
                row.get('GID_0'),
                row.get('COUNTRY'),
                row.get('NAME_1'),
                row.get('VARNAME_1'),
                row.get('NL_NAME_1'),
                row.get('TYPE_1'),
                row.get('ENGTYPE_1'),
                row.get('CC_1'),
                row.get('HASC_1'),
                row['geometry'].wkb if row['geometry'] is not None else None,
                division_id,
                pays_division_id,
                True,  # est_autorise
                True,  # est_actif
                True,  # affiche_par_defaut
                row.get('COUNTRY')  # nom_pays
            )
            records.append(record)
        
        # Insérer dans la base
        insert_query = """
            INSERT INTO localisation.divisions_administratives_niveau1 
            (gid_1, gid_0, pays, nom_1, nom_variante_1, nom_local_1, type_1, 
             type_anglais_1, code_1, hasc_1, geometrie, division_id, pays_division_id,
             est_autorise, est_actif, affiche_par_defaut, nom_pays)
            VALUES %s
        """
        
        execute_values(cursor, insert_query, records)
        conn.commit()
        
        print(f"  ✅ {len(records)} divisions niveau 1 chargées")
        return len(records)
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return 0
    finally:
        cursor.close()

def load_niveau2(conn, gpkg_file, country_code, mapping):
    """Charger les divisions de niveau 2"""
    cursor = conn.cursor()
    
    print(f"\n  📂 Chargement niveau 2 (Communes/Territoires)...")
    
    try:
        # Lire les données niveau 2
        gdf = gpd.read_file(gpkg_file, layer=f"ADM_ADM_2")
        
        if gdf.empty:
            print(f"  ⚠️  Aucune donnée niveau 2 trouvée")
            return 0
        
        print(f"  📊 {len(gdf)} divisions trouvées")
        
        # Récupérer le division_id du pays
        cursor.execute("""
            SELECT division_id 
            FROM localisation.divisions_administratives_niveau0
            WHERE gid_0 = %s
        """, (country_code,))
        
        result = cursor.fetchone()
        if not result:
            print(f"  ❌ Pays {country_code} non trouvé dans niveau0")
            return 0
            
        pays_division_id = result[0]
        
        # Récupérer les division_id des parents (niveau 1)
        cursor.execute("""
            SELECT gid_1, division_id 
            FROM localisation.divisions_administratives_niveau1
            WHERE gid_0 = %s
        """, (country_code,))
        
        parent_mapping = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Préparer les données
        records = []
        for idx, row in gdf.iterrows():
            division_id = generate_division_id(
                country_code,
                mapping['continent'],
                mapping['region'],
                idx + 1
            )
            
            parent_division_id = parent_mapping.get(row.get('GID_1'))
            
            record = (
                row.get('GID_2'),
                row.get('GID_0'),
                row.get('COUNTRY'),
                row.get('GID_1'),
                row.get('NAME_1'),
                row.get('NL_NAME_1'),
                row.get('NAME_2'),
                row.get('VARNAME_2'),
                row.get('NL_NAME_2'),
                row.get('TYPE_2'),
                row.get('ENGTYPE_2'),
                row.get('CC_2'),
                row.get('HASC_2'),
                row['geometry'].wkb if row['geometry'] is not None else None,
                division_id,
                pays_division_id,
                parent_division_id,
                True,  # est_autorise
                True,  # est_actif
                True,  # affiche_par_defaut
                row.get('COUNTRY')  # nom_pays
            )
            records.append(record)
        
        # Insérer dans la base
        insert_query = """
            INSERT INTO localisation.divisions_administratives_niveau2 
            (gid_2, gid_0, pays, gid_1, nom_1, nom_local_1, nom_2, nom_variante_2, 
             nom_local_2, type_2, type_anglais_2, code_2, hasc_2, geometrie, division_id, 
             pays_division_id, parent_division_id, est_autorise, est_actif, 
             affiche_par_defaut, nom_pays)
            VALUES %s
        """
        
        execute_values(cursor, insert_query, records)
        conn.commit()
        
        print(f"  ✅ {len(records)} divisions niveau 2 chargées")
        return len(records)
        
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return 0
    finally:
        cursor.close()

def process_country(country_code, country_name):
    """Traiter un pays"""
    print(f"\n{'='*70}")
    print(f"🌍 {country_name} ({country_code})")
    print(f"{'='*70}")
    
    # Télécharger les données
    gpkg_file = download_gadm_data(country_code)
    if not gpkg_file:
        return None
    
    # Connexion à la base
    conn = get_db_connection()
    
    # Récupérer le mapping
    mapping = get_pays_mapping(conn, country_code)
    if not mapping:
        print(f"  ❌ Pas de mapping trouvé pour {country_code}")
        conn.close()
        return None
    
    print(f"  ✓ Mapping: {mapping['continent']}-{mapping['region']}")
    
    # Charger les niveaux
    stats = {
        'country_code': country_code,
        'country_name': country_name,
        'niveau1': load_niveau1(conn, gpkg_file, country_code, mapping),
        'niveau2': load_niveau2(conn, gpkg_file, country_code, mapping)
    }
    
    conn.close()
    
    print(f"\n  ✅ Chargement terminé pour {country_name}")
    print(f"     - Niveau 1: {stats['niveau1']} divisions")
    print(f"     - Niveau 2: {stats['niveau2']} divisions")
    
    return stats

def main():
    print("="*70)
    print(" "*15 + "CHARGEMENT GADM - PAYS AFRICAINS")
    print("="*70)
    print(f"\nPays à charger: {', '.join(PAYS_A_CHARGER.values())}")
    
    all_stats = []
    
    for country_code, country_name in PAYS_A_CHARGER.items():
        stats = process_country(country_code, country_name)
        if stats:
            all_stats.append(stats)
    
    # Résumé final
    print("\n" + "="*70)
    print(" "*20 + "RÉSUMÉ FINAL")
    print("="*70)
    
    total_niveau1 = sum(s['niveau1'] for s in all_stats)
    total_niveau2 = sum(s['niveau2'] for s in all_stats)
    
    print(f"\n📊 Statistiques globales:")
    print(f"   - Pays traités: {len(all_stats)}")
    print(f"   - Total niveau 1: {total_niveau1} divisions")
    print(f"   - Total niveau 2: {total_niveau2} divisions")
    print(f"   - Total général: {total_niveau1 + total_niveau2} divisions")
    
    print("\n📋 Détails par pays:")
    for stats in all_stats:
        print(f"   {stats['country_name']} ({stats['country_code']}):")
        print(f"      - Niveau 1: {stats['niveau1']}")
        print(f"      - Niveau 2: {stats['niveau2']}")
    
    print("\n" + "="*70)
    print("✅ CHARGEMENT TERMINÉ")
    print("="*70)

if __name__ == '__main__':
    main()
