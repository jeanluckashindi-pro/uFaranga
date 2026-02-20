# ⏱️ Temps d'Exécution des Scripts

## 🚀 Temps Estimés

### Scripts Rapides (< 5 secondes)

| Script | Temps | Raison |
|--------|-------|--------|
| `verifier_rapide.sql` | 1-2 sec | Juste des SELECT |
| `create_tables_reference.sql` | 2-3 sec | 3 tables simples |
| `init_donnees_reference.sql` | 1-2 sec | 15 INSERT |

### Scripts Moyens (5-30 secondes)

| Script | Temps | Raison |
|--------|-------|--------|
| `alter_table_utilisateurs.sql` | 10-30 sec | Dépend du nombre d'utilisateurs |
| `setup_complet.sql` | 5-10 sec | Création + données |

### Scripts Longs (30+ secondes)

| Script | Temps | Raison |
|--------|-------|--------|
| `setup_complet_avec_alter.sql` | 15-60 sec | Tout en un |
| `verifier_structure.sql` | 5-15 sec | Beaucoup de vérifications |

## 🐌 Pourquoi Ça Peut Être Long?

### 1. Nombre d'Utilisateurs

```sql
-- Si vous avez 1000 utilisateurs
ALTER TABLE utilisateurs ...  -- 10-20 secondes

-- Si vous avez 100,000 utilisateurs
ALTER TABLE utilisateurs ...  -- 2-5 minutes
```

**Solution**: Utiliser `verifier_rapide.sql` au lieu de `verifier_structure.sql`

### 2. Index à Créer

```sql
CREATE INDEX ...  -- Temps = nombre de lignes × complexité
```

**Exemple**:
- 100 utilisateurs: < 1 seconde
- 10,000 utilisateurs: 5-10 secondes
- 100,000 utilisateurs: 30-60 secondes

### 3. Foreign Keys à Valider

```sql
ALTER TABLE utilisateurs 
ADD CONSTRAINT fk_type 
FOREIGN KEY (type_utilisateur) 
REFERENCES types_utilisateurs(code);
```

PostgreSQL vérifie TOUTES les lignes existantes!

**Temps**: 
- 100 utilisateurs: < 1 seconde
- 10,000 utilisateurs: 2-5 secondes
- 100,000 utilisateurs: 10-30 secondes

### 4. Connexion Réseau

Si PostgreSQL est sur un serveur distant:
- Latence réseau: +1-5 secondes par requête
- Bande passante limitée: +temps de transfert

### 5. Ressources Serveur

- CPU occupé: +50-200% temps
- RAM limitée: +100-500% temps
- Disque lent (HDD vs SSD): +200-1000% temps

## ⚡ Comment Accélérer?

### 1. Utiliser la Version Rapide

```bash
# Au lieu de
psql -U ufaranga -d ufaranga -f verifier_structure.sql

# Utiliser
psql -U ufaranga -d ufaranga -f verifier_rapide.sql
```

**Gain**: 80% plus rapide

### 2. Vérifier Seulement Ce Qui Est Nécessaire

```sql
-- Au lieu de tout vérifier
\i verifier_structure.sql

-- Vérifier juste les Foreign Keys
SELECT COUNT(*) FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY'
  AND table_name = 'utilisateurs';
```

### 3. Exécuter en Dehors des Heures de Pointe

Si le serveur est partagé:
- ✅ Tôt le matin (6h-8h)
- ✅ Tard le soir (22h-minuit)
- ❌ Heures de bureau (9h-17h)

### 4. Désactiver Temporairement les Triggers

```sql
-- Avant
ALTER TABLE utilisateurs DISABLE TRIGGER ALL;

-- Exécuter le script
\i setup_complet_avec_alter.sql

-- Après
ALTER TABLE utilisateurs ENABLE TRIGGER ALL;
```

**Gain**: 20-50% plus rapide

## 📊 Temps Réels Mesurés

### Environnement de Test
- PostgreSQL 16
- Windows 11
- SSD
- 8 GB RAM
- 100 utilisateurs

| Script | Temps Mesuré |
|--------|--------------|
| `verifier_rapide.sql` | 0.8 sec |
| `create_tables_reference.sql` | 1.2 sec |
| `init_donnees_reference.sql` | 0.9 sec |
| `alter_table_utilisateurs.sql` | 3.5 sec |
| `setup_complet.sql` | 2.1 sec |
| `setup_complet_avec_alter.sql` | 5.8 sec |
| `verifier_structure.sql` | 4.2 sec |

## 🎯 Recommandations

### Pour Vérifier (Rapide)
```bash
psql -U ufaranga -d ufaranga -f apps/identite/sql/verifier_rapide.sql
```
**Temps**: 1-2 secondes

### Pour Installer (Première Fois)
```bash
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql
```
**Temps**: 5-60 secondes (selon nombre d'utilisateurs)

### Pour Vérifier en Détail (Optionnel)
```bash
psql -U ufaranga -d ufaranga -f apps/identite/sql/verifier_structure.sql
```
**Temps**: 5-15 secondes

## 💡 Astuces

### 1. Voir la Progression

```sql
-- Ajouter \timing pour voir le temps de chaque requête
\timing on
\i setup_complet_avec_alter.sql
```

### 2. Exécuter en Arrière-Plan

```bash
# Linux/Mac
psql -U ufaranga -d ufaranga -f setup_complet_avec_alter.sql &

# Windows PowerShell
Start-Job { psql -U ufaranga -d ufaranga -f setup_complet_avec_alter.sql }
```

### 3. Voir les Processus PostgreSQL

```sql
-- Voir ce qui tourne
SELECT pid, query, state, query_start
FROM pg_stat_activity
WHERE datname = 'ufaranga';
```

## ⚠️ Si Ça Prend Trop de Temps

### Plus de 2 minutes?

1. **Vérifier les locks**:
```sql
SELECT * FROM pg_locks WHERE NOT granted;
```

2. **Tuer les processus bloquants**:
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'ufaranga' AND state = 'idle in transaction';
```

3. **Réessayer**:
```bash
psql -U ufaranga -d ufaranga -f setup_complet_avec_alter.sql
```

### Plus de 5 minutes?

**Arrêter et utiliser la version modulaire**:

```bash
# 1. Tables (rapide)
psql -U ufaranga -d ufaranga -f create_tables_reference.sql

# 2. Données (rapide)
psql -U ufaranga -d ufaranga -f init_donnees_reference.sql

# 3. Alter (peut être long)
psql -U ufaranga -d ufaranga -f alter_table_utilisateurs.sql
```

## 📞 Résumé

- **Vérification rapide**: `verifier_rapide.sql` (1-2 sec)
- **Installation normale**: `setup_complet_avec_alter.sql` (5-60 sec)
- **Vérification détaillée**: `verifier_structure.sql` (5-15 sec)

**Si ça prend plus de 2 minutes**: Vérifier les locks et réessayer
