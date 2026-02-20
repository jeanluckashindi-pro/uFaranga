# Tables de Référence - Module Identité

## Vue d'ensemble

Les statuts, types d'utilisateurs et niveaux KYC ont été normalisés dans des tables séparées pour une meilleure gestion et extensibilité.

## Structure des Tables

### 1. Types d'Utilisateurs (`identite.types_utilisateurs`)

Table de référence pour les différents types de comptes utilisateurs.

**Colonnes:**
- `code` (PK) : Code unique (ex: CLIENT, AGENT, MARCHAND)
- `libelle` : Nom affiché (ex: "Client", "Agent")
- `description` : Description détaillée du type
- `ordre_affichage` : Ordre d'affichage dans les listes
- `est_actif` : Si le type est actif
- `date_creation` : Date de création
- `date_modification` : Date de dernière modification

**Types disponibles:**
| Code | Libellé | Description |
|------|---------|-------------|
| CLIENT | Client | Client standard de la plateforme |
| AGENT | Agent | Agent de service (dépôt, retrait, etc.) |
| MARCHAND | Marchand | Commerçant acceptant les paiements |
| ADMIN | Administrateur | Administrateur de la plateforme |
| SUPER_ADMIN | Super Administrateur | Super administrateur avec tous les droits |
| SYSTEME | Système | Compte système pour les opérations automatiques |

### 2. Niveaux KYC (`identite.niveaux_kyc`)

Table de référence pour les niveaux de vérification KYC (Know Your Customer).

**Colonnes:**
- `niveau` (PK) : Niveau numérique (0, 1, 2, 3)
- `libelle` : Nom du niveau
- `description` : Description du niveau
- `limite_transaction_journaliere` : Limite de transaction par jour (BIF)
- `limite_solde_maximum` : Solde maximum autorisé (BIF)
- `documents_requis` : Liste JSON des documents requis
- `est_actif` : Si le niveau est actif
- `date_creation` : Date de création
- `date_modification` : Date de dernière modification

**Niveaux disponibles:**
| Niveau | Libellé | Limite Journalière | Solde Max | Documents Requis |
|--------|---------|-------------------|-----------|------------------|
| 0 | Non vérifié | 0 BIF | 0 BIF | Aucun |
| 1 | Basique | 50,000 BIF | 100,000 BIF | Téléphone, Email |
| 2 | Complet | 500,000 BIF | 2,000,000 BIF | Téléphone, Email, Pièce d'identité, Selfie |
| 3 | Premium | 5,000,000 BIF | 20,000,000 BIF | Téléphone, Email, Pièce d'identité, Selfie, Justificatif de domicile |

### 3. Statuts Utilisateurs (`identite.statuts_utilisateurs`)

Table de référence pour les statuts de compte utilisateur.

**Colonnes:**
- `code` (PK) : Code unique (ex: ACTIF, SUSPENDU)
- `libelle` : Nom affiché
- `description` : Description du statut
- `couleur` : Couleur hexadécimale pour l'affichage
- `permet_connexion` : Si l'utilisateur peut se connecter
- `permet_transactions` : Si l'utilisateur peut effectuer des transactions
- `ordre_affichage` : Ordre d'affichage
- `est_actif` : Si le statut est actif
- `date_creation` : Date de création
- `date_modification` : Date de dernière modification

**Statuts disponibles:**
| Code | Libellé | Couleur | Connexion | Transactions |
|------|---------|---------|-----------|--------------|
| ACTIF | Actif | 🟢 Vert | ✅ Oui | ✅ Oui |
| EN_VERIFICATION | En vérification | 🟡 Jaune | ✅ Oui | ❌ Non |
| SUSPENDU | Suspendu | 🟠 Orange | ❌ Non | ❌ Non |
| BLOQUE | Bloqué | 🔴 Rouge | ❌ Non | ❌ Non |
| FERME | Fermé | ⚫ Gris | ❌ Non | ❌ Non |

## Utilisation

### Initialisation des Données

Après avoir appliqué les migrations, initialisez les données de référence:

```bash
python manage.py init_donnees_reference
```

Cette commande crée toutes les entrées par défaut dans les trois tables.

### Création d'un Utilisateur

```python
from apps.identite.models import Utilisateur, TypeUtilisateur, NiveauKYC, StatutUtilisateur

# Récupérer les références
type_client = TypeUtilisateur.objects.get(code='CLIENT')
niveau_basique = NiveauKYC.objects.get(niveau=1)
statut_actif = StatutUtilisateur.objects.get(code='ACTIF')

# Créer l'utilisateur
utilisateur = Utilisateur.objects.create_user(
    courriel='jean@example.com',
    numero_telephone='+25762046725',
    mot_de_passe='MotDePasse123!',
    prenom='Jean',
    nom_famille='Dupont',
    date_naissance='1990-01-01',
    type_utilisateur=type_client,
    niveau_kyc=niveau_basique,
    statut=statut_actif
)
```

### Vérification des Permissions

```python
# Vérifier si l'utilisateur peut se connecter
if utilisateur.statut.permet_connexion:
    print("Connexion autorisée")

# Vérifier si l'utilisateur peut effectuer des transactions
if utilisateur.peut_effectuer_transactions():
    print("Transactions autorisées")

# Obtenir les limites KYC
limite_jour = utilisateur.niveau_kyc.limite_transaction_journaliere
limite_solde = utilisateur.niveau_kyc.limite_solde_maximum
```

### Changer le Statut d'un Utilisateur

```python
# Suspendre un utilisateur
statut_suspendu = StatutUtilisateur.objects.get(code='SUSPENDU')
utilisateur.statut = statut_suspendu
utilisateur.raison_statut = "Activité suspecte détectée"
utilisateur.save()
```

### Upgrade KYC

```python
# Passer au niveau KYC supérieur
niveau_complet = NiveauKYC.objects.get(niveau=2)
utilisateur.niveau_kyc = niveau_complet
utilisateur.date_validation_kyc = timezone.now()
utilisateur.save()
```

## Avantages de cette Architecture

1. **Extensibilité** : Facile d'ajouter de nouveaux types, niveaux ou statuts sans modifier le code
2. **Maintenance** : Modification des libellés, descriptions et paramètres sans migration
3. **Traçabilité** : Historique des modifications sur les tables de référence
4. **Validation** : Contraintes de clés étrangères garantissent l'intégrité
5. **Performance** : Index sur les clés étrangères pour des requêtes rapides
6. **Internationalisation** : Facile d'ajouter des traductions dans les tables de référence
7. **Business Logic** : Règles métier (limites, permissions) centralisées dans les tables

## Migration depuis l'Ancien Système

Si vous avez des données existantes avec les anciens CHOICES:

```python
# Script de migration (à exécuter une seule fois)
from apps.identite.models import Utilisateur, TypeUtilisateur, NiveauKYC, StatutUtilisateur

# Mapper les anciennes valeurs vers les nouvelles références
for utilisateur in Utilisateur.objects.all():
    # Type utilisateur
    if isinstance(utilisateur.type_utilisateur, str):
        type_obj = TypeUtilisateur.objects.get(code=utilisateur.type_utilisateur)
        utilisateur.type_utilisateur = type_obj
    
    # Niveau KYC
    if isinstance(utilisateur.niveau_kyc, int):
        niveau_obj = NiveauKYC.objects.get(niveau=utilisateur.niveau_kyc)
        utilisateur.niveau_kyc = niveau_obj
    
    # Statut
    if isinstance(utilisateur.statut, str):
        statut_obj = StatutUtilisateur.objects.get(code=utilisateur.statut)
        utilisateur.statut = statut_obj
    
    utilisateur.save()
```

## API REST

Les endpoints restent identiques, mais les réponses incluent maintenant les détails complets:

```json
{
  "id": "uuid",
  "courriel": "jean@example.com",
  "type_utilisateur": {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard de la plateforme"
  },
  "niveau_kyc": {
    "niveau": 1,
    "libelle": "Basique",
    "limite_transaction_journaliere": "50000.00",
    "limite_solde_maximum": "100000.00"
  },
  "statut": {
    "code": "ACTIF",
    "libelle": "Actif",
    "couleur": "#28a745",
    "permet_connexion": true,
    "permet_transactions": true
  }
}
```

## Notes Importantes

- Les tables de référence utilisent `on_delete=models.PROTECT` pour éviter la suppression accidentelle
- Les données de référence doivent être initialisées avant de créer des utilisateurs
- Les modifications des tables de référence sont tracées avec `date_modification`
- Le champ `est_actif` permet de désactiver temporairement un type/niveau/statut sans le supprimer
