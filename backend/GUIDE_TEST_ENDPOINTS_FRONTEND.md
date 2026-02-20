# 🧪 Guide de Test: Endpoints depuis le Frontend

## 🎯 Objectif

Tester que les endpoints de localisation sont maintenant accessibles depuis votre frontend React (port 3001).

## ⚠️ IMPORTANT: URL Correcte

Vos endpoints backend sont sur le port **8000**, pas 3001!

```javascript
// ❌ FAUX
const url = 'http://localhost:3001/api/v1/localisation/pays/';

// ✅ CORRECT
const url = 'http://127.0.0.1:8000/api/v1/localisation/pays/';
```

## 📝 Tests à Effectuer

### Test 1: Charger les Pays (Sans Authentification)

```javascript
// Dans votre composant React ou console navigateur
fetch('http://127.0.0.1:8000/api/v1/localisation/pays/')
  .then(response => {
    console.log('Status:', response.status); // Devrait être 200
    return response.json();
  })
  .then(data => {
    console.log('Pays:', data);
    // Devrait afficher un tableau de pays
  })
  .catch(error => {
    console.error('Erreur:', error);
  });
```

**Résultat Attendu:**
```javascript
[
  {
    id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    code_iso_2: "BI",
    code_iso_3: "BDI",
    nom: "Burundi",
    nom_anglais: "Burundi",
    indicatif_telephonique: "+257",
    autorise_systeme: true,
    est_actif: true,
    metadonnees: { ... }
  },
  // ... autres pays
]
```

### Test 2: Charger les Provinces d'un Pays

```javascript
// Récupérer d'abord les pays
const pays = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/')
  .then(r => r.json());

// Prendre l'ID du premier pays (Burundi)
const paysId = pays[0].id;

// Charger les provinces de ce pays
const provinces = await fetch(
  `http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=${paysId}`
).then(r => r.json());

console.log('Provinces:', provinces);
```

**Résultat Attendu:**
```javascript
[
  {
    id: "d4e5f6a7-b8c9-0123-def1-234567890123",
    pays: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    code: "BM",
    nom: "Bujumbura Mairie",
    est_actif: true
  },
  // ... autres provinces
]
```

### Test 3: Cascade Complète (Pays → Province → District → Quartier)

```javascript
async function testCascadeLocalisation() {
  try {
    // 1. Charger les pays
    console.log('1. Chargement des pays...');
    const pays = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/')
      .then(r => r.json());
    console.log('✅ Pays chargés:', pays.length);
    
    // 2. Sélectionner le Burundi
    const burundi = pays.find(p => p.code_iso_2 === 'BI');
    console.log('2. Pays sélectionné:', burundi.nom);
    
    // 3. Charger les provinces
    console.log('3. Chargement des provinces...');
    const provinces = await fetch(
      `http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=${burundi.id}`
    ).then(r => r.json());
    console.log('✅ Provinces chargées:', provinces.length);
    
    // 4. Sélectionner Bujumbura Mairie
    const bujumbura = provinces.find(p => p.code === 'BM');
    console.log('4. Province sélectionnée:', bujumbura.nom);
    
    // 5. Charger les districts
    console.log('5. Chargement des districts...');
    const districts = await fetch(
      `http://127.0.0.1:8000/api/v1/localisation/districts/?province_id=${bujumbura.id}`
    ).then(r => r.json());
    console.log('✅ Districts chargés:', districts.length);
    
    // 6. Sélectionner Mukaza
    const mukaza = districts.find(d => d.code === 'MUK');
    console.log('6. District sélectionné:', mukaza.nom);
    
    // 7. Charger les quartiers
    console.log('7. Chargement des quartiers...');
    const quartiers = await fetch(
      `http://127.0.0.1:8000/api/v1/localisation/quartiers/?district_id=${mukaza.id}`
    ).then(r => r.json());
    console.log('✅ Quartiers chargés:', quartiers.length);
    
    // 8. Afficher le premier quartier
    console.log('8. Premier quartier:', quartiers[0].nom);
    
    console.log('\n🎉 Test cascade réussi!');
    
    return {
      pays: burundi,
      province: bujumbura,
      district: mukaza,
      quartier: quartiers[0]
    };
    
  } catch (error) {
    console.error('❌ Erreur:', error);
  }
}

// Exécuter le test
testCascadeLocalisation();
```

### Test 4: Charger les Données de Référence pour Inscription

```javascript
async function chargerDonneesInscription() {
  try {
    // Charger toutes les données de référence en parallèle
    const [types, niveaux, statuts, pays] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/v1/identite/types-utilisateurs/').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/v1/identite/niveaux-kyc/').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/v1/identite/statuts-utilisateurs/').then(r => r.json()),
      fetch('http://127.0.0.1:8000/api/v1/localisation/pays/').then(r => r.json())
    ]);
    
    console.log('✅ Types utilisateurs:', types.length);
    console.log('✅ Niveaux KYC:', niveaux.length);
    console.log('✅ Statuts:', statuts.length);
    console.log('✅ Pays:', pays.length);
    
    return { types, niveaux, statuts, pays };
    
  } catch (error) {
    console.error('❌ Erreur:', error);
  }
}

// Exécuter le test
chargerDonneesInscription();
```

## 🔧 Composant React Exemple

### Sélecteur de Localisation

```jsx
import React, { useState, useEffect } from 'react';

function SelecteurLocalisation() {
  const [pays, setPays] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [quartiers, setQuartiers] = useState([]);
  
  const [paysSelectionne, setPaysSelectionne] = useState('');
  const [provinceSelectionnee, setProvinceSelectionnee] = useState('');
  const [districtSelectionne, setDistrictSelectionne] = useState('');
  const [quartierSelectionne, setQuartierSelectionne] = useState('');
  
  const API_BASE = 'http://127.0.0.1:8000/api/v1';
  
  // Charger les pays au montage
  useEffect(() => {
    fetch(`${API_BASE}/localisation/pays/`)
      .then(r => r.json())
      .then(data => setPays(data))
      .catch(err => console.error('Erreur pays:', err));
  }, []);
  
  // Charger les provinces quand un pays est sélectionné
  useEffect(() => {
    if (paysSelectionne) {
      fetch(`${API_BASE}/localisation/provinces/?pays_id=${paysSelectionne}`)
        .then(r => r.json())
        .then(data => setProvinces(data))
        .catch(err => console.error('Erreur provinces:', err));
    } else {
      setProvinces([]);
    }
  }, [paysSelectionne]);
  
  // Charger les districts quand une province est sélectionnée
  useEffect(() => {
    if (provinceSelectionnee) {
      fetch(`${API_BASE}/localisation/districts/?province_id=${provinceSelectionnee}`)
        .then(r => r.json())
        .then(data => setDistricts(data))
        .catch(err => console.error('Erreur districts:', err));
    } else {
      setDistricts([]);
    }
  }, [provinceSelectionnee]);
  
  // Charger les quartiers quand un district est sélectionné
  useEffect(() => {
    if (districtSelectionne) {
      fetch(`${API_BASE}/localisation/quartiers/?district_id=${districtSelectionne}`)
        .then(r => r.json())
        .then(data => setQuartiers(data))
        .catch(err => console.error('Erreur quartiers:', err));
    } else {
      setQuartiers([]);
    }
  }, [districtSelectionne]);
  
  return (
    <div>
      <h2>Sélection de Localisation</h2>
      
      <div>
        <label>Pays:</label>
        <select 
          value={paysSelectionne} 
          onChange={(e) => {
            setPaysSelectionne(e.target.value);
            setProvinceSelectionnee('');
            setDistrictSelectionne('');
            setQuartierSelectionne('');
          }}
        >
          <option value="">-- Sélectionner un pays --</option>
          {pays.map(p => (
            <option key={p.id} value={p.id}>
              {p.nom} ({p.code_iso_2})
            </option>
          ))}
        </select>
      </div>
      
      {paysSelectionne && (
        <div>
          <label>Province:</label>
          <select 
            value={provinceSelectionnee} 
            onChange={(e) => {
              setProvinceSelectionnee(e.target.value);
              setDistrictSelectionne('');
              setQuartierSelectionne('');
            }}
          >
            <option value="">-- Sélectionner une province --</option>
            {provinces.map(p => (
              <option key={p.id} value={p.id}>
                {p.nom} ({p.code})
              </option>
            ))}
          </select>
        </div>
      )}
      
      {provinceSelectionnee && (
        <div>
          <label>District:</label>
          <select 
            value={districtSelectionne} 
            onChange={(e) => {
              setDistrictSelectionne(e.target.value);
              setQuartierSelectionne('');
            }}
          >
            <option value="">-- Sélectionner un district --</option>
            {districts.map(d => (
              <option key={d.id} value={d.id}>
                {d.nom} ({d.code})
              </option>
            ))}
          </select>
        </div>
      )}
      
      {districtSelectionne && (
        <div>
          <label>Quartier:</label>
          <select 
            value={quartierSelectionne} 
            onChange={(e) => setQuartierSelectionne(e.target.value)}
          >
            <option value="">-- Sélectionner un quartier --</option>
            {quartiers.map(q => (
              <option key={q.id} value={q.id}>
                {q.nom} ({q.code})
              </option>
            ))}
          </select>
        </div>
      )}
      
      {quartierSelectionne && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#e8f5e9' }}>
          <h3>✅ Sélection Complète</h3>
          <p>Pays ID: {paysSelectionne}</p>
          <p>Province ID: {provinceSelectionnee}</p>
          <p>District ID: {districtSelectionne}</p>
          <p>Quartier ID: {quartierSelectionne}</p>
        </div>
      )}
    </div>
  );
}

export default SelecteurLocalisation;
```

## 🐛 Dépannage

### Erreur: CORS

Si vous voyez:
```
Access to fetch at 'http://127.0.0.1:8000/...' from origin 'http://localhost:3001' 
has been blocked by CORS policy
```

**Solution:** Vérifiez que Django a CORS configuré dans `config/settings/base.py`:
```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001',
    'http://127.0.0.1:3001',
]
```

### Erreur: 403 Forbidden

Si vous voyez toujours 403:
1. Vérifiez que le serveur Django est redémarré
2. Vérifiez l'URL (doit être port 8000, pas 3001)
3. Vérifiez que vous utilisez GET, pas POST

### Erreur: Connection Refused

Si vous voyez:
```
Failed to fetch: net::ERR_CONNECTION_REFUSED
```

**Solution:** Le serveur Django n'est pas démarré. Lancez:
```bash
python manage.py runserver
```

## ✅ Checklist de Test

- [ ] Les pays se chargent sans erreur 403
- [ ] Les provinces se chargent avec filtre `pays_id`
- [ ] Les districts se chargent avec filtre `province_id`
- [ ] Les quartiers se chargent avec filtre `district_id`
- [ ] La cascade complète fonctionne
- [ ] Les IDs sont bien des UUIDs
- [ ] Les données de référence (types, niveaux, statuts) se chargent
- [ ] Le composant React affiche les sélecteurs en cascade

## 🎉 Succès!

Si tous les tests passent, vous pouvez maintenant:
1. ✅ Créer un formulaire d'inscription CLIENT
2. ✅ Créer un formulaire de création ADMIN/AGENT/MARCHAND
3. ✅ Utiliser les IDs dans vos payloads
4. ✅ Envoyer les requêtes de création d'utilisateur

**Bon développement!** 🚀
