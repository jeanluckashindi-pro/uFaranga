#!/usr/bin/env python3
"""
Script de vérification finale du chargement des divisions africaines
"""

import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def verify_african_countries():
    """Vérifier les pays africains activés"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("=" * 80)
    print(" " * 20 + "VÉRIFICATION FINALE - PAYS AFRICAINS ACTIVÉS")
    print("=" * 80)
    
    # Statistiques par pays
    cursor.execute("""
        SELECT 
            n0.division_id,
            n0.nom_pays,
            n0.gid_0,
            COUNT(DISTINCT n1.division_id) as nb_niveau1,
            COUNT(DISTINCT n2.division_id) as nb_niveau2,
            n0.est_actif,
            n0.est_autorise
        FROM localisation.divisions_administratives_niveau0 n0
        LEFT JOIN localisation.divisions_administratives_niveau1 n1 
            ON n0.division_id = n1.pays_division_id
        LEFT JOIN localisation.divisions_administratives_niveau2 n2 
            ON n0.division_id = n2.pays_division_id
        WHERE n0.gid_0 IN ('BDI', 'COG', 'COD')
        GROUP BY n0.division_id, n0.nom_pays, n0.gid_0, n0.est_actif, n0.est_autorise
        ORDER BY n0.nom_pays
    """)
    
    results = cursor.fetchall()
    
    print(f"\n{'Pays':<25} {'Division ID':<25} {'Niveau 1':<12} {'Niveau 2':<12} {'Statut'}")
    print("-" * 80)
    
    total_n1 = 0
    total_n2 = 0
    
    for row in results:
        division_id, nom_pays, gid_0, nb_n1, nb_n2, est_actif, est_autorise = row
        
        total_n1 += nb_n1
        total_n2 += nb_n2
        
        statut = "✅ Actif" if est_actif and est_autorise else "❌ Inactif"
        icon = "🟢" if nb_n1 > 0 and nb_n2 > 0 else "🔴"
        
        print(f"{icon} {nom_pays:<23} {division_id:<25} {nb_n1:<12} {nb_n2:<12} {statut}")
    
    print("-" * 80)
    print(f"{'TOTAL':<25} {'':<25} {total_n1:<12} {total_n2:<12}")
    
    # Exemples de divisions
    print("\n" + "=" * 80)
    print(" " * 25 + "EXEMPLES DE DIVISIONS CHARGÉES")
    print("=" * 80)
    
    for country_code, country_name in [('BDI', 'Burundi'), ('COG', 'Congo'), ('COD', 'RD Congo')]:
        print(f"\n🌍 {country_name} ({country_code})")
        print("-" * 60)
        
        # Niveau 1
        cursor.execute("""
            SELECT division_id, nom_1, type_1
            FROM localisation.divisions_administratives_niveau1
            WHERE gid_0 = %s
            ORDER BY nom_1
            LIMIT 5
        """, (country_code,))
        
        provinces = cursor.fetchall()
        if provinces:
            print(f"\n  📍 Niveau 1 (Provinces) - {len(provinces)} premiers:")
            for div_id, nom, type_div in provinces:
                print(f"     {div_id} - {nom} ({type_div})")
        
        # Niveau 2
        cursor.execute("""
            SELECT division_id, nom_2, type_2
            FROM localisation.divisions_administratives_niveau2
            WHERE gid_0 = %s
            ORDER BY nom_2
            LIMIT 5
        """, (country_code,))
        
        communes = cursor.fetchall()
        if communes:
            print(f"\n  📍 Niveau 2 (Communes/Territoires) - {len(communes)} premiers:")
            for div_id, nom, type_div in communes:
                print(f"     {div_id} - {nom} ({type_div})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ VÉRIFICATION TERMINÉE")
    print("=" * 80)

def main():
    try:
        verify_african_countries()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
