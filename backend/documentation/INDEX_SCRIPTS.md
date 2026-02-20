# Index des Scripts - Système de Localisation

## 📁 Scripts SQL (`scripts_sql/`)

### 1. Peuplement des Pays
- **completer_tous_pays_africains.sql**
  - Peupler 54 pays africains avec continent et sous-région
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/completer_tous_pays_africains.sql`

- **completer_metadonnees_pays.sql**
  - Ajouter métadonnées complètes pour chaque pays
  - Capitale, devise, langues, indicatif téléphonique, population, etc.
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_pays.sql`

### 2. Peuplement des Provinces
- **peupler_toutes_provinces_districts.sql**
  - Provinces pour Afrique de l'Est (12 pays)
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/peupler_toutes_provinces_districts.sql`

- **peupler_provinces_afrique_centrale.sql**
  - Provinces pour Afrique Centrale (9 pays)
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_centrale.sql`

- **peupler_provinces_afrique_ouest.sql**
  - Provinces pour Afrique de l'Ouest (16 pays)
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_ouest.sql`

### 3. Métadonnées
- **completer_metadonnees_localisation.sql**
  - Métadonnées pour provinces, districts et quartiers
  - Population, économie, infrastructures, services
  - Exécution: `psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_localisation.sql`

## 🐍 Scripts Python (`scripts_python/`)

### 1. Peuplement Automatique
- **peupler_districts_quartiers_complet.py**
  - Créer automatiquement districts et quartiers pour toutes les provinces
  - Génère 3,374 districts et 16,542 quartiers
  - Exécution: `python scripts_python/peupler_districts_quartiers_complet.py`

### 2. Génération de Métadonnées
- **generer_metadonnees_automatiques.py**
  - Générer métadonnées intelligentes pour toutes les entités
  - Détection automatique du type de zone
  - Exécution: `python scripts_python/generer_metadonnees_automatiques.py`

## 📋 Ordre d'Exécution Recommandé

1. **Pays** (2 scripts SQL)
   ```bash
   psql -U postgres -d ufaranga -f scripts_sql/completer_tous_pays_africains.sql
   psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_pays.sql
   ```

2. **Provinces** (3 scripts SQL)
   ```bash
   psql -U postgres -d ufaranga -f scripts_sql/peupler_toutes_provinces_districts.sql
   psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_centrale.sql
   psql -U postgres -d ufaranga -f scripts_sql/peupler_provinces_afrique_ouest.sql
   ```

3. **Métadonnées Provinces** (1 script SQL)
   ```bash
   psql -U postgres -d ufaranga -f scripts_sql/completer_metadonnees_localisation.sql
   ```

4. **Districts et Quartiers** (1 script Python)
   ```bash
   python scripts_python/peupler_districts_quartiers_complet.py
   ```

5. **Métadonnées Automatiques** (1 script Python)
   ```bash
   python scripts_python/generer_metadonnees_automatiques.py
   ```

## ✅ Résultat Final

- 54 pays africains ✅
- 1,095 provinces ✅
- 3,374 districts ✅
- 16,542 quartiers ✅
- **Total: 21,065 entités** ✅

Toutes avec coordonnées GPS et métadonnées complètes!
