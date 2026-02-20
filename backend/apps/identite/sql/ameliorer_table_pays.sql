-- =============================================================================
-- AMÉLIORATION DE LA TABLE PAYS
-- =============================================================================
-- Ajout des champs de téléphonie et validation
-- =============================================================================

SET search_path TO localisation, public;

\echo '========================================='
\echo 'AMÉLIORATION TABLE PAYS'
\echo '========================================='
\echo ''

-- =============================================================================
-- 1. AJOUTER LES COLONNES DE TÉLÉPHONIE
-- =============================================================================

\echo '1. Ajout des colonnes de téléphonie...'

ALTER TABLE localisation.pays
    -- Codes ISO (si pas déjà présents)
    ADD COLUMN IF NOT EXISTS code_iso_alpha2 CHAR(2) UNIQUE,
    ADD COLUMN IF NOT EXISTS code_iso_alpha3 CHAR(3) UNIQUE,
    ADD COLUMN IF NOT EXISTS code_iso_numerique CHAR(3) UNIQUE,
    
    -- Téléphonie
    ADD COLUMN IF NOT EXISTS code_telephonique VARCHAR(10),
    ADD COLUMN IF NOT EXISTS format_numero_national VARCHAR(50),
    ADD COLUMN IF NOT EXISTS longueur_numero_min INTEGER DEFAULT 8,
    ADD COLUMN IF NOT EXISTS longueur_numero_max INTEGER DEFAULT 15,
    ADD COLUMN IF NOT EXISTS regex_validation VARCHAR(200),
    ADD COLUMN IF NOT EXISTS exemples_numeros TEXT[],
    
    -- Devise
    ADD COLUMN IF NOT EXISTS code_devise CHAR(3),
    ADD COLUMN IF NOT EXISTS symbole_devise VARCHAR(10),
    
    -- Géographie
    ADD COLUMN IF NOT EXISTS continent VARCHAR(50),
    ADD COLUMN IF NOT EXISTS sous_region VARCHAR(100),
    ADD COLUMN IF NOT EXISTS capitale VARCHAR(100),
    
    -- Statut et sécurité
    ADD COLUMN IF NOT EXISTS autorise_inscription BOOLEAN DEFAULT true,
    ADD COLUMN IF NOT EXISTS autorise_transactions BOOLEAN DEFAULT true,
    ADD COLUMN IF NOT EXISTS niveau_risque VARCHAR(20) DEFAULT 'NORMAL',
    
    -- Limites
    ADD COLUMN IF NOT EXISTS limite_numeros_par_utilisateur INTEGER DEFAULT 3,
    ADD COLUMN IF NOT EXISTS limite_transaction_journaliere NUMERIC(15,2),
    
    -- Métadonnées
    ADD COLUMN IF NOT EXISTS metadonnees JSONB DEFAULT '{}'::jsonb;

\echo '✓ Colonnes ajoutées'
\echo ''

-- =============================================================================
-- 2. CRÉER LES INDEX
-- =============================================================================

\echo '2. Création des index...'

CREATE INDEX IF NOT EXISTS idx_pays_code_iso2 ON localisation.pays(code_iso_alpha2);
CREATE INDEX IF NOT EXISTS idx_pays_code_iso3 ON localisation.pays(code_iso_alpha3);
CREATE INDEX IF NOT EXISTS idx_pays_code_tel ON localisation.pays(code_telephonique);
CREATE INDEX IF NOT EXISTS idx_pays_continent ON localisation.pays(continent);

\echo '✓ Index créés'
\echo ''

-- =============================================================================
-- 3. AJOUTER LES COMMENTAIRES
-- =============================================================================

COMMENT ON COLUMN localisation.pays.code_iso_alpha2 IS 'Code ISO 3166-1 alpha-2 (ex: BI, RW, CD)';
COMMENT ON COLUMN localisation.pays.code_iso_alpha3 IS 'Code ISO 3166-1 alpha-3 (ex: BDI, RWA, COD)';
COMMENT ON COLUMN localisation.pays.code_telephonique IS 'Code téléphonique international (ex: +257, +250)';
COMMENT ON COLUMN localisation.pays.regex_validation IS 'Expression régulière pour valider les numéros de ce pays';
COMMENT ON COLUMN localisation.pays.limite_numeros_par_utilisateur IS 'Nombre maximum de numéros qu''un utilisateur peut avoir';

\echo '✓ Commentaires ajoutés'
\echo ''

-- =============================================================================
-- 4. DONNÉES INITIALES POUR LES PAYS D'AFRIQUE DE L'EST
-- =============================================================================

\echo '3. Insertion des données pour les pays d''Afrique de l''Est...'

-- Burundi
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'BI', 'Burundi', 'BI', 'BDI', '108',
    '+257', 'XX XX XX XX', 8, 8,
    '^[67]\d{7}$', ARRAY['+25762046725', '+25779123456'],
    'BIF', 'FBu', 'Afrique', 'Afrique de l''Est', 'Gitega',
    true, true, 'NORMAL',
    3, 5000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_iso_numerique = EXCLUDED.code_iso_numerique,
    code_telephonique = EXCLUDED.code_telephonique,
    format_numero_national = EXCLUDED.format_numero_national,
    longueur_numero_min = EXCLUDED.longueur_numero_min,
    longueur_numero_max = EXCLUDED.longueur_numero_max,
    regex_validation = EXCLUDED.regex_validation,
    exemples_numeros = EXCLUDED.exemples_numeros,
    code_devise = EXCLUDED.code_devise,
    symbole_devise = EXCLUDED.symbole_devise,
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    capitale = EXCLUDED.capitale,
    limite_numeros_par_utilisateur = EXCLUDED.limite_numeros_par_utilisateur;

-- Rwanda
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'RW', 'Rwanda', 'RW', 'RWA', '646',
    '+250', 'XXX XXX XXX', 9, 9,
    '^7\d{8}$', ARRAY['+250788123456', '+250722987654'],
    'RWF', 'RF', 'Afrique', 'Afrique de l''Est', 'Kigali',
    true, true, 'NORMAL',
    3, 10000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_telephonique = EXCLUDED.code_telephonique,
    regex_validation = EXCLUDED.regex_validation;

-- RD Congo
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'CD', 'République Démocratique du Congo', 'CD', 'COD', '180',
    '+243', 'XXX XXX XXX', 9, 9,
    '^[89]\d{8}$', ARRAY['+243812345678', '+243998765432'],
    'CDF', 'FC', 'Afrique', 'Afrique Centrale', 'Kinshasa',
    true, true, 'NORMAL',
    3, 5000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_telephonique = EXCLUDED.code_telephonique,
    regex_validation = EXCLUDED.regex_validation;

-- Tanzanie
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'TZ', 'Tanzanie', 'TZ', 'TZA', '834',
    '+255', 'XXX XXX XXX', 9, 9,
    '^[67]\d{8}$', ARRAY['+255712345678', '+255654987321'],
    'TZS', 'TSh', 'Afrique', 'Afrique de l''Est', 'Dodoma',
    true, true, 'NORMAL',
    3, 10000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_telephonique = EXCLUDED.code_telephonique,
    regex_validation = EXCLUDED.regex_validation;

-- Kenya
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'KE', 'Kenya', 'KE', 'KEN', '404',
    '+254', 'XXX XXX XXX', 9, 9,
    '^[17]\d{8}$', ARRAY['+254712345678', '+254722987654'],
    'KES', 'KSh', 'Afrique', 'Afrique de l''Est', 'Nairobi',
    true, true, 'NORMAL',
    3, 15000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_telephonique = EXCLUDED.code_telephonique,
    regex_validation = EXCLUDED.regex_validation;

-- Ouganda
INSERT INTO localisation.pays (
    code, nom, code_iso_alpha2, code_iso_alpha3, code_iso_numerique,
    code_telephonique, format_numero_national, longueur_numero_min, longueur_numero_max,
    regex_validation, exemples_numeros,
    code_devise, symbole_devise, continent, sous_region, capitale,
    autorise_inscription, autorise_transactions, niveau_risque,
    limite_numeros_par_utilisateur, limite_transaction_journaliere
) VALUES (
    'UG', 'Ouganda', 'UG', 'UGA', '800',
    '+256', 'XXX XXX XXX', 9, 9,
    '^[37]\d{8}$', ARRAY['+256712345678', '+256772987654'],
    'UGX', 'USh', 'Afrique', 'Afrique de l''Est', 'Kampala',
    true, true, 'NORMAL',
    3, 10000000
)
ON CONFLICT (code) DO UPDATE SET
    code_iso_alpha2 = EXCLUDED.code_iso_alpha2,
    code_iso_alpha3 = EXCLUDED.code_iso_alpha3,
    code_telephonique = EXCLUDED.code_telephonique,
    regex_validation = EXCLUDED.regex_validation;

\echo '✓ Données des pays insérées'
\echo ''

-- =============================================================================
-- 5. VÉRIFICATION
-- =============================================================================

\echo '4. Vérification des données...'
\echo ''

SELECT 
    code,
    nom,
    code_iso_alpha2,
    code_telephonique,
    code_devise,
    limite_numeros_par_utilisateur
FROM localisation.pays
WHERE code IN ('BI', 'RW', 'CD', 'TZ', 'KE', 'UG')
ORDER BY nom;

\echo ''
\echo '========================================='
\echo '✓ TABLE PAYS AMÉLIORÉE!'
\echo '========================================='
\echo ''
