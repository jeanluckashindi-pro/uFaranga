"""
Script pour générer un rapport détaillé de la couverture géographique
"""
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.localisation.models import Pays, Province, District, Quartier
from django.db import connection
from django.db.models import Count


def generer_rapport():
    rapport = []
    rapport.append("# Rapport de Couverture Geographique")
    rapport.append(f"\nDate: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # Statistiques globales
    rapport.append("## Statistiques Globales\n")
    rapport.append(f"- Pays: {Pays.objects.count()}")
    rapport.append(f"- Provinces: {Province.objects.count()}")
    rapport.append(f"- Districts: {District.objects.count()}")
    rapport.append(f"- Quartiers: {Quartier.objects.count()}\n")
    
    # Détail par pays
    rapport.append("## Detail par Pays\n")
    rapport.append("| Pays | Code | Provinces | Districts | Quartiers | Statut |")
    rapport.append("|------|------|-----------|-----------|-----------|--------|")
    
    pays_list = Pays.objects.all().annotate(
        nb_provinces=Count('provinces'),
        nb_districts=Count('provinces__districts'),
        nb_quartiers=Count('provinces__districts__quartiers')
    ).order_by('nom')
    
    for pays in pays_list:
        statut = "OK" if pays.nb_provinces > 0 else "INCOMPLET"
        rapport.append(
            f"| {pays.nom} | {pays.code_iso_2} | {pays.nb_provinces} | "
            f"{pays.nb_districts} | {pays.nb_quartiers} | {statut} |"
        )
    
    return "\n".join(rapport)


if __name__ == '__main__':
    print("Generation du rapport...")
    rapport = generer_rapport()
    
    filename = f"RAPPORT_GEO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(rapport)
    
    print(f"Rapport genere: {filename}")
    print("\n" + rapport)
