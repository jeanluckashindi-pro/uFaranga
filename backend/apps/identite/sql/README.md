# Scripts SQL - Données de Référence Identité

Ce dossier contient les scripts SQL pour créer et initialiser les données de référence du module identité.

## 📁 Fichiers disponibles

### 1. `create_tables_reference.sql` ⭐ EXÉCUTER EN PREMIER
Script pour créer les 3 tables de référence (types, niveaux KYC, statuts).

### 2. `init_donnees_reference.sql`
Script complet qui insère toutes les données de référence en une seule fois.

### 3. `requetes_individuelles.sql`
Requêtes SQL individuelles que vous pouvez copier-coller une par une.

## 🚀 Utilisation

### ⚠️ IMPORTANT: Ordre d'exécution

```bash
# 1. D'ABORD: Créer les tables
psql -U ufaranga -d ufaranga -f apps/identite/sql/create_tables_reference.sql

# 2. ENSUITE: Insérer les données
psql -U ufaranga -d ufaranga -f apps/identite/sql/init_donnees_reference.sql
```

### Option 1: Via psql (PostgreSQL) - RECOMMANDÉ

```bash
# Se connecter à la base de données
psql -U ufaranga -d ufaranga

# Exécuter les scripts dans l'ordre
\i apps/identite/sql/create_tables_reference.sql
\i apps/identite/sql/init_donnees_reference.sql
```

### Option 2: Via pgAdmin ou autre client SQL

1. Ouvrir pgAdmin
2. Se connecter à la base de données `ufaranga`
3. Ouvrir l'éditeur de requêtes
4. **ÉTAPE 1**: Copier-coller le contenu de `create_tables_reference.sql` et exécuter
5. **ÉTAPE 2**: Copier-coller le contenu de `init_donnees_reference.sql` et exécuter

### Option 3: Via Django (après avoir créé les tables manuellement)

```bash
# Si les tables existent déjà
python manage.py init_donnees_reference
```

### Option 4: Requêtes individuelles

Ouvrir `requetes_individuelles.sql` et copier-coller les requêtes une par une selon vos besoins.

## 📊 Données insérées

### Types d'utilisateurs (6 types)
- `CLIENT` - Client standard
- `AGENT` - Agent de service
- `MARCHAND` - Commerçant
- `ADMIN` - Administrateur
- `SUPER_ADMIN` - Super administrateur
- `SYSTEME` - Compte système

### Niveaux KYC (4 niveaux)
- `0` - Non vérifié (0 BIF)
- `1` - Basique (50,000 BIF/jour, 100,000 BIF max)
- `2` - Complet (500,000 BIF/jour, 2,000,000 BIF max)
- `3` - Premium (5,000,000 BIF/jour, 20,000,000 BIF max)

### Statuts utilisateurs (5 statuts)
- `ACTIF` - Compte actif (connexion ✓, transactions ✓)
- `EN_VERIFICATION` - En vérification (connexion ✓, transactions ✗)
- `SUSPENDU` - Suspendu (connexion ✗, transactions ✗)
- `BLOQUE` - Bloqué (connexion ✗, transactions ✗)
- `FERME` - Fermé (connexion ✗, transactions ✗)

## ✅ Vérification

Après l'exécution, vérifier que les données sont bien insérées:

```sql
-- Compter les enregistrements
SELECT 
    (SELECT COUNT(*) FROM identite.types_utilisateurs) as nb_types,
    (SELECT COUNT(*) FROM identite.niveaux_kyc) as nb_niveaux,
    (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as nb_statuts;

-- Résultat attendu: nb_types=6, nb_niveaux=4, nb_statuts=5
```

## 🔍 Vérifier si les tables existent

```sql
-- Vérifier l'existence des tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'identite' 
  AND table_name IN ('types_utilisateurs', 'niveaux_kyc', 'statuts_utilisateurs');
```

## ⚠️ Notes importantes

1. **Ordre d'exécution**: Toujours créer les tables AVANT d'insérer les données
2. Les scripts utilisent `CREATE TABLE IF NOT EXISTS` et `ON CONFLICT DO UPDATE`
3. Vous pouvez exécuter les scripts plusieurs fois sans problème
4. Les données existantes seront mises à jour, pas dupliquées
5. Les `date_modification` seront automatiquement mises à jour

## 🔄 Ordre d'exécution complet

1. **Créer le schéma** (si pas déjà fait): `CREATE SCHEMA IF NOT EXISTS identite;`
2. **Créer les tables**: `create_tables_reference.sql`
3. **Insérer les données**: `init_donnees_reference.sql`
4. **Créer les utilisateurs**: Utiliser les endpoints Django

## 🛠️ Personnalisation

Pour modifier les limites KYC ou ajouter de nouveaux types:

1. Éditer le fichier SQL
2. Modifier les valeurs selon vos besoins
3. Ré-exécuter le script

Exemple pour modifier les limites du niveau KYC 1:

```sql
UPDATE identite.niveaux_kyc 
SET 
    limite_transaction_journaliere = 100000,
    limite_solde_maximum = 200000,
    date_modification = NOW()
WHERE niveau = 1;
```

## 🐛 Dépannage

### Erreur: "relation does not exist"
→ Les tables n'existent pas. Exécuter `create_tables_reference.sql` d'abord.

### Erreur: "permission denied"
→ Vérifier les permissions PostgreSQL de l'utilisateur `ufaranga`.

### Erreur: "schema does not exist"
→ Créer le schéma: `CREATE SCHEMA IF NOT EXISTS identite;`

## 📞 Support

En cas de problème:
1. Vérifier que le schéma `identite` existe
2. Vérifier que les tables sont créées
3. Vérifier les permissions PostgreSQL
4. Consulter les logs d'erreur
