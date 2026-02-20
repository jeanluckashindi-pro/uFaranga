#!/usr/bin/env python
"""
Script pour améliorer la table pays et créer les tables de numéros de téléphone
"""
import os
import sys
import django
import psycopg2
from datetime import datetime

# Configuration Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname='ufaranga',
    user='ufaranga',
    password='12345',
    host='localhost',
    port='5432'
)
conn.autocommit = False
cursor = conn.cursor()

def print_step(message):
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✓ {message}")

def print_error(message):
    print(f"✗ {message}")

try:
    print_step("AMÉLIORATION TABLE PAYS")
    
    # 1. Ajouter les colonnes de téléphonie à la table pays
    print("\n1. Ajout des colonnes de téléphonie...")
    
    colonnes_telephonie = [
        ("code_telephonique", "VARCHAR(10)"),
        ("format_numero_national", "VARCHAR(50)"),
        ("longueur_numero_min", "INTEGER DEFAULT 8"),
        ("longueur_numero_max", "INTEGER DEFAULT 15"),
        ("regex_validation", "VARCHAR(200)"),
        ("exemples_numeros", "TEXT[]"),
        ("code_devise", "CHAR(3)"),
        ("symbole_devise", "VARCHAR(10)"),
        ("continent", "VARCHAR(50)"),
        ("sous_region", "VARCHAR(100)"),
        ("capitale", "VARCHAR(100)"),
        ("autorise_inscription", "BOOLEAN DEFAULT true"),
        ("autorise_transactions", "BOOLEAN DEFAULT true"),
        ("niveau_risque", "VARCHAR(20) DEFAULT 'NORMAL'"),
        ("limite_numeros_par_utilisateur", "INTEGER DEFAULT 3"),
        ("limite_transaction_journaliere", "NUMERIC(15,2)"),
    ]
    
    for colonne, type_sql in colonnes_telephonie:
        try:
            cursor.execute(f"""
                ALTER TABLE localisation.pays 
                ADD COLUMN IF NOT EXISTS {colonne} {type_sql}
            """)
            print_success(f"Colonne {colonne} ajoutée")
        except Exception as e:
            print_error(f"Erreur colonne {colonne}: {e}")
    
    conn.commit()
    print_success("Colonnes de téléphonie ajoutées")
    
    # 2. Créer les index
    print("\n2. Création des index...")
    
    index_queries = [
        "CREATE INDEX IF NOT EXISTS idx_pays_code_tel ON localisation.pays(code_telephonique)",
        "CREATE INDEX IF NOT EXISTS idx_pays_continent ON localisation.pays(continent)",
    ]
    
    for query in index_queries:
        try:
            cursor.execute(query)
            print_success(f"Index créé")
        except Exception as e:
            print_error(f"Erreur index: {e}")
    
    conn.commit()
    print_success("Index créés")
    
    # 3. Mettre à jour les données des pays
    print("\n3. Mise à jour des données des pays...")
    
    pays_data = [
        {
            'code_iso_2': 'BI',
            'nom': 'Burundi',
            'code_telephonique': '+257',
            'format_numero_national': 'XX XX XX XX',
            'longueur_numero_min': 8,
            'longueur_numero_max': 8,
            'regex_validation': r'^[67]\d{7}$',
            'exemples_numeros': ['+25762046725', '+25779123456'],
            'code_devise': 'BIF',
            'symbole_devise': 'FBu',
            'continent': 'Afrique',
            'sous_region': 'Afrique de l\'Est',
            'capitale': 'Gitega',
            'limite_numeros_par_utilisateur': 3,
            'limite_transaction_journaliere': 5000000
        },
        {
            'code_iso_2': 'RW',
            'nom': 'Rwanda',
            'code_telephonique': '+250',
            'format_numero_national': 'XXX XXX XXX',
            'longueur_numero_min': 9,
            'longueur_numero_max': 9,
            'regex_validation': r'^7\d{8}$',
            'exemples_numeros': ['+250788123456', '+250722987654'],
            'code_devise': 'RWF',
            'symbole_devise': 'RF',
            'continent': 'Afrique',
            'sous_region': 'Afrique de l\'Est',
            'capitale': 'Kigali',
            'limite_numeros_par_utilisateur': 3,
            'limite_transaction_journaliere': 10000000
        },
        {
            'code_iso_2': 'CD',
            'nom': 'République Démocratique du Congo',
            'code_telephonique': '+243',
            'format_numero_national': 'XXX XXX XXX',
            'longueur_numero_min': 9,
            'longueur_numero_max': 9,
            'regex_validation': r'^[89]\d{8}$',
            'exemples_numeros': ['+243812345678', '+243998765432'],
            'code_devise': 'CDF',
            'symbole_devise': 'FC',
            'continent': 'Afrique',
            'sous_region': 'Afrique Centrale',
            'capitale': 'Kinshasa',
            'limite_numeros_par_utilisateur': 3,
            'limite_transaction_journaliere': 5000000
        },
    ]
    
    for pays in pays_data:
        try:
            cursor.execute("""
                UPDATE localisation.pays
                SET 
                    code_telephonique = %s,
                    format_numero_national = %s,
                    longueur_numero_min = %s,
                    longueur_numero_max = %s,
                    regex_validation = %s,
                    exemples_numeros = %s,
                    code_devise = %s,
                    symbole_devise = %s,
                    continent = %s,
                    sous_region = %s,
                    capitale = %s,
                    limite_numeros_par_utilisateur = %s,
                    limite_transaction_journaliere = %s,
                    autorise_inscription = true,
                    autorise_transactions = true,
                    niveau_risque = 'NORMAL'
                WHERE code_iso_2 = %s
            """, (
                pays['code_telephonique'],
                pays['format_numero_national'],
                pays['longueur_numero_min'],
                pays['longueur_numero_max'],
                pays['regex_validation'],
                pays['exemples_numeros'],
                pays['code_devise'],
                pays['symbole_devise'],
                pays['continent'],
                pays['sous_region'],
                pays['capitale'],
                pays['limite_numeros_par_utilisateur'],
                pays['limite_transaction_journaliere'],
                pays['code_iso_2']
            ))
            print_success(f"Pays {pays['nom']} mis à jour")
        except Exception as e:
            print_error(f"Erreur pays {pays['nom']}: {e}")
    
    conn.commit()
    print_success("Données des pays mises à jour")
    
    print_step("CRÉATION TABLES NUMÉROS TÉLÉPHONE")
    
    # 4. Créer la table numeros_telephone
    print("\n4. Création table numeros_telephone...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identite.numeros_telephone (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id) ON DELETE CASCADE,
            pays_id UUID NOT NULL REFERENCES localisation.pays(id),
            code_pays VARCHAR(10) NOT NULL,
            numero_national VARCHAR(20) NOT NULL,
            numero_complet VARCHAR(30) NOT NULL UNIQUE,
            numero_formate VARCHAR(30),
            type_numero VARCHAR(20) DEFAULT 'MOBILE' CHECK (type_numero IN ('MOBILE', 'FIXE', 'VOIP')),
            usage VARCHAR(20) DEFAULT 'PERSONNEL' CHECK (usage IN ('PERSONNEL', 'PROFESSIONNEL', 'URGENCE')),
            est_principal BOOLEAN DEFAULT false,
            est_verifie BOOLEAN DEFAULT false,
            date_verification TIMESTAMP WITH TIME ZONE,
            methode_verification VARCHAR(50),
            code_verification_hash VARCHAR(255),
            tentatives_verification INTEGER DEFAULT 0,
            derniere_tentative_verification TIMESTAMP WITH TIME ZONE,
            statut VARCHAR(20) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'SUSPENDU', 'BLOQUE', 'SUPPRIME')),
            raison_statut TEXT,
            date_changement_statut TIMESTAMP WITH TIME ZONE,
            nombre_connexions_reussies INTEGER DEFAULT 0,
            nombre_connexions_echouees INTEGER DEFAULT 0,
            derniere_connexion TIMESTAMP WITH TIME ZONE,
            derniere_connexion_ip INET,
            operateur VARCHAR(100),
            type_ligne VARCHAR(20) CHECK (type_ligne IN ('PREPAYE', 'POSTPAYE', NULL)),
            date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_suppression TIMESTAMP WITH TIME ZONE,
            cree_par UUID,
            modifie_par UUID,
            metadonnees JSONB DEFAULT '{}'::jsonb,
            CONSTRAINT chk_numero_format CHECK (numero_complet ~ '^\+[1-9]\d{1,14}$')
        )
    """)
    
    print_success("Table numeros_telephone créée")
    
    # Index pour numeros_telephone
    index_numeros = [
        "CREATE INDEX IF NOT EXISTS idx_numeros_utilisateur ON identite.numeros_telephone(utilisateur_id)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_pays ON identite.numeros_telephone(pays_id)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_complet ON identite.numeros_telephone(numero_complet)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_statut ON identite.numeros_telephone(statut)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_verifie ON identite.numeros_telephone(est_verifie)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_principal ON identite.numeros_telephone(utilisateur_id, est_principal) WHERE est_principal = true",
    ]
    
    for query in index_numeros:
        cursor.execute(query)
    
    print_success("Index pour numeros_telephone créés")
    
    # 5. Créer la table historique_numeros_telephone
    print("\n5. Création table historique_numeros_telephone...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identite.historique_numeros_telephone (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            numero_telephone_id UUID NOT NULL REFERENCES identite.numeros_telephone(id),
            utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id),
            action VARCHAR(50) NOT NULL,
            ancien_statut VARCHAR(20),
            nouveau_statut VARCHAR(20),
            raison TEXT,
            details JSONB DEFAULT '{}'::jsonb,
            date_action TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            effectue_par UUID,
            adresse_ip INET,
            user_agent TEXT
        )
    """)
    
    print_success("Table historique_numeros_telephone créée")
    
    # Index pour historique
    index_historique = [
        "CREATE INDEX IF NOT EXISTS idx_historique_numero ON identite.historique_numeros_telephone(numero_telephone_id)",
        "CREATE INDEX IF NOT EXISTS idx_historique_utilisateur ON identite.historique_numeros_telephone(utilisateur_id)",
        "CREATE INDEX IF NOT EXISTS idx_historique_date ON identite.historique_numeros_telephone(date_action DESC)",
    ]
    
    for query in index_historique:
        cursor.execute(query)
    
    print_success("Index pour historique créés")
    
    # 6. Créer la table limites_numeros_par_pays
    print("\n6. Création table limites_numeros_par_pays...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identite.limites_numeros_par_pays (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            pays_id UUID NOT NULL REFERENCES localisation.pays(id),
            type_utilisateur VARCHAR(20) NOT NULL REFERENCES identite.types_utilisateurs(code),
            nombre_max_numeros INTEGER NOT NULL DEFAULT 3,
            nombre_max_numeros_verifies INTEGER NOT NULL DEFAULT 2,
            autorise_numeros_etrangers BOOLEAN DEFAULT false,
            pays_autorises UUID[],
            date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            CONSTRAINT uq_limite_pays_type UNIQUE (pays_id, type_utilisateur)
        )
    """)
    
    print_success("Table limites_numeros_par_pays créée")
    
    # 7. Créer le trigger pour l'historique
    print("\n7. Création des triggers...")
    
    cursor.execute("""
        CREATE OR REPLACE FUNCTION identite.enregistrer_historique_numero()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                INSERT INTO identite.historique_numeros_telephone
                (numero_telephone_id, utilisateur_id, action, nouveau_statut)
                VALUES (NEW.id, NEW.utilisateur_id, 'AJOUT', NEW.statut);
            ELSIF TG_OP = 'UPDATE' THEN
                IF OLD.statut != NEW.statut THEN
                    INSERT INTO identite.historique_numeros_telephone
                    (numero_telephone_id, utilisateur_id, action, ancien_statut, nouveau_statut)
                    VALUES (NEW.id, NEW.utilisateur_id, 'MODIFICATION', OLD.statut, NEW.statut);
                END IF;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    cursor.execute("""
        DROP TRIGGER IF EXISTS trg_historique_numero ON identite.numeros_telephone
    """)
    
    cursor.execute("""
        CREATE TRIGGER trg_historique_numero
        AFTER INSERT OR UPDATE ON identite.numeros_telephone
        FOR EACH ROW
        EXECUTE FUNCTION identite.enregistrer_historique_numero()
    """)
    
    print_success("Triggers créés")
    
    # 8. Ajouter les commentaires
    print("\n8. Ajout des commentaires...")
    
    commentaires = [
        "COMMENT ON TABLE identite.numeros_telephone IS 'Numéros de téléphone des utilisateurs avec validation et limites'",
        "COMMENT ON COLUMN identite.numeros_telephone.numero_complet IS 'Numéro au format international (ex: +25762046725)'",
        "COMMENT ON COLUMN identite.numeros_telephone.est_principal IS 'Numéro principal de l''utilisateur (un seul par utilisateur)'",
        "COMMENT ON TABLE identite.historique_numeros_telephone IS 'Historique de tous les changements sur les numéros'",
        "COMMENT ON TABLE identite.limites_numeros_par_pays IS 'Limites de numéros par pays et type d''utilisateur'",
    ]
    
    for comment in commentaires:
        cursor.execute(comment)
    
    print_success("Commentaires ajoutés")
    
    # Commit final
    conn.commit()
    
    # Vérification
    print_step("VÉRIFICATION")
    
    cursor.execute("""
        SELECT 
            code_iso_2,
            nom,
            code_telephonique,
            code_devise,
            limite_numeros_par_utilisateur
        FROM localisation.pays
        WHERE code_iso_2 IN ('BI', 'RW', 'CD')
        ORDER BY nom
    """)
    
    print("\nPays configurés:")
    print(f"{'Code':<6} {'Nom':<40} {'Téléphone':<12} {'Devise':<6} {'Limite':<6}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<6} {row[1]:<40} {row[2]:<12} {row[3]:<6} {row[4]:<6}")
    
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'identite'
        AND table_name LIKE '%numero%'
        ORDER BY table_name
    """)
    
    print("\nTables créées:")
    for row in cursor.fetchall():
        print(f"  ✓ identite.{row[0]}")
    
    print_step("✓ SUCCÈS!")
    print("\nProchaines étapes:")
    print("1. Créer les modèles Django pour les nouvelles tables")
    print("2. Créer les migrations Django")
    print("3. Créer les serializers et views pour l'API")
    print("4. Implémenter la validation des numéros")
    print("5. Créer les endpoints pour gérer les numéros")

except Exception as e:
    conn.rollback()
    print_error(f"ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    cursor.close()
    conn.close()
