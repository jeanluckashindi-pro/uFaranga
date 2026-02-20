# 🚀 Guide Rapide - Setup Tables de Référence

## ⚡ Solution la plus rapide (TOUT EN UN)

### Option 1: Script complet avec modification de la table utilisateurs ⭐ RECOMMANDÉ

```bash
# Depuis le dossier backend/
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql
```

Ce script fait TOUT:
- ✅ Crée les 3 tables de référence
- ✅ Insère les données (6 types, 4 niveaux, 5 statuts)
- ✅ Modifie la table `utilisateurs` pour utiliser les Foreign Keys

### Option 2: Étape par étape

```bash
# 1. Créer les tables
psql -U ufaranga -d ufaranga -f apps/identite/sql/create_tables_reference.sql

# 2. Insérer les données
psql -U ufaranga -d ufaranga -f apps/identite/sql/init_donnees_reference.sql

# 3. Modifier la table utilisateurs
psql -U ufaranga -d ufaranga -f apps/identite/sql/alter_table_utilisateurs.sql
```

## ✅ Vérification

Après l'exécution, vous devriez voir:

```
✓ Table types_utilisateurs créée
✓ Table niveaux_kyc créée
✓ Table statuts_utilisateurs créée
✓ 6 types d'utilisateurs insérés
✓ 4 niveaux KYC insérés
✓ 5 statuts utilisateurs insérés

 types | niveaux | statuts 
-------+---------+---------
     6 |       4 |       5
```

## 🔄 Redémarrer Django

Après le setup SQL:

```bash
# Arrêter Django (Ctrl+C)
# Puis redémarrer
python manage.py runserver
```

## 🧪 Tester la connexion

Essayez de vous connecter avec un utilisateur existant. L'erreur devrait être résolue.

## ❌ En cas d'erreur

### "relation does not exist"
→ Le script n'a pas été exécuté. Relancer `setup_complet.sql`

### "permission denied"
→ Vérifier les permissions PostgreSQL:
```sql
GRANT ALL PRIVILEGES ON SCHEMA identite TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA identite TO ufaranga;
```

### "psql: command not found"
→ PostgreSQL n'est pas dans le PATH. Utiliser le chemin complet:
```bash
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U ufaranga -d ufaranga -f setup_complet.sql
```

## 📊 Consulter les données

```sql
-- Se connecter à PostgreSQL
psql -U ufaranga -d ufaranga

-- Voir les types
SELECT * FROM identite.types_utilisateurs ORDER BY ordre_affichage;

-- Voir les niveaux KYC
SELECT * FROM identite.niveaux_kyc ORDER BY niveau;

-- Voir les statuts
SELECT * FROM identite.statuts_utilisateurs ORDER BY ordre_affichage;
```

## 🎯 Résumé des fichiers

- `setup_complet.sql` ⭐ - Script tout-en-un (RECOMMANDÉ)
- `executer_setup.bat` - Script Windows pour exécution facile
- `create_tables_reference.sql` - Création des tables uniquement
- `init_donnees_reference.sql` - Insertion des données uniquement
- `requetes_individuelles.sql` - Requêtes une par une

## 💡 Astuce

Si vous devez réinitialiser les données:

```sql
-- Supprimer les données (pas les tables)
TRUNCATE identite.types_utilisateurs CASCADE;
TRUNCATE identite.niveaux_kyc CASCADE;
TRUNCATE identite.statuts_utilisateurs CASCADE;

-- Puis ré-exécuter setup_complet.sql
```
