-- Peupler les provinces pour Afrique de l'Ouest
-- Connexion: psql -U postgres -d ufaranga -f peupler_provinces_afrique_de_l'ouest.sql

BEGIN;

-- SN - 14 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DAK', 'Dakar', 14.6928, -17.4467 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'THI', 'Thiès', 14.7886, -16.9261 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DIO', 'Diourbel', 14.6542, -16.2292 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'FAT', 'Fatick', 14.3397, -16.4111 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAO', 'Kaolack', 14.15, -16.0667 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KOL', 'Kolda', 12.8833, -14.95 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LOU', 'Louga', 15.6167, -16.2167 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAT', 'Matam', 15.6556, -13.2553 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SLO', 'Saint-Louis', 16.0181, -16.4897 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SED', 'Sédhiou', 12.7081, -15.5569 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAM', 'Tambacounda', 13.7708, -13.6681 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KED', 'Kédougou', 12.5569, -12.1744 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAF', 'Kaffrine', 14.1056, -15.55 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ZIG', 'Ziguinchor', 12.5833, -16.2667 FROM localisation.pays WHERE code_iso_2 = 'SN'
ON CONFLICT DO NOTHING;


-- CI - 12 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ABI', 'Abidjan', 5.36, -4.0083 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'YAM', 'Yamoussoukro', 6.8276, -5.2893 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOU', 'Bouaké', 7.69, -5.03 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DAL', 'Daloa', 6.8772, -6.4503 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KOR', 'Korhogo', 9.4581, -5.6297 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAN', 'San-Pédro', 4.75, -6.6333 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAN', 'Man', 7.4125, -7.5539 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ABO', 'Aboisso', 5.4667, -3.2 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ABI', 'Abengourou', 6.7297, -3.4964 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AGN', 'Agnibilékrou', 7.1333, -3.2 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAN', 'Bangolo', 7.0167, -7.4833 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BIA', 'Biankouma', 7.7333, -7.6167 FROM localisation.pays WHERE code_iso_2 = 'CI'
ON CONFLICT DO NOTHING;


-- GH - 16 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GAR', 'Greater Accra', 5.6037, -0.187 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ASH', 'Ashanti', 6.75, -1.6 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WES', 'Western', 5.0, -2.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CEN', 'Central', 5.5, -1.0 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EAS', 'Eastern', 6.25, -0.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'VOL', 'Volta', 6.5, 0.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NOR', 'Northern', 9.5, -1.0 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'UE', 'Upper East', 10.75, -0.8333 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'UW', 'Upper West', 10.25, -2.25 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAH', 'Bono', 7.6667, -2.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BE', 'Bono East', 7.75, -1.05 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AHA', 'Ahafo', 7.25, -2.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OTI', 'Oti', 7.9, 0.3 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAV', 'Savannah', 9.0833, -1.5 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NE', 'North East', 10.5, -0.3333 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WN', 'Western North', 6.2, -2.75 FROM localisation.pays WHERE code_iso_2 = 'GH'
ON CONFLICT DO NOTHING;


-- NG - 16 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'FCT', 'Abuja FCT', 9.0765, 7.3986 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LAG', 'Lagos', 6.5244, 3.3792 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAN', 'Kano', 12.0022, 8.592 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAD', 'Kaduna', 10.5105, 7.4165 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'IBA', 'Ibadan', 7.3775, 3.947 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PH', 'Port Harcourt', 4.8156, 7.0498 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BEN', 'Benin City', 6.335, 5.6037 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAI', 'Maiduguri', 11.8333, 13.15 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ZAR', 'Zaria', 11.0667, 7.7 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ABA', 'Aba', 5.1167, 7.3667 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'JOS', 'Jos', 9.9167, 8.8833 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ILO', 'Ilorin', 8.4966, 4.5425 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OWE', 'Owerri', 5.4833, 7.0333 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ENE', 'Enugu', 6.4403, 7.4914 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ABI', 'Abeokuta', 7.1475, 3.3619 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AKU', 'Akure', 7.2571, 5.2058 FROM localisation.pays WHERE code_iso_2 = 'NG'
ON CONFLICT DO NOTHING;


-- BJ - 12 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ALA', 'Alibori', 11.0, 2.6667 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ATL', 'Atlantique', 6.6667, 2.2333 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ATA', 'Atacora', 10.5, 1.6667 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOR', 'Borgou', 9.5, 2.6667 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'COL', 'Collines', 8.0, 2.3333 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'COU', 'Couffo', 7.0, 1.75 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DON', 'Donga', 9.7, 1.6667 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LIT', 'Littoral', 6.3654, 2.4183 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MON', 'Mono', 6.5, 1.75 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OUE', 'Ouémé', 6.5, 2.6 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PLA', 'Plateau', 7.25, 2.6 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ZOU', 'Zou', 7.3333, 2.1667 FROM localisation.pays WHERE code_iso_2 = 'BJ'
ON CONFLICT DO NOTHING;


-- TG - 5 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAR', 'Maritime', 6.1256, 1.2256 FROM localisation.pays WHERE code_iso_2 = 'TG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PLA', 'Plateaux', 7.5333, 1.1667 FROM localisation.pays WHERE code_iso_2 = 'TG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CEN', 'Centrale', 8.9833, 1.0833 FROM localisation.pays WHERE code_iso_2 = 'TG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAR', 'Kara', 9.55, 1.1833 FROM localisation.pays WHERE code_iso_2 = 'TG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAV', 'Savanes', 10.5, 0.5 FROM localisation.pays WHERE code_iso_2 = 'TG'
ON CONFLICT DO NOTHING;


-- BF - 13 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CEN', 'Centre', 12.3714, -1.5197 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOU', 'Boucle du Mouhoun', 12.25, -3.5 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CAS', 'Cascades', 10.5, -4.5 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CNO', 'Centre-Nord', 13.0, -1.0 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CES', 'Centre-Est', 11.5, 0.0 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'COU', 'Centre-Ouest', 12.0, -2.5 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CSU', 'Centre-Sud', 11.5, -1.0 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EST', 'Est', 12.0, 0.5 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HAU', 'Hauts-Bassins', 11.1833, -4.3 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NOR', 'Nord', 13.5, -2.0 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PLA', 'Plateau-Central', 12.3, -0.75 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAH', 'Sahel', 14.0, -0.5 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SOU', 'Sud-Ouest', 10.5, -3.0 FROM localisation.pays WHERE code_iso_2 = 'BF'
ON CONFLICT DO NOTHING;


-- ML - 11 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BKO', 'Bamako', 12.6392, -8.0029 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAY', 'Kayes', 14.45, -11.4333 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KOU', 'Koulikoro', 12.8622, -7.5597 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SIK', 'Sikasso', 11.3167, -5.6667 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SEG', 'Ségou', 13.4317, -6.2633 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MOP', 'Mopti', 14.4833, -4.1833 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TOM', 'Tombouctou', 16.7667, -3.0167 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GAO', 'Gao', 16.2667, -0.05 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KID', 'Kidal', 18.4411, 1.4078 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MEN', 'Ménaka', 15.9167, 2.4 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAO', 'Taoudénit', 22.6833, -3.9833 FROM localisation.pays WHERE code_iso_2 = 'ML'
ON CONFLICT DO NOTHING;


-- NE - 8 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NIA', 'Niamey', 13.5127, 2.1128 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AGA', 'Agadez', 16.9735, 7.9911 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DIF', 'Diffa', 13.3156, 12.6113 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DOS', 'Dosso', 13.05, 3.1944 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAR', 'Maradi', 13.5, 7.1017 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAH', 'Tahoua', 14.8903, 5.2653 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TIL', 'Tillabéri', 14.2111, 1.4528 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ZIN', 'Zinder', 13.8069, 8.9881 FROM localisation.pays WHERE code_iso_2 = 'NE'
ON CONFLICT DO NOTHING;


-- MR - 13 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NKC', 'Nouakchott', 18.0858, -15.9785 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HOD', 'Hodh Ech Chargui', 18.5, -7.0 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HOG', 'Hodh El Gharbi', 16.6667, -9.5 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ASS', 'Assaba', 16.75, -11.5 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GOR', 'Gorgol', 15.9667, -12.6333 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BRA', 'Brakna', 17.2333, -13.05 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TRA', 'Trarza', 17.8667, -14.65 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ADR', 'Adrar', 20.5, -10.0 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'DAK', 'Dakhlet Nouadhibou', 20.9, -17.0333 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAG', 'Tagant', 18.55, -9.9 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GUI', 'Guidimaka', 15.25, -12.25 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TIR', 'Tiris Zemmour', 24.5, -9.5 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'INC', 'Inchiri', 20.0, -15.5 FROM localisation.pays WHERE code_iso_2 = 'MR'
ON CONFLICT DO NOTHING;


-- GM - 6 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAN', 'Banjul', 13.4549, -16.579 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WES', 'Western', 13.35, -16.6 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LRR', 'Lower River', 13.3833, -15.8333 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CRR', 'Central River', 13.5833, -14.8333 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NBR', 'North Bank', 13.5, -15.8333 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'URR', 'Upper River', 13.45, -13.8 FROM localisation.pays WHERE code_iso_2 = 'GM'
ON CONFLICT DO NOTHING;


-- GN - 8 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CON', 'Conakry', 9.6412, -13.5784 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOK', 'Boké', 10.9333, -14.2833 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'FAR', 'Faranah', 10.0333, -10.7333 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAN', 'Kankan', 10.3833, -9.3 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KIN', 'Kindia', 10.05, -12.85 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LAB', 'Labé', 11.3167, -12.2833 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAM', 'Mamou', 10.375, -12.0833 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NZE', 'Nzérékoré', 7.75, -8.8167 FROM localisation.pays WHERE code_iso_2 = 'GN'
ON CONFLICT DO NOTHING;


-- GW - 9 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BIS', 'Bissau', 11.8636, -15.5982 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAF', 'Bafatá', 12.1667, -14.65 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BIO', 'Biombo', 11.8833, -15.7333 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOL', 'Bolama', 11.5833, -15.4833 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CAC', 'Cacheu', 12.2667, -16.1667 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GAB', 'Gabú', 12.2833, -14.2167 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OIO', 'Oio', 12.45, -15.2167 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'QUI', 'Quinara', 11.8833, -15.1833 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TOM', 'Tombali', 11.3333, -14.9833 FROM localisation.pays WHERE code_iso_2 = 'GW'
ON CONFLICT DO NOTHING;


-- SL - 5 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WES', 'Western Area', 8.4657, -13.2317 FROM localisation.pays WHERE code_iso_2 = 'SL'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NOR', 'Northern', 9.5, -12.0 FROM localisation.pays WHERE code_iso_2 = 'SL'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SOU', 'Southern', 7.8833, -11.75 FROM localisation.pays WHERE code_iso_2 = 'SL'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EAS', 'Eastern', 8.1667, -10.8333 FROM localisation.pays WHERE code_iso_2 = 'SL'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NWE', 'North West', 8.8833, -12.9167 FROM localisation.pays WHERE code_iso_2 = 'SL'
ON CONFLICT DO NOTHING;


-- LR - 15 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MON', 'Montserrado', 6.55, -10.55 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NIM', 'Nimba', 7.6167, -8.4167 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOM', 'Bomi', 6.75, -10.8333 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BON', 'Bong', 6.8333, -9.3667 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GBA', 'Gbarpolu', 7.495, -10.0808 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GKE', 'Grand Kru', 4.7617, -8.2217 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GBA', 'Grand Bassa', 6.23, -9.8125 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GCA', 'Grand Cape Mount', 7.0467, -11.0717 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GGE', 'Grand Gedeh', 5.9222, -8.2217 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LOF', 'Lofa', 8.1917, -9.7233 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAR', 'Margibi', 6.515, -10.305 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAR', 'Maryland', 4.73, -7.7317 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RIV', 'River Cess', 5.9025, -9.4567 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'RIV', 'River Gee', 5.26, -7.8717 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SIN', 'Sinoe', 5.4983, -8.66 FROM localisation.pays WHERE code_iso_2 = 'LR'
ON CONFLICT DO NOTHING;


-- CV - 8 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PRA', 'Praia', 14.9177, -23.5092 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MIN', 'Mindelo', 16.8864, -24.9881 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAL', 'Sal', 16.75, -22.9333 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOA', 'Boa Vista', 16.1333, -22.8333 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAO', 'São Filipe', 14.895, -24.495 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAN', 'Santa Maria', 16.5967, -22.905 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ASS', 'Assomada', 15.1, -23.6833 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'TAR', 'Tarrafal', 15.2783, -23.7517 FROM localisation.pays WHERE code_iso_2 = 'CV'
ON CONFLICT DO NOTHING;


COMMIT;

-- Vérifier les résultats
SELECT 
    p.nom as pays,
    COUNT(pr.id) as nb_provinces
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.code_iso_2 IN ('SN', 'CI', 'GH', 'NG', 'BJ', 'TG', 'BF', 'ML', 'NE', 'MR', 'GM', 'GN', 'GW', 'SL', 'LR', 'CV')
GROUP BY p.nom
ORDER BY p.nom;
