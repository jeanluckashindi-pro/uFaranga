#!/usr/bin/env python
"""
Import des données GADM (Global Administrative Areas)
Télécharge et importe les frontières administratives exactes pour Burundi et RDC
"""
import os
import sys
import requests
import zipfile
import json
from pathlib import Path
import psycopg2

DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

# URLs GADM pour télécharger les données (format GeoJSON)
GADM_URLS = {
    'BI': {
        'name': 'Burundi',
        'url': 'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_BDI_1.json',  # Niveau 1 = Provinces
        'level': 1
    },
    'CD': {
        'name': 'RDC',
        'url': 'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_COD_1.json',  # Niveau 1 = Provinces
        'level': 1
    }
}

def download_gadm_data(country_code, output_dir='gadm_data'):
    """Télécharge les données GADM pour un pays"""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    country_info = GADM_URLS.get(country_code)
    if not country_info:
        print(f"❌ Pays {country_code} non supporté")
        return None
    
    output_file = Path(output_dir) / f"gadm_{country_code}_level{country_info['level']}.json"
    
    # Si le fichier existe déjà, ne pas retélécharger
    if output_file.exists():
        print(f"✅ Fichier déjà téléchargé: {output_file}")
        return output_file
    
    print(f"📥 Téléchargement des données GADM pour {country_info['name']}...")
    print(f"   URL: {country_info['url']}")
    
    try:
        response = requests.get(country_info['url'], stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r   Progression: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ Téléchargement terminé: {output_file}")
        print(f"   Taille: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
        return output_file
        
    except Exception as e:
        print(f"\n❌ Erreur lors du téléchargement: {e}")
        if output_file.exists():
            output_file.unlink()
        return None

def import_gadm_to_postgres(geojson_file, country_code):
    """Importe les données GADM dans PostgreSQL"""
    
    print(f"\n📊 Import des données dans PostgreSQL...")
    
    # Lire le fichier GeoJSON
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = data.get('features', [])
    print(f"   Nombre de régions trouvées: {len(features)}")
    
    if not features:
        print("❌ Aucune donnée trouvée dans le fichier")
        return
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Récupérer l'ID du pays
    cur.execute("SELECT id FROM localisation.pays WHERE code_iso_2 = %s", (country_code,))
    result = cur.fetchone()
    if not result:
        print(f"❌ Pays {country_code} non trouvé dans la base")
        cur.close()
        conn.close()
        return
    
    pays_id = result[0]
    
    updated = 0
    not_found = []
    
    for feature in features:
        props = feature['properties']
        geometry = feature['geometry']
        
        # Nom de la province (GADM utilise NAME_1 pour le niveau 1)
        province_name = props.get('NAME_1', '').strip()
        
        if not province_name:
            continue
        
        # Convertir la géométrie en format WKT pour PostGIS
        geom_json = json.dumps(geometry)
        
        # Chercher la province correspondante dans la base
        # Essayer plusieurs variantes du nom
        province_variants = [
            province_name,
            province_name.replace('é', 'e').replace('É', 'E'),
            province_name.replace('û', 'u').replace('Û', 'U'),
            province_name.replace('ô', 'o').replace('Ô', 'O'),
        ]
        
        province_id = None
        for variant in province_variants:
            cur.execute("""
                SELECT id FROM localisation.provinces 
                WHERE pays_id = %s 
                AND (nom ILIKE %s OR nom ILIKE %s)
                LIMIT 1
            """, (pays_id, variant, f"%{variant}%"))
            
            result = cur.fetchone()
            if result:
                province_id = result[0]
                break
        
        if province_id:
            # Mettre à jour la géométrie
            try:
                cur.execute("""
                    UPDATE localisation.provinces
                    SET geometrie = ST_Multi(ST_GeomFromGeoJSON(%s))
                    WHERE id = %s
                """, (geom_json, province_id))
                
                # Calculer et mettre à jour le centre
                cur.execute("""
                    UPDATE localisation.provinces
                    SET centre_geo = ST_Centroid(geometrie),
                        centre_latitude = ST_Y(ST_Centroid(geometrie)),
                        centre_longitude = ST_X(ST_Centroid(geometrie))
                    WHERE id = %s
                """, (province_id,))
                
                updated += 1
                print(f"   ✅ {province_name}")
            except Exception as e:
                print(f"   ⚠️  Erreur pour {province_name}: {e}")
        else:
            not_found.append(province_name)
            print(f"   ⚠️  Province non trouvée: {province_name}")
    
    conn.commit()
    
    print(f"\n📊 Résumé:")
    print(f"   ✅ {updated} provinces mises à jour")
    if not_found:
        print(f"   ⚠️  {len(not_found)} provinces non trouvées:")
        for name in not_found:
            print(f"      - {name}")
    
    # Vérification finale
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(geometrie) as avec_geometrie,
            ROUND(AVG(ST_Area(geometrie::geography)/1000000)::numeric, 0) as superficie_moy
        FROM localisation.provinces
        WHERE pays_id = %s
    """, (pays_id,))
    
    row = cur.fetchone()
    print(f"\n📈 Statistiques finales:")
    print(f"   Total provinces: {row[0]}")
    print(f"   Avec géométrie: {row[1]}")
    print(f"   Superficie moyenne: {row[2]} km²")
    
    cur.close()
    conn.close()

def main():
    print("=" * 70)
    print("IMPORT DES DONNÉES GADM - FRONTIÈRES ADMINISTRATIVES EXACTES")
    print("=" * 70)
    print()
    
    # Télécharger et importer pour chaque pays
    for country_code in ['BI', 'CD']:
        country_name = GADM_URLS[country_code]['name']
        
        print(f"\n{'=' * 70}")
        print(f"🌍 {country_name} ({country_code})")
        print("=" * 70)
        
        # Télécharger
        geojson_file = download_gadm_data(country_code)
        
        if geojson_file:
            # Importer
            import_gadm_to_postgres(geojson_file, country_code)
        else:
            print(f"❌ Impossible de traiter {country_name}")
    
    print("\n" + "=" * 70)
    print("✅ IMPORT TERMINÉ!")
    print("=" * 70)
    print("\n💡 Les provinces ont maintenant leurs frontières administratives exactes")
    print("   Source: GADM (Global Administrative Areas) v4.1")

if __name__ == '__main__':
    main()
