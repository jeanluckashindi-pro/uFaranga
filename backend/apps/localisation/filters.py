"""
Filtres pour les ViewSets du schéma localisation.
"""
import django_filters
from .models import Pays


class PaysFilterSet(django_filters.FilterSet):
    """Filtres pour la liste des pays."""

    code_iso_2 = django_filters.CharFilter(lookup_expr='iexact', label='Code ISO 2 (exact)')
    code_iso_3 = django_filters.CharFilter(lookup_expr='iexact', label='Code ISO 3 (exact)')
    nom = django_filters.CharFilter(lookup_expr='icontains', label='Nom (contient)')
    nom_anglais = django_filters.CharFilter(lookup_expr='icontains', label='Nom anglais (contient)')
    est_actif = django_filters.BooleanFilter(label='Actif')
    autorise_systeme = django_filters.BooleanFilter(label='Autorisé dans le système')

    class Meta:
        model = Pays
        fields = ['code_iso_2', 'code_iso_3', 'nom', 'nom_anglais', 'est_actif', 'autorise_systeme']
