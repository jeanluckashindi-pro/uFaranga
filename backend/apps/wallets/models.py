from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Currency(models.Model):
    """Modèle pour les devises supportées"""
    
    code = models.CharField(max_length=3, unique=True, primary_key=True)  # USD, EUR, XOF, etc.
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    decimal_places = models.IntegerField(default=2)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'currencies'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Wallet(models.Model):
    """Modèle pour les portefeuilles utilisateur"""
    
    WALLET_TYPES = [
        ('PERSONAL', 'Personal Wallet'),
        ('BUSINESS', 'Business Wallet'),
        ('SAVINGS', 'Savings Wallet'),
        ('ESCROW', 'Escrow Wallet'),
    ]
    
    WALLET_STATUS = [
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('FROZEN', 'Frozen'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()  # Référence vers User Service
    
    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPES, default='PERSONAL')
    status = models.CharField(max_length=20, choices=WALLET_STATUS, default='ACTIVE')
    
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    balance = models.DecimalField(
        max_digits=19, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Limites
    daily_limit = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    monthly_limit = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    
    # Métadonnées
    name = models.CharField(max_length=100, blank=True)  # Nom personnalisé du wallet
    description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_transaction_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'wallets'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['currency']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Wallet {self.id} - {self.currency.code} ({self.balance})"
    
    @property
    def is_active(self):
        return self.status == 'ACTIVE'
    
    def can_debit(self, amount):
        """Vérifier si le wallet peut être débité"""
        return (
            self.is_active and 
            self.balance >= amount and 
            amount > 0
        )
    
    def can_credit(self, amount):
        """Vérifier si le wallet peut être crédité"""
        return self.is_active and amount > 0


class WalletTransaction(models.Model):
    """Historique des transactions de wallet (pour audit)"""
    
    TRANSACTION_TYPES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    balance_before = models.DecimalField(max_digits=19, decimal_places=2)
    balance_after = models.DecimalField(max_digits=19, decimal_places=2)
    
    # Référence vers la transaction principale
    external_transaction_id = models.UUIDField()
    reference = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wallet_transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wallet', '-created_at']),
            models.Index(fields=['external_transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} {self.amount} - {self.wallet.currency.code}"


class WalletLimit(models.Model):
    """Limites spécifiques par wallet et période"""
    
    LIMIT_TYPES = [
        ('DAILY', 'Daily Limit'),
        ('WEEKLY', 'Weekly Limit'),
        ('MONTHLY', 'Monthly Limit'),
        ('YEARLY', 'Yearly Limit'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='limits')
    limit_type = models.CharField(max_length=20, choices=LIMIT_TYPES)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    used_amount = models.DecimalField(max_digits=19, decimal_places=2, default=Decimal('0.00'))
    
    # Période de validité
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallet_limits'
        unique_together = ['wallet', 'limit_type', 'valid_from']
    
    def __str__(self):
        return f"{self.wallet} - {self.limit_type}: {self.amount}"
    
    @property
    def remaining_amount(self):
        return self.amount - self.used_amount
    
    @property
    def is_exceeded(self):
        return self.used_amount >= self.amount


class ExchangeRate(models.Model):
    """Taux de change entre devises"""
    
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_to')
    
    rate = models.DecimalField(max_digits=19, decimal_places=8)
    inverse_rate = models.DecimalField(max_digits=19, decimal_places=8)
    
    # Source du taux (API, manuel, etc.)
    source = models.CharField(max_length=50, default='manual')
    
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exchange_rates'
        unique_together = ['from_currency', 'to_currency', 'valid_from']
        indexes = [
            models.Index(fields=['from_currency', 'to_currency', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.from_currency.code}/{self.to_currency.code}: {self.rate}"
    
    def convert_amount(self, amount):
        """Convertir un montant avec ce taux"""
        return amount * self.rate
