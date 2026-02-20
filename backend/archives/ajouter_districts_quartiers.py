"""
Script pour ajouter des districts et quartiers aux provinces existantes
Focus sur les grandes villes et capitales
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier
from decimal import Decimal


# =============================================================================
# DONNÉES DES DISTRICTS ET QUARTIERS
# =============================================================================

DISTRICTS_QUARTIERS = {
    'BI': {  # Burundi
        'BM': {  # Bujumbura Mairie
            'nom_province': 'Bujumbura Mairie',
            'districts': [
                {
                    'code': 'MUK',
                    'nom': 'Mukaza',
                    'quartiers': [
                        {'code': 'ROH', 'nom': 'Rohero'},
                        {'code': 'AST', 'nom': 'Asiatique'},
                        {'code': 'CEN', 'nom': 'Centre Ville'},
                        {'code': 'BUY', 'nom': 'Buyenzi'},
                        {'code': 'NYA', 'nom': 'Nyakabiga'},
                    ]
                },
                {
                    'code': 'NTH',
                    'nom': 'Ntahangwa',
                    'quartiers': [
                        {'code': 'KAM', 'nom': 'Kamenge'},
                        {'code': 'KIN', 'nom': 'Kinindo'},
                        {'code': 'KAN', 'nom': 'Kanyosha'},
                        {'code': 'MUS', 'nom': 'Musaga'},
                    ]
                },
                {
                    'code': 'MUR',
                    'nom': 'Muramvya',
                    'quartiers': [
                        {'code': 'GIH', 'nom': 'Gihosha'},
                        {'code': 'KAB', 'nom': 'Kabondo'},
                    ]
                },
            ]
        },
        'GI': {  # Gitega
            'nom_province': 'Gitega',
            'districts': [
                {
                    'code': 'GIT',
                    'nom': 'Gitega Ville',
                    'quartiers': [
                        {'code': 'MAR', 'nom': 'Maramvya'},
                        {'code': 'MUK', 'nom': 'Mushasha'},
                    ]
                },
            ]
        },
    },
    'RW': {  # Rwanda
        'KIG': {  # Kigali
            'nom_province': 'Kigali',
            'districts': [
                {
                    'code': 'GAS',
                    'nom': 'Gasabo',
                    'quartiers': [
                        {'code': 'KIM', 'nom': 'Kimihurura'},
                        {'code': 'REM', 'nom': 'Remera'},
                        {'code': 'KIC', 'nom': 'Kicukiro'},
                    ]
                },
                {
                    'code': 'KIC',
                    'nom': 'Kicukiro',
                    'quartiers': [
                        {'code': 'GIK', 'nom': 'Gikondo'},
                        {'code': 'KAN', 'nom': 'Kanombe'},
                    ]
                },
                {
                    'code': 'NYA',
                    'nom': 'Nyarugenge',
                    'quartiers': [
                        {'code': 'CEN', 'nom': 'Centre Ville'},
                        {'code': 'NYA', 'nom': 'Nyamirambo'},
                    ]
                },
            ]
        },
    },
    'KE': {  # Kenya
        'NAI': {  # Nairobi
            'nom_province': 'Nairobi',
            'districts': [
                {
                    'code': 'CBD',
                    'nom': 'Central Business District',
                    'quartiers': [
                        {'code': 'CEN', 'nom': 'City Centre'},
                        {'code': 'UPT', 'nom': 'Upperhill'},
                    ]
                },
                {
                    'code': 'WES',
                    'nom': 'Westlands',
                    'quartiers': [
                        {'code': 'WES', 'nom': 'Westlands'},
                        {'code': 'KIL', 'nom': 'Kilimani'},
                    ]
                },
            ]
        },
    },
    'CD': {  # RD Congo
        'KIN': {  # Kinshasa
            'nom_province': 'Kinshasa',
            'districts': [
                {
                    'code': 'GOM',
                    'nom': 'Gombe',
                    'quartiers': [
                        {'code': 'CEN', 'nom': 'Centre Ville'},
                        {'code': 'LIM', 'nom': 'Limete'},
                    ]
                },
                {
                    'code': 'KAL',
                    'nom': 'Kalamu',
                    'quartiers': [
                        {'code': 'KAL', 'nom': 'Kalamu'},
                        {'code': 'MAT', 'nom': 'Matonge'},
                    ]
                },
                {
                    'code': 'NGI',
                    'nom': 'Ngiri-Ngiri',
                    'quartiers': [
                        {'code': 'NGI', 'nom': 'Ngiri-Ngiri'},
                    ]
                },
            ]
        },
    },
    'SN': {  # Sénégal
        'DAK': {  # Dakar
            'nom_province': 'Dakar',
            'districts': [
                {
                    'code': 'PLA',
                    'nom': 'Plateau',
                    'quartiers': [
                        {'code': 'PLA', 'nom': 'Plateau'},
                        {'code': 'MED', 'nom': 'Médina'},
                    ]
                },
                {
                    'code': 'ALM',
                    'nom': 'Almadies',
                    'quartiers': [
                        {'code': 'ALM', 'nom': 'Almadies'},
                        {'code': 'NGA', 'nom': 'Ngor'},
                    ]
                },
            ]
        },
    },
    'NG': {  # Nigeria
        'LAG': {  # Lagos
            'nom_province': 'Lagos',
            'districts': [
                {
                    'code': 'ISL',
                    'nom': 'Lagos Island',
                    'quartiers': [
                        {'code': 'VIC', 'nom': 'Victoria Island'},
                        {'code': 'IKO', 'nom': 'Ikoyi'},
                    ]
                },
                {
                    'code': 'MAI',
                    'nom': 'Lagos Mainland',
                    'quartiers': [
                        {'code': 'YAB', 'nom': 'Yaba'},
                        {'code': 'SUR', 'nom': 'Surulere'},
                    ]
                },
            ]
        },
    },
    'MA': {  # Maroc
        'CAS': {  # Casablanca
            'nom_province': 'Casablanca',
            'districts': [
                {
                    'code': 'AIN',
                    'nom': 'Ain Chock',
                    'quartiers': [
                        {'code': 'AIN', 'nom': 'Ain Chock'},
                    ]
                },
                {
                    'code': 'ANA',
                    'nom': 'Anfa',
                    'quartiers': [
                        {'code': 'ANA', 'nom': 'Anfa'},
                        {'code': 'MAA', 'nom': 'Maarif'},
                    ]
                },
            ]
        },
    },
    'EG': {  # Égypte
        'CAI': {  # Le Caire
            'nom_province': 'Le Caire',
            'districts': [
                {
                    'code': 'NAC',
                    'nom': 'Nasr City',
                    'quartiers': [
                        {'code': 'NAC', 'nom': 'Nasr City'},
                    ]
                },
                {
                    'code': 'HEL',
                    'nom': 'Heliopolis',
                    'quartiers': [
                        {'code': 'HEL', 'nom': 'Heliopolis'},
                    ]
                },
            ]
        },
    },
    'ZA': {  # Afrique du Sud
        'GAU': {  # Gauteng
            'nom_province': 'Gauteng',
            'districts': [
                {
                    'code': 'JHB',
                    'nom': 'Johannesburg',
                    'quartiers': [
                        {'code': 'CBD', 'nom': 'CBD'},
                        {'code': 'SAN', 'nom': 'Sandton'},
                        {'code': 'SOW', 'nom': 'Soweto'},
                    ]
                },
                {
                    'code': 'PTA',
                    'nom': 'Pretoria',
                    'quartiers': [
                        {'code': 'CEN', 'nom': 'Pretoria Central'},
                        {'code': 'HAT', 'nom': 'Hatfield'},
                    ]
                },
            ]
        },
    },
}


# =============================================================================
# FONCTIONS
# =============================================================================

def ajouter_districts_quartiers():
    """Ajoute les districts et quartiers pour les provinces définies"""
    print("\n" + "="*80)
    print("AJOUT DES DISTRICTS ET QUARTIERS")
    print("="*80)
    
    stats = {
        'districts_crees': 0,
        'quartiers_crees': 0,
        'erreurs': []
    }
    
    for code_pays, provinces_data in DISTRICTS_QUARTIERS.items():
        try:
            pays = Pays.objects.get(code_iso_2=code_pays)
            print(f"\n🌍 Pays: {pays.nom} ({code_pays})")
            
            for code_province, province_data in provinces_data.items():
                try:
                    province = Province.objects.get(
                        pays=pays,
                        code=code_province
                    )
                    print(f"\n  📂 Province: {province.nom}")
                    
                    # Créer les districts
                    for district_data in province_data['districts']:
                        district, created = District.objects.get_or_create(
                            province=province,
                            code=district_data['code'],
                            defaults={
                                'nom': district_data['nom'],
                                'autorise_systeme': True,
                                'est_actif': True,
                            }
                        )
                        
                        if created:
                            stats['districts_crees'] += 1
                            print(f"    ✅ District créé: {district.nom}")
                        else:
                            print(f"    ℹ️  District existe: {district.nom}")
                        
                        # Créer les quartiers
                        if 'quartiers' in district_data:
                            for quartier_data in district_data['quartiers']:
                                quartier, q_created = Quartier.objects.get_or_create(
                                    district=district,
                                    code=quartier_data['code'],
                                    defaults={
                                        'nom': quartier_data['nom'],
                                        'autorise_systeme': True,
                                        'est_actif': True,
                                    }
                                )
                                
                                if q_created:
                                    stats['quartiers_crees'] += 1
                                    print(f"      ✅ Quartier créé: {quartier.nom}")
                                else:
                                    print(f"      ℹ️  Quartier existe: {quartier.nom}")
                
                except Province.DoesNotExist:
                    error_msg = f"Province {code_province} introuvable pour {code_pays}"
                    stats['erreurs'].append(error_msg)
                    print(f"  ❌ {error_msg}")
        
        except Pays.DoesNotExist:
            error_msg = f"Pays {code_pays} introuvable"
            stats['erreurs'].append(error_msg)
            print(f"❌ {error_msg}")
        
        except Exception as e:
            error_msg = f"Erreur pour {code_pays}: {str(e)}"
            stats['erreurs'].append(error_msg)
            print(f"❌ {error_msg}")
    
    print("\n" + "="*80)
    print("RÉSUMÉ")
    print("="*80)
    print(f"Districts créés: {stats['districts_crees']}")
    print(f"Quartiers créés: {stats['quartiers_crees']}")
    print(f"Erreurs: {len(stats['erreurs'])}")
    
    if stats['erreurs']:
        print("\nErreurs rencontrées:")
        for err in stats['erreurs']:
            print(f"  - {err}")
    
    return stats


def afficher_statistiques():
    """Affiche les statistiques finales"""
    print("\n" + "="*80)
    print("STATISTIQUES FINALES")
    print("="*80)
    
    # Statistiques par pays
    pays_list = Pays.objects.filter(
        provinces__isnull=False
    ).distinct()
    
    print("\nPar pays:")
    print("{:<30} {:<12} {:<12} {:<12}".format(
        "Pays", "Provinces", "Districts", "Quartiers"
    ))
    print("-" * 70)
    
    for pays in pays_list:
        nb_provinces = Province.objects.filter(pays=pays).count()
        nb_districts = District.objects.filter(province__pays=pays).count()
        nb_quartiers = Quartier.objects.filter(district__province__pays=pays).count()
        
        if nb_districts > 0 or nb_quartiers > 0:
            print(f"{pays.nom:<30} {nb_provinces:<12} {nb_districts:<12} {nb_quartiers:<12}")
    
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


def main():
    """Fonction principale"""
    print("\n" + "="*80)
    print("SCRIPT D'AJOUT DES DISTRICTS ET QUARTIERS")
    print("="*80)
    print("\nCe script va ajouter des districts et quartiers pour:")
    print("- Les grandes villes et capitales")
    print("- Les provinces principales de chaque pays")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Ajouter les districts et quartiers
    stats = ajouter_districts_quartiers()
    
    # Afficher les statistiques
    afficher_statistiques()
    
    print("\n" + "="*80)
    print("✅ SCRIPT TERMINÉ")
    print("="*80)
    print(f"\nRésumé:")
    print(f"  - {stats['districts_crees']} districts créés")
    print(f"  - {stats['quartiers_crees']} quartiers créés")


if __name__ == '__main__':
    main()
