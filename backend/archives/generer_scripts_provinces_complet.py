#!/usr/bin/env python
"""
Script pour générer les fichiers SQL de peuplement des provinces
pour tous les 54 pays africains
"""

# Données des provinces par pays (principales villes/régions)
PROVINCES_PAR_PAYS = {
    # AFRIQUE DE L'OUEST
    'SN': [  # Sénégal - 14 régions
        ('DAK', 'Dakar', 14.6928, -17.4467),
        ('THI', 'Thiès', 14.7886, -16.9261),
        ('DIO', 'Diourbel', 14.6542, -16.2292),
        ('FAT', 'Fatick', 14.3397, -16.4111),
        ('KAO', 'Kaolack', 14.1500, -16.0667),
        ('KOL', 'Kolda', 12.8833, -14.9500),
        ('LOU', 'Louga', 15.6167, -16.2167),
        ('MAT', 'Matam', 15.6556, -13.2553),
        ('SLO', 'Saint-Louis', 16.0181, -16.4897),
        ('SED', 'Sédhiou', 12.7081, -15.5569),
        ('TAM', 'Tambacounda', 13.7708, -13.6681),
        ('KED', 'Kédougou', 12.5569, -12.1744),
        ('KAF', 'Kaffrine', 14.1056, -15.5500),
        ('ZIG', 'Ziguinchor', 12.5833, -16.2667),
    ],
    'CI': [  # Côte d'Ivoire - 14 districts
        ('ABI', 'Abidjan', 5.3600, -4.0083),
        ('YAM', 'Yamoussoukro', 6.8276, -5.2893),
        ('BOU', 'Bouaké', 7.6900, -5.0300),
        ('DAL', 'Daloa', 6.8772, -6.4503),
        ('KOR', 'Korhogo', 9.4581, -5.6297),
        ('SAN', 'San-Pédro', 4.7500, -6.6333),
        ('MAN', 'Man', 7.4125, -7.5539),
        ('ABO', 'Aboisso', 5.4667, -3.2000),
        ('ABI', 'Abengourou', 6.7297, -3.4964),
        ('AGN', 'Agnibilékrou', 7.1333, -3.2000),
        ('BAN', 'Bangolo', 7.0167, -7.4833),
        ('BIA', 'Biankouma', 7.7333, -7.6167),
    ],
    'GH': [  # Ghana - 16 régions
        ('GAR', 'Greater Accra', 5.6037, -0.1870),
        ('ASH', 'Ashanti', 6.7500, -1.6000),
        ('WES', 'Western', 5.0000, -2.5000),
        ('CEN', 'Central', 5.5000, -1.0000),
        ('EAS', 'Eastern', 6.2500, -0.5000),
        ('VOL', 'Volta', 6.5000, 0.5000),
        ('NOR', 'Northern', 9.5000, -1.0000),
        ('UE', 'Upper East', 10.7500, -0.8333),
        ('UW', 'Upper West', 10.2500, -2.2500),
        ('BAH', 'Bono', 7.6667, -2.5000),
        ('BE', 'Bono East', 7.7500, -1.0500),
        ('AHA', 'Ahafo', 7.2500, -2.5000),
        ('OTI', 'Oti', 7.9000, 0.3000),
        ('SAV', 'Savannah', 9.0833, -1.5000),
        ('NE', 'North East', 10.5000, -0.3333),
        ('WN', 'Western North', 6.2000, -2.7500),
    ],
    'NG': [  # Nigeria - 36 états + FCT
        ('FCT', 'Abuja FCT', 9.0765, 7.3986),
        ('LAG', 'Lagos', 6.5244, 3.3792),
        ('KAN', 'Kano', 12.0022, 8.5920),
        ('KAD', 'Kaduna', 10.5105, 7.4165),
        ('IBA', 'Ibadan', 7.3775, 3.9470),
        ('PH', 'Port Harcourt', 4.8156, 7.0498),
        ('BEN', 'Benin City', 6.3350, 5.6037),
        ('MAI', 'Maiduguri', 11.8333, 13.1500),
        ('ZAR', 'Zaria', 11.0667, 7.7000),
        ('ABA', 'Aba', 5.1167, 7.3667),
        ('JOS', 'Jos', 9.9167, 8.8833),
        ('ILO', 'Ilorin', 8.4966, 4.5425),
        ('OWE', 'Owerri', 5.4833, 7.0333),
        ('ENE', 'Enugu', 6.4403, 7.4914),
        ('ABI', 'Abeokuta', 7.1475, 3.3619),
        ('AKU', 'Akure', 7.2571, 5.2058),
    ],
    'BJ': [  # Bénin - 12 départements
        ('ALA', 'Alibori', 11.0000, 2.6667),
        ('ATL', 'Atlantique', 6.6667, 2.2333),
        ('ATA', 'Atacora', 10.5000, 1.6667),
        ('BOR', 'Borgou', 9.5000, 2.6667),
        ('COL', 'Collines', 8.0000, 2.3333),
        ('COU', 'Couffo', 7.0000, 1.7500),
        ('DON', 'Donga', 9.7000, 1.6667),
        ('LIT', 'Littoral', 6.3654, 2.4183),
        ('MON', 'Mono', 6.5000, 1.7500),
        ('OUE', 'Ouémé', 6.5000, 2.6000),
        ('PLA', 'Plateau', 7.2500, 2.6000),
        ('ZOU', 'Zou', 7.3333, 2.1667),
    ],
    'TG': [  # Togo - 5 régions
        ('MAR', 'Maritime', 6.1256, 1.2256),
        ('PLA', 'Plateaux', 7.5333, 1.1667),
        ('CEN', 'Centrale', 8.9833, 1.0833),
        ('KAR', 'Kara', 9.5500, 1.1833),
        ('SAV', 'Savanes', 10.5000, 0.5000),
    ],
    'BF': [  # Burkina Faso - 13 régions
        ('CEN', 'Centre', 12.3714, -1.5197),
        ('BOU', 'Boucle du Mouhoun', 12.2500, -3.5000),
        ('CAS', 'Cascades', 10.5000, -4.5000),
        ('CNO', 'Centre-Nord', 13.0000, -1.0000),
        ('CES', 'Centre-Est', 11.5000, 0.0000),
        ('COU', 'Centre-Ouest', 12.0000, -2.5000),
        ('CSU', 'Centre-Sud', 11.5000, -1.0000),
        ('EST', 'Est', 12.0000, 0.5000),
        ('HAU', 'Hauts-Bassins', 11.1833, -4.3000),
        ('NOR', 'Nord', 13.5000, -2.0000),
        ('PLA', 'Plateau-Central', 12.3000, -0.7500),
        ('SAH', 'Sahel', 14.0000, -0.5000),
        ('SOU', 'Sud-Ouest', 10.5000, -3.0000),
    ],
    'ML': [  # Mali - 10 régions + Bamako
        ('BKO', 'Bamako', 12.6392, -8.0029),
        ('KAY', 'Kayes', 14.4500, -11.4333),
        ('KOU', 'Koulikoro', 12.8622, -7.5597),
        ('SIK', 'Sikasso', 11.3167, -5.6667),
        ('SEG', 'Ségou', 13.4317, -6.2633),
        ('MOP', 'Mopti', 14.4833, -4.1833),
        ('TOM', 'Tombouctou', 16.7667, -3.0167),
        ('GAO', 'Gao', 16.2667, -0.0500),
        ('KID', 'Kidal', 18.4411, 1.4078),
        ('MEN', 'Ménaka', 15.9167, 2.4000),
        ('TAO', 'Taoudénit', 22.6833, -3.9833),
    ],
    'NE': [  # Niger - 8 régions
        ('NIA', 'Niamey', 13.5127, 2.1128),
        ('AGA', 'Agadez', 16.9735, 7.9911),
        ('DIF', 'Diffa', 13.3156, 12.6113),
        ('DOS', 'Dosso', 13.0500, 3.1944),
        ('MAR', 'Maradi', 13.5000, 7.1017),
        ('TAH', 'Tahoua', 14.8903, 5.2653),
        ('TIL', 'Tillabéri', 14.2111, 1.4528),
        ('ZIN', 'Zinder', 13.8069, 8.9881),
    ],
    'MR': [  # Mauritanie - 15 régions
        ('NKC', 'Nouakchott', 18.0858, -15.9785),
        ('HOD', 'Hodh Ech Chargui', 18.5000, -7.0000),
        ('HOG', 'Hodh El Gharbi', 16.6667, -9.5000),
        ('ASS', 'Assaba', 16.7500, -11.5000),
        ('GOR', 'Gorgol', 15.9667, -12.6333),
        ('BRA', 'Brakna', 17.2333, -13.0500),
        ('TRA', 'Trarza', 17.8667, -14.6500),
        ('ADR', 'Adrar', 20.5000, -10.0000),
        ('DAK', 'Dakhlet Nouadhibou', 20.9000, -17.0333),
        ('TAG', 'Tagant', 18.5500, -9.9000),
        ('GUI', 'Guidimaka', 15.2500, -12.2500),
        ('TIR', 'Tiris Zemmour', 24.5000, -9.5000),
        ('INC', 'Inchiri', 20.0000, -15.5000),
    ],
    'GM': [  # Gambie - 6 régions
        ('BAN', 'Banjul', 13.4549, -16.5790),
        ('WES', 'Western', 13.3500, -16.6000),
        ('LRR', 'Lower River', 13.3833, -15.8333),
        ('CRR', 'Central River', 13.5833, -14.8333),
        ('NBR', 'North Bank', 13.5000, -15.8333),
        ('URR', 'Upper River', 13.4500, -13.8000),
    ],
    'GN': [  # Guinée - 8 régions
        ('CON', 'Conakry', 9.6412, -13.5784),
        ('BOK', 'Boké', 10.9333, -14.2833),
        ('FAR', 'Faranah', 10.0333, -10.7333),
        ('KAN', 'Kankan', 10.3833, -9.3000),
        ('KIN', 'Kindia', 10.0500, -12.8500),
        ('LAB', 'Labé', 11.3167, -12.2833),
        ('MAM', 'Mamou', 10.3750, -12.0833),
        ('NZE', 'Nzérékoré', 7.7500, -8.8167),
    ],
    'GW': [  # Guinée-Bissau - 9 régions
        ('BIS', 'Bissau', 11.8636, -15.5982),
        ('BAF', 'Bafatá', 12.1667, -14.6500),
        ('BIO', 'Biombo', 11.8833, -15.7333),
        ('BOL', 'Bolama', 11.5833, -15.4833),
        ('CAC', 'Cacheu', 12.2667, -16.1667),
        ('GAB', 'Gabú', 12.2833, -14.2167),
        ('OIO', 'Oio', 12.4500, -15.2167),
        ('QUI', 'Quinara', 11.8833, -15.1833),
        ('TOM', 'Tombali', 11.3333, -14.9833),
    ],
    'SL': [  # Sierra Leone - 5 régions
        ('WES', 'Western Area', 8.4657, -13.2317),
        ('NOR', 'Northern', 9.5000, -12.0000),
        ('SOU', 'Southern', 7.8833, -11.7500),
        ('EAS', 'Eastern', 8.1667, -10.8333),
        ('NWE', 'North West', 8.8833, -12.9167),
    ],
    'LR': [  # Libéria - 15 comtés
        ('MON', 'Montserrado', 6.5500, -10.5500),
        ('NIM', 'Nimba', 7.6167, -8.4167),
        ('BOM', 'Bomi', 6.7500, -10.8333),
        ('BON', 'Bong', 6.8333, -9.3667),
        ('GBA', 'Gbarpolu', 7.4950, -10.0808),
        ('GKE', 'Grand Kru', 4.7617, -8.2217),
        ('GBA', 'Grand Bassa', 6.2300, -9.8125),
        ('GCA', 'Grand Cape Mount', 7.0467, -11.0717),
        ('GGE', 'Grand Gedeh', 5.9222, -8.2217),
        ('LOF', 'Lofa', 8.1917, -9.7233),
        ('MAR', 'Margibi', 6.5150, -10.3050),
        ('MAR', 'Maryland', 4.7300, -7.7317),
        ('RIV', 'River Cess', 5.9025, -9.4567),
        ('RIV', 'River Gee', 5.2600, -7.8717),
        ('SIN', 'Sinoe', 5.4983, -8.6600),
    ],
    'CV': [  # Cap-Vert - 22 municipalités (principales îles)
        ('PRA', 'Praia', 14.9177, -23.5092),
        ('MIN', 'Mindelo', 16.8864, -24.9881),
        ('SAL', 'Sal', 16.7500, -22.9333),
        ('BOA', 'Boa Vista', 16.1333, -22.8333),
        ('SAO', 'São Filipe', 14.8950, -24.4950),
        ('SAN', 'Santa Maria', 16.5967, -22.9050),
        ('ASS', 'Assomada', 15.1000, -23.6833),
        ('TAR', 'Tarrafal', 15.2783, -23.7517),
    ],
}

def generer_script_sql(region, pays_list):
    """Générer un script SQL pour une région"""
    script = f"""-- Peupler les provinces pour {region}
-- Connexion: psql -U postgres -d ufaranga -f peupler_provinces_{region.lower().replace(' ', '_')}.sql

BEGIN;

"""
    
    for code_pays, provinces in pays_list.items():
        pays_nom = code_pays  # Simplification
        script += f"-- {pays_nom} - {len(provinces)} provinces\n"
        
        for code, nom, lat, lon in provinces:
            script += f"""INSERT INTO localisation.provinces (id, pays_id, code, nom, latitude_centre, longitude_centre) 
SELECT gen_random_uuid(), id, '{code}', '{nom}', {lat}, {lon} FROM localisation.pays WHERE code_iso_2 = '{code_pays}'
ON CONFLICT DO NOTHING;

"""
        script += "\n"
    
    script += """COMMIT;

-- Vérifier les résultats
SELECT 
    p.nom as pays,
    COUNT(pr.id) as nb_provinces
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.code_iso_2 IN ("""
    
    codes = "', '".join(pays_list.keys())
    script += f"'{codes}'"
    script += """)
GROUP BY p.nom
ORDER BY p.nom;
"""
    
    return script

# Générer le script pour l'Afrique de l'Ouest
print("Génération du script pour l'Afrique de l'Ouest...")
script_ouest = generer_script_sql("Afrique de l'Ouest", PROVINCES_PAR_PAYS)

with open('peupler_provinces_afrique_ouest.sql', 'w', encoding='utf-8') as f:
    f.write(script_ouest)

print("✅ Script généré: peupler_provinces_afrique_ouest.sql")
print(f"   Total: {sum(len(v) for v in PROVINCES_PAR_PAYS.values())} provinces")
