# 🏦 Schéma Amélioré - Système Bancaire Professionnel

## 🎯 Objectifs

1. **Localisation complète**: Pays → Province → Ville → Commune → Quartier → Avenue
2. **Gestion des numéros**: Code pays + validation + limite par utilisateur
3. **Traçabilité**: Qui a créé/modifié quoi et quand
4. **Sécurité**: Contrôle des numéros autorisés par pays

---

## 📊 Structure des Tables

### 1. PAYS (localisation.pays)

```sql
CREATE TABLE localisation.pays (
    -- Identifiant
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Codes ISO
    code_iso_alpha2 CHAR(2) UNIQUE NOT NULL,        -- Ex: BI, RW, CD
    code_iso_alpha3 CHAR(3) UNIQUE NOT NULL,        -- Ex: BDI, RWA, COD
    code_iso_numerique CHAR(3) UNIQUE NOT NULL,     -- Ex: 108, 646, 180
    
    -- Informations
    nom_officiel VARCHAR(200) NOT NULL,              -- Ex: République du Burundi
    nom_court VARCHAR(100) NOT NULL,                 -- Ex: Burundi
    nom_local VARCHAR(200),                          -- Ex: Republika y'Uburundi
    
    -- Téléphonie
    code_telephonique VARCHAR(10) NOT NULL,          -- Ex: +257, +250, +243
    format_numero_national VARCHAR(50),              -- Ex: XX XX XX XX
    longueur_numero_min INTEGER DEFAULT 8,
    longueur_numero_max INTEGER DEFAULT 15,
    regex_validation VARCHAR(200),                   -- Ex: ^[67]\d{7}$
    
    -- Devise
    code_devise CHAR(3) NOT NULL,                    -- Ex: BIF, RWF, CDF
    symbole_devise VARCHAR(10),                      -- Ex: FBu, RF, FC
    
    -- Géographie
    continent VARCHAR(50),                           -- Ex: Afrique
    sous_region VARCHAR(100),                        -- Ex: Afrique de l'Est
    capitale VARCHAR(100),
    
    -- Statut
    est_actif BOOLEAN DEFAULT true,
    autorise_inscription BOOLEAN DEFAULT true,       -- Permet inscription depuis ce pays
    autorise_transactions BOOLEAN DEFAULT true,      -- Permet transactions
    niveau_risque VARCHAR(20) DEFAULT 'NORMAL',      -- FAIBLE, NORMAL, ELEVE
    
    -- Limites par défaut pour ce pays
    limite_numeros_par_utilisateur INTEGER DEFAULT 3,
    limite_transaction_journaliere NUMERIC(15,2),
    
    -- Métadonnées
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    cree_par UUID,
    modifie_par UUID,
    metadonnees JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_pays_code_iso2 ON localisation.pays(code_iso_alpha2);
CREATE INDEX idx_pays_code_tel ON localisation.pays(code_telephonique);
CREATE INDEX idx_pays_actif ON localisation.pays(est_actif);
```

### 2. NUMEROS_TELEPHONE (identite.numeros_telephone)

```sql
CREATE TABLE identite.numeros_telephone (
    -- Identifiant
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Utilisateur
    utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id) ON DELETE CASCADE,
    
    -- Numéro
    pays_id UUID NOT NULL REFERENCES localisation.pays(id),
    code_pays VARCHAR(10) NOT NULL,                  -- Ex: +257
    numero_national VARCHAR(20) NOT NULL,            -- Ex: 62046725 (sans code pays)
    numero_complet VARCHAR(30) NOT NULL UNIQUE,      -- Ex: +25762046725
    numero_formate VARCHAR(30),                      -- Ex: +257 62 04 67 25
    
    -- Type et usage
    type_numero VARCHAR(20) DEFAULT 'MOBILE',        -- MOBILE, FIXE, VOIP
    usage VARCHAR(20) DEFAULT 'PERSONNEL',           -- PERSONNEL, PROFESSIONNEL, URGENCE
    est_principal BOOLEAN DEFAULT false,             -- Numéro principal de l'utilisateur
    
    -- Vérification
    est_verifie BOOLEAN DEFAULT false,
    date_verification TIMESTAMP WITH TIME ZONE,
    methode_verification VARCHAR(50),                -- SMS, APPEL, WHATSAPP
    code_verification_hash VARCHAR(255),
    tentatives_verification INTEGER DEFAULT 0,
    derniere_tentative_verification TIMESTAMP WITH TIME ZONE,
    
    -- Statut
    statut VARCHAR(20) DEFAULT 'ACTIF',              -- ACTIF, SUSPENDU, BLOQUE, SUPPRIME
    raison_statut TEXT,
    date_changement_statut TIMESTAMP WITH TIME ZONE,
    
    -- Sécurité
    nombre_connexions_reussies INTEGER DEFAULT 0,
    nombre_connexions_echouees INTEGER DEFAULT 0,
    derniere_connexion TIMESTAMP WITH TIME ZONE,
    derniere_connexion_ip INET,
    
    -- Opérateur télécom (optionnel)
    operateur VARCHAR(100),                          -- Ex: Econet, Lumitel, Smart
    type_ligne VARCHAR(20),                          -- PREPAYE, POSTPAYE
    
    -- Métadonnées
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_suppression TIMESTAMP WITH TIME ZONE,       -- Soft delete
    cree_par UUID,
    modifie_par UUID,
    metadonnees JSONB DEFAULT '{}'::jsonb,
    
    -- Contraintes
    CONSTRAINT chk_numero_format CHECK (numero_complet ~ '^\+[1-9]\d{1,14}$'),
    CONSTRAINT chk_un_seul_principal_par_user UNIQUE (utilisateur_id, est_principal) 
        WHERE est_principal = true
);

-- Index
CREATE INDEX idx_numeros_utilisateur ON identite.numeros_telephone(utilisateur_id);
CREATE INDEX idx_numeros_pays ON identite.numeros_telephone(pays_id);
CREATE INDEX idx_numeros_complet ON identite.numeros_telephone(numero_complet);
CREATE INDEX idx_numeros_statut ON identite.numeros_telephone(statut);
CREATE INDEX idx_numeros_verifie ON identite.numeros_telephone(est_verifie);
CREATE INDEX idx_numeros_principal ON identite.numeros_telephone(utilisateur_id, est_principal) 
    WHERE est_principal = true;
```

### 3. UTILISATEURS (identite.utilisateurs) - MODIFIÉ

```sql
ALTER TABLE identite.utilisateurs
    -- Supprimer l'ancien champ numero_telephone
    DROP COLUMN IF EXISTS numero_telephone,
    
    -- Ajouter référence au numéro principal
    ADD COLUMN numero_telephone_principal_id UUID 
        REFERENCES identite.numeros_telephone(id) ON DELETE SET NULL,
    
    -- Nationalité (référence au pays)
    ADD COLUMN nationalite_id UUID 
        REFERENCES localisation.pays(id),
    
    -- Pays de résidence (référence au pays)
    ADD COLUMN pays_residence_id UUID 
        REFERENCES localisation.pays(id),
    
    -- Localisation détaillée
    ADD COLUMN pays_id UUID 
        REFERENCES localisation.pays(id),
    ADD COLUMN province_id UUID 
        REFERENCES localisation.provinces(id),
    ADD COLUMN ville_id UUID 
        REFERENCES localisation.villes(id),
    ADD COLUMN commune_id UUID 
        REFERENCES localisation.communes(id),
    ADD COLUMN quartier_id UUID 
        REFERENCES localisation.quartiers(id),
    ADD COLUMN avenue VARCHAR(200),
    ADD COLUMN numero_maison VARCHAR(50),
    
    -- Adresse complète (générée automatiquement)
    ADD COLUMN adresse_complete TEXT GENERATED ALWAYS AS (
        CONCAT_WS(', ',
            NULLIF(avenue, ''),
            NULLIF(numero_maison, ''),
            NULLIF(quartier, ''),
            NULLIF(commune, ''),
            NULLIF(ville, ''),
            NULLIF(province, '')
        )
    ) STORED;
```

### 4. HISTORIQUE_NUMEROS (identite.historique_numeros_telephone)

```sql
CREATE TABLE identite.historique_numeros_telephone (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Référence
    numero_telephone_id UUID NOT NULL REFERENCES identite.numeros_telephone(id),
    utilisateur_id UUID NOT NULL REFERENCES identite.utilisateurs(id),
    
    -- Action
    action VARCHAR(50) NOT NULL,                     -- AJOUT, VERIFICATION, MODIFICATION, SUPPRESSION, SUSPENSION
    ancien_statut VARCHAR(20),
    nouveau_statut VARCHAR(20),
    
    -- Détails
    raison TEXT,
    details JSONB DEFAULT '{}'::jsonb,
    
    -- Traçabilité
    date_action TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    effectue_par UUID,                               -- ID de l'utilisateur ou admin qui a fait l'action
    adresse_ip INET,
    user_agent TEXT
);

CREATE INDEX idx_historique_numero ON identite.historique_numeros_telephone(numero_telephone_id);
CREATE INDEX idx_historique_utilisateur ON identite.historique_numeros_telephone(utilisateur_id);
CREATE INDEX idx_historique_date ON identite.historique_numeros_telephone(date_action DESC);
```

### 5. LIMITES_NUMEROS_PAR_PAYS (identite.limites_numeros_par_pays)

```sql
CREATE TABLE identite.limites_numeros_par_pays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Pays
    pays_id UUID NOT NULL REFERENCES localisation.pays(id),
    
    -- Type d'utilisateur
    type_utilisateur VARCHAR(20) NOT NULL REFERENCES identite.types_utilisateurs(code),
    
    -- Limites
    nombre_max_numeros INTEGER NOT NULL DEFAULT 3,
    nombre_max_numeros_verifies INTEGER NOT NULL DEFAULT 2,
    
    -- Restrictions
    autorise_numeros_etrangers BOOLEAN DEFAULT false,
    pays_autorises UUID[],                           -- Array de pays_id autorisés
    
    -- Métadonnées
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT uq_limite_pays_type UNIQUE (pays_id, type_utilisateur)
);
```

---

## 🔄 Relations et Contraintes

### Règles Métier

1. **Un utilisateur peut avoir plusieurs numéros** (limite selon pays et type)
2. **Un numéro ne peut appartenir qu'à un seul utilisateur**
3. **Un seul numéro principal par utilisateur**
4. **Validation du format selon le pays**
5. **Historique complet de tous les changements**

### Triggers à Créer

```sql
-- 1. Vérifier la limite de numéros par utilisateur
CREATE OR REPLACE FUNCTION verifier_limite_numeros()
RETURNS TRIGGER AS $$
DECLARE
    nb_numeros INTEGER;
    limite INTEGER;
BEGIN
    -- Compter les numéros actifs de l'utilisateur
    SELECT COUNT(*) INTO nb_numeros
    FROM identite.numeros_telephone
    WHERE utilisateur_id = NEW.utilisateur_id
      AND statut = 'ACTIF';
    
    -- Récupérer la limite
    SELECT nombre_max_numeros INTO limite
    FROM identite.limites_numeros_par_pays
    WHERE pays_id = NEW.pays_id
      AND type_utilisateur = (
          SELECT type_utilisateur 
          FROM identite.utilisateurs 
          WHERE id = NEW.utilisateur_id
      );
    
    -- Utiliser la limite par défaut du pays si pas de limite spécifique
    IF limite IS NULL THEN
        SELECT limite_numeros_par_utilisateur INTO limite
        FROM localisation.pays
        WHERE id = NEW.pays_id;
    END IF;
    
    -- Vérifier
    IF nb_numeros >= limite THEN
        RAISE EXCEPTION 'Limite de numéros atteinte (% max)', limite;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_verifier_limite_numeros
BEFORE INSERT ON identite.numeros_telephone
FOR EACH ROW
EXECUTE FUNCTION verifier_limite_numeros();

-- 2. Enregistrer dans l'historique
CREATE OR REPLACE FUNCTION enregistrer_historique_numero()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO identite.historique_numeros_telephone
        (numero_telephone_id, utilisateur_id, action, nouveau_statut)
        VALUES (NEW.id, NEW.utilisateur_id, 'AJOUT', NEW.statut);
    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.statut != NEW.statut THEN
            INSERT INTO identite.historique_numeros_telephone
            (numero_telephone_id, utilisateur_id, action, ancien_statut, nouveau_statut)
            VALUES (NEW.id, NEW.utilisateur_id, 'MODIFICATION', OLD.statut, NEW.statut);
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_historique_numero
AFTER INSERT OR UPDATE ON identite.numeros_telephone
FOR EACH ROW
EXECUTE FUNCTION enregistrer_historique_numero();

-- 3. Valider le format du numéro selon le pays
CREATE OR REPLACE FUNCTION valider_format_numero()
RETURNS TRIGGER AS $$
DECLARE
    regex_pays VARCHAR(200);
    longueur_min INTEGER;
    longueur_max INTEGER;
BEGIN
    -- Récupérer les règles du pays
    SELECT regex_validation, longueur_numero_min, longueur_numero_max
    INTO regex_pays, longueur_min, longueur_max
    FROM localisation.pays
    WHERE id = NEW.pays_id;
    
    -- Vérifier la longueur
    IF LENGTH(NEW.numero_national) < longueur_min 
       OR LENGTH(NEW.numero_national) > longueur_max THEN
        RAISE EXCEPTION 'Longueur de numéro invalide (min: %, max: %)', 
            longueur_min, longueur_max;
    END IF;
    
    -- Vérifier le format avec regex si défini
    IF regex_pays IS NOT NULL AND NEW.numero_national !~ regex_pays THEN
        RAISE EXCEPTION 'Format de numéro invalide pour ce pays';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valider_format_numero
BEFORE INSERT OR UPDATE ON identite.numeros_telephone
FOR EACH ROW
EXECUTE FUNCTION valider_format_numero();
```

---

## 📝 Exemples d'Utilisation

### Ajouter un numéro à un utilisateur

```sql
INSERT INTO identite.numeros_telephone (
    utilisateur_id,
    pays_id,
    code_pays,
    numero_national,
    numero_complet,
    type_numero,
    usage,
    est_principal
) VALUES (
    'uuid-utilisateur',
    (SELECT id FROM localisation.pays WHERE code_iso_alpha2 = 'BI'),
    '+257',
    '62046725',
    '+25762046725',
    'MOBILE',
    'PERSONNEL',
    true
);
```

### Vérifier combien de numéros un utilisateur peut encore ajouter

```sql
SELECT 
    u.id,
    u.prenom,
    u.nom_famille,
    COUNT(nt.id) as numeros_actuels,
    COALESCE(l.nombre_max_numeros, p.limite_numeros_par_utilisateur) as limite,
    COALESCE(l.nombre_max_numeros, p.limite_numeros_par_utilisateur) - COUNT(nt.id) as numeros_restants
FROM identite.utilisateurs u
LEFT JOIN identite.numeros_telephone nt ON nt.utilisateur_id = u.id AND nt.statut = 'ACTIF'
LEFT JOIN localisation.pays p ON p.id = u.pays_residence_id
LEFT JOIN identite.limites_numeros_par_pays l ON l.pays_id = p.id AND l.type_utilisateur = u.type_utilisateur
WHERE u.id = 'uuid-utilisateur'
GROUP BY u.id, u.prenom, u.nom_famille, l.nombre_max_numeros, p.limite_numeros_par_utilisateur;
```

---

## 🎯 Avantages de Cette Structure

1. ✅ **Séparation des préoccupations**: Numéros dans leur propre table
2. ✅ **Validation automatique**: Format selon le pays
3. ✅ **Limites configurables**: Par pays et type d'utilisateur
4. ✅ **Historique complet**: Traçabilité de tous les changements
5. ✅ **Sécurité**: Contrôle des numéros autorisés
6. ✅ **Scalabilité**: Peut gérer des millions d'utilisateurs
7. ✅ **Conformité**: Respect des normes bancaires
8. ✅ **Flexibilité**: Facile d'ajouter de nouvelles règles

---

## 📊 Statistiques Possibles

```sql
-- Nombre de numéros par pays
SELECT 
    p.nom_court,
    COUNT(nt.id) as nombre_numeros,
    COUNT(DISTINCT nt.utilisateur_id) as nombre_utilisateurs
FROM localisation.pays p
LEFT JOIN identite.numeros_telephone nt ON nt.pays_id = p.id
GROUP BY p.nom_court
ORDER BY nombre_numeros DESC;

-- Utilisateurs avec plusieurs numéros
SELECT 
    u.prenom,
    u.nom_famille,
    COUNT(nt.id) as nombre_numeros,
    STRING_AGG(nt.numero_complet, ', ') as numeros
FROM identite.utilisateurs u
JOIN identite.numeros_telephone nt ON nt.utilisateur_id = u.id
WHERE nt.statut = 'ACTIF'
GROUP BY u.id, u.prenom, u.nom_famille
HAVING COUNT(nt.id) > 1;
```
