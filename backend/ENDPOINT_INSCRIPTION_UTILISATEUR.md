# 📝 Endpoint d'Inscription - Créer un Nouvel Utilisateur

## 🎯 Endpoint Principal

```
POST /api/v1/authentification/inscription/
```

**Permission:** Aucune authentification requise (AllowAny)

---

## 📋 Champs Requis

### Champs Obligatoires

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `email` | string | Adresse e-mail unique | `jean.dupont@example.com` |
| `password` | string | Mot de passe (min 8 caractères) | `MonMotDePasse123!` |
| `password_confirm` | string | Confirmation du mot de passe | `MonMotDePasse123!` |
| `first_name` | string | Prénom | `Jean` |
| `last_name` | string | Nom de famille | `Dupont` |

### Champs Optionnels

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `username` | string | Nom d'utilisateur (auto-généré si absent) | `jeandupont` |
| `phone_number` | string | Numéro de téléphone | `+25762046725` |
| `country` | string | Pays | `BI` |
| `city` | string | Ville | `Bujumbura` |

---

## 📝 Exemple de Requête

### Inscription Minimale (Champs Obligatoires)

```bash
POST /api/v1/authentification/inscription/
Content-Type: application/json

{
  "email": "jean.dupont@example.com",
  "password": "MonMotDePasse123!",
  "password_confirm": "MonMotDePasse123!",
  "first_name": "Jean",
  "last_name": "Dupont"
}
```

### Inscription Complète (Tous les Champs)

```bash
POST /api/v1/authentification/inscription/
Content-Type: application/json

{
  "email": "jean.dupont@example.com",
  "username": "jeandupont",
  "password": "MonMotDePasse123!",
  "password_confirm": "MonMotDePasse123!",
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone_number": "+25762046725",
  "country": "BI",
  "city": "Bujumbura"
}
```

---

## ✅ Réponse en Cas de Succès

**Status:** `201 Created`

```json
{
  "message": "Inscription réussie",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "jean.dupont@example.com",
    "username": "jeandupont",
    "first_name": "Jean",
    "last_name": "Dupont",
    "phone_number": "+25762046725",
    "country": "BI",
    "city": "Bujumbura",
    "kyc_level": 0,
    "is_phone_verified": false,
    "is_email_verified": false,
    "is_active": true,
    "date_joined": "2024-02-20T10:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Note:** Les tokens JWT sont automatiquement générés pour connexion immédiate après inscription.

---

## ❌ Erreurs Possibles

### 1. Email Déjà Utilisé

**Status:** `400 Bad Request`

```json
{
  "email": [
    "Un utilisateur avec cet email existe déjà."
  ]
}
```

### 2. Mots de Passe Non Identiques

**Status:** `400 Bad Request`

```json
{
  "password_confirm": [
    "Les mots de passe ne correspondent pas."
  ]
}
```

### 3. Mot de Passe Trop Faible

**Status:** `400 Bad Request`

```json
{
  "password": [
    "Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.",
    "Ce mot de passe est trop courant.",
    "Ce mot de passe est entièrement numérique."
  ]
}
```

### 4. Téléphone Déjà Utilisé

**Status:** `400 Bad Request`

```json
{
  "phone_number": [
    "Ce numéro de téléphone est déjà utilisé."
  ]
}
```

### 5. Champs Manquants

**Status:** `400 Bad Request`

```json
{
  "email": [
    "Ce champ est obligatoire."
  ],
  "first_name": [
    "Ce champ est obligatoire."
  ]
}
```

---

## 🔐 Règles de Validation

### Mot de Passe

Le mot de passe doit respecter les règles suivantes:

- ✅ Minimum 8 caractères
- ✅ Ne pas être trop courant (ex: "password123")
- ✅ Ne pas être entièrement numérique
- ✅ Ne pas être trop similaire aux informations personnelles

### Email

- ✅ Format valide (ex: `user@example.com`)
- ✅ Unique dans le système
- ✅ Converti en minuscules automatiquement

### Téléphone

- ✅ Format international recommandé (ex: `+25762046725`)
- ✅ Unique dans le système (si fourni)
- ✅ Optionnel

---

## 🚀 Après l'Inscription

### 1. Connexion Automatique

L'utilisateur reçoit immédiatement des tokens JWT et peut utiliser l'application sans se reconnecter.

### 2. Profil Créé Automatiquement

Un profil utilisateur (`UserProfile`) est créé automatiquement avec des valeurs par défaut.

### 3. Niveau KYC Initial

L'utilisateur commence avec `kyc_level = 0` (Non vérifié).

### 4. Vérifications Requises

Pour utiliser pleinement la plateforme, l'utilisateur doit:
- ✅ Vérifier son email
- ✅ Vérifier son téléphone
- ✅ Compléter son profil KYC

---

## 📱 Exemple d'Utilisation Frontend

### JavaScript / Fetch

```javascript
async function inscrireUtilisateur(data) {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/authentification/inscription/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errors = await response.json();
      throw new Error(JSON.stringify(errors));
    }

    const result = await response.json();
    
    // Sauvegarder les tokens
    localStorage.setItem('access_token', result.tokens.access);
    localStorage.setItem('refresh_token', result.tokens.refresh);
    
    // Rediriger vers le dashboard
    window.location.href = '/dashboard';
    
    return result;
  } catch (error) {
    console.error('Erreur inscription:', error);
    throw error;
  }
}

// Utilisation
const userData = {
  email: 'jean.dupont@example.com',
  password: 'MonMotDePasse123!',
  password_confirm: 'MonMotDePasse123!',
  first_name: 'Jean',
  last_name: 'Dupont',
  phone_number: '+25762046725',
  country: 'BI',
  city: 'Bujumbura'
};

inscrireUtilisateur(userData)
  .then(result => {
    console.log('Inscription réussie:', result);
  })
  .catch(error => {
    console.error('Échec inscription:', error);
  });
```

### React / Axios

```javascript
import axios from 'axios';

const inscrireUtilisateur = async (userData) => {
  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/v1/authentification/inscription/',
      userData
    );
    
    // Sauvegarder les tokens
    localStorage.setItem('access_token', response.data.tokens.access);
    localStorage.setItem('refresh_token', response.data.tokens.refresh);
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // Erreurs de validation
      throw error.response.data;
    }
    throw error;
  }
};

// Composant React
function FormulaireInscription() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    country: 'BI',
    city: ''
  });
  
  const [errors, setErrors] = useState({});
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    
    try {
      const result = await inscrireUtilisateur(formData);
      console.log('Inscription réussie:', result);
      // Rediriger
      navigate('/dashboard');
    } catch (error) {
      setErrors(error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Champs du formulaire */}
      {errors.email && <span className="error">{errors.email[0]}</span>}
      {/* ... */}
    </form>
  );
}
```

---

## 🔄 Flux Complet d'Inscription

```
1. Utilisateur remplit le formulaire
   ↓
2. Frontend envoie POST /api/v1/authentification/inscription/
   ↓
3. Backend valide les données
   ↓
4. Backend crée l'utilisateur (users.User)
   ↓
5. Backend crée le profil (UserProfile)
   ↓
6. Backend génère les tokens JWT
   ↓
7. Backend retourne user + tokens
   ↓
8. Frontend sauvegarde les tokens
   ↓
9. Frontend redirige vers dashboard
   ↓
10. Utilisateur connecté automatiquement
```

---

## 🎯 Prochaines Étapes Après Inscription

### 1. Vérifier l'Email

```bash
POST /api/v1/authentification/envoyer-code-confirmation/
{
  "telephone": "+25762046725",
  "prenom": "Jean"
}
```

### 2. Vérifier le Téléphone

```bash
POST /api/v1/authentification/verifier-code-confirmation/
{
  "telephone": "+25762046725",
  "code": "12345"
}
```

### 3. Compléter le Profil

```bash
PATCH /api/v1/identite/moi/
Authorization: Bearer <access_token>

{
  "date_naissance": "1990-01-15",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero"
}
```

### 4. Augmenter le Niveau KYC

Pour augmenter le niveau KYC, l'utilisateur doit:
- Fournir une pièce d'identité
- Prendre un selfie
- Attendre la validation par un administrateur

---

## 📊 Types d'Utilisateurs Disponibles

Après inscription, l'utilisateur est automatiquement de type `CLIENT`. Les autres types sont:

| Type | Code | Description | Limite Numéros |
|------|------|-------------|----------------|
| Client | `CLIENT` | Utilisateur standard | 3 |
| Agent | `AGENT` | Agent de service | 5 |
| Marchand | `MARCHAND` | Commerçant | 5 |
| Admin | `ADMIN` | Administrateur | Illimité |
| Super Admin | `SUPER_ADMIN` | Super administrateur | Illimité |
| Système | `SYSTEME` | Compte système | Illimité |

**Note:** Le type d'utilisateur ne peut être changé que par un administrateur.

---

## 🔒 Sécurité

### Données Sensibles

- ✅ Le mot de passe est hashé avec PBKDF2
- ✅ Le mot de passe n'est jamais retourné dans les réponses
- ✅ Les tokens JWT expirent après 60 minutes (access) et 7 jours (refresh)

### Protection CSRF

- ✅ Endpoint protégé contre les attaques CSRF
- ✅ Validation stricte des données
- ✅ Rate limiting recommandé en production

---

## ✅ Résumé

**Endpoint:** `POST /api/v1/authentification/inscription/`

**Champs obligatoires:**
- email
- password
- password_confirm
- first_name
- last_name

**Retourne:**
- Informations utilisateur
- Tokens JWT (access + refresh)
- Message de succès

**Après inscription:**
- Connexion automatique
- Profil créé
- KYC niveau 0
- Vérifications requises (email, téléphone)

L'utilisateur peut immédiatement utiliser l'application avec les tokens reçus! 🚀
