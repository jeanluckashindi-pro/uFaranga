# 📊 Guide de Peuplement SQL Direct

## 🎯 Objectif

Peupler la base de données PostgreSQL directement avec des scripts SQL, sans passer par Django.

## 📁 Fichiers Créés

### Scripts SQL (2 fichiers)

1. **peupler_localisation_sql.sql** - Peuple les pays africains
   - Ajoute les colonnes `continent` et `sous_region`
   - Insère 19 pays africains avec métadonnées
   - Crée les index

2. **peupler_provinces_sql.sql** - Peuple les provinces
   - Insère 68+ provinces pour les 19 pays
   - Utilise `ON CONFLICT DO NOTHING` pour éviter les doublons

### Scripts d'Exécution (2 fichiers)

3. **executer_peuplement.bat** - Pour Windows
4. **executer_peuplement.sh** - Pour Linux/Mac

---

## 🚀 Méthode 1: Utiliser le Script Batch (Windows)

### Étape 1: Ouvrir le Terminal

```cmd
cd D:\Projets\Decima Techno\uFaranga\backend
```

### Étape 2: Exécuter le Script

```cmd
executer_peuplement.bat
```

Le script va:
1. Vérifier que `psql` est disponible
2. Exécuter `peupler_localisation_sql.sql`
3. Exécuter `peupler_provinces_sql.sql`
4. Afficher les statistiques

### Output Attendu

```
============================================================================
PEUPLEMENT DE LA BASE DE DONNEES UFARANGA
============================================================================

Configuration:
  Utilisateur: ufaranga
  Base: ufaranga
  Host: localhost:5432

============================================================================
ETAPE 1: Peupler les pays africains
============================================================================

BEGIN
ALTER TABLE
ALTER TABLE
CREATE INDEX
CREATE INDEX
COMMIT
BEGIN
INSERT 0 1
INSERT 0 1
...
COMMIT

============================================================================
ETAPE 2: Peupler les provinces
============================================================================

BEGIN
INSERT 0 17
INSERT 0 5
...
COMMIT

============================================================================
VERIFICATION
============================================================================

 continent | sous_region        | nb_pays
-----------+--------------------+---------
 Afrique   | Afrique Australe   |       1
 Afrique   | Afrique Centrale   |       5
 Afrique   | Afrique de l'Est   |       5
 Afrique   | Afrique de l'Ouest |       4
 Afrique   | Afrique du Nord    |       4

============================================================================
PEUPLEMENT TERMINE AVEC SUCCES!
============================================================================
```

---

## 🐧 Méthode 2: Utiliser le Script Shell (Linux/Mac)

### Étape 1: Rendre le Script Exécutable

```bash
chmod +x executer_peuplement.sh
```

### Étape 2: Exécuter le Script

```bash
./executer_peuplement.sh
```

---

## 🔧 Méthode 3: Exécution Manuelle

### Étape 1: Se Connecter à PostgreSQL

```bash
psql -U ufaranga -d ufaranga
```

Mot de passe: `12345`

### Étape 2: Exécuter les Scripts

```sql
-- Dans psql
\i peupler_localisation_sql.sql
\i peupler_provinces_sql.sql
```

Ou depuis le terminal:

```bash
psql -U ufaranga -d ufaranga -f peupler_localisation_sql.sql
psql -U ufaranga -d ufaranga -f peupler_provinces_sql.sql
```

---

## ✅ Vérification

### 1. Vérifier les Colonnes

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'localisation'
AND table_name = 'pays'
AND column_name IN ('continent', 'sous_region');
```

**Résultat Attendu:**
```
 column_name | data_type
-------------+-------------------
 continent   | character varying
 sous_region | character varying
```

### 2. Vérifier les Pays

```sql
SELECT code_iso_2, nom, continent, sous_region
FROM localisation.pays
WHERE continent = 'Afrique'
ORDER BY sous_region, nom;
```

**Résultat Attendu:** 19 pays africains

### 3. Vérifier les Provinces

```sql
SELECT 
    pays.nom as pays,
    COUNT(provinces.id) as nb_provinces
FROM localisation.pays pays
LEFT JOIN localisation.provinces provinces ON provinces.pays_id = pays.id
WHERE pays.continent = 'Afrique'
GROUP BY pays.nom
ORDER BY nb_provinces DESC;
```

**Résultat Attendu:**
```
 pays                              | nb_provinces
-----------------------------------+--------------
 Burundi                           |           17
 RD Congo                          |            8
 Rwanda                            |            5
 ...
```

### 4. Statistiques par Sous-Région

```sql
SELECT 
    sous_region,
    COUNT(*) as nb_pays
FROM localisation.pays
WHERE continent = 'Afrique'
GROUP BY sous_region
ORDER BY nb_pays DESC;
```

**Résultat Attendu:**
```
 sous_region           | nb_pays
-----------------------+---------
 Afrique de l'Est      |       5
 Afrique Centrale      |       5
 Afrique de l'Ouest    |       4
 Afrique du Nord       |       4
 Afrique Australe      |       1
```

### 5. Tester l'API

```bash
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique
```

---

## 🐛 Dépannage

### Erreur: psql Not Found

**Problème:**
```
'psql' n'est pas reconnu en tant que commande interne
```

**Solution Windows:**
1. Ajouter PostgreSQL au PATH:
   ```
   C:\Program Files\PostgreSQL\15\bin
   ```
2. Ou utiliser le chemin complet:
   ```cmd
   "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U ufaranga -d ufaranga -f peupler_localisation_sql.sql
   ```

### Erreur: Password Authentication Failed

**Problème:**
```
psql: FATAL: password authentication failed for user "ufaranga"
```

**Solution:**
1. Vérifier le mot de passe dans le script (12345)
2. Ou créer un fichier `.pgpass`:
   ```
   localhost:5432:ufaranga:ufaranga:12345
   ```

### Erreur: Permission Denied

**Problème:**
```
ERROR: permission denied for schema localisation
```

**Solution:**
```sql
-- Se connecter en tant que postgres
psql -U postgres -d ufaranga

-- Donner les droits
GRANT ALL PRIVILEGES ON SCHEMA localisation TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA localisation TO ufaranga;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA localisation TO ufaranga;
```

### Erreur: Column Already Exists

**Problème:**
```
ERROR: column "continent" of relation "pays" already exists
```

**Solution:** C'est normal! Le script utilise `ADD COLUMN IF NOT EXISTS`. Continuez.

### Erreur: Duplicate Key

**Problème:**
```
ERROR: duplicate key value violates unique constraint "pays_code_iso_2_key"
```

**Solution:** C'est normal! Le script utilise `ON CONFLICT DO UPDATE`. Les données sont mises à jour.

---

## 📊 Données Insérées

### Pays (19 pays)

**Afrique de l'Est (5):**
- Burundi (BI)
- Rwanda (RW)
- Kenya (KE)
- Tanzanie (TZ)
- Ouganda (UG)

**Afrique Centrale (5):**
- RD Congo (CD)
- Congo (CG)
- Cameroun (CM)
- Gabon (GA)
- RCA (CF)

**Afrique de l'Ouest (4):**
- Sénégal (SN)
- Côte d'Ivoire (CI)
- Ghana (GH)
- Nigeria (NG)

**Afrique du Nord (4):**
- Maroc (MA)
- Algérie (DZ)
- Tunisie (TN)
- Égypte (EG)

**Afrique Australe (1):**
- Afrique du Sud (ZA)

### Provinces (68+ provinces)

Chaque pays a ses provinces principales. Voir le script `peupler_provinces_sql.sql` pour la liste complète.

---

## 🔄 Rollback

### Supprimer les Provinces

```sql
DELETE FROM localisation.provinces
WHERE pays_id IN (
    SELECT id FROM localisation.pays WHERE continent = 'Afrique'
);
```

### Supprimer les Pays

```sql
DELETE FROM localisation.pays WHERE continent = 'Afrique';
```

### Supprimer les Colonnes

```sql
ALTER TABLE localisation.pays DROP COLUMN IF EXISTS continent;
ALTER TABLE localisation.pays DROP COLUMN IF EXISTS sous_region;
```

---

## 🎯 Prochaines Étapes

Après avoir exécuté les scripts SQL:

### 1. Ajouter des Districts et Quartiers

```bash
python ajouter_districts_quartiers.py
```

### 2. Générer un Rapport

```bash
python generer_rapport_geo.py
```

### 3. Tester l'API

```bash
# Tous les pays africains
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique

# Pays d'Afrique de l'Est
curl "http://127.0.0.1:8000/api/v1/localisation/pays/?sous_region=Afrique%20de%20l'Est"

# Provinces du Burundi
curl http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=<uuid_burundi>
```

---

## 📝 Notes Importantes

1. **Idempotent:** Les scripts peuvent être exécutés plusieurs fois sans problème
2. **Transactions:** Tout est dans des transactions (BEGIN/COMMIT)
3. **Sécurisé:** Utilise `ON CONFLICT` pour éviter les doublons
4. **Rapide:** Prend environ 5-10 secondes
5. **Pas de Django:** Fonctionne directement avec PostgreSQL

---

## ✅ Checklist

- [ ] PostgreSQL installé et accessible
- [ ] Utilisateur `ufaranga` existe avec mot de passe `12345`
- [ ] Base de données `ufaranga` existe
- [ ] Schema `localisation` existe
- [ ] Tables `pays` et `provinces` existent
- [ ] Scripts SQL téléchargés
- [ ] Script batch/shell exécuté
- [ ] Vérifications effectuées
- [ ] API testée

---

**✅ Peuplement SQL prêt à l'emploi!** 🚀

**Commande Rapide:**
```cmd
executer_peuplement.bat
```
