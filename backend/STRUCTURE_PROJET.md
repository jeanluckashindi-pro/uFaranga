# Structure du Projet Ufaranga

**Date**: 2026-02-20  
**Version**: 1.0  
**Statut**: ✅ PROPRE ET ORGANISÉ

---

## 📁 Arborescence Complète

```
ufaranga/
│
├── 📄 .gitignore                          # Fichiers à ignorer par Git
├── 📄 README.md                           # Documentation principale
├── 📄 NETTOYAGE_PROJET.md                 # Rapport de nettoyage
├── 📄 STRUCTURE_PROJET.md                 # Ce fichier
├── 📄 manage.py                           # Script Django
├── 📄 Dockerfile                          # Configuration Docker
│
├── 📂 .kiro/                              # Configuration Kiro
│   ├── settings/
│   ├── specs/
│   └── steering/
│
├── 📂 apps/                               # Applications Django (12 apps)
│   ├── audit/                             # Audit et traçabilité
│   ├── authentication/                    # Authentification SMS
│   ├── bancaire/                          # Intégration bancaire
│   ├── commission/                        # Commissions
│   ├── compliance/                        # KYC, AML
│   ├── configuration/                     # Configuration système
│   ├── developpeurs/                      # API développeurs
│   ├── identite/                          # Gestion utilisateurs
│   ├── localisation/                      # Pays, provinces, districts
│   ├── notification/                      # Notifications
│   ├── portefeuille/                      # Portefeuilles virtuels
│   ├── public_api/                        # API publique
│   ├── transaction/                       # Transactions
│   ├── users/                             # Utilisateurs Django
│   └── wallets/                           # Wallets
│
├── 📂 config/                             # Configuration Django
│   ├── settings/
│   │   ├── base.py                        # Configuration de base
│   │   ├── development.py                 # Développement
│   │   └── production.py                  # Production
│   ├── urls.py                            # URLs principales
│   └── wsgi.py                            # WSGI
│
├── 📂 database_actuelle/                  # Structure SQL (5 fichiers)
│   ├── 📄 README.md                       # Guide complet de la base
│   ├── 📄 ufaranga_structure_updated_20260220.sql
│   │                                      # Structure complète (33 tables)
│   ├── 📄 triggers_grand_livre_automatique.sql
│   │                                      # Triggers automatiques
│   ├── 📄 GRAND_LIVRE_AUTOMATIQUE.md      # Documentation grand livre
│   └── 📄 RAPPORT_SYNCHRONISATION_COMPLETE.md
│                                          # Rapport synchronisation
│
├── 📂 documentation/                      # Documentation (9 fichiers)
│   ├── 📄 INDEX.md                        # Index de la documentation
│   ├── 📄 START_HERE.md                   # Point d'entrée
│   ├── 📄 DEMARRAGE_RAPIDE.md             # Guide rapide
│   ├── 📄 README.md                       # Vue d'ensemble
│   ├── 📄 README_LOCALISATION_COMPLETE.md # Module localisation
│   ├── 📄 CONFIGURATION_SMS_COMPLETE.md   # Configuration SMS
│   ├── 📄 QUICK_REFERENCE_ENDPOINTS.md    # Référence API
│   ├── 📄 OUTPUTS_REELS_ENDPOINTS.md      # Exemples API
│   └── 📄 ARBORESCENCE_COMPLETE.md        # Structure détaillée
│
├── 📂 logs/                               # Logs (vidés)
│   └── user-service.log                   # Log principal (vide)
│
├── 📂 scripts/                            # Scripts utilitaires (vide)
│
├── 📂 archives/                           # Archives
│
└── 📂 venv/                               # Environnement virtuel Python
```

---

## 🗄️ Base de Données PostgreSQL

### Structure (11 schémas, 33 tables)

```
PostgreSQL: ufaranga
│
├── 📊 audit (3 tables)
│   ├── historique_modifications
│   ├── journaux_evenements
│   └── sessions_utilisateurs
│
├── 📊 bancaire (3 tables)
│   ├── banques_partenaires
│   ├── comptes_bancaires_reels
│   └── mouvements_bancaires_reels
│
├── 📊 commission (2 tables)
│   ├── commissions
│   └── grilles_commissions
│
├── 📊 compliance (3 tables)
│   ├── documents_kyc
│   ├── screening_aml
│   └── verifications_kyc
│
├── 📊 configuration (9 tables)
│   ├── blacklist
│   ├── limites_transactions
│   ├── parametres_systeme
│   ├── taux_change
│   ├── plafonds_configuration          # Configuration dynamique
│   ├── regles_metier                   # Configuration dynamique
│   ├── frais_configuration             # Configuration dynamique
│   ├── types_transaction               # Configuration dynamique
│   └── devises_autorisees              # Configuration dynamique
│
├── 📊 ledger (1 table)
│   └── ecritures_comptables            # Grand livre (IMMUABLE)
│
├── 📊 notification (1 table)
│   └── notifications
│
├── 📊 portefeuille (5 tables)
│   ├── comptes                         # Comptes virtuels
│   ├── devises                         # Devises supportées
│   ├── historique_taux_change          # Historique (IMMUABLE)
│   ├── portefeuilles_virtuels
│   └── taux_change                     # Taux de change
│
├── 📊 reconciliation (2 tables)
│   ├── ecarts_reconciliation
│   └── sessions_reconciliation
│
├── 📊 securite (2 tables)
│   ├── alertes_fraude
│   └── sessions
│
└── 📊 transaction (2 tables)
    ├── grand_livre_comptable
    └── transactions
```

---

## 📚 Documentation

### Points d'Entrée

1. **Démarrage Rapide**
   - `README.md` (racine)
   - `documentation/START_HERE.md`
   - `documentation/DEMARRAGE_RAPIDE.md`

2. **Base de Données**
   - `database_actuelle/README.md`
   - `database_actuelle/GRAND_LIVRE_AUTOMATIQUE.md`
   - `database_actuelle/RAPPORT_SYNCHRONISATION_COMPLETE.md`

3. **API**
   - `documentation/QUICK_REFERENCE_ENDPOINTS.md`
   - `documentation/OUTPUTS_REELS_ENDPOINTS.md`

4. **Modules Spécifiques**
   - `documentation/README_LOCALISATION_COMPLETE.md`
   - `documentation/CONFIGURATION_SMS_COMPLETE.md`

---

## 🎯 Fichiers Clés

### Configuration
- `config/settings/base.py` - Configuration Django de base
- `.gitignore` - Fichiers ignorés par Git
- `Dockerfile` - Configuration Docker

### Base de Données
- `database_actuelle/ufaranga_structure_updated_20260220.sql` - Structure complète
- `database_actuelle/triggers_grand_livre_automatique.sql` - Triggers automatiques

### Documentation
- `README.md` - Documentation principale
- `documentation/INDEX.md` - Index complet
- `NETTOYAGE_PROJET.md` - Rapport de nettoyage

---

## 📊 Statistiques

### Code Python
- **Applications Django**: 15 apps
- **Modèles**: ~40 modèles
- **Vues**: ~50 vues
- **Serializers**: ~30 serializers

### Base de Données
- **Schémas**: 11
- **Tables**: 33
- **Fonctions**: 5 fonctions utilitaires
- **Triggers**: 8 triggers de protection
- **Vues**: 2 vues de contrôle

### Documentation
- **Fichiers racine**: 3 fichiers
- **database_actuelle**: 5 fichiers
- **documentation**: 9 fichiers
- **Total**: 17 fichiers de documentation

---

## 🔧 Commandes Utiles

### Développement
```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Lancer le serveur
python manage.py runserver

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Base de Données
```bash
# Se connecter à PostgreSQL
psql -U postgres -d ufaranga

# Charger la structure
psql -U postgres -d ufaranga -f database_actuelle/ufaranga_structure_updated_20260220.sql

# Charger les triggers
psql -U postgres -d ufaranga -f database_actuelle/triggers_grand_livre_automatique.sql

# Vérifier les tables
psql -U postgres -d ufaranga -c "SELECT schemaname, COUNT(*) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema') GROUP BY schemaname;"
```

### Nettoyage
```bash
# Nettoyer le cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Vider les logs
> logs/user-service.log
```

---

## 🚀 Déploiement

### Prérequis
- Python 3.8+
- PostgreSQL 10.3+
- Django 4.x
- Django REST Framework

### Étapes
1. Cloner le projet
2. Créer l'environnement virtuel
3. Installer les dépendances
4. Créer la base de données
5. Charger la structure SQL
6. Appliquer les migrations Django
7. Lancer le serveur

Voir `documentation/DEMARRAGE_RAPIDE.md` pour les détails.

---

## 📞 Support

### Documentation
- **Général**: `README.md`
- **Base de données**: `database_actuelle/README.md`
- **API**: `documentation/QUICK_REFERENCE_ENDPOINTS.md`
- **Index complet**: `documentation/INDEX.md`

### Liens Utiles
- API: http://127.0.0.1:8000/api/v1/
- Swagger: http://127.0.0.1:8000/api/docs/swagger/
- ReDoc: http://127.0.0.1:8000/api/docs/redoc/

---

**Structure Claire et Organisée!**  
**Documentation Complète!**  
**Prêt pour le Développement!**  
**Prêt pour la Production!**
