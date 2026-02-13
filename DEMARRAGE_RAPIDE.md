# 🚀 Démarrage Rapide - API Publique uFaranga

## En 3 Étapes Simples

### Étape 1: Créer le Schéma PostgreSQL ⚡

```bash
# Ouvrir PostgreSQL
psql -U ufaranga -d ufaranga

# Exécuter le script
\i database_setup/11_schema_developpeurs.sql

# Quitter
\q
```

### Étape 2: Créer un Compte Développeur 👤

```bash
cd backend
python create_developer_account.py
```

Le script vous guidera interactivement:
```
🚀 CRÉATION D'UN COMPTE DÉVELOPPEUR - uFaranga API

Nom de l'entreprise: Ma Startup
Nom du contact: Dupont
Prénom du contact: Jean
Email du contact: jean@startup.com
Téléphone: +25779123456
Ville: Bujumbura

Type de compte:
  1. SANDBOX (Test - Gratuit)
  2. PRODUCTION (Production)
Choisir (1 ou 2) [1]: 1

✅ Compte créé avec succès!

Générer une clé API maintenant? (O/n): O

🔑 VOTRE CLÉ API:
======================================================================
ufar_test_abc123xyz789def456ghi789jkl012
======================================================================

⚠️  CONSERVEZ CETTE CLÉ PRÉCIEUSEMENT!
```

### Étape 3: Tester l'API 🎯

```bash
# Remplacer VOTRE_CLE par la clé générée
curl -X GET "http://localhost:8000/api/public/health/" \
  -H "Authorization: ApiKey VOTRE_CLE"
```

**Réponse attendue:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-13T...",
  "version": "1.0.0"
}
```

---

## ✅ C'est Tout!

Vous pouvez maintenant utiliser tous les endpoints:

```bash
# Calculer les frais
curl "http://localhost:8000/api/public/fees/calculator/?amount=10000&type=P2P" \
  -H "Authorization: ApiKey VOTRE_CLE"

# Grille tarifaire
curl "http://localhost:8000/api/public/fees/schedule/" \
  -H "Authorization: ApiKey VOTRE_CLE"

# Taux de change
curl "http://localhost:8000/api/public/exchange-rates/" \
  -H "Authorization: ApiKey VOTRE_CLE"

# Pays supportés
curl "http://localhost:8000/api/public/countries/" \
  -H "Authorization: ApiKey VOTRE_CLE"
```

---

## 📚 Documentation Complète

- **Guide d'accès détaillé:** `ACCES_API_PUBLIQUE.md`
- **Documentation API:** `backend/PUBLIC_API_COMPLETE.md`
- **Guide de test:** `backend/TEST_PUBLIC_API.md`
- **Guide développeur:** `backend/DEVELOPER_API_GUIDE.md`

---

## 💡 Exemples de Code

### Python
```python
import requests

API_KEY = "ufar_test_abc123..."
headers = {"Authorization": f"ApiKey {API_KEY}"}

response = requests.get(
    "http://localhost:8000/api/public/health/",
    headers=headers
)
print(response.json())
```

### JavaScript
```javascript
const API_KEY = 'ufar_test_abc123...';
const headers = {'Authorization': `ApiKey ${API_KEY}`};

fetch('http://localhost:8000/api/public/health/', { headers })
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## 🆘 Besoin d'Aide?

**Problème:** "Clé API invalide"  
**Solution:** Vérifiez que vous avez bien copié la clé complète

**Problème:** "Quota dépassé"  
**Solution:** Attendez 1 minute ou augmentez vos quotas

**Problème:** Le serveur ne répond pas  
**Solution:** Vérifiez que Django est démarré: `python manage.py runserver`

---

**Bon développement! 🎉**
