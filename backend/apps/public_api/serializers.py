"""
Serializers pour l'API publique
"""
from rest_framework import serializers


class FeesCalculatorSerializer(serializers.Serializer):
    """Serializer pour le calculateur de frais"""
    amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        required=True,
        help_text="Montant de la transaction"
    )
    type = serializers.ChoiceField(
        choices=[
            'P2P', 'DEPOT', 'RETRAIT', 'PAIEMENT_MARCHAND',
            'PAIEMENT_FACTURE', 'RECHARGE_TELEPHONIQUE',
            'VIREMENT_BANCAIRE', 'TRANSFERT_INTERNATIONAL'
        ],
        required=True,
        help_text="Type de transaction"
    )
    currency = serializers.CharField(
        max_length=3,
        default='BIF',
        help_text="Devise (BIF, USD, EUR, etc.)"
    )


class FeesResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse du calculateur"""
    montant = serializers.DecimalField(max_digits=18, decimal_places=2)
    devise = serializers.CharField(max_length=3)
    type_transaction = serializers.CharField()
    frais = serializers.DecimalField(max_digits=18, decimal_places=2)
    commission = serializers.DecimalField(max_digits=18, decimal_places=2)
    montant_total = serializers.DecimalField(max_digits=18, decimal_places=2)
    details = serializers.DictField()


class ValidatePhoneSerializer(serializers.Serializer):
    """Serializer pour validation de numéro de téléphone"""
    phone = serializers.CharField(
        max_length=20,
        required=True,
        help_text="Numéro de téléphone à valider (format international)"
    )


class ValidateAccountSerializer(serializers.Serializer):
    """Serializer pour validation de compte"""
    account = serializers.CharField(
        max_length=100,
        required=True,
        help_text="Numéro de compte, email ou téléphone"
    )


class AgentSearchSerializer(serializers.Serializer):
    """Serializer pour recherche d'agents"""
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=8,
        required=False,
        help_text="Latitude"
    )
    longitude = serializers.DecimalField(
        max_digits=11,
        decimal_places=8,
        required=False,
        help_text="Longitude"
    )
    radius = serializers.IntegerField(
        default=5000,
        help_text="Rayon de recherche en mètres (défaut: 5000m)"
    )
    city = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Ville"
    )
    name = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Nom de l'agent"
    )


class RegisterInitiateSerializer(serializers.Serializer):
    """Serializer pour initier une inscription"""
    phone = serializers.CharField(
        max_length=20,
        required=True,
        help_text="Numéro de téléphone (format international)"
    )
    email = serializers.EmailField(
        required=True,
        help_text="Adresse email"
    )
    first_name = serializers.CharField(
        max_length=100,
        required=True,
        help_text="Prénom"
    )
    last_name = serializers.CharField(
        max_length=100,
        required=True,
        help_text="Nom de famille"
    )


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer pour vérification OTP"""
    phone = serializers.CharField(
        max_length=20,
        required=True,
        help_text="Numéro de téléphone"
    )
    otp = serializers.CharField(
        max_length=6,
        required=True,
        help_text="Code OTP à 6 chiffres"
    )
