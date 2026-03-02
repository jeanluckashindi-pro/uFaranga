#!/usr/bin/env python
"""
Script pour créer la structure administrative complète de la RDC
basée sur les données GADM et la structure officielle congolaise.

Structure RDC:
- Pays
- Provinces (26)
- Territoires/Villes (correspondant aux districts GADM niveau 2)
- Secteurs/Chefferies (à créer manuellement ou depuis d'autres sources)
- Groupements
- Villages/Localités
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Commune, Secteur


def creer_structure_rdc_base():
    """
    Crée une structure de base pour la RDC avec des secteurs/territoires types.
    Les districts GADM correspondent aux Territoires congolais.
    """
    print("=== Création de la structure administrative RDC ===\n")
    
    # Récupérer le pays RDC
    rdc = Pays.objects.filter(code_iso_3='COD').first()
    if not rdc:
        print("❌ Pays RDC non trouvé. Importez d'abord les données GADM.")
        return
    
    print(f"✓ Pays: {rdc.nom}")
    
    # Compter les provinces et districts
    provinces = Province.objects.filter(pays=rdc)
    districts = District.objects.filter(province__pays=rdc)
    
    print(f"✓ Provinces: {provinces.count()}")
    print(f"✓ Territoires/Villes (Districts): {districts.count()}")
    
    # Pour chaque district (territoire), créer des communes de base
    print("\n=== Création des communes pour les territoires ===")
    
    communes_creees = 0
    for district in districts:
        # Vérifier si des communes existent déjà
        if district.communes.exists():
            continue
        
        # Créer une commune chef-lieu par défaut
        commune_nom = f"{district.nom} Centre"
        
        # Pour les villes, créer plusieurs communes
        if "(ville)" in district.nom.lower() or district.nom in ['Kinshasa', 'Lubumbashi', 'Goma', 'Bukavu', 'Kisangani']:
            # Créer 3 communes de base pour les grandes villes
            for i, suffix in enumerate(['Centre', 'Nord', 'Sud'], 1):
                Commune.objects.get_or_create(
                    district=district,
                    code=f"{district.code}_{i}",
                    defaults={
                        'nom': f"{district.nom.replace('(ville)', '').strip()} {suffix}",
                        'centre_latitude': 0,
                        'centre_longitude': 0,
                        'zone_urbaine': True,
                        'est_actif': True,
                    }
                )
                communes_creees += 1
        else:
            # Pour les territoires ruraux, créer une commune chef-lieu
            Commune.objects.get_or_create(
                district=district,
                code=f"{district.code}_1",
                defaults={
                    'nom': commune_nom,
                    'centre_latitude': 0,
                    'centre_longitude': 0,
                    'zone_urbaine': False,
                    'est_actif': True,
                }
            )
            communes_creees += 1
    
    print(f"✓ {communes_creees} communes créées")
    
    # Créer des secteurs de base pour quelques communes
    print("\n=== Création de secteurs de base ===")
    
    secteurs_crees = 0
    communes = Commune.objects.filter(district__province__pays=rdc)[:50]  # Limiter aux 50 premières
    
    for commune in communes:
        # Créer 2-3 secteurs par commune
        nb_secteurs = 3 if commune.zone_urbaine else 2
        
        for i in range(1, nb_secteurs + 1):
            secteur_nom = f"Secteur {i}" if commune.zone_urbaine else f"Canton {i}"
            
            Secteur.objects.get_or_create(
                commune=commune,
                code=f"{commune.code}_S{i}",
                defaults={
                    'nom': f"{commune.nom} - {secteur_nom}",
                    'type_secteur': 'ARRONDISSEMENT' if commune.zone_urbaine else 'CANTON',
                    'centre_latitude': 0,
                    'centre_longitude': 0,
                    'est_actif': True,
                }
            )
            secteurs_crees += 1
    
    print(f"✓ {secteurs_crees} secteurs/chefferies créés")
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DE LA STRUCTURE RDC")
    print("="*60)
    print(f"Pays:                    1")
    print(f"Provinces:               {provinces.count()}")
    print(f"Territoires/Villes:      {districts.count()}")
    print(f"Communes:                {Commune.objects.filter(district__province__pays=rdc).count()}")
    print(f"Secteurs/Chefferies:     {Secteur.objects.filter(commune__district__province__pays=rdc).count()}")
    print("="*60)
    
    print("\n✅ Structure de base créée avec succès!")
    print("\nℹ️  Note: Cette structure est une base. Vous pouvez:")
    print("   - Ajouter plus de communes pour chaque territoire")
    print("   - Créer des secteurs/chefferies spécifiques")
    print("   - Importer des données plus détaillées depuis d'autres sources")


def afficher_statistiques_rdc():
    """Affiche les statistiques de la structure RDC"""
    rdc = Pays.objects.filter(code_iso_3='COD').first()
    if not rdc:
        print("❌ Pays RDC non trouvé")
        return
    
    print("\n" + "="*60)
    print("STATISTIQUES RDC")
    print("="*60)
    
    provinces = Province.objects.filter(pays=rdc)
    print(f"\nProvinces ({provinces.count()}):")
    for prov in provinces.order_by('nom'):
        territoires = District.objects.filter(province=prov).count()
        communes = Commune.objects.filter(district__province=prov).count()
        print(f"  • {prov.nom:30} - {territoires:3} territoires, {communes:4} communes")
    
    print("="*60)


def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Créer la structure administrative RDC')
    parser.add_argument('--creer', action='store_true', help='Créer la structure de base')
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    args = parser.parse_args()
    
    if args.creer:
        creer_structure_rdc_base()
    
    if args.stats:
        afficher_statistiques_rdc()
    
    if not args.creer and not args.stats:
        print("Usage:")
        print("  python scripts/import_rdc_structure.py --creer    # Créer la structure")
        print("  python scripts/import_rdc_structure.py --stats    # Voir les stats")


if __name__ == '__main__':
    main()
