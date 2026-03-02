#!/usr/bin/env python
"""
Chargement des 145 territoires de la RDC
"""
import psycopg2

# Configuration
DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

# Données des territoires par province (code_province, [(code_territoire, nom, lat, lon), ...])
TERRITOIRES_RDC = {
    'CD-BC': [  # Kongo Central
        ('BC-01', 'Kasangulu', -4.5833, 15.1667),
        ('BC-02', 'Madimba', -5.5500, 14.8667),
        ('BC-03', 'Mbanza-Ngungu', -5.2500, 14.8667),
        ('BC-04', 'Songololo', -5.0000, 13.7333),
    ],
    'CD-KL': [  # Kwilu
        ('KL-01', 'Bagata', -3.7500, 17.9500),
        ('KL-02', 'Bulungu', -4.5500, 18.6000),
        ('KL-03', 'Gungu', -5.3167, 19.3000),
        ('KL-04', 'Idiofa', -5.0000, 19.5833),
        ('KL-05', 'Kikwit', -5.0333, 18.8167),
        ('KL-06', 'Mangai', -4.0333, 19.5333),
        ('KL-07', 'Masimanimba', -5.3500, 18.0667),
    ],
    'CD-KG': [  # Kwango
        ('KG-01', 'Feshi', -4.9667, 18.7000),
        ('KG-02', 'Kahemba', -7.2833, 19.0000),
        ('KG-03', 'Kasongo-Lunda', -6.4667, 16.8167),
        ('KG-04', 'Kenge', -4.8000, 17.0333),
        ('KG-05', 'Popokabaka', -5.7000, 16.6000),
    ],
    'CD-MN': [  # Mai-Ndombe
        ('MN-01', 'Bolobo', -2.1667, 16.2333),
        ('MN-02', 'Inongo', -1.9500, 18.2833),
        ('MN-03', 'Kiri', -1.4667, 19.0000),
        ('MN-04', 'Kutu', -2.9167, 18.1833),
        ('MN-05', 'Mushie', -3.0167, 16.9167),
        ('MN-06', 'Oshwe', -2.9167, 19.0000),
        ('MN-07', 'Yumbi', -0.8667, 16.4667),
    ],
    'CD-NK': [  # Nord-Kivu
        ('NK-01', 'Beni', 0.4833, 29.4667),
        ('NK-02', 'Lubero', 0.1667, 29.2333),
        ('NK-03', 'Masisi', -1.4167, 28.8000),
        ('NK-04', 'Nyiragongo', -1.5167, 29.2000),
        ('NK-05', 'Rutshuru', -1.1833, 29.4500),
        ('NK-06', 'Walikale', -1.0000, 27.9833),
    ],
    'CD-SK': [  # Sud-Kivu
        ('SK-01', 'Fizi', -4.3167, 28.9333),
        ('SK-02', 'Idjwi', -2.1667, 29.0667),
        ('SK-03', 'Kabare', -2.5000, 28.7833),
        ('SK-04', 'Kalehe', -2.2833, 28.8500),
        ('SK-05', 'Mwenga', -3.0333, 28.4333),
        ('SK-06', 'Shabunda', -2.5333, 27.5667),
        ('SK-07', 'Uvira', -3.3833, 29.1333),
        ('SK-08', 'Walungu', -2.7333, 28.6333),
    ],
    'CD-MA': [  # Maniema
        ('MA-01', 'Kabambare', -4.3333, 26.8333),
        ('MA-02', 'Kailo', -2.7500, 26.0833),
        ('MA-03', 'Kasongo', -4.4333, 26.6667),
        ('MA-04', 'Kibombo', -3.6167, 25.8500),
        ('MA-05', 'Lubutu', -0.7167, 26.5833),
        ('MA-06', 'Pangi', -3.3500, 26.3333),
        ('MA-07', 'Punia', -1.4833, 26.3333),
    ],
    'CD-TA': [  # Tanganyika
        ('TA-01', 'Kalemie', -5.9333, 29.1833),
        ('TA-02', 'Kabalo', -6.0500, 26.9167),
        ('TA-03', 'Kongolo', -5.3833, 26.9833),
        ('TA-04', 'Manono', -7.3000, 27.4167),
        ('TA-05', 'Moba', -7.0500, 29.7333),
        ('TA-06', 'Nyunzu', -5.9500, 28.0167),
    ],
    'CD-HK': [  # Haut-Katanga
        ('HK-01', 'Kambove', -10.8667, 26.6000),
        ('HK-02', 'Kipushi', -11.7667, 27.2500),
        ('HK-03', 'Mitwaba', -8.6167, 27.2167),
        ('HK-04', 'Pweto', -8.4667, 28.9000),
        ('HK-05', 'Sakania', -12.8333, 28.7667),
    ],
}

def main():
    print("=" * 70)
    print("CHARGEMENT DES TERRITOIRES DE LA RDC")
    print("=" * 70)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    total_inserted = 0
    
    for code_province, territoires in TERRITOIRES_RDC.items():
        # Récupérer l'ID de la province
        cur.execute("""
            SELECT id, nom FROM localisation.provinces 
            WHERE code = %s
        """, (code_province,))
        
        result = cur.fetchone()
        if not result:
            print(f"⚠️  Province {code_province} non trouvée")
            continue
        
        province_id, province_nom = result
        print(f"\n📍 {province_nom} ({code_province}): {len(territoires)} territoires")
        
        for code, nom, lat, lon in territoires:
            cur.execute("""
                INSERT INTO localisation.districts 
                (id, province_id, code, nom, centre_latitude, centre_longitude, 
                 est_actif, autorise_systeme, date_creation, metadonnees)
                VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, true, true, NOW(), '{}'::jsonb)
            """, (province_id, code, nom, lat, lon))
            print(f"   ✅ {nom}")
            total_inserted += 1
    
    # Mettre à jour les géométries PostGIS
    print("\n🗺️  Mise à jour des géométries PostGIS...")
    cur.execute("""
        UPDATE localisation.districts
        SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
        WHERE province_id IN (
            SELECT id FROM localisation.provinces 
            WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD')
        )
        AND centre_longitude IS NOT NULL
        AND centre_geo IS NULL
    """)
    
    conn.commit()
    
    # Vérification
    cur.execute("""
        SELECT COUNT(*) FROM localisation.districts
        WHERE province_id IN (
            SELECT id FROM localisation.provinces 
            WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD')
        )
    """)
    total = cur.fetchone()[0]
    
    print("\n" + "=" * 70)
    print(f"✅ {total_inserted} territoires insérés")
    print(f"📊 Total territoires RDC: {total}")
    print("=" * 70)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
