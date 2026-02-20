# 📝 Endpoint - Créer un Utilisateur Complet

## 🎯 Endpoint

```
POST /api/v1/identite/utilisateurs/creer/
```

**Permission:** Public (AllowAny) - Peut être changé en IsAdminUser si réservé aux admins

---

## 📋 Champs Disponibles

### 1. Authentification (OBLIGATOIRES)

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `courriel` | string | Adresse e-mail unique | `jean.dupont@example.com` |
| `numero_telephone` | string | Numéro au format international | `+25762046725` |
| `mot_de_passe` | string | Mot de passe (min 8 caractères) | `MonMotDePasse123!` |
| `mot_de_passe_confirmation` | string | Confirmation du mot de passe | `MonMotDePasse123!` |

### 2. Informations Personnelles (OBLIGATOIRES)

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `prenom` | string | Prénom | `Jean` |
| `nom_famille` | string | Nom de famille | `Dupont` |
| `date_naissance` | date | Date de naissance (YYYY-MM-DD) | `1990-01-15` |

### 3. Informations Personnelles (OPTIONNELLES)

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `lieu_naissance` | string | Lieu de naissance | `Bujumbura` |
| `nationalite` | string | Code ISO du pays | `BI` |

### 4. Adresse (OPTIONNELLES)

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `pays_residence` | string | Code ISO du pays de résidence | `BI` |
| `province` | string | Province | `Bujumbura Mairie` |
| `ville` | string | Ville | `Bujumbura` |
| `commune` | string | Commune | `Mukaza` |
| `quartier` | string | Quartier | `Rohero` |
| `avenue` | string | Avenue | `Avenue de la Liberté` |
| `numero_maison` | string | Numéro de maison | `123` |
| `code_postal` | string | Code postal | `BP 1234` |

### 5. Type, KYC, Statut (OPTIONNELLES avec valeurs par défaut)

| Champ | Type | Défaut | Description | Valeurs Possibles |
|-------|------|--------|-------------|-------------------|
| `type_utilisateur_code` | string | `CLIENT` | Type d'utilisateur | `CLIENT`, `AGENT`, `MARCHAND`, `ADMIN`, `SUPER_ADMIN`, `SYSTEME` |
| `niveau_kyc_code` | integer | `0` | Niveau KYC | `0`, `1`, `2`, `3` |
| `statut_code` | string | `ACTIF` | Statut du compte | `ACTIF`, `EN_VERIFICATION`, `SUSPENDU`, `BLOQUE`, `FERME` |

### 6. Localisation (OPTIONNELLES - Relations avec tables de localisation)

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `pays_code` | string | Code ISO du pays | `BI` |
| `province_code` | string | Code de la province | `BM` |
| `district_code` | string | Code du district | `MUK` |
| `quartier_code` | string | Code du quartier | `ROH` |

### 7. Vérifications (OPTIONNELLES)

| Champ | Type | Défaut | Description |
|-------|------|--------|-------------|
| `telephone_verifie` | boolean | `false` | Téléphone vérifié |
| `courriel_verifie` | boolean | `false` | Email vérifié |

### 8. Métadonnées (OPTIONNELLES)

| Champ | Type | Défaut | Description |
|-------|------|--------|-------------|
| `metadonnees` | object | `{}` | Données JSON supplémentaires |

---

## 📝 Exemples de Requêtes

### Exemple 1: Inscription Minimale (Client Standard)

```bash
POST /api/v1/identite/utilisateurs/creer/
Content-Type: application/json

{
  "courriel": "jean.dupont@example.com",
  "numero_telephone": "+25762046725",
  "mot_de_passe": "MonMotDePasse123!",
  "mot_de_passe_confirmation": "MonMotDePasse123!",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "date_naissance": "1990-01-15"
}
```

**Résultat:** Utilisateur CLIENT, KYC niveau 0, statut ACTIF

---

### Exemple 2: Inscription Complète avec Adresse

```bash
POST /api/v1/identite/utilisateurs/creer/
Content-Type: application/json

{
  "courriel": "marie.martin@example.com",
  "numero_telephone": "+25779123456",
  "mot_de_passe": "SecurePass456!",
  "mot_de_passe_confirmation": "SecurePass456!",
  
  "prenom": "Marie",
  "nom_famille": "Martin",
  "date_naissance": "1985-05-20",
  "lieu_naissance": "Gitega",
  "nationalite": "BI",
  
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue de la Liberté",
  "numero_maison": "456",
  "code_postal": "BP 5678"
}
```

---

### Exemple 3: Créer un Agent (avec localisation géographique)

```bash
POST /api/v1/identite/utilisateurs/creer/
Content-Type: application/json

{
  "courriel": "agent.service@ufaranga.bi",
  "numero_telephone": "+25768987654",
  "mot_de_passe": "AgentPass789!",
  "mot_de_passe_confirmation": "AgentPass789!",
  
  "prenom": "Pierre",
  "nom_famille": "Nkurunziza",
  "date_naissance": "1988-03-10",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  
  "type_utilisateur_code": "AGENT",
  "niveau_kyc_code": 2,
  "statut_code": "ACTIF",
  
  "pays_code": "BI",
  "province_code": "BM",
  "district_code": "MUK",
  "quartier_code": "ROH",
  
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue du Commerce",
  "numero_maison": "789"
}
```

---

### Exemple 4: Créer un Marchand Vérifié

```bash
POST /api/v1/identite/utilisateurs/creer/
Content-Type: application/json

{
  "courriel": "boutique.centrale@example.com",
  "numero_telephone": "+25761234567",
  "mot_de_passe": "MarchandSecure123!",
  "mot_de_passe_confirmation": "MarchandSecure123!",
  
  "prenom": "Boutique",
  "nom_famille": "Centrale",
  "date_naissance": "1980-01-01",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  
  "type_utilisateur_code": "MARCHAND",
  "niveau_kyc_code": 3,
  "statut_code": "ACTIF",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "pays_residence": "BI",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  
  "metadonnees": {
    "nom_commercial": "Boutique Centrale",
    "numero_registre_commerce": "RC/BJA/2020/12345",
    "secteur_activite": "Commerce de détail"
  }
}
```

---

## ✅ Réponse en Cas de Succès

**Status:** `201 Created`

```json
{
  "message": "Utilisateur créé avec succès",
  "utilisateur": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "courriel": "jean.dupont@example.com",
    "numero_telephone": "+25762046725",
    "prenom": "Jean",
    "nom_famille": "Dupont",
    "nom_complet": "Jean Dupont",
    "date_naissance": "1990-01-15",
    "lieu_naissance": "Bujumbura",
    "nationalite": "BI",
    
    "type_utilisateur": "CLIENT",
    "type_utilisateur_details": {
      "code": "CLIENT",
      "libelle": "Client",
      "description": "Client standard de la plateforme",
      "ordre_affichage": 1,
      "est_actif": true
    },
    
    "niveau_kyc": 0,
    "niveau_kyc_details": {
      "niveau": 0,
      "libelle": "Non vérifié",
      "description": "Compte non vérifié",
      "limite_transaction_journaliere": 50000.00,
      "limite_solde_maximum": 200000.00,
      "documents_requis": [],
      "est_actif": true
    },
    
    "statut": "ACTIF",
    "statut_details": {
      "code": "ACTIF",
      "libelle": "Actif",
      "description": "Compte actif et opérationnel",
      "couleur": "#28a745",
      "permet_connexion": true,
      "permet_transactions": true,
      "ordre_affichage": 1,
      "est_actif": true
    },
    
    "pays_details": {
      "id": "uuid",
      "code_iso_2": "BI",
      "code_iso_3": "BDI",
      "nom": "Burundi",
      "telephonie": {
        "code_telephonique": "+257",
        "format_numero_national": "XX XX XX XX",
        "operateurs": ["Econet", "Lumitel", "Smart"]
      },
      "devise": {
        "code": "BIF",
        "symbole": "FBu"
      }
    },
    
    "province_details": {
      "id": "uuid",
      "code": "BM",
      "nom": "Bujumbura Mairie"
    },
    
    "telephone_verifie": false,
    "courriel_verifie": false,
    "est_actif": true,
    "date_creation": "2024-02-20T10:00:00Z",
    
    "profil": {
      "id": "uuid",
      "langue": "fr",
      "devise_preferee": "BIF",
      "fuseau_horaire": "Africa/Bujumbura"
    },
    
    "numeros_telephone": []
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

---

## ❌ Erreurs Possibles

### 1. Email Déjà Utilisé

```json
{
  "courriel": [
    "Cette adresse e-mail est déjà utilisée."
  ]
}
```

### 2. Téléphone Déjà Utilisé

```json
{
  "numero_telephone": [
    "Ce numéro de téléphone est déjà utilisé."
  ]
}
```

### 3. Mots de Passe Non Identiques

```json
{
  "mot_de_passe_confirmation": [
    "Les mots de passe ne correspondent pas."
  ]
}
```

### 4. Type Utilisateur Invalide

```json
{
  "type_utilisateur_code": [
    "Type utilisateur \"INVALID\" introuvable."
  ]
}
```

### 5. Niveau KYC Invalide

```json
{
  "niveau_kyc_code": [
    "Niveau KYC \"5\" introuvable."
  ]
}
```

### 6. Pays Introuvable

```json
{
  "pays_code": [
    "Pays \"XX\" introuvable."
  ]
}
```

---

## 🔍 Endpoints Complémentaires

### 1. Lister les Types d'Utilisateurs

```bash
GET /api/v1/identite/types-utilisateurs/
```

**Réponse:**
```json
[
  {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard de la plateforme",
    "ordre_affichage": 1,
    "est_actif": true
  },
  {
    "code": "AGENT",
    "libelle": "Agent",
    "description": "Agent de service",
    "ordre_affichage": 2,
    "est_actif": true
  }
]
```

### 2. Lister les Niveaux KYC

```bash
GET /api/v1/identite/niveaux-kyc/
```

**Réponse:**
```json
[
  {
    "niveau": 0,
    "libelle": "Non vérifié",
    "description": "Compte non vérifié",
    "limite_transaction_journaliere": 50000.00,
    "limite_solde_maximum": 200000.00,
    "documents_requis": [],
    "est_actif": true
  },
  {
    "niveau": 1,
    "libelle": "Basique",
    "description": "Vérification basique avec pièce d'identité",
    "limite_transaction_journaliere": 500000.00,
    "limite_solde_maximum": 2000000.00,
    "documents_requis": [
      "Carte d'identité nationale",
      "Selfie avec carte d'identité"
    ],
    "est_actif": true
  }
]
```

### 3. Lister les Statuts

```bash
GET /api/v1/identite/statuts-utilisateurs/
```

**Réponse:**
```json
[
  {
    "code": "ACTIF",
    "libelle": "Actif",
    "description": "Compte actif et opérationnel",
    "couleur": "#28a745",
    "permet_connexion": true,
    "permet_transactions": true,
    "ordre_affichage": 1,
    "est_actif": true
  }
]
```

---

## 📊 Tableau Récapitulatif des Types

### Types d'Utilisateurs

| Code | Libellé | Limite Numéros | Description |
|------|---------|----------------|-------------|
| `CLIENT` | Client | 3 | Utilisateur standard |
| `AGENT` | Agent | 5 | Agent de service |
| `MARCHAND` | Marchand | 5 | Commerçant |
| `ADMIN` | Administrateur | Illimité | Administrateur |
| `SUPER_ADMIN` | Super Admin | Illimité | Super administrateur |
| `SYSTEME` | Système | Illimité | Compte système |

### Niveaux KYC

| Niveau | Libellé | Limite Journalière | Solde Max | Documents |
|--------|---------|-------------------|-----------|-----------|
| `0` | Non vérifié | 50 000 BIF | 200 000 BIF | Aucun |
| `1` | Basique | 500 000 BIF | 2 000 000 BIF | CNI + Selfie |
| `2` | Complet | 2 000 000 BIF | 10 000 000 BIF | CNI + Justificatif domicile |
| `3` | Premium | 10 000 000 BIF | Illimité | Tous documents |

### Statuts

| Code | Libellé | Couleur | Connexion | Transactions |
|------|---------|---------|-----------|--------------|
| `ACTIF` | Actif | #28a745 (vert) | ✅ | ✅ |
| `EN_VERIFICATION` | En vérification | #ffc107 (orange) | ✅ | ❌ |
| `SUSPENDU` | Suspendu | #fd7e14 (orange) | ❌ | ❌ |
| `BLOQUE` | Bloqué | #dc3545 (rouge) | ❌ | ❌ |
| `FERME` | Fermé | #6c757d (gris) | ❌ | ❌ |

---

## ✅ Résumé

**Endpoint:** `POST /api/v1/identite/utilisateurs/creer/`

**Crée un utilisateur complet avec:**
- ✅ Informations personnelles complètes
- ✅ Type d'utilisateur (CLIENT, AGENT, MARCHAND, etc.)
- ✅ Niveau KYC avec limites de transaction
- ✅ Statut du compte avec permissions
- ✅ Localisation géographique complète
- ✅ Adresse détaillée
- ✅ Profil automatique
- ✅ Tokens JWT pour connexion immédiate

**Tous les champs de la table `identite.utilisateurs` sont alimentés!** 🚀
