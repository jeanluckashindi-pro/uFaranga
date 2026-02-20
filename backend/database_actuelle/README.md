# Base de Données - Système Bancaire Mobile

## 📋 Vue d'ensemble

Ce dossier contient la structure complète et mise à jour de la base de données PostgreSQL pour le système bancaire mobile type M-PESA.

## 📁 Fichiers

### ufaranga_structure_updated_20260220.sql
Structure complète de la base de données avec :
- 8 schémas (audit, bancaire, commission, compliance, configuration, notification, portefeuille, transaction)
- Tables de devises et taux de change
- Tables de configuration dynamique
- Tables de comptes et transactions
- Tables d'audit immuables
- Triggers automatiques
- Fonctions utilitaires
- Données initiales

## 🚀 Installation

### Option 1 : Réinitialisation complète (ATTENTION: Supprime toutes les données!)

```bash
# 1. Réinitialiser la base
psql -U postgres -d ufaranga -f ../scripts/reset_database.sql

# 2. Créer la nouvelle structure
psql -U postgres -d ufaranga -f ufaranga_structure_updated_20260220.sql
```

### Option 2 : Création sur nouvelle base

```bash
# 1. Créer la base de données
createdb -U postgres ufaranga

# 2. Créer la structure
psql -U postgres -d ufaranga -f ufaranga_structure_updated_20260220.sql
```

## 📊 Structure de la base

### Schémas

1. **audit** - Historique immuable (append-only)
   - historique_taux_change
   - historique_comptes
   - historique_transactions

2. **bancaire** - Intégration bancaire
   - banques_partenaires
   - comptes_bancaires_reels

3. **configuration** - Configuration dynamique
   - plafonds_configuration
   - regles_metier
   - frais_configuration
   - types_transaction
   - devises_autorisees

4. **portefeuille** - Comptes virtuels
   - devises
   - taux_change
   - comptes

5. **transaction** - Transactions
   - transactions

6. **commission** - Commissions et rémunérations (à implémenter)

7. **compliance** - KYC et conformité (à implémenter)

8. **notification** - Notifications (à implémenter)

## 🔧 Fonctionnalités

### Configuration Dynamique

Le système utilise des tables de configuration pour rendre toutes les règles modifiables sans redéploiement :

```sql
-- Obtenir plafond applicable
SELECT * FROM configuration.get_plafond_applicable(1, 'CLIENT', 'BIF');

-- Obtenir règle métier
SELECT configuration.get_regle_metier('MAX_COMPTES_PAR_DEVISE');

-- Calculer frais
SELECT configuration.calculer_frais('TRANSFERT', 100000, 'BIF', 'CLIENT', 'CLIENT');

-- Vérifier limite comptes
SELECT configuration.verifier_limite_comptes('uuid_utilisateur', 'CLIENT', 'BIF');
```

### Historique Immuable

Les tables d'audit sont protégées contre toute modification ou suppression :

```sql
-- Tentative de modification = ERREUR
UPDATE audit.historique_taux_change SET taux = 3000 WHERE id = 'uuid';
-- ERREUR: L'historique des taux est IMMUABLE

-- Tentative de suppression = ERREUR
DELETE FROM audit.historique_comptes WHERE id = 'uuid';
-- ERREUR: L'historique des comptes est IMMUABLE
```

### Triggers Automatiques

- Calcul automatique des taux inverses et taux avec marges
- Enregistrement automatique dans l'historique
- Protection contre modification/suppression de l'historique

## 📈 Données Initiales

### Devises (8)
- BIF (Franc Burundais)
- USD (Dollar Américain)
- EUR (Euro)
- RWF (Franc Rwandais)
- KES (Shilling Kenyan)
- TZS (Shilling Tanzanien)
- UGX (Shilling Ougandais)
- CDF (Franc Congolais)

### Taux de Change (7 paires)
- USD → BIF, EUR, RWF, KES, TZS, UGX, CDF

### Plafonds (12 configurations)
- CLIENT KYC 0-3 pour BIF et USD
- AGENT pour BIF et USD
- MARCHAND pour BIF et USD

### Règles Métier (7 règles)
- MAX_COMPTES_PAR_DEVISE
- DEVISES_AUTORISEES (CLIENT, AGENT, MARCHAND)
- DELAI_SYNCHRONISATION
- SEUIL_2FA
- TOLERANCE_ECART_SYNC

### Types de Transactions (8 types)
- DEPOT, RETRAIT, TRANSFERT, PAIEMENT
- FRAIS, COMMISSION, AJUSTEMENT, REMBOURSEMENT

### Configuration Frais (10 configurations)
- Dépôts gratuits
- Retraits par paliers
- Transferts en pourcentage
- Paiements marchands

### Devises Autorisées (18 configurations)
- CLIENT: BIF, USD (1 compte chacun)
- AGENT: BIF, USD, EUR, RWF (2-3 comptes)
- MARCHAND: BIF, USD, EUR (1-2 comptes)
- ADMIN: Toutes devises (5 comptes)

## 🔒 Sécurité

### Contraintes
- Soldes toujours >= 0
- Solde actuel = solde disponible + solde réservé
- Taux de change > 0
- Pas de taux entre même devise
- Unicité utilisateur + devise

### Audit
- Toutes les modifications tracées
- QUI, QUAND, QUOI, COMMENT, POURQUOI
- Historique immuable
- Adresse IP et User Agent

## 📝 Prochaines Étapes

1. Implémenter les modèles Django correspondants
2. Créer les APIs REST pour CRUD
3. Implémenter le moteur de transactions
4. Implémenter la synchronisation bancaire
5. Ajouter les tests unitaires et d'intégration

## 🆘 Support

Pour toute question, consulter :
- `../scripts/README_CONFIGURATION_DYNAMIQUE.md` - Guide configuration
- `.kiro/specs/systeme-bancaire-mobile/requirements.md` - Spécifications complètes
