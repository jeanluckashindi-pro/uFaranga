from rest_framework import serializers
from decimal import Decimal
from .models import Wallet, Currency, WalletTransaction, WalletLimit, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol', 'decimal_places', 'is_active']


class WalletSerializer(serializers.ModelSerializer):
    currency_details = CurrencySerializer(source='currency', read_only=True)
    balance_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = [
            'id', 'user_id', 'wallet_type', 'status', 'currency', 'currency_details',
            'balance', 'balance_formatted', 'daily_limit', 'monthly_limit',
            'name', 'description', 'created_at', 'updated_at', 'last_transaction_at'
        ]
        read_only_fields = ['id', 'balance', 'created_at', 'updated_at', 'last_transaction_at']
    
    def get_balance_formatted(self, obj):
        return f"{obj.currency.symbol}{obj.balance}"


class WalletCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user_id', 'wallet_type', 'currency', 'name', 'description']
    
    def validate_currency(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Cette devise n'est pas active.")
        return value


class WalletTransactionSerializer(serializers.ModelSerializer):
    wallet_details = WalletSerializer(source='wallet', read_only=True)
    amount_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = WalletTransaction
        fields = [
            'id', 'wallet', 'wallet_details', 'transaction_type', 'amount', 'amount_formatted',
            'balance_before', 'balance_after', 'external_transaction_id', 
            'reference', 'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_amount_formatted(self, obj):
        symbol = obj.wallet.currency.symbol
        sign = '+' if obj.transaction_type == 'CREDIT' else '-'
        return f"{sign}{symbol}{obj.amount}"


class BalanceUpdateSerializer(serializers.Serializer):
    """Serializer pour les mises à jour de solde"""
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    operation = serializers.ChoiceField(choices=['CREDIT', 'DEBIT'])
    reference = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    external_transaction_id = serializers.UUIDField()
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être positif.")
        return value


class TransferSerializer(serializers.Serializer):
    """Serializer pour les transferts entre wallets"""
    from_wallet_id = serializers.UUIDField()
    to_wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    reference = serializers.CharField(max_length=100, required=False)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être positif.")
        return value
    
    def validate(self, data):
        if data['from_wallet_id'] == data['to_wallet_id']:
            raise serializers.ValidationError("Les wallets source et destination doivent être différents.")
        return data


class WalletLimitSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.ReadOnlyField()
    is_exceeded = serializers.ReadOnlyField()
    
    class Meta:
        model = WalletLimit
        fields = [
            'id', 'wallet', 'limit_type', 'amount', 'used_amount', 'remaining_amount',
            'is_exceeded', 'valid_from', 'valid_until', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'used_amount', 'created_at']


class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency_details = CurrencySerializer(source='from_currency', read_only=True)
    to_currency_details = CurrencySerializer(source='to_currency', read_only=True)
    
    class Meta:
        model = ExchangeRate
        fields = [
            'id', 'from_currency', 'from_currency_details', 'to_currency', 'to_currency_details',
            'rate', 'inverse_rate', 'source', 'valid_from', 'valid_until', 
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'inverse_rate', 'created_at']
    
    def validate(self, data):
        if data['from_currency'] == data['to_currency']:
            raise serializers.ValidationError("Les devises source et destination doivent être différentes.")
        return data
    
    def create(self, validated_data):
        # Calculer automatiquement le taux inverse
        validated_data['inverse_rate'] = 1 / validated_data['rate']
        return super().create(validated_data)


class CurrencyConversionSerializer(serializers.Serializer):
    """Serializer pour la conversion de devises"""
    from_currency = serializers.CharField(max_length=3)
    to_currency = serializers.CharField(max_length=3)
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être positif.")
        return value
