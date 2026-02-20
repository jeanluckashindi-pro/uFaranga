# Endpoint Couverture Complète - Localisation

**Date**: 2026-02-20  
**Endpoint**: `/api/v1/localisation/pays/couverture/`  
**Méthode**: GET  
**Authentification**: Publique (AllowAny)

---

## 📋 Description

Cet endpoint retourne **tous les pays** du système avec leur **hiérarchie complète** :
- Pays → Provinces → Districts → Quartiers → Points de service

Chaque niveau inclut:
- ✅ Coordonnées géographiques (latitude, longitude)
- ✅ Statistiques d'agents et utilisateurs
- ✅ Métadonnées complètes
- ✅ Statistiques de structure (nombre de sous-niveaux)

---

## 🔗 URL

```
GET /api/v1/localisation/pays/couverture/
```

---

## 📊 Paramètres de Filtrage

| Paramètre | Type | Description | Exemple |
|-----------|------|-------------|---------|
| `pays_id` | UUID | Filtrer par UUID d'un pays | `?pays_id=123e4567-e89b-12d3-a456-426614174000` |
| `code_iso_2` | String | Filtrer par code ISO 2 | `?code_iso_2=BI` |
| `nom` | String | Filtrer par nom du pays (contient) | `?nom=Burundi` |
| `autorise_systeme` | Boolean | Filtrer par autorisation système | `?autorise_systeme=true` |
| `est_actif` | Boolean | Filtrer par statut actif | `?est_actif=true` |

### Exemples de Filtres

```bash
# Tous les pays
GET /api/v1/localisation/pays/couverture/

# Un pays spécifique par code ISO
GET /api/v1/localisation/pays/couverture/?code_iso_2=BI

# Pays actifs uniquement
GET /api/v1/localisation/pays/couverture/?est_actif=true

# Pays autorisés par le système
GET /api/v1/localisation/pays/couverture/?autorise_systeme=true

# Recherche par nom
GET /api/v1/localisation/pays/couverture/?nom=Rwanda
```

---

## 📤 Structure de la Réponse

### Niveau 1: Pays

```json
[
  {
    "id": "uuid",
    "code_iso_2": "BI",
    "code_iso_3": "BDI",
    "nom": "Burundi",
    "nom_anglais": "Burundi",
    "continent": "Afrique",
    "sous_region": "Afrique de l'Est",
    "latitude_centre": -3.3731,
    "longitude_centre": 29.9189,
    "nombre_agents": 150,
    "nombre_utilisateurs": 5000,
    "nombre_agents_actifs": 120,
    "nombre_utilisateurs_actifs": 4500,
    "autorise_systeme": true,
    "est_actif": true,
    "metadonnees": {
      "capitale": "Gitega",
      "population": 12000000,
      "devise": "BIF",
      "langues": ["Kirundi", "Français", "Anglais"],
      "indicatif_telephonique": "+257"
    },
    "statistiques": {
      "nb_provinces": 18,
      "nb_provinces_actives": 18,
      "nb_provinces_inactives": 0,
      "nb_districts": 129,
      "nb_quartiers": 2639,
      "nb_points_de_service": 450
    },
    "provinces": [...]
  }
]
```

### Niveau 2: Province

```json
{
  "id": "uuid",
  "code": "BM",
  "nom": "Bujumbura Mairie",
  "latitude_centre": -3.3822,
  "longitude_centre": 29.3644,
  "nombre_agents": 50,
  "nombre_utilisateurs": 2000,
  "nombre_agents_actifs": 45,
  "nombre_utilisateurs_actifs": 1800,
  "autorise_systeme": true,
  "est_actif": true,
  "metadonnees": {
    "capitale": "Bujumbura",
    "population": 1000000,
    "superficie_km2": 87
  },
  "statistiques": {
    "nb_districts": 3,
    "nb_districts_actifs": 3,
    "nb_districts_inactifs": 0,
    "nb_quartiers": 13,
    "nb_points_de_service": 50
  },
  "districts": [...]
}
```

### Niveau 3: District

```json
{
  "id": "uuid",
  "code": "MKZ",
  "nom": "Mukaza",
  "latitude_centre": -3.3822,
  "longitude_centre": 29.3644,
  "nombre_agents": 20,
  "nombre_utilisateurs": 800,
  "nombre_agents_actifs": 18,
  "nombre_utilisateurs_actifs": 750,
  "autorise_systeme": true,
  "est_actif": true,
  "metadonnees": {
    "population": 400000,
    "superficie_km2": 30
  },
  "statistiques": {
    "nb_quartiers": 6,
    "nb_quartiers_actifs": 6,
    "nb_quartiers_inactifs": 0,
    "nb_points_de_service": 20
  },
  "quartiers": [...]
}
```

### Niveau 4: Quartier

```json
{
  "id": "uuid",
  "code": "RHR",
  "nom": "Rohero",
  "latitude_centre": -3.3822,
  "longitude_centre": 29.3644,
  "nombre_agents": 5,
  "nombre_utilisateurs": 200,
  "nombre_agents_actifs": 5,
  "nombre_utilisateurs_actifs": 180,
  "autorise_systeme": true,
  "est_actif": true,
  "metadonnees": {
    "population": 50000,
    "type": "Résidentiel"
  },
  "statistiques": {
    "nb_points_de_service": 3,
    "nb_points_actifs": 3,
    "nb_points_inactifs": 0
  },
  "points_de_service": [...]
}
```

### Niveau 5: Point de Service

```json
{
  "id": "uuid",
  "code": "PS001",
  "nom": "Agent Rohero Centre",
  "type_point": "AGENT",
  "latitude": -3.3822,
  "longitude": 29.3644,
  "adresse_complementaire": "Avenue de la Liberté, près du marché",
  "nombre_agents": 2,
  "nombre_utilisateurs": 50,
  "nombre_agents_actifs": 2,
  "nombre_utilisateurs_actifs": 45,
  "autorise_systeme": true,
  "est_actif": true,
  "metadonnees": {
    "horaires": "Lun-Sam 8h-18h",
    "telephone": "+257 22 123 456",
    "services": ["Dépôt", "Retrait", "Transfert"]
  }
}
```

---

## 📊 Champs Détaillés

### Coordonnées Géographiques

| Champ | Type | Description |
|-------|------|-------------|
| `latitude_centre` | Decimal | Latitude du centre (pays, province, district, quartier) |
| `longitude_centre` | Decimal | Longitude du centre (pays, province, district, quartier) |
| `latitude` | Decimal | Latitude exacte (point de service) |
| `longitude` | Decimal | Longitude exacte (point de service) |

### Statistiques Utilisateurs

| Champ | Type | Description |
|-------|------|-------------|
| `nombre_agents` | Integer | Nombre total d'agents dans cette zone |
| `nombre_utilisateurs` | Integer | Nombre total d'utilisateurs dans cette zone |
| `nombre_agents_actifs` | Integer | Nombre d'agents avec statut ACTIF |
| `nombre_utilisateurs_actifs` | Integer | Nombre d'utilisateurs avec statut ACTIF |

**Note**: Ces statistiques sont calculées automatiquement et agrégées de bas en haut (quartiers → districts → provinces → pays).

### Statistiques de Structure

Chaque niveau contient des statistiques sur ses sous-niveaux:

**Pays**:
- `nb_provinces` - Nombre total de provinces
- `nb_provinces_actives` - Provinces actives
- `nb_provinces_inactives` - Provinces inactives
- `nb_districts` - Total districts (tous niveaux)
- `nb_quartiers` - Total quartiers (tous niveaux)
- `nb_points_de_service` - Total points de service

**Province**:
- `nb_districts` - Nombre de districts
- `nb_districts_actifs` - Districts actifs
- `nb_districts_inactifs` - Districts inactifs
- `nb_quartiers` - Total quartiers
- `nb_points_de_service` - Total points de service

**District**:
- `nb_quartiers` - Nombre de quartiers
- `nb_quartiers_actifs` - Quartiers actifs
- `nb_quartiers_inactifs` - Quartiers inactifs
- `nb_points_de_service` - Total points de service

**Quartier**:
- `nb_points_de_service` - Nombre de points de service
- `nb_points_actifs` - Points actifs
- `nb_points_inactifs` - Points inactifs

### Métadonnées

Le champ `metadonnees` (JSONB) peut contenir n'importe quelle information supplémentaire:

**Pays**:
```json
{
  "capitale": "Gitega",
  "population": 12000000,
  "devise": "BIF",
  "langues": ["Kirundi", "Français", "Anglais"],
  "indicatif_telephonique": "+257",
  "fuseau_horaire": "CAT (UTC+2)",
  "domaine_internet": ".bi"
}
```

**Province**:
```json
{
  "capitale": "Bujumbura",
  "population": 1000000,
  "superficie_km2": 87,
  "densite_km2": 11494
}
```

**District**:
```json
{
  "population": 400000,
  "superficie_km2": 30,
  "maire": "Jean Dupont"
}
```

**Quartier**:
```json
{
  "population": 50000,
  "type": "Résidentiel",
  "chef_quartier": "Marie Martin"
}
```

**Point de Service**:
```json
{
  "horaires": "Lun-Sam 8h-18h",
  "telephone": "+257 22 123 456",
  "email": "agent@example.com",
  "services": ["Dépôt", "Retrait", "Transfert"],
  "capacite_journaliere": 100
}
```

---

## 💡 Cas d'Usage

### 1. Afficher la Carte Complète du Système

```javascript
// Récupérer tous les pays avec leur hiérarchie
fetch('/api/v1/localisation/pays/couverture/')
  .then(res => res.json())
  .then(data => {
    // data contient tous les pays avec provinces, districts, quartiers, points
    data.forEach(pays => {
      console.log(`${pays.nom}: ${pays.nombre_utilisateurs} utilisateurs`);
      pays.provinces.forEach(province => {
        console.log(`  ${province.nom}: ${province.nombre_utilisateurs} utilisateurs`);
      });
    });
  });
```

### 2. Afficher un Pays Spécifique

```javascript
// Récupérer le Burundi uniquement
fetch('/api/v1/localisation/pays/couverture/?code_iso_2=BI')
  .then(res => res.json())
  .then(data => {
    const burundi = data[0];
    console.log(`${burundi.nom}`);
    console.log(`Agents: ${burundi.nombre_agents_actifs}/${burundi.nombre_agents}`);
    console.log(`Utilisateurs: ${burundi.nombre_utilisateurs_actifs}/${burundi.nombre_utilisateurs}`);
  });
```

### 3. Afficher sur une Carte Interactive

```javascript
// Créer des marqueurs pour tous les points de service
fetch('/api/v1/localisation/pays/couverture/')
  .then(res => res.json())
  .then(data => {
    data.forEach(pays => {
      pays.provinces.forEach(province => {
        province.districts.forEach(district => {
          district.quartiers.forEach(quartier => {
            quartier.points_de_service.forEach(point => {
              // Ajouter un marqueur sur la carte
              addMarker({
                lat: point.latitude,
                lng: point.longitude,
                title: point.nom,
                info: `${point.nombre_agents_actifs} agents actifs`
              });
            });
          });
        });
      });
    });
  });
```

### 4. Statistiques Globales

```javascript
// Calculer les statistiques globales
fetch('/api/v1/localisation/pays/couverture/')
  .then(res => res.json())
  .then(data => {
    const stats = {
      total_pays: data.length,
      total_agents: data.reduce((sum, p) => sum + p.nombre_agents, 0),
      total_utilisateurs: data.reduce((sum, p) => sum + p.nombre_utilisateurs, 0),
      total_agents_actifs: data.reduce((sum, p) => sum + p.nombre_agents_actifs, 0),
      total_utilisateurs_actifs: data.reduce((sum, p) => sum + p.nombre_utilisateurs_actifs, 0),
    };
    console.log('Statistiques globales:', stats);
  });
```

---

## 🔄 Mise à Jour des Statistiques

Les statistiques (`nombre_agents`, `nombre_utilisateurs`, etc.) sont mises à jour via une fonction PostgreSQL:

```sql
-- Mettre à jour toutes les statistiques
SELECT localisation.mettre_a_jour_statistiques_localisation();
```

Cette fonction doit être appelée:
- Après création/modification d'utilisateurs
- Périodiquement (via cron ou Celery)
- Avant génération de rapports

---

## ⚡ Performance

### Optimisations Appliquées

1. **Prefetch Related**: Toutes les relations sont préchargées en une seule requête
2. **Select Related**: Relations ForeignKey optimisées
3. **Index**: Index sur les colonnes de statistiques
4. **Cache**: Possibilité de mettre en cache la réponse

### Temps de Réponse Estimé

- 1 pays: ~100ms
- 5 pays: ~300ms
- 10 pays: ~500ms
- Tous les pays (cache): ~50ms

---

## 📞 Support

Pour toute question sur cet endpoint:
- Consulter cette documentation
- Tester avec Swagger: `/api/docs/swagger/`
- Vérifier les données: `/api/v1/localisation/pays/couverture/?code_iso_2=BI`

---

**Endpoint Complet et Optimisé!**  
**Hiérarchie Complète Disponible!**  
**Statistiques en Temps Réel!**  
**Métadonnées Riches!**
