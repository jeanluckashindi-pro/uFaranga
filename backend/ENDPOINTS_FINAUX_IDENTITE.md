# 📋 Endpoints Finaux - Module IDENTITÉ

## 🎯 Deux Endpoints Séparés

### 1. Inscription Publique (CLIENT)
### 2. Création Admin (AGENT/MARCHAND/ADMIN)

---

## 1️⃣ INSCRIPTION PUBLIQUE - Créer un CLIENT

```
POST /api/v1/identite/inscription/
```

**Permission:** Public (AllowAny)

**Crée automatiquement:**
- Type: `CLIENT`
- KYC: Niveau `0`
- Statut: `ACTIF`
- Email vérifié: `false`
- Téléphone vérifié: `false`

### Champs Obligatoires

```json
{
  "courriel": "user@example.com",
  "numero_telephone": "+25762046725",
  "mot_de_passe": "SecurePass123!",
  "mot_de_passe_confirmation": "SecurePass123!",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "date_naissance": "1990-01-15"
}
```

### Champs Optionnels (IDs)

```json
{
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue de la Liberté",
  "numero_maison": "123",
  "code_postal": "BP 1234",
  
  "pays_id": "uuid-du-pays",
  "province_id": "uuid-de-la-province",
  "district_id": "uuid-du-district",
  "quartier_id": "uuid-du-quartier",
  
  "metadonnees": {}
}
```

### Réponse

```json
{
  "message": "Inscription réussie",
  "utilisateur": {
    "id": "uuid",
    "courriel": "user@example.com",
    "numero_telephone": "+25762046725",
    "prenom": "Jean",
    "nom_famille": "Dupont",
    "nom_complet": "Jean Dupont",
    "date_naissance": "1990-01-15",
    
    "type_utilisateur": "CLIENT",
    "type_utilisateur_details": {
      "code": "CLIENT",
      "libelle": "Client",
      "description": "Client standard de la plateforme"
    },
    
    "niveau_kyc": 0,
    "niveau_kyc_details": {
      "niveau": 0,
      "libelle": "Non vérifié",
      "limite_transaction_journaliere": 50000.00,
      "limite_solde_maximum": 200000.00
    },
    
    "statut": "ACTIF",
    "statut_details": {
      "code": "ACTIF",
      "libelle": "Actif",
      "permet_connexion": true,
      "permet_transactions": true
    },
    
    "telephone_verifie": false,
    "courriel_verifie": false,
    "est_actif": true,
    "date_creation": "2024-02-20T10:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

## 2️⃣ CRÉER UN ADMIN/AGENT/MARCHAND

```
POST /api/v1/identite/admin/creer-utilisateur/
```

**Permission:** IsAuthenticated + IsAdminUser

**Vérifications:**
- ✅ Utilisateur connecté est authentifié
- ✅ Utilisateur connecté est ADMIN ou SUPER_ADMIN
- ✅ Type demandé n'est PAS CLIENT (utiliser l'inscription pour ça)

### Champs Obligatoires

```json
{
  "courriel": "agent@ufaranga.bi",
  "numero_telephone": "+25768987654",
  "mot_de_passe": "AgentPass789!",
  "mot_de_passe_confirmation": "AgentPass789!",
  "prenom": "Pierre",
  "nom_famille": "Nkurunziza",
  "date_naissance": "1988-03-10",
  
  "type_utilisateur_id": "AGENT",
  "niveau_kyc_id": 2,
  "statut_id": "ACTIF"
}
```

### Champs Optionnels

```json
{
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue du Commerce",
  "numero_maison": "789",
  "code_postal": "BP 5678",
  
  "pays_id": "uuid-du-pays",
  "province_id": "uuid-de-la-province",
  "district_id": "uuid-du-district",
  "quartier_id": "uuid-du-quartier",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "metadonnees": {
    "departement": "Service Client",
    "matricule": "AG-2024-001"
  }
}
```

### Types Autorisés

| Code | Libellé | Description |
|------|---------|-------------|
| `AGENT` | Agent | Agent de service |
| `MARCHAND` | Marchand | Commerçant |
| `ADMIN` | Administrateur | Administrateur |
| `SUPER_ADMIN` | Super Admin | Super administrateur |

**Note:** `CLIENT` n'est PAS autorisé (utiliser l'endpoint d'inscription)

### Réponse

```json
{
  "message": "Utilisateur Agent créé avec succès",
  "utilisateur": {
    "id": "uuid",
    "courriel": "agent@ufaranga.bi",
    "numero_telephone": "+25768987654",
    "prenom": "Pierre",
    "nom_famille": "Nkurunziza",
    "nom_complet": "Pierre Nkurunziza",
    
    "type_utilisateur": "AGENT",
    "type_utilisateur_details": {
      "code": "AGENT",
      "libelle": "Agent",
      "description": "Agent de service"
    },
    
    "niveau_kyc": 2,
    "niveau_kyc_details": {
      "niveau": 2,
      "libelle": "Complet",
      "limite_transaction_journaliere": 2000000.00,
      "limite_solde_maximum": 10000000.00
    },
    
    "statut": "ACTIF",
    "telephone_verifie": true,
    "courriel_verifie": true,
    "est_actif": true
  },
  "cree_par": {
    "courriel": "admin@ufaranga.bi",
    "nom_complet": "Admin Principal",
    "type": "SUPER_ADMIN"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Erreur si Non-Admin

```json
{
  "error": "Accès refusé",
  "message": "Seuls les administrateurs peuvent créer des comptes AGENT/MARCHAND/ADMIN",
  "votre_type": "CLIENT"
}
```

---

## 📊 Utilisation des IDs

### Relations Stockées par ID

Toutes les relations sont stockées par ID dans la table `identite.utilisateurs`:

| Champ Base de Données | Type | Description |
|------------------------|------|-------------|
| `type_utilisateur` | VARCHAR(20) | Code du type (FK vers types_utilisateurs) |
| `niveau_kyc` | INTEGER | Niveau KYC (FK vers niveaux_kyc) |
| `statut` | VARCHAR(20) | Code du statut (FK vers statuts_utilisateurs) |
| `pays` | UUID | ID du pays (FK vers localisation.pays) |
| `province_geo` | UUID | ID de la province (FK vers localisation.provinces) |
| `district` | UUID | ID du district (FK vers localisation.districts) |
| `quartier_geo` | UUID | ID du quartier (FK vers localisation.quartiers) |

### Récupérer les IDs

#### Types d'Utilisateurs
```bash
GET /api/v1/identite/types-utilisateurs/
```

Réponse:
```json
[
  {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard"
  },
  {
    "code": "AGENT",
    "libelle": "Agent",
    "description": "Agent de service"
  }
]
```

#### Niveaux KYC
```bash
GET /api/v1/identite/niveaux-kyc/
```

Réponse:
```json
[
  {
    "niveau": 0,
    "libelle": "Non vérifié",
    "limite_transaction_journaliere": 50000.00
  },
  {
    "niveau": 1,
    "libelle": "Basique",
    "limite_transaction_journaliere": 500000.00
  }
]
```

#### Statuts
```bash
GET /api/v1/identite/statuts-utilisateurs/
```

Réponse:
```json
[
  {
    "code": "ACTIF",
    "libelle": "Actif",
    "permet_connexion": true,
    "permet_transactions": true
  }
]
```

#### Pays
```bash
GET /api/v1/localisation/pays/
```

Réponse:
```json
[
  {
    "id": "uuid-burundi",
    "code_iso_2": "BI",
    "nom": "Burundi"
  }
]
```

---

## 🔐 Sécurité et Vérifications

### Endpoint Inscription (CLIENT)

✅ Aucune authentification requise  
✅ Type forcé à CLIENT  
✅ KYC forcé à 0  
✅ Statut forcé à ACTIF  
✅ Email NON vérifié  
✅ Téléphone NON vérifié  

### Endpoint Admin (AGENT/MARCHAND/ADMIN)

✅ Authentification requise (Bearer token)  
✅ Vérification que l'utilisateur est ADMIN ou SUPER_ADMIN  
✅ Vérification du type dans le payload  
✅ Interdiction de créer un CLIENT  
✅ Possibilité de marquer email/téléphone comme vérifiés  
✅ Traçabilité: qui a créé l'utilisateur  

---

## 🔄 Flux Complet

### Inscription CLIENT

```
1. Frontend appelle POST /api/v1/identite/inscription/
   ↓
2. Backend crée utilisateur CLIENT, KYC 0, ACTIF
   ↓
3. Backend génère tokens JWT
   ↓
4. Frontend sauvegarde tokens
   ↓
5. Utilisateur connecté (non vérifié)
   ↓
6. Frontend demande vérification email/téléphone
```

### Création AGENT par Admin

```
1. Admin connecté appelle POST /api/v1/identite/admin/creer-utilisateur/
   ↓
2. Backend vérifie que l'utilisateur est ADMIN/SUPER_ADMIN
   ↓
3. Backend vérifie le type demandé (AGENT, MARCHAND, ADMIN)
   ↓
4. Backend crée l'utilisateur avec les paramètres fournis
   ↓
5. Backend enregistre qui a créé l'utilisateur
   ↓
6. Backend génère tokens JWT
   ↓
7. Admin reçoit les détails + tokens
   ↓
8. Admin peut transmettre les identifiants au nouvel utilisateur
```

---

## 📝 Exemples cURL

### Inscription CLIENT

```bash
curl -X POST http://127.0.0.1:8000/api/v1/identite/inscription/ \
  -H "Content-Type: application/json" \
  -d '{
    "courriel": "client@example.com",
    "numero_telephone": "+25762046725",
    "mot_de_passe": "ClientPass123!",
    "mot_de_passe_confirmation": "ClientPass123!",
    "prenom": "Jean",
    "nom_famille": "Dupont",
    "date_naissance": "1990-01-15"
  }'
```

### Créer un AGENT (Admin)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/identite/admin/creer-utilisateur/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_access_token>" \
  -d '{
    "courriel": "agent@ufaranga.bi",
    "numero_telephone": "+25768987654",
    "mot_de_passe": "AgentPass789!",
    "mot_de_passe_confirmation": "AgentPass789!",
    "prenom": "Pierre",
    "nom_famille": "Nkurunziza",
    "date_naissance": "1988-03-10",
    "type_utilisateur_id": "AGENT",
    "niveau_kyc_id": 2,
    "statut_id": "ACTIF",
    "telephone_verifie": true,
    "courriel_verifie": true
  }'
```

---

## ✅ Résumé

### Endpoint 1: Inscription CLIENT
- **URL:** `/api/v1/identite/inscription/`
- **Permission:** Public
- **Type:** CLIENT (automatique)
- **KYC:** 0 (automatique)
- **Vérifications:** NON (automatique)

### Endpoint 2: Créer Admin/Agent/Marchand
- **URL:** `/api/v1/identite/admin/creer-utilisateur/`
- **Permission:** Admin uniquement
- **Type:** AGENT, MARCHAND, ADMIN, SUPER_ADMIN
- **KYC:** Configurable
- **Vérifications:** Configurables
- **Traçabilité:** Enregistre qui a créé

**Les deux endpoints utilisent des IDs pour les relations et alimentent complètement la table `identite.utilisateurs`!** 🚀
