# Service SMS de Confirmation - Version 2

## Nouveautés

✅ **Durée de validité : 15 minutes** (au lieu de 5)  
✅ **Stockage en base de données** (au lieu de Redis)  
✅ **Historique des changements de mot de passe**  
✅ **Remplacement automatique des codes** (si nouveau code envoyé avant expiration)  
✅ **Vérification stricte** (code + téléphone + délai)  
✅ **Traçabilité complète** (IP, user agent, dates)

## Architecture

### Tables de Base de Données

#### 1. `authentification.codes_confirmation_sms`

Stocke tous les codes SMS envoyés avec leur statut.

```sql
CREATE TABLE authentification.codes_confirmation_sms (
    id UUID PRIMARY KEY,
    utilisateur_id UUID,
    numero_telephone VARCHAR(20) NOT NULL,
    courriel VARCHAR(254),
    prenom VARCHAR(100),
    code VARCHAR(5) NOT NULL,
    code_formate VARCHAR(50) NOT NULL,
    type_code VARCHAR(30) NOT NULL,
    date_creation TIMESTAMP NOT NULL,
    date_expiration TIMESTAMP NOT NULL,
    duree_validite_minutes INTEGER DEFAULT 15,
    statut VARCHAR(20) NOT NULL,  -- ACTIF, UTILISE, EXPIRE, REMPLACE
    date_utilisation TIMESTAMP,
    nombre_tentatives INTEGER DEFAULT 0,
    adresse_ip INET,
    user_agent TEXT,
    message_envoye TEXT,
    reponse_service_sms JSONB,
    metadonnees JSONB
);
```

#### 2. `authentification.historique_mot_de_passe`

Enregistre tous les changements de mot de passe.

```sql
CREATE TABLE authentification.historique_mot_de_passe (
    id UUID PRIMARY KEY,
    utilisateur_id UUID NOT NULL,
    courriel VARCHAR(254) NOT NULL,
    numero_telephone VARCHAR(20) NOT NULL,
    type_changement VARCHAR(30) NOT NULL,
    ancien_hash VARCHAR(255),
    nouveau_hash VARCHAR(255) NOT NULL,
    adresse_ip INET,
    user_agent TEXT,
    code_confirmation_utilise VARCHAR(5),
    date_changement TIMESTAMP NOT NULL,
    raison TEXT,
    metadonnees JSONB
);
```

## Endpoints API

### 1. Envoyer un Code de Confirmation

**URL** : `POST /api/v1/authentification/envoyer-code-confirmation/`

**Body** :
```json
{
  "telephone": "62046725",
  "prenom": "Jean-luc"
}
```

**Réponse** :
```json
{
  "success": true,
  "message": "Code de confirmation envoyé avec succès",
  "code_formate": "UF-CCF-PSW-12345",
  "telephone": "62046725",
  "date_expiration": "2024-01-15T10:45:00Z",
  "duree_validite_minutes": 15
}
```

**Comportement** :
- Si un code actif existe déjà pour ce numéro, il est marqué comme "REMPLACE"
- Un nouveau code est généré et envoyé
- Le code est valide pendant 15 minutes

### 2. Vérifier un Code

**URL** : `POST /api/v1/authentification/verifier-code-confirmation/`

**Body** :
```json
{
  "telephone": "62046725",
  "code": "12345"
}
```

**Réponse Succès** :
```json
{
  "success": true,
  "message": "Code de confirmation valide",
  "telephone": "62046725",
  "type_code": "VERIFICATION_TELEPHONE",
  "utilisateur_id": "uuid"
}
```

**Réponse Erreur** :
```json
{
  "success": false,
  "message": "Code invalide ou expiré"
}
```

**Comportement** :
- Vérifie que le code correspond au numéro de téléphone
- Vérifie que le code n'est pas expiré (15 minutes)
- Incrémente le compteur de tentatives
- Marque le code comme "UTILISE" si valide
- Marque le code comme "EXPIRE" si expiré

### 3. Réinitialiser le Mot de Passe avec SMS

**URL** : `POST /api/v1/authentification/reinitialiser-mot-de-passe-sms/`

**Body** :
```json
{
  "telephone": "62046725",
  "code": "12345",
  "nouveau_mot_de_passe": "NouveauMotDePasse123!",
  "nouveau_mot_de_passe_confirmation": "NouveauMotDePasse123!"
}
```

**Réponse** :
```json
{
  "success": true,
  "message": "Mot de passe réinitialisé avec succès",
  "nombre_changements_total": 3
}
```

**Comportement** :
1. Vérifie le code SMS
2. Trouve l'utilisateur par numéro de téléphone
3. Change le mot de passe dans `identite.utilisateurs`
4. Synchronise avec `users.User`
5. Enregistre dans l'historique
6. Met à jour `derniere_modification_mdp`
7. Retourne le nombre total de changements

### 4. Consulter l'Historique

**URL** : `GET /api/v1/authentification/historique-mot-de-passe/`

**Headers** : `Authorization: Bearer <token>`

**Réponse** :
```json
{
  "nombre_total": 5,
  "historique": [
    {
      "id": "uuid",
      "type_changement": "REINITIALISATION",
      "type_changement_display": "Réinitialisation par SMS",
      "date_changement": "2024-01-15T10:30:00Z",
      "adresse_ip": "192.168.1.1",
      "code_utilise": "12345",
      "raison": "Réinitialisation par code SMS"
    },
    {
      "id": "uuid",
      "type_changement": "MODIFICATION",
      "type_changement_display": "Modification par l'utilisateur",
      "date_changement": "2024-01-10T14:20:00Z",
      "adresse_ip": "192.168.1.2",
      "code_utilise": "",
      "raison": "Modification par l'utilisateur"
    }
  ]
}
```

## Flux Complet : Réinitialisation de Mot de Passe

### Étape 1 : Demander un code

```javascript
// Frontend
const response = await fetch('/api/v1/authentification/envoyer-code-confirmation/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    telephone: '62046725',
    prenom: 'Jean-luc'
  })
});

const data = await response.json();
// {
//   "success": true,
//   "code_formate": "UF-CCF-PSW-12345",
//   "date_expiration": "2024-01-15T10:45:00Z"
// }
```

### Étape 2 : L'utilisateur reçoit le SMS

```
Message SMS :
"Bonjour Jean-luc, votre code de confirmation est: UF-CCF-PSW-12345"
```

### Étape 3 : Réinitialiser le mot de passe

```javascript
// Frontend
const resetResponse = await fetch('/api/v1/authentification/reinitialiser-mot-de-passe-sms/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    telephone: '62046725',
    code: '12345',
    nouveau_mot_de_passe: 'NouveauMotDePasse123!',
    nouveau_mot_de_passe_confirmation: 'NouveauMotDePasse123!'
  })
});

const resetData = await resetResponse.json();
// {
//   "success": true,
//   "message": "Mot de passe réinitialisé avec succès",
//   "nombre_changements_total": 3
// }
```

## Logique de Remplacement des Codes

### Scénario : Nouvel envoi avant expiration

```python
# Utilisateur demande un code
envoyer_code_confirmation("62046725")  # Code: 12345, expire dans 15 min

# 5 minutes plus tard, l'utilisateur redemande un code
envoyer_code_confirmation("62046725")  # Code: 67890, expire dans 15 min

# Résultat en base de données :
# Code 12345 : statut = "REMPLACE"
# Code 67890 : statut = "ACTIF"

# Seul le code 67890 est valide
verifier_code_confirmation("62046725", "12345")  # ❌ Invalide
verifier_code_confirmation("62046725", "67890")  # ✅ Valide
```

## Sécurité

### Traçabilité

Chaque action est enregistrée avec :
- Adresse IP
- User Agent
- Date et heure
- Code utilisé (si applicable)

### Limites

- Code valide : 15 minutes
- Nombre de tentatives : illimité (mais tracé)
- Un seul code actif par numéro à la fois

### Historique

- Tous les changements de mot de passe sont enregistrés
- Impossible de supprimer l'historique
- Consultation limitée à l'utilisateur connecté

## Types de Changement de Mot de Passe

| Type | Description |
|------|-------------|
| `CREATION` | Création du compte |
| `MODIFICATION` | Modification par l'utilisateur |
| `REINITIALISATION` | Réinitialisation par SMS |
| `REINITIALISATION_EMAIL` | Réinitialisation par email |
| `FORCE_ADMIN` | Forcé par un administrateur |
| `EXPIRATION` | Changement suite à expiration |

## Types de Code SMS

| Type | Description |
|------|-------------|
| `VERIFICATION_TELEPHONE` | Vérification de téléphone |
| `REINITIALISATION_MDP` | Réinitialisation mot de passe |
| `DOUBLE_AUTH` | Double authentification |
| `CONFIRMATION_TRANSACTION` | Confirmation de transaction |
| `AUTRE` | Autre |

## Statuts de Code

| Statut | Description |
|--------|-------------|
| `ACTIF` | Code valide et utilisable |
| `UTILISE` | Code déjà utilisé |
| `EXPIRE` | Code expiré (> 15 minutes) |
| `REMPLACE` | Remplacé par un nouveau code |

## Tâches Automatiques

### Nettoyage des codes expirés

```python
# Tâche Celery exécutée toutes les heures
@shared_task
def nettoyer_codes_expires_task():
    """Marque tous les codes expirés comme EXPIRE"""
    count = nettoyer_codes_expires()
    return count
```

Configuration Celery :
```python
# config/celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'nettoyer-codes-expires': {
        'task': 'authentication.nettoyer_codes_expires',
        'schedule': crontab(minute=0),  # Toutes les heures
    },
}
```

## Migration

### Créer les tables

```bash
python manage.py makemigrations authentication
python manage.py migrate authentication
```

### Vérifier les tables

```sql
-- Vérifier la table des codes
SELECT * FROM authentification.codes_confirmation_sms 
ORDER BY date_creation DESC 
LIMIT 10;

-- Vérifier l'historique
SELECT * FROM authentification.historique_mot_de_passe 
ORDER BY date_changement DESC 
LIMIT 10;

-- Statistiques
SELECT 
    statut, 
    COUNT(*) as nombre 
FROM authentification.codes_confirmation_sms 
GROUP BY statut;
```

## Tests

### Test complet

```bash
python test_sms_confirmation.py
```

### Test manuel

```bash
# 1. Envoyer un code
curl -X POST http://localhost:8000/api/v1/authentification/envoyer-code-confirmation/ \
  -H "Content-Type: application/json" \
  -d '{"telephone": "62046725", "prenom": "Jean-luc"}'

# 2. Réinitialiser le mot de passe
curl -X POST http://localhost:8000/api/v1/authentification/reinitialiser-mot-de-passe-sms/ \
  -H "Content-Type: application/json" \
  -d '{
    "telephone": "62046725",
    "code": "12345",
    "nouveau_mot_de_passe": "NouveauMdp123!",
    "nouveau_mot_de_passe_confirmation": "NouveauMdp123!"
  }'

# 3. Consulter l'historique (nécessite authentification)
curl -X GET http://localhost:8000/api/v1/authentification/historique-mot-de-passe/ \
  -H "Authorization: Bearer <votre_token>"
```

## Monitoring

### Requêtes utiles

```sql
-- Codes actifs
SELECT COUNT(*) FROM authentification.codes_confirmation_sms 
WHERE statut = 'ACTIF';

-- Codes expirés aujourd'hui
SELECT COUNT(*) FROM authentification.codes_confirmation_sms 
WHERE statut = 'EXPIRE' 
AND DATE(date_creation) = CURRENT_DATE;

-- Changements de mot de passe aujourd'hui
SELECT COUNT(*) FROM authentification.historique_mot_de_passe 
WHERE DATE(date_changement) = CURRENT_DATE;

-- Top 10 utilisateurs avec le plus de changements
SELECT 
    courriel, 
    COUNT(*) as nombre_changements 
FROM authentification.historique_mot_de_passe 
GROUP BY courriel 
ORDER BY nombre_changements DESC 
LIMIT 10;
```

## Dépendances

- Django 4.2+
- PostgreSQL (pour JSONB et UUID)
- Celery (pour les tâches périodiques)
- requests (pour l'API SMS)

## Variables d'Environnement

```bash
SMS_SERVICE_URL=https://prodev.mediabox.bi:22629/sms
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ufaranga
DB_USER=admin
DB_PASSWORD=secret123
```
