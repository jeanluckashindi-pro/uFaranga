-- ============================================================================
-- Script SQL pour peupler les données de localisation
-- Base: ufaranga, Schema: localisation
-- Utilisateur: ufaranga
-- ============================================================================

-- Connexion: psql -U ufaranga -d ufaranga -f peupler_localisation_sql.sql

BEGIN;

-- ============================================================================
-- 1. AJOUTER LES COLONNES CONTINENT ET SOUS_REGION
-- ============================================================================

-- Ajouter la colonne continent
ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS continent VARCHAR(50);

-- Ajouter la colonne sous_region
ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS sous_region VARCHAR(100);

-- Créer les index
CREATE INDEX IF NOT EXISTS idx_pays_continent ON localisation.pays(continent);
CREATE INDEX IF NOT EXISTS idx_pays_sous_region ON localisation.pays(sous_region);

COMMIT;

-- ============================================================================
-- 2. PEUPLER LES PAYS AFRICAINS
-- ============================================================================

BEGIN;

-- AFRIQUE DE L'EST

-- Burundi
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'BI', 'BDI', 'Burundi', 'Burundi',
    'Afrique', 'Afrique de l''Est',
    -3.3731, 29.9189,
    true, true,
    '{"capitale": "Gitega", "telephonie": {"code_telephonique": "+257"}, "devise": {"code": "BIF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Rwanda
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'RW', 'RWA', 'Rwanda', 'Rwanda',
    'Afrique', 'Afrique de l''Est',
    -1.9403, 29.8739,
    true, true,
    '{"capitale": "Kigali", "telephonie": {"code_telephonique": "+250"}, "devise": {"code": "RWF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Kenya
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'KE', 'KEN', 'Kenya', 'Kenya',
    'Afrique', 'Afrique de l''Est',
    -0.0236, 37.9062,
    true, true,
    '{"capitale": "Nairobi", "telephonie": {"code_telephonique": "+254"}, "devise": {"code": "KES"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Tanzanie
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'TZ', 'TZA', 'Tanzanie', 'Tanzania',
    'Afrique', 'Afrique de l''Est',
    -6.3690, 34.8888,
    true, true,
    '{"capitale": "Dodoma", "telephonie": {"code_telephonique": "+255"}, "devise": {"code": "TZS"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Ouganda
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'UG', 'UGA', 'Ouganda', 'Uganda',
    'Afrique', 'Afrique de l''Est',
    1.3733, 32.2903,
    true, true,
    '{"capitale": "Kampala", "telephonie": {"code_telephonique": "+256"}, "devise": {"code": "UGX"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- AFRIQUE CENTRALE

-- RD Congo
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'CD', 'COD', 'République Démocratique du Congo', 'Democratic Republic of the Congo',
    'Afrique', 'Afrique Centrale',
    -4.0383, 21.7587,
    true, true,
    '{"capitale": "Kinshasa", "telephonie": {"code_telephonique": "+243"}, "devise": {"code": "CDF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Congo
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'CG', 'COG', 'République du Congo', 'Republic of the Congo',
    'Afrique', 'Afrique Centrale',
    -4.2634, 15.2429,
    true, true,
    '{"capitale": "Brazzaville", "telephonie": {"code_telephonique": "+242"}, "devise": {"code": "XAF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Cameroun
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'CM', 'CMR', 'Cameroun', 'Cameroon',
    'Afrique', 'Afrique Centrale',
    7.3697, 12.3547,
    true, true,
    '{"capitale": "Yaoundé", "telephonie": {"code_telephonique": "+237"}, "devise": {"code": "XAF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Gabon
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'GA', 'GAB', 'Gabon', 'Gabon',
    'Afrique', 'Afrique Centrale',
    -0.8037, 11.6094,
    true, true,
    '{"capitale": "Libreville", "telephonie": {"code_telephonique": "+241"}, "devise": {"code": "XAF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- République Centrafricaine
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'CF', 'CAF', 'République Centrafricaine', 'Central African Republic',
    'Afrique', 'Afrique Centrale',
    6.6111, 20.9394,
    true, true,
    '{"capitale": "Bangui", "telephonie": {"code_telephonique": "+236"}, "devise": {"code": "XAF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- AFRIQUE DE L'OUEST

-- Sénégal
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'SN', 'SEN', 'Sénégal', 'Senegal',
    'Afrique', 'Afrique de l''Ouest',
    14.4974, -14.4524,
    true, true,
    '{"capitale": "Dakar", "telephonie": {"code_telephonique": "+221"}, "devise": {"code": "XOF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Côte d'Ivoire
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'CI', 'CIV', 'Côte d''Ivoire', 'Ivory Coast',
    'Afrique', 'Afrique de l''Ouest',
    7.5400, -5.5471,
    true, true,
    '{"capitale": "Yamoussoukro", "telephonie": {"code_telephonique": "+225"}, "devise": {"code": "XOF"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Ghana
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'GH', 'GHA', 'Ghana', 'Ghana',
    'Afrique', 'Afrique de l''Ouest',
    7.9465, -1.0232,
    true, true,
    '{"capitale": "Accra", "telephonie": {"code_telephonique": "+233"}, "devise": {"code": "GHS"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Nigeria
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'NG', 'NGA', 'Nigeria', 'Nigeria',
    'Afrique', 'Afrique de l''Ouest',
    9.0820, 8.6753,
    true, true,
    '{"capitale": "Abuja", "telephonie": {"code_telephonique": "+234"}, "devise": {"code": "NGN"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- AFRIQUE DU NORD

-- Maroc
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'MA', 'MAR', 'Maroc', 'Morocco',
    'Afrique', 'Afrique du Nord',
    31.7917, -7.0926,
    true, true,
    '{"capitale": "Rabat", "telephonie": {"code_telephonique": "+212"}, "devise": {"code": "MAD"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Algérie
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'DZ', 'DZA', 'Algérie', 'Algeria',
    'Afrique', 'Afrique du Nord',
    28.0339, 1.6596,
    true, true,
    '{"capitale": "Alger", "telephonie": {"code_telephonique": "+213"}, "devise": {"code": "DZD"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Tunisie
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'TN', 'TUN', 'Tunisie', 'Tunisia',
    'Afrique', 'Afrique du Nord',
    33.8869, 9.5375,
    true, true,
    '{"capitale": "Tunis", "telephonie": {"code_telephonique": "+216"}, "devise": {"code": "TND"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- Égypte
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'EG', 'EGY', 'Égypte', 'Egypt',
    'Afrique', 'Afrique du Nord',
    26.8206, 30.8025,
    true, true,
    '{"capitale": "Le Caire", "telephonie": {"code_telephonique": "+20"}, "devise": {"code": "EGP"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

-- AFRIQUE AUSTRALE

-- Afrique du Sud
INSERT INTO localisation.pays (id, code_iso_2, code_iso_3, nom, nom_anglais, continent, sous_region, latitude_centre, longitude_centre, autorise_systeme, est_actif, metadonnees)
VALUES (
    gen_random_uuid(),
    'ZA', 'ZAF', 'Afrique du Sud', 'South Africa',
    'Afrique', 'Afrique Australe',
    -30.5595, 22.9375,
    true, true,
    '{"capitale": "Pretoria", "telephonie": {"code_telephonique": "+27"}, "devise": {"code": "ZAR"}}'::jsonb
)
ON CONFLICT (code_iso_2) DO UPDATE SET
    continent = EXCLUDED.continent,
    sous_region = EXCLUDED.sous_region,
    metadonnees = EXCLUDED.metadonnees;

COMMIT;

-- ============================================================================
-- 3. AFFICHER LES RÉSULTATS
-- ============================================================================

SELECT 
    code_iso_2,
    nom,
    continent,
    sous_region,
    (metadonnees->>'capitale') as capitale
FROM localisation.pays
WHERE continent = 'Afrique'
ORDER BY sous_region, nom;

-- Statistiques
SELECT 
    sous_region,
    COUNT(*) as nb_pays
FROM localisation.pays
WHERE continent = 'Afrique'
GROUP BY sous_region
ORDER BY nb_pays DESC;
