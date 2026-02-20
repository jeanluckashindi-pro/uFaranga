# 📖 Explication: Modification de la Table Utilisateurs

## 🎯 Objectif

Transformer les colonnes simples de la table `utilisateurs` en relations (Foreign Keys) vers les tables de référence.

## 📊 Avant / Après

### AVANT (Colonnes simples)

```sql
CREATE TABLE identite.utilisateurs (
    id UUID PRIMARY KEY,
    courriel VARCHAR(255),
    -- ...
    type_utilisateur VARCHAR(20),      -- Valeur en dur: 'CLIENT', 'AGENT'
    niveau_kyc INTEGER,                -- Valeur en dur: 0, 1, 2, 3
    statut VARCHAR(20)                 -- Valeur en dur: 'ACTIF', 'SUSPENDU'
);
```

**Problèmes:**
- ❌ Pas de validation (on peut mettre n'importe quoi)
- ❌ Pas d'informations supplémentaires (couleur, limites, etc.)
- ❌ Difficile de modifier les libellés

### APRÈS (Foreign Keys)

```sql
CREATE TABLE identite.utilisateurs (
    id UUID PRIMARY KEY,
    courriel VARCHAR(255),
    -- ...
    type_utilisateur VARCHAR(20) REFERENCES identite.types_utilisateurs(code),
    niveau_kyc INTEGER REFERENCES identite.niveaux_kyc(niveau),
    statut VARCHAR(20) REFERENCES identite.statuts_utilisateurs(code)
);
```

**Avantages:**
- ✅ Validation automatique (seules les valeurs existantes sont acceptées)
- ✅ Accès aux informations riches (couleur, limites, permissions)
- ✅ Modification centralisée des libellés

## 🔄 Étapes de la Modification

### Étape 1: Vérification

```sql
-- Vérifier que les tables de référence existent et contiennent des données
SELECT COUNT(*) FROM identite.types_utilisateurs;  -- Doit retourner 6
SELECT COUNT(*) FROM identite.niveaux_kyc;         -- Doit retourner 4
SELECT COUNT(*) FROM identite.statuts_utilisateurs; -- Doit retourner 5
```

**Pourquoi?** On ne peut pas créer de Foreign Key vers une table vide.

### Étape 2: Sauvegarde

```sql
-- Créer des colonnes temporaires
ALTER TABLE identite.utilisateurs 
ADD COLUMN type_utilisateur_old VARCHAR(20),
ADD COLUMN niveau_kyc_old INTEGER,
ADD COLUMN statut_old VARCHAR(20);

-- Copier les valeurs actuelles
UPDATE identite.utilisateurs 
SET 
    type_utilisateur_old = type_utilisateur,
    niveau_kyc_old = niveau_kyc,
    statut_old = statut;
```

**Pourquoi?** Pour ne pas perdre les données existantes.

**Exemple:**
```
Avant:
id | type_utilisateur | niveau_kyc | statut
---+------------------+------------+--------
1  | CLIENT           | 1          | ACTIF

Après sauvegarde:
id | type_utilisateur | niveau_kyc | statut | type_old | kyc_old | statut_old
---+------------------+------------+--------+----------+---------+------------
1  | CLIENT           | 1          | ACTIF  | CLIENT   | 1       | ACTIF
```

### Étape 3: Suppression

```sql
-- Supprimer les anciennes colonnes
ALTER TABLE identite.utilisateurs 
DROP COLUMN type_utilisateur CASCADE,
DROP COLUMN niveau_kyc CASCADE,
DROP COLUMN statut CASCADE;
```

**Pourquoi?** On ne peut pas changer le type d'une colonne existante en Foreign Key directement.

**Résultat:**
```
id | type_old | kyc_old | statut_old
---+----------+---------+------------
1  | CLIENT   | 1       | ACTIF
```

### Étape 4: Création avec Foreign Keys

```sql
-- Ajouter les nouvelles colonnes avec Foreign Keys
ALTER TABLE identite.utilisateurs 
ADD COLUMN type_utilisateur VARCHAR(20) 
    REFERENCES identite.types_utilisateurs(code) ON DELETE RESTRICT,
ADD COLUMN niveau_kyc INTEGER 
    REFERENCES identite.niveaux_kyc(niveau) ON DELETE RESTRICT,
ADD COLUMN statut VARCHAR(20) 
    REFERENCES identite.statuts_utilisateurs(code) ON DELETE RESTRICT;
```

**Explication des options:**

- `REFERENCES identite.types_utilisateurs(code)`: Crée la relation
- `ON DELETE RESTRICT`: Empêche la suppression d'un type si des utilisateurs l'utilisent

**Résultat:**
```
id | type_utilisateur | niveau_kyc | statut | type_old | kyc_old | statut_old
---+------------------+------------+--------+----------+---------+------------
1  | NULL             | NULL       | NULL   | CLIENT   | 1       | ACTIF
```

### Étape 5: Restauration

```sql
-- Restaurer les valeurs depuis les colonnes temporaires
UPDATE identite.utilisateurs 
SET 
    type_utilisateur = COALESCE(type_utilisateur_old, 'CLIENT'),
    niveau_kyc = COALESCE(niveau_kyc_old, 0),
    statut = COALESCE(statut_old, 'ACTIF');
```

**Explication:**
- `COALESCE(valeur, defaut)`: Utilise `valeur` si elle existe, sinon `defaut`

**Résultat:**
```
id | type_utilisateur | niveau_kyc | statut | type_old | kyc_old | statut_old
---+------------------+------------+--------+----------+---------+------------
1  | CLIENT           | 1          | ACTIF  | CLIENT   | 1       | ACTIF
```

### Étape 6: Contraintes

```sql
-- Définir les valeurs par défaut
ALTER TABLE identite.utilisateurs 
ALTER COLUMN type_utilisateur SET DEFAULT 'CLIENT',
ALTER COLUMN niveau_kyc SET DEFAULT 0,
ALTER COLUMN statut SET DEFAULT 'ACTIF';

-- Rendre les colonnes obligatoires
ALTER TABLE identite.utilisateurs 
ALTER COLUMN type_utilisateur SET NOT NULL,
ALTER COLUMN niveau_kyc SET NOT NULL,
ALTER COLUMN statut SET NOT NULL;
```

**Pourquoi?**
- `DEFAULT`: Valeur automatique pour les nouveaux utilisateurs
- `NOT NULL`: Empêche les valeurs vides

### Étape 7: Index

```sql
-- Créer des index pour améliorer les performances
CREATE INDEX idx_utilisateurs_type ON identite.utilisateurs(type_utilisateur);
CREATE INDEX idx_utilisateurs_niveau_kyc ON identite.utilisateurs(niveau_kyc);
CREATE INDEX idx_utilisateurs_statut ON identite.utilisateurs(statut);
```

**Pourquoi?** Accélère les requêtes comme:
```sql
SELECT * FROM utilisateurs WHERE statut = 'ACTIF';
SELECT * FROM utilisateurs WHERE niveau_kyc >= 2;
```

### Étape 8: Nettoyage

```sql
-- Supprimer les colonnes temporaires
ALTER TABLE identite.utilisateurs 
DROP COLUMN type_utilisateur_old,
DROP COLUMN niveau_kyc_old,
DROP COLUMN statut_old;
```

**Résultat final:**
```
id | type_utilisateur | niveau_kyc | statut
---+------------------+------------+--------
1  | CLIENT           | 1          | ACTIF
```

## 🔍 Validation des Foreign Keys

### Test 1: Insertion valide

```sql
-- ✅ Fonctionne (CLIENT existe dans types_utilisateurs)
INSERT INTO identite.utilisateurs (courriel, type_utilisateur, niveau_kyc, statut)
VALUES ('test@example.com', 'CLIENT', 1, 'ACTIF');
```

### Test 2: Insertion invalide

```sql
-- ❌ Erreur: type 'INVALIDE' n'existe pas
INSERT INTO identite.utilisateurs (courriel, type_utilisateur, niveau_kyc, statut)
VALUES ('test@example.com', 'INVALIDE', 1, 'ACTIF');

-- Erreur: insert or update on table "utilisateurs" violates foreign key constraint
```

### Test 3: Suppression protégée

```sql
-- ❌ Erreur: impossible de supprimer un type utilisé
DELETE FROM identite.types_utilisateurs WHERE code = 'CLIENT';

-- Erreur: update or delete on table "types_utilisateurs" violates foreign key constraint
```

## 📈 Utilisation dans les Requêtes

### Avant (colonnes simples)

```sql
-- Récupérer les utilisateurs actifs
SELECT * FROM identite.utilisateurs WHERE statut = 'ACTIF';

-- Pas d'accès aux informations supplémentaires
```

### Après (avec Foreign Keys)

```sql
-- Récupérer les utilisateurs actifs avec toutes les infos
SELECT 
    u.*,
    tu.libelle as type_libelle,
    nk.libelle as niveau_libelle,
    nk.limite_transaction_journaliere,
    su.libelle as statut_libelle,
    su.couleur as statut_couleur,
    su.permet_connexion,
    su.permet_transactions
FROM identite.utilisateurs u
JOIN identite.types_utilisateurs tu ON u.type_utilisateur = tu.code
JOIN identite.niveaux_kyc nk ON u.niveau_kyc = nk.niveau
JOIN identite.statuts_utilisateurs su ON u.statut = su.code
WHERE su.code = 'ACTIF';
```

**Résultat:**
```
id | courriel | type_libelle | niveau_libelle | limite_journaliere | statut_libelle | couleur  | permet_connexion
---+----------+--------------+----------------+--------------------+----------------+----------+-----------------
1  | test@... | Client       | Basique        | 50000.00           | Actif          | #28a745  | true
```

## 🎯 Avantages Concrets

### 1. Validation Automatique

```sql
-- ❌ AVANT: Accepte n'importe quoi
UPDATE utilisateurs SET statut = 'TYPO_ERROR' WHERE id = 1;  -- Pas d'erreur!

-- ✅ APRÈS: Validation automatique
UPDATE utilisateurs SET statut = 'TYPO_ERROR' WHERE id = 1;  -- Erreur FK!
```

### 2. Informations Riches

```python
# AVANT
if utilisateur.statut == 'ACTIF':
    print("Actif")  # Juste le code

# APRÈS
if utilisateur.statut.code == 'ACTIF':
    print(utilisateur.statut.libelle)  # "Actif"
    print(utilisateur.statut.couleur)  # "#28a745"
    if utilisateur.statut.permet_connexion:
        # Autoriser la connexion
```

### 3. Modification Centralisée

```sql
-- Changer le libellé pour TOUS les utilisateurs
UPDATE identite.statuts_utilisateurs 
SET libelle = 'Compte Actif' 
WHERE code = 'ACTIF';

-- Tous les utilisateurs voient le nouveau libellé automatiquement
```

## ⚠️ Points d'Attention

### 1. Données Existantes

Si vous avez des utilisateurs avec des valeurs invalides:

```sql
-- Trouver les valeurs invalides
SELECT DISTINCT type_utilisateur 
FROM identite.utilisateurs 
WHERE type_utilisateur NOT IN (SELECT code FROM identite.types_utilisateurs);

-- Les corriger AVANT d'exécuter le script
UPDATE identite.utilisateurs 
SET type_utilisateur = 'CLIENT' 
WHERE type_utilisateur NOT IN (SELECT code FROM identite.types_utilisateurs);
```

### 2. Performance

Les Foreign Keys ajoutent une légère surcharge:
- ✅ Validation à chaque INSERT/UPDATE
- ✅ Vérification à chaque DELETE

Mais les index compensent largement!

### 3. Cascade

`ON DELETE RESTRICT` empêche la suppression accidentelle:

```sql
-- Si vous voulez vraiment supprimer un type
-- 1. D'abord, réassigner les utilisateurs
UPDATE identite.utilisateurs SET type_utilisateur = 'CLIENT' WHERE type_utilisateur = 'ANCIEN_TYPE';

-- 2. Ensuite, supprimer le type
DELETE FROM identite.types_utilisateurs WHERE code = 'ANCIEN_TYPE';
```

## 📞 Résumé

Le script `alter_table_utilisateurs.sql`:
1. ✅ Sauvegarde les données existantes
2. ✅ Supprime les anciennes colonnes
3. ✅ Crée les nouvelles colonnes avec Foreign Keys
4. ✅ Restaure les données
5. ✅ Ajoute les contraintes et index
6. ✅ Nettoie les colonnes temporaires

**Résultat**: Table `utilisateurs` normalisée avec validation automatique et accès aux informations riches!
