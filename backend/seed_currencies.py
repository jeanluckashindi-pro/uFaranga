
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.wallets.models import Currency

def seed_currencies():
    currencies = [
        {'code': 'BIF', 'name': 'Franc Burundais', 'symbol': 'FBu', 'decimal_places': 0},
        {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'decimal_places': 2},
        {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'decimal_places': 2},
        {'code': 'XOF', 'name': 'Franc CFA (BCEAO)', 'symbol': 'CFA', 'decimal_places': 0},
    ]

    for curr in currencies:
        obj, created = Currency.objects.get_or_create(
            code=curr['code'],
            defaults=curr
        )
        if created:
            print(f"Created currency: {obj}")
        else:
            print(f"Currency already exists: {obj}")

if __name__ == '__main__':
    seed_currencies()
