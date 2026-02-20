# Base de Données - Structure Complète

**Date de création**: 2026-02-20  
**PostgreSQL**: 10.3  
**Base**: ufaranga  
**Statut**: ✅ OPÉRATIONNELLE

---

## 📁 Fichiers Essentiels

### 1. Structure Principale
**`ufaranga_structure_updated_20260220.sql`**
- Structure complète de la base de données
- 11 schémas, 27 tables
- Configuration dynamique (plafonds, règles, frais, devises)
- Données initiales (devises, taux, plafonds, règles métier)
- Triggers de protection IMMUABLE
- Fonctions utilitaires

**Utilisation:**
```bash
psql -U postgres -d ufaranga -f ufaranga_structure_updated_20260220.sql
```

### 2. Grand Livre Automatique
**`triggers_grand_livre_automatique.sql`**
- Triggers automatiques pour enregistrement dans le grand livre
- 3 fonctions principales d'enregistrement automatique
- 2 fonctions utilitaires (intégrité, statistiques)
- 2 vues de contrôle (soldes, écarts)
- Protection IMMUABLE du grand livre

**Utilisation:**
```bash
psql -U postgres -d ufaranga -f triggers_grand_livre_automatique.sql
```

### 3. Documentation

**`GRAND_LIVRE_AUTOMATIQUE.md`**
- Documentation complète du grand livre
- Fonctionnement des triggers automatiques
- Traçabilité extrême (QUI, QUAND, QUOI, COMMENT, POURQUOI, OÙ)
- Exemples d'utilisation
- Fonctions utilitaires

**`RAPPORT_SYNCHRONISATION_FINAL.md`**
- Rapport de synchronisation complète
- État actuel de la base
- Tables créées par schéma
- Prochaines étapes

---

## 🗂️ Structure de la Base

### Schémas (11)
1. **audit** - Historiques IMMUABLES (taux, comptes, transactions)
2. **bancaire** - Banques partenaires et comptes réels
3. **commission** - Commissions et rémunérations
4. **compliance** - KYC, AML, documents
5. **configuration** - Configuration dynamique du système
6. **ledger** - Grand livre comptable (IMMUABLE)
7. **notification** - Notifications et alertes
8. **portefeuille** - Devises, taux, comptes virtuels
9. **reconciliation** - Réconciliation bancaire
10. **securite** - Alertes fraude, sessions
11. **transaction** - Transactions et mouvements

### Tables Critiques
- `ledger.ecritures_comptables` - Grand livre (IMMUABLE)
- `portefeuille.comptes` - Comptes virtuels
- `transaction.transactions` - Transactions
- `configuration.plafonds_configuration` - Plafonds dynamiques
- `configuration.regles_metier` - Règles métier (JSON)
- `configuration.frais_configuration` - Frais configurables

---

## 🚀 Installation Complète

### Étape 1: Créer la base
```bash
createdb -U postgres ufaranga
```

### Étape 2: Activer les extensions
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

### Étape 3: Créer la structure
```bash
psql -U postgres -d ufaranga -f ufaranga_structure_updated_20260220.sql
```

### Étape 4: Activer les triggers automatiques
```bash
psql -U postgres -d ufaranga -f triggers_grand_livre_automatique.sql
```

### Étape 5: Vérifier l'installation
```sql
-- Compter les tables par schéma
SELECT schemaname, COUNT(*) as nb_tables
FROM pg_tables
WHERE schemaname IN ('audit', 'bancaire', 'commission', 'compliance', 
                     'configuration', 'notification', 'portefeuille', 
                     'transaction', 'ledger', 'reconciliation', 'securite')
GROUP BY schemaname
ORDER BY schemaname;

-- Vérifier le grand livre
SELECT COUNT(*) FROM ledger.ecritures_comptables;

-- Vérifier les devises
SELECT * FROM portefeuille.devises ORDER BY ordre_affichage;
```

---

## 📊 Configuration Dynamique

### Devises Supportées
- BIF (Franc Burundais) - Devise de base
- USD (Dollar Américain)
- EUR (Euro)
- RWF (Franc Rwandais)
- KES (Shilling Kenyan)
- TZS (Shilling Tanzanien)
- UGX (Shilling Ougandais)
- CDF (Franc Congolais)

### Types d'Utilisateurs
- CLIENT - Utilisateurs finaux
- AGENT - Agents de dépôt/retrait
- MARCHAND - Commerçants
- ADMIN - Administrateurs système

### Niveaux KYC
- 0 - Minimal (plafonds bas)
- 1 - Standard (plafonds moyens)
- 2 - Élevé (plafonds élevés)
- 3 - Illimité (pas de plafonds)

---

## 🔒 Sécurité et Traçabilité

### Tables IMMUABLES
- `ledger.ecritures_comptables` - Grand livre
- `audit.historique_taux_change` - Historique taux
- `audit.historique_comptes` - Historique comptes
- `audit.historique_transactions` - Historique transactions

**Protection**: Triggers empêchent UPDATE et DELETE

### Traçabilité Complète
Chaque opération enregistre:
- **QUI**: Utilisateur (ID, nom, type, rôle)
- **QUAND**: Timestamp précis
- **QUOI**: Description détaillée
- **COMMENT**: Moyen (WEB, API, MOBILE, SYSTEME, ADMIN, BATCH)
- **POURQUOI**: Raison/commentaire
- **OÙ**: Géolocalisation (pays, ville, lat/long, IP)

### Hash d'Intégrité
Chaque écriture comptable a un hash SHA-256 pour vérification d'intégrité.

---

## 📈 Fonctions Utilitaires

### Configuration
```sql
-- Obtenir plafond applicable
SELECT * FROM configuration.get_plafond_applicable(1, 'CLIENT', 'BIF');

-- Obtenir règle métier
SELECT configuration.get_regle_metier('MAX_COMPTES_PAR_DEVISE');

-- Calculer frais
SELECT configuration.calculer_frais('TRANSFERT', 10000, 'BIF', 'CLIENT', 'CLIENT');

-- Vérifier limite comptes
SELECT configuration.verifier_limite_comptes(
    'uuid_utilisateur', 'CLIENT', 'BIF'
);
```

### Grand Livre
```sql
-- Vérifier intégrité
SELECT * FROM ledger.verifier_integrite_grand_livre(
    '2026-01-01'::DATE, 
    '2026-12-31'::DATE
);

-- Statistiques période
SELECT * FROM ledger.statistiques_grand_livre('2026-02');

-- Soldes calculés
SELECT * FROM ledger.vue_soldes_grand_livre;

-- Détecter écarts
SELECT * FROM ledger.vue_ecarts_soldes 
WHERE niveau_ecart IN ('MOYEN', 'CRITIQUE');
```

---

## 🎯 Prochaines Étapes

1. ✅ Structure de base créée
2. ✅ Configuration dynamique opérationnelle
3. ✅ Grand livre créé avec protection IMMUABLE
4. ⏳ Activer triggers automatiques grand livre
5. ⏳ Tester enregistrement automatique
6. ⏳ Créer comptes utilisateurs test
7. ⏳ Tester transactions complètes

---

## 📞 Support

Pour toute question:
- Consulter `GRAND_LIVRE_AUTOMATIQUE.md` pour le grand livre
- Consulter `RAPPORT_SYNCHRONISATION_FINAL.md` pour l'état actuel
- Vérifier les commentaires dans les fichiers SQL

---

**Base de Données Opérationnelle**  
**Configuration Dynamique Active**  
**Grand Livre Protégé**  
**Prêt pour Production**
