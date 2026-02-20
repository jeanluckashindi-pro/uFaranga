# Grand Livre Automatique - Documentation Complète

**Date**: 2026-02-20  
**Statut**: ✅ ACTIF  
**Niveau**: PRÉCISION ET VIGILANCE EXTRÊME

---

## 📋 Vue d'ensemble

Le grand livre comptable enregistre AUTOMATIQUEMENT toutes les opérations financières avec une précision et une vigilance extrême. Chaque transaction, chaque modification de solde, chaque opération fiscale est tracée de manière immuable.

---

## 🎯 Fonctionnement Automatique

### Déclencheurs Automatiques

#### 1. Transaction Validée ou Annulée
**Trigger**: `trigger_grand_livre_transaction`  
**Table**: `transaction.transactions`  
**Quand**: APRÈS INSERT ou UPDATE  
**Condition**: Statut = 'VALIDEE' ou 'ANNULEE'

**Ce qui est enregistré automatiquement:**

✅ **Écriture DÉBIT** (compte source)
- Numéro d'écriture unique: ECR + YYYYMM + séquence + '-D'
- Montant total (montant + frais)
- Solde AVANT et APRÈS
- Compte contrepartie (destination)
- Classification comptable automatique
- Hash d'intégrité SHA-256

✅ **Écriture CRÉDIT** (compte destination)
- Numéro d'écriture unique: ECR + YYYYMM + séquence + '-C'
- Montant (sans frais)
- Solde AVANT et APRÈS
- Compte contrepartie (source)
- Classification comptable automatique
- Hash d'intégrité SHA-256

✅ **Écriture FRAIS** (si frais > 0)
- Numéro d'écriture unique: ECR + YYYYMM + séquence + '-F'
- Montant des frais
- Catégorie: FRAIS_BANCAIRES
- Sous-catégorie: FRAIS_[TYPE_TRANSACTION]
- Hash d'intégrité SHA-256

#### 2. Modification de Solde
**Trigger**: `trigger_grand_livre_solde`  
**Table**: `portefeuille.comptes`  
**Quand**: APRÈS UPDATE  
**Condition**: Solde actuel modifié

**Ce qui est enregistré:**
- Type: AJUSTEMENT_SOLDE
- Sens: DÉBIT ou CRÉDIT selon variation
- Montant: Différence absolue
- Solde AVANT et APRÈS
- Raison: Ajustement automatique

#### 3. Vérification Avant Insertion
**Trigger**: `trigger_verifier_coherence`  
**Table**: `ledger.ecritures_comptables`  
**Quand**: AVANT INSERT

**Vérifications effectuées:**
- ✅ Cohérence du solde (solde_après = solde_avant ± montant)
- ✅ Hash d'intégrité présent et valide (64 caractères)
- ✅ Utilisateur renseigné (qui_utilisateur_id)
- ✅ Description de l'action présente (quoi)

**Si erreur**: Transaction annulée avec message explicite

---

## 📊 Traçabilité Extrême

Chaque écriture comptable contient:

### Identification
- `numero_ecriture` - Numéro unique (ECR + YYYYMM + séquence)
- `transaction_id` - Lien vers transaction
- `reference_transaction` - Référence externe
- `type_transaction` - Type d'opération

### Comptabilité
- `compte_id` - Compte concerné
- `numero_compte` - Numéro du compte
- `sens` - DEBIT ou CREDIT
- `montant` - Montant de l'opération
- `devise` - Devise
- `solde_avant` - Solde AVANT opération
- `solde_apres` - Solde APRÈS opération
- `compte_contrepartie_id` - Compte contrepartie (double entrée)

### Classification
- `categorie_comptable` - Catégorie (ENCAISSEMENT, DECAISSEMENT, VIREMENT, etc.)
- `sous_categorie` - Sous-catégorie (type transaction)
- `code_analytique` - Code analytique (optionnel)
- `centre_cout` - Centre de coût (optionnel)

### Période
- `exercice_comptable` - Année (YYYY)
- `periode_comptable` - Période (YYYY-MM)
- `date_comptable` - Date comptable
- `date_valeur` - Date de valeur

### Traçabilité QUI
- `qui_utilisateur_id` - UUID utilisateur
- `qui_nom` - Nom utilisateur
- `qui_type` - Type utilisateur (CLIENT, AGENT, etc.)
- `qui_role` - Rôle utilisateur

### Traçabilité QUAND
- `quand` - Timestamp précis
- `cree_le` - Date création

### Traçabilité QUOI
- `quoi` - Description détaillée de l'action

### Traçabilité COMMENT
- `comment` - Moyen (WEB, API, MOBILE, SYSTEME, ADMIN, BATCH)

### Traçabilité POURQUOI
- `pourquoi` - Raison/commentaire

### Contexte Technique
- `adresse_ip` - Adresse IP
- `user_agent` - User agent
- `device_id` - Identifiant device
- `session_id` - ID session
- `request_id` - ID requête
- `correlation_id` - ID corrélation (traçabilité distribuée)

### Géolocalisation
- `pays` - Code pays (ISO 2)
- `ville` - Ville
- `latitude` - Latitude
- `longitude` - Longitude

### Sécurité
- `statut` - VALIDEE, ANNULEE, CORRIGEE
- `hash_integrite` - Hash SHA-256 pour vérification intégrité
- `metadonnees` - Métadonnées JSON

---

## 🔧 Fonctions Utilitaires

### 1. Vérifier Intégrité du Grand Livre

```sql
SELECT * FROM ledger.verifier_integrite_grand_livre(
    '2026-01-01'::DATE,  -- Date début
    '2026-12-31'::DATE   -- Date fin
);
```

**Retourne:**
- `total_ecritures` - Nombre total d'écritures
- `total_debits` - Somme des débits
- `total_credits` - Somme des crédits
- `difference` - Différence (doit être ~0)
- `est_equilibre` - TRUE si équilibré
- `ecritures_sans_hash` - Nombre d'écritures sans hash (doit être 0)
- `ecritures_incoherentes` - Nombre d'écritures incohérentes (doit être 0)
- `message` - Message de statut

**Exemple de résultat:**
```
total_ecritures | total_debits | total_credits | difference | est_equilibre | ecritures_sans_hash | ecritures_incoherentes | message
1250            | 15000000.00  | 15000000.00   | 0.00       | true          | 0                   | 0                      | Grand livre équilibré ✓
```

### 2. Statistiques du Grand Livre

```sql
SELECT * FROM ledger.statistiques_grand_livre('2026-02');
```

**Retourne:**
- `periode` - Période (YYYY-MM)
- `nombre_ecritures` - Nombre d'écritures
- `nombre_transactions` - Nombre de transactions distinctes
- `volume_debits` - Volume total débits
- `volume_credits` - Volume total crédits
- `nombre_comptes_actifs` - Nombre de comptes actifs
- `categories` - Répartition par catégorie (JSON)

### 3. Générer Numéro d'Écriture

```sql
SELECT ledger.generer_numero_ecriture();
-- Résultat: ECR20260200000123
```

---

## 📈 Vues de Contrôle

### 1. Soldes selon le Grand Livre

```sql
SELECT * FROM ledger.vue_soldes_grand_livre
WHERE numero_compte = 'COMPTE123';
```

**Colonnes:**
- `compte_id` - ID du compte
- `numero_compte` - Numéro du compte
- `devise` - Devise
- `solde_grand_livre` - Solde calculé depuis le grand livre (SOURCE DE VÉRITÉ)
- `derniere_ecriture` - Date dernière écriture
- `nombre_ecritures` - Nombre d'écritures

### 2. Détection Écarts

```sql
SELECT * FROM ledger.vue_ecarts_soldes
WHERE niveau_ecart IN ('MOYEN', 'CRITIQUE')
ORDER BY ABS(ecart) DESC;
```

**Colonnes:**
- `compte_id` - ID du compte
- `numero_compte` - Numéro du compte
- `devise` - Devise
- `solde_compte` - Solde dans table comptes
- `solde_grand_livre` - Solde calculé depuis grand livre
- `ecart` - Différence
- `niveau_ecart` - OK, FAIBLE, MOYEN, CRITIQUE
- `derniere_synchronisation` - Date dernière sync
- `derniere_ecriture` - Date dernière écriture

**Niveaux d'écart:**
- `OK` - Écart < 0.01
- `FAIBLE` - Écart < 100
- `MOYEN` - Écart < 1000
- `CRITIQUE` - Écart >= 1000

---

## 🔒 Protection et Sécurité

### Immuabilité
- ❌ **UPDATE interdit** - Trigger bloque toute modification
- ❌ **DELETE interdit** - Trigger bloque toute suppression
- ✅ **Annulation** - Créer écriture d'annulation avec référence

### Hash d'Intégrité
Chaque écriture a un hash SHA-256 calculé sur:
- ID transaction
- Référence transaction
- Montant
- Devise
- Timestamp

**Vérification:**
```sql
SELECT 
    numero_ecriture,
    hash_integrite,
    encode(digest(
        transaction_id::TEXT || 
        reference_transaction || 
        montant::TEXT || 
        devise || 
        cree_le::TEXT,
        'sha256'
    ), 'hex') as hash_recalcule
FROM ledger.ecritures_comptables
WHERE hash_integrite != encode(digest(...), 'hex');
-- Doit retourner 0 ligne
```

### Cohérence
Vérification automatique avant chaque insertion:
- Solde après = Solde avant ± Montant
- Hash présent et valide
- Utilisateur renseigné
- Description présente

---

## 📝 Exemples d'Utilisation

### Exemple 1: Transaction Simple

```sql
-- Insérer une transaction (le grand livre s'enregistre automatiquement)
INSERT INTO transaction.transactions (
    id, reference_transaction, type_transaction,
    compte_source_id, compte_destination_id,
    montant, devise, frais, montant_total,
    statut, cree_par
) VALUES (
    uuid_generate_v4(),
    'TRX-2026-001',
    'TRANSFERT',
    'uuid_compte_source',
    'uuid_compte_destination',
    10000.00,
    'BIF',
    50.00,
    10050.00,
    'VALIDEE',
    'uuid_utilisateur'
);

-- Résultat automatique dans le grand livre:
-- 3 écritures créées:
-- 1. ECR20260200000123-D (Débit compte source: 10050 BIF)
-- 2. ECR20260200000123-C (Crédit compte destination: 10000 BIF)
-- 3. ECR20260200000123-F (Frais: 50 BIF)
```

### Exemple 2: Vérifier Intégrité Mensuelle

```sql
-- Vérifier intégrité du mois en cours
SELECT * FROM ledger.verifier_integrite_grand_livre(
    DATE_TRUNC('month', CURRENT_DATE)::DATE,
    CURRENT_DATE
);
```

### Exemple 3: Détecter Écarts

```sql
-- Trouver tous les comptes avec écarts
SELECT 
    numero_compte,
    solde_compte,
    solde_grand_livre,
    ecart,
    niveau_ecart
FROM ledger.vue_ecarts_soldes
WHERE niveau_ecart != 'OK'
ORDER BY ABS(ecart) DESC
LIMIT 10;
```

### Exemple 4: Historique Complet d'un Compte

```sql
-- Voir toutes les écritures d'un compte
SELECT 
    numero_ecriture,
    date_comptable,
    type_transaction,
    sens,
    montant,
    solde_avant,
    solde_apres,
    qui_nom,
    quoi
FROM ledger.ecritures_comptables
WHERE numero_compte = 'COMPTE123'
ORDER BY quand DESC
LIMIT 50;
```

---

## 🎯 Avantages

### Pour la Comptabilité
✅ Comptabilité double entrée automatique  
✅ Équilibre garanti (débits = crédits)  
✅ Reconstitution état à n'importe quel instant  
✅ Classification automatique  
✅ Périodes comptables gérées  

### Pour l'Audit
✅ Traçabilité complète (QUI, QUAND, QUOI, COMMENT, POURQUOI, OÙ)  
✅ Immuabilité garantie  
✅ Hash d'intégrité  
✅ Détection automatique d'anomalies  
✅ Rapports d'intégrité  

### Pour la Sécurité
✅ Protection contre modification/suppression  
✅ Vérification cohérence automatique  
✅ Géolocalisation des opérations  
✅ Tracking sessions et devices  
✅ Détection écarts temps réel  

### Pour la Performance
✅ Enregistrement asynchrone (triggers AFTER)  
✅ Index optimisés  
✅ Vues matérialisées disponibles  
✅ Requêtes rapides  

---

## 🚨 Alertes et Monitoring

### Alertes Automatiques

**1. Écart Critique Détecté**
```sql
-- Créer alerte si écart > 1000
SELECT * FROM ledger.vue_ecarts_soldes
WHERE niveau_ecart = 'CRITIQUE';
```

**2. Grand Livre Déséquilibré**
```sql
-- Vérifier équilibre quotidien
SELECT * FROM ledger.verifier_integrite_grand_livre()
WHERE est_equilibre = FALSE;
```

**3. Écritures Sans Hash**
```sql
-- Détecter écritures sans hash (CRITIQUE)
SELECT COUNT(*) FROM ledger.ecritures_comptables
WHERE hash_integrite IS NULL OR LENGTH(hash_integrite) != 64;
-- Doit retourner 0
```

---

## 📞 Support

Pour toute question sur le grand livre automatique:
- Consulter cette documentation
- Vérifier l'intégrité avec `verifier_integrite_grand_livre()`
- Consulter les vues de contrôle
- Contacter l'équipe technique

---

**Grand Livre Automatique Actif**  
**Précision et Vigilance Extrême Garanties**  
**Toutes les Opérations Financières Tracées**
