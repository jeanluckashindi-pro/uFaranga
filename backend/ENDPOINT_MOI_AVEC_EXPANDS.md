# 📱 Endpoint `/api/v1/identite/moi/` - Avec Expands Complets

## 🎯 Objectif

L'endpoint `/api/v1/identite/moi/` retourne maintenant TOUTES les informations de l'utilisateur connecté avec des **expands** pour voir les détails complets de chaque relation.

---

## 📊 Structure de la Réponse

### Champs de base

```json
{
  "id": "uuid",
  "courriel": "user@example.com",
  "numero_telephone": "+25762046725",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "nom_complet": "Jean Dupont",
  "date_naissance": "1990-01-15",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "pays_residence": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue de la Liberté",
  "numero_maison": "123",
  "adresse_complete": "Avenue de la Liberté, 123, Rohero, Mukaza, Bujumbura",
  "code_postal": "",
  
  "telephone_verifie": true,
  "telephone_verifie_le": "2024-01-15T10:30:00Z",
  "courriel_verifie": true,
  "courriel_verifie_le": "2024-01-15T10:25:00Z",
  
  "niveau_kyc": 1,
  "date_validation_kyc": "2024-01-15T11:00:00Z",
  "validateur_kyc_id": null,
  
  "type_utilisateur": "CLIENT",
  "statut": "ACTIF",
  "raison_statut": "",
  
  "nombre_tentatives_connexion": 0,
  "bloque_jusqua": null,
  "double_auth_activee": false,
  
  "est_actif": true,
  "date_creation": "2024-01-15T10:00:00Z",
  "date_modification": "2024-01-15T10:30:00Z",
  "derniere_connexion": "2024-02-20T08:00:00Z",
  "derniere_modification_mdp": "2024-01-15T10:00:00Z",
  
  "is_staff": false,
  "is_superuser": false,
  
  "metadonnees": {}
}
```

---

## 🔍 EXPANDS - Détails Complets

### 1. `type_utilisateur_details` - Type d'Utilisateur

Détails complets du type d'utilisateur (CLIENT, AGENT, MARCHAND, etc.)

```json
{
  "type_utilisateur": "CLIENT",
  "type_utilisateur_details": {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard de la plateforme",
    "ordre_affichage": 1,
    "est_actif": true
  }
}
```

**Valeurs possibles:**
- `CLIENT` - Client standard
- `AGENT` - Agent de service
- `MARCHAND` - Commerçant
- `ADMIN` - Administrateur
- `SUPER_ADMIN` - Super administrateur
- `SYSTEME` - Compte système

---

### 2. `niveau_kyc_details` - Niveau KYC

Détails complets du niveau KYC avec limites de transaction

```json
{
  "niveau_kyc": 1,
  "niveau_kyc_details": {
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
}
```

**Niveaux disponibles:**
- `0` - Non vérifié (limite: 50 000 BIF/jour)
- `1` - Basique (limite: 500 000 BIF/jour)
- `2` - Complet (limite: 2 000 000 BIF/jour)
- `3` - Premium (limite: 10 000 000 BIF/jour)

---

### 3. `statut_details` - Statut du Compte

Détails complets du statut avec permissions

```json
{
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
  }
}
```

**Statuts possibles:**
- `ACTIF` - Compte actif (vert #28a745)
- `EN_VERIFICATION` - En cours de vérification (orange #ffc107)
- `SUSPENDU` - Compte suspendu temporairement (orange #fd7e14)
- `BLOQUE` - Compte bloqué (rouge #dc3545)
- `FERME` - Compte fermé définitivement (gris #6c757d)

---

### 4. `numeros_telephone` - Liste des Numéros

Tous les numéros de téléphone de l'utilisateur avec détails

```json
{
  "numeros_telephone": [
    {
      "id": "uuid-1",
      "pays_code_iso_2": "BI",
      "pays_nom": "Burundi",
      "code_pays": "+257",
      "numero_national": "62046725",
      "numero_complet": "+25762046725",
      "numero_formate": "+257 62 04 67 25",
      "type_numero": "MOBILE",
      "usage": "PERSONNEL",
      "est_principal": true,
      "est_verifie": true,
      "date_verification": "2024-01-15T10:30:00Z",
      "methode_verification": "SMS",
      "statut": "ACTIF",
      "raison_statut": "",
      "operateur": "Econet",
      "type_ligne": "PREPAYE",
      "nombre_connexions_reussies": 45,
      "derniere_connexion": "2024-02-20T08:00:00Z",
      "date_creation": "2024-01-15T10:00:00Z",
      "date_modification": "2024-01-15T10:30:00Z"
    },
    {
      "id": "uuid-2",
      "pays_code_iso_2": "BI",
      "pays_nom": "Burundi",
      "code_pays": "+257",
      "numero_national": "79123456",
      "numero_complet": "+25779123456",
      "numero_formate": "+257 79 12 34 56",
      "type_numero": "MOBILE",
      "usage": "PROFESSIONNEL",
      "est_principal": false,
      "est_verifie": true,
      "date_verification": "2024-01-20T14:00:00Z",
      "methode_verification": "SMS",
      "statut": "ACTIF",
      "raison_statut": "",
      "operateur": "Lumitel",
      "type_ligne": "PREPAYE",
      "nombre_connexions_reussies": 12,
      "derniere_connexion": "2024-02-18T15:30:00Z",
      "date_creation": "2024-01-20T13:45:00Z",
      "date_modification": "2024-01-20T14:00:00Z"
    }
  ]
}
```

**Informations par numéro:**
- `est_principal` - Indique le numéro principal (un seul par utilisateur)
- `est_verifie` - Numéro vérifié par SMS
- `type_numero` - MOBILE, FIXE, VOIP
- `usage` - PERSONNEL, PROFESSIONNEL, URGENCE
- `statut` - ACTIF, SUSPENDU, BLOQUE, SUPPRIME
- `operateur` - Econet, Lumitel, Smart (Burundi)
- `type_ligne` - PREPAYE, POSTPAYE

---

### 5. `pays_details` - Détails du Pays

Informations complètes sur le pays avec téléphonie et devise

```json
{
  "pays_details": {
    "id": "uuid",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
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
    }
  }
}
```

---

### 6. `province_details` - Détails de la Province

```json
{
  "province_details": {
    "id": "uuid",
    "code": "BM",
    "nom": "Bujumbura Mairie"
  }
}
```

---

### 7. `district_details` - Détails du District

```json
{
  "district_details": {
    "id": "uuid",
    "code": "MUK",
    "nom": "Mukaza"
  }
}
```

---

### 8. `quartier_details` - Détails du Quartier

```json
{
  "quartier_details": {
    "id": "uuid",
    "code": "ROH",
    "nom": "Rohero"
  }
}
```

---

### 9. `profil` - Profil et Préférences

```json
{
  "profil": {
    "id": "uuid",
    "url_avatar": "https://cdn.example.com/avatars/user123.jpg",
    "url_photo_couverture": "",
    "biographie": "Utilisateur de uFaranga depuis 2024",
    "langue": "fr",
    "devise_preferee": "BIF",
    "fuseau_horaire": "Africa/Bujumbura",
    "format_date": "DD/MM/YYYY",
    "format_heure": "24h",
    "notifications_courriel": true,
    "notifications_sms": true,
    "notifications_push": true,
    "notifications_transactions": true,
    "notifications_marketing": false,
    "profil_public": false,
    "afficher_telephone": false,
    "afficher_courriel": false,
    "date_creation": "2024-01-15T10:00:00Z",
    "date_modification": "2024-01-15T10:00:00Z",
    "metadonnees": {}
  }
}
```

---

## 📝 Exemple de Réponse Complète

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "courriel": "jean.dupont@example.com",
  "numero_telephone": "+25762046725",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "nom_complet": "Jean Dupont",
  "date_naissance": "1990-01-15",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "pays_residence": "BI",
  
  "type_utilisateur": "CLIENT",
  "type_utilisateur_details": {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard de la plateforme",
    "ordre_affichage": 1,
    "est_actif": true
  },
  
  "niveau_kyc": 1,
  "niveau_kyc_details": {
    "niveau": 1,
    "libelle": "Basique",
    "description": "Vérification basique avec pièce d'identité",
    "limite_transaction_journaliere": 500000.00,
    "limite_solde_maximum": 2000000.00,
    "documents_requis": ["Carte d'identité nationale", "Selfie"],
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
  
  "numeros_telephone": [
    {
      "id": "uuid-1",
      "pays_code_iso_2": "BI",
      "pays_nom": "Burundi",
      "code_pays": "+257",
      "numero_national": "62046725",
      "numero_complet": "+25762046725",
      "numero_formate": "+257 62 04 67 25",
      "type_numero": "MOBILE",
      "usage": "PERSONNEL",
      "est_principal": true,
      "est_verifie": true,
      "date_verification": "2024-01-15T10:30:00Z",
      "methode_verification": "SMS",
      "statut": "ACTIF",
      "operateur": "Econet",
      "type_ligne": "PREPAYE",
      "nombre_connexions_reussies": 45,
      "derniere_connexion": "2024-02-20T08:00:00Z",
      "date_creation": "2024-01-15T10:00:00Z"
    }
  ],
  
  "pays_details": {
    "id": "uuid",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
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
    }
  },
  
  "province_details": {
    "id": "uuid",
    "code": "BM",
    "nom": "Bujumbura Mairie"
  },
  
  "district_details": {
    "id": "uuid",
    "code": "MUK",
    "nom": "Mukaza"
  },
  
  "quartier_details": {
    "id": "uuid",
    "code": "ROH",
    "nom": "Rohero"
  },
  
  "profil": {
    "id": "uuid",
    "url_avatar": "https://cdn.example.com/avatars/user123.jpg",
    "langue": "fr",
    "devise_preferee": "BIF",
    "fuseau_horaire": "Africa/Bujumbura",
    "notifications_courriel": true,
    "notifications_sms": true,
    "notifications_push": true,
    "notifications_transactions": true,
    "notifications_marketing": false,
    "profil_public": false
  },
  
  "telephone_verifie": true,
  "courriel_verifie": true,
  "double_auth_activee": false,
  "est_actif": true,
  "date_creation": "2024-01-15T10:00:00Z",
  "derniere_connexion": "2024-02-20T08:00:00Z"
}
```

---

## 🚀 Utilisation

### Requête

```bash
GET /api/v1/identite/moi/
Authorization: Bearer <token>
```

### Réponse

Toutes les informations de l'utilisateur avec les expands automatiquement inclus.

---

## ✅ Avantages

1. **Une seule requête** - Toutes les infos en un appel
2. **Détails complets** - Plus besoin de faire des requêtes supplémentaires
3. **Type utilisateur** - Voir les permissions et le rôle
4. **Niveau KYC** - Voir les limites de transaction
5. **Statut** - Voir si le compte peut se connecter/transacter
6. **Numéros multiples** - Liste de tous les numéros avec leur statut
7. **Localisation** - Détails complets du pays, province, district, quartier
8. **Téléphonie** - Infos de validation par pays (regex, format, opérateurs)

---

## 📱 Cas d'Usage Frontend

### Afficher le type d'utilisateur avec badge

```javascript
const { type_utilisateur_details } = userData;

<Badge color={type_utilisateur_details.code === 'CLIENT' ? 'blue' : 'green'}>
  {type_utilisateur_details.libelle}
</Badge>
```

### Afficher les limites KYC

```javascript
const { niveau_kyc_details } = userData;

<div>
  <p>Niveau: {niveau_kyc_details.libelle}</p>
  <p>Limite journalière: {niveau_kyc_details.limite_transaction_journaliere} {userData.pays_details.devise.symbole}</p>
  <p>Solde maximum: {niveau_kyc_details.limite_solde_maximum} {userData.pays_details.devise.symbole}</p>
</div>
```

### Afficher le statut avec couleur

```javascript
const { statut_details } = userData;

<Badge style={{ backgroundColor: statut_details.couleur }}>
  {statut_details.libelle}
</Badge>

{!statut_details.permet_transactions && (
  <Alert type="warning">
    Vous ne pouvez pas effectuer de transactions
  </Alert>
)}
```

### Afficher les numéros de téléphone

```javascript
const { numeros_telephone } = userData;

{numeros_telephone.map(numero => (
  <div key={numero.id}>
    <p>
      {numero.numero_formate}
      {numero.est_principal && <Badge>Principal</Badge>}
      {numero.est_verifie && <Icon name="check" color="green" />}
    </p>
    <p>Opérateur: {numero.operateur}</p>
  </div>
))}
```

---

## 🎯 Résumé

L'endpoint `/api/v1/identite/moi/` retourne maintenant:

✅ Informations de base de l'utilisateur  
✅ **Type utilisateur** avec détails complets (CLIENT, AGENT, etc.)  
✅ **Niveau KYC** avec limites de transaction  
✅ **Statut** avec permissions (connexion, transactions)  
✅ **Liste des numéros** de téléphone avec vérification  
✅ **Détails du pays** avec téléphonie et devise  
✅ **Localisation complète** (province, district, quartier)  
✅ **Profil** avec préférences et notifications  

Tout en une seule requête! 🚀
