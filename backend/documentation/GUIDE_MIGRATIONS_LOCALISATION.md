# 🔄 Guide des Migrations - Localisation

## 📋 Vue d'Ensemble

Ce guide explique comment appliquer les modifications au modèle de localisation pour ajouter les colonnes `continent` et `sous_region`.

## 🎯 Modifications Apportées

### 1. Modèle Pays (`apps/localisation/models.py`)

**Champs Ajoutés:**
```python
continent = models.CharField(
    max_length=50,
    blank=True,
    null=True,
    db_index=True,
    help_text='Continent du pays (ex: Afrique, Europe, Asie)'
)

sous_region = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    db_index=True,
    help_text='Sous-région géographique (ex: Afrique de l\'Est)'
)
```

**Index Ajoutés:**
```python
indexes = [
    models.Index(fields=['continent']),
    models.Index(fields=['sous_region']),
    models.Index(fields=['code_iso_2']),
]
```

### 2. Serializers (`apps/localisation/serializers.py`)

**Champs Ajoutés aux Serializers:**
- `PaysSerializer`
- `CouverturePaysSerializer`
- `PaysDetailSerializer`

### 3. Filtres (`apps/localisation/filters.py`)

**Filtres Ajoutés:**
```python
continent = django_filters.CharFilter(lookup_expr='iexact')
sous_region = django_filters.CharFilter(lookup_expr='icontains')
```

---

## 🚀 Méthode 1: Utiliser les Migrations Django (Recommandé)

### Étape 1: Créer la Migration

```bash
python manage.py makemigrations localisation
```

**Output Attendu:**
```
Migrations for 'localisation':
  apps/localisation/migrations/0002_add_continent_sous_region.py
    - Add field continent to pays
    - Add field sous_region to pays
```

### Étape 2: Appliquer la Migration

```bash
python manage.py migrate localisation
```

**Output Attendu:**
```
Operations to perform:
  Apply all migrations: localisation
Running migrations:
  Applying localisation.0002_add_continent_sous_region... OK
```

### Étape 3: Vérifier

```bash
python manage.py showmigrations localisation
```

**Output Attendu:**
```
localisation
 [X] 0001_initial
 [X] 0002_add_continent_sous_region
```

---

## 🔧 Méthode 2: Utiliser le Script Python (Alternative)

Si vous préférez ne pas utiliser les migrations Django:

```bash
python analyser_et_completer_localisation.py
```

Le script va:
1. Détecter si les colonnes existent
2. Les ajouter via SQL direct si nécessaire
3. Créer les index

---

## ✅ Vérification

### 1. Vérifier les Colonnes en Base

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'localisation'
AND table_name = 'pays'
AND column_name IN ('continent', 'sous_region');
```

**Résultat Attendu:**
```
column_name  | data_type         | is_nullable
-------------+-------------------+-------------
continent    | character varying | YES
sous_region  | character varying | YES
```

### 2. Vérifier les Index

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'localisation'
AND tablename = 'pays'
AND indexname LIKE '%continent%' OR indexname LIKE '%sous_region%';
```

### 3. Tester l'API

```bash
# Tous les pays
curl http://127.0.0.1:8000/api/v1/localisation/pays/

# Pays africains
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique

# Pays d'Afrique de l'Est
curl "http://127.0.0.1:8000/api/v1/localisation/pays/?sous_region=Afrique%20de%20l'Est"
```

### 4. Vérifier dans Django Shell

```bash
python manage.py shell
```

```python
from apps.localisation.models import Pays

# Vérifier qu'on peut accéder aux nouveaux champs
pays = Pays.objects.first()
print(f"Continent: {pays.continent}")
print(f"Sous-région: {pays.sous_region}")

# Filtrer par continent
pays_africains = Pays.objects.filter(continent='Afrique')
print(f"Pays africains: {pays_africains.count()}")

# Filtrer par sous-région
pays_est = Pays.objects.filter(sous_region__icontains='Est')
print(f"Pays d'Afrique de l'Est: {pays_est.count()}")
```

---

## 📊 Peupler les Données

Après avoir appliqué les migrations, peuplez les données:

```bash
python analyser_et_completer_localisation.py
```

Répondez `o` (oui) quand demandé:
- Ajouter les colonnes? → `o` (ou skip si déjà fait)
- Peupler les pays africains? → `o`

---

## 🔄 Rollback (Si Nécessaire)

### Annuler la Migration Django

```bash
# Revenir à la migration précédente
python manage.py migrate localisation 0001_initial

# Supprimer le fichier de migration
rm apps/localisation/migrations/0002_add_continent_sous_region.py
```

### Supprimer les Colonnes Manuellement

```sql
ALTER TABLE localisation.pays DROP COLUMN IF EXISTS continent;
ALTER TABLE localisation.pays DROP COLUMN IF EXISTS sous_region;
```

---

## 🐛 Dépannage

### Erreur: Migration Already Applied

**Problème:**
```
Migration localisation.0002_add_continent_sous_region is already applied
```

**Solution:** C'est normal, la migration est déjà appliquée. Continuez.

### Erreur: Column Already Exists

**Problème:**
```
column "continent" of relation "pays" already exists
```

**Solution:** Les colonnes existent déjà. Vous pouvez:
1. Utiliser `--fake` pour marquer la migration comme appliquée:
   ```bash
   python manage.py migrate localisation 0002_add_continent_sous_region --fake
   ```

### Erreur: Permission Denied

**Problème:**
```
permission denied for schema localisation
```

**Solution:**
```sql
-- Se connecter en tant que postgres
GRANT ALL PRIVILEGES ON SCHEMA localisation TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA localisation TO ufaranga;
```

---

## 📝 Checklist Complète

### Avant Migration
- [ ] Backup de la base de données
- [ ] Django configuré correctement
- [ ] Environnement virtuel activé

### Pendant Migration
- [ ] Migration créée (`makemigrations`)
- [ ] Migration appliquée (`migrate`)
- [ ] Aucune erreur dans les logs

### Après Migration
- [ ] Colonnes `continent` et `sous_region` existent
- [ ] Index créés
- [ ] Modèle Django mis à jour
- [ ] Serializers mis à jour
- [ ] Filtres mis à jour
- [ ] API retourne les nouveaux champs
- [ ] Données peuplées (19 pays africains)

---

## 🎯 Prochaines Étapes

Après avoir appliqué les migrations:

1. **Peupler les Données:**
   ```bash
   python analyser_et_completer_localisation.py
   ```

2. **Ajouter Districts et Quartiers:**
   ```bash
   python ajouter_districts_quartiers.py
   ```

3. **Générer un Rapport:**
   ```bash
   python generer_rapport_geo.py
   ```

4. **Tester l'API:**
   ```bash
   curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique
   ```

---

**✅ Migrations prêtes à être appliquées!** 🚀
