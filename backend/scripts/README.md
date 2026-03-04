# Scripts de Gestion des Divisions Administratives

Ce dossier contient les scripts pour gérer les divisions administratives dans le système Ufaranga.

## 📁 Fichiers Disponibles

### Scripts Python

#### 1. `load_gadm_african_countries.py`
**Description**: Charge les divisions administratives depuis GADM pour les pays africains.

**Usage**:
```bash
python scripts/load_gadm_african_countries.py
```

**Fonctionnalités**:
- Télécharge automatiquement les données GADM depuis geodata.ucdavis.edu
- Charge les divisions niveau 1 (provinces/régions) et niveau 2 (communes/districts)
- Génère automatiquement les division_id au format `UF-{ISO3}-{CONTINENT}-{REGION}-{ID}`
- Établit les relations hiérarchiques (parent_division_id)
- Active automatiquement les divisions (est_actif=TRUE, est_autorise=TRUE)

**Configuration**:
Modifier la variable `PAYS_A_CHARGER` dans le script pour ajouter d'autres pays:
```python
PAYS_A_CHARGER = {
    'BDI': 'Burundi',
    'COG': 'Congo',
    'COD': 'Democratic Republic of the Congo',
    # Ajouter d'autres pays ici
}
```

#### 2. `check_table_structure.py`
**Description**: Vérifie la structure des tables divisions_administratives.

**Usage**:
```bash
python scripts/check_table_structure.py
```

**Fonctionnalités**:
- Affiche les colonnes de chaque table (niveau0, niveau1, niveau2)
- Affiche les types de données et contraintes
- Utile pour déboguer ou adapter les scripts de chargement

#### 3. `verify_final_status.py`
**Description**: Vérifie le statut final du chargement des divisions.

**Usage**:
```bash
python scripts/verify_final_status.py
```

**Fonctionnalités**:
- Affiche les statistiques par pays (nombre de divisions par niveau)
- Affiche des exemples de divisions chargées
- Vérifie l'activation des pays
- Utile pour valider que tout est correctement chargé

### Rapports

#### `RAPPORT_FINAL_COMPLET.md`
Rapport détaillé du chargement des divisions administratives pour le Burundi, Congo et RD Congo.

**Contenu**:
- Résumé exécutif avec statistiques
- Structure hiérarchique des données
- Exemples de divisions chargées
- Requêtes SQL utiles
- Validation et tests effectués

---

## 🚀 Guide de Démarrage Rapide

### Charger des Divisions pour de Nouveaux Pays

1. **Vérifier que le pays a un mapping**:
   ```sql
   SELECT * FROM localisation.pays_mapping WHERE code_iso3 = 'XXX';
   ```

2. **Ajouter le mapping si nécessaire**:
   ```sql
   INSERT INTO localisation.pays_mapping 
   (code_iso3, nom_pays, continent_code, region_code, sequence_number)
   VALUES ('XXX', 'Nom du Pays', 'AFR', 'EAS', 1);
   ```

3. **Modifier le script de chargement**:
   Éditer `load_gadm_african_countries.py` et ajouter le pays dans `PAYS_A_CHARGER`.

4. **Exécuter le script**:
   ```bash
   python scripts/load_gadm_african_countries.py
   ```

5. **Vérifier le chargement**:
   ```bash
   python scripts/verify_final_status.py
   ```

---

## 📊 Statistiques Actuelles

### Pays Chargés
- 🇧🇮 **Burundi** (BDI): 17 provinces + 133 communes = 150 divisions
- 🇨🇬 **Congo** (COG): 12 régions + 48 districts = 60 divisions
- 🇨🇩 **RD Congo** (COD): 26 provinces + 240 territoires = 266 divisions

**Total**: 476 divisions administratives chargées

---

## 🔧 Configuration de la Base de Données

Les scripts utilisent la configuration suivante:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ufaranga',
    'user': 'ufaranga',
    'password': '12345',
}
```

Modifier ces valeurs dans chaque script si votre configuration est différente.

---

## 📋 Prérequis

### Packages Python Requis
```bash
pip install psycopg2-binary geopandas requests
```

### Structure de la Base de Données
Les tables suivantes doivent exister:
- `localisation.divisions_administratives_niveau0`
- `localisation.divisions_administratives_niveau1`
- `localisation.divisions_administratives_niveau2`
- `localisation.pays_mapping`
- `localisation.continents_regions`

---

## 🗺️ Format des Division_ID

Format standardisé: `UF-{ISO3}-{CONTINENT}-{REGION}-{SEQUENCE}`

**Exemples**:
- `UF-BDI-AFR-EAS-001` - Burundi, Afrique de l'Est, séquence 001
- `UF-COG-AFR-CAF-001` - Congo, Afrique Centrale, séquence 001
- `UF-COD-AFR-CAF-002` - RD Congo, Afrique Centrale, séquence 002

**Codes Continents**:
- AFR - Afrique
- AME - Amériques
- ASI - Asie
- EUR - Europe
- OCE - Océanie

**Codes Régions Africaines**:
- NAF - Afrique du Nord
- WAF - Afrique de l'Ouest
- CAF - Afrique Centrale
- EAS - Afrique de l'Est
- SAF - Afrique Australe

---

## 🔍 Requêtes SQL Utiles

### Lister tous les pays actifs
```sql
SELECT division_id, nom_pays, continent_code, region_code
FROM localisation.divisions_administratives_niveau0
WHERE est_actif = TRUE
ORDER BY continent_code, nom_pays;
```

### Lister les provinces d'un pays
```sql
SELECT division_id, nom_1, type_1
FROM localisation.divisions_administratives_niveau1
WHERE pays_division_id = 'UF-BDI-AFR-EAS-001'
ORDER BY nom_1;
```

### Compter les divisions par pays
```sql
SELECT 
    n0.nom_pays,
    COUNT(DISTINCT n1.division_id) as nb_niveau1,
    COUNT(DISTINCT n2.division_id) as nb_niveau2
FROM localisation.divisions_administratives_niveau0 n0
LEFT JOIN localisation.divisions_administratives_niveau1 n1 
    ON n0.division_id = n1.pays_division_id
LEFT JOIN localisation.divisions_administratives_niveau2 n2 
    ON n0.division_id = n2.pays_division_id
WHERE n0.est_actif = TRUE
GROUP BY n0.nom_pays;
```

---

## 📞 Support

Pour toute question ou problème:
1. Consulter le `RAPPORT_FINAL_COMPLET.md`
2. Vérifier la structure des tables avec `check_table_structure.py`
3. Vérifier le statut avec `verify_final_status.py`

---

**Dernière mise à jour**: 4 mars 2026  
**Version**: 1.0  
**Système**: Ufaranga - Module Localisation