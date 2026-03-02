-- Nettoyage et chargement des VRAIES données officielles
-- Burundi: 18 provinces (2023)
-- RDC: 26 provinces (depuis 2015)

-- ============================================================================
-- BURUNDI: 18 Provinces officielles (2023)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, centre_latitude, centre_longitude, est_actif, autorise_systeme, date_creation, metadonnees)
SELECT 
    gen_random_uuid(),
    (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI'),
    code,
    nom,
    lat,
    lon,
    true,
    true,
    NOW(),
    '{}'::jsonb
FROM (VALUES
    ('BI-BB', 'Bubanza', -3.0833, 29.3833),
    ('BI-BM', 'Bujumbura Mairie', -3.3822, 29.3644),
    ('BI-BL', 'Bujumbura Rural', -3.5000, 29.5000),
    ('BI-BR', 'Bururi', -3.9500, 29.6167),
    ('BI-CA', 'Cankuzo', -3.2167, 30.6000),
    ('BI-CI', 'Cibitoke', -2.8833, 29.1167),
    ('BI-GI', 'Gitega', -3.4271, 29.9246),
    ('BI-KR', 'Karuzi', -3.1000, 30.1667),
    ('BI-KY', 'Kayanza', -2.9167, 29.6333),
    ('BI-KI', 'Kirundo', -2.5833, 30.1000),
    ('BI-MA', 'Makamba', -4.1333, 29.8000),
    ('BI-MU', 'Muramvya', -3.2667, 29.6167),
    ('BI-MY', 'Muyinga', -2.8500, 30.3333),
    ('BI-MW', 'Mwaro', -3.5167, 29.7000),
    ('BI-NG', 'Ngozi', -2.9083, 29.8306),
    ('BI-RM', 'Rumonge', -3.9733, 29.4386),
    ('BI-RT', 'Rutana', -3.9267, 30.0000),
    ('BI-RY', 'Ruyigi', -3.4833, 30.2500)
) AS t(code, nom, lat, lon);

-- Mettre à jour les géométries PostGIS pour les provinces du Burundi
UPDATE localisation.provinces
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI')
  AND centre_longitude IS NOT NULL;

-- ============================================================================
-- RDC: 26 Provinces officielles (depuis 2015)
-- ============================================================================

INSERT INTO localisation.provinces (id, pays_id, code, nom, centre_latitude, centre_longitude, est_actif, autorise_systeme, date_creation, metadonnees)
SELECT 
    gen_random_uuid(),
    (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD'),
    code,
    nom,
    lat,
    lon,
    true,
    true,
    NOW(),
    '{}'::jsonb
FROM (VALUES
    ('CD-KN', 'Kinshasa', -4.3276, 15.3136),
    ('CD-BC', 'Kongo Central', -5.0333, 14.8500),
    ('CD-KL', 'Kwilu', -5.0333, 18.7667),
    ('CD-KG', 'Kwango', -5.0333, 17.5000),
    ('CD-MN', 'Mai-Ndombe', -2.0000, 18.5000),
    ('CD-EQ', 'Équateur', 0.0000, 23.0000),
    ('CD-MO', 'Mongala', 1.8333, 21.1667),
    ('CD-NU', 'Nord-Ubangi', 3.4667, 21.2167),
    ('CD-SU', 'Sud-Ubangi', 2.8333, 21.7500),
    ('CD-TS', 'Tshuapa', -1.0000, 22.4167),
    ('CD-IT', 'Ituri', 1.6667, 29.0000),
    ('CD-HU', 'Haut-Uélé', 3.4167, 28.3333),
    ('CD-TO', 'Tshopo', 0.5167, 25.1833),
    ('CD-BU', 'Bas-Uélé', 2.3333, 24.0000),
    ('CD-NK', 'Nord-Kivu', -0.7167, 29.2333),
    ('CD-SK', 'Sud-Kivu', -2.5000, 28.8667),
    ('CD-MA', 'Maniema', -2.8833, 26.1500),
    ('CD-TA', 'Tanganyika', -6.1000, 27.5833),
    ('CD-HK', 'Haut-Katanga', -11.6667, 27.4833),
    ('CD-LU', 'Lualaba', -10.7000, 25.6667),
    ('CD-HL', 'Haut-Lomami', -8.8000, 25.3667),
    ('CD-LO', 'Lomami', -6.1500, 24.4833),
    ('CD-SA', 'Sankuru', -2.9167, 23.6167),
    ('CD-KC', 'Kasaï Central', -5.9000, 22.4167),
    ('CD-KE', 'Kasaï Oriental', -4.3333, 23.5833),
    ('CD-KS', 'Kasaï', -5.0333, 20.7500)
) AS t(code, nom, lat, lon);

-- Mettre à jour les géométries PostGIS pour les provinces de la RDC
UPDATE localisation.provinces
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'CD')
  AND centre_longitude IS NOT NULL;

-- ============================================================================
-- VÉRIFICATION
-- ============================================================================

SELECT 
    p.nom as pays,
    p.code_iso_2,
    COUNT(pr.id) as nb_provinces_officielles,
    COUNT(pr.centre_geo) as nb_avec_geometrie
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.code_iso_2 IN ('BI', 'CD')
GROUP BY p.nom, p.code_iso_2
ORDER BY p.nom;

-- Liste des provinces
SELECT 
    p.nom as pays,
    pr.code,
    pr.nom as province,
    ST_AsText(pr.centre_geo) as position
FROM localisation.provinces pr
JOIN localisation.pays p ON pr.pays_id = p.id
WHERE p.code_iso_2 IN ('BI', 'CD')
ORDER BY p.nom, pr.nom;
