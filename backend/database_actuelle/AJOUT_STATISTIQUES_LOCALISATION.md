# Ajout des Colonnes Statistiques - Module Localisation

**Date**: 2026-02-20  
**Statut**: ✅ TERMINÉ  
**Tables Modifiées**: 5 tables

---

## 📊 Colonnes Ajoutées

Les colonnes suivantes ont été ajoutées à **toutes** les tables du schéma localisation:

1. `nombre_agents` (INTEGER, DEFAULT 0)
   - Nombre total d'agents dans cette zone géographique

2. `nombre_utilisateurs` (INTEGER, DEFAULT 0)
   - Nombre total d'utilisateurs dans cette zone géographique

3. `nombre_agents_actifs` (INTEGER, DEFAULT 0)
   - Nombre d'agents avec statut ACTIF dans cette zone

4. `nombre_utilisateurs_actifs` (INTEGER, DEFAULT 0)
   - Nombre d'utilisateurs avec statut ACTIF dans cette zone

---

## 🗄️ Tables Modifiées

### 1. localisation.pays
```sql
ALTER TABLE localisation.pays
ADD COLUMN nombre_agents INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_agents_actifs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs_actifs INTEGER DEFAULT 0 NOT NULL;
```

### 2. localisation.provinces
```sql
ALTER TABLE localisation.provinces
ADD COLUMN nombre_agents INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_agents_actifs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs_actifs INTEGER DEFAULT 0 NOT NULL;
```

### 3. localisation.districts
```sql
ALTER TABLE localisation.districts
ADD COLUMN nombre_agents INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_agents_actifs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs_actifs INTEGER DEFAULT 0 NOT NULL;
```

### 4. localisation.quartiers
```sql
ALTER TABLE localisation.quartiers
ADD COLUMN nombre_agents INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_agents_actifs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs_actifs INTEGER DEFAULT 0 NOT NULL;
```

### 5. localisation.points_de_service
```sql
ALTER TABLE localisation.points_de_service
ADD COLUMN nombre_agents INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_agents_actifs INTEGER DEFAULT 0 NOT NULL,
ADD COLUMN nombre_utilisateurs_actifs INTEGER DEFAULT 0 NOT NULL;
```

---

## 🔧 Fonction de Mise à Jour

Une fonction PostgreSQL a été créée pour mettre à jour automatiquement ces statistiques:

```sql
SELECT localisation.mettre_a_jour_statistiques_localisation();
```

### Fonctionnement

La fonction met à jour les statistiques dans l'ordre hiérarchique:
1. **Quartiers** - Compte directement depuis `identite.utilisateurs`
2. **Districts** - Agrège depuis les quartiers
3. **Provinces** - Agrège depuis les districts
4. **Pays** - Agrège depuis les provinces
5. **Points de service** - Compte directement depuis `identite.utilisateurs`

### Exemple d'Utilisation

```sql
-- Mettre à jour toutes les statistiques
SELECT localisation.mettre_a_jour_statistiques_localisation();

-- Vérifier les statistiques d'un pays
SELECT 
    nom,
    nombre_agents,
    nombre_utilisateurs,
    nombre_agents_actifs,
    nombre_utilisateurs_actifs
FROM localisation.pays
WHERE code_iso_2 = 'BI';

-- Vérifier les statistiques d'une province
SELECT 
    p.nom as province,
    pa.nom as pays,
    p.nombre_agents,
    p.nombre_utilisateurs,
    p.nombre_agents_actifs,
    p.nombre_utilisateurs_actifs
FROM localisation.provinces p
JOIN localisation.pays pa ON p.pays_id = pa.id
WHERE pa.code_iso_2 = 'BI';
```

---

## 🐍 Modèles Django Mis à Jour

Les modèles Django dans `apps/localisation/models.py` ont été mis à jour:

### Classe Pays
```python
# Statistiques
nombre_agents = models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce pays')
nombre_utilisateurs = models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce pays')
nombre_agents_actifs = models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce pays')
nombre_utilisateurs_actifs = models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce pays')
```

### Classe Province
```python
# Statistiques
nombre_agents = models.IntegerField(default=0, help_text='Nombre total d\'agents dans cette province')
nombre_utilisateurs = models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans cette province')
nombre_agents_actifs = models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans cette province')
nombre_utilisateurs_actifs = models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans cette province')
```

### Classe District
```python
# Statistiques
nombre_agents = models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce district')
nombre_utilisateurs = models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce district')
nombre_agents_actifs = models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce district')
nombre_utilisateurs_actifs = models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce district')
```

### Classe Quartier
```python
# Statistiques
nombre_agents = models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce quartier')
nombre_utilisateurs = models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce quartier')
nombre_agents_actifs = models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce quartier')
nombre_utilisateurs_actifs = models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce quartier')
```

### Classe PointDeService
```python
# Statistiques
nombre_agents = models.IntegerField(default=0, help_text='Nombre total d\'agents à ce point de service')
nombre_utilisateurs = models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs à ce point de service')
nombre_agents_actifs = models.IntegerField(default=0, help_text='Nombre d\'agents actifs à ce point de service')
nombre_utilisateurs_actifs = models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs à ce point de service')
```

---

## 📝 Migration Django

Une migration Django a été créée:

**Fichier**: `apps/localisation/migrations/0005_add_statistiques_columns.py`

### Appliquer la Migration

```bash
python manage.py migrate localisation
```

---

## 📊 Exemples de Requêtes

### 1. Statistiques par Pays
```sql
SELECT 
    nom,
    code_iso_2,
    nombre_agents,
    nombre_utilisateurs,
    nombre_agents_actifs,
    nombre_utilisateurs_actifs,
    ROUND(nombre_agents_actifs::DECIMAL / NULLIF(nombre_agents, 0) * 100, 2) as taux_agents_actifs,
    ROUND(nombre_utilisateurs_actifs::DECIMAL / NULLIF(nombre_utilisateurs, 0) * 100, 2) as taux_utilisateurs_actifs
FROM localisation.pays
WHERE est_actif = TRUE
ORDER BY nombre_utilisateurs DESC;
```

### 2. Top 10 Provinces par Nombre d'Utilisateurs
```sql
SELECT 
    p.nom as province,
    pa.nom as pays,
    p.nombre_agents,
    p.nombre_utilisateurs,
    p.nombre_agents_actifs,
    p.nombre_utilisateurs_actifs
FROM localisation.provinces p
JOIN localisation.pays pa ON p.pays_id = pa.id
WHERE p.est_actif = TRUE
ORDER BY p.nombre_utilisateurs DESC
LIMIT 10;
```

### 3. Districts avec le Plus d'Agents Actifs
```sql
SELECT 
    d.nom as district,
    p.nom as province,
    pa.nom as pays,
    d.nombre_agents_actifs,
    d.nombre_utilisateurs_actifs
FROM localisation.districts d
JOIN localisation.provinces p ON d.province_id = p.id
JOIN localisation.pays pa ON p.pays_id = pa.id
WHERE d.est_actif = TRUE
ORDER BY d.nombre_agents_actifs DESC
LIMIT 10;
```

### 4. Quartiers sans Agents
```sql
SELECT 
    q.nom as quartier,
    d.nom as district,
    p.nom as province,
    q.nombre_utilisateurs
FROM localisation.quartiers q
JOIN localisation.districts d ON q.district_id = d.id
JOIN localisation.provinces p ON d.province_id = p.id
WHERE q.est_actif = TRUE
  AND q.nombre_agents = 0
  AND q.nombre_utilisateurs > 0
ORDER BY q.nombre_utilisateurs DESC;
```

### 5. Points de Service les Plus Actifs
```sql
SELECT 
    ps.nom as point_service,
    ps.type_point,
    q.nom as quartier,
    ps.nombre_agents_actifs,
    ps.nombre_utilisateurs_actifs
FROM localisation.points_de_service ps
JOIN localisation.quartiers q ON ps.quartier_id = q.id
WHERE ps.est_actif = TRUE
ORDER BY ps.nombre_utilisateurs_actifs DESC
LIMIT 20;
```

---

## 🔄 Mise à Jour Automatique (Future)

### Trigger Automatique

Un trigger peut être activé pour mettre à jour automatiquement les statistiques:

```sql
-- Activer le trigger (une fois la table identite.utilisateurs créée)
DROP TRIGGER IF EXISTS trigger_maj_stats_localisation ON identite.utilisateurs;
CREATE TRIGGER trigger_maj_stats_localisation
    AFTER INSERT OR UPDATE OR DELETE ON identite.utilisateurs
    FOR EACH STATEMENT
    EXECUTE PROCEDURE localisation.trigger_maj_statistiques();
```

### Mise à Jour Périodique

Créer un job cron ou une tâche Celery pour mettre à jour les statistiques:

```python
# Dans tasks.py
from django.db import connection

@shared_task
def mettre_a_jour_statistiques_localisation():
    """Met à jour les statistiques de localisation"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT localisation.mettre_a_jour_statistiques_localisation();")
    return "Statistiques mises à jour"
```

---

## ✅ Vérification

### Vérifier les Colonnes
```sql
SELECT 
    column_name,
    data_type,
    column_default
FROM information_schema.columns
WHERE table_schema = 'localisation'
  AND table_name = 'pays'
  AND column_name LIKE 'nombre_%'
ORDER BY column_name;
```

### Vérifier les Index
```sql
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_indexes
WHERE schemaname = 'localisation'
  AND indexname LIKE '%stats%';
```

---

## 📞 Support

Pour mettre à jour les statistiques:
```sql
SELECT localisation.mettre_a_jour_statistiques_localisation();
```

Pour vérifier les statistiques:
```sql
SELECT * FROM localisation.pays WHERE code_iso_2 = 'BI';
```

---

**Colonnes Statistiques Ajoutées!**  
**Fonction de Mise à Jour Créée!**  
**Modèles Django Synchronisés!**  
**Prêt pour Utilisation!**
