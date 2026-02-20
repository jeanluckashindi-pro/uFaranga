# 📋 Résumé - Endpoints Module IDENTITÉ

## 🎯 Endpoints Disponibles

### 1. Créer un Utilisateur Complet

```
POST /api/v1/identite/utilisateurs/creer/
```

**Crée un utilisateur avec TOUS les détails:**
- Informations personnelles (nom, prénom, date de naissance, etc.)
- Type d'utilisateur (CLIENT, AGENT, MARCHAND, ADMIN, etc.)
- Niveau KYC (0, 1, 2, 3) avec limites de transaction
- Statut (ACTIF, EN_VERIFICATION, SUSPENDU, BLOQUE, FERME)
- Localisation complète (pays, province, district, quartier)
- Adresse détaillée (avenue, numéro de maison, etc.)
- Profil automatique créé
- Tokens JWT pour connexion immédiate

**Exemple minimal:**
```json
{
  "courriel": "user@example.com",
  "numero_telephone": "+25762046725",
  "mot_de_passe": "SecurePass123!",
  "mot_de_passe_confirmation": "SecurePass123!",
  "prenom": "Jean",
  "nom_famille": "Dupont",
  "date_naissance": "1990-01-15"
}
```

**Exemple complet (Agent):**
```json
{
  "courriel": "agent@ufaranga.bi",
  "numero_telephone": "+25768987654",
  "mot_de_passe": "AgentPass789!",
  "mot_de_passe_confirmation": "AgentPass789!",
  "prenom": "Pierre",
  "nom_famille": "Nkurunziza",
  "date_naissance": "1988-03-10",
  "lieu_naissance": "Bujumbura",
  "nationalite": "BI",
  "type_utilisateur_code": "AGENT",
  "niveau_kyc_code": 2,
  "statut_code": "ACTIF",
  "pays_code": "BI",
  "province_code": "BM",
  "district_code": "MUK",
  "quartier_code": "ROH",
  "province": "Bujumbura Mairie",
  "ville": "Bujumbura",
  "commune": "Mukaza",
  "quartier": "Rohero",
  "avenue": "Avenue du Commerce",
  "numero_maison": "789"
}
```

---

### 2. Profil Utilisateur Connecté (avec Expands)

```
GET /api/v1/identite/moi/
```

**Retourne TOUTES les informations avec expands:**
- `type_utilisateur_details` - Détails du type (CLIENT, AGENT, etc.)
- `niveau_kyc_details` - Niveau KYC avec limites
- `statut_details` - Statut avec permissions
- `numeros_telephone` - Liste de tous les numéros
- `pays_details` - Infos du pays avec téléphonie et devise
- `province_details` - Détails de la province
- `district_details` - Détails du district
- `quartier_details` - Détails du quartier
- `profil` - Préférences et notifications

**Tout en une seule requête!**

---

### 3. Tables de Référence

#### Types d'Utilisateurs
```
GET /api/v1/identite/types-utilisateurs/
```

Retourne: CLIENT, AGENT, MARCHAND, ADMIN, SUPER_ADMIN, SYSTEME

#### Niveaux KYC
```
GET /api/v1/identite/niveaux-kyc/
```

Retourne: Niveaux 0, 1, 2, 3 avec limites de transaction

#### Statuts Utilisateurs
```
GET /api/v1/identite/statuts-utilisateurs/
```

Retourne: ACTIF, EN_VERIFICATION, SUSPENDU, BLOQUE, FERME

---

### 4. Gestion des Numéros de Téléphone

#### Lister les numéros
```
GET /api/v1/identite/numeros-telephone/
```

#### Ajouter un numéro
```
POST /api/v1/identite/numeros-telephone/ajouter_numero/
{
  "pays_code_iso_2": "BI",
  "code_pays": "+257",
  "numero_national": "79123456",
  "numero_complet": "+25779123456",
  "type_numero": "MOBILE",
  "usage": "PERSONNEL",
  "operateur": "Lumitel"
}
```

#### Envoyer code de vérification
```
POST /api/v1/identite/numeros-telephone/{id}/envoyer_code_verification/
```

#### Vérifier le code
```
POST /api/v1/identite/numeros-telephone/{id}/verifier_code/
{
  "code": "123456"
}
```

#### Définir comme principal
```
POST /api/v1/identite/numeros-telephone/{id}/definir_principal/
```

#### Voir numéros restants
```
GET /api/v1/identite/numeros-telephone/numeros_restants/?pays_code_iso_2=BI
```

---

## 📊 Données de Référence

### Types d'Utilisateurs

| Code | Libellé | Limite Numéros |
|------|---------|----------------|
| CLIENT | Client | 3 |
| AGENT | Agent | 5 |
| MARCHAND | Marchand | 5 |
| ADMIN | Administrateur | Illimité |
| SUPER_ADMIN | Super Admin | Illimité |
| SYSTEME | Système | Illimité |

### Niveaux KYC

| Niveau | Libellé | Limite Journalière | Solde Max |
|--------|---------|-------------------|-----------|
| 0 | Non vérifié | 50 000 BIF | 200 000 BIF |
| 1 | Basique | 500 000 BIF | 2 000 000 BIF |
| 2 | Complet | 2 000 000 BIF | 10 000 000 BIF |
| 3 | Premium | 10 000 000 BIF | Illimité |

### Statuts

| Code | Libellé | Connexion | Transactions |
|------|---------|-----------|--------------|
| ACTIF | Actif | ✅ | ✅ |
| EN_VERIFICATION | En vérification | ✅ | ❌ |
| SUSPENDU | Suspendu | ❌ | ❌ |
| BLOQUE | Bloqué | ❌ | ❌ |
| FERME | Fermé | ❌ | ❌ |

---

## 🔄 Flux Complet d'Inscription

```
1. Frontend appelle POST /api/v1/identite/utilisateurs/creer/
   ↓
2. Backend valide les données
   ↓
3. Backend récupère les objets de référence (Type, KYC, Statut)
   ↓
4. Backend récupère les objets de localisation (Pays, Province, etc.)
   ↓
5. Backend crée l'utilisateur dans identite.utilisateurs
   ↓
6. Backend crée le profil automatiquement
   ↓
7. Backend génère les tokens JWT
   ↓
8. Backend retourne utilisateur complet + tokens
   ↓
9. Frontend sauvegarde les tokens
   ↓
10. Frontend redirige vers dashboard
   ↓
11. Utilisateur connecté avec profil complet!
```

---

## 📁 Fichiers Créés

### Backend
- ✅ `apps/identite/serializers.py` - CreerUtilisateurSerializer + Expands
- ✅ `apps/identite/views.py` - CreerUtilisateurView + ViewSets
- ✅ `apps/identite/urls.py` - Routes du module
- ✅ `config/urls.py` - Ajout de l'app identite

### Documentation
- ✅ `ENDPOINT_CREER_UTILISATEUR_COMPLET.md` - Guide complet de création
- ✅ `ENDPOINT_MOI_AVEC_EXPANDS.md` - Guide du profil avec expands
- ✅ `SYSTEME_NUMEROS_TELEPHONE_COMPLETE.md` - Système de numéros
- ✅ `RESUME_ENDPOINTS_IDENTITE.md` - Ce fichier

### Base de Données
- ✅ Tables créées: numeros_telephone, historique_numeros_telephone, limites_numeros_par_pays
- ✅ Métadonnées pays enrichies (téléphonie, devise, géographie)
- ✅ Limites configurées par pays et type d'utilisateur

---

## ✅ Avantages du Système

### 1. Création Complète
- Un seul endpoint pour créer un utilisateur avec TOUS les détails
- Pas besoin de multiples requêtes
- Validation automatique de toutes les relations

### 2. Profil Enrichi
- Endpoint `/moi/` retourne tout avec expands
- Type, KYC, Statut avec détails complets
- Liste des numéros de téléphone
- Localisation complète

### 3. Gestion des Numéros
- Plusieurs numéros par utilisateur
- Vérification par SMS
- Un numéro principal
- Limites selon pays et type
- Historique complet

### 4. Flexibilité
- Champs optionnels pour inscription rapide
- Champs complets pour profil détaillé
- Métadonnées JSON pour données supplémentaires

### 5. Sécurité
- Mots de passe hashés
- Tokens JWT automatiques
- Validation stricte des données
- Historique des changements

---

## 🚀 Utilisation Rapide

### Créer un client simple
```bash
curl -X POST http://127.0.0.1:8000/api/v1/identite/utilisateurs/creer/ \
  -H "Content-Type: application/json" \
  -d '{
    "courriel": "test@example.com",
    "numero_telephone": "+25762046725",
    "mot_de_passe": "TestPass123!",
    "mot_de_passe_confirmation": "TestPass123!",
    "prenom": "Test",
    "nom_famille": "User",
    "date_naissance": "1990-01-01"
  }'
```

### Voir son profil complet
```bash
curl -X GET http://127.0.0.1:8000/api/v1/identite/moi/ \
  -H "Authorization: Bearer <access_token>"
```

### Ajouter un numéro
```bash
curl -X POST http://127.0.0.1:8000/api/v1/identite/numeros-telephone/ajouter_numero/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "pays_code_iso_2": "BI",
    "code_pays": "+257",
    "numero_national": "79123456",
    "numero_complet": "+25779123456",
    "type_numero": "MOBILE",
    "usage": "PROFESSIONNEL"
  }'
```

---

## 📚 Documentation Complète

Consultez les fichiers suivants pour plus de détails:

1. **ENDPOINT_CREER_UTILISATEUR_COMPLET.md** - Tous les détails de création
2. **ENDPOINT_MOI_AVEC_EXPANDS.md** - Profil avec expands
3. **SYSTEME_NUMEROS_TELEPHONE_COMPLETE.md** - Gestion des numéros
4. **ENDPOINT_INSCRIPTION_UTILISATEUR.md** - Inscription simple (ancien)

---

## ✅ Résumé Final

Le module IDENTITÉ est maintenant complet avec:

✅ Endpoint de création d'utilisateur avec TOUS les champs  
✅ Endpoint de profil avec expands complets  
✅ Gestion complète des numéros de téléphone  
✅ Tables de référence (Types, KYC, Statuts)  
✅ Localisation géographique complète  
✅ Validation automatique  
✅ Tokens JWT automatiques  
✅ Documentation complète  

**Tout est prêt pour créer des utilisateurs complets dans la table `identite.utilisateurs`!** 🚀
