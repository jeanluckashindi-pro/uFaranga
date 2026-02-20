-- =============================================================================
-- CRÉATION DE LA STRUCTURE POUR GESTION DES NUMÉROS DE TÉLÉPHONE
-- =============================================================================
-- Système bancaire professionnel avec validation et limites
-- =============================================================================

SET search_path TO identite, localisation, public;

\echo '========================================='
\echo 'CRÉATION STRUCTURE NUMÉROS TÉLÉPHONE'
\echo '========================================='
\echo ''

-- =============================================================================
-- 1. TABLE: numeros_telephone
-- =============================================================================

\echo '1. Création table numeros_telephone...'

CREATE TABLE IF NOT EXISTS identite.numeros_telephone (
    -- Identifiant
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Utilisateur
    utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id) ON DELETE CASCADE,
    
    -- Numéro
    pays_id UUID NOT NULL REFERENCES localisation.pays(id),
    code_pays VARCHAR(10) NOT NULL,
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
    metadonnees JSONB DEFAULT '{}'::jsonb,
    
    -- Contraintes
    CONSTRAINT chk_numero_format CHECK (numero_complet ~ '^\+[1-9]\d{1,14}$')
);

-- Index
CREATE INDEX IF NOT EXISTS idx_numeros_utilisateur ON identite.numeros_telephone(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_numeros_pays ON identite.numeros_telephone(pays_id);
CREATE INDEX IF NOT EXISTS idx_numeros_complet ON identite.numeros_telephone(numero_complet);
CREATE INDEX IF NOT EXISTS idx_numeros_statut ON identite.numeros_telephone(statut);
CREATE INDEX IF NOT EXISTS idx_numeros_verifie ON identite.numeros_telephone(est_verifie);
CREATE INDEX IF NOT EXISTS idx_numeros_principal ON identite.numeros_telephone(utilisateur_id, est_principal) WHERE est_principal = true;

\echo '✓ Table numeros_telephone créée'
\echo ''

-- =============================================================================
-- 2. TABLE: historique_numeros_telephone
-- =============================================================================

\echo '2. Création table historique_numeros_telephone...'

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
);

CREATE INDEX IF NOT EXISTS idx_historique_numero ON identite.historique_numeros_telephone(numero_telephone_id);
CREATE INDEX IF NOT EXISTS idx_historique_utilisateur ON identite.historique_numeros_telephone(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_historique_date ON identite.historique_numeros_telephone(date_action DESC);

\echo '✓ Table historique_numeros_telephone créée'
\echo ''

-- =============================================================================
-- 3. TABLE: limites_numeros_par_pays
-- =============================================================================

\echo '3. Création table limites_numeros_par_pays...'

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
);

\echo '✓ Table limites_numeros_par_pays créée'
\echo ''

-- =============================================================================
-- 4. TRIGGERS
-- =============================================================================

\echo '4. Création des triggers...'

-- Trigger: Enregistrer dans l'historique
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

DROP TRIGGER IF EXISTS trg_historique_numero ON identite.numeros_telephone;
CREATE TRIGGER trg_historique_numero
AFTER INSERT OR UPDATE ON identite.numeros_telephone
FOR EACH ROW
EXECUTE FUNCTION identite.enregistrer_historique_numero();

\echo '✓ Triggers créés'
\echo ''

-- =============================================================================
-- 5. COMMENTAIRES
-- =============================================================================

COMMENT ON TABLE identite.numeros_telephone IS 'Numéros de téléphone des utilisateurs avec validation et limites';
COMMENT ON COLUMN identite.numeros_telephone.numero_complet IS 'Numéro au format international (ex: +25762046725)';
COMMENT ON COLUMN identite.numeros_telephone.est_principal IS 'Numéro principal de l''utilisateur (un seul par utilisateur)';
COMMENT ON COLUMN identite.numeros_telephone.est_verifie IS 'Numéro vérifié par SMS/appel';

COMMENT ON TABLE identite.historique_numeros_telephone IS 'Historique de tous les changements sur les numéros';
COMMENT ON TABLE identite.limites_numeros_par_pays IS 'Limites de numéros par pays et type d''utilisateur';

\echo ''
\echo '========================================='
\echo '✓ STRUCTURE CRÉÉE AVEC SUCCÈS!'
\echo '========================================='
\echo ''
\echo 'Prochaines étapes:'
\echo '1. Ajouter les champs de téléphonie dans la table pays'
\echo '2. Migrer les numéros existants'
\echo '3. Configurer les limites par pays'
\echo ''
