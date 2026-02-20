# Spécification: Système de Paiements Gouvernementaux et Fiscaux

**Feature Name**: paiements-gouvernementaux-fiscaux  
**Date de création**: 20 février 2026  
**Statut**: Draft  
**Priorité**: Haute

---

## 1. Vision et Contexte

### 1.1 Vision Globale

Transformer uFaranga en un système de paiement urbain complet qui facilite les transactions gouvernementales et fiscales, permettant aux citoyens de payer directement leurs obligations fiscales, taxes, et services gouvernementaux sans se déplacer.

### 1.2 Valeur Ajoutée

Le système agit comme un **miroir bidirectionnel** entre les citoyens et le gouvernement:
- **Citoyens → Gouvernement**: Paiements fiscaux, taxes, amendes, services publics
- **Gouvernement → Citoyens**: Subventions, allocations, remboursements, salaires fonctionnaires

### 1.3 Cas d'Usage Principaux

1. **Transport Urbain**
   - Paiement de tickets de bus/taxi
   - Abonnements mensuels
   - Cartes de transport prépayées

2. **Taxes et Impôts**
   - Impôts sur le revenu
   - Taxes foncières
   - Taxes professionnelles
   - TVA pour commerçants

3. **Services Gouvernementaux**
   - Frais de passeport/visa
   - Permis de conduire
   - Actes de naissance/mariage
   - Certificats divers

4. **Amendes et Pénalités**
   - Amendes de circulation
   - Amendes administratives
   - Pénalités de retard

5. **Factures Publiques**
   - Électricité (REGIDESO)
   - Eau
   - Ordures ménagères

6. **Imports et Douanes**
   - Droits de douane
   - Taxes d'importation
   - Frais de dédouanement

---

## 2. Acteurs du Système

### 2.1 Acteurs Existants (à étendre)

| Acteur | Rôle Actuel | Extension Nécessaire |
|--------|-------------|---------------------|
| CLIENT | Utilisateur final | Ajouter profil "Contribuable" |
| AGENT | Agent de dépôt/retrait | Ajouter "Agent Gouvernemental" |
| MARCHAND | Commerçant | Ajouter "Service Public" |
| ADMIN | Administrateur | Ajouter "Admin Fiscal" |

### 2.2 Nouveaux Acteurs

| Acteur | Description | Permissions |
|--------|-------------|-------------|
| TAXMAN | Percepteur fiscal | Collecte taxes, génère rapports fiscaux |
| GOVT_SERVICE | Service gouvernemental | Émet factures services publics |
| CUSTOMS_OFFICER | Agent des douanes | Gère imports/exports, droits de douane |
| TRANSPORT_OPERATOR | Opérateur de transport | Gère tickets, abonnements transport |
| UTILITY_PROVIDER | Fournisseur de services publics | Factures eau, électricité |

---

## 3. User Stories

### 3.1 Paiement de Taxes

**US-001: En tant que citoyen, je veux payer mes impôts directement depuis mon portefeuille mobile**

**Critères d'acceptation:**
- [ ] Je peux voir la liste de mes obligations fiscales
- [ ] Je peux sélectionner une taxe à payer
- [ ] Le système calcule automatiquement les pénalités de retard
- [ ] Je reçois un reçu officiel après paiement
- [ ] Le paiement est enregistré dans le système fiscal gouvernemental
- [ ] Je peux télécharger/imprimer le reçu en PDF

**US-002: En tant que percepteur fiscal, je veux suivre les paiements de taxes en temps réel**

**Critères d'acceptation:**
- [ ] Je peux voir un tableau de bord des paiements du jour
- [ ] Je peux filtrer par type de taxe
- [ ] Je peux générer des rapports de collecte
- [ ] Je peux voir les contribuables en retard
- [ ] Je peux envoyer des rappels automatiques

### 3.2 Transport Urbain

**US-003: En tant que passager, je veux payer mon ticket de bus avec mon téléphone**

**Critères d'acceptation:**
- [ ] Je peux scanner un QR code dans le bus
- [ ] Le paiement est instantané
- [ ] Je reçois un ticket électronique
- [ ] Le chauffeur reçoit confirmation du paiement
- [ ] Mon historique de trajets est enregistré

**US-004: En tant qu'opérateur de transport, je veux gérer les abonnements mensuels**

**Critères d'acceptation:**
- [ ] Je peux créer des formules d'abonnement
- [ ] Les clients peuvent s'abonner via l'app
- [ ] Le renouvellement est automatique
- [ ] Je reçois des rapports de revenus quotidiens
- [ ] Je peux bloquer des abonnements frauduleux

### 3.3 Services Gouvernementaux

**US-005: En tant que citoyen, je veux payer mes frais de passeport en ligne**

**Critères d'acceptation:**
- [ ] Je peux voir les frais requis pour chaque service
- [ ] Je peux payer directement depuis l'app
- [ ] Je reçois un numéro de référence
- [ ] Le service gouvernemental reçoit notification
- [ ] Je peux suivre l'état de ma demande

**US-006: En tant que service gouvernemental, je veux émettre des factures pour mes services**

**Critères d'acceptation:**
- [ ] Je peux créer une facture avec référence unique
- [ ] La facture est envoyée au citoyen via l'app
- [ ] Je reçois notification du paiement
- [ ] Je peux générer des rapports de revenus
- [ ] Je peux annuler/rembourser une facture

### 3.4 Imports et Douanes

**US-007: En tant qu'importateur, je veux payer mes droits de douane électroniquement**

**Critères d'acceptation:**
- [ ] Je peux voir le montant des droits calculés
- [ ] Je peux payer en plusieurs devises
- [ ] Je reçois un certificat de paiement
- [ ] Les douanes reçoivent confirmation instantanée
- [ ] Mon dossier d'importation est mis à jour automatiquement

**US-008: En tant qu'agent des douanes, je veux suivre les paiements de droits de douane**

**Critères d'acceptation:**
- [ ] Je peux voir tous les paiements en attente
- [ ] Je peux valider un paiement
- [ ] Je peux générer des rapports de collecte
- [ ] Je peux voir l'historique d'un importateur
- [ ] Je peux bloquer un importateur frauduleux

### 3.5 Factures Publiques

**US-009: En tant que citoyen, je veux payer ma facture d'électricité via l'app**

**Critères d'acceptation:**
- [ ] Je peux entrer mon numéro de compteur
- [ ] Le système récupère ma facture automatiquement
- [ ] Je peux payer en un clic
- [ ] Je reçois confirmation de paiement
- [ ] Le fournisseur reçoit le paiement instantanément

**US-010: En tant que fournisseur de services publics, je veux émettre des factures électroniques**

**Critères d'acceptation:**
- [ ] Je peux importer des factures en masse (CSV/Excel)
- [ ] Les factures sont envoyées automatiquement aux clients
- [ ] Je reçois notification des paiements
- [ ] Je peux gérer les impayés
- [ ] Je peux générer des rapports de recouvrement

---

## 4. Exigences Fonctionnelles

### 4.1 Gestion des Entités Gouvernementales

**REQ-001: Le système doit supporter plusieurs types d'entités gouvernementales**

- Ministères
- Administrations locales
- Services publics
- Régies financières
- Douanes et accises

**REQ-002: Chaque entité doit avoir:**
- Un identifiant unique gouvernemental
- Un compte de collecte dédié
- Des permissions spécifiques
- Un tableau de bord de suivi
- Des rapports automatiques

### 4.2 Types de Transactions Gouvernementales

**REQ-003: Nouveaux types de transactions à ajouter:**

| Type | Code | Description |
|------|------|-------------|
| Taxe sur le revenu | TAX_INCOME | Impôt sur le revenu |
| Taxe foncière | TAX_PROPERTY | Taxe sur propriété |
| TVA | TAX_VAT | Taxe sur valeur ajoutée |
| Droits de douane | CUSTOMS_DUTY | Droits d'importation |
| Amende circulation | FINE_TRAFFIC | Amende de circulation |
| Frais passeport | GOVT_PASSPORT | Frais de passeport |
| Frais visa | GOVT_VISA | Frais de visa |
| Permis conduire | GOVT_LICENSE | Permis de conduire |
| Acte naissance | GOVT_BIRTH_CERT | Acte de naissance |
| Facture électricité | UTILITY_ELECTRICITY | Facture électricité |
| Facture eau | UTILITY_WATER | Facture eau |
| Ticket transport | TRANSPORT_TICKET | Ticket de transport |
| Abonnement transport | TRANSPORT_SUBSCRIPTION | Abonnement transport |

### 4.3 Référencement Fiscal

**REQ-004: Chaque transaction gouvernementale doit avoir:**
- Numéro de référence fiscal unique
- Code de l'entité bénéficiaire
- Catégorie fiscale
- Période fiscale (année, trimestre, mois)
- Statut de conformité

**REQ-005: Intégration avec système fiscal national:**
- API de synchronisation avec base fiscale gouvernementale
- Envoi automatique des reçus au système fiscal
- Réconciliation quotidienne
- Rapports mensuels automatiques

### 4.4 Reçus et Certificats Officiels

**REQ-006: Génération de reçus officiels:**
- Format PDF avec logo gouvernemental
- QR code de vérification
- Signature électronique
- Numéro de série unique
- Horodatage certifié

**REQ-007: Types de documents:**
- Reçu de paiement fiscal
- Certificat de paiement douanier
- Quittance de service public
- Ticket de transport électronique
- Facture acquittée

### 4.5 Calendrier Fiscal

**REQ-008: Gestion des échéances fiscales:**
- Calendrier des dates limites de paiement
- Calcul automatique des pénalités de retard
- Rappels automatiques avant échéance
- Historique des paiements fiscaux
- Prévisions de paiements futurs

### 4.6 Rapports et Statistiques

**REQ-009: Rapports pour le gouvernement:**
- Collecte quotidienne par type de taxe
- Collecte mensuelle par région
- Top contribuables
- Retards de paiement
- Prévisions de revenus

**REQ-010: Rapports pour les citoyens:**
- Historique fiscal personnel
- Certificat de conformité fiscale
- Récapitulatif annuel
- Prévisions de taxes à venir

---

## 5. Exigences Non-Fonctionnelles

### 5.1 Performance

**NFR-001: Temps de réponse**
- Paiement fiscal: < 3 secondes
- Génération de reçu: < 2 secondes
- Synchronisation gouvernementale: < 5 secondes
- Rapports: < 10 secondes

**NFR-002: Disponibilité**
- 99.9% de disponibilité
- Maintenance planifiée hors heures de pointe
- Backup en temps réel

### 5.2 Sécurité

**NFR-003: Authentification renforcée**
- 2FA obligatoire pour transactions > 100,000 BIF
- Biométrie pour agents gouvernementaux
- Signature électronique pour reçus officiels

**NFR-004: Audit et traçabilité**
- Toutes les transactions gouvernementales sont IMMUABLES
- Logs détaillés avec géolocalisation
- Hash d'intégrité sur tous les reçus
- Archivage légal de 10 ans minimum

### 5.3 Conformité

**NFR-005: Conformité légale**
- Respect des lois fiscales nationales
- Format de reçus conforme aux normes gouvernementales
- Archivage conforme aux exigences légales
- Rapports conformes aux formats officiels

**NFR-006: Protection des données**
- Chiffrement des données fiscales
- Accès restreint aux données sensibles
- Anonymisation pour statistiques
- RGPD/protection de la vie privée

### 5.4 Scalabilité

**NFR-007: Capacité**
- Support de 10 millions d'utilisateurs
- 1 million de transactions/jour
- 100,000 transactions simultanées
- Stockage de 10 ans de données

---

## 6. Architecture Technique

### 6.1 Nouveaux Schémas de Base de Données

**Schema: fiscal**
- `entites_gouvernementales` - Entités gouvernementales
- `types_taxes` - Types de taxes et impôts
- `obligations_fiscales` - Obligations fiscales des citoyens
- `paiements_fiscaux` - Paiements de taxes
- `penalites_fiscales` - Pénalités de retard
- `recus_officiels` - Reçus officiels générés
- `calendrier_fiscal` - Échéances fiscales

**Schema: transport**
- `operateurs_transport` - Opérateurs de transport
- `lignes_transport` - Lignes de bus/taxi
- `tickets_transport` - Tickets vendus
- `abonnements_transport` - Abonnements actifs
- `trajets` - Historique des trajets

**Schema: douanes**
- `declarations_import` - Déclarations d'importation
- `droits_douane` - Droits de douane calculés
- `paiements_douane` - Paiements effectués
- `certificats_dedouanement` - Certificats émis

**Schema: services_publics**
- `fournisseurs_services` - Fournisseurs (électricité, eau, etc.)
- `compteurs` - Compteurs des clients
- `factures_services` - Factures émises
- `paiements_services` - Paiements reçus

### 6.2 Nouvelles Applications Django

```
apps/
├── fiscal/              # Gestion fiscale et taxes
├── transport/           # Transport urbain
├── douanes/            # Imports et douanes
├── services_publics/   # Services publics (eau, électricité)
├── gouvernement/       # Entités gouvernementales
└── documents/          # Génération de documents officiels
```

### 6.3 APIs Externes

**API-001: Système Fiscal National**
- Synchronisation des paiements
- Vérification des obligations fiscales
- Mise à jour des statuts de conformité

**API-002: Système de Transport**
- Validation des tickets
- Gestion des abonnements
- Suivi des trajets

**API-003: Système Douanier**
- Récupération des déclarations
- Calcul des droits
- Émission de certificats

**API-004: Fournisseurs de Services**
- Récupération des factures
- Confirmation des paiements
- Mise à jour des compteurs

---

## 7. Flux de Travail

### 7.1 Flux: Paiement de Taxe

```
1. Citoyen ouvre l'app
2. Sélectionne "Payer mes taxes"
3. Système récupère obligations fiscales depuis API gouvernementale
4. Citoyen sélectionne une taxe
5. Système calcule pénalités si retard
6. Citoyen confirme le paiement
7. Système débite le portefeuille
8. Système crédite le compte gouvernemental
9. Système génère reçu officiel (PDF + QR code)
10. Système envoie confirmation à l'API fiscale
11. Citoyen reçoit reçu par email/SMS
12. Transaction enregistrée dans grand livre
```

### 7.2 Flux: Paiement de Ticket de Transport

```
1. Passager monte dans le bus
2. Scanne QR code affiché dans le bus
3. App affiche le tarif
4. Passager confirme le paiement
5. Système débite le portefeuille
6. Système crédite l'opérateur de transport
7. Système génère ticket électronique
8. Chauffeur reçoit notification
9. Passager montre le ticket au contrôleur
10. Transaction enregistrée
```

### 7.3 Flux: Paiement de Droits de Douane

```
1. Importateur reçoit notification de déclaration
2. Ouvre l'app et voit le montant des droits
3. Système affiche détails (TVA, droits, frais)
4. Importateur sélectionne devise de paiement
5. Système applique taux de change
6. Importateur confirme
7. Système débite le portefeuille
8. Système crédite le compte des douanes
9. Système génère certificat de paiement
10. API douanière reçoit confirmation
11. Dossier d'importation mis à jour
12. Marchandises peuvent être libérées
```

---

## 8. Modèle de Données

### 8.1 Entité Gouvernementale

```python
class EntiteGouvernementale(models.Model):
    id = UUIDField(primary_key=True)
    code_entite = CharField(unique=True)  # Ex: MIN_FIN, DOUANES, OBR
    nom_officiel = CharField()
    type_entite = CharField(choices=TYPE_CHOICES)
    ministere_tutelle = CharField()
    
    # Compte de collecte
    compte_collecte_id = UUIDField()
    
    # Contact
    email_officiel = EmailField()
    telephone_officiel = CharField()
    adresse_siege = TextField()
    
    # Configuration
    logo_url = URLField()
    signature_electronique = TextField()
    format_recu = JSONField()
    
    # Métadonnées
    est_actif = BooleanField(default=True)
    date_creation = DateTimeField()
    metadonnees = JSONField()
```

### 8.2 Obligation Fiscale

```python
class ObligationFiscale(models.Model):
    id = UUIDField(primary_key=True)
    reference_fiscale = CharField(unique=True)
    
    # Contribuable
    utilisateur_id = UUIDField()
    numero_contribuable = CharField()
    
    # Type de taxe
    type_taxe = ForeignKey(TypeTaxe)
    entite_beneficiaire = ForeignKey(EntiteGouvernementale)
    
    # Montants
    montant_principal = DecimalField()
    montant_penalite = DecimalField(default=0)
    montant_total = DecimalField()
    devise = CharField(default='BIF')
    
    # Période
    annee_fiscale = IntegerField()
    trimestre = IntegerField(null=True)
    mois = IntegerField(null=True)
    
    # Échéances
    date_echeance = DateField()
    date_limite_paiement = DateField()
    
    # Statut
    statut = CharField(choices=STATUT_CHOICES)
    date_paiement = DateTimeField(null=True)
    transaction_paiement_id = UUIDField(null=True)
    
    # Métadonnées
    date_creation = DateTimeField()
    metadonnees = JSONField()
```

### 8.3 Reçu Officiel

```python
class RecuOfficiel(models.Model):
    id = UUIDField(primary_key=True)
    numero_recu = CharField(unique=True)
    
    # Transaction liée
    transaction_id = UUIDField()
    obligation_fiscale_id = UUIDField(null=True)
    
    # Émetteur
    entite_emettrice = ForeignKey(EntiteGouvernementale)
    agent_emetteur_id = UUIDField(null=True)
    
    # Bénéficiaire
    utilisateur_id = UUIDField()
    nom_beneficiaire = CharField()
    
    # Contenu
    type_document = CharField(choices=TYPE_DOC_CHOICES)
    montant = DecimalField()
    devise = CharField()
    description = TextField()
    
    # Sécurité
    qr_code_data = TextField()
    hash_integrite = CharField()
    signature_electronique = TextField()
    
    # Fichiers
    pdf_url = URLField()
    pdf_hash = CharField()
    
    # Métadonnées
    date_emission = DateTimeField()
    est_valide = BooleanField(default=True)
    date_annulation = DateTimeField(null=True)
    raison_annulation = TextField()
    metadonnees = JSONField()
```

---

## 9. Intégrations

### 9.1 API Système Fiscal National

**Endpoints requis:**
- `GET /api/obligations/{numero_contribuable}` - Récupérer obligations
- `POST /api/paiements` - Notifier un paiement
- `GET /api/statut/{reference_fiscale}` - Vérifier statut
- `POST /api/recus` - Enregistrer un reçu

### 9.2 API Opérateurs de Transport

**Endpoints requis:**
- `GET /api/tarifs/{ligne_id}` - Récupérer tarifs
- `POST /api/tickets` - Valider un ticket
- `GET /api/abonnements/{user_id}` - Vérifier abonnement
- `POST /api/trajets` - Enregistrer un trajet

### 9.3 API Système Douanier

**Endpoints requis:**
- `GET /api/declarations/{importateur_id}` - Récupérer déclarations
- `POST /api/paiements` - Notifier paiement de droits
- `POST /api/certificats` - Générer certificat
- `GET /api/statut/{declaration_id}` - Statut de déclaration

---

## 10. Phases d'Implémentation

### Phase 1: Infrastructure de Base (2 semaines)
- [ ] Créer schémas de base de données (fiscal, transport, douanes, services_publics)
- [ ] Créer applications Django
- [ ] Définir nouveaux types d'utilisateurs
- [ ] Définir nouveaux types de transactions
- [ ] Créer modèles de base

### Phase 2: Gestion Fiscale (3 semaines)
- [ ] Gestion des entités gouvernementales
- [ ] Gestion des obligations fiscales
- [ ] Paiement de taxes
- [ ] Génération de reçus officiels
- [ ] Intégration API fiscale
- [ ] Calendrier fiscal et rappels

### Phase 3: Transport Urbain (2 semaines)
- [ ] Gestion des opérateurs de transport
- [ ] Paiement de tickets
- [ ] Gestion des abonnements
- [ ] QR codes pour validation
- [ ] Historique des trajets

### Phase 4: Douanes et Imports (2 semaines)
- [ ] Gestion des déclarations
- [ ] Calcul des droits de douane
- [ ] Paiement multi-devises
- [ ] Certificats de dédouanement
- [ ] Intégration API douanière

### Phase 5: Services Publics (2 semaines)
- [ ] Gestion des fournisseurs
- [ ] Récupération des factures
- [ ] Paiement de factures
- [ ] Historique de consommation
- [ ] Intégration APIs fournisseurs

### Phase 6: Rapports et Analytics (1 semaine)
- [ ] Tableaux de bord gouvernementaux
- [ ] Rapports de collecte
- [ ] Statistiques fiscales
- [ ] Prévisions de revenus
- [ ] Export de données

### Phase 7: Tests et Déploiement (2 semaines)
- [ ] Tests unitaires
- [ ] Tests d'intégration
- [ ] Tests de charge
- [ ] Tests de sécurité
- [ ] Déploiement progressif

---

## 11. Risques et Mitigation

### 11.1 Risques Techniques

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Indisponibilité API gouvernementale | Élevé | Moyenne | Cache local, mode dégradé |
| Surcharge système (jour de paie) | Élevé | Élevée | Scaling horizontal, CDN |
| Erreurs de synchronisation | Élevé | Moyenne | Réconciliation automatique |
| Fraude fiscale | Élevé | Moyenne | Détection de fraude, audit |

### 11.2 Risques Légaux

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Non-conformité légale | Critique | Faible | Audit légal, certification |
| Litige sur reçus | Élevé | Faible | Signature électronique, archivage |
| Protection des données | Élevé | Moyenne | Chiffrement, accès restreint |

### 11.3 Risques Opérationnels

| Risque | Impact | Probabilité | Mitigation |
|--------|--------|-------------|------------|
| Formation insuffisante | Moyen | Élevée | Programme de formation |
| Résistance au changement | Moyen | Élevée | Communication, pilote |
| Support client surchargé | Moyen | Élevée | FAQ, chatbot, agents dédiés |

---

## 12. Métriques de Succès

### 12.1 KPIs Techniques
- Disponibilité: > 99.9%
- Temps de réponse: < 3s
- Taux d'erreur: < 0.1%
- Transactions/seconde: > 1000

### 12.2 KPIs Business
- Nombre d'utilisateurs actifs: > 1M en 6 mois
- Volume de transactions fiscales: > 100M BIF/jour
- Taux d'adoption: > 30% des contribuables
- Satisfaction utilisateur: > 4.5/5

### 12.3 KPIs Gouvernementaux
- Réduction des délais de paiement: -50%
- Augmentation de la collecte: +20%
- Réduction des coûts administratifs: -30%
- Taux de conformité fiscale: +15%

---

## 13. Dépendances

### 13.1 Dépendances Externes
- Accord avec ministère des Finances
- Intégration avec système fiscal national
- Partenariat avec opérateurs de transport
- Accord avec fournisseurs de services publics
- Certification légale des reçus électroniques

### 13.2 Dépendances Internes
- Architecture existante uFaranga opérationnelle
- Grand livre comptable fonctionnel
- Système de portefeuilles stable
- Infrastructure de sécurité robuste

---

## 14. Annexes

### 14.1 Glossaire

- **Contribuable**: Personne physique ou morale ayant des obligations fiscales
- **Obligation fiscale**: Dette fiscale envers l'État
- **Reçu officiel**: Document légal prouvant un paiement
- **Entité gouvernementale**: Organisation publique collectant des revenus
- **Conformité fiscale**: Respect des obligations fiscales

### 14.2 Références

- Loi fiscale nationale
- Règlements douaniers
- Normes de reçus électroniques
- Standards de sécurité gouvernementaux

---

**Document vivant - À mettre à jour régulièrement**
