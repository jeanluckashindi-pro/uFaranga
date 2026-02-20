-- Compléter les métadonnées des pays africains
-- Connexion: psql -U postgres -d ufaranga -f completer_metadonnees_pays.sql

BEGIN;

-- AFRIQUE DE L'EST

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Gitega',
    'devise', 'Franc burundais (BIF)',
    'langues', ARRAY['Kirundi', 'Français', 'Anglais'],
    'indicatif_tel', '+257',
    'fuseau_horaire', 'UTC+2',
    'population', 12889576,
    'superficie_km2', 27834
) WHERE code_iso_2 = 'BI';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Kigali',
    'devise', 'Franc rwandais (RWF)',
    'langues', ARRAY['Kinyarwanda', 'Français', 'Anglais'],
    'indicatif_tel', '+250',
    'fuseau_horaire', 'UTC+2',
    'population', 13776698,
    'superficie_km2', 26338
) WHERE code_iso_2 = 'RW';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Nairobi',
    'devise', 'Shilling kényan (KES)',
    'langues', ARRAY['Swahili', 'Anglais'],
    'indicatif_tel', '+254',
    'fuseau_horaire', 'UTC+3',
    'population', 54027487,
    'superficie_km2', 580367
) WHERE code_iso_2 = 'KE';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Dodoma',
    'devise', 'Shilling tanzanien (TZS)',
    'langues', ARRAY['Swahili', 'Anglais'],
    'indicatif_tel', '+255',
    'fuseau_horaire', 'UTC+3',
    'population', 65497748,
    'superficie_km2', 947303
) WHERE code_iso_2 = 'TZ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Kampala',
    'devise', 'Shilling ougandais (UGX)',
    'langues', ARRAY['Anglais', 'Swahili'],
    'indicatif_tel', '+256',
    'fuseau_horaire', 'UTC+3',
    'population', 47249585,
    'superficie_km2', 241038
) WHERE code_iso_2 = 'UG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Addis-Abeba',
    'devise', 'Birr éthiopien (ETB)',
    'langues', ARRAY['Amharique'],
    'indicatif_tel', '+251',
    'fuseau_horaire', 'UTC+3',
    'population', 123379924,
    'superficie_km2', 1104300
) WHERE code_iso_2 = 'ET';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Mogadiscio',
    'devise', 'Shilling somalien (SOS)',
    'langues', ARRAY['Somali', 'Arabe'],
    'indicatif_tel', '+252',
    'fuseau_horaire', 'UTC+3',
    'population', 17597511,
    'superficie_km2', 637657
) WHERE code_iso_2 = 'SO';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Djibouti',
    'devise', 'Franc djiboutien (DJF)',
    'langues', ARRAY['Français', 'Arabe'],
    'indicatif_tel', '+253',
    'fuseau_horaire', 'UTC+3',
    'population', 1120849,
    'superficie_km2', 23200
) WHERE code_iso_2 = 'DJ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Asmara',
    'devise', 'Nakfa (ERN)',
    'langues', ARRAY['Tigrinya', 'Arabe', 'Anglais'],
    'indicatif_tel', '+291',
    'fuseau_horaire', 'UTC+3',
    'population', 3684032,
    'superficie_km2', 117600
) WHERE code_iso_2 = 'ER';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Moroni',
    'devise', 'Franc comorien (KMF)',
    'langues', ARRAY['Comorien', 'Arabe', 'Français'],
    'indicatif_tel', '+269',
    'fuseau_horaire', 'UTC+3',
    'population', 888451,
    'superficie_km2', 1862
) WHERE code_iso_2 = 'KM';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Victoria',
    'devise', 'Roupie seychelloise (SCR)',
    'langues', ARRAY['Créole seychellois', 'Français', 'Anglais'],
    'indicatif_tel', '+248',
    'fuseau_horaire', 'UTC+4',
    'population', 107660,
    'superficie_km2', 452
) WHERE code_iso_2 = 'SC';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Port-Louis',
    'devise', 'Roupie mauricienne (MUR)',
    'langues', ARRAY['Créole mauricien', 'Français', 'Anglais'],
    'indicatif_tel', '+230',
    'fuseau_horaire', 'UTC+4',
    'population', 1299469,
    'superficie_km2', 2040
) WHERE code_iso_2 = 'MU';

-- AFRIQUE CENTRALE

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Kinshasa',
    'devise', 'Franc congolais (CDF)',
    'langues', ARRAY['Français', 'Lingala', 'Swahili', 'Kikongo', 'Tshiluba'],
    'indicatif_tel', '+243',
    'fuseau_horaire', 'UTC+1/+2',
    'population', 99010212,
    'superficie_km2', 2344858
) WHERE code_iso_2 = 'CD';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Brazzaville',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Français', 'Lingala', 'Kikongo'],
    'indicatif_tel', '+242',
    'fuseau_horaire', 'UTC+1',
    'population', 5970424,
    'superficie_km2', 342000
) WHERE code_iso_2 = 'CG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Yaoundé',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Français', 'Anglais'],
    'indicatif_tel', '+237',
    'fuseau_horaire', 'UTC+1',
    'population', 27914536,
    'superficie_km2', 475442
) WHERE code_iso_2 = 'CM';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Libreville',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+241',
    'fuseau_horaire', 'UTC+1',
    'population', 2341179,
    'superficie_km2', 267668
) WHERE code_iso_2 = 'GA';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Bangui',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Français', 'Sango'],
    'indicatif_tel', '+236',
    'fuseau_horaire', 'UTC+1',
    'population', 5579144,
    'superficie_km2', 622984
) WHERE code_iso_2 = 'CF';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'N''Djamena',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Français', 'Arabe'],
    'indicatif_tel', '+235',
    'fuseau_horaire', 'UTC+1',
    'population', 17723315,
    'superficie_km2', 1284000
) WHERE code_iso_2 = 'TD';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Malabo',
    'devise', 'Franc CFA (XAF)',
    'langues', ARRAY['Espagnol', 'Français', 'Portugais'],
    'indicatif_tel', '+240',
    'fuseau_horaire', 'UTC+1',
    'population', 1674908,
    'superficie_km2', 28051
) WHERE code_iso_2 = 'GQ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'São Tomé',
    'devise', 'Dobra (STN)',
    'langues', ARRAY['Portugais'],
    'indicatif_tel', '+239',
    'fuseau_horaire', 'UTC+0',
    'population', 227380,
    'superficie_km2', 964
) WHERE code_iso_2 = 'ST';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Luanda',
    'devise', 'Kwanza (AOA)',
    'langues', ARRAY['Portugais'],
    'indicatif_tel', '+244',
    'fuseau_horaire', 'UTC+1',
    'population', 35588987,
    'superficie_km2', 1246700
) WHERE code_iso_2 = 'AO';

-- AFRIQUE DE L'OUEST

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Dakar',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français', 'Wolof'],
    'indicatif_tel', '+221',
    'fuseau_horaire', 'UTC+0',
    'population', 17316449,
    'superficie_km2', 196722
) WHERE code_iso_2 = 'SN';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Yamoussoukro',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+225',
    'fuseau_horaire', 'UTC+0',
    'population', 28160542,
    'superficie_km2', 322463
) WHERE code_iso_2 = 'CI';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Accra',
    'devise', 'Cedi ghanéen (GHS)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+233',
    'fuseau_horaire', 'UTC+0',
    'population', 33475870,
    'superficie_km2', 238533
) WHERE code_iso_2 = 'GH';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Abuja',
    'devise', 'Naira (NGN)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+234',
    'fuseau_horaire', 'UTC+1',
    'population', 218541212,
    'superficie_km2', 923768
) WHERE code_iso_2 = 'NG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Porto-Novo',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+229',
    'fuseau_horaire', 'UTC+1',
    'population', 13352864,
    'superficie_km2', 114763
) WHERE code_iso_2 = 'BJ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Lomé',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+228',
    'fuseau_horaire', 'UTC+0',
    'population', 8848699,
    'superficie_km2', 56785
) WHERE code_iso_2 = 'TG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Ouagadougou',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+226',
    'fuseau_horaire', 'UTC+0',
    'population', 22100683,
    'superficie_km2', 274200
) WHERE code_iso_2 = 'BF';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Bamako',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+223',
    'fuseau_horaire', 'UTC+0',
    'population', 22593590,
    'superficie_km2', 1240192
) WHERE code_iso_2 = 'ML';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Niamey',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+227',
    'fuseau_horaire', 'UTC+1',
    'population', 26207977,
    'superficie_km2', 1267000
) WHERE code_iso_2 = 'NE';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Nouakchott',
    'devise', 'Ouguiya (MRU)',
    'langues', ARRAY['Arabe', 'Français'],
    'indicatif_tel', '+222',
    'fuseau_horaire', 'UTC+0',
    'population', 4736139,
    'superficie_km2', 1030700
) WHERE code_iso_2 = 'MR';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Banjul',
    'devise', 'Dalasi (GMD)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+220',
    'fuseau_horaire', 'UTC+0',
    'population', 2639916,
    'superficie_km2', 11295
) WHERE code_iso_2 = 'GM';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Conakry',
    'devise', 'Franc guinéen (GNF)',
    'langues', ARRAY['Français'],
    'indicatif_tel', '+224',
    'fuseau_horaire', 'UTC+0',
    'population', 13859341,
    'superficie_km2', 245857
) WHERE code_iso_2 = 'GN';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Bissau',
    'devise', 'Franc CFA (XOF)',
    'langues', ARRAY['Portugais'],
    'indicatif_tel', '+245',
    'fuseau_horaire', 'UTC+0',
    'population', 2105566,
    'superficie_km2', 36125
) WHERE code_iso_2 = 'GW';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Freetown',
    'devise', 'Leone (SLL)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+232',
    'fuseau_horaire', 'UTC+0',
    'population', 8605718,
    'superficie_km2', 71740
) WHERE code_iso_2 = 'SL';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Monrovia',
    'devise', 'Dollar libérien (LRD)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+231',
    'fuseau_horaire', 'UTC+0',
    'population', 5302681,
    'superficie_km2', 111369
) WHERE code_iso_2 = 'LR';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Praia',
    'devise', 'Escudo cap-verdien (CVE)',
    'langues', ARRAY['Portugais'],
    'indicatif_tel', '+238',
    'fuseau_horaire', 'UTC-1',
    'population', 593149,
    'superficie_km2', 4033
) WHERE code_iso_2 = 'CV';

-- AFRIQUE DU NORD

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Rabat',
    'devise', 'Dirham marocain (MAD)',
    'langues', ARRAY['Arabe', 'Berbère', 'Français'],
    'indicatif_tel', '+212',
    'fuseau_horaire', 'UTC+1',
    'population', 37457971,
    'superficie_km2', 446550
) WHERE code_iso_2 = 'MA';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Alger',
    'devise', 'Dinar algérien (DZD)',
    'langues', ARRAY['Arabe', 'Berbère', 'Français'],
    'indicatif_tel', '+213',
    'fuseau_horaire', 'UTC+1',
    'population', 44903225,
    'superficie_km2', 2381741
) WHERE code_iso_2 = 'DZ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Tunis',
    'devise', 'Dinar tunisien (TND)',
    'langues', ARRAY['Arabe', 'Français'],
    'indicatif_tel', '+216',
    'fuseau_horaire', 'UTC+1',
    'population', 12356117,
    'superficie_km2', 163610
) WHERE code_iso_2 = 'TN';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Le Caire',
    'devise', 'Livre égyptienne (EGP)',
    'langues', ARRAY['Arabe'],
    'indicatif_tel', '+20',
    'fuseau_horaire', 'UTC+2',
    'population', 110990103,
    'superficie_km2', 1002450
) WHERE code_iso_2 = 'EG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Tripoli',
    'devise', 'Dinar libyen (LYD)',
    'langues', ARRAY['Arabe'],
    'indicatif_tel', '+218',
    'fuseau_horaire', 'UTC+2',
    'population', 6812341,
    'superficie_km2', 1759540
) WHERE code_iso_2 = 'LY';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Khartoum',
    'devise', 'Livre soudanaise (SDG)',
    'langues', ARRAY['Arabe', 'Anglais'],
    'indicatif_tel', '+249',
    'fuseau_horaire', 'UTC+2',
    'population', 46874204,
    'superficie_km2', 1886068
) WHERE code_iso_2 = 'SD';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Djouba',
    'devise', 'Livre sud-soudanaise (SSP)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+211',
    'fuseau_horaire', 'UTC+2',
    'population', 11381378,
    'superficie_km2', 644329
) WHERE code_iso_2 = 'SS';

-- AFRIQUE AUSTRALE

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Pretoria',
    'devise', 'Rand (ZAR)',
    'langues', ARRAY['Afrikaans', 'Anglais', 'Zoulou', 'Xhosa'],
    'indicatif_tel', '+27',
    'fuseau_horaire', 'UTC+2',
    'population', 59893885,
    'superficie_km2', 1221037
) WHERE code_iso_2 = 'ZA';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Gaborone',
    'devise', 'Pula (BWP)',
    'langues', ARRAY['Anglais', 'Tswana'],
    'indicatif_tel', '+267',
    'fuseau_horaire', 'UTC+2',
    'population', 2630296,
    'superficie_km2', 581730
) WHERE code_iso_2 = 'BW';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Windhoek',
    'devise', 'Dollar namibien (NAD)',
    'langues', ARRAY['Anglais', 'Afrikaans'],
    'indicatif_tel', '+264',
    'fuseau_horaire', 'UTC+2',
    'population', 2567012,
    'superficie_km2', 825615
) WHERE code_iso_2 = 'NA';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Lusaka',
    'devise', 'Kwacha zambien (ZMW)',
    'langues', ARRAY['Anglais'],
    'indicatif_tel', '+260',
    'fuseau_horaire', 'UTC+2',
    'population', 19610769,
    'superficie_km2', 752612
) WHERE code_iso_2 = 'ZM';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Harare',
    'devise', 'Dollar zimbabwéen (ZWL)',
    'langues', ARRAY['Anglais', 'Shona', 'Ndébélé'],
    'indicatif_tel', '+263',
    'fuseau_horaire', 'UTC+2',
    'population', 16320537,
    'superficie_km2', 390757
) WHERE code_iso_2 = 'ZW';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Maputo',
    'devise', 'Metical (MZN)',
    'langues', ARRAY['Portugais'],
    'indicatif_tel', '+258',
    'fuseau_horaire', 'UTC+2',
    'population', 32969518,
    'superficie_km2', 801590
) WHERE code_iso_2 = 'MZ';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Lilongwe',
    'devise', 'Kwacha malawite (MWK)',
    'langues', ARRAY['Anglais', 'Chichewa'],
    'indicatif_tel', '+265',
    'fuseau_horaire', 'UTC+2',
    'population', 20405317,
    'superficie_km2', 118484
) WHERE code_iso_2 = 'MW';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Antananarivo',
    'devise', 'Ariary (MGA)',
    'langues', ARRAY['Malgache', 'Français'],
    'indicatif_tel', '+261',
    'fuseau_horaire', 'UTC+3',
    'population', 29611714,
    'superficie_km2', 587041
) WHERE code_iso_2 = 'MG';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Maseru',
    'devise', 'Loti (LSL)',
    'langues', ARRAY['Sotho', 'Anglais'],
    'indicatif_tel', '+266',
    'fuseau_horaire', 'UTC+2',
    'population', 2305825,
    'superficie_km2', 30355
) WHERE code_iso_2 = 'LS';

UPDATE localisation.pays SET metadonnees = jsonb_build_object(
    'capitale', 'Mbabane',
    'devise', 'Lilangeni (SZL)',
    'langues', ARRAY['Swati', 'Anglais'],
    'indicatif_tel', '+268',
    'fuseau_horaire', 'UTC+2',
    'population', 1201670,
    'superficie_km2', 17364
) WHERE code_iso_2 = 'SZ';

COMMIT;

-- Vérifier les résultats
SELECT 
    code_iso_2,
    nom,
    metadonnees->>'capitale' as capitale,
    metadonnees->>'devise' as devise,
    metadonnees->>'indicatif_tel' as indicatif
FROM localisation.pays
WHERE continent = 'Afrique'
ORDER BY sous_region, nom
LIMIT 10;

-- Compter les pays avec métadonnées complètes
SELECT COUNT(*) as pays_avec_metadonnees
FROM localisation.pays
WHERE continent = 'Afrique' 
AND metadonnees IS NOT NULL 
AND metadonnees != '{}'::jsonb;
