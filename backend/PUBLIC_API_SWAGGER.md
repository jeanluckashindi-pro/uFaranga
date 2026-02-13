# 📚 Documentation Swagger - API Publique uFaranga

## ✅ Ce qui a été ajouté

### 1. Nouveaux Endpoints (Total: 17 endpoints)

#### Système (3)
- ✅ `GET /api/public/health/` - Vérification de santé
- ✅ `GET /api/public/status/` - Statut des services
- ✅ `GET /api/public/version/` - Version de l'API

#### Tarification (3)
- ✅ `GET /api/public/fees/calculator/` - Calculateur de frais
- ✅ `GET /api/public/fees/schedule/` - Grille tarifaire
- ✅ `GET /api/public/exchange-rates/` - Taux de change

#### Informations (3)
- ✅ `GET /api/public/countries/` - Pays supportés
- ✅ `GET /api/public/currencies/` - Devises supportées
- ✅ `GET /api/public/transaction-types/` - Types de transactions

#### Validation (2) 🆕
- ✅ `POST /api/public/validate/phone/` - Valider un numéro de téléphone
- ✅ `POST /api/public/validate/account/` - Vérifier si un compte existe

#### Agents (2) 🆕
- ✅ `GET /api/public/agents/search/` - Rechercher des agents à proximité
- ✅ `GET /api/public/agents/{id}/` - Détails d'un agent

#### Inscription (2) 🆕
- ✅ `POST /api/public/register/initiate/` - Initier une inscription
- ✅ `POST /api/public/register/verify-otp/` - Vérifier le code OTP

#### Support (2) 🆕
- ✅ `POST /api/public/contact/` - Contacter le support
- ✅ `GET /api/public/faq/` - Questions fréquentes

### 2. Documentation Swagger/OpenAPI

#### URLs de Documentation
```
📖 Swagger UI:  http://localhost:8000/api/public/docs/
📖 ReDoc:       http://localhost:8000/api/public/redoc/
📖 Schema JSON: http://localhost:8000/api/public/schema/
```

#### Fichiers Créés
```
backend/apps/public_api/
├── serializers.py       # Serializers pour validation
├── schema.py            # Configuration OpenAPI
└── swagger_views.py     # Vues Swagger personnalisées
```

### 3. Fonctionnalités Swagger

✅ **Interface Interactive**
- Tester les endpoints directement depuis le navigateur
- Authentification API Key intégrée
- Exemples de requêtes/réponses
- Validation automatique des paramètres

✅ **Documentation Complète**
- Description de chaque endpoint
- Paramètres requis/optionnels
- Codes de réponse HTTP
- Exemples de données
- Informations sur les quotas

✅ **Authentification Documentée**
- Schéma API Key expliqué
- Exemples d'utilisation
- Headers requis

✅ **Organisation par Tags**
- Système
- Tarification
- Informations
- Validation
- Agents
- Inscription
- Support

## 🚀 Accéder à la Documentation

### Étape 1: Démarrer le Serveur

```bash
cd backend
python manage.py runserver
```

### Étape 2: Ouvrir Swagger UI

Ouvrez votre navigateur et allez sur:
```
http://localhost:8000/api/public/docs/
```

### Étape 3: S'Authentifier

1. Cliquez sur le bouton **"Authorize"** en haut à droite
2. Entrez votre clé API dans le format:
   ```
   ApiKey ufar_test_abc123xyz789...
   ```
3. Cliquez sur **"Authorize"**
4. Fermez la fenêtre

### Étape 4: Tester les Endpoints

1. Choisissez un endpoint (ex: `GET /api/public/health/`)
2. Cliquez sur **"Try it out"**
3. Remplissez les paramètres si nécessaire
4. Cliquez sur **"Execute"**
5. Voir la réponse en bas

## 📸 Captures d'Écran (Description)

### Swagger UI
```
┌─────────────────────────────────────────────────────────┐
│  uFaranga Public API - Documentation Interactive        │
│  Version 1.0.0                                          │
│                                                         │
│  [Authorize] 🔐                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📁 Système                                             │
│    GET  /api/public/health/        Vérification santé  │
│    GET  /api/public/status/        Statut services     │
│    GET  /api/public/version/       Version API         │
│                                                         │
│  📁 Tarification                                        │
│    GET  /api/public/fees/calculator/  Calculer frais   │
│    GET  /api/public/fees/schedule/    Grille tarifaire │
│    GET  /api/public/exchange-rates/   Taux de change   │
│                                                         │
│  📁 Validation                                          │
│    POST /api/public/validate/phone/   Valider téléphone│
│    POST /api/public/validate/account/ Vérifier compte  │
│                                                         │
│  📁 Agents                                              │
│    GET  /api/public/agents/search/    Rechercher agents│
│    GET  /api/public/agents/{id}/      Détails agent    │
│                                                         │
│  📁 Inscription                                         │
│    POST /api/public/register/initiate/    Initier      │
│    POST /api/public/register/verify-otp/  Vérifier OTP │
│                                                         │
│  📁 Support                                             │
│    POST /api/public/contact/          Contacter support│
│    GET  /api/public/faq/              FAQ              │
└─────────────────────────────────────────────────────────┘
```

## 💡 Exemples d'Utilisation

### Exemple 1: Calculer les Frais

**Dans Swagger UI:**
1. Ouvrir `GET /api/public/fees/calculator/`
2. Cliquer "Try it out"
3. Remplir:
   - `amount`: 10000
   - `type`: P2P
   - `currency`: BIF
4. Cliquer "Execute"

**Réponse:**
```json
{
  "montant": 10000.0,
  "devise": "BIF",
  "type_transaction": "P2P",
  "frais": 100.0,
  "commission": 50.0,
  "montant_total": 10150.0,
  "details": {
    "taux_frais": 1.0,
    "taux_commission": 0.5
  }
}
```

### Exemple 2: Valider un Téléphone

**Dans Swagger UI:**
1. Ouvrir `POST /api/public/validate/phone/`
2. Cliquer "Try it out"
3. Remplir le body:
   ```json
   {
     "phone": "+25779123456"
   }
   ```
4. Cliquer "Execute"

**Réponse:**
```json
{
  "phone": "+25779123456",
  "is_valid": true,
  "country_code": "BI",
  "formatted": "+25779123456",
  "message": "Numéro valide"
}
```

### Exemple 3: Rechercher des Agents

**Dans Swagger UI:**
1. Ouvrir `GET /api/public/agents/search/`
2. Cliquer "Try it out"
3. Remplir:
   - `latitude`: -3.3761
   - `longitude`: 29.3611
   - `radius`: 5000
4. Cliquer "Execute"

**Réponse:**
```json
{
  "count": 2,
  "agents": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174001",
      "name": "Agent Central Bujumbura",
      "type": "AGENT",
      "address": "Avenue de la Liberté, Bujumbura",
      "city": "Bujumbura",
      "country": "BI",
      "latitude": -3.3761,
      "longitude": 29.3611,
      "distance_meters": 1200,
      "phone": "+25779123456",
      "services": ["DEPOT", "RETRAIT", "P2P"],
      "is_open": true
    }
  ]
}
```

## 🔧 Configuration Avancée

### Personnaliser le Schéma

Modifier `backend/apps/public_api/swagger_views.py`:

```python
schema['info'] = {
    'title': 'Votre Titre',
    'version': '2.0.0',
    'description': 'Votre description...'
}
```

### Ajouter des Exemples

Dans vos vues, utiliser `@extend_schema`:

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    summary='Mon endpoint',
    description='Description détaillée',
    examples=[
        OpenApiExample(
            'Exemple 1',
            value={'key': 'value'},
            request_only=True
        )
    ]
)
@api_view(['POST'])
def my_view(request):
    ...
```

### Ajouter des Paramètres

```python
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Terme de recherche'
        )
    ]
)
```

## 📊 Comparaison Swagger vs ReDoc

| Fonctionnalité | Swagger UI | ReDoc |
|----------------|------------|-------|
| Interface | Interactive | Lecture seule |
| Test direct | ✅ Oui | ❌ Non |
| Design | Classique | Moderne |
| Navigation | Par tags | Par sections |
| Recherche | ✅ Oui | ✅ Oui |
| Export | ✅ JSON/YAML | ✅ JSON/YAML |

**Recommandation:**
- **Swagger UI** pour les développeurs (tests interactifs)
- **ReDoc** pour la documentation publique (plus élégant)

## 🎯 Bonnes Pratiques

### 1. Documenter Tous les Endpoints

```python
@extend_schema(
    tags=['Ma Catégorie'],
    summary='Résumé court',
    description='Description détaillée avec exemples',
    responses={
        200: MonSerializer,
        400: 'Erreur de validation',
        401: 'Non authentifié',
        429: 'Quota dépassé'
    }
)
```

### 2. Utiliser des Serializers

```python
class MonSerializer(serializers.Serializer):
    field1 = serializers.CharField(help_text='Description du champ')
    field2 = serializers.IntegerField(help_text='Autre description')
```

### 3. Ajouter des Exemples

```python
@extend_schema(
    examples=[
        OpenApiExample(
            'Exemple succès',
            value={'status': 'success'},
            response_only=True,
            status_codes=['200']
        ),
        OpenApiExample(
            'Exemple erreur',
            value={'error': 'invalid_input'},
            response_only=True,
            status_codes=['400']
        )
    ]
)
```

## 🆘 Dépannage

### Problème: Swagger ne charge pas

**Solution:**
```bash
# Vérifier que drf-spectacular est installé
pip install drf-spectacular

# Vérifier les settings
python manage.py spectacular --file schema.yml
```

### Problème: Authentification ne fonctionne pas

**Solution:**
Vérifier que vous utilisez le bon format:
```
ApiKey ufar_test_abc123...
```
Pas juste `ufar_test_abc123...`

### Problème: Endpoints manquants

**Solution:**
Vérifier que les URLs sont bien incluses:
```python
# Dans config/urls.py
path('api/public/', include('apps.public_api.urls')),
```

## 📚 Ressources

- **Swagger UI:** http://localhost:8000/api/public/docs/
- **ReDoc:** http://localhost:8000/api/public/redoc/
- **Schema JSON:** http://localhost:8000/api/public/schema/
- **drf-spectacular docs:** https://drf-spectacular.readthedocs.io/

---

**Documentation complète et interactive disponible! 🎉**
