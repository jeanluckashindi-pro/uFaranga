# 📋 Refactoring Complet - Module Identité

## 🎯 Objectif

Normaliser les données de référence (types utilisateurs, niveaux KYC, statuts) dans des tables séparées au lieu d'utiliser des choix en dur dans le modèle.

## ✅ Ce qui a été fait

### 1. Nouveaux Modèles Django

Trois nouvelles tables de référence créées dans `apps/identite/models.py`:

#### `TypeUtilisateur`
- **Clé primaire**: `code` (VARCHAR)
- **Données**: CLIENT, AGENT, MARCHAND, ADMIN, SUPER_ADMIN, SYSTEME
- **Champs**: libelle, description, ordre_affichage, est_actif

#### `NiveauKYC`
- **Clé primaire**: `niveau` (INTEGER)
- **Données**: 0 (Non vérifié), 1 (Basique), 2 (Complet), 3 (Premium)
- **Champs**: libelle, description, limites de transaction/solde, documents_requis (JSON)

#### `StatutUtilisateur`
- **Clé primaire**: `code` (VARCHAR)
- **Données**: ACTIF, EN_VERIFICATION, SUSPENDU, BLOQUE, FERME
- **Champs**: libelle, description, couleur, permet_connexion, permet_transactions

### 2. Modèle Utilisateur Refactorisé

Le modèle `Utilisateur` a été modifié:

**AVANT** (choix en dur):
```python
type_utilisateur = models.CharField(max_length=20, choices=TYPE_CHOICES)
niveau_kyc = models.IntegerField(choices=KYC_CHOICES)
statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
```

**APRÈS** (relations ForeignKey):
```python
type_utilisateur = models.ForeignKey(TypeUtilisateur, on_delete=models.PROTECT)
niveau_kyc = models.ForeignKey(NiveauKYC, on_delete=models.PROTECT)
statut = models.ForeignKey(StatutUtilisateur, on_delete=models.PROTECT)
```

### 3. Scripts SQL Créés

Tous les scripts sont dans `apps/identite/sql/`:

| Fichier | Description |
|---------|-------------|
| `setup_complet.sql` ⭐ | Script tout-en-un (création + données) |
| `executer_setup.bat` | Script Windows pour exécution facile |
| `create_tables_reference.sql` | Création des tables uniquement |
| `init_donnees_reference.sql` | Insertion des données uniquement |
| `requetes_individuelles.sql` | Requêtes une par une |
| `GUIDE_RAPIDE.md` | Guide d'utilisation rapide |
| `README.md` | Documentation complète |

### 4. Commande Django

Commande de gestion créée: `apps/identite/management/commands/init_donnees_reference.py`

Usage:
```bash
python manage.py init_donnees_reference
```

### 5. Migrations Django

- `0002_niveaukyc_statututilisateur_typeutilisateur_and_more.py` - Création des tables
- `0003_init_donnees_reference.py` - Insertion des données

## 📊 Données de Référence

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

| Niveau | Libellé | Limite Journalière | Solde Max | Documents |
|--------|---------|-------------------|-----------|-----------|
| 0 | Non vérifié | 0 BIF | 0 BIF | Aucun |
| 1 | Basique | 50,000 BIF | 100,000 BIF | téléphone, email |
| 2 | Complet | 500,000 BIF | 2,000,000 BIF | + pièce d'identité, selfie |
| 3 | Premium | 5,000,000 BIF | 20,000,000 BIF | + justificatif domicile |

### Statuts Utilisateurs (5)

| Code | Libellé | Couleur | Connexion | Transactions |
|------|---------|---------|-----------|--------------|
| ACTIF | Actif | 🟢 #28a745 | ✅ | ✅ |
| EN_VERIFICATION | En vérification | 🟡 #ffc107 | ✅ | ❌ |
| SUSPENDU | Suspendu | 🟠 #fd7e14 | ❌ | ❌ |
| BLOQUE | Bloqué | 🔴 #dc3545 | ❌ | ❌ |
| FERME | Fermé | ⚫ #6c757d | ❌ | ❌ |

## 🚀 Installation

### Méthode 1: Script SQL (Recommandé)

```bash
# Depuis le dossier backend/
psql -U ufaranga -d ufaranga -f apps/identite/sql/setup_complet.sql
```

### Méthode 2: Script Windows

Double-cliquer sur `apps/identite/sql/executer_setup.bat`

### Méthode 3: Commande Django

```bash
# Après avoir créé les tables manuellement
python manage.py init_donnees_reference
```

## ✅ Vérification

```sql
-- Compter les enregistrements
SELECT 
    (SELECT COUNT(*) FROM identite.types_utilisateurs) as types,
    (SELECT COUNT(*) FROM identite.niveaux_kyc) as niveaux,
    (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as statuts;

-- Résultat attendu: types=6, niveaux=4, statuts=5
```

## 🔄 Impact sur le Code

### Avant
```python
# Accès direct à la valeur
if utilisateur.statut == 'ACTIF':
    # ...

if utilisateur.niveau_kyc >= 1:
    # ...
```

### Après
```python
# Accès via la relation
if utilisateur.statut.code == 'ACTIF':
    # ...

if utilisateur.niveau_kyc.niveau >= 1:
    # ...

# Nouveaux attributs disponibles
print(utilisateur.statut.libelle)  # "Actif"
print(utilisateur.statut.couleur)  # "#28a745"
print(utilisateur.statut.permet_connexion)  # True

print(utilisateur.niveau_kyc.limite_transaction_journaliere)  # 50000
print(utilisateur.niveau_kyc.documents_requis)  # ["telephone", "email"]
```

## 📈 Avantages

1. ✅ **Flexibilité**: Ajouter/modifier types sans changer le code
2. ✅ **Traçabilité**: Historique des modifications (date_modification)
3. ✅ **Richesse**: Plus d'informations (couleurs, limites, permissions)
4. ✅ **Maintenance**: Centralisation des données de référence
5. ✅ **Évolutivité**: Facile d'ajouter de nouveaux champs
6. ✅ **Internationalisation**: Possibilité d'ajouter des traductions

## 🔧 Maintenance

### Ajouter un nouveau type d'utilisateur

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

### Ajouter un nouveau statut

```sql
INSERT INTO identite.statuts_utilisateurs 
(code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage)
VALUES ('INACTIF', 'Inactif', 'Compte inactif', '#999999', false, false, 6);
```

## 📝 Notes Importantes

1. Les migrations Django ont été marquées comme `--fake` car les tables existent déjà
2. Les scripts SQL utilisent `ON CONFLICT DO UPDATE` pour éviter les doublons
3. Les relations utilisent `on_delete=models.PROTECT` pour éviter les suppressions accidentelles
4. Les champs texte `province` et `quartier` coexistent avec les FK `province_geo` et `quartier_geo`

## 🐛 Dépannage

### Erreur: "relation does not exist"
→ Exécuter `setup_complet.sql`

### Erreur: "column does not exist"
→ Redémarrer Django après avoir exécuté les scripts SQL

### Erreur: "permission denied"
→ Vérifier les permissions PostgreSQL de l'utilisateur `ufaranga`

## 📞 Support

Pour toute question ou problème:
1. Consulter `apps/identite/sql/GUIDE_RAPIDE.md`
2. Consulter `apps/identite/sql/README.md`
3. Vérifier les logs Django dans `logs/user-service.log`
