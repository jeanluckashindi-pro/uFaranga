-- ============================================================================
-- Script SQL pour peupler les PROVINCES
-- Base: ufaranga, Schema: localisation
-- ============================================================================

-- Connexion: psql -U ufaranga -d ufaranga -f peupler_provinces_sql.sql

BEGIN;

-- ============================================================================
-- PROVINCES DU BURUNDI (17 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('BB', 'Bubanza'),
    ('BM', 'Bujumbura Mairie'),
    ('BR', 'Bujumbura Rural'),
    ('BU', 'Bururi'),
    ('CA', 'Cankuzo'),
    ('CI', 'Cibitoke'),
    ('GI', 'Gitega'),
    ('KI', 'Kirundo'),
    ('KR', 'Karuzi'),
    ('KY', 'Kayanza'),
    ('MA', 'Makamba'),
    ('MU', 'Muramvya'),
    ('MW', 'Mwaro'),
    ('MY', 'Muyinga'),
    ('NG', 'Ngozi'),
    ('RT', 'Rutana'),
    ('RY', 'Ruyigi')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU RWANDA (5 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('KIG', 'Kigali'),
    ('EST', 'Est'),
    ('NOR', 'Nord'),
    ('OUE', 'Ouest'),
    ('SUD', 'Sud')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU KENYA (4 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('NAI', 'Nairobi'),
    ('MOM', 'Mombasa'),
    ('KIS', 'Kisumu'),
    ('NAK', 'Nakuru')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DE TANZANIE (4 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('DAR', 'Dar es Salaam'),
    ('DOD', 'Dodoma'),
    ('ARU', 'Arusha'),
    ('MWA', 'Mwanza')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES D'OUGANDA (4 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('KAM', 'Kampala'),
    ('ENT', 'Entebbe'),
    ('GUL', 'Gulu'),
    ('MBA', 'Mbarara')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'UG'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DE RD CONGO (8 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('KIN', 'Kinshasa'),
    ('BAS', 'Bas-Congo'),
    ('BAN', 'Bandundu'),
    ('EQU', 'Équateur'),
    ('KAS', 'Kasaï-Oriental'),
    ('KAT', 'Katanga'),
    ('NOR', 'Nord-Kivu'),
    ('SUD', 'Sud-Kivu')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU CONGO (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('BRA', 'Brazzaville'),
    ('PNR', 'Pointe-Noire')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU CAMEROUN (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('YAO', 'Yaoundé'),
    ('DOU', 'Douala')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU GABON (1 province)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('LIB', 'Libreville')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DE RCA (1 province)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('BAN', 'Bangui')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU SÉNÉGAL (3 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('DAK', 'Dakar'),
    ('THI', 'Thiès'),
    ('SLO', 'Saint-Louis')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DE CÔTE D'IVOIRE (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('ABI', 'Abidjan'),
    ('YAM', 'Yamoussoukro')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU GHANA (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('ACC', 'Accra'),
    ('KUM', 'Kumasi')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU NIGERIA (3 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('ABU', 'Abuja'),
    ('LAG', 'Lagos'),
    ('KAN', 'Kano')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DU MAROC (3 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('RAB', 'Rabat'),
    ('CAS', 'Casablanca'),
    ('MAR', 'Marrakech')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'MA'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES D'ALGÉRIE (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('ALG', 'Alger'),
    ('ORA', 'Oran')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'DZ'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES DE TUNISIE (1 province)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('TUN', 'Tunis')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'TN'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES D'ÉGYPTE (2 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('CAI', 'Le Caire'),
    ('ALE', 'Alexandrie')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'EG'
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PROVINCES D'AFRIQUE DU SUD (3 provinces)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, autorise_systeme, est_actif)
SELECT 
    gen_random_uuid(),
    p.id,
    prov.code,
    prov.nom,
    true,
    true
FROM localisation.pays p
CROSS JOIN (VALUES
    ('GAU', 'Gauteng'),
    ('WCA', 'Western Cape'),
    ('KZN', 'KwaZulu-Natal')
) AS prov(code, nom)
WHERE p.code_iso_2 = 'ZA'
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- AFFICHER LES RÉSULTATS
-- ============================================================================

SELECT 
    pays.nom as pays,
    pays.code_iso_2,
    COUNT(provinces.id) as nb_provinces
FROM localisation.pays pays
LEFT JOIN localisation.provinces provinces ON provinces.pays_id = pays.id
WHERE pays.continent = 'Afrique'
GROUP BY pays.id, pays.nom, pays.code_iso_2
ORDER BY nb_provinces DESC, pays.nom;

-- Total
SELECT COUNT(*) as total_provinces
FROM localisation.provinces
WHERE pays_id IN (
    SELECT id FROM localisation.pays WHERE continent = 'Afrique'
);
