#!/usr/bin/env python
"""
Vérification rapide de la structure
"""
import psycopg

DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def main():
    print("=" * 50)
    print("VÉRIFICATION DE LA STRUCTURE")
    print("=" * 50)
    print()
    
    try:
        conn = psycopg.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 1. Tables
        print("1. Tables:")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'identite' 
              AND table_name IN ('utilisateurs', 'types_utilisateurs', 'niveaux_kyc', 'statuts_utilisateurs');
        """)
        nb_tables = cursor.fetchone()[0]
        print(f"   {nb_tables}/4 tables trouvées {'✓' if nb_tables == 4 else '✗'}")
        print()
        
        # 2. Foreign Keys importantes
        print("2. Foreign Keys (Relations):")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.key_column_usage
            WHERE table_schema = 'identite'
              AND table_name = 'utilisateurs'
              AND constraint_name IN (
                  'utilisateurs_type_utilisateur_fkey',
                  'utilisateurs_niveau_kyc_fkey',
                  'utilisateurs_statut_fkey'
              )
            ORDER BY column_name;
        """)
        fks = cursor.fetchall()
        for fk in fks:
            print(f"   ✓ {fk[0]}")
        print(f"   {len(fks)}/3 Foreign Keys trouvées {'✓' if len(fks) == 3 else '✗'}")
        print()
        
        # 3. Données
        print("3. Données:")
        cursor.execute("SELECT COUNT(*) FROM identite.types_utilisateurs;")
        nb_types = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM identite.niveaux_kyc;")
        nb_niveaux = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM identite.statuts_utilisateurs;")
        nb_statuts = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM identite.utilisateurs;")
        nb_users = cursor.fetchone()[0]
        
        print(f"   Types: {nb_types}/6 {'✓' if nb_types == 6 else '✗'}")
        print(f"   Niveaux KYC: {nb_niveaux}/4 {'✓' if nb_niveaux == 4 else '✗'}")
        print(f"   Statuts: {nb_statuts}/5 {'✓' if nb_statuts == 5 else '✗'}")
        print(f"   Utilisateurs: {nb_users}")
        print()
        
        # 4. Test jointure
        print("4. Test Jointure:")
        cursor.execute("""
            SELECT 
                u.courriel,
                tu.libelle as type,
                nk.libelle as niveau,
                su.libelle as statut
            FROM identite.utilisateurs u
            LEFT JOIN identite.types_utilisateurs tu ON u.type_utilisateur = tu.code
            LEFT JOIN identite.niveaux_kyc nk ON u.niveau_kyc = nk.niveau
            LEFT JOIN identite.statuts_utilisateurs su ON u.statut = su.code
            LIMIT 1;
        """)
        result = cursor.fetchone()
        if result:
            print(f"   Email: {result[0]}")
            print(f"   Type: {result[1]}")
            print(f"   Niveau: {result[2]}")
            print(f"   Statut: {result[3]}")
            print("   ✓ Jointure fonctionne")
        else:
            print("   ✗ Aucun utilisateur trouvé")
        print()
        
        # Résumé
        print("=" * 50)
        if nb_tables == 4 and len(fks) == 3 and nb_types == 6 and nb_niveaux == 4 and nb_statuts == 5:
            print("✓ STRUCTURE CORRECTE!")
            print("→ Vous pouvez redémarrer Django")
        else:
            print("✗ Problèmes détectés")
            if nb_tables != 4:
                print(f"  → Tables manquantes ({nb_tables}/4)")
            if len(fks) != 3:
                print(f"  → Foreign Keys manquantes ({len(fks)}/3)")
            if nb_types != 6:
                print(f"  → Types incorrects ({nb_types}/6)")
            if nb_niveaux != 4:
                print(f"  → Niveaux incorrects ({nb_niveaux}/4)")
            if nb_statuts != 5:
                print(f"  → Statuts incorrects ({nb_statuts}/5)")
        print("=" * 50)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ ERREUR: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
