# ⚡ Setup Rapide - API Publique

## Problème Actuel

Vous avez deux problèmes à résoudre:

### 1. ❌ Schéma PostgreSQL `developpeurs` n'existe pas encore
### 2. ✅ Swagger fonctionne maintenant (après correction)

---

## 🔧 Solution: Créer le Schéma PostgreSQL

### Option 1: Via psql (Recommandé)

```bash
# Ouvrir une invite de commande
psql -U ufaranga -d ufaranga

# Dans psql, exécuter:
\i D:/Projets/Decima Techno/uFaranga/database_setup/11_schema_developpeurs.sql

# Vérifier que ça a marché:
\dn developpeurs
\dt developpeurs.*

# Quitter
\q
```

### Option 2: Via pgAdmin

1. Ouvrir pgAdmin
2. Se connecter à la base `ufaranga`
3. Clic droit sur la base → Query Tool
4. Ouvrir le fichier `database_setup/11_schema_developpeurs.sql`
5. Exécuter (F5)
6. Vérifier dans Schemas → developpeurs

### Option 3: Copier-Coller le SQL

Si psql ne fonctionne pas, voici le SQL minimal à exécuter:

```sql
-- Créer le schéma
CREATE SCHEMA IF NOT EXISTS developpeurs;

-- Table comptes développeurs
CREATE TABLE developpeurs.comptes_developpeurs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nom_entreprise VARCHAR(200) NOT NULL,
    nom_contact VARCHAR(200) NOT NULL,
    prenom_contact VARCHAR(200),
    courriel_contact VARCHAR(255) UNIQUE NOT NULL,
    telephone_contact VARCHAR(20),
    pays VARCHAR(2) DEFAULT 'BI',
    ville VARCHAR(100),
    type_compte VARCHAR(30) DEFAULT 'SANDBOX',
    statut VARCHAR(20) DEFAULT 'ACTIF',
    courriel_verifie BOOLEAN DEFAULT FALSE,
    quota_requetes_jour INTEGER DEFAULT 1000,
    quota_requetes_mois INTEGER DEFAULT 30000,
    limite_taux_par_minute INTEGER DEFAULT 60,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table clés API
CREATE TABLE developpeurs.cles_api (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    compte_developpeur_id UUID NOT NULL REFERENCES developpeurs.comptes_developpeurs(id) ON DELETE CASCADE,
    cle_api VARCHAR(64) UNIQUE NOT NULL,
    prefixe_cle VARCHAR(20) NOT NULL,
    hash_cle TEXT NOT NULL,
    nom_cle VARCHAR(100) NOT NULL,
    description TEXT,
    environnement VARCHAR(20) DEFAULT 'SANDBOX',
    scopes JSONB DEFAULT '["public:read"]'::jsonb,
    est_active BOOLEAN DEFAULT TRUE,
    date_expiration TIMESTAMP WITH TIME ZONE,
    derniere_utilisation TIMESTAMP WITH TIME ZONE,
    nombre_utilisations BIGINT DEFAULT 0,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Donner les permissions
GRANT ALL ON SCHEMA developpeurs TO ufaranga;
GRANT ALL ON ALL TABLES IN SCHEMA developpeurs TO ufaranga;
GRANT ALL ON ALL SEQUENCES IN SCHEMA developpeurs TO ufaranga;
```

---

## ✅ Après avoir créé le schéma

### 1. Créer un compte développeur

```bash
cd backend
python quick_create_dev_account.py
```

Vous obtiendrez une clé API comme:
```
ufar_test_abc123xyz789def456ghi789jkl012
```

### 2. Tester avec Swagger

Ouvrez votre navigateur:
```
http://127.0.0.1:8000/api/public/docs/
```

1. Cliquez sur **"Authorize"** (en haut à droite)
2. Entrez: `ApiKey ufar_test_abc123xyz789def456ghi789jkl012`
3. Cliquez **"Authorize"**
4. Testez un endpoint (ex: GET /api/public/health/)

### 3. Tester avec cURL

```bash
curl "http://127.0.0.1:8000/api/public/health/" \
  -H "Authorization: ApiKey ufar_test_abc123xyz789def456ghi789jkl012"
```

---

## 🎯 Endpoints Disponibles Sans Clé API

Ces endpoints fonctionnent SANS clé API:

```
✅ http://127.0.0.1:8000/api/public/docs/      # Swagger UI
✅ http://127.0.0.1:8000/api/public/redoc/     # ReDoc
✅ http://127.0.0.1:8000/api/public/schema/    # Schema JSON
```

Testez maintenant:
```
http://127.0.0.1:8000/api/public/docs/
```

---

## 🆘 Si ça ne marche toujours pas

### Vérifier que le serveur tourne
```bash
# Le serveur doit afficher:
# Starting development server at http://127.0.0.1:8000/
```

### Vérifier les logs
```bash
# Dans le terminal où tourne le serveur
# Vous devriez voir les requêtes
```

### Redémarrer le serveur
```bash
# Ctrl+C pour arrêter
# Puis relancer:
python manage.py runserver
```

---

**Une fois le schéma créé, tout fonctionnera! 🚀**
