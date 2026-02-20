# uFaranga Backend - Système de Localisation

## 🎯 Vue d'Ensemble

Système de localisation géographique complet pour l'Afrique avec 21,065 entités:
- 54 pays africains
- 1,095 provinces
- 3,374 districts
- 16,542 quartiers

## 📁 Structure du Projet

```
.
├── scripts_sql/              # Scripts SQL de peuplement
├── scripts_python/           # Scripts Python utilitaires
├── documentation/            # Documentation complète
├── archives/                 # Fichiers archivés
├── apps/                     # Applications Django
│   ├── localisation/        # Module de localisation
│   ├── identite/            # Module d'identité
│   └── ...
└── config/                   # Configuration Django
```

## 🚀 Démarrage Rapide

### 1. Peupler la Base de Données

```bash
# Étape 1: Pays avec métadonnées
psql -U postgres -d ufaranga -f scripts_sql/completer_tous_pays_africains.sql
psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_pays.sql

# Étape 2: Provinces
psql -U postgres -d ufaranga -f scripts_sql/peupler_toutes_provinces_districts.sql
psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_centrale.sql
psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_ouest.sql

# Étape 3: Métadonnées provinces
psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_localisation.sql

# Étape 4: Districts et Quartiers
python scripts_python/peupler_districts_quartiers_complet.py

# Étape 5: Métadonnées automatiques
python scripts_python/generer_metadonnees_automatiques.py
```

### 2. Lancer le Serveur

```bash
python manage.py runserver
```

### 3. Tester l'API

```bash
# Tous les pays africains
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique

# Provinces d'un pays
curl http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id={uuid}

# Districts d'une province
curl http://127.0.0.1:8000/api/v1/localisation/districts/?province_id={uuid}

# Quartiers d'un district
curl http://127.0.0.1:8000/api/v1/localisation/quartiers/?district_id={uuid}
```

## 📊 Statistiques

| Niveau | Quantité | Avec GPS | Avec Métadonnées |
|--------|----------|----------|------------------|
| Pays | 54 | 100% | 100% |
| Provinces | 1,095 | 100% | 100% |
| Districts | 3,374 | 100% | 100% |
| Quartiers | 16,542 | 100% | 100% |
| **TOTAL** | **21,065** | **100%** | **100%** |

## 📖 Documentation

Consultez `documentation/RAPPORT_FINAL_COMPLET_LOCALISATION.md` pour la documentation complète.

## 🔧 Scripts Disponibles

### Scripts SQL (`scripts_sql/`)
- `completer_tous_pays_africains.sql` - Peupler 54 pays africains
- `completer_metadonnees_pays.sql` - Métadonnées des pays
- `peupler_toutes_provinces_districts.sql` - Provinces Afrique de l'Est
- `peupler_provinces_afrique_centrale.sql` - Provinces Afrique Centrale
- `peupler_provinces_afrique_ouest.sql` - Provinces Afrique de l'Ouest
- `completer_metadonnees_localisation.sql` - Métadonnées provinces

### Scripts Python (`scripts_python/`)
- `peupler_districts_quartiers_complet.py` - Créer districts et quartiers
- `generer_metadonnees_automatiques.py` - Générer métadonnées automatiques

## 🌐 API Endpoints

- `GET /api/v1/localisation/pays/` - Liste des pays
- `GET /api/v1/localisation/provinces/` - Liste des provinces
- `GET /api/v1/localisation/districts/` - Liste des districts
- `GET /api/v1/localisation/quartiers/` - Liste des quartiers

## 📝 Licence

Propriétaire - uFaranga

## 👥 Équipe

Développé pour uFaranga Backend
