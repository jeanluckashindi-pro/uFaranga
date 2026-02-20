#!/usr/bin/env python
"""
Script rapide pour créer un compte développeur de test
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.developpeurs.models import CompteDeveloppeur, CleAPI
from datetime import datetime, timedelta

print("\n" + "="*70)
print("🚀 CRÉATION RAPIDE D'UN COMPTE DÉVELOPPEUR DE TEST")
print("="*70 + "\n")

# Créer le compte
compte = CompteDeveloppeur.objects.create(
    nom_entreprise="Test Company",
    nom_contact="Test User",
    courriel_contact="test@example.com",
    type_compte="SANDBOX",
    statut="ACTIF",
    courriel_verifie=True,
    quota_requetes_jour=1000,
    quota_requetes_mois=30000,
    limite_taux_par_minute=60
)

print(f"✅ Compte créé: {compte.nom_entreprise}")

# Générer une clé API
cle_complete, prefixe = CleAPI.generer_cle('SANDBOX')
cle_hash = CleAPI.hasher_cle(cle_complete)

cle_api = CleAPI.objects.create(
    compte_developpeur=compte,
    cle_api=cle_complete[:64],
    prefixe_cle=prefixe,
    hash_cle=cle_hash,
    nom_cle="Clé de test",
    environnement="SANDBOX",
    scopes=["public:read", "fees:read", "agents:read", "validation:write"],
    est_active=True,
    date_expiration=datetime.now() + timedelta(days=365)
)

print(f"✅ Clé API créée!\n")
print("="*70)
print("🔑 VOTRE CLÉ API:")
print("="*70)
print(f"\n{cle_complete}\n")
print("="*70)
print("\n💡 Testez maintenant:")
print(f'\ncurl "http://127.0.0.1:8000/api/public/health/" \\')
print(f'  -H "Authorization: ApiKey {cle_complete}"')
print("\nOu ouvrez: http://127.0.0.1:8000/api/public/docs/\n")
