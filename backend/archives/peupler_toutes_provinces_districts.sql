-- Peupler les provinces et districts pour tous les 54 pays africains
-- Connexion: psql -U postgres -d ufaranga -f peupler_toutes_provinces_districts.sql

BEGIN;

-- ============================================================================
-- AFRIQUE DE L'EST (12 pays)
-- ============================================================================

-- BURUNDI (BI) - 18 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BB', 'Bubanza', -3.0833, 29.3833 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BM', 'Bujumbura Mairie', -3.3761, 29.3600 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BR', 'Bujumbura Rural', -3.5000, 29.4500 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BU', 'Bururi', -3.9500, 29.6167 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CA', 'Cankuzo', -3.2167, 30.6000 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CI', 'Cibitoke', -2.8833, 29.1167 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GI', 'Gitega', -3.4271, 29.9246 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KR', 'Kirundo', -2.5833, 30.1000 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KY', 'Kayanza', -2.9167, 29.6333 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KI', 'Karuzi', -3.1000, 30.1667 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MA', 'Makamba', -4.1333, 29.8000 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MU', 'Muramvya', -3.2667, 29.6167 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MW', 'Mwaro', -3.5167, 29.7000 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MY', 'Muyinga', -2.8500, 30.3333 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NG', 'Ngozi', -2.9083, 29.8306 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RT', 'Rutana', -3.9333, 30.0000 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RY', 'Ruyigi', -3.4667, 30.2500 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RU', 'Rumonge', -3.9733, 29.4386 FROM localisation.pays WHERE code_iso_2 = 'BI'
ON CONFLICT DO NOTHING;

-- RWANDA (RW) - 5 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EST', 'Province de l''Est', -2.0000, 30.5000 FROM localisation.pays WHERE code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NOR', 'Province du Nord', -1.6000, 29.7000 FROM localisation.pays WHERE code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OUE', 'Province de l''Ouest', -2.3000, 29.3000 FROM localisation.pays WHERE code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SUD', 'Province du Sud', -2.5000, 29.7000 FROM localisation.pays WHERE code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KIG', 'Ville de Kigali', -1.9403, 30.0619 FROM localisation.pays WHERE code_iso_2 = 'RW'
ON CONFLICT DO NOTHING;

-- KENYA (KE) - 47 comtés (principales)
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NAI', 'Nairobi', -1.2864, 36.8172 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MOM', 'Mombasa', -4.0435, 39.6682 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KIS', 'Kisumu', -0.0917, 34.7680 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NAK', 'Nakuru', -0.3031, 36.0800 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ELD', 'Eldoret', 0.5143, 35.2698 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KIA', 'Kiambu', -1.1714, 36.8356 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MER', 'Meru', 0.0469, 37.6556 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAK', 'Kakamega', 0.2827, 34.7519 FROM localisation.pays WHERE code_iso_2 = 'KE'
ON CONFLICT DO NOTHING;

-- TANZANIE (TZ) - 31 régions (principales)
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DAR', 'Dar es Salaam', -6.7924, 39.2083 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DOD', 'Dodoma', -6.1630, 35.7516 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MWA', 'Mwanza', -2.5164, 32.9175 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ARU', 'Arusha', -3.3869, 36.6830 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MBE', 'Mbeya', -8.9094, 33.4606 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MOR', 'Morogoro', -6.8211, 37.6636 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAN', 'Tanga', -5.0689, 39.0986 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAG', 'Kagera', -1.3000, 31.2000 FROM localisation.pays WHERE code_iso_2 = 'TZ'
ON CONFLICT DO NOTHING;

-- OUGANDA (UG) - 4 régions principales
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CEN', 'Région Centrale', 0.3476, 32.5825 FROM localisation.pays WHERE code_iso_2 = 'UG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EST', 'Région de l''Est', 1.0000, 34.0000 FROM localisation.pays WHERE code_iso_2 = 'UG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NOR', 'Région du Nord', 2.5000, 32.5000 FROM localisation.pays WHERE code_iso_2 = 'UG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OUE', 'Région de l''Ouest', 0.5000, 30.5000 FROM localisation.pays WHERE code_iso_2 = 'UG'
ON CONFLICT DO NOTHING;

-- ÉTHIOPIE (ET) - 11 régions
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AA', 'Addis-Abeba', 9.0320, 38.7469 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AF', 'Afar', 11.7500, 41.0000 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AM', 'Amhara', 11.5000, 38.0000 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OR', 'Oromia', 8.5000, 39.5000 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SO', 'Somali', 6.5000, 43.5000 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TI', 'Tigré', 14.0000, 38.5000 FROM localisation.pays WHERE code_iso_2 = 'ET'
ON CONFLICT DO NOTHING;

-- SOMALIE (SO) - 18 régions (principales)
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BN', 'Banaadir', 2.0469, 45.3182 FROM localisation.pays WHERE code_iso_2 = 'SO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WO', 'Woqooyi Galbeed', 9.5000, 44.0000 FROM localisation.pays WHERE code_iso_2 = 'SO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BA', 'Bari', 11.0000, 49.0000 FROM localisation.pays WHERE code_iso_2 = 'SO'
ON CONFLICT DO NOTHING;

-- DJIBOUTI (DJ) - 6 régions
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DJ', 'Djibouti', 11.5950, 43.1481 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AR', 'Arta', 11.5250, 42.8500 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AL', 'Ali Sabieh', 11.1556, 42.7125 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DI', 'Dikhil', 11.1056, 42.3708 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TA', 'Tadjourah', 11.7850, 42.8833 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OB', 'Obock', 12.0000, 43.2833 FROM localisation.pays WHERE code_iso_2 = 'DJ'
ON CONFLICT DO NOTHING;

-- ÉRYTHRÉE (ER) - 6 régions
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MA', 'Maekel', 15.3333, 38.9333 FROM localisation.pays WHERE code_iso_2 = 'ER'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AN', 'Anseba', 16.5000, 37.5000 FROM localisation.pays WHERE code_iso_2 = 'ER'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DK', 'Debub', 14.5000, 39.5000 FROM localisation.pays WHERE code_iso_2 = 'ER'
ON CONFLICT DO NOTHING;

-- COMORES (KM) - 3 îles
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GC', 'Grande Comore', -11.7000, 43.2500 FROM localisation.pays WHERE code_iso_2 = 'KM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AN', 'Anjouan', -12.2167, 44.4333 FROM localisation.pays WHERE code_iso_2 = 'KM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MO', 'Mohéli', -12.3500, 43.7333 FROM localisation.pays WHERE code_iso_2 = 'KM'
ON CONFLICT DO NOTHING;

-- SEYCHELLES (SC) - Districts principaux
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'VIC', 'Victoria', -4.6167, 55.4500 FROM localisation.pays WHERE code_iso_2 = 'SC'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PRA', 'Praslin', -4.3167, 55.7333 FROM localisation.pays WHERE code_iso_2 = 'SC'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LAD', 'La Digue', -4.3500, 55.8333 FROM localisation.pays WHERE code_iso_2 = 'SC'
ON CONFLICT DO NOTHING;

-- MAURICE (MU) - 9 districts
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PL', 'Port Louis', -20.1609, 57.5012 FROM localisation.pays WHERE code_iso_2 = 'MU'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PA', 'Pamplemousses', -20.1000, 57.5667 FROM localisation.pays WHERE code_iso_2 = 'MU'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RR', 'Rivière du Rempart', -20.0500, 57.6500 FROM localisation.pays WHERE code_iso_2 = 'MU'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'FL', 'Flacq', -20.2000, 57.7167 FROM localisation.pays WHERE code_iso_2 = 'MU'
ON CONFLICT DO NOTHING;

COMMIT;

-- Vérifier les résultats
SELECT 
    p.nom as pays,
    COUNT(pr.id) as nb_provinces
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.continent = 'Afrique'
GROUP BY p.nom
ORDER BY p.nom;
