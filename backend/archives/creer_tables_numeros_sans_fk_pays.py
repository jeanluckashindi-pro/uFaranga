#!/usr/bin/env python
"""
Script pour créer les tables de numéros de téléphone SANS foreign key vers pays
On utilisera pays_code_iso_2 au lieu de pays_id pour éviter les problèmes de permissions
"""
import os
import sys
import django
import psycopg2
import json

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
    print_step("CRÉATION TABLES NUMÉROS TÉLÉPHONE")
    
    # 1. Créer la table numeros_telephone (SANS FK vers pays)
    print("\n1. Création table numeros_telephone...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identite.numeros_telephone (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            
            -- Utilisateur
            utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id) ON DELETE CASCADE,
            
            -- Pays (code ISO au lieu de FK pour éviter problème de permissions)
            pays_code_iso_2 CHAR(2) NOT NULL,
            code_pays VARCHAR(10) NOT NULL,
            
            -- Numéro
            numero_national VARCHAR(20) NOT NULL,
            numero_complet VARCHAR(30) NOT NULL UNIQUE,
            numero_formate VARCHAR(30),
            
            -- Type et usage
            type_numero VARCHAR(20) DEFAULT 'MOBILE' CHECK (type_numero IN ('MOBILE', 'FIXE', 'VOIP')),
            usage VARCHAR(20) DEFAULT 'PERSONNEL' CHECK (usage IN ('PERSONNEL', 'PROFESSIONNEL', 'URGENCE')),
            est_principal BOOLEAN DEFAULT false,
            
            -- Vérification
            est_verifie BOOLEAN DEFAULT false,
            date_verification TIMESTAMP WITH TIME ZONE,
            methode_verification VARCHAR(50),
            code_verification_hash VARCHAR(255),
            tentatives_verification INTEGER DEFAULT 0,
            derniere_tentative_verification TIMESTAMP WITH TIME ZONE,
            
            -- Statut
            statut VARCHAR(20) DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'SUSPENDU', 'BLOQUE', 'SUPPRIME')),
            raison_statut TEXT,
            date_changement_statut TIMESTAMP WITH TIME ZONE,
            
            -- Sécurité
            nombre_connexions_reussies INTEGER DEFAULT 0,
            nombre_connexions_echouees INTEGER DEFAULT 0,
            derniere_connexion TIMESTAMP WITH TIME ZONE,
            derniere_connexion_ip INET,
            
            -- Opérateur
            operateur VARCHAR(100),
            type_ligne VARCHAR(20) CHECK (type_ligne IN ('PREPAYE', 'POSTPAYE', NULL)),
            
            -- Métadonnées
            date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_suppression TIMESTAMP WITH TIME ZONE,
            cree_par UUID,
            modifie_par UUID,
            metadonnees JSONB DEFAULT '{}'::jsonb
        )
    """)
    
    print_success("Table numeros_telephone créée")
    
    # Index pour numeros_telephone
    print("\n2. Création des index pour numeros_telephone...")
    
    index_numeros = [
        "CREATE INDEX IF NOT EXISTS idx_numeros_utilisateur ON identite.numeros_telephone(utilisateur_id)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_pays_code ON identite.numeros_telephone(pays_code_iso_2)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_complet ON identite.numeros_telephone(numero_complet)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_statut ON identite.numeros_telephone(statut)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_verifie ON identite.numeros_telephone(est_verifie)",
        "CREATE INDEX IF NOT EXISTS idx_numeros_principal ON identite.numeros_telephone(utilisateur_id, est_principal) WHERE est_principal = true",
    ]
    
    for query in index_numeros:
        cursor.execute(query)
        print_success("Index créé")
    
    # 3. Créer la table historique_numeros_telephone
    print("\n3. Création table historique_numeros_telephone...")
    
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
    print("\n4. Création des index pour historique...")
    
    index_historique = [
        "CREATE INDEX IF NOT EXISTS idx_historique_numero ON identite.historique_numeros_telephone(numero_telephone_id)",
        "CREATE INDEX IF NOT EXISTS idx_historique_utilisateur ON identite.historique_numeros_telephone(utilisateur_id)",
        "CREATE INDEX IF NOT EXISTS idx_historique_date ON identite.historique_numeros_telephone(date_action DESC)",
    ]
    
    for query in index_historique:
        cursor.execute(query)
        print_success("Index créé")
    
    # 5. Créer la table limites_numeros_par_pays (SANS FK vers pays)
    print("\n5. Création table limites_numeros_par_pays...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identite.limites_numeros_par_pays (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            pays_code_iso_2 CHAR(2) NOT NULL,
            type_utilisateur VARCHAR(20) NOT NULL REFERENCES identite.types_utilisateurs(code),
            nombre_max_numeros INTEGER NOT NULL DEFAULT 3,
            nombre_max_numeros_verifies INTEGER NOT NULL DEFAULT 2,
            autorise_numeros_etrangers BOOLEAN DEFAULT false,
            pays_autorises_codes CHAR(2)[],
            date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            CONSTRAINT uq_limite_pays_type UNIQUE (pays_code_iso_2, type_utilisateur)
        )
    """)
    
    print_success("Table limites_numeros_par_pays créée")
    
    # 6. Créer le trigger pour l'historique
    print("\n6. Création des triggers...")
    
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
        EXECUTE PROCEDURE identite.enregistrer_historique_numero()
    """)
    
    print_success("Triggers créés")
    
    # 7. Ajouter les commentaires
    print("\n7. Ajout des commentaires...")
    
    commentaires = [
        "COMMENT ON TABLE identite.numeros_telephone IS 'Numéros de téléphone des utilisateurs avec validation et limites'",
        "COMMENT ON COLUMN identite.numeros_telephone.numero_complet IS 'Numéro au format international (ex: +25762046725)'",
        "COMMENT ON COLUMN identite.numeros_telephone.est_principal IS 'Numéro principal de l''utilisateur (un seul par utilisateur)'",
        "COMMENT ON COLUMN identite.numeros_telephone.pays_code_iso_2 IS 'Code ISO du pays (ex: BI, RW, CD)'",
        "COMMENT ON TABLE identite.historique_numeros_telephone IS 'Historique de tous les changements sur les numéros'",
        "COMMENT ON TABLE identite.limites_numeros_par_pays IS 'Limites de numéros par pays et type d''utilisateur'",
    ]
    
    for comment in commentaires:
        cursor.execute(comment)
    
    print_success("Commentaires ajoutés")
    
    # 8. Mettre à jour les métadonnées des pays avec les infos de téléphonie
    print("\n8. Mise à jour des métadonnées des pays...")
    
    pays_data = [
        {
            'code_iso_2': 'BI',
            'metadata': {
                'telephonie': {
                    'code_telephonique': '+257',
                    'format_numero_national': 'XX XX XX XX',
                    'longueur_numero_min': 8,
                    'longueur_numero_max': 8,
                    'regex_validation': r'^[67]\d{7}$',
                    'exemples_numeros': ['+25762046725', '+25779123456'],
                    'operateurs': ['Econet', 'Lumitel', 'Smart']
                },
                'devise': {
                    'code': 'BIF',
                    'symbole': 'FBu',
                    'nom': 'Franc burundais'
                },
                'geographie': {
                    'continent': 'Afrique',
                    'sous_region': 'Afrique de l\'Est',
                    'capitale': 'Gitega'
                },
                'limites': {
                    'numeros_par_utilisateur': 3,
                    'transaction_journaliere': 5000000
                },
                'autorisations': {
                    'inscription': True,
                    'transactions': True,
                    'niveau_risque': 'NORMAL'
                }
            }
        },
        {
            'code_iso_2': 'RW',
            'metadata': {
                'telephonie': {
                    'code_telephonique': '+250',
                    'format_numero_national': 'XXX XXX XXX',
                    'longueur_numero_min': 9,
                    'longueur_numero_max': 9,
                    'regex_validation': r'^7\d{8}$',
                    'exemples_numeros': ['+250788123456', '+250722987654'],
                    'operateurs': ['MTN', 'Airtel']
                },
                'devise': {
                    'code': 'RWF',
                    'symbole': 'RF',
                    'nom': 'Franc rwandais'
                },
                'geographie': {
                    'continent': 'Afrique',
                    'sous_region': 'Afrique de l\'Est',
                    'capitale': 'Kigali'
                },
                'limites': {
                    'numeros_par_utilisateur': 3,
                    'transaction_journaliere': 10000000
                },
                'autorisations': {
                    'inscription': True,
                    'transactions': True,
                    'niveau_risque': 'NORMAL'
                }
            }
        },
        {
            'code_iso_2': 'CD',
            'metadata': {
                'telephonie': {
                    'code_telephonique': '+243',
                    'format_numero_national': 'XXX XXX XXX',
                    'longueur_numero_min': 9,
                    'longueur_numero_max': 9,
                    'regex_validation': r'^[89]\d{8}$',
                    'exemples_numeros': ['+243812345678', '+243998765432'],
                    'operateurs': ['Vodacom', 'Airtel', 'Orange']
                },
                'devise': {
                    'code': 'CDF',
                    'symbole': 'FC',
                    'nom': 'Franc congolais'
                },
                'geographie': {
                    'continent': 'Afrique',
                    'sous_region': 'Afrique Centrale',
                    'capitale': 'Kinshasa'
                },
                'limites': {
                    'numeros_par_utilisateur': 3,
                    'transaction_journaliere': 5000000
                },
                'autorisations': {
                    'inscription': True,
                    'transactions': True,
                    'niveau_risque': 'NORMAL'
                }
            }
        },
    ]
    
    for pays in pays_data:
        try:
            cursor.execute("""
                UPDATE localisation.pays
                SET metadonnees = %s::jsonb
                WHERE code_iso_2 = %s
            """, (json.dumps(pays['metadata']), pays['code_iso_2']))
            print_success(f"Métadonnées du pays {pays['code_iso_2']} mises à jour")
        except Exception as e:
            print_error(f"Erreur pays {pays['code_iso_2']}: {e}")
    
    # 9. Insérer des limites par défaut
    print("\n9. Insertion des limites par défaut...")
    
    cursor.execute("""
        INSERT INTO identite.limites_numeros_par_pays 
        (pays_code_iso_2, type_utilisateur, nombre_max_numeros, nombre_max_numeros_verifies)
        VALUES 
        ('BI', 'CLIENT', 3, 2),
        ('BI', 'AGENT', 5, 3),
        ('BI', 'MARCHAND', 5, 3),
        ('RW', 'CLIENT', 3, 2),
        ('RW', 'AGENT', 5, 3),
        ('CD', 'CLIENT', 3, 2)
        ON CONFLICT (pays_code_iso_2, type_utilisateur) DO NOTHING
    """)
    
    print_success("Limites par défaut insérées")
    
    # Commit final
    conn.commit()
    
    # Vérification
    print_step("VÉRIFICATION")
    
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
    
    cursor.execute("""
        SELECT 
            code_iso_2,
            nom,
            metadonnees->'telephonie'->>'code_telephonique' as code_tel,
            metadonnees->'devise'->>'code' as devise
        FROM localisation.pays
        WHERE code_iso_2 IN ('BI', 'RW', 'CD')
        ORDER BY nom
    """)
    
    print("\nPays configurés (métadonnées):")
    print(f"{'Code':<6} {'Nom':<40} {'Téléphone':<12} {'Devise':<6}")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"{row[0]:<6} {row[1]:<40} {row[2] or 'N/A':<12} {row[3] or 'N/A':<6}")
    
    cursor.execute("""
        SELECT 
            pays_code_iso_2,
            type_utilisateur,
            nombre_max_numeros
        FROM identite.limites_numeros_par_pays
        ORDER BY pays_code_iso_2, type_utilisateur
    """)
    
    print("\nLimites configurées:")
    print(f"{'Pays':<6} {'Type':<15} {'Max numéros':<12}")
    print("-" * 40)
    for row in cursor.fetchall():
        print(f"{row[0]:<6} {row[1]:<15} {row[2]:<12}")
    
    print_step("✓ SUCCÈS!")
    print("\nTables créées:")
    print("  ✓ identite.numeros_telephone")
    print("  ✓ identite.historique_numeros_telephone")
    print("  ✓ identite.limites_numeros_par_pays")
    print("\nProchaines étapes:")
    print("1. Créer les modèles Django pour les nouvelles tables")
    print("2. Créer les serializers et views pour l'API")
    print("3. Implémenter la validation des numéros")
    print("4. Créer les endpoints pour gérer les numéros")
    print("\nNote: Les infos de téléphonie sont stockées dans pays.metadonnees")
    print("Note: Utilisation de pays_code_iso_2 au lieu de FK pour éviter les problèmes de permissions")

except Exception as e:
    conn.rollback()
    print_error(f"ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    cursor.close()
    conn.close()
