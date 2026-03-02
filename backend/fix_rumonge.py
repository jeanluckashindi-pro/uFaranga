#!/usr/bin/env python
"""
Correction de la province de Rumonge avec données OpenStreetMap
"""
import requests
import json
import psycopg2

DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def get_rumonge_from_osm():
    """Récupère les frontières de Rumonge depuis Overpass API (OpenStreetMap)"""
    
    print("📥 Téléchargement des frontières de Rumonge depuis OpenStreetMap...")
    
    # Requête Overpass pour Rumonge
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:25];
    (
      relation["name"="Rumonge"]["admin_level"="4"]["boundary"="administrative"];
    );
    out geom;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('elements'):
            print(f"✅ Données trouvées: {len(data['elements'])} élément(s)")
            return data['elements'][0] if data['elements'] else None
        else:
            print("⚠️  Aucune donnée trouvée sur OpenStreetMap")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def osm_to_geojson(osm_element):
    """Convertit un élément OSM en GeoJSON"""
    
    if osm_element['type'] != 'relation':
        return None
    
    # Extraire les coordonnées des membres
    coordinates = []
    for member in osm_element.get('members', []):
        if member['type'] == 'way' and member.get('geometry'):
            way_coords = [[node['lon'], node['lat']] for node in member['geometry']]
            coordinates.append(way_coords)
    
    if not coordinates:
        return None
    
    # Créer le GeoJSON
    geojson = {
        'type': 'Polygon',
        'coordinates': coordinates
    }
    
    return geojson

def create_rumonge_from_bururi():
    """Crée Rumonge en prenant une partie de Bururi (approximation basée sur la géographie)"""
    
    print("\n📍 Création de Rumonge à partir de données géographiques...")
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Rumonge est au sud-ouest du Burundi, sur le lac Tanganyika
    # Coordonnées approximatives de la province
    rumonge_polygon = """
    POLYGON((
        29.2 -4.5,
        29.2 -3.7,
        29.6 -3.7,
        29.6 -4.5,
        29.2 -4.5
    ))
    """
    
    # Mettre à jour avec un polygone plus précis basé sur la position géographique
    cur.execute("""
        UPDATE localisation.provinces
        SET geometrie = ST_Multi(ST_GeomFromText(%s, 4326)),
            centre_geo = ST_Centroid(ST_GeomFromText(%s, 4326)),
            centre_latitude = ST_Y(ST_Centroid(ST_GeomFromText(%s, 4326))),
            centre_longitude = ST_X(ST_Centroid(ST_GeomFromText(%s, 4326)))
        WHERE code = 'BI-RM'
    """, (rumonge_polygon, rumonge_polygon, rumonge_polygon, rumonge_polygon))
    
    conn.commit()
    
    # Vérifier
    cur.execute("""
        SELECT 
            nom,
            ROUND(ST_Area(geometrie::geography)/1000000) as superficie_km2,
            ST_NPoints(geometrie) as nb_points,
            ST_AsText(centre_geo) as centre
        FROM localisation.provinces
        WHERE code = 'BI-RM'
    """)
    
    row = cur.fetchone()
    print(f"\n✅ Rumonge mise à jour:")
    print(f"   Nom: {row[0]}")
    print(f"   Superficie: {row[1]} km²")
    print(f"   Points: {row[2]}")
    print(f"   Centre: {row[3]}")
    
    cur.close()
    conn.close()

def main():
    print("=" * 70)
    print("CORRECTION DE LA PROVINCE DE RUMONGE")
    print("=" * 70)
    
    # Essayer d'abord OpenStreetMap
    osm_data = get_rumonge_from_osm()
    
    if osm_data:
        geojson = osm_to_geojson(osm_data)
        if geojson:
            print("✅ Données OSM converties en GeoJSON")
            
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            
            geom_json = json.dumps(geojson)
            cur.execute("""
                UPDATE localisation.provinces
                SET geometrie = ST_Multi(ST_GeomFromGeoJSON(%s)),
                    centre_geo = ST_Centroid(ST_GeomFromGeoJSON(%s)),
                    centre_latitude = ST_Y(ST_Centroid(ST_GeomFromGeoJSON(%s))),
                    centre_longitude = ST_X(ST_Centroid(ST_GeomFromGeoJSON(%s)))
                WHERE code = 'BI-RM'
            """, (geom_json, geom_json, geom_json, geom_json))
            
            conn.commit()
            cur.close()
            conn.close()
            
            print("✅ Rumonge mise à jour avec données OSM")
        else:
            print("⚠️  Impossible de convertir les données OSM")
            create_rumonge_from_bururi()
    else:
        print("\n⚠️  OpenStreetMap non disponible, utilisation de données approximatives")
        create_rumonge_from_bururi()
    
    print("\n" + "=" * 70)
    print("✅ CORRECTION TERMINÉE")
    print("=" * 70)

if __name__ == '__main__':
    main()
