# 📚 Index des Fichiers SQL - Module Identité

## 🎯 Fichiers Principaux (À Utiliser)

### ⭐ `setup_complet_avec_alter.sql` - RECOMMANDÉ
**Usage:** Installation complète en 1 commande
```bash
psql -U ufaranga -d ufaranga -f setup_complet_avec_alter.sql
```
**Contenu:**
- Crée les 3 tables de référence
- Insère les données (6 types, 4 niveaux, 5 statuts)
- Modifie la table `utilisateurs` avec Foreign Keys

---

### `setup_complet.sql`
**Usage:** Installation sans modification de la table utilisateurs
```bash
psql -U ufaranga -d ufaranga -f setup_complet.sql
```
**Contenu:**
- Crée les 3 tables de référence
- Insère les données

---

## 📋 Fichiers Modulaires (Installation Étape par Étape)

### 1. `create_tables_reference.sql`
**Usage:** Créer uniquement les tables
```bash
psql -U ufaranga -d ufaranga -f create_tables_reference.sql
```
**Contenu:**
- CREATE TABLE types_utilisateurs
- CREATE TABLE niveaux_kyc
- CREATE TABLE statuts_utilisateurs
- Index et commentaires

---

### 2. `init_donnees_reference.sql`
**Usage:** Insérer uniquement les données
```bash
psql -U ufaranga -d ufaranga -f init_donnees_reference.sql
```
**Contenu:**
- INSERT 6 types d'utilisateurs
- INSERT 4 niveaux KYC
- INSERT 5 statuts utilisateurs

---

### 3. `alter_table_utilisateurs.sql`
**Usage:** Modifier la table utilisateurs
```bash
psql -U ufaranga -d ufaranga -f alter_table_utilisateurs.sql
```
**Contenu:**
- Sauvegarde des données existantes
- Suppression des anciennes colonnes
- Ajout des Foreign Keys
- Restauration des données
- Création des index

---

## 📖 Fichiers de Référence (Requêtes Individuelles)

### `requetes_individuelles.sql`
**Usage:** Copier-coller des requêtes une par une
**Contenu:**
- Requêtes INSERT individuelles pour chaque type
- Requêtes INSERT individuelles pour chaque niveau
- Requêtes INSERT individuelles pour chaque statut
- Requêtes de consultation
- Requêtes de mise à jour
- Requêtes de suppression

---

## 📚 Documentation

### `README.md`
Documentation complète avec:
- Instructions d'installation détaillées
- Explications des données
- Exemples d'utilisation
- Dépannage

### `GUIDE_RAPIDE.md`
Guide de démarrage rapide avec:
- Commandes essentielles
- Vérifications
- Dépannage rapide

### `EXPLICATION_ALTER.md`
Explication détaillée de la modification de la table utilisateurs:
- Avant/Après
- Étapes détaillées
- Exemples concrets
- Avantages

### `COMMANDES_RAPIDES.md`
Référence rapide des commandes:
- Installation
- Vérification
- Consultation
- Maintenance
- Dépannage

### `INDEX.md` (ce fichier)
Index de tous les fichiers disponibles

---

## 🔧 Fichiers Utilitaires

### `executer_setup.bat`
Script Windows pour exécution facile
```cmd
executer_setup.bat
```

---

## 🗂️ Structure Complète

```
apps/identite/sql/
├── 📄 setup_complet_avec_alter.sql  ⭐ RECOMMANDÉ
├── 📄 setup_complet.sql
├── 📄 create_tables_reference.sql
├── 📄 init_donnees_reference.sql
├── 📄 alter_table_utilisateurs.sql
├── 📄 requetes_individuelles.sql
├── 📄 executer_setup.bat
├── 📖 README.md
├── 📖 GUIDE_RAPIDE.md
├── 📖 EXPLICATION_ALTER.md
├── 📖 COMMANDES_RAPIDES.md
└── 📖 INDEX.md (ce fichier)
```

---

## 🎯 Quel Fichier Utiliser?

### Cas 1: Nouvelle Installation
→ `setup_complet_avec_alter.sql` ⭐

### Cas 2: Tables déjà créées, besoin de données
→ `init_donnees_reference.sql`

### Cas 3: Données déjà insérées, besoin de modifier utilisateurs
→ `alter_table_utilisateurs.sql`

### Cas 4: Installation progressive
→ `create_tables_reference.sql` puis `init_donnees_reference.sql` puis `alter_table_utilisateurs.sql`

### Cas 5: Besoin de requêtes spécifiques
→ `requetes_individuelles.sql`

---

## 📊 Données Insérées

### Types d'Utilisateurs (6)
| Code | Libellé | Description |
|------|---------|-------------|
| CLIENT | Client | Client standard de la plateforme |
| AGENT | Agent | Agent de service (dépôt, retrait, etc.) |
| MARCHAND | Marchand | Commerçant acceptant les paiements |
| ADMIN | Administrateur | Administrateur de la plateforme |
| SUPER_ADMIN | Super Administrateur | Super administrateur avec tous les droits |
| SYSTEME | Système | Compte système pour les opérations automatiques |

### Niveaux KYC (4)
| Niveau | Libellé | Limite Journalière | Solde Max |
|--------|---------|-------------------|-----------|
| 0 | Non vérifié | 0 BIF | 0 BIF |
| 1 | Basique | 50,000 BIF | 100,000 BIF |
| 2 | Complet | 500,000 BIF | 2,000,000 BIF |
| 3 | Premium | 5,000,000 BIF | 20,000,000 BIF |

### Statuts Utilisateurs (5)
| Code | Libellé | Couleur | Connexion | Transactions |
|------|---------|---------|-----------|--------------|
| ACTIF | Actif | 🟢 #28a745 | ✅ | ✅ |
| EN_VERIFICATION | En vérification | 🟡 #ffc107 | ✅ | ❌ |
| SUSPENDU | Suspendu | 🟠 #fd7e14 | ❌ | ❌ |
| BLOQUE | Bloqué | 🔴 #dc3545 | ❌ | ❌ |
| FERME | Fermé | ⚫ #6c757d | ❌ | ❌ |

---

## 🚀 Démarrage Rapide

```bash
# 1. Installation complète
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet_avec_alter.sql

# 2. Vérification
psql -U ufaranga -d ufaranga -c "SELECT (SELECT COUNT(*) FROM identite.types_utilisateurs) as types, (SELECT COUNT(*) FROM identite.niveaux_kyc) as niveaux, (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as statuts;"

# 3. Redémarrer Django
python manage.py runserver
```

---

## 📞 Besoin d'Aide?

1. Consulter `GUIDE_RAPIDE.md` pour démarrer
2. Consulter `README.md` pour la documentation complète
3. Consulter `EXPLICATION_ALTER.md` pour comprendre la modification
4. Consulter `COMMANDES_RAPIDES.md` pour les commandes utiles
