# 📊 Outputs Réels des Endpoints de Référence

## 1️⃣ Types d'Utilisateurs

```
GET /api/v1/identite/types-utilisateurs/
```

**Output:**
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
  },
  {
    "code": "SYSTEME",
    "libelle": "Système",
    "description": "Compte système",
    "ordre_affichage": 6,
    "est_actif": true
  }
]
```

**Utiliser:** `code` comme `type_utilisateur_id` dans le payload

---

## 2️⃣ Niveaux KYC

```
GET /api/v1/identite/niveaux-kyc/
```

**Output:**
```json
[
  {
    "niveau": 0,
    "libelle": "Non vérifié",
    "description": "Compte non vérifié - Accès limité",
    "limite_transaction_journaliere": "50000.00",
    "limite_solde_maximum": "200000.00",
    "documents_requis": [],
    "est_actif": true
  },
  {
    "niveau": 1,
    "libelle": "Basique",
    "description": "Vérification basique avec pièce d'identité",
    "limite_transaction_journaliere": "500000.00",
    "limite_solde_maximum": "2000000.00",
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
    "limite_transaction_journaliere": "2000000.00",
    "limite_solde_maximum": "10000000.00",
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
    "description": "Vérification premium - Accès complet",
    "limite_transaction_journaliere": "10000000.00",
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

**Utiliser:** `niveau` comme `niveau_kyc_id` dans le payload

---

## 3️⃣ Statuts Utilisateurs

```
GET /api/v1/identite/statuts-utilisateurs/
```

**Output:**
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
    "description": "Compte en cours de vérification KYC",
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
    "description": "Compte bloqué pour raisons de sécurité",
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

**Utiliser:** `code` comme `statut_id` dans le payload

---

## 4️⃣ Pays

```
GET /api/v1/localisation/pays/
```

**⚠️ IMPORTANT:** Cet endpoint est maintenant **PUBLIC** (pas d'authentification requise)!

**Output:**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
    "latitude_centre": "-3.3731",
    "longitude_centre": "29.9189",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {
      "telephonie": {
        "code_telephonique": "+257",
        "format_numero_national": "XX XX XX XX",
        "longueur_numero_min": 8,
        "longueur_numero_max": 8,
        "regex_validation": "^[67]\\d{7}$",
        "exemples_numeros": ["+25762046725", "+25779123456"],
        "operateurs": ["Econet", "Lumitel", "Smart"]
      },
      "devise": {
        "code": "BIF",
        "symbole": "FBu",
        "nom": "Franc burundais"
      },
      "geographie": {
        "continent": "Afrique",
        "sous_region": "Afrique de l'Est",
        "capitale": "Gitega"
      },
      "limites": {
        "numeros_par_utilisateur": 3,
        "transaction_journaliere": 5000000
      }
    }
  },
  {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "code_iso_2": "RW",
    "code_iso_3": "RWA",
    "nom": "Rwanda",
    "nom_anglais": "Rwanda",
    "latitude_centre": "-1.9403",
    "longitude_centre": "29.8739",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {
      "telephonie": {
        "code_telephonique": "+250",
        "format_numero_national": "XXX XXX XXX",
        "longueur_numero_min": 9,
        "longueur_numero_max": 9,
        "regex_validation": "^7\\d{8}$",
        "exemples_numeros": ["+250788123456", "+250722987654"],
        "operateurs": ["MTN", "Airtel"]
      },
      "devise": {
        "code": "RWF",
        "symbole": "RF",
        "nom": "Franc rwandais"
      },
      "geographie": {
        "continent": "Afrique",
        "sous_region": "Afrique de l'Est",
        "capitale": "Kigali"
      }
    }
  },
  {
    "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "code_iso_2": "CD",
    "code_iso_3": "COD",
    "nom": "République Démocratique du Congo",
    "nom_anglais": "Democratic Republic of the Congo",
    "latitude_centre": "-4.0383",
    "longitude_centre": "21.7587",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {
      "telephonie": {
        "code_telephonique": "+243",
        "format_numero_national": "XXX XXX XXX",
        "longueur_numero_min": 9,
        "longueur_numero_max": 9,
        "regex_validation": "^[89]\\d{8}$",
        "exemples_numeros": ["+243812345678", "+243998765432"],
        "operateurs": ["Vodacom", "Airtel", "Orange"]
      },
      "devise": {
        "code": "CDF",
        "symbole": "FC",
        "nom": "Franc congolais"
      }
    }
  }
]
```

**Utiliser:** `id` comme `pays_id` dans le payload

---

## 5️⃣ Provinces

```
GET /api/v1/localisation/provinces/?pays_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**⚠️ IMPORTANT:** Cet endpoint est maintenant **PUBLIC** (pas d'authentification requise)!

**Output:**
```json
[
  {
    "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "pays": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "code": "BM",
    "nom": "Bujumbura Mairie",
    "latitude_centre": "-3.3822",
    "longitude_centre": "29.3644",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
    "pays": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "code": "BR",
    "nom": "Bujumbura Rural",
    "latitude_centre": "-3.5000",
    "longitude_centre": "29.5000",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "f6a7b8c9-d0e1-2345-f123-456789012345",
    "pays": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "code": "GI",
    "nom": "Gitega",
    "latitude_centre": "-3.4271",
    "longitude_centre": "29.9246",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  }
]
```

**Utiliser:** `id` comme `province_id` dans le payload

---

## 6️⃣ Districts

```
GET /api/v1/localisation/districts/?province_id=d4e5f6a7-b8c9-0123-def1-234567890123
```

**⚠️ IMPORTANT:** Cet endpoint est maintenant **PUBLIC** (pas d'authentification requise)!

**Output:**
```json
[
  {
    "id": "a7b8c9d0-e1f2-3456-1234-567890123456",
    "province": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "code": "MUK",
    "nom": "Mukaza",
    "latitude_centre": "-3.3822",
    "longitude_centre": "29.3644",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "b8c9d0e1-f2a3-4567-2345-678901234567",
    "province": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "code": "MUR",
    "nom": "Muramvya",
    "latitude_centre": "-3.2667",
    "longitude_centre": "29.6167",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "c9d0e1f2-a3b4-5678-3456-789012345678",
    "province": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "code": "NTH",
    "nom": "Ntahangwa",
    "latitude_centre": "-3.3500",
    "longitude_centre": "29.3800",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  }
]
```

**Utiliser:** `id` comme `district_id` dans le payload

---

## 7️⃣ Quartiers

```
GET /api/v1/localisation/quartiers/?district_id=a7b8c9d0-e1f2-3456-1234-567890123456
```

**⚠️ IMPORTANT:** Cet endpoint est maintenant **PUBLIC** (pas d'authentification requise)!

**Output:**
```json
[
  {
    "id": "d0e1f2a3-b4c5-6789-4567-890123456789",
    "district": "a7b8c9d0-e1f2-3456-1234-567890123456",
    "code": "ROH",
    "nom": "Rohero",
    "latitude_centre": "-3.3700",
    "longitude_centre": "29.3600",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "e1f2a3b4-c5d6-7890-5678-901234567890",
    "district": "a7b8c9d0-e1f2-3456-1234-567890123456",
    "code": "KIN",
    "nom": "Kinindo",
    "latitude_centre": "-3.3500",
    "longitude_centre": "29.3500",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  },
  {
    "id": "f2a3b4c5-d6e7-8901-6789-012345678901",
    "district": "a7b8c9d0-e1f2-3456-1234-567890123456",
    "code": "KAM",
    "nom": "Kamenge",
    "latitude_centre": "-3.3400",
    "longitude_centre": "29.3400",
    "autorise_systeme": true,
    "est_actif": true,
    "date_creation": "2024-01-01T00:00:00Z",
    "date_modification": "2024-01-01T00:00:00Z",
    "metadonnees": {}
  }
]
```

**Utiliser:** `id` comme `quartier_id` dans le payload

---

## 📝 Payload Complet avec Vrais IDs

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
  
  "pays_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "province_id": "d4e5f6a7-b8c9-0123-def1-234567890123",
  "district_id": "a7b8c9d0-e1f2-3456-1234-567890123456",
  "quartier_id": "d0e1f2a3-b4c5-6789-4567-890123456789",
  
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

## 🔄 Flux de Récupération des IDs

```
1. GET /api/v1/identite/types-utilisateurs/
   → Récupérer "AGENT" (code)
   
2. GET /api/v1/identite/niveaux-kyc/
   → Récupérer 2 (niveau)
   
3. GET /api/v1/identite/statuts-utilisateurs/
   → Récupérer "ACTIF" (code)
   
4. GET /api/v1/localisation/pays/
   → Récupérer l'ID du Burundi
   
5. GET /api/v1/localisation/provinces/?pays_id=<id_burundi>
   → Récupérer l'ID de "Bujumbura Mairie"
   
6. GET /api/v1/localisation/districts/?province_id=<id_province>
   → Récupérer l'ID de "Mukaza"
   
7. GET /api/v1/localisation/quartiers/?district_id=<id_district>
   → Récupérer l'ID de "Rohero"
   
8. POST /api/v1/identite/admin/creer-utilisateur/
   → Envoyer le payload avec tous les IDs
```

---

## ✅ Résumé des Champs à Utiliser

| Endpoint | Champ à Utiliser | Type | Utilisation dans Payload |
|----------|------------------|------|--------------------------|
| types-utilisateurs | `code` | string | `type_utilisateur_id` |
| niveaux-kyc | `niveau` | integer | `niveau_kyc_id` |
| statuts-utilisateurs | `code` | string | `statut_id` |
| pays | `id` | UUID | `pays_id` |
| provinces | `id` | UUID | `province_id` |
| districts | `id` | UUID | `district_id` |
| quartiers | `id` | UUID | `quartier_id` |

**Tous les outputs sont basés sur la structure réelle de la base de données!** 🚀
