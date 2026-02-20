# 🎯 Guide Complet - Créer un Admin/Agent/Marchand

## 📋 Étape 1: Récupérer les IDs de Référence

### 1.1 Types d'Utilisateurs

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
  },
  {
    "code": "MARCHAND",
    "libelle": "Marchand",
    "description": "Commerçant",
    "ordre_affichage": 3,
    "est_actif": true
  },
  {
    "code": "ADMIN",
    "libelle": "Administrateur",
    "description": "Administrateur de la plateforme",
    "ordre_affichage": 4,
    "est_actif": true
  },
  {
    "code": "SUPER_ADMIN",
    "libelle": "Super Administrateur",
    "description": "Super administrateur avec tous les droits",
    "ordre_affichage": 5,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `code` comme `type_utilisateur_id`

---

### 1.2 Niveaux KYC

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
  },
  {
    "niveau": 2,
    "libelle": "Complet",
    "description": "Vérification complète avec justificatifs",
    "limite_transaction_journaliere": 2000000.00,
    "limite_solde_maximum": 10000000.00,
    "documents_requis": [
      "Carte d'identité nationale",
      "Justificatif de domicile",
      "Selfie avec carte d'identité"
    ],
    "est_actif": true
  },
  {
    "niveau": 3,
    "libelle": "Premium",
    "description": "Vérification premium avec tous les documents",
    "limite_transaction_journaliere": 10000000.00,
    "limite_solde_maximum": null,
    "documents_requis": [
      "Carte d'identité nationale",
      "Justificatif de domicile",
      "Justificatif de revenus",
      "Selfie avec carte d'identité"
    ],
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `niveau` comme `niveau_kyc_id`

---

### 1.3 Statuts Utilisateurs

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
  },
  {
    "code": "EN_VERIFICATION",
    "libelle": "En vérification",
    "description": "Compte en cours de vérification",
    "couleur": "#ffc107",
    "permet_connexion": true,
    "permet_transactions": false,
    "ordre_affichage": 2,
    "est_actif": true
  },
  {
    "code": "SUSPENDU",
    "libelle": "Suspendu",
    "description": "Compte suspendu temporairement",
    "couleur": "#fd7e14",
    "permet_connexion": false,
    "permet_transactions": false,
    "ordre_affichage": 3,
    "est_actif": true
  },
  {
    "code": "BLOQUE",
    "libelle": "Bloqué",
    "description": "Compte bloqué",
    "couleur": "#dc3545",
    "permet_connexion": false,
    "permet_transactions": false,
    "ordre_affichage": 4,
    "est_actif": true
  },
  {
    "code": "FERME",
    "libelle": "Fermé",
    "description": "Compte fermé définitivement",
    "couleur": "#6c757d",
    "permet_connexion": false,
    "permet_transactions": false,
    "ordre_affichage": 5,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `code` comme `statut_id`

---

### 1.4 Pays

```bash
GET /api/v1/localisation/pays/
```

**Réponse:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
    "latitude_centre": -3.3731,
    "longitude_centre": 29.9189,
    "autorise_systeme": true,
    "est_actif": true
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "code_iso_2": "RW",
    "code_iso_3": "RWA",
    "nom": "Rwanda",
    "nom_anglais": "Rwanda",
    "latitude_centre": -1.9403,
    "longitude_centre": 29.8739,
    "autorise_systeme": true,
    "est_actif": true
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "code_iso_2": "CD",
    "code_iso_3": "COD",
    "nom": "République Démocratique du Congo",
    "nom_anglais": "Democratic Republic of the Congo",
    "latitude_centre": -4.0383,
    "longitude_centre": 21.7587,
    "autorise_systeme": true,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `id` comme `pays_id`

---

### 1.5 Provinces (par pays)

```bash
GET /api/v1/localisation/provinces/?pays_id=550e8400-e29b-41d4-a716-446655440001
```

**Réponse:**
```json
[
  {
    "id": "650e8400-e29b-41d4-a716-446655440001",
    "pays": "550e8400-e29b-41d4-a716-446655440001",
    "code": "BM",
    "nom": "Bujumbura Mairie",
    "latitude_centre": -3.3822,
    "longitude_centre": 29.3644,
    "autorise_systeme": true,
    "est_actif": true
  },
  {
    "id": "650e8400-e29b-41d4-a716-446655440002",
    "pays": "550e8400-e29b-41d4-a716-446655440001",
    "code": "BR",
    "nom": "Bujumbura Rural",
    "latitude_centre": -3.5000,
    "longitude_centre": 29.5000,
    "autorise_systeme": true,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `id` comme `province_id`

---

### 1.6 Districts (par province)

```bash
GET /api/v1/localisation/districts/?province_id=650e8400-e29b-41d4-a716-446655440001
```

**Réponse:**
```json
[
  {
    "id": "750e8400-e29b-41d4-a716-446655440001",
    "province": "650e8400-e29b-41d4-a716-446655440001",
    "code": "MUK",
    "nom": "Mukaza",
    "latitude_centre": -3.3822,
    "longitude_centre": 29.3644,
    "autorise_systeme": true,
    "est_actif": true
  },
  {
    "id": "750e8400-e29b-41d4-a716-446655440002",
    "province": "650e8400-e29b-41d4-a716-446655440001",
    "code": "MUR",
    "nom": "Muramvya",
    "latitude_centre": -3.2667,
    "longitude_centre": 29.6167,
    "autorise_systeme": true,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `id` comme `district_id`

---

### 1.7 Quartiers (par district)

```bash
GET /api/v1/localisation/quartiers/?district_id=750e8400-e29b-41d4-a716-446655440001
```

**Réponse:**
```json
[
  {
    "id": "850e8400-e29b-41d4-a716-446655440001",
    "district": "750e8400-e29b-41d4-a716-446655440001",
    "code": "ROH",
    "nom": "Rohero",
    "latitude_centre": -3.3700,
    "longitude_centre": 29.3600,
    "autorise_systeme": true,
    "est_actif": true
  },
  {
    "id": "850e8400-e29b-41d4-a716-446655440002",
    "district": "750e8400-e29b-41d4-a716-446655440001",
    "code": "KIN",
    "nom": "Kinindo",
    "latitude_centre": -3.3500,
    "longitude_centre": 29.3500,
    "autorise_systeme": true,
    "est_actif": true
  }
]
```

**Utiliser:** Le champ `id` comme `quartier_id`

---

## 📝 Étape 2: Payload Complet pour Créer un AGENT

### Exemple 1: Agent avec Localisation Complète

```bash
POST /api/v1/identite/admin/creer-utilisateur/
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "courriel": "agent.service@ufaranga.bi",
  "numero_telephone": "+25768987654",
  "mot_de_passe": "AgentSecure123!",
  "mot_de_passe_confirmation": "AgentSecure123!",
  
  "prenom": "Pierre",
  "nom_famille": "Nkurunziza",
  "date_naissance": "1988-03-10",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  
  "type_utilisateur_id": "AGENT",
  "niveau_kyc_id": 2,
  "statut_id": "ACTIF",
  
  "pays_id": "550e8400-e29b-41d4-a716-446655440001",
  "province_id": "650e8400-e29b-41d4-a716-446655440001",
  "district_id": "750e8400-e29b-41d4-a716-446655440001",
  "quartier_id": "850e8400-e29b-41d4-a716-446655440001",
  
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue du Commerce",
  "numero_maison": "123",
  "code_postal": "BP 1234",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "metadonnees": {
    "departement": "Service Client",
    "matricule": "AG-2024-001",
    "date_embauche": "2024-01-15"
  }
}
```

---

### Exemple 2: Marchand Vérifié

```json
{
  "courriel": "boutique.centrale@ufaranga.bi",
  "numero_telephone": "+25761234567",
  "mot_de_passe": "MarchandPass456!",
  "mot_de_passe_confirmation": "MarchandPass456!",
  
  "prenom": "Boutique",
  "nom_famille": "Centrale",
  "date_naissance": "1980-01-01",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  
  "type_utilisateur_id": "MARCHAND",
  "niveau_kyc_id": 3,
  "statut_id": "ACTIF",
  
  "pays_id": "550e8400-e29b-41d4-a716-446655440001",
  "province_id": "650e8400-e29b-41d4-a716-446655440001",
  
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Centre-ville",
  "avenue": "Avenue de la Liberté",
  "numero_maison": "456",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "metadonnees": {
    "nom_commercial": "Boutique Centrale",
    "numero_registre_commerce": "RC/BJA/2020/12345",
    "secteur_activite": "Commerce de détail",
    "tva": "4001234567"
  }
}
```

---

### Exemple 3: Administrateur

```json
{
  "courriel": "admin.regional@ufaranga.bi",
  "numero_telephone": "+25779876543",
  "mot_de_passe": "AdminSecure789!",
  "mot_de_passe_confirmation": "AdminSecure789!",
  
  "prenom": "Marie",
  "nom_famille": "Ndayishimiye",
  "date_naissance": "1985-05-20",
  "lieu_naissance": "Gitega",
  "nationalite": "BI",
  
  "type_utilisateur_id": "ADMIN",
  "niveau_kyc_id": 3,
  "statut_id": "ACTIF",
  
  "pays_id": "550e8400-e29b-41d4-a716-446655440001",
  
  "pays_residence": "BI",
  "ville": "Bujumbura",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "metadonnees": {
    "role": "Administrateur Régional",
    "region": "Bujumbura",
    "niveau_acces": "REGIONAL"
  }
}
```

---

### Exemple 4: Super Admin

```json
{
  "courriel": "superadmin@ufaranga.bi",
  "numero_telephone": "+25762000000",
  "mot_de_passe": "SuperSecure999!",
  "mot_de_passe_confirmation": "SuperSecure999!",
  
  "prenom": "System",
  "nom_famille": "Administrator",
  "date_naissance": "1990-01-01",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  
  "type_utilisateur_id": "SUPER_ADMIN",
  "niveau_kyc_id": 3,
  "statut_id": "ACTIF",
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  
  "metadonnees": {
    "role": "Super Administrateur",
    "niveau_acces": "GLOBAL",
    "permissions": ["ALL"]
  }
}
```

---

## 🔄 Flux Complet avec Frontend

### JavaScript / React

```javascript
// 1. Récupérer les types d'utilisateurs
const getTypesUtilisateurs = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/identite/types-utilisateurs/');
  const types = await response.json();
  return types;
};

// 2. Récupérer les niveaux KYC
const getNiveauxKYC = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/identite/niveaux-kyc/');
  const niveaux = await response.json();
  return niveaux;
};

// 3. Récupérer les statuts
const getStatuts = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/identite/statuts-utilisateurs/');
  const statuts = await response.json();
  return statuts;
};

// 4. Récupérer les pays
const getPays = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/');
  const pays = await response.json();
  return pays;
};

// 5. Récupérer les provinces d'un pays
const getProvinces = async (paysId) => {
  const response = await fetch(`http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=${paysId}`);
  const provinces = await response.json();
  return provinces;
};

// 6. Créer un agent
const creerAgent = async (data, adminToken) => {
  const response = await fetch('http://127.0.0.1:8000/api/v1/identite/admin/creer-utilisateur/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${adminToken}`
    },
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(JSON.stringify(error));
  }
  
  return await response.json();
};

// Utilisation
const creerNouvelAgent = async () => {
  const adminToken = localStorage.getItem('access_token');
  
  const agentData = {
    courriel: 'agent@ufaranga.bi',
    numero_telephone: '+25768987654',
    mot_de_passe: 'AgentPass123!',
    mot_de_passe_confirmation: 'AgentPass123!',
    prenom: 'Pierre',
    nom_famille: 'Nkurunziza',
    date_naissance: '1988-03-10',
    type_utilisateur_id: 'AGENT',
    niveau_kyc_id: 2,
    statut_id: 'ACTIF',
    pays_id: '550e8400-e29b-41d4-a716-446655440001',
    telephone_verifie: true,
    courriel_verifie: true
  };
  
  try {
    const result = await creerAgent(agentData, adminToken);
    console.log('Agent créé:', result);
    return result;
  } catch (error) {
    console.error('Erreur:', error);
    throw error;
  }
};
```

---

## 📊 Tableau Récapitulatif des IDs

| Champ Payload | Type | Source Endpoint | Champ à Utiliser |
|---------------|------|-----------------|------------------|
| `type_utilisateur_id` | string | `/api/v1/identite/types-utilisateurs/` | `code` |
| `niveau_kyc_id` | integer | `/api/v1/identite/niveaux-kyc/` | `niveau` |
| `statut_id` | string | `/api/v1/identite/statuts-utilisateurs/` | `code` |
| `pays_id` | UUID | `/api/v1/localisation/pays/` | `id` |
| `province_id` | UUID | `/api/v1/localisation/provinces/` | `id` |
| `district_id` | UUID | `/api/v1/localisation/districts/` | `id` |
| `quartier_id` | UUID | `/api/v1/localisation/quartiers/` | `id` |

---

## ✅ Checklist de Création

### Avant de créer un Agent/Marchand/Admin:

1. ✅ Récupérer le token d'admin
2. ✅ Vérifier que vous êtes ADMIN ou SUPER_ADMIN
3. ✅ Récupérer les types d'utilisateurs disponibles
4. ✅ Récupérer les niveaux KYC
5. ✅ Récupérer les statuts
6. ✅ Récupérer les pays (si localisation nécessaire)
7. ✅ Récupérer les provinces du pays sélectionné
8. ✅ Préparer le payload avec tous les IDs
9. ✅ Envoyer la requête POST avec le token admin
10. ✅ Vérifier la réponse et sauvegarder les tokens générés

---

## 🎯 Résumé

**Endpoints de référence:**
- Types: `GET /api/v1/identite/types-utilisateurs/`
- KYC: `GET /api/v1/identite/niveaux-kyc/`
- Statuts: `GET /api/v1/identite/statuts-utilisateurs/`
- Pays: `GET /api/v1/localisation/pays/`
- Provinces: `GET /api/v1/localisation/provinces/?pays_id=<uuid>`
- Districts: `GET /api/v1/localisation/districts/?province_id=<uuid>`
- Quartiers: `GET /api/v1/localisation/quartiers/?district_id=<uuid>`

**Endpoint de création:**
- `POST /api/v1/identite/admin/creer-utilisateur/`

**Tous les IDs sont récupérés depuis les endpoints de référence et utilisés dans le payload!** 🚀
