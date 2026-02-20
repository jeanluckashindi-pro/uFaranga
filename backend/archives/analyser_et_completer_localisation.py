"""
Script pour analyser et compléter les données de localisation

1. Vérifie quels pays n'ont pas de provinces/districts/quartiers
2. Ajoute les colonnes continent et sous_region à la table pays
3. Peuple les données pour les pays africains avec leurs divisions administratives
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier
from django.db import connection
from django.db.models import Count, Q
from decimal import Decimal


# =============================================================================
# DONNÉES DES PAYS AFRICAINS
# =============================================================================

PAYS_AFRICAINS = {
    # Afrique de l'Est
    'BI': {
        'nom': 'Burundi',
        'nom_anglais': 'Burundi',
        'code_iso_3': 'BDI',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Est',
        'capitale': 'Gitega',
        'latitude': Decimal('-3.3731'),
        'longitude': Decimal('29.9189'),
        'indicatif': '+257',
        'devise': 'BIF',
        'provinces': [
            {'code': 'BB', 'nom': 'Bubanza'},
            {'code': 'BM', 'nom': 'Bujumbura Mairie'},
            {'code': 'BR', 'nom': 'Bujumbura Rural'},
            {'code': 'BU', 'nom': 'Bururi'},
            {'code': 'CA', 'nom': 'Cankuzo'},
            {'code': 'CI', 'nom': 'Cibitoke'},
            {'code': 'GI', 'nom': 'Gitega'},
            {'code': 'KI', 'nom': 'Kirundo'},
            {'code': 'KR', 'nom': 'Karuzi'},
            {'code': 'KY', 'nom': 'Kayanza'},
            {'code': 'MA', 'nom': 'Makamba'},
            {'code': 'MU', 'nom': 'Muramvya'},
            {'code': 'MW', 'nom': 'Mwaro'},
            {'code': 'MY', 'nom': 'Muyinga'},
            {'code': 'NG', 'nom': 'Ngozi'},
            {'code': 'RT', 'nom': 'Rutana'},
            {'code': 'RY', 'nom': 'Ruyigi'},
        ]
    },
    'RW': {
        'nom': 'Rwanda',
        'nom_anglais': 'Rwanda',
        'code_iso_3': 'RWA',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Est',
        'capitale': 'Kigali',
        'latitude': Decimal('-1.9403'),
        'longitude': Decimal('29.8739'),
        'indicatif': '+250',
        'devise': 'RWF',
        'provinces': [
            {'code': 'KIG', 'nom': 'Kigali'},
            {'code': 'EST', 'nom': 'Est'},
            {'code': 'NOR', 'nom': 'Nord'},
            {'code': 'OUE', 'nom': 'Ouest'},
            {'code': 'SUD', 'nom': 'Sud'},
        ]
    },
    'KE': {
        'nom': 'Kenya',
        'nom_anglais': 'Kenya',
        'code_iso_3': 'KEN',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Est',
        'capitale': 'Nairobi',
        'latitude': Decimal('-0.0236'),
        'longitude': Decimal('37.9062'),
        'indicatif': '+254',
        'devise': 'KES',
        'provinces': [
            {'code': 'NAI', 'nom': 'Nairobi'},
            {'code': 'MOM', 'nom': 'Mombasa'},
            {'code': 'KIS', 'nom': 'Kisumu'},
            {'code': 'NAK', 'nom': 'Nakuru'},
        ]
    },
    'TZ': {
        'nom': 'Tanzanie',
        'nom_anglais': 'Tanzania',
        'code_iso_3': 'TZA',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Est',
        'capitale': 'Dodoma',
        'latitude': Decimal('-6.3690'),
        'longitude': Decimal('34.8888'),
        'indicatif': '+255',
        'devise': 'TZS',
        'provinces': [
            {'code': 'DAR', 'nom': 'Dar es Salaam'},
            {'code': 'DOD', 'nom': 'Dodoma'},
            {'code': 'ARU', 'nom': 'Arusha'},
            {'code': 'MWA', 'nom': 'Mwanza'},
        ]
    },
    'UG': {
        'nom': 'Ouganda',
        'nom_anglais': 'Uganda',
        'code_iso_3': 'UGA',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Est',
        'capitale': 'Kampala',
        'latitude': Decimal('1.3733'),
        'longitude': Decimal('32.2903'),
        'indicatif': '+256',
        'devise': 'UGX',
        'provinces': [
            {'code': 'KAM', 'nom': 'Kampala'},
            {'code': 'ENT', 'nom': 'Entebbe'},
            {'code': 'GUL', 'nom': 'Gulu'},
            {'code': 'MBA', 'nom': 'Mbarara'},
        ]
    },
    
    # Afrique Centrale
    'CD': {
        'nom': 'République Démocratique du Congo',
        'nom_anglais': 'Democratic Republic of the Congo',
        'code_iso_3': 'COD',
        'continent': 'Afrique',
        'sous_region': 'Afrique Centrale',
        'capitale': 'Kinshasa',
        'latitude': Decimal('-4.0383'),
        'longitude': Decimal('21.7587'),
        'indicatif': '+243',
        'devise': 'CDF',
        'provinces': [
            {'code': 'KIN', 'nom': 'Kinshasa'},
            {'code': 'BAS', 'nom': 'Bas-Congo'},
            {'code': 'BAN', 'nom': 'Bandundu'},
            {'code': 'EQU', 'nom': 'Équateur'},
            {'code': 'KAS', 'nom': 'Kasaï-Oriental'},
            {'code': 'KAT', 'nom': 'Katanga'},
            {'code': 'NOR', 'nom': 'Nord-Kivu'},
            {'code': 'SUD', 'nom': 'Sud-Kivu'},
        ]
    },
    'CG': {
        'nom': 'République du Congo',
        'nom_anglais': 'Republic of the Congo',
        'code_iso_3': 'COG',
        'continent': 'Afrique',
        'sous_region': 'Afrique Centrale',
        'capitale': 'Brazzaville',
        'latitude': Decimal('-4.2634'),
        'longitude': Decimal('15.2429'),
        'indicatif': '+242',
        'devise': 'XAF',
        'provinces': [
            {'code': 'BRA', 'nom': 'Brazzaville'},
            {'code': 'PNR', 'nom': 'Pointe-Noire'},
        ]
    },
    'CM': {
        'nom': 'Cameroun',
        'nom_anglais': 'Cameroon',
        'code_iso_3': 'CMR',
        'continent': 'Afrique',
        'sous_region': 'Afrique Centrale',
        'capitale': 'Yaoundé',
        'latitude': Decimal('7.3697'),
        'longitude': Decimal('12.3547'),
        'indicatif': '+237',
        'devise': 'XAF',
        'provinces': [
            {'code': 'YAO', 'nom': 'Yaoundé'},
            {'code': 'DOU', 'nom': 'Douala'},
        ]
    },
    'GA': {
        'nom': 'Gabon',
        'nom_anglais': 'Gabon',
        'code_iso_3': 'GAB',
        'continent': 'Afrique',
        'sous_region': 'Afrique Centrale',
        'capitale': 'Libreville',
        'latitude': Decimal('-0.8037'),
        'longitude': Decimal('11.6094'),
        'indicatif': '+241',
        'devise': 'XAF',
        'provinces': [
            {'code': 'LIB', 'nom': 'Libreville'},
        ]
    },
    'CF': {
        'nom': 'République Centrafricaine',
        'nom_anglais': 'Central African Republic',
        'code_iso_3': 'CAF',
        'continent': 'Afrique',
        'sous_region': 'Afrique Centrale',
        'capitale': 'Bangui',
        'latitude': Decimal('6.6111'),
        'longitude': Decimal('20.9394'),
        'indicatif': '+236',
        'devise': 'XAF',
        'provinces': [
            {'code': 'BAN', 'nom': 'Bangui'},
        ]
    },
    
    # Afrique de l'Ouest
    'SN': {
        'nom': 'Sénégal',
        'nom_anglais': 'Senegal',
        'code_iso_3': 'SEN',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Ouest',
        'capitale': 'Dakar',
        'latitude': Decimal('14.4974'),
        'longitude': Decimal('-14.4524'),
        'indicatif': '+221',
        'devise': 'XOF',
        'provinces': [
            {'code': 'DAK', 'nom': 'Dakar'},
            {'code': 'THI', 'nom': 'Thiès'},
            {'code': 'SLO', 'nom': 'Saint-Louis'},
        ]
    },
    'CI': {
        'nom': 'Côte d\'Ivoire',
        'nom_anglais': 'Ivory Coast',
        'code_iso_3': 'CIV',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Ouest',
        'capitale': 'Yamoussoukro',
        'latitude': Decimal('7.5400'),
        'longitude': Decimal('-5.5471'),
        'indicatif': '+225',
        'devise': 'XOF',
        'provinces': [
            {'code': 'ABI', 'nom': 'Abidjan'},
            {'code': 'YAM', 'nom': 'Yamoussoukro'},
        ]
    },
    'GH': {
        'nom': 'Ghana',
        'nom_anglais': 'Ghana',
        'code_iso_3': 'GHA',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Ouest',
        'capitale': 'Accra',
        'latitude': Decimal('7.9465'),
        'longitude': Decimal('-1.0232'),
        'indicatif': '+233',
        'devise': 'GHS',
        'provinces': [
            {'code': 'ACC', 'nom': 'Accra'},
            {'code': 'KUM', 'nom': 'Kumasi'},
        ]
    },
    'NG': {
        'nom': 'Nigeria',
        'nom_anglais': 'Nigeria',
        'code_iso_3': 'NGA',
        'continent': 'Afrique',
        'sous_region': 'Afrique de l\'Ouest',
        'capitale': 'Abuja',
        'latitude': Decimal('9.0820'),
        'longitude': Decimal('8.6753'),
        'indicatif': '+234',
        'devise': 'NGN',
        'provinces': [
            {'code': 'ABU', 'nom': 'Abuja'},
            {'code': 'LAG', 'nom': 'Lagos'},
            {'code': 'KAN', 'nom': 'Kano'},
        ]
    },
    
    # Afrique du Nord
    'MA': {
        'nom': 'Maroc',
        'nom_anglais': 'Morocco',
        'code_iso_3': 'MAR',
        'continent': 'Afrique',
        'sous_region': 'Afrique du Nord',
        'capitale': 'Rabat',
        'latitude': Decimal('31.7917'),
        'longitude': Decimal('-7.0926'),
        'indicatif': '+212',
        'devise': 'MAD',
        'provinces': [
            {'code': 'RAB', 'nom': 'Rabat'},
            {'code': 'CAS', 'nom': 'Casablanca'},
            {'code': 'MAR', 'nom': 'Marrakech'},
        ]
    },
    'DZ': {
        'nom': 'Algérie',
        'nom_anglais': 'Algeria',
        'code_iso_3': 'DZA',
        'continent': 'Afrique',
        'sous_region': 'Afrique du Nord',
        'capitale': 'Alger',
        'latitude': Decimal('28.0339'),
        'longitude': Decimal('1.6596'),
        'indicatif': '+213',
        'devise': 'DZD',
        'provinces': [
            {'code': 'ALG', 'nom': 'Alger'},
            {'code': 'ORA', 'nom': 'Oran'},
        ]
    },
    'TN': {
        'nom': 'Tunisie',
        'nom_anglais': 'Tunisia',
        'code_iso_3': 'TUN',
        'continent': 'Afrique',
        'sous_region': 'Afrique du Nord',
        'capitale': 'Tunis',
        'latitude': Decimal('33.8869'),
        'longitude': Decimal('9.5375'),
        'indicatif': '+216',
        'devise': 'TND',
        'provinces': [
            {'code': 'TUN', 'nom': 'Tunis'},
        ]
    },
    'EG': {
        'nom': 'Égypte',
        'nom_anglais': 'Egypt',
        'code_iso_3': 'EGY',
        'continent': 'Afrique',
        'sous_region': 'Afrique du Nord',
        'capitale': 'Le Caire',
        'latitude': Decimal('26.8206'),
        'longitude': Decimal('30.8025'),
        'indicatif': '+20',
        'devise': 'EGP',
        'provinces': [
            {'code': 'CAI', 'nom': 'Le Caire'},
            {'code': 'ALE', 'nom': 'Alexandrie'},
        ]
    },
    
    # Afrique Australe
    'ZA': {
        'nom': 'Afrique du Sud',
        'nom_anglais': 'South Africa',
        'code_iso_3': 'ZAF',
        'continent': 'Afrique',
        'sous_region': 'Afrique Australe',
        'capitale': 'Pretoria',
        'latitude': Decimal('-30.5595'),
        'longitude': Decimal('22.9375'),
        'indicatif': '+27',
        'devise': 'ZAR',
        'provinces': [
            {'code': 'GAU', 'nom': 'Gauteng'},
            {'code': 'WCA', 'nom': 'Western Cape'},
            {'code': 'KZN', 'nom': 'KwaZulu-Natal'},
        ]
    },
}


# =============================================================================
# FONCTIONS D'ANALYSE
# =============================================================================

def analyser_couverture_pays():
    """Analyse la couverture géographique de chaque pays"""
    print("\n" + "="*80)
    print("ANALYSE DE LA COUVERTURE GÉOGRAPHIQUE")
    print("="*80)
    
    pays_list = Pays.objects.all().annotate(
        nb_provinces=Count('provinces'),
        nb_districts=Count('provinces__districts'),
        nb_quartiers=Count('provinces__districts__quartiers')
    ).order_by('nom')
    
    print(f"\nTotal pays dans la base: {pays_list.count()}")
    print("\n{:<30} {:<10} {:<12} {:<12} {:<12}".format(
        "Pays", "Code", "Provinces", "Districts", "Quartiers"
    ))
    print("-" * 80)
    
    pays_incomplets = []
    
    for pays in pays_list:
        statut = "✅" if pays.nb_provinces > 0 else "❌"
        print(f"{statut} {pays.nom:<28} {pays.code_iso_2:<10} {pays.nb_provinces:<12} {pays.nb_districts:<12} {pays.nb_quartiers:<12}")
        
        if pays.nb_provinces == 0:
            pays_incomplets.append(pays)
    
    print("\n" + "="*80)
    print(f"RÉSUMÉ: {len(pays_incomplets)} pays sans divisions administratives")
    print("="*80)
    
    if pays_incomplets:
        print("\nPays à compléter:")
        for pays in pays_incomplets:
            print(f"  - {pays.nom} ({pays.code_iso_2})")
    
    return pays_incomplets


def verifier_colonnes_continent():
    """Vérifie si les colonnes continent et sous_region existent"""
    print("\n" + "="*80)
    print("VÉRIFICATION DES COLONNES CONTINENT ET SOUS-RÉGION")
    print("="*80)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'localisation' 
            AND table_name = 'pays'
            ORDER BY ordinal_position;
        """)
        colonnes = cursor.fetchall()
    
    colonnes_existantes = [col[0] for col in colonnes]
    
    print("\nColonnes actuelles dans localisation.pays:")
    for col_name, col_type in colonnes:
        print(f"  - {col_name} ({col_type})")
    
    continent_existe = 'continent' in colonnes_existantes
    sous_region_existe = 'sous_region' in colonnes_existantes
    
    print(f"\n✅ Colonne 'continent': {'Existe' if continent_existe else 'N\'existe pas'}")
    print(f"✅ Colonne 'sous_region': {'Existe' if sous_region_existe else 'N\'existe pas'}")
    
    return continent_existe, sous_region_existe


def ajouter_colonnes_geographiques():
    """Ajoute les colonnes continent et sous_region"""
    print("\n" + "="*80)
    print("AJOUT DES COLONNES GÉOGRAPHIQUES")
    print("="*80)
    
    with connection.cursor() as cursor:
        try:
            # Ajouter colonne continent
            print("\n1. Ajout de la colonne 'continent'...")
            cursor.execute("""
                ALTER TABLE localisation.pays 
                ADD COLUMN IF NOT EXISTS continent VARCHAR(50);
            """)
            print("   ✅ Colonne 'continent' ajoutée")
            
            # Ajouter colonne sous_region
            print("\n2. Ajout de la colonne 'sous_region'...")
            cursor.execute("""
                ALTER TABLE localisation.pays 
                ADD COLUMN IF NOT EXISTS sous_region VARCHAR(100);
            """)
            print("   ✅ Colonne 'sous_region' ajoutée")
            
            # Créer des index pour améliorer les performances
            print("\n3. Création des index...")
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_pays_continent 
                ON localisation.pays(continent);
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_pays_sous_region 
                ON localisation.pays(sous_region);
            """)
            print("   ✅ Index créés")
            
            connection.commit()
            print("\n✅ Colonnes géographiques ajoutées avec succès!")
            
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            connection.rollback()


def peupler_pays_africains():
    """Peuple les pays africains avec leurs données"""
    print("\n" + "="*80)
    print("PEUPLEMENT DES PAYS AFRICAINS")
    print("="*80)
    
    stats = {
        'pays_crees': 0,
        'pays_mis_a_jour': 0,
        'provinces_creees': 0,
        'erreurs': []
    }
    
    for code_iso_2, data in PAYS_AFRICAINS.items():
        try:
            print(f"\n📍 Traitement: {data['nom']} ({code_iso_2})")
            
            # Créer ou mettre à jour le pays
            pays, created = Pays.objects.update_or_create(
                code_iso_2=code_iso_2,
                defaults={
                    'code_iso_3': data['code_iso_3'],
                    'nom': data['nom'],
                    'nom_anglais': data['nom_anglais'],
                    'latitude_centre': data['latitude'],
                    'longitude_centre': data['longitude'],
                    'autorise_systeme': True,
                    'est_actif': True,
                    'metadonnees': {
                        'continent': data['continent'],
                        'sous_region': data['sous_region'],
                        'capitale': data['capitale'],
                        'telephonie': {
                            'code_telephonique': data['indicatif'],
                        },
                        'devise': {
                            'code': data['devise'],
                        }
                    }
                }
            )
            
            if created:
                stats['pays_crees'] += 1
                print(f"   ✅ Pays créé")
            else:
                stats['pays_mis_a_jour'] += 1
                print(f"   ✅ Pays mis à jour")
            
            # Mettre à jour continent et sous_region via SQL direct
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE localisation.pays 
                    SET continent = %s, sous_region = %s 
                    WHERE code_iso_2 = %s
                """, [data['continent'], data['sous_region'], code_iso_2])
            
            # Créer les provinces
            if 'provinces' in data:
                print(f"   📂 Création de {len(data['provinces'])} provinces...")
                for prov_data in data['provinces']:
                    province, prov_created = Province.objects.get_or_create(
                        pays=pays,
                        code=prov_data['code'],
                        defaults={
                            'nom': prov_data['nom'],
                            'autorise_systeme': True,
                            'est_actif': True,
                        }
                    )
                    if prov_created:
                        stats['provinces_creees'] += 1
                        print(f"      ✅ {prov_data['nom']}")
        
        except Exception as e:
            error_msg = f"Erreur pour {code_iso_2}: {str(e)}"
            stats['erreurs'].append(error_msg)
            print(f"   ❌ {error_msg}")
    
    print("\n" + "="*80)
    print("RÉSUMÉ DU PEUPLEMENT")
    print("="*80)
    print(f"Pays créés: {stats['pays_crees']}")
    print(f"Pays mis à jour: {stats['pays_mis_a_jour']}")
    print(f"Provinces créées: {stats['provinces_creees']}")
    print(f"Erreurs: {len(stats['erreurs'])}")
    
    if stats['erreurs']:
        print("\nErreurs rencontrées:")
        for err in stats['erreurs']:
            print(f"  - {err}")
    
    return stats


def afficher_statistiques_finales():
    """Affiche les statistiques finales"""
    print("\n" + "="*80)
    print("STATISTIQUES FINALES")
    print("="*80)
    
    # Statistiques par continent
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COALESCE(continent, 'Non défini') as continent,
                COUNT(*) as nb_pays,
                SUM(CASE WHEN EXISTS (
                    SELECT 1 FROM localisation.provinces p WHERE p.pays_id = pays.id
                ) THEN 1 ELSE 0 END) as pays_avec_provinces
            FROM localisation.pays
            GROUP BY continent
            ORDER BY continent;
        """)
        stats_continent = cursor.fetchall()
    
    print("\nPar continent:")
    print("{:<30} {:<15} {:<20}".format("Continent", "Nb Pays", "Avec Provinces"))
    print("-" * 70)
    for continent, nb_pays, avec_prov in stats_continent:
        print(f"{continent:<30} {nb_pays:<15} {avec_prov:<20}")
    
    # Statistiques par sous-région
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COALESCE(sous_region, 'Non défini') as sous_region,
                COUNT(*) as nb_pays,
                SUM(CASE WHEN EXISTS (
                    SELECT 1 FROM localisation.provinces p WHERE p.pays_id = pays.id
                ) THEN 1 ELSE 0 END) as pays_avec_provinces
            FROM localisation.pays
            WHERE continent = 'Afrique' OR continent IS NULL
            GROUP BY sous_region
            ORDER BY sous_region;
        """)
        stats_sous_region = cursor.fetchall()
    
    print("\nPar sous-région (Afrique):")
    print("{:<30} {:<15} {:<20}".format("Sous-région", "Nb Pays", "Avec Provinces"))
    print("-" * 70)
    for sous_region, nb_pays, avec_prov in stats_sous_region:
        print(f"{sous_region:<30} {nb_pays:<15} {avec_prov:<20}")
    
    # Total général
    total_pays = Pays.objects.count()
    total_provinces = Province.objects.count()
    total_districts = District.objects.count()
    total_quartiers = Quartier.objects.count()
    
    print("\nTotal général:")
    print(f"  Pays: {total_pays}")
    print(f"  Provinces: {total_provinces}")
    print(f"  Districts: {total_districts}")
    print(f"  Quartiers: {total_quartiers}")


# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("SCRIPT D'ANALYSE ET COMPLÉTION DE LA LOCALISATION")
    print("="*80)
    print("\nCe script va:")
    print("1. Analyser la couverture géographique actuelle")
    print("2. Vérifier/Ajouter les colonnes continent et sous_region")
    print("3. Peupler les pays africains avec leurs divisions")
    print("4. Afficher les statistiques finales")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # 1. Analyser la couverture actuelle
    pays_incomplets = analyser_couverture_pays()
    
    # 2. Vérifier et ajouter les colonnes
    continent_existe, sous_region_existe = verifier_colonnes_continent()
    
    if not continent_existe or not sous_region_existe:
        reponse = input("\nVoulez-vous ajouter les colonnes manquantes? (o/n): ")
        if reponse.lower() == 'o':
            ajouter_colonnes_geographiques()
    
    # 3. Peupler les pays africains
    reponse = input("\nVoulez-vous peupler les pays africains? (o/n): ")
    if reponse.lower() == 'o':
        stats = peupler_pays_africains()
    
    # 4. Afficher les statistiques finales
    afficher_statistiques_finales()
    
    print("\n" + "="*80)
    print("✅ SCRIPT TERMINÉ")
    print("="*80)


if __name__ == '__main__':
    main()
