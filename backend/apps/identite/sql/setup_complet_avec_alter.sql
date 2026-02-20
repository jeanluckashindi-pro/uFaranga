-- =============================================================================
-- SCRIPT COMPLET: Création + Données + Modification table utilisateurs
-- =============================================================================
-- Ce script fait TOUT en une seule fois:
-- 1. Crée les tables de référence
-- 2. Insère les données
-- 3. Modifie la table utilisateurs pour utiliser les Foreign Keys
-- =============================================================================

\echo '========================================='
\echo 'SETUP COMPLET MODULE IDENTITE'
\echo '========================================='
\echo ''

-- Activer le schéma identite
SET search_path TO identite, public;

-- =============================================================================
-- PARTIE 1: CRÉATION DES TABLES DE RÉFÉRENCE
-- =============================================================================

\echo '========================================='
\echo 'ÉTAPE 1: Création des tables de référence'
\echo '========================================='
\echo ''

-- TABLE: TYPES D'UTILISATEURS
CREATE TABLE IF NOT EXISTS identite.types_utilisateurs (
    code VARCHAR(20) PRIMARY KEY,
    libelle VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    ordre_affichage INTEGER DEFAULT 0,
    est_actif BOOLEAN DEFAULT true,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_types_utilisateurs_ordre ON identite.types_utilisateurs(ordre_affichage);
CREATE INDEX IF NOT EXISTS idx_types_utilisateurs_actif ON identite.types_utilisateurs(est_actif);

\echo '✓ Table types_utilisateurs créée'

-- TABLE: NIVEAUX KYC
CREATE TABLE IF NOT EXISTS identite.niveaux_kyc (
    niveau INTEGER PRIMARY KEY,
    libelle VARCHAR(50) NOT NULL,
    description TEXT DEFAULT '',
    limite_transaction_journaliere NUMERIC(15, 2),
    limite_solde_maximum NUMERIC(15, 2),
    documents_requis JSONB DEFAULT '[]'::jsonb,
    est_actif BOOLEAN DEFAULT true,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_niveaux_kyc_actif ON identite.niveaux_kyc(est_actif);

\echo '✓ Table niveaux_kyc créée'

-- TABLE: STATUTS UTILISATEURS
CREATE TABLE IF NOT EXISTS identite.statuts_utilisateurs (
    code VARCHAR(20) PRIMARY KEY,
    libelle VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    couleur VARCHAR(7) DEFAULT '#000000',
    permet_connexion BOOLEAN DEFAULT true,
    permet_transactions BOOLEAN DEFAULT true,
    ordre_affichage INTEGER DEFAULT 0,
    est_actif BOOLEAN DEFAULT true,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_statuts_utilisateurs_ordre ON identite.statuts_utilisateurs(ordre_affichage);
CREATE INDEX IF NOT EXISTS idx_statuts_utilisateurs_actif ON identite.statuts_utilisateurs(est_actif);

\echo '✓ Table statuts_utilisateurs créée'
\echo ''

-- =============================================================================
-- PARTIE 2: INSERTION DES DONNÉES
-- =============================================================================

\echo '========================================='
\echo 'ÉTAPE 2: Insertion des données'
\echo '========================================='
\echo ''

-- DONNÉES: TYPES D'UTILISATEURS
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES 
    ('CLIENT', 'Client', 'Client standard de la plateforme', 1, true, NOW(), NOW()),
    ('AGENT', 'Agent', 'Agent de service (dépôt, retrait, etc.)', 2, true, NOW(), NOW()),
    ('MARCHAND', 'Marchand', 'Commerçant acceptant les paiements', 3, true, NOW(), NOW()),
    ('ADMIN', 'Administrateur', 'Administrateur de la plateforme', 4, true, NOW(), NOW()),
    ('SUPER_ADMIN', 'Super Administrateur', 'Super administrateur avec tous les droits', 5, true, NOW(), NOW()),
    ('SYSTEME', 'Système', 'Compte système pour les opérations automatiques', 6, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    ordre_affichage = EXCLUDED.ordre_affichage,
    date_modification = NOW();

\echo '✓ 6 types d''utilisateurs insérés'

-- DONNÉES: NIVEAUX KYC
INSERT INTO identite.niveaux_kyc (niveau, libelle, description, limite_transaction_journaliere, limite_solde_maximum, documents_requis, est_actif, date_creation, date_modification)
VALUES 
    (0, 'Non vérifié', 'Aucune vérification effectuée', 0, 0, '[]'::jsonb, true, NOW(), NOW()),
    (1, 'Basique', 'Vérification basique (téléphone + email)', 50000, 100000, '["telephone", "email"]'::jsonb, true, NOW(), NOW()),
    (2, 'Complet', 'Vérification complète (pièce d''identité)', 500000, 2000000, '["telephone", "email", "piece_identite", "selfie"]'::jsonb, true, NOW(), NOW()),
    (3, 'Premium', 'Vérification premium (justificatif de domicile)', 5000000, 20000000, '["telephone", "email", "piece_identite", "selfie", "justificatif_domicile"]'::jsonb, true, NOW(), NOW())
ON CONFLICT (niveau) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    limite_transaction_journaliere = EXCLUDED.limite_transaction_journaliere,
    limite_solde_maximum = EXCLUDED.limite_solde_maximum,
    documents_requis = EXCLUDED.documents_requis,
    date_modification = NOW();

\echo '✓ 4 niveaux KYC insérés'

-- DONNÉES: STATUTS UTILISATEURS
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES 
    ('ACTIF', 'Actif', 'Compte actif et opérationnel', '#28a745', true, true, 1, true, NOW(), NOW()),
    ('EN_VERIFICATION', 'En vérification', 'Compte en cours de vérification KYC', '#ffc107', true, false, 2, true, NOW(), NOW()),
    ('SUSPENDU', 'Suspendu', 'Compte temporairement suspendu', '#fd7e14', false, false, 3, true, NOW(), NOW()),
    ('BLOQUE', 'Bloqué', 'Compte bloqué pour raisons de sécurité', '#dc3545', false, false, 4, true, NOW(), NOW()),
    ('FERME', 'Fermé', 'Compte définitivement fermé', '#6c757d', false, false, 5, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    couleur = EXCLUDED.couleur,
    permet_connexion = EXCLUDED.permet_connexion,
    permet_transactions = EXCLUDED.permet_transactions,
    ordre_affichage = EXCLUDED.ordre_affichage,
    date_modification = NOW();

\echo '✓ 5 statuts utilisateurs insérés'
\echo ''

-- =============================================================================
-- PARTIE 3: MODIFICATION DE LA TABLE UTILISATEURS
-- =============================================================================

\echo '========================================='
\echo 'ÉTAPE 3: Modification de la table utilisateurs'
\echo '========================================='
\echo ''

-- Sauvegarder les anciennes valeurs
ALTER TABLE identite.utilisateurs 
ADD COLUMN IF NOT EXISTS type_utilisateur_old VARCHAR(20),
ADD COLUMN IF NOT EXISTS niveau_kyc_old INTEGER,
ADD COLUMN IF NOT EXISTS statut_old VARCHAR(20);

-- Copier les valeurs actuelles
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identite' AND table_name = 'utilisateurs' AND column_name = 'type_utilisateur' AND data_type = 'character varying') THEN
        EXECUTE 'UPDATE identite.utilisateurs SET type_utilisateur_old = type_utilisateur';
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identite' AND table_name = 'utilisateurs' AND column_name = 'niveau_kyc' AND data_type = 'integer') THEN
        EXECUTE 'UPDATE identite.utilisateurs SET niveau_kyc_old = niveau_kyc';
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identite' AND table_name = 'utilisateurs' AND column_name = 'statut' AND data_type = 'character varying') THEN
        EXECUTE 'UPDATE identite.utilisateurs SET statut_old = statut';
    END IF;
END $$;

\echo '✓ Valeurs sauvegardées'

-- Supprimer les anciennes colonnes
ALTER TABLE identite.utilisateurs 
DROP COLUMN IF EXISTS type_utilisateur CASCADE,
DROP COLUMN IF EXISTS niveau_kyc CASCADE,
DROP COLUMN IF EXISTS statut CASCADE;

\echo '✓ Anciennes colonnes supprimées'

-- Ajouter les nouvelles colonnes avec Foreign Keys
ALTER TABLE identite.utilisateurs 
ADD COLUMN type_utilisateur VARCHAR(20) REFERENCES identite.types_utilisateurs(code) ON DELETE RESTRICT,
ADD COLUMN niveau_kyc INTEGER REFERENCES identite.niveaux_kyc(niveau) ON DELETE RESTRICT,
ADD COLUMN statut VARCHAR(20) REFERENCES identite.statuts_utilisateurs(code) ON DELETE RESTRICT;

\echo '✓ Nouvelles colonnes ajoutées avec Foreign Keys'

-- Restaurer les valeurs
UPDATE identite.utilisateurs 
SET 
    type_utilisateur = COALESCE(type_utilisateur_old, 'CLIENT'),
    niveau_kyc = COALESCE(niveau_kyc_old, 0),
    statut = COALESCE(statut_old, 'ACTIF');

\echo '✓ Valeurs restaurées'

-- Définir les valeurs par défaut et NOT NULL
ALTER TABLE identite.utilisateurs 
ALTER COLUMN type_utilisateur SET DEFAULT 'CLIENT',
ALTER COLUMN niveau_kyc SET DEFAULT 0,
ALTER COLUMN statut SET DEFAULT 'ACTIF',
ALTER COLUMN type_utilisateur SET NOT NULL,
ALTER COLUMN niveau_kyc SET NOT NULL,
ALTER COLUMN statut SET NOT NULL;

\echo '✓ Contraintes configurées'

-- Créer les index
CREATE INDEX IF NOT EXISTS idx_utilisateurs_type ON identite.utilisateurs(type_utilisateur);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_niveau_kyc ON identite.utilisateurs(niveau_kyc);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_statut ON identite.utilisateurs(statut);

\echo '✓ Index créés'

-- Nettoyer les colonnes temporaires
ALTER TABLE identite.utilisateurs 
DROP COLUMN IF EXISTS type_utilisateur_old,
DROP COLUMN IF EXISTS niveau_kyc_old,
DROP COLUMN IF EXISTS statut_old;

\echo '✓ Nettoyage effectué'
\echo ''

-- =============================================================================
-- VÉRIFICATION FINALE
-- =============================================================================

\echo '========================================='
\echo 'VÉRIFICATION FINALE'
\echo '========================================='
\echo ''

SELECT 
    (SELECT COUNT(*) FROM identite.types_utilisateurs) as types,
    (SELECT COUNT(*) FROM identite.niveaux_kyc) as niveaux,
    (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as statuts;

\echo ''
\echo '========================================='
\echo '✓ SETUP COMPLET TERMINÉ AVEC SUCCÈS!'
\echo '========================================='
\echo ''
\echo 'Tables créées: 3'
\echo 'Types utilisateurs: 6'
\echo 'Niveaux KYC: 4'
\echo 'Statuts: 5'
\echo 'Table utilisateurs: Modifiée avec Foreign Keys'
\echo ''
\echo 'Vous pouvez maintenant redémarrer Django'
\echo '========================================='
