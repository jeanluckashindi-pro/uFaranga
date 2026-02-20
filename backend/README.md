# Ufaranga - Système Bancaire Mobile

**Version**: 1.0  
**Date**: 2026-02-20  
**Statut**: ✅ OPÉRATIONNEL

Système bancaire mobile de grande envergure type M-PESA avec configuration dynamique, grand livre comptable automatique et traçabilité extrême.

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8+
- PostgreSQL 10.3+
- Django 4.x
- Django REST Framework

### Installation

1. **Cloner le projet**
```bash
git clone <repository>
cd ufaranga
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Créer la base de données**
```bash
createdb -U postgres ufaranga
psql -U postgres -d ufaranga -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U postgres -d ufaranga -c "CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";"
```

5. **Charger la structure**
```bash
psql -U postgres -d ufaranga -f database_actuelle/ufaranga_structure_updated_20260220.sql
psql -U postgres -d ufaranga -f database_actuelle/triggers_grand_livre_automatique.sql
```

6. **Appliquer les migrations Django**
```bash
python manage.py migrate
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

8. **Accéder à l'API**
- API: http://127.0.0.1:8000/api/v1/
- Swagger: http://127.0.0.1:8000/api/docs/swagger/
- ReDoc: http://127.0.0.1:8000/api/docs/redoc/

---

## 📚 Documentation

### Documentation Principale
- **[documentation/START_HERE.md](documentation/START_HERE.md)** - Point d'entrée
- **[documentation/INDEX.md](documentation/INDEX.md)** - Index complet
- **[documentation/DEMARRAGE_RAPIDE.md](documentation/DEMARRAGE_RAPIDE.md)** - Guide rapide

### Base de Données
- **[database_actuelle/README.md](database_actuelle/README.md)** - Structure complète
- **[database_actuelle/GRAND_LIVRE_AUTOMATIQUE.md](database_actuelle/GRAND_LIVRE_AUTOMATIQUE.md)** - Grand livre

### API
- **[documentation/QUICK_REFERENCE_ENDPOINTS.md](documentation/QUICK_REFERENCE_ENDPOINTS.md)** - Référence API
- **[documentation/OUTPUTS_REELS_ENDPOINTS.md](documentation/OUTPUTS_REELS_ENDPOINTS.md)** - Exemples

---

## 🏗️ Architecture

### Applications Django
```
apps/
├── authentication/     # Authentification (SMS, sessions)
├── identite/          # Gestion des utilisateurs et KYC
├── localisation/      # Pays, provinces, districts, quartiers
├── portefeuille/      # Comptes virtuels et soldes
├── transaction/       # Transactions et mouvements
├── bancaire/          # Intégration bancaire
├── configuration/     # Configuration dynamique
├── audit/             # Audit et traçabilité
├── compliance/        # KYC, AML
├── notification/      # Notifications
├── commission/        # Commissions
└── public_api/        # API publique
```

### Base de Données (11 schémas)
```
PostgreSQL
├── audit              # Historiques IMMUABLES
├── bancaire           # Banques et comptes réels
├── commission         # Commissions
├── compliance         # KYC, AML
├── configuration      # Configuration dynamique
├── ledger             # Grand livre comptable (IMMUABLE)
├── notification       # Notifications
├── portefeuille       # Devises, taux, comptes virtuels
├── reconciliation     # Réconciliation bancaire
├── securite           # Fraude, sessions
└── transaction        # Transactions
```

---

## 🎯 Fonctionnalités Principales

### ✅ Configuration Dynamique
- Plafonds par KYC et devise
- Règles métier configurables (JSON)
- Frais configurables par type de transaction
- Devises autorisées par type d'utilisateur
- Nombre de comptes par devise configurable

### ✅ Grand Livre Automatique
- Enregistrement automatique de TOUTES les opérations
- Comptabilité double entrée
- Traçabilité extrême (QUI, QUAND, QUOI, COMMENT, POURQUOI, OÙ)
- Protection IMMUABLE (triggers)
- Hash d'intégrité SHA-256

### ✅ Multi-Devises
- 8 devises supportées (BIF, USD, EUR, RWF, KES, TZS, UGX, CDF)
- Taux de change avec marges
- Conversion automatique
- Historique IMMUABLE des taux

### ✅ Types d'Utilisateurs
- CLIENT - Utilisateurs finaux
- AGENT - Agents de dépôt/retrait
- MARCHAND - Commerçants
- ADMIN - Administrateurs

### ✅ Niveaux KYC
- KYC 0 - Minimal (plafonds bas)
- KYC 1 - Standard (plafonds moyens)
- KYC 2 - Élevé (plafonds élevés)
- KYC 3 - Illimité (pas de plafonds)

### ✅ Types de Transactions
- DEPOT - Ajout d'argent
- RETRAIT - Retrait d'argent
- TRANSFERT - Transfert P2P
- PAIEMENT - Paiement marchand
- FRAIS - Prélèvement de frais
- COMMISSION - Commission agent/marchand
- AJUSTEMENT - Correction manuelle
- REMBOURSEMENT - Remboursement

---

## 🔒 Sécurité

### Authentification
- Authentification par SMS (OTP)
- Sessions sécurisées
- 2FA configurable
- Biométrie supportée

### Traçabilité
- Audit complet de toutes les opérations
- Historiques IMMUABLES
- Géolocalisation des opérations
- Hash d'intégrité

### Protection
- Triggers IMMUABLES sur tables critiques
- Détection de fraude
- Alertes automatiques
- Réconciliation bancaire

---

## 📊 API Endpoints

### Authentification
- `POST /api/v1/auth/login/` - Connexion
- `POST /api/v1/auth/logout/` - Déconnexion
- `POST /api/v1/auth/sms/send/` - Envoyer OTP
- `POST /api/v1/auth/sms/verify/` - Vérifier OTP

### Identité
- `GET /api/v1/identite/utilisateurs/` - Liste utilisateurs
- `GET /api/v1/identite/utilisateurs/{id}/` - Détails utilisateur
- `GET /api/v1/identite/utilisateurs/statistiques/` - Statistiques
- `GET /api/v1/identite/utilisateurs/par_type/` - Par type

### Localisation
- `GET /api/v1/localisation/pays/` - Liste pays
- `GET /api/v1/localisation/provinces/` - Liste provinces
- `GET /api/v1/localisation/districts/` - Liste districts
- `GET /api/v1/localisation/quartiers/` - Liste quartiers
- `GET /api/v1/localisation/complete/` - Localisation complète

### Portefeuille
- `GET /api/v1/portefeuille/comptes/` - Liste comptes
- `GET /api/v1/portefeuille/comptes/{id}/` - Détails compte
- `GET /api/v1/portefeuille/comptes/{id}/solde/` - Solde
- `GET /api/v1/portefeuille/comptes/{id}/historique/` - Historique

### Transactions
- `POST /api/v1/transactions/` - Créer transaction
- `GET /api/v1/transactions/` - Liste transactions
- `GET /api/v1/transactions/{id}/` - Détails transaction
- `POST /api/v1/transactions/{id}/annuler/` - Annuler

---

## 🛠️ Configuration

### Variables d'Environnement
```bash
# Base de données
DATABASE_NAME=ufaranga
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# SMS
SMS_PROVIDER=your_provider
SMS_API_KEY=your_api_key
```

### Settings Django
- `config/settings/base.py` - Configuration de base
- `config/settings/development.py` - Développement
- `config/settings/production.py` - Production

---

## 🧪 Tests

```bash
# Tous les tests
python manage.py test

# Tests d'une app
python manage.py test apps.identite

# Tests avec coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📦 Déploiement

### Docker
```bash
docker build -t ufaranga .
docker run -p 8000:8000 ufaranga
```

### Production
1. Configurer les variables d'environnement
2. Désactiver DEBUG
3. Configurer ALLOWED_HOSTS
4. Utiliser gunicorn/uwsgi
5. Configurer nginx
6. Activer HTTPS
7. Configurer les backups

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 Licence

Ce projet est sous licence propriétaire.

---

## 📞 Support

Pour toute question ou problème:
1. Consulter la documentation dans `documentation/`
2. Vérifier les exemples dans `documentation/OUTPUTS_REELS_ENDPOINTS.md`
3. Consulter le grand livre dans `database_actuelle/GRAND_LIVRE_AUTOMATIQUE.md`

---

**Système Bancaire Mobile Opérationnel**  
**Configuration Dynamique Active**  
**Grand Livre Automatique Protégé**  
**Prêt pour Production**
