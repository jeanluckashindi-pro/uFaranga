-- Peupler les provinces pour l'Afrique Centrale (9 pays)
-- Connexion: psql -U postgres -d ufaranga -f peupler_provinces_afrique_centrale.sql

BEGIN;

-- ============================================================================
-- AFRIQUE CENTRALE (9 pays)
-- ============================================================================

-- RD CONGO (CD) - 26 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KIN', 'Kinshasa', -4.3276, 15.3136 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAS', 'Bas-Congo', -5.8000, 13.5000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BAN', 'Bandundu', -3.3167, 17.3833 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EQU', 'Équateur', 0.0000, 23.0000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ORI', 'Province Orientale', 1.5000, 25.0000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NKI', 'Nord-Kivu', -0.7167, 29.2333 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SKI', 'Sud-Kivu', -2.5000, 28.5000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAN', 'Maniema', -2.0000, 26.0000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAT', 'Katanga', -10.0000, 26.0000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KAS', 'Kasaï', -5.0000, 21.0000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KOR', 'Kasaï-Oriental', -6.0000, 23.5000 FROM localisation.pays WHERE code_iso_2 = 'CD'
ON CONFLICT DO NOTHING;

-- CONGO (CG) - 12 départements
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BZV', 'Brazzaville', -4.2634, 15.2429 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PNR', 'Pointe-Noire', -4.7692, 11.8636 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KOU', 'Kouilou', -4.1500, 11.8833 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NIA', 'Niari', -3.0000, 12.5000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LEK', 'Lékoumou', -3.1667, 13.5000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BOU', 'Bouenza', -4.1167, 13.6167 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'POO', 'Pool', -3.5000, 15.0000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PLA', 'Plateaux', -2.0000, 15.5000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CUV', 'Cuvette', -0.5000, 16.0000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CUO', 'Cuvette-Ouest', -0.5000, 14.5000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SAN', 'Sangha', 1.5000, 16.0000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LIK', 'Likouala', 2.0000, 18.0000 FROM localisation.pays WHERE code_iso_2 = 'CG'
ON CONFLICT DO NOTHING;

-- CAMEROUN (CM) - 10 régions
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CE', 'Centre', 4.0511, 11.5021 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LT', 'Littoral', 4.0511, 9.7679 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OU', 'Ouest', 5.4500, 10.4167 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NO', 'Nord-Ouest', 6.0000, 10.1500 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SW', 'Sud-Ouest', 4.1500, 9.2333 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'SU', 'Sud', 2.9000, 11.5167 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ES', 'Est', 4.5000, 14.5000 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AD', 'Adamaoua', 7.0000, 13.0000 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NO', 'Nord', 9.3333, 13.3833 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EN', 'Extrême-Nord', 10.5900, 14.2000 FROM localisation.pays WHERE code_iso_2 = 'CM'
ON CONFLICT DO NOTHING;

-- GABON (GA) - 9 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'EST', 'Estuaire', 0.4162, 9.4673 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HO', 'Haut-Ogooué', -1.4500, 13.5833 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MO', 'Moyen-Ogooué', -0.7000, 10.4000 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NG', 'Ngounié', -1.5000, 10.9167 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NY', 'Nyanga', -2.9167, 11.0833 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OG', 'Ogooué-Ivindo', 0.5000, 13.0000 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OL', 'Ogooué-Lolo', -0.8333, 12.4500 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'OM', 'Ogooué-Maritime', -1.5000, 9.8333 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WN', 'Woleu-Ntem', 2.1167, 11.5000 FROM localisation.pays WHERE code_iso_2 = 'GA'
ON CONFLICT DO NOTHING;

-- RCA (CF) - 16 préfectures
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BGF', 'Bangui', 4.3947, 18.5582 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BB', 'Bamingui-Bangoran', 8.0000, 20.6667 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BGG', 'Basse-Kotto', 4.8333, 21.0000 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HK', 'Haute-Kotto', 6.5000, 23.5000 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HS', 'Haut-Mbomou', 6.2500, 25.4667 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KB', 'Kémo', 5.8833, 19.3833 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LB', 'Lobaye', 4.0000, 17.5000 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MB', 'Mbomou', 5.5000, 23.0000 FROM localisation.pays WHERE code_iso_2 = 'CF'
ON CONFLICT DO NOTHING;

-- TCHAD (TD) - 23 régions (principales)
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ND', 'N''Djamena', 12.1348, 15.0557 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BA', 'Batha', 13.8333, 18.4167 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BG', 'Borkou', 17.9167, 18.8333 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CB', 'Chari-Baguirmi', 11.4500, 15.2833 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'GR', 'Guéra', 11.0500, 18.4167 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KA', 'Kanem', 14.8333, 15.3333 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LC', 'Lac', 13.6667, 14.1000 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LO', 'Logone Occidental', 8.6167, 15.8833 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LR', 'Logone Oriental', 8.3333, 16.5833 FROM localisation.pays WHERE code_iso_2 = 'TD'
ON CONFLICT DO NOTHING;

-- GUINÉE ÉQUATORIALE (GQ) - 7 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BN', 'Bioko Nord', 3.7500, 8.7833 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BS', 'Bioko Sud', 3.4167, 8.6667 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'AN', 'Annobón', -1.4167, 5.6333 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CS', 'Centro Sur', 1.4500, 10.4833 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'KN', 'Kié-Ntem', 2.1500, 10.9833 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LI', 'Litoral', 1.6167, 9.7667 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'WN', 'Wele-Nzas', 1.5833, 11.2833 FROM localisation.pays WHERE code_iso_2 = 'GQ'
ON CONFLICT DO NOTHING;

-- SAO TOMÉ-ET-PRINCIPE (ST) - 2 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ST', 'São Tomé', 0.3333, 6.7333 FROM localisation.pays WHERE code_iso_2 = 'ST'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'PR', 'Príncipe', 1.6167, 7.4000 FROM localisation.pays WHERE code_iso_2 = 'ST'
ON CONFLICT DO NOTHING;

-- ANGOLA (AO) - 18 provinces
INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LUA', 'Luanda', -8.8383, 13.2344 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BGO', 'Bengo', -9.0000, 13.7000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BGU', 'Benguela', -12.5763, 13.4055 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'BIE', 'Bié', -12.5000, 17.5000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CAB', 'Cabinda', -5.5500, 12.2000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CCU', 'Cuando Cubango', -15.0000, 18.0000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CNO', 'Cuanza Norte', -9.2500, 14.5000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CUS', 'Cuanza Sul', -10.5000, 15.5000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'CNN', 'Cunene', -16.0000, 16.0000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HUA', 'Huambo', -12.7764, 15.7389 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'HUI', 'Huíla', -14.9167, 14.5167 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LNO', 'Lunda Norte', -8.5000, 19.0000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'LSU', 'Lunda Sul', -10.5000, 20.5000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MAL', 'Malanje', -9.5400, 16.3411 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'MOX', 'Moxico', -12.0000, 20.0000 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'NAM', 'Namibe', -15.1961, 12.1522 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'UIG', 'Uíge', -7.6086, 15.0614 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, 'ZAI', 'Zaire', -6.1667, 12.8333 FROM localisation.pays WHERE code_iso_2 = 'AO'
ON CONFLICT DO NOTHING;

COMMIT;

-- Vérifier les résultats
SELECT 
    p.nom as pays,
    COUNT(pr.id) as nb_provinces
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.sous_region = 'Afrique Centrale'
GROUP BY p.nom
ORDER BY p.nom;
