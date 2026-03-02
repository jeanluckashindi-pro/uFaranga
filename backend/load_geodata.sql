-- Chargement des données géographiques réelles pour Burundi et RDC
-- Source: Natural Earth Data et OpenStreetMap

-- ============================================================================
-- BURUNDI - Données géographiques
-- ============================================================================

-- Frontières du Burundi (simplifié)
UPDATE localisation.pays
SET geometrie = ST_GeomFromText('MULTIPOLYGON(((
    29.339998 -4.499983,
    29.276384 -3.293907,
    29.024926 -2.839258,
    29.632176 -2.917858,
    30.469696 -2.413858,
    30.527677 -2.807632,
    30.743013 -3.034285,
    30.752263 -3.359766,
    30.506766 -3.568567,
    30.116333 -4.090138,
    29.753512 -4.452389,
    29.339998 -4.499983
)))', 4326),
centre_geo = ST_SetSRID(ST_MakePoint(29.9189, -3.3731), 4326),
centre_latitude = -3.3731,
centre_longitude = 29.9189,
bbox_nord = -2.310123,
bbox_sud = -4.465713,
bbox_est = 30.847729,
bbox_ouest = 28.993061,
superficie_km2 = 27834
WHERE code_iso_2 = 'BI';

-- ============================================================================
-- RDC - Données géographiques
-- ============================================================================

-- Frontières de la RDC (très simplifié - le pays est immense)
UPDATE localisation.pays
SET geometrie = ST_GeomFromText('MULTIPOLYGON(((
    30.83 3.50,
    29.95 2.80,
    29.58 1.34,
    29.58 0.59,
    29.82 -0.20,
    29.88 -1.45,
    29.58 -1.34,
    29.58 -2.92,
    29.28 -3.29,
    29.25 -4.45,
    29.08 -5.65,
    29.42 -5.94,
    29.52 -6.31,
    30.20 -7.08,
    30.74 -8.34,
    28.88 -8.48,
    28.35 -9.20,
    28.73 -9.61,
    28.45 -10.79,
    28.37 -11.49,
    29.34 -12.36,
    29.62 -13.39,
    28.93 -13.25,
    28.52 -12.69,
    27.39 -12.13,
    27.16 -11.61,
    26.55 -11.92,
    25.75 -11.78,
    25.42 -11.33,
    24.78 -11.24,
    24.31 -11.26,
    24.26 -10.95,
    23.91 -10.93,
    23.46 -10.87,
    22.84 -11.02,
    22.40 -10.99,
    22.21 -11.09,
    22.06 -9.89,
    21.73 -9.41,
    21.80 -8.91,
    21.88 -7.97,
    21.75 -7.29,
    20.60 -7.28,
    20.51 -6.94,
    19.89 -6.98,
    19.49 -7.15,
    19.01 -7.99,
    18.46 -8.04,
    18.13 -7.99,
    17.47 -8.07,
    17.09 -7.55,
    16.86 -7.22,
    16.58 -6.62,
    16.33 -5.87,
    13.38 -5.86,
    13.02 -5.98,
    12.74 -5.96,
    12.32 -6.10,
    12.18 -5.79,
    12.44 -5.68,
    12.47 -5.25,
    12.64 -4.99,
    12.99 -4.78,
    13.26 -4.88,
    13.60 -4.50,
    14.14 -4.51,
    14.21 -4.79,
    14.58 -4.97,
    15.17 -4.34,
    15.75 -3.86,
    16.00 -3.54,
    15.97 -2.71,
    16.41 -1.74,
    16.87 -1.23,
    17.52 -0.74,
    17.64 -0.42,
    17.66 0.23,
    17.77 0.86,
    17.83 1.39,
    18.09 2.37,
    18.54 2.90,
    18.62 3.47,
    18.45 4.25,
    19.47 5.03,
    20.29 4.69,
    20.93 4.32,
    22.04 4.15,
    22.70 4.63,
    23.55 4.62,
    24.39 5.10,
    24.81 4.90,
    25.07 4.79,
    25.28 5.17,
    26.40 5.15,
    27.04 5.13,
    27.37 5.23,
    27.98 4.41,
    28.43 4.29,
    28.70 4.46,
    29.16 4.39,
    29.72 4.60,
    30.42 3.98,
    30.83 3.50
)))', 4326),
centre_geo = ST_SetSRID(ST_MakePoint(23.6566, -4.0383), 4326),
centre_latitude = -4.0383,
centre_longitude = 23.6566,
bbox_nord = 5.386098,
bbox_sud = -13.455675,
bbox_est = 31.305912,
bbox_ouest = 12.204144,
superficie_km2 = 2344858
WHERE code_iso_2 = 'CD';

-- ============================================================================
-- RWANDA - Données géographiques (voisin du Burundi)
-- ============================================================================

UPDATE localisation.pays
SET geometrie = ST_GeomFromText('MULTIPOLYGON(((
    30.42 -1.13,
    30.82 -1.70,
    30.76 -2.29,
    30.47 -2.41,
    29.94 -2.34,
    29.63 -2.92,
    29.02 -2.84,
    29.12 -2.29,
    29.25 -2.21,
    29.29 -1.62,
    29.58 -1.34,
    29.82 -1.44,
    30.42 -1.13
)))', 4326),
centre_geo = ST_SetSRID(ST_MakePoint(29.8739, -1.9403), 4326),
centre_latitude = -1.9403,
centre_longitude = 29.8739,
bbox_nord = -1.047,
bbox_sud = -2.840,
bbox_est = 30.895,
bbox_ouest = 28.862,
superficie_km2 = 26338
WHERE code_iso_2 = 'RW';

-- ============================================================================
-- TANZANIE - Données géographiques (voisin du Burundi)
-- ============================================================================

UPDATE localisation.pays
SET geometrie = ST_GeomFromText('MULTIPOLYGON(((
    33.90 -0.95,
    34.07 -1.05,
    37.69 -3.09,
    37.77 -3.67,
    39.20 -4.67,
    38.74 -5.90,
    38.79 -6.47,
    39.44 -6.84,
    39.47 -7.10,
    39.19 -7.70,
    39.25 -8.01,
    39.19 -8.49,
    39.54 -9.11,
    39.95 -10.10,
    40.32 -10.32,
    39.52 -10.90,
    38.43 -11.29,
    37.83 -11.27,
    37.47 -11.57,
    36.78 -11.59,
    36.51 -11.72,
    35.31 -11.44,
    34.56 -11.52,
    34.28 -10.16,
    33.94 -9.69,
    33.74 -9.42,
    32.76 -9.23,
    32.19 -8.93,
    31.56 -8.76,
    31.16 -8.61,
    30.74 -8.34,
    30.20 -7.08,
    29.62 -6.52,
    29.42 -5.94,
    29.52 -5.42,
    29.34 -4.98,
    29.75 -4.45,
    30.12 -4.09,
    30.51 -3.57,
    30.75 -3.03,
    30.74 -2.41,
    30.47 -2.41,
    30.42 -1.13,
    30.77 -1.01,
    31.86 -1.03,
    33.90 -0.95
)))', 4326),
centre_geo = ST_SetSRID(ST_MakePoint(34.8888, -6.3690), 4326),
centre_latitude = -6.3690,
centre_longitude = 34.8888,
bbox_nord = -0.984,
bbox_sud = -11.745,
bbox_est = 40.444,
bbox_ouest = 29.340,
superficie_km2 = 947303
WHERE code_iso_2 = 'TZ';

-- ============================================================================
-- Vérification des données chargées
-- ============================================================================

SELECT 
    nom,
    code_iso_2,
    ROUND(superficie_km2::numeric, 0) as superficie_km2,
    ST_AsText(centre_geo) as centre,
    ST_GeometryType(geometrie) as type_geometrie,
    ST_NPoints(geometrie) as nombre_points,
    CASE 
        WHEN geometrie IS NOT NULL THEN 'OUI'
        ELSE 'NON'
    END as geometrie_chargee
FROM localisation.pays
WHERE code_iso_2 IN ('BI', 'CD', 'RW', 'TZ')
ORDER BY nom;

-- Test de distance entre pays
SELECT 
    p1.nom as pays_depart,
    p2.nom as pays_arrivee,
    ROUND(ST_Distance(p1.centre_geo::geography, p2.centre_geo::geography)/1000) as distance_km,
    CASE 
        WHEN ST_Touches(p1.geometrie, p2.geometrie) THEN 'Frontière commune'
        WHEN ST_Distance(p1.geometrie, p2.geometrie) < 0.01 THEN 'Très proche'
        ELSE 'Séparés'
    END as relation
FROM localisation.pays p1
CROSS JOIN localisation.pays p2
WHERE p1.code_iso_2 = 'BI' 
  AND p2.code_iso_2 IN ('CD', 'RW', 'TZ')
ORDER BY distance_km;
