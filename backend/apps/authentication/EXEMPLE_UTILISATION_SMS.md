# Exemple d'Utilisation - Service SMS de Confirmation

## Scénario : Vérification de Téléphone lors de l'Inscription

### Étape 1 : L'utilisateur saisit son numéro de téléphone

```javascript
// Frontend - Demande d'envoi du code
const response = await fetch('/api/v1/authentification/envoyer-code-confirmation/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    telephone: '62046725',
    prenom: 'Jean-luc'
  })
});

const data = await response.json();
console.log(data);
// {
//   "success": true,
//   "message": "Code de confirmation envoyé avec succès",
//   "code_formate": "UF-CCF-PSW-12345",
//   "telephone": "62046725"
// }
```

### Étape 2 : L'utilisateur reçoit le SMS

```
Message SMS reçu :
"Bonjour Jean-luc, votre code de confirmation est: UF-CCF-PSW-12345"
```

### Étape 3 : L'utilisateur saisit le code

```javascript
// Frontend - Vérification du code
const verifyResponse = await fetch('/api/v1/authentification/verifier-code-confirmation/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    telephone: '62046725',
    code: '12345'  // Seulement les 5 chiffres, sans le préfixe
  })
});

const verifyData = await verifyResponse.json();
console.log(verifyData);
// {
//   "success": true,
//   "message": "Code de confirmation valide",
//   "telephone": "62046725"
// }
```

## Scénario : Réinitialisation de Mot de Passe

### Flux complet

```python
# Backend - Service de réinitialisation de mot de passe

from apps.authentication.services_sms import envoyer_code_confirmation, verifier_code_confirmation
from apps.identite.models import Utilisateur as UtilisateurIdentite

def demander_reinitialisation_mdp(telephone):
    """Étape 1 : Envoyer le code de vérification"""
    
    # Vérifier que l'utilisateur existe
    utilisateur = UtilisateurIdentite.objects.filter(
        numero_telephone=telephone
    ).first()
    
    if not utilisateur:
        return {'success': False, 'message': 'Utilisateur introuvable'}
    
    # Envoyer le code
    resultat = envoyer_code_confirmation(
        telephone=telephone,
        prenom=utilisateur.prenom
    )
    
    return resultat


def confirmer_reinitialisation_mdp(telephone, code, nouveau_mdp):
    """Étape 2 : Vérifier le code et changer le mot de passe"""
    
    # Vérifier le code
    if not verifier_code_confirmation(telephone, code):
        return {'success': False, 'message': 'Code invalide ou expiré'}
    
    # Changer le mot de passe
    utilisateur = UtilisateurIdentite.objects.filter(
        numero_telephone=telephone
    ).first()
    
    if not utilisateur:
        return {'success': False, 'message': 'Utilisateur introuvable'}
    
    utilisateur.set_password(nouveau_mdp)
    utilisateur.save()
    
    return {'success': True, 'message': 'Mot de passe réinitialisé avec succès'}
```

## Scénario : Vérification 2FA (Double Authentification)

```python
# Backend - Vérification 2FA lors de la connexion

from apps.authentication.services_sms import envoyer_code_confirmation, verifier_code_confirmation

def activer_2fa_pour_connexion(utilisateur):
    """Envoyer un code 2FA lors de la connexion"""
    
    resultat = envoyer_code_confirmation(
        telephone=utilisateur.numero_telephone,
        prenom=utilisateur.prenom
    )
    
    if resultat['success']:
        # Stocker temporairement que l'utilisateur attend la 2FA
        cache.set(
            f'2fa_pending:{utilisateur.id}',
            True,
            timeout=300  # 5 minutes
        )
    
    return resultat


def verifier_2fa_connexion(utilisateur, code):
    """Vérifier le code 2FA"""
    
    # Vérifier que la 2FA est en attente
    if not cache.get(f'2fa_pending:{utilisateur.id}'):
        return False
    
    # Vérifier le code
    if verifier_code_confirmation(utilisateur.numero_telephone, code):
        # Supprimer le flag 2FA en attente
        cache.delete(f'2fa_pending:{utilisateur.id}')
        return True
    
    return False
```

## Gestion des Erreurs

### Erreur : Numéro de téléphone invalide

```json
{
  "telephone": [
    "Format de numéro invalide. Utilisez 8 à 15 chiffres, avec ou sans le préfixe +"
  ]
}
```

### Erreur : Code expiré

```json
{
  "success": false,
  "message": "Code de confirmation invalide ou expiré"
}
```

### Erreur : Service SMS indisponible

```json
{
  "success": false,
  "message": "Erreur réseau: Connection timeout",
  "error": "..."
}
```

## Bonnes Pratiques

### 1. Limiter les Tentatives

```python
from django.core.cache import cache

def envoyer_code_avec_limite(telephone):
    """Limiter à 3 envois par heure"""
    
    cache_key = f'sms_attempts:{telephone}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 3:
        return {
            'success': False,
            'message': 'Trop de tentatives. Réessayez dans 1 heure.'
        }
    
    # Envoyer le code
    resultat = envoyer_code_confirmation(telephone)
    
    if resultat['success']:
        # Incrémenter le compteur
        cache.set(cache_key, attempts + 1, timeout=3600)  # 1 heure
    
    return resultat
```

### 2. Vérifier les Tentatives de Validation

```python
def verifier_code_avec_limite(telephone, code):
    """Limiter à 5 tentatives de vérification"""
    
    cache_key = f'verify_attempts:{telephone}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 5:
        # Supprimer le code pour forcer un nouvel envoi
        cache.delete(f'sms_confirmation:{telephone}')
        return False
    
    # Vérifier le code
    if verifier_code_confirmation(telephone, code):
        # Réinitialiser le compteur
        cache.delete(cache_key)
        return True
    
    # Incrémenter le compteur d'échecs
    cache.set(cache_key, attempts + 1, timeout=300)  # 5 minutes
    return False
```

### 3. Logger les Événements de Sécurité

```python
import logging

logger = logging.getLogger('security')

def envoyer_code_avec_audit(telephone, user_ip=None):
    """Envoyer un code avec audit de sécurité"""
    
    logger.info(
        f"Demande d'envoi de code SMS",
        extra={
            'telephone': telephone,
            'ip': user_ip,
            'timestamp': timezone.now()
        }
    )
    
    resultat = envoyer_code_confirmation(telephone)
    
    if resultat['success']:
        logger.info(f"Code SMS envoyé avec succès à {telephone}")
    else:
        logger.error(f"Échec d'envoi SMS à {telephone}: {resultat['message']}")
    
    return resultat
```

## Tests Unitaires

```python
from django.test import TestCase
from django.core.cache import cache
from apps.authentication.services_sms import (
    generer_code_confirmation,
    formater_code_sms,
    stocker_code_confirmation,
    verifier_code_confirmation
)

class SMSConfirmationTestCase(TestCase):
    
    def setUp(self):
        cache.clear()
    
    def test_generer_code_5_chiffres(self):
        """Le code doit contenir exactement 5 chiffres"""
        code = generer_code_confirmation()
        self.assertEqual(len(code), 5)
        self.assertTrue(code.isdigit())
    
    def test_formater_code(self):
        """Le code doit être formaté avec le préfixe UF-CCF-PSW-"""
        code = "12345"
        code_formate = formater_code_sms(code)
        self.assertEqual(code_formate, "UF-CCF-PSW-12345")
    
    def test_stocker_et_verifier_code(self):
        """Le code stocké doit être vérifiable"""
        telephone = "62046725"
        code = "12345"
        
        # Stocker
        self.assertTrue(stocker_code_confirmation(telephone, code))
        
        # Vérifier
        self.assertTrue(verifier_code_confirmation(telephone, code))
    
    def test_code_invalide(self):
        """Un code incorrect doit être rejeté"""
        telephone = "62046725"
        stocker_code_confirmation(telephone, "12345")
        
        self.assertFalse(verifier_code_confirmation(telephone, "99999"))
    
    def test_code_supprime_apres_verification(self):
        """Le code doit être supprimé après vérification réussie"""
        telephone = "62046725"
        code = "12345"
        
        stocker_code_confirmation(telephone, code)
        self.assertTrue(verifier_code_confirmation(telephone, code))
        
        # Deuxième tentative doit échouer
        self.assertFalse(verifier_code_confirmation(telephone, code))
```
