# ⚡ Quick Reference: Endpoints de Localisation

## 🌍 Endpoints Publics (Pas d'Auth Requise)

```bash
# Pays
GET http://127.0.0.1:8000/api/v1/localisation/pays/
GET http://127.0.0.1:8000/api/v1/localisation/pays/{id}/
GET http://127.0.0.1:8000/api/v1/localisation/pays/couverture/

# Provinces
GET http://127.0.0.1:8000/api/v1/localisation/provinces/
GET http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id={uuid}

# Districts
GET http://127.0.0.1:8000/api/v1/localisation/districts/
GET http://127.0.0.1:8000/api/v1/localisation/districts/?province_id={uuid}

# Quartiers
GET http://127.0.0.1:8000/api/v1/localisation/quartiers/
GET http://127.0.0.1:8000/api/v1/localisation/quartiers/?district_id={uuid}
```

## 📋 Endpoints de Référence (Publics)

```bash
# Types d'utilisateurs
GET http://127.0.0.1:8000/api/v1/identite/types-utilisateurs/

# Niveaux KYC
GET http://127.0.0.1:8000/api/v1/identite/niveaux-kyc/

# Statuts
GET http://127.0.0.1:8000/api/v1/identite/statuts-utilisateurs/
```

## 👤 Endpoints de Création

```bash
# Inscription CLIENT (Public)
POST http://127.0.0.1:8000/api/v1/identite/inscription/

# Création ADMIN/AGENT/MARCHAND (Auth Requise)
POST http://127.0.0.1:8000/api/v1/identite/admin/creer-utilisateur/
```

## 💻 Code JavaScript

### Charger Cascade Complète
```javascript
const API = 'http://127.0.0.1:8000/api/v1';

// 1. Pays
const pays = await fetch(`${API}/localisation/pays/`).then(r => r.json());
const paysId = pays[0].id;

// 2. Provinces
const provinces = await fetch(`${API}/localisation/provinces/?pays_id=${paysId}`).then(r => r.json());
const provinceId = provinces[0].id;

// 3. Districts
const districts = await fetch(`${API}/localisation/districts/?province_id=${provinceId}`).then(r => r.json());
const districtId = districts[0].id;

// 4. Quartiers
const quartiers = await fetch(`${API}/localisation/quartiers/?district_id=${districtId}`).then(r => r.json());
const quartierId = quartiers[0].id;
```

### Charger Données de Référence
```javascript
const [types, niveaux, statuts] = await Promise.all([
  fetch(`${API}/identite/types-utilisateurs/`).then(r => r.json()),
  fetch(`${API}/identite/niveaux-kyc/`).then(r => r.json()),
  fetch(`${API}/identite/statuts-utilisateurs/`).then(r => r.json())
]);
```

## 📝 Payload Exemple

### Inscription CLIENT
```json
{
  "courriel": "client@example.com",
  "numero_telephone": "+25762046725",
  "mot_de_passe": "SecurePass123!",
  "mot_de_passe_confirmation": "SecurePass123!",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "date_naissance": "1990-01-15",
  "pays_id": "uuid-du-pays",
  "province_id": "uuid-de-la-province",
  "district_id": "uuid-du-district",
  "quartier_id": "uuid-du-quartier"
}
```

### Création ADMIN/AGENT
```json
{
  "courriel": "agent@example.com",
  "numero_telephone": "+25768987654",
  "mot_de_passe": "AgentPass123!",
  "mot_de_passe_confirmation": "AgentPass123!",
  "prenom": "Pierre",
  "nom_famille": "Martin",
  "date_naissance": "1988-03-10",
  "type_utilisateur_id": "AGENT",
  "niveau_kyc_id": 2,
  "statut_id": "ACTIF",
  "pays_id": "uuid-du-pays",
  "province_id": "uuid-de-la-province",
  "district_id": "uuid-du-district",
  "quartier_id": "uuid-du-quartier",
  "telephone_verifie": true,
  "courriel_verifie": true
}
```

## 🔑 Champs à Utiliser

| Endpoint | Champ | Type | Usage |
|----------|-------|------|-------|
| types-utilisateurs | `code` | string | `type_utilisateur_id` |
| niveaux-kyc | `niveau` | integer | `niveau_kyc_id` |
| statuts-utilisateurs | `code` | string | `statut_id` |
| pays | `id` | UUID | `pays_id` |
| provinces | `id` | UUID | `province_id` |
| districts | `id` | UUID | `district_id` |
| quartiers | `id` | UUID | `quartier_id` |

## ⚠️ Points Importants

1. **URL Backend:** Port 8000 (pas 3001!)
2. **Pas d'Auth:** Endpoints de localisation en lecture
3. **Filtres:** Utilisez `?pays_id=`, `?province_id=`, `?district_id=`
4. **IDs:** Tous les IDs sont des UUIDs (sauf niveau_kyc qui est un integer)
5. **Cascade:** Pays → Province → District → Quartier

## 🐛 Dépannage Rapide

| Erreur | Solution |
|--------|----------|
| 403 Forbidden | Redémarrer Django |
| CORS Error | Vérifier config CORS |
| Connection Refused | Django pas démarré |
| Port 3001 | Utiliser port 8000 |

## 📚 Documentation Complète

- **INDEX_DOCUMENTATION_LOCALISATION.md** - Index complet
- **RESUME_CORRECTION_ENDPOINTS.md** - Vue d'ensemble
- **GUIDE_TEST_ENDPOINTS_FRONTEND.md** - Tests et intégration
- **OUTPUTS_REELS_ENDPOINTS.md** - Structure des données

---

**✅ Endpoints prêts à l'emploi!** 🚀
