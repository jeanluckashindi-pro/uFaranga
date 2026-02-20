# 🚀 LISEZ-MOI - Setup Module Identité

## ⚡ Démarrage Ultra-Rapide (2 minutes)

### 1️⃣ Exécuter le script SQL

```bash
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql
```

Mot de passe: `12345`

### 2️⃣ Redémarrer Django

```bash
python manage.py runserver
```

### 3️⃣ Tester la connexion

✅ L'erreur 500 devrait être résolue!

---

## 📚 Documentation Disponible

| Fichier | Description | Quand l'utiliser |
|---------|-------------|------------------|
| **INSTRUCTIONS_FINALES.md** | Guide étape par étape | Pour résoudre l'erreur de connexion |
| **RESUME_MODIFICATIONS.md** | Résumé de tous les changements | Pour comprendre ce qui a été fait |
| **FICHIERS_CREES.md** | Liste de tous les fichiers | Pour naviguer dans la documentation |
| **apps/identite/sql/INDEX.md** | Index des scripts SQL | Pour choisir le bon script |
| **apps/identite/sql/GUIDE_RAPIDE.md** | Guide rapide SQL | Pour démarrer rapidement |
| **apps/identite/REFACTORING_COMPLETE.md** | Documentation technique | Pour comprendre l'architecture |

---

## 🎯 Que Fait le Script?

Le script `setup_complet_avec_alter.sql` fait 3 choses:

### 1. Crée 3 Tables de Référence

- **types_utilisateurs**: CLIENT, AGENT, MARCHAND, ADMIN, SUPER_ADMIN, SYSTEME
- **niveaux_kyc**: 0 (Non vérifié), 1 (Basique), 2 (Complet), 3 (Premium)
- **statuts_utilisateurs**: ACTIF, EN_VERIFICATION, SUSPENDU, BLOQUE, FERME

### 2. Insère les Données

- 6 types d'utilisateurs
- 4 niveaux KYC avec limites de transaction
- 5 statuts avec couleurs et permissions

### 3. Modifie la Table Utilisateurs

- Transforme les colonnes simples en Foreign Keys
- Ajoute la validation automatique
- Permet l'accès aux informations riches (couleurs, limites, etc.)

---

## ✅ Vérification

Après l'exécution, vérifier:

```bash
psql -U ufaranga -d ufaranga -c "SELECT (SELECT COUNT(*) FROM identite.types_utilisateurs) as types, (SELECT COUNT(*) FROM identite.niveaux_kyc) as niveaux, (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as statuts;"
```

**Résultat attendu**: `types=6, niveaux=4, statuts=5`

---

## 🔧 Problèmes Courants

### "psql: command not found"

```bash
# Trouver psql
Get-ChildItem "C:\Program Files\PostgreSQL" -Recurse -Filter psql.exe

# Utiliser le chemin complet
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql
```

### "permission denied"

```sql
# Se connecter en tant que postgres
psql -U postgres -d ufaranga

# Donner les permissions
GRANT ALL PRIVILEGES ON SCHEMA identite TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA identite TO ufaranga;
```

### "relation does not exist"

```bash
# Créer le schéma
psql -U ufaranga -d ufaranga -c "CREATE SCHEMA IF NOT EXISTS identite;"

# Réexécuter le script
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql
```

---

## 📊 Données Créées

### Types d'Utilisateurs
- CLIENT - Client standard
- AGENT - Agent de service
- MARCHAND - Commerçant
- ADMIN - Administrateur
- SUPER_ADMIN - Super administrateur
- SYSTEME - Compte système

### Niveaux KYC
- Niveau 0: Non vérifié (0 BIF)
- Niveau 1: Basique (50,000 BIF/jour, 100,000 BIF max)
- Niveau 2: Complet (500,000 BIF/jour, 2,000,000 BIF max)
- Niveau 3: Premium (5,000,000 BIF/jour, 20,000,000 BIF max)

### Statuts
- ACTIF 🟢 - Connexion ✅, Transactions ✅
- EN_VERIFICATION 🟡 - Connexion ✅, Transactions ❌
- SUSPENDU 🟠 - Connexion ❌, Transactions ❌
- BLOQUE 🔴 - Connexion ❌, Transactions ❌
- FERME ⚫ - Connexion ❌, Transactions ❌

---

## 🎓 Pour Aller Plus Loin

### Consulter les données

```sql
# Types
SELECT * FROM identite.types_utilisateurs ORDER BY ordre_affichage;

# Niveaux KYC
SELECT * FROM identite.niveaux_kyc ORDER BY niveau;

# Statuts
SELECT * FROM identite.statuts_utilisateurs ORDER BY ordre_affichage;
```

### Ajouter un nouveau type

```sql
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage)
VALUES ('PARTENAIRE', 'Partenaire', 'Partenaire commercial', 7);
```

### Modifier les limites KYC

```sql
UPDATE identite.niveaux_kyc 
SET limite_transaction_journaliere = 100000
WHERE niveau = 1;
```

---

## 📞 Besoin d'Aide?

1. **Démarrage**: Lire `INSTRUCTIONS_FINALES.md`
2. **Comprendre**: Lire `RESUME_MODIFICATIONS.md`
3. **Référence SQL**: Consulter `apps/identite/sql/INDEX.md`
4. **Commandes**: Consulter `apps/identite/sql/COMMANDES_RAPIDES.md`
5. **Détails techniques**: Lire `apps/identite/REFACTORING_COMPLETE.md`

---

## 🎉 C'est Tout!

Après avoir exécuté le script et redémarré Django, votre application devrait fonctionner correctement.

**Bonne chance! 🚀**
