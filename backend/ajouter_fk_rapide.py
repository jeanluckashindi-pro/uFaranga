#!/usr/bin/env python
"""
Script rapide pour ajouter les Foreign Keys
Usage: python ajouter_fk_rapide.py
"""
import psycopg

# Configuration
DB_CONFIG = {
    'dbname': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def main():
    print("Connexion à la base de données...")
    
    try:
        # Connexion
        conn = psycopg.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Connecté\n")
        
        # Supprimer les anciennes contraintes
        print("Suppression des anciennes contraintes...")
        cursor.execute("ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_type_utilisateur_fkey CASCADE;")
        cursor.execute("ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_niveau_kyc_fkey CASCADE;")
        cursor.execute("ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_statut_fkey CASCADE;")
        print("✓ Anciennes contraintes supprimées\n")
        
        # Ajouter les Foreign Keys
        print("Ajout des Foreign Keys...")
        
        print("  → type_utilisateur...")
        cursor.execute("""
            ALTER TABLE identite.utilisateurs 
            ADD CONSTRAINT utilisateurs_type_utilisateur_fkey 
            FOREIGN KEY (type_utilisateur) 
            REFERENCES identite.types_utilisateurs(code);
        """)
        
        print("  → niveau_kyc...")
        cursor.execute("""
            ALTER TABLE identite.utilisateurs 
            ADD CONSTRAINT utilisateurs_niveau_kyc_fkey 
            FOREIGN KEY (niveau_kyc) 
            REFERENCES identite.niveaux_kyc(niveau);
        """)
        
        print("  → statut...")
        cursor.execute("""
            ALTER TABLE identite.utilisateurs 
            ADD CONSTRAINT utilisateurs_statut_fkey 
            FOREIGN KEY (statut) 
            REFERENCES identite.statuts_utilisateurs(code);
        """)
        
        print("✓ Foreign Keys ajoutées\n")
        
        # Créer les index
        print("Création des index...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_utilisateurs_type ON identite.utilisateurs(type_utilisateur);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_utilisateurs_niveau_kyc ON identite.utilisateurs(niveau_kyc);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_utilisateurs_statut ON identite.utilisateurs(statut);")
        print("✓ Index créés\n")
        
        # Commit
        conn.commit()
        
        # Vérifier
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY'
              AND table_schema = 'identite'
              AND table_name = 'utilisateurs'
              AND constraint_name LIKE 'utilisateurs_%_fkey';
        """)
        count = cursor.fetchone()[0]
        
        print(f"Vérification: {count} Foreign Keys créées (3 attendues)")
        
        if count == 3:
            print("\n🎉 SUCCÈS! Structure correcte!")
            print("→ Vous pouvez maintenant redémarrer Django")
        else:
            print(f"\n⚠️ Problème: Seulement {count} Foreign Keys créées")
        
        # Fermer
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
