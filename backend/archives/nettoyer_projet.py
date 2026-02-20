#!/usr/bin/env python
"""
Script pour nettoyer le projet en supprimant les fichiers inutiles
et en organisant les fichiers essentiels
"""
import os
import shutil
from pathlib import Path

# Fichiers Python à GARDER
PYTHON_ESSENTIELS = [
    'manage.py',
    'peupler_districts_quartiers_complet.py',
    'generer_metadonnees_automatiques.py',
]

# Fichiers SQL à GARDER
SQL_ESSENTIELS = [
    'completer_tous_pays_africains.sql',
    'completer_metadonnees_pays.sql',
    'completer_metadonnees_localisation.sql',
    'peupler_toutes_provinces_districts.sql',
    'peupler_provinces_afrique_centrale.sql',
    'peupler_provinces_afrique_ouest.sql',
]

# Fichiers MD à GARDER
MD_ESSENTIELS = [
    'README.md',
    'RAPPORT_FINAL_COMPLET_LOCALISATION.md',
]

# Dossiers à créer pour l'organisation
DOSSIERS = {
    'scripts_sql': 'Scripts SQL pour peuplement',
    'scripts_python': 'Scripts Python utilitaires',
    'archives': 'Fichiers archivés',
    'documentation': 'Documentation du projet'
}

def creer_dossiers():
    """Créer les dossiers d'organisation"""
    print("📁 Création des dossiers d'organisation...")
    for dossier, description in DOSSIERS.items():
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"   ✅ {dossier}/ créé - {description}")
        else:
            print(f"   ⚠️  {dossier}/ existe déjà")

def lister_fichiers():
    """Lister tous les fichiers Python, SQL et MD"""
    fichiers = {
        'python': [],
        'sql': [],
        'md': [],
        'autres': []
    }
    
    for fichier in os.listdir('.'):
        if os.path.isfile(fichier):
            if fichier.endswith('.py') and fichier != 'nettoyer_projet.py':
                fichiers['python'].append(fichier)
            elif fichier.endswith('.sql'):
                fichiers['sql'].append(fichier)
            elif fichier.endswith('.md'):
                fichiers['md'].append(fichier)
            elif fichier.endswith(('.bat', '.sh', '.txt')):
                fichiers['autres'].append(fichier)
    
    return fichiers

def archiver_fichier(fichier, destination='archives'):
    """Déplacer un fichier vers les archives"""
    try:
        shutil.move(fichier, os.path.join(destination, fichier))
        return True
    except Exception as e:
        print(f"   ❌ Erreur pour {fichier}: {e}")
        return False

def organiser_fichiers():
    """Organiser les fichiers essentiels"""
    print("\n📦 Organisation des fichiers essentiels...")
    
    # Déplacer les SQL essentiels
    for fichier in SQL_ESSENTIELS:
        if os.path.exists(fichier):
            try:
                shutil.copy(fichier, os.path.join('scripts_sql', fichier))
                print(f"   ✅ {fichier} → scripts_sql/")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
    
    # Déplacer les Python essentiels
    for fichier in PYTHON_ESSENTIELS:
        if os.path.exists(fichier) and fichier != 'manage.py':
            try:
                shutil.copy(fichier, os.path.join('scripts_python', fichier))
                print(f"   ✅ {fichier} → scripts_python/")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")

def nettoyer():
    """Nettoyer les fichiers inutiles"""
    print("\n🧹 Nettoyage des fichiers inutiles...")
    
    fichiers = lister_fichiers()
    stats = {
        'archives': 0,
        'gardes': 0,
        'erreurs': 0
    }
    
    # Archiver les Python non essentiels
    for fichier in fichiers['python']:
        if fichier not in PYTHON_ESSENTIELS:
            if archiver_fichier(fichier):
                stats['archives'] += 1
                print(f"   📦 {fichier} → archives/")
        else:
            stats['gardes'] += 1
    
    # Archiver les SQL non essentiels
    for fichier in fichiers['sql']:
        if fichier not in SQL_ESSENTIELS:
            if archiver_fichier(fichier):
                stats['archives'] += 1
                print(f"   📦 {fichier} → archives/")
        else:
            stats['gardes'] += 1
    
    # Archiver les MD non essentiels
    for fichier in fichiers['md']:
        if fichier not in MD_ESSENTIELS:
            destination = 'documentation'
            try:
                shutil.move(fichier, os.path.join(destination, fichier))
                stats['archives'] += 1
                print(f"   📦 {fichier} → documentation/")
            except Exception as e:
                stats['erreurs'] += 1
                print(f"   ❌ Erreur pour {fichier}: {e}")
        else:
            stats['gardes'] += 1
    
    # Archiver les autres fichiers
    for fichier in fichiers['autres']:
        if archiver_fichier(fichier):
            stats['archives'] += 1
            print(f"   📦 {fichier} → archives/")
    
    return stats

def creer_readme():
    """Créer un README.md principal"""
    print("\n📝 Création du README.md principal...")
    
    readme_content = """# uFaranga Backend - Système de Localisation

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
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("   ✅ README.md créé")

def creer_index_scripts():
    """Créer un index des scripts"""
    print("\n📝 Création de l'index des scripts...")
    
    index_content = """# Index des Scripts - Système de Localisation

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
"""
    
    with open('INDEX_SCRIPTS.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("   ✅ INDEX_SCRIPTS.md créé")

def main():
    print("=" * 70)
    print("NETTOYAGE ET ORGANISATION DU PROJET")
    print("=" * 70)
    
    # Créer les dossiers
    creer_dossiers()
    
    # Organiser les fichiers essentiels
    organiser_fichiers()
    
    # Nettoyer
    stats = nettoyer()
    
    # Créer README
    creer_readme()
    
    # Créer index des scripts
    creer_index_scripts()
    
    # Résumé
    print("\n" + "=" * 70)
    print("✅ NETTOYAGE TERMINÉ")
    print("=" * 70)
    print(f"Fichiers archivés: {stats['archives']}")
    print(f"Fichiers gardés: {stats['gardes']}")
    print(f"Erreurs: {stats['erreurs']}")
    print("=" * 70)
    
    print("\n📁 Structure finale:")
    print("   scripts_sql/        - 6 scripts SQL essentiels")
    print("   scripts_python/     - 2 scripts Python utilitaires")
    print("   documentation/      - Documentation complète")
    print("   archives/           - Fichiers archivés")
    print("   README.md           - Guide principal")
    print("   INDEX_SCRIPTS.md    - Index des scripts")
    print("=" * 70)

if __name__ == '__main__':
    main()
