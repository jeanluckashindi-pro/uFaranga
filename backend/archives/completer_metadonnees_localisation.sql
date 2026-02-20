-- Compléter les métadonnées pour provinces, districts et quartiers
-- Connexion: psql -U postgres -d ufaranga -f completer_metadonnees_localisation.sql

BEGIN;

-- ============================================================================
-- PROVINCES - Ajouter métadonnées enrichies
-- ============================================================================

-- Burundi - Provinces
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 850000,
    'superficie_km2', 1089,
    'chef_lieu', 'Bubanza',
    'code_postal', '1000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kirundi', 'Français'],
    'economie_principale', ARRAY['Agriculture', 'Commerce'],
    'sites_touristiques', ARRAY['Parc National de la Kibira']
) WHERE code = 'BB' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1200000,
    'superficie_km2', 87,
    'chef_lieu', 'Bujumbura',
    'code_postal', '1100',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kirundi', 'Français', 'Swahili'],
    'economie_principale', ARRAY['Services', 'Commerce', 'Administration'],
    'sites_touristiques', ARRAY['Lac Tanganyika', 'Musée Vivant', 'Monument de l''Unité']
) WHERE code = 'BM' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1500000,
    'superficie_km2', 1706,
    'chef_lieu', 'Gitega',
    'code_postal', '2000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kirundi', 'Français'],
    'economie_principale', ARRAY['Agriculture', 'Administration'],
    'sites_touristiques', ARRAY['Musée National', 'Tambours sacrés', 'Palais présidentiel']
) WHERE code = 'GI' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 700000,
    'superficie_km2', 1636,
    'chef_lieu', 'Ngozi',
    'code_postal', '3000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kirundi', 'Français'],
    'economie_principale', ARRAY['Agriculture', 'Élevage'],
    'sites_touristiques', ARRAY['Marché de Ngozi']
) WHERE code = 'NG' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');

-- Rwanda - Provinces
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 2600000,
    'superficie_km2', 5883,
    'chef_lieu', 'Rwamagana',
    'code_postal', '30000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kinyarwanda', 'Français', 'Anglais'],
    'economie_principale', ARRAY['Agriculture', 'Élevage', 'Commerce'],
    'sites_touristiques', ARRAY['Parc National Akagera', 'Lac Muhazi']
) WHERE code = 'EST' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1900000,
    'superficie_km2', 3276,
    'chef_lieu', 'Musanze',
    'code_postal', '20000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kinyarwanda', 'Français', 'Anglais'],
    'economie_principale', ARRAY['Tourisme', 'Agriculture'],
    'sites_touristiques', ARRAY['Parc des Volcans', 'Gorilles de montagne', 'Lac Burera']
) WHERE code = 'NOR' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 2500000,
    'superficie_km2', 5963,
    'chef_lieu', 'Karongi',
    'code_postal', '40000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kinyarwanda', 'Français', 'Anglais'],
    'economie_principale', ARRAY['Agriculture', 'Pêche', 'Tourisme'],
    'sites_touristiques', ARRAY['Lac Kivu', 'Parc National Nyungwe']
) WHERE code = 'OUE' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 2900000,
    'superficie_km2', 5964,
    'chef_lieu', 'Huye',
    'code_postal', '50000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kinyarwanda', 'Français', 'Anglais'],
    'economie_principale', ARRAY['Agriculture', 'Éducation'],
    'sites_touristiques', ARRAY['Musée National', 'Université Nationale', 'Arboretum']
) WHERE code = 'SUD' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1300000,
    'superficie_km2', 730,
    'chef_lieu', 'Kigali',
    'code_postal', '10000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Kinyarwanda', 'Français', 'Anglais', 'Swahili'],
    'economie_principale', ARRAY['Services', 'Commerce', 'Technologie', 'Administration'],
    'sites_touristiques', ARRAY['Mémorial du Génocide', 'Centre-ville moderne', 'Marché Kimironko'],
    'est_capitale', true
) WHERE code = 'KIG' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

-- Kenya - Principales provinces
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 4500000,
    'superficie_km2', 696,
    'chef_lieu', 'Nairobi',
    'code_postal', '00100',
    'fuseau_horaire', 'UTC+3',
    'langues_principales', ARRAY['Swahili', 'Anglais', 'Kikuyu'],
    'economie_principale', ARRAY['Services', 'Finance', 'Technologie', 'Tourisme'],
    'sites_touristiques', ARRAY['Parc National de Nairobi', 'Musée National', 'Centre Giraffe'],
    'est_capitale', true
) WHERE code = 'NAI' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1300000,
    'superficie_km2', 229,
    'chef_lieu', 'Mombasa',
    'code_postal', '80100',
    'fuseau_horaire', 'UTC+3',
    'langues_principales', ARRAY['Swahili', 'Anglais'],
    'economie_principale', ARRAY['Port', 'Tourisme', 'Commerce'],
    'sites_touristiques', ARRAY['Fort Jesus', 'Plages', 'Vieille ville']
) WHERE code = 'MOM' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 1200000,
    'superficie_km2', 2009,
    'chef_lieu', 'Kisumu',
    'code_postal', '40100',
    'fuseau_horaire', 'UTC+3',
    'langues_principales', ARRAY['Swahili', 'Anglais', 'Luo'],
    'economie_principale', ARRAY['Pêche', 'Commerce', 'Agriculture'],
    'sites_touristiques', ARRAY['Lac Victoria', 'Musée Kisumu', 'Impala Sanctuary']
) WHERE code = 'KIS' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');

-- RD Congo - Principales provinces
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 15000000,
    'superficie_km2', 9965,
    'chef_lieu', 'Kinshasa',
    'code_postal', '1000',
    'fuseau_horaire', 'UTC+1',
    'langues_principales', ARRAY['Français', 'Lingala', 'Kikongo'],
    'economie_principale', ARRAY['Services', 'Commerce', 'Administration', 'Port'],
    'sites_touristiques', ARRAY['Fleuve Congo', 'Marché Central', 'Académie des Beaux-Arts'],
    'est_capitale', true
) WHERE code = 'KIN' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 8000000,
    'superficie_km2', 132250,
    'chef_lieu', 'Lubumbashi',
    'code_postal', '2000',
    'fuseau_horaire', 'UTC+2',
    'langues_principales', ARRAY['Français', 'Swahili', 'Bemba'],
    'economie_principale', ARRAY['Mines', 'Cuivre', 'Cobalt'],
    'sites_touristiques', ARRAY['Musée National', 'Zoo de Lubumbashi']
) WHERE code = 'KAT' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD');

-- Sénégal - Régions
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 3800000,
    'superficie_km2', 547,
    'chef_lieu', 'Dakar',
    'code_postal', '10000',
    'fuseau_horaire', 'UTC+0',
    'langues_principales', ARRAY['Français', 'Wolof'],
    'economie_principale', ARRAY['Services', 'Port', 'Pêche', 'Tourisme'],
    'sites_touristiques', ARRAY['Île de Gorée', 'Monument de la Renaissance', 'Marché Sandaga'],
    'est_capitale', true
) WHERE code = 'DAK' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'SN');

-- Nigeria - États principaux
UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 3500000,
    'superficie_km2', 1769,
    'chef_lieu', 'Abuja',
    'code_postal', '900001',
    'fuseau_horaire', 'UTC+1',
    'langues_principales', ARRAY['Anglais', 'Hausa', 'Yoruba'],
    'economie_principale', ARRAY['Administration', 'Services', 'Commerce'],
    'sites_touristiques', ARRAY['Aso Rock', 'Mosquée Nationale', 'Millennium Park'],
    'est_capitale', true
) WHERE code = 'FCT' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'NG');

UPDATE localisation.provinces SET metadonnees = jsonb_build_object(
    'population_estimee', 15000000,
    'superficie_km2', 3577,
    'chef_lieu', 'Ikeja',
    'code_postal', '100001',
    'fuseau_horaire', 'UTC+1',
    'langues_principales', ARRAY['Anglais', 'Yoruba', 'Igbo'],
    'economie_principale', ARRAY['Finance', 'Commerce', 'Port', 'Industrie'],
    'sites_touristiques', ARRAY['Île Victoria', 'Lekki Beach', 'Musée National']
) WHERE code = 'LAG' AND pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 = 'NG');

-- ============================================================================
-- TEMPLATE GÉNÉRIQUE pour les provinces sans données spécifiques
-- ============================================================================

-- Mettre à jour toutes les provinces qui n'ont pas encore de métadonnées
UPDATE localisation.provinces pr
SET metadonnees = jsonb_build_object(
    'population_estimee', CASE 
        WHEN pr.nom ILIKE '%capital%' OR pr.nom ILIKE '%ville%' THEN 500000
        ELSE 200000
    END,
    'superficie_km2', 5000,
    'chef_lieu', pr.nom,
    'fuseau_horaire', p.metadonnees->>'fuseau_horaire',
    'langues_principales', p.metadonnees->'langues',
    'economie_principale', ARRAY['Agriculture', 'Commerce'],
    'derniere_mise_a_jour', CURRENT_DATE::text
)
FROM localisation.pays p
WHERE pr.pays_id = p.id
AND (pr.metadonnees IS NULL OR pr.metadonnees = '{}'::jsonb);

COMMIT;

-- ============================================================================
-- Vérifier les résultats
-- ============================================================================

-- Compter les provinces avec métadonnées
SELECT 
    'Provinces' as niveau,
    COUNT(*) as total,
    COUNT(CASE WHEN metadonnees IS NOT NULL AND metadonnees != '{}'::jsonb THEN 1 END) as avec_metadonnees,
    ROUND(COUNT(CASE WHEN metadonnees IS NOT NULL AND metadonnees != '{}'::jsonb THEN 1 END) * 100.0 / COUNT(*), 2) as pourcentage
FROM localisation.provinces;

-- Exemples de métadonnées
SELECT 
    p.nom as pays,
    pr.nom as province,
    pr.metadonnees->>'population_estimee' as population,
    pr.metadonnees->>'chef_lieu' as chef_lieu,
    pr.metadonnees->>'economie_principale' as economie
FROM localisation.provinces pr
JOIN localisation.pays p ON pr.pays_id = p.id
WHERE pr.metadonnees IS NOT NULL 
AND pr.metadonnees != '{}'::jsonb
LIMIT 10;
