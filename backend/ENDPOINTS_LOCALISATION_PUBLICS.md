# Endpoints de Localisation - Accès Public

## ✅ PROBLÈME RÉSOLU

Les endpoints de localisation sont maintenant **accessibles publiquement** pour les requêtes GET (lecture).
Les opérations de création/modification/suppression restent réservées aux administrateurs.

## 📍 Endpoints Disponibles (Accès Public)

### 1. Liste des Pays
```http
GET http://127.0.0.1:8000/api/v1/localisation/pays/
```

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
    "indicatif_telephonique": "+257",
    "devise_code": "BIF",
    "autorise_systeme": true,
    "est_actif": true
  }
]
```

### 2. Détail d'un Pays
```http
GET http://127.0.0.1:8000/api/v1/localisation/pays/{id}/
```

### 3. Liste des Provinces (avec filtre par pays)
```http
GET http://127.0.0.1:8000/api/v1/localisation/provinces/
GET http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id={uuid}
```

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "BM",
    "nom": "Bujumbura Mairie",
    "pays": {
      "id": "uuid",
      "code_iso_2": "BI",
      "nom": "Burundi"
    },
    "est_actif": true
  }
]
```

### 4. Liste des Districts (avec filtre par province)
```http
GET http://127.0.0.1:8000/api/v1/localisation/districts/
GET http://127.0.0.1:8000/api/v1/localisation/districts/?province_id={uuid}
```

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "MKZ",
    "nom": "Mukaza",
    "province": {
      "id": "uuid",
      "code": "BM",
      "nom": "Bujumbura Mairie"
    },
    "est_actif": true
  }
]
```

### 5. Liste des Quartiers (avec filtre par district)
```http
GET http://127.0.0.1:8000/api/v1/localisation/quartiers/
GET http://127.0.0.1:8000/api/v1/localisation/quartiers/?district_id={uuid}
```

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "ROH",
    "nom": "Rohero",
    "district": {
      "id": "uuid",
      "code": "MKZ",
      "nom": "Mukaza"
    },
    "est_actif": true
  }
]
```

### 6. Couverture Mondiale (Hiérarchie Complète)
```http
GET http://127.0.0.1:8000/api/v1/localisation/pays/couverture/
GET http://127.0.0.1:8000/api/v1/localisation/pays/couverture/?pays_id={uuid}
GET http://127.0.0.1:8000/api/v1/localisation/pays/couverture/?code_iso_2=BI
```

**Réponse:** Hiérarchie complète pays → provinces → districts → quartiers → points de service

## 🔒 Permissions

### Accès Public (AllowAny)
- ✅ `GET /api/v1/localisation/pays/` - Liste
- ✅ `GET /api/v1/localisation/pays/{id}/` - Détail
- ✅ `GET /api/v1/localisation/pays/couverture/` - Couverture
- ✅ `GET /api/v1/localisation/provinces/` - Liste
- ✅ `GET /api/v1/localisation/provinces/{id}/` - Détail
- ✅ `GET /api/v1/localisation/districts/` - Liste
- ✅ `GET /api/v1/localisation/districts/{id}/` - Détail
- ✅ `GET /api/v1/localisation/quartiers/` - Liste
- ✅ `GET /api/v1/localisation/quartiers/{id}/` - Détail

### Accès Restreint (SYSTEME/SUPER_ADMIN uniquement)
- 🔒 `POST /api/v1/localisation/pays/` - Créer
- 🔒 `PUT /api/v1/localisation/pays/{id}/` - Modifier
- 🔒 `PATCH /api/v1/localisation/pays/{id}/` - Modifier partiellement
- 🔒 `DELETE /api/v1/localisation/pays/{id}/` - Supprimer
- (Idem pour provinces, districts, quartiers)

## 🎯 Utilisation dans le Frontend

### Exemple: Charger les Pays
```javascript
// Aucune authentification requise!
const response = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/');
const pays = await response.json();
console.log(pays);
```

### Exemple: Charger les Provinces d'un Pays
```javascript
const paysId = 'uuid-du-pays';
const response = await fetch(`http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=${paysId}`);
const provinces = await response.json();
```

### Exemple: Cascade Complète
```javascript
// 1. Charger les pays
const pays = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/').then(r => r.json());

// 2. Utilisateur sélectionne un pays
const paysSelectionne = pays[0].id;

// 3. Charger les provinces de ce pays
const provinces = await fetch(
  `http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=${paysSelectionne}`
).then(r => r.json());

// 4. Utilisateur sélectionne une province
const provinceSelectionnee = provinces[0].id;

// 5. Charger les districts de cette province
const districts = await fetch(
  `http://127.0.0.1:8000/api/v1/localisation/districts/?province_id=${provinceSelectionnee}`
).then(r => r.json());

// 6. Utilisateur sélectionne un district
const districtSelectionne = districts[0].id;

// 7. Charger les quartiers de ce district
const quartiers = await fetch(
  `http://127.0.0.1:8000/api/v1/localisation/quartiers/?district_id=${districtSelectionne}`
).then(r => r.json());
```

## 🔧 Modifications Techniques

### Fichier: `apps/localisation/views.py`

Ajout de la méthode `get_permissions()` à chaque ViewSet:

```python
def get_permissions(self):
    """
    Permissions publiques pour GET (list, retrieve).
    Permissions admin pour POST/PUT/PATCH/DELETE.
    """
    if self.action in ['list', 'retrieve']:
        return [AllowAny()]
    return [IsSystemeOrSuperAdmin()]
```

Cette méthode permet de:
- ✅ Autoriser tout le monde (AllowAny) pour les actions `list` et `retrieve` (GET)
- 🔒 Restreindre aux admins (IsSystemeOrSuperAdmin) pour `create`, `update`, `partial_update`, `destroy`

## ✅ Résultat

Les endpoints de localisation sont maintenant utilisables par le frontend pour:
1. Formulaire d'inscription CLIENT (public)
2. Formulaire de création ADMIN/AGENT/MARCHAND (authentifié)
3. Sélection de pays/province/district/quartier dans n'importe quel formulaire

**Plus d'erreur 403!** 🎉
