# Système d'Inscription Développeur uFaranga

## Vue d'ensemble

Le système d'inscription développeur permet aux développeurs et entreprises de créer un compte pour accéder à l'API uFaranga et intégrer les paiements mobiles dans leurs applications.

## Pages créées

### 1. Page d'inscription (`/developpeurs/inscription`)
Formulaire multi-étapes (6 étapes) pour créer un compte développeur.

### 2. Dashboard développeur (`/developpeurs/dashboard`)
Interface de gestion des clés API et suivi des transactions.

## Processus d'inscription (6 étapes)

### Étape 1 : Informations du développeur
- **Type de compte** : Individuel ou Entreprise/Startup
- **Nom complet** : Nom de la personne ou de l'entreprise
- **Pays** : Sélection du pays de résidence
- **Email professionnel** : Email de contact
- **Numéro de téléphone** : Téléphone de contact

### Étape 2 : Sécurité du compte
- **Mot de passe** : Minimum 8 caractères avec complexité
- **Confirmation mot de passe** : Vérification
- **2FA (optionnel)** : 
  - SMS
  - Email
  - Application (Google Authenticator)
- **Codes de récupération** : Générés après validation

### Étape 3 : Vérification d'identité (KYC)

#### Pour les comptes individuels :
- Type de pièce d'identité (Passeport, CNI, Permis)
- Numéro de pièce d'identité
- Upload de la pièce d'identité (recto-verso)
- Photo selfie avec pièce d'identité

#### Pour les entreprises :
- Nom de l'entreprise
- Numéro de registre de commerce
- NIF (Numéro d'Identification Fiscale)
- Adresse légale
- Nom du représentant légal
- Pièce d'identité du représentant légal

### Étape 4 : Informations techniques
- **Nom de l'application** : Nom du projet
- **Description** : Description détaillée de l'utilisation de l'API
- **URL du site web** : Site web de l'application (optionnel)
- **URL de callback** : URL de retour après paiement
- **URL de webhook** : URL pour recevoir les notifications
- **Plateformes cibles** : Web, Android, iOS, Desktop
- **Environnement initial** : Sandbox (test) ou Production

### Étape 5 : Configuration paiement
- **Devise principale** : BIF, USD, EUR, RWF
- **Moyens de paiement** :
  - Mobile Money
  - Carte bancaire
  - Virement bancaire
  - Crypto
- **Limite de transaction** : 1M, 5M, 10M BIF ou illimité
- **Mode test** : Accès au sandbox avec comptes virtuels

### Étape 6 : Validation et conformité
- **Résumé** : Récapitulatif des informations
- **Acceptation** :
  - Conditions Générales d'Utilisation
  - Politique de Confidentialité
  - Normes AML/KYC/RGPD
- **Information sur les clés API** : Explication de la réception des clés
- **Logs & Audit** : Information sur l'enregistrement des transactions

## Clés API

Après validation du compte (24-48h), le développeur reçoit :

### Environnement Sandbox (Test)
- **API Key (publique)** : `pk_test_...`
- **Secret Key (privée)** : `sk_test_...`
- **Webhook Secret** : `whsec_test_...`

### Environnement Production (Réel)
- **API Key (publique)** : `pk_live_...`
- **Secret Key (privée)** : `sk_live_...`
- **Webhook Secret** : `whsec_live_...`

## Dashboard développeur

Le dashboard permet de :
- Visualiser les statistiques (transactions, volume, taux de succès)
- Gérer les clés API (copier, afficher, régénérer)
- Consulter les transactions récentes
- Accéder à la documentation et au sandbox
- Contacter le support

## Sécurité

### Bonnes pratiques
- Ne jamais exposer les clés privées côté client
- Utiliser HTTPS pour toutes les requêtes
- Stocker les clés dans des variables d'environnement
- Régénérer les clés en cas de compromission
- Activer la 2FA pour une sécurité maximale

### Vérification des webhooks
Les webhooks doivent être vérifiés avec le Webhook Secret pour garantir leur authenticité.

## Conformité

Le système respecte :
- **AML** (Anti-Money Laundering) : Lutte contre le blanchiment d'argent
- **KYC** (Know Your Customer) : Vérification d'identité
- **RGPD** : Protection des données personnelles
- **PCI DSS** : Sécurité des paiements par carte

## Routes

- `/developpeurs` : Page principale API
- `/developpeurs/inscription` : Formulaire d'inscription
- `/developpeurs/dashboard` : Dashboard développeur
- `/sandbox` : Environnement de test
- `/sdks` : SDKs officiels

## Technologies utilisées

- React avec hooks (useState)
- React Router pour la navigation
- Lucide React pour les icônes
- Tailwind CSS pour le styling
- Formulaire multi-étapes avec validation

## Prochaines étapes

1. Intégration backend pour l'enregistrement des comptes
2. Système d'authentification (login/logout)
3. Génération réelle des clés API
4. Upload et stockage des documents KYC
5. Système de validation manuelle des comptes
6. Envoi d'emails de confirmation
7. Génération des codes de récupération 2FA
8. API de gestion des webhooks
9. Logs et audit des transactions
10. Système de facturation et limites
