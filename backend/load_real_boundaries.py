#!/usr/bin/env python
"""
Chargement des frontières réelles (polygones) pour Burundi et RDC
Source: Données simplifiées depuis Natural Earth et GADM
"""
import psycopg2
import requests
import json

DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def download_geojson(country_code):
    """Télécharge les données GeoJSON depuis une source publique"""
    # API publique pour les frontières administratives
    url = f"https://raw.githubusercontent.com/datasets/geo-countries/master/data/{country_code}.geojson"
    
    print(f"📥 Téléchargement des données pour {country_code}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Alternative: utiliser geojson.xyz
    url2 = f"https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_admin_0_countries.geojson"
    try:
        response = requests.get(url2, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Filtrer par code pays
            for feature in data['features']:
                if feature['properties'].get('ISO_A2') == country_code:
                    return {'type': 'FeatureCollection', 'features': [feature]}
    except:
        pass
    
    return None

def load_boundaries_from_web():
    """Charge les frontières depuis le web"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("=" * 70)
    print("CHARGEMENT DES FRONTIÈRES RÉELLES")
    print("=" * 70)
    
    # Essayer de télécharger les données
    for country_code, iso2 in [('burundi', 'BI'), ('congo-democratic-republic', 'CD')]:
        print(f"\n🌍 Traitement: {country_code}")
        
        geojson = download_geojson(country_code)
        if geojson:
            print(f"✅ Données téléchargées")
            # Mettre à jour la géométrie
            geom_json = json.dumps(geojson['features'][0]['geometry'])
            cur.execute("""
                UPDATE localisation.pays
                SET geometrie = ST_Multi(ST_GeomFromGeoJSON(%s))
                WHERE code_iso_2 = %s
            """, (geom_json, iso2))
            print(f"✅ Frontières mises à jour")
        else:
            print(f"⚠️  Impossible de télécharger les données")
    
    conn.commit()
    cur.close()
    conn.close()

def create_province_boundaries_from_points():
    """Crée des polygones approximatifs pour les provinces basés sur les points"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "=" * 70)
    print("CRÉATION DES ZONES PROVINCIALES")
    print("=" * 70)
    
    # Pour chaque province, créer un buffer autour du point central
    # C'est une approximation, mais mieux que rien
    
    print("\n📍 Burundi - Création de zones approximatives...")
    cur.execute("""
        UPDATE localisation.provinces pr
        SET geometrie = ST_Multi(
            ST_Buffer(
                centre_geo::geography,
                50000  -- 50 km de rayon pour les provinces
            )::geometry
        )
        WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI')
          AND centre_geo IS NOT NULL
          AND geometrie IS NULL
    """)
    bi_count = cur.rowcount
    print(f"✅ {bi_count} provinces du Burundi")
    
    print("\n📍 RDC - Création de zones approximatives...")
    cur.execute("""
        UPDATE localisation.provinces pr
        SET geometrie = ST_Multi(
            ST_Buffer(
                centre_geo::geography,
                100000  -- 100 km de rayon pour les provinces de la RDC (plus grandes)
            )::geometry
        )
        WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD')
          AND centre_geo IS NOT NULL
          AND geometrie IS NULL
    """)
    cd_count = cur.rowcount
    print(f"✅ {cd_count} provinces de la RDC")
    
    # Créer des zones pour les territoires/districts
    print("\n📍 Territoires - Création de zones approximatives...")
    cur.execute("""
        UPDATE localisation.districts d
        SET geometrie = ST_Multi(
            ST_Buffer(
                centre_geo::geography,
                30000  -- 30 km de rayon pour les territoires
            )::geometry
        )
        WHERE province_id IN (
            SELECT id FROM localisation.provinces 
            WHERE pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 IN ('BI', 'CD'))
        )
        AND centre_geo IS NOT NULL
        AND geometrie IS NULL
    """)
    terr_count = cur.rowcount
    print(f"✅ {terr_count} territoires")
    
    conn.commit()
    
    # Vérification
    print("\n" + "=" * 70)
    print("VÉRIFICATION")
    print("=" * 70)
    
    cur.execute("""
        SELECT 
            p.nom as pays,
            COUNT(pr.id) as nb_provinces,
            COUNT(pr.geometrie) as nb_avec_polygones,
            ROUND(AVG(ST_Area(pr.geometrie::geography)/1000000)::numeric, 0) as superficie_moy_km2
        FROM localisation.pays p
        LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
        WHERE p.code_iso_2 IN ('BI', 'CD')
        GROUP BY p.nom
        ORDER BY p.nom
    """)
    
    print("\n📊 Provinces:")
    for row in cur.fetchall():
        print(f"   {row[0]}: {row[1]} provinces, {row[2]} avec polygones, superficie moy: {row[3]} km²")
    
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(geometrie) as avec_polygones
        FROM localisation.districts
        WHERE province_id IN (
            SELECT id FROM localisation.provinces 
            WHERE pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 IN ('BI', 'CD'))
        )
    """)
    
    row = cur.fetchone()
    print(f"\n📊 Territoires: {row[0]} total, {row[1]} avec polygones")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ TERMINÉ!")
    print("=" * 70)
    print("\n💡 NOTE: Les polygones des provinces sont approximatifs (buffers circulaires).")
    print("   Pour des frontières exactes, il faut importer des fichiers shapefile officiels.")

if __name__ == '__main__':
    # Option 1: Essayer de télécharger depuis le web (peut échouer)
    # load_boundaries_from_web()
    
    # Option 2: Créer des zones approximatives (toujours fonctionne)
    create_province_boundaries_from_points()
