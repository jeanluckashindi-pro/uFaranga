-- Peupler toutes les provinces avec coordonnées GPS
-- Connexion: psql -U postgres -d ufaranga -f peupler_provinces_gps.sql

BEGIN;

-- Supprimer les doublons d'abord
DELETE FROM localisation.provinces a USING localisation.provinces b
WHERE a.id < b.id AND a.pays_id = b.pays_id AND a.code = b.code;

-- BURUNDI - Mettre à jour avec GPS
UPDATE localisation.provinces SET latitude_centre = -3.0833, longitude_centre = 29.3833 WHERE code = 'BB' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.3822, longitude_centre = 29.3644 WHERE code = 'BM' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.5000, longitude_centre = 29.5000 WHERE code = 'BR' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.9500, longitude_centre = 29.6167 WHERE code = 'BU' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.2167, longitude_centre = 30.6000 WHERE code = 'CA' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -2.8833, longitude_centre = 29.1167 WHERE code = 'CI' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.4271, longitude_centre = 29.9246 WHERE code = 'GI' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -2.5833, longitude_centre = 30.1000 WHERE code = 'KI' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.1000, longitude_centre = 30.1667 WHERE code = 'KR' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -2.9167, longitude_centre = 29.6333 WHERE code = 'KY' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -4.1333, longitude_centre = 29.8000 WHERE code = 'MA' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.2667, longitude_centre = 29.6167 WHERE code = 'MU' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.5167, longitude_centre = 29.7000 WHERE code = 'MW' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -2.8500, longitude_centre = 30.3333 WHERE code = 'MY' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -2.9167, longitude_centre = 29.8333 WHERE code = 'NG' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.9333, longitude_centre = 30.0000 WHERE code = 'RT' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');
UPDATE localisation.provinces SET latitude_centre = -3.4833, longitude_centre = 30.2500 WHERE code = 'RY' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'BI');

-- RWANDA - Mettre à jour avec GPS
UPDATE localisation.provinces SET latitude_centre = -1.9536, longitude_centre = 30.0606 WHERE code = 'KIG' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');
UPDATE localisation.provinces SET latitude_centre = -2.0000, longitude_centre = 30.5000 WHERE code = 'EST' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');
UPDATE localisation.provinces SET latitude_centre = -1.5000, longitude_centre = 29.8000 WHERE code = 'NOR' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');
UPDATE localisation.provinces SET latitude_centre = -2.0000, longitude_centre = 29.3000 WHERE code = 'OUE' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');
UPDATE localisation.provinces SET latitude_centre = -2.5000, longitude_centre = 29.7000 WHERE code = 'SUD' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'RW');

-- KENYA - Mettre à jour avec GPS
UPDATE localisation.provinces SET latitude_centre = -1.2921, longitude_centre = 36.8219 WHERE code = 'NAI' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');
UPDATE localisation.provinces SET latitude_centre = -4.0435, longitude_centre = 39.6682 WHERE code = 'MOM' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');
UPDATE localisation.provinces SET latitude_centre = -0.0917, longitude_centre = 34.7680 WHERE code = 'KIS' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');
UPDATE localisation.provinces SET latitude_centre = -0.3031, longitude_centre = 36.0800 WHERE code = 'NAK' AND pays_id = (SELECT id FROM localisation.pays WHERE code_iso_2 = 'KE');

COMMIT;

-- Vérifier
SELECT 
    pays.nom as pays,
    provinces.code,
    provinces.nom,
    provinces.latitude_centre,
    provinces.longitude_centre
FROM localisation.provinces provinces
JOIN localisation.pays pays ON pays.id = provinces.pays_id
WHERE pays.continent = 'Afrique'
AND provinces.latitude_centre IS NOT NULL
ORDER BY pays.nom, provinces.nom
LIMIT 20;
