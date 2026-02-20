# ✅ FIX: Erreur 403 sur les Endpoints de Localisation

## 🐛 Problème Initial

```
GET http://127.0.0.1:8000/api/v1/localisation/pays/

Réponse:
{
  "success": false,
  "status_code": 403,
  "errors": {
    "detail": "Accès réservé aux comptes Système et Super Administrateur."
  }
}
```

Les endpoints de localisation (pays, provinces, districts, quartiers) étaient protégés par la permission `IsSystemeOrSuperAdmin` pour TOUTES les actions, y compris la lecture (GET).

Cela empêchait:
- ❌ Le formulaire d'inscription CLIENT (public) de charger les pays/provinces/districts/quartiers
- ❌ Le formulaire de création ADMIN/AGENT/MARCHAND de charger les données de localisation
- ❌ Tout frontend non authentifié d'accéder aux données géographiques

## ✅ Solution Appliquée

### Modification: `apps/localisation/views.py`

Ajout de la méthode `get_permissions()` à chaque ViewSet pour différencier les permissions selon l'action:

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

### ViewSets Modifiés

1. ✅ `PaysViewSet` - Ajout de `get_permissions()` + action `couverture` publique
2. ✅ `ProvinceViewSet` - Ajout de `get_permissions()`
3. ✅ `DistrictViewSet` - Ajout de `get_permissions()`
4. ✅ `QuartierViewSet` - Ajout de `get_permissions()`
5. ✅ `PointDeServiceViewSet` - Ajout de `get_permissions()`

### Import Ajouté

```python
from rest_framework.permissions import AllowAny
```

## 🎯 Résultat

### Actions Publiques (AllowAny) ✅

- `GET /api/v1/localisation/pays/` - Liste des pays
- `GET /api/v1/localisation/pays/{id}/` - Détail d'un pays
- `GET /api/v1/localisation/pays/couverture/` - Couverture mondiale
- `GET /api/v1/localisation/provinces/` - Liste des provinces
- `GET /api/v1/localisation/provinces/{id}/` - Détail d'une province
- `GET /api/v1/localisation/districts/` - Liste des districts
- `GET /api/v1/localisation/districts/{id}/` - Détail d'un district
- `GET /api/v1/localisation/quartiers/` - Liste des quartiers
- `GET /api/v1/localisation/quartiers/{id}/` - Détail d'un quartier

### Actions Restreintes (IsSystemeOrSuperAdmin) 🔒

- `POST /api/v1/localisation/pays/` - Créer un pays
- `PUT /api/v1/localisation/pays/{id}/` - Modifier un pays
- `PATCH /api/v1/localisation/pays/{id}/` - Modifier partiellement
- `DELETE /api/v1/localisation/pays/{id}/` - Supprimer un pays
- (Idem pour provinces, districts, quartiers)

## 🧪 Test

### Avant (403 Forbidden)
```bash
curl http://127.0.0.1:8000/api/v1/localisation/pays/
# {"success": false, "status_code": 403, "errors": {"detail": "Accès réservé..."}}
```

### Après (200 OK)
```bash
curl http://127.0.0.1:8000/api/v1/localisation/pays/
# [{"id": "...", "code_iso_2": "BI", "nom": "Burundi", ...}]
```

## 📚 Documentation

- `ENDPOINTS_LOCALISATION_PUBLICS.md` - Guide complet des endpoints publics
- `OUTPUTS_REELS_ENDPOINTS.md` - Mis à jour avec les notes "PUBLIC"

## 🚀 Impact

Les formulaires frontend peuvent maintenant:
1. ✅ Charger la liste des pays sans authentification
2. ✅ Charger les provinces d'un pays sélectionné
3. ✅ Charger les districts d'une province sélectionnée
4. ✅ Charger les quartiers d'un district sélectionné
5. ✅ Utiliser ces IDs dans les payloads d'inscription/création

**Plus d'erreur 403 sur les endpoints de localisation!** 🎉
