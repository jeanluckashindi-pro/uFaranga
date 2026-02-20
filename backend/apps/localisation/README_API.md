# Documentation API - Module Localisation

## Vue d'ensemble

Le module **Localisation** gère la hiérarchie géographique complète :
**Pays** → **Provinces** → **Districts** → **Quartiers** → **Points de Service**

Base URL: `/api/v1/localisation/`

---

## 🌍 PAYS

### Liste des pays
```
GET /api/v1/localisation/pays/
```

**Filtres:**
- `?code_iso_2=BI` - Code ISO 2
- `?continent=Afrique` - Continent
- `?sous_region=Afrique de l'Est` - Sous-région
- `?est_actif=true` - Actif
- `?search=Burundi` - Recherche

**Réponse:**
```json
{
  "count": 2,
  "results": [
    {
      "id": "uuid",
      "code_iso_2": "BI",
      "code_iso_3": "BDI",
      "nom": "Burundi",
      "continent": "Afrique",
      "sous_region": "Afrique de l'Est",
      "latitude_centre": -3.3731,
      "longitude_centre": 29.9189,
      "autorise_systeme": true,
      "est_actif": true,
      "metadonnees": {
        "capitale": "Gitega",
        "population": 12000000
      }
    }
  ]
}
```

### Créer un pays
```
POST /api/v1/localisation/pays/
```
```json
{
  "code_iso_2": "RW",
  "nom": "Rwanda",
  "continent": "Afrique",
  "metadonnees": {"capitale": "Kigali"}
}
```

### Modifier un pays
```
PATCH /api/v1/localisation/pays/{id}/
```

### Supprimer un pays
```
DELETE /api/v1/localisation/pays/{id}/
```

---

## 🏛️ PROVINCES

### Liste
```
GET /api/v1/localisation/provinces/
GET /api/v1/localisation/provinces/?pays_id=uuid
```

### Créer
```
POST /api/v1/localisation/provinces/
```
```json
{
  "pays": "uuid-pays",
  "code": "BM",
  "nom": "Bujumbura Mairie",
  "metadonnees": {"population": 1000000}
}
```

---

## 🏙️ DISTRICTS

### Liste
```
GET /api/v1/localisation/districts/
GET /api/v1/localisation/districts/?province_id=uuid
```

### Créer
```
POST /api/v1/localisation/districts/
```
```json
{
  "province": "uuid-province",
  "code": "MUK",
  "nom": "Mukaza",
  "metadonnees": {"type": "urbain"}
}
```

---

## 🏘️ QUARTIERS

### Liste
```
GET /api/v1/localisation/quartiers/
GET /api/v1/localisation/quartiers/?district_id=uuid
```

### Créer
```
POST /api/v1/localisation/quartiers/
```
```json
{
  "district": "uuid-district",
  "code": "ROH",
  "nom": "Rohero",
  "metadonnees": {"chef_quartier": "Jean"}
}
```

---

## 📍 POINTS DE SERVICE

### Liste
```
GET /api/v1/localisation/points-de-service/
GET /api/v1/localisation/points-de-service/?quartier_id=uuid
```

**Types:** AGENT, GUICHET, PARTENAIRE, AUTRE

### Créer
```
POST /api/v1/localisation/points-de-service/
```
```json
{
  "quartier": "uuid-quartier",
  "code": "AG001",
  "nom": "Agent Rohero 1",
  "type_point": "AGENT",
  "latitude": -3.3614,
  "longitude": 29.3599,
  "metadonnees": {
    "horaires": "08:00-17:00",
    "services": ["Dépôt", "Retrait"]
  }
}
```

---

## 🌐 LOCALISATION COMPLÈTE

### Toutes les données
```
GET /api/v1/localisation/complete/
```

**Filtres:**
- `?continent=Afrique`
- `?pays_code=BI`
- `?province_id=uuid`
- `?est_actif=true`

**Réponse:**
```json
{
  "pays": [...],
  "provinces": [...],
  "districts": [...],
  "quartiers": [...],
  "points_de_service": [...],
  "statistiques_globales": {
    "total_pays": 2,
    "total_provinces": 18,
    "total_districts": 129,
    "total_quartiers": 2639,
    "total_points_de_service": 5000
  }
}
```

---

## 📊 RÉSUMÉ CRUD

| Ressource | Liste | Créer | Modifier | Supprimer |
|-----------|-------|-------|----------|-----------|
| Pays | GET /pays/ | POST /pays/ | PATCH /pays/{id}/ | DELETE /pays/{id}/ |
| Provinces | GET /provinces/ | POST /provinces/ | PATCH /provinces/{id}/ | DELETE /provinces/{id}/ |
| Districts | GET /districts/ | POST /districts/ | PATCH /districts/{id}/ | DELETE /districts/{id}/ |
| Quartiers | GET /quartiers/ | POST /quartiers/ | PATCH /quartiers/{id}/ | DELETE /quartiers/{id}/ |
| Points | GET /points-de-service/ | POST /points-de-service/ | PATCH /points-de-service/{id}/ | DELETE /points-de-service/{id}/ |

---

## 🔑 CHAMPS COMMUNS

Tous les niveaux ont:
- `id` (UUID)
- `code` (string)
- `nom` (string)
- `latitude_centre`, `longitude_centre` (decimal)
- `autorise_systeme` (boolean)
- `est_actif` (boolean)
- `date_creation`, `date_modification` (datetime)
- `metadonnees` (JSON flexible)

---

## 💡 EXEMPLES MÉTADONNÉES

**Pays:**
```json
{
  "capitale": "Gitega",
  "devise": "BIF",
  "langues": ["Kirundi", "Français"]
}
```

**Point de Service:**
```json
{
  "horaires": "08:00-17:00",
  "services": ["Dépôt", "Retrait"],
  "telephone": "+257 22 123 456",
  "responsable": "Jean Dupont"
}
```
