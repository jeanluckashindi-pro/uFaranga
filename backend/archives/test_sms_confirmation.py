#!/usr/bin/env python
"""
Script de test pour le service SMS de confirmation - Version 2.
Usage: python test_sms_confirmation.py
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.authentication.services_sms import (
    generer_code_confirmation,
    formater_code_sms,
    stocker_code_confirmation,
    verifier_code_confirmation,
    envoyer_code_confirmation,
    compter_changements_mdp
)
from apps.authentication.models import CodeConfirmationSMS, HistoriqueMotDePasse

def test_generation_code():
    """Test de génération de code"""
    print("\n=== Test 1: Génération de code ===")
    code = generer_code_confirmation()
    print(f"✓ Code généré: {code}")
    print(f"✓ Longueur: {len(code)} chiffres")
    print(f"✓ Est numérique: {code.isdigit()}")
    assert len(code) == 5, "Le code doit contenir 5 chiffres"
    assert code.isdigit(), "Le code doit être numérique"
    print("✓ Test réussi!")

def test_formatage_code():
    """Test de formatage du code"""
    print("\n=== Test 2: Formatage du code ===")
    code = "12345"
    code_formate = formater_code_sms(code)
    print(f"✓ Code original: {code}")
    print(f"✓ Code formaté: {code_formate}")
    assert code_formate == "UF-CCF-PSW-12345", "Le format doit être UF-CCF-PSW-XXXXX"
    print("✓ Test réussi!")

def test_stockage_verification():
    """Test de stockage et vérification"""
    print("\n=== Test 3: Stockage et vérification ===")
    telephone = "62046725"
    code = "12345"
    
    # Stocker
    print(f"→ Stockage du code {code} pour {telephone}")
    resultat = stocker_code_confirmation(telephone, code, duree_minutes=5)
    print(f"✓ Stockage: {'Réussi' if resultat else 'Échoué'}")
    assert resultat, "Le stockage doit réussir"
    
    # Vérifier avec le bon code
    print(f"→ Vérification avec le bon code")
    valide = verifier_code_confirmation(telephone, code)
    print(f"✓ Vérification: {'Valide' if valide else 'Invalide'}")
    assert valide, "Le code doit être valide"
    
    # Vérifier à nouveau (doit échouer car le code est supprimé)
    print(f"→ Vérification à nouveau (doit échouer)")
    valide = verifier_code_confirmation(telephone, code)
    print(f"✓ Deuxième vérification: {'Valide' if valide else 'Invalide (attendu)'}")
    assert not valide, "Le code ne doit plus être valide après utilisation"
    
    print("✓ Test réussi!")

def test_code_invalide():
    """Test avec un code invalide"""
    print("\n=== Test 4: Code invalide ===")
    telephone = "62046725"
    code_correct = "12345"
    code_incorrect = "99999"
    
    # Stocker le bon code
    stocker_code_confirmation(telephone, code_correct)
    
    # Vérifier avec un mauvais code
    print(f"→ Vérification avec un code incorrect")
    valide = verifier_code_confirmation(telephone, code_incorrect)
    print(f"✓ Résultat: {'Valide' if valide else 'Invalide (attendu)'}")
    assert not valide, "Le code incorrect doit être rejeté"
    
    # Le bon code doit toujours être valide
    print(f"→ Vérification avec le bon code")
    valide = verifier_code_confirmation(telephone, code_correct)
    print(f"✓ Résultat: {'Valide (attendu)' if valide else 'Invalide'}")
    assert valide, "Le bon code doit toujours être valide"
    
    print("✓ Test réussi!")

def test_envoi_sms_simulation():
    """Test d'envoi SMS (simulation)"""
    print("\n=== Test 5: Envoi SMS (simulation) ===")
    print("⚠ Ce test va tenter d'envoyer un vrai SMS!")
    print("⚠ Assurez-vous que le service SMS est configuré et accessible.")
    
    reponse = input("\nVoulez-vous continuer? (o/n): ")
    if reponse.lower() != 'o':
        print("✓ Test ignoré")
        return
    
    telephone = input("Entrez le numéro de téléphone: ")
    prenom = input("Entrez le prénom (optionnel): ") or None
    
    print(f"\n→ Envoi du code à {telephone}")
    resultat = envoyer_code_confirmation(telephone, prenom)
    
    if resultat['success']:
        print(f"✓ SMS envoyé avec succès!")
        print(f"✓ Code formaté: {resultat['code_formate']}")
        print(f"✓ Code brut (pour test): {resultat['code']}")
        
        # Test de vérification
        code_saisi = input("\nEntrez le code reçu par SMS (5 chiffres): ")
        if verifier_code_confirmation(telephone, code_saisi):
            print("✓ Code vérifié avec succès!")
        else:
            print("✗ Code invalide ou expiré")
    else:
        print(f"✗ Erreur: {resultat['message']}")
        if 'error' in resultat:
            print(f"  Détails: {resultat['error']}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("TEST DU SERVICE SMS DE CONFIRMATION")
    print("=" * 60)
    
    try:
        # Tests automatiques
        test_generation_code()
        test_formatage_code()
        test_stockage_verification()
        test_code_invalide()
        
        # Test manuel (optionnel)
        test_envoi_sms_simulation()
        
        print("\n" + "=" * 60)
        print("✓ TOUS LES TESTS SONT RÉUSSIS!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ ÉCHEC DU TEST: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERREUR INATTENDUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
