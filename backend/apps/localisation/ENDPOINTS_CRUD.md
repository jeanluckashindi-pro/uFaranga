# CRUD complet – Schéma Localisation

Tous les endpoints sont sous **`/api/v1/localisation/`**.  
**Accès réservé** : utilisateurs identite avec `type_utilisateur` **SYSTEME** ou **SUPER_ADMIN**.  
Authentification : **Bearer JWT** obligatoire.

---

## 1. Pays (`localisation.pays`)

| Méthode | URL | Action |
|--------|-----|--------|
| GET | `/api/v1/localisation/pays/` | Liste (pagination, **filtres**, `?search=`, `?ordering=`) |
| POST | `/api/v1/localisation/pays/` | Créer |
| GET | `/api/v1/localisation/pays/{id}/` | Détail |
| PUT | `/api/v1/localisation/pays/{id}/` | Modifier (complet) |
| PATCH | `/api/v1/localisation/pays/{id}/` | Modifier (partiel) |
| DELETE | `/api/v1/localisation/pays/{id}/` | Supprimer |

**Champs** : `id`, `code_iso_2`, `code_iso_3`, `nom`, `nom_anglais`, `latitude_centre`, `longitude_centre`, `autorise_systeme`, `est_actif`, `date_creation`, `date_modification`, `metadonnees`.

**Filtres (GET liste)** :

| Paramètre | Type | Description |
|-----------|------|-------------|
| `code_iso_2` | string | Code ISO 2 (exact, insensible à la casse) |
| `code_iso_3` | string | Code ISO 3 (exact, insensible à la casse) |
| `nom` | string | Nom du pays (contient, insensible à la casse) |
| `nom_anglais` | string | Nom en anglais (contient, insensible à la casse) |
| `est_actif` | bool | `true` = actifs uniquement, `false` = inactifs uniquement |
| `autorise_systeme` | bool | `true` = autorisés dans le système, `false` = non autorisés |

Exemples :  
`GET /api/v1/localisation/pays/?est_actif=true`  
`GET /api/v1/localisation/pays/?code_iso_2=BI`  
`GET /api/v1/localisation/pays/?nom=burundi`

### Couverture mondiale – GET `GET /api/v1/localisation/pays/couverture/`

Endpoint pour **visualiser la hiérarchie complète** des pays couverts : **pays → provinces → districts → quartiers → points de vente**, avec **coordonnées**, **statistiques** (total, actifs, inactifs) à chaque niveau. Toutes les zones sont retournées avec leur statut `autorise_systeme` et `est_actif`.

**Filtres** :

| Paramètre | Type | Description |
|-----------|------|-------------|
| `pays_id` | UUID | Un seul pays (ex. `?pays_id=550e8400-e29b-41d4-a716-446655440001`) |
| `code_iso_2` | string | Code ISO 2 (ex. `BI`, `RW`) |
| `nom` | string | Nom du pays (contient) |
| `autorise_systeme` | bool | Si fourni : filtrer par pays autorisés (`true`) ou non (`false`) dans le système |
| `est_actif` | bool | Si fourni : filtrer par pays actifs (`true`) ou inactifs (`false`) |

**Réponse** : tableau de pays (sans pagination). Chaque pays contient :
- `id`, `code_iso_2`, `code_iso_3`, `nom`, `nom_anglais`, `latitude_centre`, `longitude_centre`, `autorise_systeme`, `est_actif`
- `statistiques` : `nb_provinces`, `nb_provinces_actives`, `nb_provinces_inactives`, `nb_districts`, `nb_quartiers`, `nb_points_de_service`
- `provinces` : tableau de provinces (chacune avec `statistiques` + `districts`)
  - chaque **district** : `statistiques` + `quartiers`
  - chaque **quartier** : `statistiques` + `points_de_service` (points de vente)
  - chaque **point de service** : `id`, `code`, `nom`, `type_point`, `latitude`, `longitude`, `autorise_systeme`, `est_actif`

À chaque niveau (province, district, quartier), `statistiques` inclut les totaux et les décomptes **actifs / inactifs** (ex. `nb_quartiers_actifs`, `nb_quartiers_inactifs`, `nb_points_actifs`, `nb_points_inactifs`).

Exemples :  
`GET /api/v1/localisation/pays/couverture/`  
`GET /api/v1/localisation/pays/couverture/?pays_id=uuid`  
`GET /api/v1/localisation/pays/couverture/?code_iso_2=BI`  
`GET /api/v1/localisation/pays/couverture/?est_actif=false`

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
    "latitude_centre": "-3.3822000",
    "longitude_centre": "29.3644000",
    "autorise_systeme": true,
    "est_actif": true,
    "statistiques": {
      "nb_provinces": 18,
      "nb_provinces_actives": 17,
      "nb_provinces_inactives": 1,
      "nb_districts": 129,
      "nb_quartiers": 2639,
      "nb_points_de_service": 1245
    },
    "provinces": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440002",
        "code": "BU",
        "nom": "Bujumbura Mairie",
        "latitude_centre": "-3.3822000",
        "longitude_centre": "29.3644000",
        "autorise_systeme": true,
        "est_actif": true,
        "statistiques": {
          "nb_districts": 3,
          "nb_districts_actifs": 3,
          "nb_districts_inactifs": 0,
          "nb_quartiers": 97,
          "nb_points_de_service": 456
        },
        "districts": [
          {
            "id": "...",
            "code": "BUJ",
            "nom": "Bujumbura",
            "autorise_systeme": true,
            "est_actif": true,
            "statistiques": {
              "nb_quartiers": 45,
              "nb_quartiers_actifs": 44,
              "nb_quartiers_inactifs": 1,
              "nb_points_de_service": 210
            },
            "quartiers": [
              {
                "id": "...",
                "code": "GIH",
                "nom": "Gihosha",
                "autorise_systeme": true,
                "est_actif": true,
                "statistiques": {
                  "nb_points_de_service": 12,
                  "nb_points_actifs": 11,
                  "nb_points_inactifs": 1
                },
                "points_de_service": [
                  {
                    "id": "...",
                    "code": "AGT-001",
                    "nom": "Agent Centre",
                    "type_point": "AGENT",
                    "latitude": "-3.3822",
                    "longitude": "29.3644",
                    "autorise_systeme": true,
                    "est_actif": true
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### Output – GET liste `GET /api/v1/localisation/pays/`

```json
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "code_iso_2": "BI",
      "code_iso_3": "BDI",
      "nom": "Burundi",
      "nom_anglais": "Burundi",
      "latitude_centre": "-3.3822000",
      "longitude_centre": "29.3644000",
      "autorise_systeme": true,
      "est_actif": true,
      "date_creation": "2024-01-15T10:00:00Z",
      "date_modification": "2024-01-15T10:00:00Z",
      "metadonnees": {}
    }
  ]
}
```

### Output – GET détail `GET /api/v1/localisation/pays/{id}/`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "code_iso_2": "BI",
  "code_iso_3": "BDI",
  "nom": "Burundi",
  "nom_anglais": "Burundi",
  "latitude_centre": "-3.3822000",
  "longitude_centre": "29.3644000",
  "autorise_systeme": true,
  "est_actif": true,
  "date_creation": "2024-01-15T10:00:00Z",
  "date_modification": "2024-01-15T10:00:00Z",
  "metadonnees": {},
  "provinces": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "code": "BU",
      "nom": "Bujumbura Mairie",
      "latitude_centre": "-3.3822000",
      "longitude_centre": "29.3644000",
      "autorise_systeme": true,
      "est_actif": true,
      "districts": [
        {
          "id": "770e8400-e29b-41d4-a716-446655440003",
          "code": "BUJ",
          "nom": "Bujumbura",
          "latitude_centre": null,
          "longitude_centre": null,
          "autorise_systeme": true,
          "est_actif": true,
          "quartiers": [
            {
              "id": "880e8400-e29b-41d4-a716-446655440004",
              "code": "GIH",
              "nom": "Gihosha",
              "latitude_centre": null,
              "longitude_centre": null,
              "autorise_systeme": true,
              "est_actif": true,
              "points_de_service": []
            }
          ]
        }
      ]
    }
  ]
}
```

---

## 2. Provinces (`localisation.provinces`)

| Méthode | URL | Action |
|--------|-----|--------|
| GET | `/api/v1/localisation/provinces/` | Liste |
| POST | `/api/v1/localisation/provinces/` | Créer |
| GET | `/api/v1/localisation/provinces/{id}/` | Détail |
| PUT | `/api/v1/localisation/provinces/{id}/` | Modifier |
| PATCH | `/api/v1/localisation/provinces/{id}/` | Modifier partiel |
| DELETE | `/api/v1/localisation/provinces/{id}/` | Supprimer |

**Filtre** : `?pays_id={uuid}` pour lister les provinces d’un pays.  
**Champs** : `id`, `pays` (UUID ou nom/code), `pays_nom`, `pays_code`, `code`, `nom`, `latitude_centre`, `longitude_centre`, `autorise_systeme`, `est_actif`, etc.

---

## 3. Districts (`localisation.districts`)

| Méthode | URL | Action |
|--------|-----|--------|
| GET | `/api/v1/localisation/districts/` | Liste |
| POST | `/api/v1/localisation/districts/` | Créer |
| GET | `/api/v1/localisation/districts/{id}/` | Détail |
| PUT | `/api/v1/localisation/districts/{id}/` | Modifier |
| PATCH | `/api/v1/localisation/districts/{id}/` | Modifier partiel |
| DELETE | `/api/v1/localisation/districts/{id}/` | Supprimer |

**Filtre** : `?province_id={uuid}`.  
**Champs** : `id`, `province` (UUID ou nom/code), `province_nom`, `pays_nom`, `code`, `nom`, coordonnées, `autorise_systeme`, etc.

---

## 4. Quartiers (`localisation.quartiers`)

| Méthode | URL | Action |
|--------|-----|--------|
| GET | `/api/v1/localisation/quartiers/` | Liste |
| POST | `/api/v1/localisation/quartiers/` | Créer |
| GET | `/api/v1/localisation/quartiers/{id}/` | Détail |
| PUT | `/api/v1/localisation/quartiers/{id}/` | Modifier |
| PATCH | `/api/v1/localisation/quartiers/{id}/` | Modifier partiel |
| DELETE | `/api/v1/localisation/quartiers/{id}/` | Supprimer |

**Filtre** : `?district_id={uuid}`.  
**Champs** : `id`, `district` (UUID ou nom/code), `district_nom`, `province_nom`, `code`, `nom`, coordonnées, `autorise_systeme`, etc.

---

## 5. Points de service (`localisation.points_de_service`)

| Méthode | URL | Action |
|--------|-----|--------|
| GET | `/api/v1/localisation/points-de-service/` | Liste |
| POST | `/api/v1/localisation/points-de-service/` | Créer |
| GET | `/api/v1/localisation/points-de-service/{id}/` | Détail |
| PUT | `/api/v1/localisation/points-de-service/{id}/` | Modifier |
| PATCH | `/api/v1/localisation/points-de-service/{id}/` | Modifier partiel |
| DELETE | `/api/v1/localisation/points-de-service/{id}/` | Supprimer |

**Filtre** : `?quartier_id={uuid}`.  
**Champs** : `id`, `quartier` (UUID ou nom/code), `quartier_nom`, `district_nom`, `code`, `nom`, `type_point` (AGENT, GUICHET, PARTENAIRE, AUTRE), `agent_utilisateur` (UUID), `latitude`, `longitude`, `adresse_complementaire`, `autorise_systeme`, etc.

---

## Options communes

- **Pagination** : liste paginée (taille par défaut selon la config DRF).
- **Recherche** : `?search=terme` sur les champs principaux (nom, code).
- **Tri** : `?ordering=nom`, `?ordering=-date_creation`, etc.
- **Relations** : pour créer/modifier, vous pouvez envoyer l’UUID du parent ou son **nom/code** (ex. `"province": "Bujumbura"`, `"quartier": "Gihosha"`).

Documentation interactive : **`/api/docs/`** (Swagger), tag *Localisation (SYSTEME/SUPER_ADMIN)*.
