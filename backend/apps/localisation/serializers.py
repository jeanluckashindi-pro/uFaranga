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
