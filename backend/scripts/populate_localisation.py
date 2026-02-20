"""
Script pour peupler la base de données avec les données de localisation
Burundi et Rwanda avec leurs provinces, districts, quartiers et points de service

Usage:
    python scripts/populate_localisation.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier, PointDeService


def creer_pays():
    """Créer les pays"""
    print("📍 Création des pays...")
    
    # Burundi
    burundi, created = Pays.objects.get_or_create(
        code_iso_2='BI',
        defaults={
            'code_iso_3': 'BDI',
            'nom': 'Burundi',
            'nom_anglais': 'Burundi',
            'continent': 'Afrique',
            'sous_region': 'Afrique de l\'Est',
            'latitude_centre': -3.3731,
            'longitude_centre': 29.9189,
            'autorise_systeme': True,
            'est_actif': True,
            'metadonnees': {
                'capitale': 'Gitega',
                'capitale_economique': 'Bujumbura',
                'population': 12889576,
                'superficie_km2': 27834,
                'devise': 'BIF',
                'code_devise': 'BIF',
                'langues': ['Kirundi', 'Français', 'Anglais'],
                'telephonie': {
                    'code_pays': '+257',
                    'format_numero_national': 'XX XX XX XX',
                    'operateurs': ['Econet', 'Lumitel', 'Smart']
                },
                'fuseau_horaire': 'Africa/Bujumbura',
                'domaine_internet': '.bi'
            }
        }
    )
    print(f"  {'✅ Créé' if created else '✓ Existe'}: {burundi.nom}")
    
    # Rwanda
    rwanda, created = Pays.objects.get_or_create(
        code_iso_2='RW',
        defaults={
            'code_iso_3': 'RWA',
            'nom': 'Rwanda',
            'nom_anglais': 'Rwanda',
            'continent': 'Afrique',
            'sous_region': 'Afrique de l\'Est',
            'latitude_centre': -1.9403,
            'longitude_centre': 29.8739,
            'autorise_systeme': True,
            'est_actif': True,
            'metadonnees': {
                'capitale': 'Kigali',
                'population': 13776698,
                'superficie_km2': 26338,
                'devise': 'Franc rwandais',
                'code_devise': 'RWF',
                'langues': ['Kinyarwanda', 'Français', 'Anglais', 'Swahili'],
                'telephonie': {
                    'code_pays': '+250',
                    'format_numero_national': 'XXX XXX XXX',
                    'operateurs': ['MTN', 'Airtel']
                },
                'fuseau_horaire': 'Africa/Kigali',
                'domaine_internet': '.rw'
            }
        }
    )
    print(f"  {'✅ Créé' if created else '✓ Existe'}: {rwanda.nom}")
    
    return burundi, rwanda


def creer_provinces_burundi(burundi):
    """Créer les provinces du Burundi"""
    print("\n🏛️  Création des provinces du Burundi...")
    
    provinces_data = [
        {'code': 'BB', 'nom': 'Bubanza', 'lat': -3.0833, 'lon': 29.3833},
        {'code': 'BM', 'nom': 'Bujumbura Mairie', 'lat': -3.3614, 'lon': 29.3599},
        {'code': 'BR', 'nom': 'Bujumbura Rural', 'lat': -3.5000, 'lon': 29.5000},
        {'code': 'BR', 'nom': 'Bururi', 'lat': -3.9500, 'lon': 29.6167},
        {'code': 'CA', 'nom': 'Cankuzo', 'lat': -3.2167, 'lon': 30.6000},
        {'code': 'CI', 'nom': 'Cibitoke', 'lat': -2.8833, 'lon': 29.1167},
        {'code': 'GI', 'nom': 'Gitega', 'lat': -3.4271, 'lon': 29.9246},
        {'code': 'KR', 'nom': 'Karuzi', 'lat': -3.1000, 'lon': 30.1667},
        {'code': 'KY', 'nom': 'Kayanza', 'lat': -2.9167, 'lon': 29.6333},
        {'code': 'KI', 'nom': 'Kirundo', 'lat': -2.5833, 'lon': 30.1000},
        {'code': 'MA', 'nom': 'Makamba', 'lat': -4.1333, 'lon': 29.8000},
        {'code': 'MU', 'nom': 'Muramvya', 'lat': -3.2667, 'lon': 29.6167},
        {'code': 'MW', 'nom': 'Mwaro', 'lat': -3.5167, 'lon': 29.7000},
        {'code': 'MY', 'nom': 'Muyinga', 'lat': -2.8500, 'lon': 30.3333},
        {'code': 'NG', 'nom': 'Ngozi', 'lat': -2.9083, 'lon': 29.8306},
        {'code': 'RM', 'nom': 'Rumonge', 'lat': -3.9733, 'lon': 29.4386},
        {'code': 'RT', 'nom': 'Rutana', 'lat': -3.9167, 'lon': 30.0000},
        {'code': 'RY', 'nom': 'Ruyigi', 'lat': -3.4833, 'lon': 30.2500},
    ]
    
    provinces = []
    for data in provinces_data:
        province, created = Province.objects.get_or_create(
            pays=burundi,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'latitude_centre': data['lat'],
                'longitude_centre': data['lon'],
                'autorise_systeme': True,
                'est_actif': True,
                'metadonnees': {
                    'type': 'province',
                    'pays': 'Burundi'
                }
            }
        )
        provinces.append(province)
        print(f"  {'✅' if created else '✓'} {province.nom}")
    
    return provinces


def creer_districts_bujumbura(bujumbura_mairie):
    """Créer les districts de Bujumbura Mairie"""
    print("\n🏙️  Création des districts de Bujumbura Mairie...")
    
    districts_data = [
        {'code': 'MUK', 'nom': 'Mukaza', 'lat': -3.3614, 'lon': 29.3599},
        {'code': 'MUR', 'nom': 'Muha', 'lat': -3.3833, 'lon': 29.3667},
        {'code': 'NTH', 'nom': 'Ntahangwa', 'lat': -3.3500, 'lon': 29.3833},
    ]
    
    districts = []
    for data in districts_data:
        district, created = District.objects.get_or_create(
            province=bujumbura_mairie,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'latitude_centre': data['lat'],
                'longitude_centre': data['lon'],
                'autorise_systeme': True,
                'est_actif': True,
                'metadonnees': {
                    'type': 'urbain',
                    'ville': 'Bujumbura'
                }
            }
        )
        districts.append(district)
        print(f"  {'✅' if created else '✓'} {district.nom}")
    
    return districts


def creer_quartiers_mukaza(mukaza):
    """Créer les quartiers du district Mukaza"""
    print("\n🏘️  Création des quartiers de Mukaza...")
    
    quartiers_data = [
        {'code': 'ROH', 'nom': 'Rohero', 'lat': -3.3614, 'lon': 29.3599},
        {'code': 'AST', 'nom': 'Asticot', 'lat': -3.3650, 'lon': 29.3620},
        {'code': 'CEN', 'nom': 'Centre Ville', 'lat': -3.3750, 'lon': 29.3600},
        {'code': 'BUY', 'nom': 'Buyenzi', 'lat': -3.3800, 'lon': 29.3550},
        {'code': 'BWT', 'nom': 'Bwiza', 'lat': -3.3700, 'lon': 29.3650},
        {'code': 'NYA', 'nom': 'Nyakabiga', 'lat': -3.3850, 'lon': 29.3600},
    ]
    
    quartiers = []
    for data in quartiers_data:
        quartier, created = Quartier.objects.get_or_create(
            district=mukaza,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'latitude_centre': data['lat'],
                'longitude_centre': data['lon'],
                'autorise_systeme': True,
                'est_actif': True,
                'metadonnees': {
                    'type': 'residentiel',
                    'district': 'Mukaza'
                }
            }
        )
        quartiers.append(quartier)
        print(f"  {'✅' if created else '✓'} {quartier.nom}")
    
    return quartiers


def creer_points_service_rohero(rohero):
    """Créer des points de service dans le quartier Rohero"""
    print("\n📍 Création des points de service à Rohero...")
    
    points_data = [
        {
            'code': 'AG-ROH-001',
            'nom': 'Agent Rohero Centre',
            'type': 'AGENT',
            'lat': -3.3614,
            'lon': 29.3599,
            'adresse': 'Avenue de la Liberté, N°123',
            'meta': {
                'horaires': {
                    'lundi_vendredi': '08:00-17:00',
                    'samedi': '08:00-12:00',
                    'dimanche': 'Fermé'
                },
                'services': ['Dépôt', 'Retrait', 'Transfert', 'Paiement factures'],
                'capacite_journaliere': 100,
                'telephone': '+257 22 123 456'
            }
        },
        {
            'code': 'GU-ROH-001',
            'nom': 'Guichet Rohero Plaza',
            'type': 'GUICHET',
            'lat': -3.3620,
            'lon': 29.3605,
            'adresse': 'Rohero Plaza, 1er étage',
            'meta': {
                'horaires': {
                    'lundi_vendredi': '08:30-16:30',
                    'samedi': '09:00-13:00',
                    'dimanche': 'Fermé'
                },
                'services': ['Dépôt', 'Retrait', 'Ouverture compte'],
                'telephone': '+257 22 234 567'
            }
        },
        {
            'code': 'PA-ROH-001',
            'nom': 'Partenaire Supermarché Rohero',
            'type': 'PARTENAIRE',
            'lat': -3.3625,
            'lon': 29.3610,
            'adresse': 'Supermarché City Center',
            'meta': {
                'horaires': {
                    'lundi_dimanche': '07:00-21:00'
                },
                'services': ['Dépôt', 'Retrait'],
                'partenaire': 'City Center Supermarket'
            }
        },
    ]
    
    points = []
    for data in points_data:
        point, created = PointDeService.objects.get_or_create(
            quartier=rohero,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'type_point': data['type'],
                'latitude': data['lat'],
                'longitude': data['lon'],
                'adresse_complementaire': data['adresse'],
                'autorise_systeme': True,
                'est_actif': True,
                'metadonnees': data['meta']
            }
        )
        points.append(point)
        print(f"  {'✅' if created else '✓'} {point.nom} ({point.type_point})")
    
    return points


def creer_provinces_rwanda(rwanda):
    """Créer les provinces du Rwanda"""
    print("\n🏛️  Création des provinces du Rwanda...")
    
    provinces_data = [
        {'code': 'KIG', 'nom': 'Kigali', 'lat': -1.9536, 'lon': 30.0606},
        {'code': 'EST', 'nom': 'Est', 'lat': -2.0000, 'lon': 30.5000},
        {'code': 'NOR', 'nom': 'Nord', 'lat': -1.5000, 'lon': 29.8000},
        {'code': 'OUE', 'nom': 'Ouest', 'lat': -2.3000, 'lon': 29.3000},
        {'code': 'SUD', 'nom': 'Sud', 'lat': -2.6000, 'lon': 29.7000},
    ]
    
    provinces = []
    for data in provinces_data:
        province, created = Province.objects.get_or_create(
            pays=rwanda,
            code=data['code'],
            defaults={
                'nom': data['nom'],
                'latitude_centre': data['lat'],
                'longitude_centre': data['lon'],
                'autorise_systeme': True,
                'est_actif': True,
                'metadonnees': {
                    'type': 'province',
                    'pays': 'Rwanda'
                }
            }
        )
        provinces.append(province)
        print(f"  {'✅' if created else '✓'} {province.nom}")
    
    return provinces


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 PEUPLEMENT DE LA BASE DE DONNÉES - LOCALISATION")
    print("=" * 60)
    
    try:
        # Créer les pays
        burundi, rwanda = creer_pays()
        
        # Créer les provinces du Burundi
        provinces_burundi = creer_provinces_burundi(burundi)
        
        # Trouver Bujumbura Mairie
        bujumbura_mairie = Province.objects.get(pays=burundi, code='BM')
        
        # Créer les districts de Bujumbura
        districts_bujumbura = creer_districts_bujumbura(bujumbura_mairie)
        
        # Trouver Mukaza
        mukaza = District.objects.get(province=bujumbura_mairie, code='MUK')
        
        # Créer les quartiers de Mukaza
        quartiers_mukaza = creer_quartiers_mukaza(mukaza)
        
        # Trouver Rohero
        rohero = Quartier.objects.get(district=mukaza, code='ROH')
        
        # Créer les points de service à Rohero
        points_rohero = creer_points_service_rohero(rohero)
        
        # Créer les provinces du Rwanda
        provinces_rwanda = creer_provinces_rwanda(rwanda)
        
        print("\n" + "=" * 60)
        print("✅ PEUPLEMENT TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"\n📊 Statistiques:")
        print(f"  • Pays: {Pays.objects.count()}")
        print(f"  • Provinces: {Province.objects.count()}")
        print(f"  • Districts: {District.objects.count()}")
        print(f"  • Quartiers: {Quartier.objects.count()}")
        print(f"  • Points de service: {PointDeService.objects.count()}")
        print("\n✨ Vous pouvez maintenant utiliser les endpoints de localisation!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
