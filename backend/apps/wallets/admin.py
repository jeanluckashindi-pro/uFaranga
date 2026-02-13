from django.contrib import admin
from .models import Wallet, WalletTransaction, Currency, ExchangeRate, WalletLimit


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'symbol', 'is_active', 'updated_at']
    search_fields = ['code', 'name']
    list_filter = ['is_active']


class WalletLimitInline(admin.TabularInline):
    model = WalletLimit
    extra = 0


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'currency', 'balance', 'wallet_type', 'status', 'created_at']
    search_fields = ['user_id', 'id']
    list_filter = ['status', 'wallet_type', 'currency']
    inlines = [WalletLimitInline]
    readonly_fields = ['balance', 'created_at', 'updated_at', 'last_transaction_at']


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'transaction_type', 'amount', 'created_at', 'reference']
    search_fields = ['wallet__user_id', 'reference', 'external_transaction_id']
    list_filter = ['transaction_type', 'created_at']
    readonly_fields = ['id', 'wallet', 'amount', 'balance_before', 'balance_after', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'rate', 'source', 'is_active', 'valid_from']
    list_filter = ['is_active', 'source']
