-- Compléter TOUS les pays africains avec continent et sous-région
-- Connexion: psql -U postgres -d ufaranga -f completer_tous_pays_africains.sql

BEGIN;

-- AFRIQUE DE L'EST
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'BI'; -- Burundi
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'RW'; -- Rwanda
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'KE'; -- Kenya
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'TZ'; -- Tanzanie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'UG'; -- Ouganda
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'ET'; -- Éthiopie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'SO'; -- Somalie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'DJ'; -- Djibouti
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'ER'; -- Érythrée
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'KM'; -- Comores
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'SC'; -- Seychelles
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Est' WHERE code_iso_2 = 'MU'; -- Maurice

-- AFRIQUE CENTRALE
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'CD'; -- RD Congo
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'CG'; -- Congo
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'CM'; -- Cameroun
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'GA'; -- Gabon
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'CF'; -- RCA
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'TD'; -- Tchad
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'GQ'; -- Guinée équatoriale
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'ST'; -- Sao Tomé-et-Principe
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Centrale' WHERE code_iso_2 = 'AO'; -- Angola

-- AFRIQUE DE L'OUEST
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'SN'; -- Sénégal
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'CI'; -- Côte d'Ivoire
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'GH'; -- Ghana
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'NG'; -- Nigeria
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'BJ'; -- Bénin
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'TG'; -- Togo
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'BF'; -- Burkina Faso
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'ML'; -- Mali
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'NE'; -- Niger
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'MR'; -- Mauritanie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'GM'; -- Gambie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'GN'; -- Guinée
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'GW'; -- Guinée-Bissau
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'SL'; -- Sierra Leone
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'LR'; -- Libéria
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique de l''Ouest' WHERE code_iso_2 = 'CV'; -- Cap-Vert

-- AFRIQUE DU NORD
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'MA'; -- Maroc
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'DZ'; -- Algérie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'TN'; -- Tunisie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'EG'; -- Égypte
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'LY'; -- Libye
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'SD'; -- Soudan
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique du Nord' WHERE code_iso_2 = 'SS'; -- Soudan du Sud

-- AFRIQUE AUSTRALE
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'ZA'; -- Afrique du Sud
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'BW'; -- Botswana
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'NA'; -- Namibie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'ZM'; -- Zambie
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'ZW'; -- Zimbabwe
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'MZ'; -- Mozambique
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'MW'; -- Malawi
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'MG'; -- Madagascar
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'LS'; -- Lesotho
UPDATE localisation.pays SET continent = 'Afrique', sous_region = 'Afrique Australe' WHERE code_iso_2 = 'SZ'; -- Eswatini

COMMIT;

-- Vérifier les résultats
SELECT 
    sous_region,
    COUNT(*) as nb_pays,
    STRING_AGG(nom, ', ' ORDER BY nom) as pays
FROM localisation.pays
WHERE continent = 'Afrique'
GROUP BY sous_region
ORDER BY sous_region;

-- Total
SELECT COUNT(*) as total_pays_africains
FROM localisation.pays
WHERE continent = 'Afrique';
