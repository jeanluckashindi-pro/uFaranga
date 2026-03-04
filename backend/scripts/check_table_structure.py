#!/usr/bin/env python3
"""
Script pour vérifier la structure des tables divisions_administratives
"""

import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
}

def check_table_structure(table_name):
    """Vérifier la structure d'une table"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print(f"Structure de la table: {table_name}")
    print(f"{'='*70}\n")
    
    cursor.execute(f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'localisation'
        AND table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    
    print(f"{'Colonne':<40} {'Type':<20} {'Nullable'}")
    print("-" * 70)
    
    for col_name, data_type, is_nullable in columns:
        print(f"{col_name:<40} {data_type:<20} {is_nullable}")
    
    cursor.close()
    conn.close()

def main():
    tables = [
        'divisions_administratives_niveau0',
        'divisions_administratives_niveau1',
        'divisions_administratives_niveau2'
    ]
    
    for table in tables:
        try:
            check_table_structure(table)
        except Exception as e:
            print(f"\n❌ Erreur pour {table}: {e}")

if __name__ == '__main__':
    main()
