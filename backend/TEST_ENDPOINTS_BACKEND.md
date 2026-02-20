# 🧪 Test des Endpoints Backend

## ⚠️ IMPORTANT: Utiliser le Port 8000 (Backend)

Les endpoints API sont sur le **backend Django** (port 8000), pas sur le frontend React (port 3001).

---

## 🚀 Démarrer le Backend

```bash
python manage.py runserver 8000
```

Le serveur devrait afficher:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 📋 URLs Correctes des Endpoints

### ❌ INCORRECT (Port Frontend)
```
http://localhost:3001/api/v1/identite/statuts-utilisateurs/
```

### ✅ CORRECT (Port Backend)
```
http://localhost:8000/api/v1/identite/statuts-utilisateurs/
```

---

## 🧪 Tests des Endpoints

### 1. Types d'Utilisateurs

```bash
# Dans le navigateur ou Postman
http://localhost:8000/api/v1/identite/types-utilisateurs/

# Avec curl
curl http://localhost:8000/api/v1/identite/types-utilisateurs/
```

**Réponse attendue:**
```json
[
  {
    "code": "CLIENT",
    "libelle": "Client",
    "description": "Client standard de la plateforme",
    "ordre_affichage": 1,
    "est_actif": true
  },
  ...
]
```

---

### 2. Niveaux KYC

```bash
http://localhost:8000/api/v1/identite/niveaux-kyc/

# Avec curl
curl http://localhost:8000/api/v1/identite/niveaux-kyc/
```

**Réponse attendue:**
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
  ...
]
```

---

### 3. Statuts Utilisateurs

```bash
http://localhost:8000/api/v1/identite/statuts-utilisateurs/

# Avec curl
curl http://localhost:8000/api/v1/identite/statuts-utilisateurs/
```

**Réponse attendue:**
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
  ...
]
```

---

### 4. Pays

```bash
http://localhost:8000/api/v1/localisation/pays/

# Avec curl
curl http://localhost:8000/api/v1/localisation/pays/
```

---

### 5. Provinces (avec filtre)

```bash
# Remplacer <pays_id> par l'ID réel du pays
http://localhost:8000/api/v1/localisation/provinces/?pays_id=<pays_id>

# Exemple
curl "http://localhost:8000/api/v1/localisation/provinces/?pays_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

---

### 6. Districts (avec filtre)

```bash
http://localhost:8000/api/v1/localisation/districts/?province_id=<province_id>
```

---

### 7. Quartiers (avec filtre)

```bash
http://localhost:8000/api/v1/localisation/quartiers/?district_id=<district_id>
```

---

## 🔧 Si les Endpoints Ne Marchent Pas

### Vérification 1: Le serveur est-il démarré?

```bash
python manage.py runserver 8000
```

Vous devriez voir:
```
Django version 4.2.16, using settings 'config.settings.base'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Vérification 2: Les URLs sont-elles configurées?

Vérifier que `config/urls.py` contient:
```python
path('api/v1/identite/', include('apps.identite.urls')),
```

---

### Vérification 3: Les tables existent-elles?

```bash
python manage.py shell
```

Puis:
```python
from apps.identite.models import TypeUtilisateur, NiveauKYC, StatutUtilisateur

# Vérifier les types
print(TypeUtilisateur.objects.all())

# Vérifier les niveaux KYC
print(NiveauKYC.objects.all())

# Vérifier les statuts
print(StatutUtilisateur.objects.all())
```

---

### Vérification 4: Tester avec la documentation Swagger

```bash
http://localhost:8000/api/docs/
```

Vous devriez voir l'interface Swagger avec tous les endpoints disponibles.

---

## 🌐 Configuration Frontend pour Appeler le Backend

Dans votre frontend React (port 3001), configurez l'URL de base de l'API:

### Option 1: Fichier .env

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Option 2: Fichier de configuration

```javascript
// src/config/api.js
export const API_BASE_URL = 'http://localhost:8000';
export const API_ENDPOINTS = {
  typesUtilisateurs: '/api/v1/identite/types-utilisateurs/',
  niveauxKYC: '/api/v1/identite/niveaux-kyc/',
  statuts: '/api/v1/identite/statuts-utilisateurs/',
  pays: '/api/v1/localisation/pays/',
  provinces: '/api/v1/localisation/provinces/',
  districts: '/api/v1/localisation/districts/',
  quartiers: '/api/v1/localisation/quartiers/',
  creerAdmin: '/api/v1/identite/admin/creer-utilisateur/',
};
```

### Option 3: Service API

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Ajouter le token automatiquement
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getTypesUtilisateurs = () => 
  api.get('/api/v1/identite/types-utilisateurs/');

export const getNiveauxKYC = () => 
  api.get('/api/v1/identite/niveaux-kyc/');

export const getStatuts = () => 
  api.get('/api/v1/identite/statuts-utilisateurs/');

export const getPays = () => 
  api.get('/api/v1/localisation/pays/');

export const getProvinces = (paysId) => 
  api.get(`/api/v1/localisation/provinces/?pays_id=${paysId}`);

export const creerAdmin = (data) => 
  api.post('/api/v1/identite/admin/creer-utilisateur/', data);

export default api;
```

### Utilisation dans un Composant React

```javascript
import { useEffect, useState } from 'react';
import { getTypesUtilisateurs, getNiveauxKYC, getStatuts } from './services/api';

function CreerUtilisateurForm() {
  const [types, setTypes] = useState([]);
  const [niveaux, setNiveaux] = useState([]);
  const [statuts, setStatuts] = useState([]);

  useEffect(() => {
    // Charger les données de référence
    const loadReferenceData = async () => {
      try {
        const [typesRes, niveauxRes, statutsRes] = await Promise.all([
          getTypesUtilisateurs(),
          getNiveauxKYC(),
          getStatuts(),
        ]);
        
        setTypes(typesRes.data);
        setNiveaux(niveauxRes.data);
        setStatuts(statutsRes.data);
      } catch (error) {
        console.error('Erreur chargement données:', error);
      }
    };

    loadReferenceData();
  }, []);

  return (
    <form>
      <select name="type_utilisateur_id">
        {types.map(type => (
          <option key={type.code} value={type.code}>
            {type.libelle}
          </option>
        ))}
      </select>

      <select name="niveau_kyc_id">
        {niveaux.map(niveau => (
          <option key={niveau.niveau} value={niveau.niveau}>
            {niveau.libelle}
          </option>
        ))}
      </select>

      <select name="statut_id">
        {statuts.map(statut => (
          <option key={statut.code} value={statut.code}>
            {statut.libelle}
          </option>
        ))}
      </select>
    </form>
  );
}
```

---

## 🔒 CORS (Si Erreur de CORS)

Si vous avez une erreur CORS, vérifier `config/settings/base.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

CORS_ALLOW_CREDENTIALS = True
```

---

## ✅ Checklist de Dépannage

1. ✅ Backend Django démarré sur port 8000
2. ✅ Utiliser `http://localhost:8000` (pas 3001)
3. ✅ Les tables de référence existent dans la base
4. ✅ Les URLs sont configurées dans `config/urls.py`
5. ✅ CORS configuré pour autoriser le frontend
6. ✅ Frontend configuré pour appeler le bon port

---

## 📝 Résumé

**Backend (Django):** Port 8000
- API: `http://localhost:8000/api/v1/...`
- Docs: `http://localhost:8000/api/docs/`

**Frontend (React):** Port 3001
- Interface: `http://localhost:3001`
- Appelle le backend sur port 8000

**Les endpoints API sont TOUJOURS sur le port 8000 (backend)!** 🚀
