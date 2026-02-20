-- =============================================================================
-- Script SQL pour CRÉER les tables de référence du module IDENTITE
-- =============================================================================
-- Usage: Exécuter ce script AVANT init_donnees_reference.sql
-- =============================================================================

-- Activer le schéma identite
SET search_path TO identite, public;

-- =============================================================================
-- 1. TABLE: TYPES D'UTILISATEURS
-- =============================================================================
CREATE TABLE IF NOT EXISTS identite.types_utilisateurs (
    code VARCHAR(20) PRIMARY KEY,
    libelle VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    ordre_affichage INTEGER DEFAULT 0,
    est_actif BOOLEAN DEFAULT true,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_types_utilisateurs_ordre ON identite.types_utilisateurs(ordre_affichage);
CREATE INDEX IF NOT EXISTS idx_types_utilisateurs_actif ON identite.types_utilisateurs(est_actif);

-- Commentaires
COMMENT ON TABLE identite.types_utilisateurs IS 'Types d''utilisateurs de la plateforme';
COMMENT ON COLUMN identite.types_utilisateurs.code IS 'Code unique du type (CLIENT, AGENT, etc.)';
COMMENT ON COLUMN identite.types_utilisateurs.libelle IS 'Libellé affiché';
COMMENT ON COLUMN identite.types_utilisateurs.ordre_affichage IS 'Ordre d''affichage dans les listes';

-- =============================================================================
-- 2. TABLE: NIVEAUX KYC
-- =============================================================================
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

-- Index
CREATE INDEX IF NOT EXISTS idx_niveaux_kyc_actif ON identite.niveaux_kyc(est_actif);

-- Commentaires
COMMENT ON TABLE identite.niveaux_kyc IS 'Niveaux de vérification KYC (Know Your Customer)';
COMMENT ON COLUMN identite.niveaux_kyc.niveau IS 'Niveau KYC (0=Non vérifié, 1=Basique, 2=Complet, 3=Premium)';
COMMENT ON COLUMN identite.niveaux_kyc.limite_transaction_journaliere IS 'Limite de transaction par jour en BIF';
COMMENT ON COLUMN identite.niveaux_kyc.limite_solde_maximum IS 'Solde maximum autorisé en BIF';
COMMENT ON COLUMN identite.niveaux_kyc.documents_requis IS 'Liste JSON des documents requis pour ce niveau';

-- =============================================================================
-- 3. TABLE: STATUTS UTILISATEURS
-- =============================================================================
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

-- Index
CREATE INDEX IF NOT EXISTS idx_statuts_utilisateurs_ordre ON identite.statuts_utilisateurs(ordre_affichage);
CREATE INDEX IF NOT EXISTS idx_statuts_utilisateurs_actif ON identite.statuts_utilisateurs(est_actif);

-- Commentaires
COMMENT ON TABLE identite.statuts_utilisateurs IS 'Statuts des comptes utilisateurs';
COMMENT ON COLUMN identite.statuts_utilisateurs.code IS 'Code unique du statut (ACTIF, SUSPENDU, etc.)';
COMMENT ON COLUMN identite.statuts_utilisateurs.couleur IS 'Couleur hexadécimale pour l''affichage (#28a745)';
COMMENT ON COLUMN identite.statuts_utilisateurs.permet_connexion IS 'Si false, l''utilisateur ne peut pas se connecter';
COMMENT ON COLUMN identite.statuts_utilisateurs.permet_transactions IS 'Si false, l''utilisateur ne peut pas effectuer de transactions';

-- =============================================================================
-- VÉRIFICATION DES TABLES CRÉÉES
-- =============================================================================

-- Lister les tables créées
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'identite' 
  AND table_name IN ('types_utilisateurs', 'niveaux_kyc', 'statuts_utilisateurs')
ORDER BY table_name;

-- Afficher la structure de chaque table
\d identite.types_utilisateurs
\d identite.niveaux_kyc
\d identite.statuts_utilisateurs

-- =============================================================================
-- FIN DU SCRIPT
-- =============================================================================

-- Message de succès
DO $$
BEGIN
    RAISE NOTICE '✓ Tables de référence créées avec succès!';
    RAISE NOTICE '→ Vous pouvez maintenant exécuter init_donnees_reference.sql';
END $$;
