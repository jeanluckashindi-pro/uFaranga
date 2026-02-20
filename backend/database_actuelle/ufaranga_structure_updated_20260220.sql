--
-- PostgreSQL database dump - STRUCTURE MISE À JOUR
-- Date: 2026-02-20
-- Description: Structure complète avec configuration dynamique
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

-- ============================================================================
-- CRÉATION DES SCHÉMAS
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS audit;
COMMENT ON SCHEMA audit IS 'Audit et traçabilité - TABLES IMMUABLES (APPEND-ONLY)';

CREATE SCHEMA IF NOT EXISTS bancaire;
COMMENT ON SCHEMA bancaire IS 'Intégration avec le système bancaire - Comptes réels et mouvements';

CREATE SCHEMA IF NOT EXISTS commission;
COMMENT ON SCHEMA commission IS 'Commissions, frais et rémunérations';

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'KYC, AML, documents et vérifications réglementaires';

CREATE SCHEMA IF NOT EXISTS configuration;
COMMENT ON SCHEMA configuration IS 'Configuration système et données de référence';

CREATE SCHEMA IF NOT EXISTS notification;
COMMENT ON SCHEMA notification IS 'Notifications et alertes';

CREATE SCHEMA IF NOT EXISTS portefeuille;
COMMENT ON SCHEMA portefeuille IS 'Portefeuilles, comptes virtuels et soldes';

CREATE SCHEMA IF NOT EXISTS transaction;
COMMENT ON SCHEMA transaction IS 'Transactions et mouvements de fonds';


-- ============================================================================
-- PARTIE 1: DEVISES ET TAUX DE CHANGE
-- ============================================================================

-- Table des devises
CREATE TABLE portefeuille.devises (
    code_devise VARCHAR(3) PRIMARY KEY,
    nom_devise VARCHAR(100) NOT NULL,
    symbole VARCHAR(10) NOT NULL,
    decimales INTEGER NOT NULL DEFAULT 2,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    pays_principal VARCHAR(2),
    ordre_affichage INTEGER DEFAULT 0,
    metadonnees JSONB DEFAULT '{}',
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_le TIMESTAMP
);

COMMENT ON TABLE portefeuille.devises IS 'Liste des devises supportées par le système';

-- Table des taux de change
CREATE TABLE portefeuille.taux_change (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    devise_source VARCHAR(3) NOT NULL REFERENCES portefeuille.devises(code_devise),
    devise_cible VARCHAR(3) NOT NULL REFERENCES portefeuille.devises(code_devise),
    taux DECIMAL(20, 8) NOT NULL CHECK (taux > 0),
    taux_inverse DECIMAL(20, 8),
    marge_achat DECIMAL(5, 4) DEFAULT 0.0000,
    marge_vente DECIMAL(5, 4) DEFAULT 0.0000,
    taux_achat DECIMAL(20, 8),
    taux_vente DECIMAL(20, 8),
    source VARCHAR(100),
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    date_debut_validite TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_le TIMESTAMP,
    CONSTRAINT unique_paire_devises UNIQUE (devise_source, devise_cible, date_debut_validite),
    CONSTRAINT pas_meme_devise CHECK (devise_source != devise_cible)
);

COMMENT ON TABLE portefeuille.taux_change IS 'Taux de change entre devises avec marges';

-- Table historique des taux (IMMUABLE)
CREATE TABLE audit.historique_taux_change (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    taux_change_id UUID NOT NULL,
    devise_source VARCHAR(3) NOT NULL,
    devise_cible VARCHAR(3) NOT NULL,
    ancien_taux DECIMAL(20, 8),
    nouveau_taux DECIMAL(20, 8) NOT NULL,
    action VARCHAR(20) NOT NULL,
    qui_utilisateur_id UUID,
    qui_nom VARCHAR(255),
    quand TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quoi TEXT NOT NULL,
    comment VARCHAR(50) NOT NULL,
    pourquoi TEXT,
    adresse_ip INET,
    user_agent TEXT,
    donnees_avant JSONB,
    donnees_apres JSONB
);

COMMENT ON TABLE audit.historique_taux_change IS 'Historique IMMUABLE des changements de taux';


-- ============================================================================
-- PARTIE 2: CONFIGURATION DYNAMIQUE
-- ============================================================================

-- Table: Configuration des Plafonds
CREATE TABLE configuration.plafonds_configuration (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    niveau_kyc INTEGER NOT NULL CHECK (niveau_kyc >= 0 AND niveau_kyc <= 3),
    type_utilisateur VARCHAR(20) NOT NULL CHECK (type_utilisateur IN ('CLIENT', 'AGENT', 'MARCHAND', 'ADMIN')),
    code_devise VARCHAR(3) NOT NULL,
    montant_max_transaction DECIMAL(20, 2) NOT NULL DEFAULT 0,
    montant_max_journalier DECIMAL(20, 2) NOT NULL DEFAULT 0,
    montant_max_mensuel DECIMAL(20, 2) NOT NULL DEFAULT 0,
    solde_maximum DECIMAL(20, 2) DEFAULT NULL,
    nombre_max_transactions_jour INTEGER DEFAULT NULL,
    date_debut_validite TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP DEFAULT NULL,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    priorite INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP,
    CONSTRAINT unique_plafond UNIQUE (niveau_kyc, type_utilisateur, code_devise, date_debut_validite)
);

COMMENT ON TABLE configuration.plafonds_configuration IS 'Configuration dynamique des plafonds par KYC, type utilisateur et devise';

CREATE INDEX idx_plafonds_actifs ON configuration.plafonds_configuration(niveau_kyc, type_utilisateur, code_devise) 
WHERE est_actif = TRUE;

-- Table: Règles Métier
CREATE TABLE configuration.regles_metier (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code_regle VARCHAR(100) NOT NULL UNIQUE,
    nom_regle VARCHAR(200) NOT NULL,
    description TEXT,
    categorie VARCHAR(50) NOT NULL,
    type_utilisateur VARCHAR(20),
    code_devise VARCHAR(3),
    valeur JSONB NOT NULL,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    priorite INTEGER NOT NULL DEFAULT 0,
    metadonnees JSONB DEFAULT '{}',
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP
);

COMMENT ON TABLE configuration.regles_metier IS 'Règles métier configurables stockées en JSON pour flexibilité maximale';

CREATE INDEX idx_regles_actives ON configuration.regles_metier(code_regle) WHERE est_actif = TRUE;
CREATE INDEX idx_regles_categorie ON configuration.regles_metier(categorie);
CREATE INDEX idx_regles_valeur ON configuration.regles_metier USING GIN(valeur);

-- Table: Configuration des Frais
CREATE TABLE configuration.frais_configuration (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type_transaction VARCHAR(50) NOT NULL,
    type_utilisateur_source VARCHAR(20),
    type_utilisateur_destination VARCHAR(20),
    code_devise VARCHAR(3) NOT NULL,
    montant_min DECIMAL(20, 2) NOT NULL DEFAULT 0,
    montant_max DECIMAL(20, 2),
    type_frais VARCHAR(20) NOT NULL CHECK (type_frais IN ('FIXE', 'POURCENTAGE', 'PALIER')),
    valeur_frais DECIMAL(10, 4) NOT NULL,
    frais_min DECIMAL(20, 2) DEFAULT 0,
    frais_max DECIMAL(20, 2),
    qui_paie VARCHAR(20) NOT NULL DEFAULT 'SOURCE' CHECK (qui_paie IN ('SOURCE', 'DESTINATION', 'PARTAGE')),
    pourcentage_source DECIMAL(5, 2) DEFAULT 100.00,
    date_debut_validite TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP DEFAULT NULL,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    priorite INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP
);

COMMENT ON TABLE configuration.frais_configuration IS 'Configuration des frais par type de transaction avec paliers de montants';

CREATE INDEX idx_frais_actifs ON configuration.frais_configuration(type_transaction, code_devise) 
WHERE est_actif = TRUE;

-- Table: Types de Transactions
CREATE TABLE configuration.types_transaction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code_type VARCHAR(50) NOT NULL UNIQUE,
    nom_type VARCHAR(100) NOT NULL,
    description TEXT,
    necessite_compte_source BOOLEAN NOT NULL DEFAULT TRUE,
    necessite_compte_destination BOOLEAN NOT NULL DEFAULT FALSE,
    impacte_solde_source VARCHAR(20) CHECK (impacte_solde_source IN ('DEBIT', 'CREDIT', 'AUCUN')),
    impacte_solde_destination VARCHAR(20) CHECK (impacte_solde_destination IN ('DEBIT', 'CREDIT', 'AUCUN')),
    types_utilisateurs_autorises JSONB NOT NULL DEFAULT '["CLIENT", "AGENT", "MARCHAND"]',
    necessite_2fa BOOLEAN NOT NULL DEFAULT FALSE,
    necessite_validation_admin BOOLEAN NOT NULL DEFAULT FALSE,
    montant_min DECIMAL(20, 2) DEFAULT 0,
    montant_max DECIMAL(20, 2),
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    icone VARCHAR(50),
    couleur VARCHAR(20),
    ordre_affichage INTEGER DEFAULT 0,
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP
);

COMMENT ON TABLE configuration.types_transaction IS 'Types de transactions configurables avec comportements et autorisations';

CREATE INDEX idx_types_actifs ON configuration.types_transaction(code_type) WHERE est_actif = TRUE;

-- Table: Devises Autorisées
CREATE TABLE configuration.devises_autorisees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type_utilisateur VARCHAR(20) NOT NULL,
    code_devise VARCHAR(3) NOT NULL,
    nombre_max_comptes INTEGER NOT NULL DEFAULT 1,
    peut_creer_compte BOOLEAN NOT NULL DEFAULT TRUE,
    peut_recevoir BOOLEAN NOT NULL DEFAULT TRUE,
    peut_envoyer BOOLEAN NOT NULL DEFAULT TRUE,
    est_actif BOOLEAN NOT NULL DEFAULT TRUE,
    date_debut_validite TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_fin_validite TIMESTAMP DEFAULT NULL,
    description TEXT,
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP,
    CONSTRAINT unique_devise_type UNIQUE (type_utilisateur, code_devise)
);

COMMENT ON TABLE configuration.devises_autorisees IS 'Devises autorisées par type d''utilisateur avec limites de comptes';

CREATE INDEX idx_devises_autorisees ON configuration.devises_autorisees(type_utilisateur, code_devise) 
WHERE est_actif = TRUE;


-- ============================================================================
-- PARTIE 3: BANQUES ET COMPTES
-- ============================================================================

-- Table: Banques Partenaires
CREATE TABLE bancaire.banques_partenaires (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code_banque VARCHAR(20) NOT NULL UNIQUE,
    nom_banque VARCHAR(200) NOT NULL,
    nom_court VARCHAR(50),
    code_swift VARCHAR(11),
    code_bic VARCHAR(11),
    pays VARCHAR(2) NOT NULL,
    adresse TEXT,
    telephone VARCHAR(50),
    email VARCHAR(100),
    site_web VARCHAR(200),
    api_endpoint VARCHAR(500),
    api_key_encrypted TEXT,
    api_version VARCHAR(20),
    timeout_secondes INTEGER DEFAULT 30,
    statut VARCHAR(20) NOT NULL DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'INACTIF', 'MAINTENANCE', 'SUSPENDU')),
    metadonnees JSONB DEFAULT '{}',
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP
);

COMMENT ON TABLE bancaire.banques_partenaires IS 'Banques partenaires avec configuration API';

CREATE INDEX idx_banques_actives ON bancaire.banques_partenaires(code_banque) WHERE statut = 'ACTIF';

-- Table: Comptes Bancaires Réels
CREATE TABLE bancaire.comptes_bancaires_reels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    banque_id UUID NOT NULL REFERENCES bancaire.banques_partenaires(id),
    numero_compte VARCHAR(50) NOT NULL,
    iban VARCHAR(34),
    code_swift VARCHAR(11),
    titulaire_nom VARCHAR(255) NOT NULL,
    titulaire_id UUID NOT NULL,
    type_compte VARCHAR(20) NOT NULL CHECK (type_compte IN ('COURANT', 'EPARGNE', 'MOBILE')),
    devise VARCHAR(3) NOT NULL,
    statut VARCHAR(20) NOT NULL DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'SUSPENDU', 'BLOQUE', 'FERME')),
    date_ouverture DATE NOT NULL DEFAULT CURRENT_DATE,
    date_fermeture DATE,
    metadonnees JSONB DEFAULT '{}',
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP,
    CONSTRAINT unique_compte_banque UNIQUE (banque_id, numero_compte)
);

COMMENT ON TABLE bancaire.comptes_bancaires_reels IS 'Comptes réels dans les banques partenaires';

CREATE INDEX idx_comptes_reels_titulaire ON bancaire.comptes_bancaires_reels(titulaire_id);
CREATE INDEX idx_comptes_reels_statut ON bancaire.comptes_bancaires_reels(statut);

-- Table: Comptes Virtuels (Portefeuilles)
CREATE TABLE portefeuille.comptes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_compte VARCHAR(50) NOT NULL UNIQUE,
    utilisateur_id UUID NOT NULL,
    compte_bancaire_reel_id UUID REFERENCES bancaire.comptes_bancaires_reels(id),
    numero_telephone VARCHAR(20) NOT NULL,
    devise VARCHAR(3) NOT NULL REFERENCES portefeuille.devises(code_devise),
    type_utilisateur VARCHAR(20) NOT NULL CHECK (type_utilisateur IN ('CLIENT', 'AGENT', 'MARCHAND', 'ADMIN')),
    niveau_kyc INTEGER NOT NULL DEFAULT 0 CHECK (niveau_kyc >= 0 AND niveau_kyc <= 3),
    solde_actuel DECIMAL(20, 2) NOT NULL DEFAULT 0.00 CHECK (solde_actuel >= 0),
    solde_disponible DECIMAL(20, 2) NOT NULL DEFAULT 0.00 CHECK (solde_disponible >= 0),
    solde_reserve DECIMAL(20, 2) NOT NULL DEFAULT 0.00 CHECK (solde_reserve >= 0),
    plafond_journalier DECIMAL(20, 2),
    consommation_journaliere DECIMAL(20, 2) NOT NULL DEFAULT 0.00,
    date_reset_journalier DATE NOT NULL DEFAULT CURRENT_DATE,
    statut VARCHAR(20) NOT NULL DEFAULT 'ACTIF' CHECK (statut IN ('ACTIF', 'SUSPENDU', 'BLOQUE', 'FERME', 'EN_VERIFICATION')),
    derniere_synchronisation TIMESTAMP,
    ecart_synchronisation DECIMAL(20, 2) DEFAULT 0.00,
    metadonnees JSONB DEFAULT '{}',
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP,
    CONSTRAINT unique_utilisateur_devise UNIQUE (utilisateur_id, devise),
    CONSTRAINT solde_coherent CHECK (solde_actuel = solde_disponible + solde_reserve)
);

COMMENT ON TABLE portefeuille.comptes IS 'Comptes virtuels (portefeuilles) liés aux comptes bancaires réels';

CREATE INDEX idx_comptes_utilisateur ON portefeuille.comptes(utilisateur_id);
CREATE INDEX idx_comptes_telephone ON portefeuille.comptes(numero_telephone);
CREATE INDEX idx_comptes_statut ON portefeuille.comptes(statut);
CREATE INDEX idx_comptes_devise ON portefeuille.comptes(devise);


-- ============================================================================
-- PARTIE 4: TRANSACTIONS
-- ============================================================================

-- Table: Transactions
CREATE TABLE transaction.transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reference_transaction VARCHAR(100) NOT NULL UNIQUE,
    type_transaction VARCHAR(50) NOT NULL,
    compte_source_id UUID REFERENCES portefeuille.comptes(id),
    compte_destination_id UUID REFERENCES portefeuille.comptes(id),
    utilisateur_source_id UUID,
    utilisateur_destination_id UUID,
    montant DECIMAL(20, 2) NOT NULL CHECK (montant > 0),
    devise VARCHAR(3) NOT NULL,
    frais DECIMAL(20, 2) NOT NULL DEFAULT 0.00,
    montant_total DECIMAL(20, 2) NOT NULL,
    taux_change DECIMAL(20, 8),
    statut VARCHAR(20) NOT NULL DEFAULT 'INITIE' CHECK (statut IN ('INITIE', 'EN_ATTENTE', 'VALIDEE', 'ECHOUEE', 'ANNULEE', 'REMBOURSEE')),
    motif_echec TEXT,
    reference_bancaire_externe VARCHAR(200),
    description TEXT,
    metadonnees JSONB DEFAULT '{}',
    date_initiation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_validation TIMESTAMP,
    date_echec TIMESTAMP,
    cree_par UUID NOT NULL,
    cree_le TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modifie_par UUID,
    modifie_le TIMESTAMP,
    CONSTRAINT montant_total_coherent CHECK (montant_total = montant + frais)
);

COMMENT ON TABLE transaction.transactions IS 'Toutes les transactions du système';

CREATE INDEX idx_transactions_reference ON transaction.transactions(reference_transaction);
CREATE INDEX idx_transactions_source ON transaction.transactions(compte_source_id);
CREATE INDEX idx_transactions_destination ON transaction.transactions(compte_destination_id);
CREATE INDEX idx_transactions_statut ON transaction.transactions(statut);
CREATE INDEX idx_transactions_type ON transaction.transactions(type_transaction);
CREATE INDEX idx_transactions_date ON transaction.transactions(date_initiation DESC);
CREATE INDEX idx_transactions_utilisateur_source ON transaction.transactions(utilisateur_source_id);


-- ============================================================================
-- PARTIE 5: AUDIT ET HISTORIQUE (TABLES IMMUABLES)
-- ============================================================================

-- Table: Historique des Comptes (IMMUABLE)
CREATE TABLE audit.historique_comptes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    compte_id UUID NOT NULL,
    numero_compte VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    ancien_solde DECIMAL(20, 2),
    nouveau_solde DECIMAL(20, 2),
    ancien_statut VARCHAR(20),
    nouveau_statut VARCHAR(20),
    transaction_id UUID,
    qui_utilisateur_id UUID NOT NULL,
    qui_nom VARCHAR(255),
    qui_type VARCHAR(20),
    quand TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quoi TEXT NOT NULL,
    comment VARCHAR(50) NOT NULL CHECK (comment IN ('WEB', 'API', 'MOBILE', 'SYSTEME', 'ADMIN')),
    pourquoi TEXT,
    adresse_ip INET,
    user_agent TEXT,
    donnees_avant JSONB,
    donnees_apres JSONB,
    metadonnees JSONB DEFAULT '{}'
);

COMMENT ON TABLE audit.historique_comptes IS 'Historique IMMUABLE de tous les changements de comptes';

CREATE INDEX idx_historique_comptes_compte ON audit.historique_comptes(compte_id);
CREATE INDEX idx_historique_comptes_date ON audit.historique_comptes(quand DESC);
CREATE INDEX idx_historique_comptes_utilisateur ON audit.historique_comptes(qui_utilisateur_id);
CREATE INDEX idx_historique_comptes_transaction ON audit.historique_comptes(transaction_id);

-- Table: Historique des Transactions (IMMUABLE)
CREATE TABLE audit.historique_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID NOT NULL,
    reference_transaction VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    ancien_statut VARCHAR(20),
    nouveau_statut VARCHAR(20),
    qui_utilisateur_id UUID NOT NULL,
    qui_nom VARCHAR(255),
    quand TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quoi TEXT NOT NULL,
    comment VARCHAR(50) NOT NULL CHECK (comment IN ('WEB', 'API', 'MOBILE', 'SYSTEME', 'ADMIN')),
    pourquoi TEXT,
    adresse_ip INET,
    user_agent TEXT,
    donnees_avant JSONB,
    donnees_apres JSONB,
    metadonnees JSONB DEFAULT '{}'
);

COMMENT ON TABLE audit.historique_transactions IS 'Historique IMMUABLE de tous les changements de transactions';

CREATE INDEX idx_historique_transactions_transaction ON audit.historique_transactions(transaction_id);
CREATE INDEX idx_historique_transactions_date ON audit.historique_transactions(quand DESC);
CREATE INDEX idx_historique_transactions_reference ON audit.historique_transactions(reference_transaction);


-- ============================================================================
-- PARTIE 6: TRIGGERS POUR CALCULS AUTOMATIQUES
-- ============================================================================

-- Trigger: Calcul automatique taux inverse et taux avec marges
CREATE OR REPLACE FUNCTION portefeuille.calculer_taux_automatique()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculer taux inverse
    NEW.taux_inverse := 1.0 / NEW.taux;
    
    -- Calculer taux avec marges
    NEW.taux_achat := NEW.taux * (1 - NEW.marge_achat);
    NEW.taux_vente := NEW.taux * (1 + NEW.marge_vente);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calculer_taux
    BEFORE INSERT OR UPDATE ON portefeuille.taux_change
    FOR EACH ROW
    EXECUTE FUNCTION portefeuille.calculer_taux_automatique();

-- Trigger: Enregistrement automatique dans historique taux
CREATE OR REPLACE FUNCTION audit.enregistrer_historique_taux()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit.historique_taux_change (
            taux_change_id, devise_source, devise_cible, nouveau_taux,
            action, quoi, comment
        ) VALUES (
            NEW.id, NEW.devise_source, NEW.devise_cible, NEW.taux,
            'INSERT', 'Création nouveau taux de change', 'SYSTEME'
        );
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit.historique_taux_change (
            taux_change_id, devise_source, devise_cible, 
            ancien_taux, nouveau_taux, action, quoi, comment,
            donnees_avant, donnees_apres
        ) VALUES (
            NEW.id, NEW.devise_source, NEW.devise_cible,
            OLD.taux, NEW.taux, 'UPDATE', 'Modification taux de change', 'SYSTEME',
            row_to_json(OLD), row_to_json(NEW)
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_historique_taux
    AFTER INSERT OR UPDATE ON portefeuille.taux_change
    FOR EACH ROW
    EXECUTE FUNCTION audit.enregistrer_historique_taux();

-- Trigger: Protection contre modification/suppression historique taux
CREATE OR REPLACE FUNCTION audit.proteger_historique_taux()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: L''historique des taux est IMMUABLE. Aucune modification ou suppression autorisée.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_proteger_historique_taux_update
    BEFORE UPDATE ON audit.historique_taux_change
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_taux();

CREATE TRIGGER trigger_proteger_historique_taux_delete
    BEFORE DELETE ON audit.historique_taux_change
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_taux();

-- Trigger: Protection contre modification/suppression historique comptes
CREATE OR REPLACE FUNCTION audit.proteger_historique_comptes()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: L''historique des comptes est IMMUABLE. Aucune modification ou suppression autorisée.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_proteger_historique_comptes_update
    BEFORE UPDATE ON audit.historique_comptes
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_comptes();

CREATE TRIGGER trigger_proteger_historique_comptes_delete
    BEFORE DELETE ON audit.historique_comptes
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_comptes();

-- Trigger: Protection contre modification/suppression historique transactions
CREATE OR REPLACE FUNCTION audit.proteger_historique_transactions()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: L''historique des transactions est IMMUABLE. Aucune modification ou suppression autorisée.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_proteger_historique_transactions_update
    BEFORE UPDATE ON audit.historique_transactions
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_transactions();

CREATE TRIGGER trigger_proteger_historique_transactions_delete
    BEFORE DELETE ON audit.historique_transactions
    FOR EACH ROW
    EXECUTE FUNCTION audit.proteger_historique_transactions();


-- ============================================================================
-- PARTIE 7: FONCTIONS UTILITAIRES
-- ============================================================================

-- Fonction: Obtenir le plafond applicable
CREATE OR REPLACE FUNCTION configuration.get_plafond_applicable(
    p_niveau_kyc INTEGER,
    p_type_utilisateur VARCHAR,
    p_code_devise VARCHAR
) RETURNS TABLE (
    montant_max_transaction DECIMAL,
    montant_max_journalier DECIMAL,
    montant_max_mensuel DECIMAL,
    solde_maximum DECIMAL,
    nombre_max_transactions_jour INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pc.montant_max_transaction,
        pc.montant_max_journalier,
        pc.montant_max_mensuel,
        pc.solde_maximum,
        pc.nombre_max_transactions_jour
    FROM configuration.plafonds_configuration pc
    WHERE pc.niveau_kyc = p_niveau_kyc
      AND pc.type_utilisateur = p_type_utilisateur
      AND pc.code_devise = p_code_devise
      AND pc.est_actif = TRUE
      AND pc.date_debut_validite <= CURRENT_TIMESTAMP
      AND (pc.date_fin_validite IS NULL OR pc.date_fin_validite > CURRENT_TIMESTAMP)
    ORDER BY pc.priorite DESC, pc.date_debut_validite DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION configuration.get_plafond_applicable IS 'Retourne le plafond applicable pour un utilisateur';

-- Fonction: Obtenir règle métier
CREATE OR REPLACE FUNCTION configuration.get_regle_metier(
    p_code_regle VARCHAR
) RETURNS JSONB AS $$
DECLARE
    v_valeur JSONB;
BEGIN
    SELECT valeur INTO v_valeur
    FROM configuration.regles_metier
    WHERE code_regle = p_code_regle
      AND est_actif = TRUE
    ORDER BY priorite DESC
    LIMIT 1;
    
    RETURN COALESCE(v_valeur, '{}'::jsonb);
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION configuration.get_regle_metier IS 'Retourne la valeur d''une règle métier';

-- Fonction: Calculer frais transaction
CREATE OR REPLACE FUNCTION configuration.calculer_frais(
    p_type_transaction VARCHAR,
    p_montant DECIMAL,
    p_code_devise VARCHAR,
    p_type_source VARCHAR DEFAULT NULL,
    p_type_destination VARCHAR DEFAULT NULL
) RETURNS DECIMAL AS $$
DECLARE
    v_config RECORD;
    v_frais DECIMAL := 0;
BEGIN
    SELECT * INTO v_config
    FROM configuration.frais_configuration
    WHERE type_transaction = p_type_transaction
      AND code_devise = p_code_devise
      AND (type_utilisateur_source IS NULL OR type_utilisateur_source = p_type_source)
      AND (type_utilisateur_destination IS NULL OR type_utilisateur_destination = p_type_destination)
      AND montant_min <= p_montant
      AND (montant_max IS NULL OR montant_max >= p_montant)
      AND est_actif = TRUE
      AND date_debut_validite <= CURRENT_TIMESTAMP
      AND (date_fin_validite IS NULL OR date_fin_validite > CURRENT_TIMESTAMP)
    ORDER BY priorite DESC, date_debut_validite DESC
    LIMIT 1;
    
    IF v_config IS NOT NULL THEN
        IF v_config.type_frais = 'FIXE' THEN
            v_frais := v_config.valeur_frais;
        ELSIF v_config.type_frais = 'POURCENTAGE' THEN
            v_frais := p_montant * v_config.valeur_frais / 100;
            v_frais := GREATEST(v_frais, COALESCE(v_config.frais_min, 0));
            IF v_config.frais_max IS NOT NULL THEN
                v_frais := LEAST(v_frais, v_config.frais_max);
            END IF;
        END IF;
    END IF;
    
    RETURN v_frais;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION configuration.calculer_frais IS 'Calcule les frais applicables pour une transaction';

-- Fonction: Vérifier nombre de comptes autorisés
CREATE OR REPLACE FUNCTION configuration.verifier_limite_comptes(
    p_utilisateur_id UUID,
    p_type_utilisateur VARCHAR,
    p_code_devise VARCHAR
) RETURNS BOOLEAN AS $$
DECLARE
    v_nombre_comptes_actuels INTEGER;
    v_nombre_max_autorise INTEGER;
BEGIN
    -- Compter les comptes existants
    SELECT COUNT(*) INTO v_nombre_comptes_actuels
    FROM portefeuille.comptes
    WHERE utilisateur_id = p_utilisateur_id
      AND devise = p_code_devise
      AND statut != 'FERME';
    
    -- Obtenir la limite autorisée
    SELECT nombre_max_comptes INTO v_nombre_max_autorise
    FROM configuration.devises_autorisees
    WHERE type_utilisateur = p_type_utilisateur
      AND code_devise = p_code_devise
      AND est_actif = TRUE
      AND date_debut_validite <= CURRENT_TIMESTAMP
      AND (date_fin_validite IS NULL OR date_fin_validite > CURRENT_TIMESTAMP)
    LIMIT 1;
    
    -- Si pas de configuration, autoriser 1 compte par défaut
    IF v_nombre_max_autorise IS NULL THEN
        v_nombre_max_autorise := 1;
    END IF;
    
    RETURN v_nombre_comptes_actuels < v_nombre_max_autorise;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION configuration.verifier_limite_comptes IS 'Vérifie si un utilisateur peut créer un nouveau compte dans une devise';


-- ============================================================================
-- PARTIE 8: DONNÉES INITIALES
-- ============================================================================

-- UUID système pour création initiale
DO $$
DECLARE
    uuid_systeme UUID := '00000000-0000-0000-0000-000000000000';
BEGIN
    -- ========================================================================
    -- Devises
    -- ========================================================================
    INSERT INTO portefeuille.devises (code_devise, nom_devise, symbole, decimales, pays_principal, ordre_affichage) VALUES
    ('BIF', 'Franc Burundais', 'FBu', 0, 'BI', 1),
    ('USD', 'Dollar Américain', '$', 2, 'US', 2),
    ('EUR', 'Euro', '€', 2, 'EU', 3),
    ('RWF', 'Franc Rwandais', 'RF', 0, 'RW', 4),
    ('KES', 'Shilling Kenyan', 'KSh', 2, 'KE', 5),
    ('TZS', 'Shilling Tanzanien', 'TSh', 2, 'TZ', 6),
    ('UGX', 'Shilling Ougandais', 'USh', 0, 'UG', 7),
    ('CDF', 'Franc Congolais', 'FC', 2, 'CD', 8)
    ON CONFLICT (code_devise) DO NOTHING;
    
    -- ========================================================================
    -- Taux de change initiaux
    -- ========================================================================
    INSERT INTO portefeuille.taux_change (devise_source, devise_cible, taux, marge_achat, marge_vente, source) VALUES
    ('USD', 'BIF', 2900.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('EUR', 'BIF', 3200.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('USD', 'RWF', 1300.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('USD', 'KES', 130.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('USD', 'TZS', 2500.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('USD', 'UGX', 3700.00, 0.0100, 0.0100, 'Banque Centrale'),
    ('USD', 'CDF', 2800.00, 0.0100, 0.0100, 'Banque Centrale')
    ON CONFLICT DO NOTHING;
    
    -- ========================================================================
    -- Plafonds par défaut
    -- ========================================================================
    INSERT INTO configuration.plafonds_configuration 
    (niveau_kyc, type_utilisateur, code_devise, montant_max_transaction, montant_max_journalier, 
     montant_max_mensuel, solde_maximum, nombre_max_transactions_jour, description, cree_par)
    VALUES 
    -- CLIENT KYC 0 - BIF
    (0, 'CLIENT', 'BIF', 50000, 50000, 500000, 100000, 10, 'Plafond minimal KYC 0 - BIF', uuid_systeme),
    (1, 'CLIENT', 'BIF', 500000, 500000, 5000000, 1000000, 50, 'Plafond standard KYC 1 - BIF', uuid_systeme),
    (2, 'CLIENT', 'BIF', 5000000, 5000000, 50000000, 10000000, 100, 'Plafond élevé KYC 2 - BIF', uuid_systeme),
    (3, 'CLIENT', 'BIF', 50000000, 50000000, 500000000, NULL, NULL, 'Plafond illimité KYC 3 - BIF', uuid_systeme),
    -- CLIENT KYC 0 - USD
    (0, 'CLIENT', 'USD', 20, 20, 200, 50, 10, 'Plafond minimal KYC 0 - USD', uuid_systeme),
    (1, 'CLIENT', 'USD', 200, 200, 2000, 500, 50, 'Plafond standard KYC 1 - USD', uuid_systeme),
    (2, 'CLIENT', 'USD', 2000, 2000, 20000, 5000, 100, 'Plafond élevé KYC 2 - USD', uuid_systeme),
    (3, 'CLIENT', 'USD', 20000, 20000, 200000, NULL, NULL, 'Plafond illimité KYC 3 - USD', uuid_systeme),
    -- AGENT - BIF
    (1, 'AGENT', 'BIF', 2000000, 10000000, 100000000, 20000000, 200, 'Plafond AGENT - BIF', uuid_systeme),
    (1, 'AGENT', 'USD', 1000, 5000, 50000, 10000, 200, 'Plafond AGENT - USD', uuid_systeme),
    -- MARCHAND - BIF
    (1, 'MARCHAND', 'BIF', 5000000, 20000000, 200000000, NULL, 500, 'Plafond MARCHAND - BIF', uuid_systeme),
    (1, 'MARCHAND', 'USD', 2000, 10000, 100000, NULL, 500, 'Plafond MARCHAND - USD', uuid_systeme)
    ON CONFLICT DO NOTHING;
    
    -- ========================================================================
    -- Règles métier
    -- ========================================================================
    INSERT INTO configuration.regles_metier 
    (code_regle, nom_regle, description, categorie, valeur, cree_par)
    VALUES 
    ('MAX_COMPTES_PAR_DEVISE', 'Nombre maximum de comptes par devise', 
     'Définit combien de comptes un utilisateur peut avoir par devise selon son type',
     'COMPTE', '{"CLIENT": 1, "AGENT": 3, "MARCHAND": 2, "ADMIN": 5}'::jsonb, uuid_systeme),
    ('DEVISES_AUTORISEES_CLIENT', 'Devises autorisées pour CLIENT', 
     'Liste des devises qu''un CLIENT peut utiliser', 'COMPTE', '["BIF", "USD"]'::jsonb, uuid_systeme),
    ('DEVISES_AUTORISEES_AGENT', 'Devises autorisées pour AGENT', 
     'Liste des devises qu''un AGENT peut utiliser', 'COMPTE', '["BIF", "USD", "EUR", "RWF"]'::jsonb, uuid_systeme),
    ('DEVISES_AUTORISEES_MARCHAND', 'Devises autorisées pour MARCHAND', 
     'Liste des devises qu''un MARCHAND peut utiliser', 'COMPTE', '["BIF", "USD", "EUR"]'::jsonb, uuid_systeme),
    ('DELAI_SYNCHRONISATION', 'Délai de synchronisation bancaire', 
     'Fréquence de synchronisation avec les banques partenaires',
     'SYNCHRONISATION', '{"minutes": 5, "en_cas_transaction": true}'::jsonb, uuid_systeme),
    ('SEUIL_2FA', 'Seuil déclenchement 2FA', 
     'Montants au-delà desquels le 2FA est obligatoire par devise',
     'SECURITE', '{"BIF": 1000000, "USD": 500, "EUR": 400}'::jsonb, uuid_systeme),
    ('TOLERANCE_ECART_SYNC', 'Tolérance écart synchronisation', 
     'Écart acceptable entre solde virtuel et réel avant alerte',
     'SYNCHRONISATION', '{"BIF": 100, "USD": 0.05, "EUR": 0.05}'::jsonb, uuid_systeme)
    ON CONFLICT DO NOTHING;
    
END $$;


DO $$
DECLARE
    uuid_systeme UUID := '00000000-0000-0000-0000-000000000000';
BEGIN
    -- ========================================================================
    -- Types de transactions
    -- ========================================================================
    INSERT INTO configuration.types_transaction 
    (code_type, nom_type, description, necessite_compte_source, necessite_compte_destination,
     impacte_solde_source, impacte_solde_destination, types_utilisateurs_autorises, 
     necessite_2fa, montant_min, cree_par, ordre_affichage)
    VALUES 
    ('DEPOT', 'Dépôt', 'Ajout d''argent sur un compte', FALSE, TRUE, 'AUCUN', 'CREDIT',
     '["AGENT"]'::jsonb, FALSE, 100, uuid_systeme, 1),
    ('RETRAIT', 'Retrait', 'Retrait d''argent d''un compte', TRUE, FALSE, 'DEBIT', 'AUCUN',
     '["AGENT"]'::jsonb, FALSE, 100, uuid_systeme, 2),
    ('TRANSFERT', 'Transfert P2P', 'Transfert entre deux utilisateurs', TRUE, TRUE, 'DEBIT', 'CREDIT',
     '["CLIENT", "AGENT", "MARCHAND"]'::jsonb, FALSE, 100, uuid_systeme, 3),
    ('PAIEMENT', 'Paiement Marchand', 'Paiement à un marchand', TRUE, TRUE, 'DEBIT', 'CREDIT',
     '["CLIENT"]'::jsonb, FALSE, 100, uuid_systeme, 4),
    ('FRAIS', 'Frais', 'Prélèvement de frais', TRUE, FALSE, 'DEBIT', 'AUCUN',
     '["ADMIN"]'::jsonb, FALSE, 0, uuid_systeme, 10),
    ('COMMISSION', 'Commission', 'Commission agent/marchand', FALSE, TRUE, 'AUCUN', 'CREDIT',
     '["ADMIN"]'::jsonb, FALSE, 0, uuid_systeme, 11),
    ('AJUSTEMENT', 'Ajustement', 'Correction manuelle du solde', TRUE, FALSE, 'CREDIT', 'AUCUN',
     '["ADMIN", "SUPER_ADMIN"]'::jsonb, TRUE, 0, uuid_systeme, 20),
    ('REMBOURSEMENT', 'Remboursement', 'Remboursement d''une transaction', FALSE, TRUE, 'AUCUN', 'CREDIT',
     '["ADMIN"]'::jsonb, FALSE, 0, uuid_systeme, 21)
    ON CONFLICT DO NOTHING;
    
    -- ========================================================================
    -- Configuration des frais
    -- ========================================================================
    INSERT INTO configuration.frais_configuration 
    (type_transaction, code_devise, montant_min, montant_max, type_frais, valeur_frais, 
     frais_min, frais_max, qui_paie, description, cree_par)
    VALUES 
    -- Frais DEPOT - Gratuit
    ('DEPOT', 'BIF', 0, NULL, 'FIXE', 0, 0, 0, 'SOURCE', 'Dépôt gratuit', uuid_systeme),
    ('DEPOT', 'USD', 0, NULL, 'FIXE', 0, 0, 0, 'SOURCE', 'Dépôt gratuit', uuid_systeme),
    -- Frais RETRAIT - Fixe par paliers
    ('RETRAIT', 'BIF', 0, 100000, 'FIXE', 100, 100, 100, 'SOURCE', 'Frais retrait petit montant', uuid_systeme),
    ('RETRAIT', 'BIF', 100001, 500000, 'FIXE', 200, 200, 200, 'SOURCE', 'Frais retrait moyen montant', uuid_systeme),
    ('RETRAIT', 'BIF', 500001, NULL, 'FIXE', 500, 500, 500, 'SOURCE', 'Frais retrait gros montant', uuid_systeme),
    ('RETRAIT', 'USD', 0, NULL, 'FIXE', 0.5, 0.5, 0.5, 'SOURCE', 'Frais retrait USD', uuid_systeme),
    -- Frais TRANSFERT - Pourcentage avec min/max
    ('TRANSFERT', 'BIF', 0, NULL, 'POURCENTAGE', 0.5, 50, 1000, 'SOURCE', 'Frais transfert 0.5% (min 50, max 1000)', uuid_systeme),
    ('TRANSFERT', 'USD', 0, NULL, 'POURCENTAGE', 1.0, 0.25, 5, 'SOURCE', 'Frais transfert 1% (min 0.25, max 5)', uuid_systeme),
    -- Frais PAIEMENT - Pourcentage payé par marchand
    ('PAIEMENT', 'BIF', 0, NULL, 'POURCENTAGE', 2.0, 100, 5000, 'DESTINATION', 'Frais marchand 2% (min 100, max 5000)', uuid_systeme),
    ('PAIEMENT', 'USD', 0, NULL, 'POURCENTAGE', 2.5, 0.5, 10, 'DESTINATION', 'Frais marchand 2.5% (min 0.5, max 10)', uuid_systeme)
    ON CONFLICT DO NOTHING;
    
    -- ========================================================================
    -- Devises autorisées par type utilisateur
    -- ========================================================================
    INSERT INTO configuration.devises_autorisees 
    (type_utilisateur, code_devise, nombre_max_comptes, peut_creer_compte, 
     peut_recevoir, peut_envoyer, description, cree_par)
    VALUES 
    -- CLIENT
    ('CLIENT', 'BIF', 1, TRUE, TRUE, TRUE, 'CLIENT peut avoir 1 compte BIF', uuid_systeme),
    ('CLIENT', 'USD', 1, TRUE, TRUE, TRUE, 'CLIENT peut avoir 1 compte USD', uuid_systeme),
    -- AGENT
    ('AGENT', 'BIF', 3, TRUE, TRUE, TRUE, 'AGENT peut avoir 3 comptes BIF', uuid_systeme),
    ('AGENT', 'USD', 3, TRUE, TRUE, TRUE, 'AGENT peut avoir 3 comptes USD', uuid_systeme),
    ('AGENT', 'EUR', 2, TRUE, TRUE, TRUE, 'AGENT peut avoir 2 comptes EUR', uuid_systeme),
    ('AGENT', 'RWF', 2, TRUE, TRUE, TRUE, 'AGENT peut avoir 2 comptes RWF', uuid_systeme),
    -- MARCHAND
    ('MARCHAND', 'BIF', 2, TRUE, TRUE, TRUE, 'MARCHAND peut avoir 2 comptes BIF', uuid_systeme),
    ('MARCHAND', 'USD', 2, TRUE, TRUE, TRUE, 'MARCHAND peut avoir 2 comptes USD', uuid_systeme),
    ('MARCHAND', 'EUR', 1, TRUE, TRUE, TRUE, 'MARCHAND peut avoir 1 compte EUR', uuid_systeme),
    -- ADMIN
    ('ADMIN', 'BIF', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes BIF', uuid_systeme),
    ('ADMIN', 'USD', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes USD', uuid_systeme),
    ('ADMIN', 'EUR', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes EUR', uuid_systeme),
    ('ADMIN', 'RWF', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes RWF', uuid_systeme),
    ('ADMIN', 'KES', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes KES', uuid_systeme),
    ('ADMIN', 'TZS', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes TZS', uuid_systeme),
    ('ADMIN', 'UGX', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes UGX', uuid_systeme),
    ('ADMIN', 'CDF', 5, TRUE, TRUE, TRUE, 'ADMIN peut avoir 5 comptes CDF', uuid_systeme)
    ON CONFLICT DO NOTHING;
    
END $$;

-- ============================================================================
-- FIN DU SCRIPT
-- ============================================================================

SELECT 'Structure de base de données créée avec succès!' AS message;
SELECT 'Schémas créés: audit, bancaire, commission, compliance, configuration, notification, portefeuille, transaction' AS schemas;
SELECT COUNT(*) AS nb_devises FROM portefeuille.devises;
SELECT COUNT(*) AS nb_taux_change FROM portefeuille.taux_change;
SELECT COUNT(*) AS nb_plafonds FROM configuration.plafonds_configuration;
SELECT COUNT(*) AS nb_regles FROM configuration.regles_metier;
SELECT COUNT(*) AS nb_frais FROM configuration.frais_configuration;
SELECT COUNT(*) AS nb_types_transaction FROM configuration.types_transaction;
SELECT COUNT(*) AS nb_devises_autorisees FROM configuration.devises_autorisees;
