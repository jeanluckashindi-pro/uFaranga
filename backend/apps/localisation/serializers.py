"""
Sérialiseurs CRUD pour le schéma localisation.
Accepte UUID ou nom/code pour les champs de relation (pays, province, district, quartier).
"""
import uuid
from rest_framework import serializers
from .models import Pays, Province, District, Quartier, PointDeService


def is_valid_uuid(value):
    if value is None:
        return False
    if isinstance(value, uuid.UUID):
        return True
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, TypeError):
        return False


class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = [
            'id', 'code_iso_2', 'code_iso_3', 'nom', 'nom_anglais',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']


# --- Couverture mondiale : hiérarchie complète avec statistiques (actifs / inactifs) à chaque niveau ---


class PointDeServiceCouvertureSerializer(serializers.ModelSerializer):
    """Point de vente / point de service pour l'endpoint couverture."""
    class Meta:
        model = PointDeService
        fields = [
            'id', 'code', 'nom', 'type_point',
            'latitude', 'longitude',
            'autorise_systeme', 'est_actif',
        ]


class QuartierCouvertureSerializer(serializers.ModelSerializer):
    """Quartier avec points de service et statistiques (actifs / inactifs)."""
    points_de_service = PointDeServiceCouvertureSerializer(many=True, read_only=True)
    statistiques = serializers.SerializerMethodField()

    class Meta:
        model = Quartier
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'statistiques',
            'points_de_service',
        ]

    def get_statistiques(self, obj):
        points = list(obj.points_de_service.all())
        actifs = sum(1 for p in points if p.est_actif)
        return {
            'nb_points_de_service': len(points),
            'nb_points_actifs': actifs,
            'nb_points_inactifs': len(points) - actifs,
        }


class DistrictCouvertureSerializer(serializers.ModelSerializer):
    """District avec quartiers et statistiques (actifs / inactifs)."""
    quartiers = QuartierCouvertureSerializer(many=True, read_only=True)
    statistiques = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'statistiques',
            'quartiers',
        ]

    def get_statistiques(self, obj):
        quartiers = list(obj.quartiers.all())
        actifs = sum(1 for q in quartiers if q.est_actif)
        points = sum(len(list(q.points_de_service.all())) for q in quartiers)
        return {
            'nb_quartiers': len(quartiers),
            'nb_quartiers_actifs': actifs,
            'nb_quartiers_inactifs': len(quartiers) - actifs,
            'nb_points_de_service': points,
        }


class ProvinceCouvertureSerializer(serializers.ModelSerializer):
    """Province avec districts et statistiques (actifs / inactifs)."""
    districts = DistrictCouvertureSerializer(many=True, read_only=True)
    statistiques = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'statistiques',
            'districts',
        ]

    def get_statistiques(self, obj):
        districts = list(obj.districts.all())
        actifs = sum(1 for d in districts if d.est_actif)
        quartiers = sum(len(list(d.quartiers.all())) for d in districts)
        points = 0
        for d in districts:
            for q in d.quartiers.all():
                points += len(list(q.points_de_service.all()))
        return {
            'nb_districts': len(districts),
            'nb_districts_actifs': actifs,
            'nb_districts_inactifs': len(districts) - actifs,
            'nb_quartiers': quartiers,
            'nb_points_de_service': points,
        }


def _pays_couverture_statistiques(obj):
    """Calcule les stats pays à partir des provinces préchargées."""
    provinces = list(obj.provinces.all())
    actifs = sum(1 for p in provinces if p.est_actif)
    nb_districts = 0
    nb_quartiers = 0
    nb_points = 0
    for p in provinces:
        for d in p.districts.all():
            nb_districts += 1
            qs = list(d.quartiers.all())
            nb_quartiers += len(qs)
            for q in qs:
                nb_points += len(list(q.points_de_service.all()))
    return {
        'nb_provinces': len(provinces),
        'nb_provinces_actives': actifs,
        'nb_provinces_inactives': len(provinces) - actifs,
        'nb_districts': nb_districts,
        'nb_quartiers': nb_quartiers,
        'nb_points_de_service': nb_points,
    }


class CouverturePaysSerializer(serializers.ModelSerializer):
    """Pays couvert : coordonnées, statistiques (actifs/inactifs) et hiérarchie complète provinces → districts → quartiers → points de vente."""
    provinces = ProvinceCouvertureSerializer(many=True, read_only=True)
    statistiques = serializers.SerializerMethodField()

    class Meta:
        model = Pays
        fields = [
            'id', 'code_iso_2', 'code_iso_3', 'nom', 'nom_anglais',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'statistiques',
            'provinces',
        ]

    def get_statistiques(self, obj):
        return _pays_couverture_statistiques(obj)


# --- Sérialiseurs imbriqués pour le détail Pays (expand provinces → districts → quartiers → points_de_service) ---

class PointDeServiceExpandSerializer(serializers.ModelSerializer):
    """Minimal pour imbrication dans quartier."""
    class Meta:
        model = PointDeService
        fields = [
            'id', 'code', 'nom', 'type_point',
            'latitude', 'longitude', 'autorise_systeme', 'est_actif',
        ]


class QuartierExpandSerializer(serializers.ModelSerializer):
    """Quartier avec points de service imbriqués."""
    points_de_service = PointDeServiceExpandSerializer(many=True, read_only=True)

    class Meta:
        model = Quartier
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'points_de_service',
        ]


class DistrictExpandSerializer(serializers.ModelSerializer):
    """District avec quartiers (et leurs points de service) imbriqués."""
    quartiers = QuartierExpandSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'quartiers',
        ]


class ProvinceExpandSerializer(serializers.ModelSerializer):
    """Province avec districts (→ quartiers → points de service) imbriqués."""
    districts = DistrictExpandSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = [
            'id', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'districts',
        ]


class PaysDetailSerializer(serializers.ModelSerializer):
    """Détail pays avec expand : provinces → districts → quartiers → points_de_service."""
    provinces = ProvinceExpandSerializer(many=True, read_only=True)

    class Meta:
        model = Pays
        fields = [
            'id', 'code_iso_2', 'code_iso_3', 'nom', 'nom_anglais',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
            'provinces',
        ]
        read_only_fields = fields


class ProvinceSerializer(serializers.ModelSerializer):
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    pays_code = serializers.CharField(source='pays.code_iso_2', read_only=True)
    pays = serializers.PrimaryKeyRelatedField(queryset=Pays.objects.all(), required=True)

    class Meta:
        model = Province
        fields = [
            'id', 'pays', 'pays_nom', 'pays_code', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def to_internal_value(self, data):
        if isinstance(data.get('pays'), str) and not is_valid_uuid(data['pays']):
            val = data['pays'].strip()
            pays = Pays.objects.filter(nom__iexact=val).first() or Pays.objects.filter(code_iso_2__iexact=val).first()
            if pays:
                data = {**data, 'pays': str(pays.id)}
        return super().to_internal_value(data)


class DistrictSerializer(serializers.ModelSerializer):
    province_nom = serializers.CharField(source='province.nom', read_only=True)
    pays_nom = serializers.CharField(source='province.pays.nom', read_only=True)
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), required=True)

    class Meta:
        model = District
        fields = [
            'id', 'province', 'province_nom', 'pays_nom', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def to_internal_value(self, data):
        if isinstance(data.get('province'), str) and not is_valid_uuid(data['province']):
            val = data['province'].strip()
            province = Province.objects.filter(nom__iexact=val).first() or Province.objects.filter(code__iexact=val).first()
            if province:
                data = {**data, 'province': str(province.id)}
        return super().to_internal_value(data)


class QuartierSerializer(serializers.ModelSerializer):
    district_nom = serializers.CharField(source='district.nom', read_only=True)
    province_nom = serializers.CharField(source='district.province.nom', read_only=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=True)

    class Meta:
        model = Quartier
        fields = [
            'id', 'district', 'district_nom', 'province_nom', 'code', 'nom',
            'latitude_centre', 'longitude_centre',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def to_internal_value(self, data):
        if isinstance(data.get('district'), str) and not is_valid_uuid(data['district']):
            val = data['district'].strip()
            district = District.objects.filter(nom__iexact=val).first() or District.objects.filter(code__iexact=val).first()
            if district:
                data = {**data, 'district': str(district.id)}
        return super().to_internal_value(data)


class PointDeServiceSerializer(serializers.ModelSerializer):
    quartier_nom = serializers.CharField(source='quartier.nom', read_only=True)
    district_nom = serializers.CharField(source='quartier.district.nom', read_only=True)
    quartier = serializers.PrimaryKeyRelatedField(queryset=Quartier.objects.all(), required=True)

    class Meta:
        model = PointDeService
        fields = [
            'id', 'quartier', 'quartier_nom', 'district_nom', 'code', 'nom',
            'type_point', 'agent_utilisateur',
            'latitude', 'longitude', 'adresse_complementaire',
            'autorise_systeme', 'est_actif',
            'date_creation', 'date_modification', 'metadonnees',
        ]
        read_only_fields = ['id', 'date_creation', 'date_modification']

    def to_internal_value(self, data):
        if isinstance(data.get('quartier'), str) and not is_valid_uuid(data['quartier']):
            val = data['quartier'].strip()
            quartier = Quartier.objects.filter(nom__iexact=val).first() or Quartier.objects.filter(code__iexact=val).first()
            if quartier:
                data = {**data, 'quartier': str(quartier.id)}
        return super().to_internal_value(data)
