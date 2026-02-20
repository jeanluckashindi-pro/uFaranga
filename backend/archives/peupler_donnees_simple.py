"""
Script simplifié pour peupler les données de localisation
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province
from django.db import connection
from decimal import Decimal

print("\n" + "="*80)
print("PEUPLEMENT DES DONNÉES DE LOCALISATION")
print("="*80)

# Données des pays
PAYS_AFRICAINS = {
    'BI': {'nom': 'Burundi', 'nom_anglais': 'Burundi', 'code_iso_3': 'BDI', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Est', 'lat': Decimal('-3.3731'), 'lon': Decimal('29.9189'), 'capitale': 'Gitega', 'tel': '+257', 'devise': 'BIF', 'provinces': 17},
    'RW': {'nom': 'Rwanda', 'nom_anglais': 'Rwanda', 'code_iso_3': 'RWA', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Est', 'lat': Decimal('-1.9403'), 'lon': Decimal('29.8739'), 'capitale': 'Kigali', 'tel': '+250', 'devise': 'RWF', 'provinces': 5},
    'KE': {'nom': 'Kenya', 'nom_anglais': 'Kenya', 'code_iso_3': 'KEN', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Est', 'lat': Decimal('-0.0236'), 'lon': Decimal('37.9062'), 'capitale': 'Nairobi', 'tel': '+254', 'devise': 'KES', 'provinces': 4},
    'TZ': {'nom': 'Tanzanie', 'nom_anglais': 'Tanzania', 'code_iso_3': 'TZA', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Est', 'lat': Decimal('-6.3690'), 'lon': Decimal('34.8888'), 'capitale': 'Dodoma', 'tel': '+255', 'devise': 'TZS', 'provinces': 4},
    'UG': {'nom': 'Ouganda', 'nom_anglais': 'Uganda', 'code_iso_3': 'UGA', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Est', 'lat': Decimal('1.3733'), 'lon': Decimal('32.2903'), 'capitale': 'Kampala', 'tel': '+256', 'devise': 'UGX', 'provinces': 4},
    'CD': {'nom': 'République Démocratique du Congo', 'nom_anglais': 'Democratic Republic of the Congo', 'code_iso_3': 'COD', 'continent': 'Afrique', 'sous_region': 'Afrique Centrale', 'lat': Decimal('-4.0383'), 'lon': Decimal('21.7587'), 'capitale': 'Kinshasa', 'tel': '+243', 'devise': 'CDF', 'provinces': 8},
    'CG': {'nom': 'République du Congo', 'nom_anglais': 'Republic of the Congo', 'code_iso_3': 'COG', 'continent': 'Afrique', 'sous_region': 'Afrique Centrale', 'lat': Decimal('-4.2634'), 'lon': Decimal('15.2429'), 'capitale': 'Brazzaville', 'tel': '+242', 'devise': 'XAF', 'provinces': 2},
    'CM': {'nom': 'Cameroun', 'nom_anglais': 'Cameroon', 'code_iso_3': 'CMR', 'continent': 'Afrique', 'sous_region': 'Afrique Centrale', 'lat': Decimal('7.3697'), 'lon': Decimal('12.3547'), 'capitale': 'Yaoundé', 'tel': '+237', 'devise': 'XAF', 'provinces': 2},
    'GA': {'nom': 'Gabon', 'nom_anglais': 'Gabon', 'code_iso_3': 'GAB', 'continent': 'Afrique', 'sous_region': 'Afrique Centrale', 'lat': Decimal('-0.8037'), 'lon': Decimal('11.6094'), 'capitale': 'Libreville', 'tel': '+241', 'devise': 'XAF', 'provinces': 1},
    'CF': {'nom': 'République Centrafricaine', 'nom_anglais': 'Central African Republic', 'code_iso_3': 'CAF', 'continent': 'Afrique', 'sous_region': 'Afrique Centrale', 'lat': Decimal('6.6111'), 'lon': Decimal('20.9394'), 'capitale': 'Bangui', 'tel': '+236', 'devise': 'XAF', 'provinces': 1},
    'SN': {'nom': 'Sénégal', 'nom_anglais': 'Senegal', 'code_iso_3': 'SEN', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Ouest', 'lat': Decimal('14.4974'), 'lon': Decimal('-14.4524'), 'capitale': 'Dakar', 'tel': '+221', 'devise': 'XOF', 'provinces': 3},
    'CI': {'nom': 'Côte d\'Ivoire', 'nom_anglais': 'Ivory Coast', 'code_iso_3': 'CIV', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Ouest', 'lat': Decimal('7.5400'), 'lon': Decimal('-5.5471'), 'capitale': 'Yamoussoukro', 'tel': '+225', 'devise': 'XOF', 'provinces': 2},
    'GH': {'nom': 'Ghana', 'nom_anglais': 'Ghana', 'code_iso_3': 'GHA', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Ouest', 'lat': Decimal('7.9465'), 'lon': Decimal('-1.0232'), 'capitale': 'Accra', 'tel': '+233', 'devise': 'GHS', 'provinces': 2},
    'NG': {'nom': 'Nigeria', 'nom_anglais': 'Nigeria', 'code_iso_3': 'NGA', 'continent': 'Afrique', 'sous_region': 'Afrique de l\'Ouest', 'lat': Decimal('9.0820'), 'lon': Decimal('8.6753'), 'capitale': 'Abuja', 'tel': '+234', 'devise': 'NGN', 'provinces': 3},
    'MA': {'nom': 'Maroc', 'nom_anglais': 'Morocco', 'code_iso_3': 'MAR', 'continent': 'Afrique', 'sous_region': 'Afrique du Nord', 'lat': Decimal('31.7917'), 'lon': Decimal('-7.0926'), 'capitale': 'Rabat', 'tel': '+212', 'devise': 'MAD', 'provinces': 3},
    'DZ': {'nom': 'Algérie', 'nom_anglais': 'Algeria', 'code_iso_3': 'DZA', 'continent': 'Afrique', 'sous_region': 'Afrique du Nord', 'lat': Decimal('28.0339'), 'lon': Decimal('1.6596'), 'capitale': 'Alger', 'tel': '+213', 'devise': 'DZD', 'provinces': 2},
    'TN': {'nom': 'Tunisie', 'nom_anglais': 'Tunisia', 'code_iso_3': 'TUN', 'continent': 'Afrique', 'sous_region': 'Afrique du Nord', 'lat': Decimal('33.8869'), 'lon': Decimal('9.5375'), 'capitale': 'Tunis', 'tel': '+216', 'devise': 'TND', 'provinces': 1},
    'EG': {'nom': 'Égypte', 'nom_anglais': 'Egypt', 'code_iso_3': 'EGY', 'continent': 'Afrique', 'sous_region': 'Afrique du Nord', 'lat': Decimal('26.8206'), 'lon': Decimal('30.8025'), 'capitale': 'Le Caire', 'tel': '+20', 'devise': 'EGP', 'provinces': 2},
    'ZA': {'nom': 'Afrique du Sud', 'nom_anglais': 'South Africa', 'code_iso_3': 'ZAF', 'continent': 'Afrique', 'sous_region': 'Afrique Australe', 'lat': Decimal('-30.5595'), 'lon': Decimal('22.9375'), 'capitale': 'Pretoria', 'tel': '+27', 'devise': 'ZAR', 'provinces': 3},
}

print("\n1. Mise à jour des pays avec continent et sous_region...")
stats = {'mis_a_jour': 0, 'erreurs': 0}

for code_iso_2, data in PAYS_AFRICAINS.items():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE localisation.pays
                SET continent = %s, sous_region = %s
                WHERE code_iso_2 = %s
            """, [data['continent'], data['sous_region'], code_iso_2])
            
            if cursor.rowcount > 0:
                stats['mis_a_jour'] += 1
                print(f"   ✅ {data['nom']} ({code_iso_2}) - {data['sous_region']}")
            else:
                print(f"   ⚠️  {data['nom']} ({code_iso_2}) - Pays non trouvé")
    except Exception as e:
        stats['erreurs'] += 1
        print(f"   ❌ Erreur pour {code_iso_2}: {e}")

print(f"\n✅ Résumé: {stats['mis_a_jour']} pays mis à jour, {stats['erreurs']} erreurs")

# Statistiques
print("\n" + "="*80)
print("STATISTIQUES")
print("="*80)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT sous_region, COUNT(*) as nb_pays
        FROM localisation.pays
        WHERE continent = 'Afrique'
        GROUP BY sous_region
        ORDER BY sous_region
    """)
    
    print("\nPar sous-région:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} pays")

print("\n" + "="*80)
print("✅ PEUPLEMENT TERMINÉ!")
print("="*80)
