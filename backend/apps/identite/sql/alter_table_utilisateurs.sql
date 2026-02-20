-- =============================================================================
-- Script SQL pour MODIFIER la table utilisateurs
-- =============================================================================
-- Ajoute les relations (Foreign Keys) vers les tables de référence
-- Usage: Exécuter APRÈS create_tables_reference.sql et init_donnees_reference.sql
-- =============================================================================

-- Activer le schéma identite
SET search_path TO identite, public;

\echo '========================================='
\echo 'MODIFICATION DE LA TABLE UTILISATEURS'
\echo '========================================='
\echo ''

-- =============================================================================
-- ÉTAPE 1: Vérifier que les tables de référence existent et contiennent des données
-- =============================================================================

\echo 'Vérification des tables de référence...'

DO $$
DECLARE
    nb_types INTEGER;
    nb_niveaux INTEGER;
    nb_statuts INTEGER;
BEGIN
    SELECT COUNT(*) INTO nb_types FROM identite.types_utilisateurs;
    SELECT COUNT(*) INTO nb_niveaux FROM identite.niveaux_kyc;
    SELECT COUNT(*) INTO nb_statuts FROM identite.statuts_utilisateurs;
    
    IF nb_types = 0 THEN
        RAISE EXCEPTION 'Table types_utilisateurs est vide. Exécutez init_donnees_reference.sql d''abord.';
    END IF;
    
    IF nb_niveaux = 0 THEN
        RAISE EXCEPTION 'Table niveaux_kyc est vide. Exécutez init_donnees_reference.sql d''abord.';
    END IF;
    
    IF nb_statuts = 0 THEN
        RAISE EXCEPTION 'Table statuts_utilisateurs est vide. Exécutez init_donnees_reference.sql d''abord.';
    END IF;
    
    RAISE NOTICE '✓ Tables de référence OK (types: %, niveaux: %, statuts: %)', nb_types, nb_niveaux, nb_statuts;
END $$;

\echo ''

-- =============================================================================
-- ÉTAPE 2: Sauvegarder les anciennes colonnes (si elles existent)
-- =============================================================================

\echo 'Sauvegarde des anciennes valeurs...'

-- Ajouter des colonnes temporaires pour sauvegarder les anciennes valeurs
ALTER TABLE identite.utilisateurs 
ADD COLUMN IF NOT EXISTS type_utilisateur_old VARCHAR(20),
ADD COLUMN IF NOT EXISTS niveau_kyc_old INTEGER,
ADD COLUMN IF NOT EXISTS statut_old VARCHAR(20);

-- Copier les valeurs actuelles si les colonnes existent
DO $$
BEGIN
    -- Sauvegarder type_utilisateur si c'est un VARCHAR
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'identite' 
        AND table_name = 'utilisateurs' 
        AND column_name = 'type_utilisateur'
        AND data_type = 'character varying'
    ) THEN
        EXECUTE 'UPDATE identite.utilisateurs SET type_utilisateur_old = type_utilisateur';
        RAISE NOTICE '✓ Valeurs type_utilisateur sauvegardées';
    END IF;
    
    -- Sauvegarder niveau_kyc si c'est un INTEGER
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'identite' 
        AND table_name = 'utilisateurs' 
        AND column_name = 'niveau_kyc'
        AND data_type = 'integer'
    ) THEN
        EXECUTE 'UPDATE identite.utilisateurs SET niveau_kyc_old = niveau_kyc';
        RAISE NOTICE '✓ Valeurs niveau_kyc sauvegardées';
    END IF;
    
    -- Sauvegarder statut si c'est un VARCHAR
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'identite' 
        AND table_name = 'utilisateurs' 
        AND column_name = 'statut'
        AND data_type = 'character varying'
    ) THEN
        EXECUTE 'UPDATE identite.utilisateurs SET statut_old = statut';
        RAISE NOTICE '✓ Valeurs statut sauvegardées';
    END IF;
END $$;

\echo ''

-- =============================================================================
-- ÉTAPE 3: Supprimer les anciennes colonnes (si elles existent)
-- =============================================================================

\echo 'Suppression des anciennes colonnes...'

-- Supprimer les anciennes colonnes si elles existent
ALTER TABLE identite.utilisateurs 
DROP COLUMN IF EXISTS type_utilisateur CASCADE,
DROP COLUMN IF EXISTS niveau_kyc CASCADE,
DROP COLUMN IF EXISTS statut CASCADE;

\echo '✓ Anciennes colonnes supprimées'
\echo ''

-- =============================================================================
-- ÉTAPE 4: Ajouter les nouvelles colonnes avec Foreign Keys
-- =============================================================================

\echo 'Ajout des nouvelles colonnes avec Foreign Keys...'

-- Ajouter type_utilisateur (Foreign Key vers types_utilisateurs)
ALTER TABLE identite.utilisateurs 
ADD COLUMN IF NOT EXISTS type_utilisateur VARCHAR(20) 
REFERENCES identite.types_utilisateurs(code) ON DELETE RESTRICT;

-- Ajouter niveau_kyc (Foreign Key vers niveaux_kyc)
ALTER TABLE identite.utilisateurs 
ADD COLUMN IF NOT EXISTS niveau_kyc INTEGER 
REFERENCES identite.niveaux_kyc(niveau) ON DELETE RESTRICT;

-- Ajouter statut (Foreign Key vers statuts_utilisateurs)
ALTER TABLE identite.utilisateurs 
ADD COLUMN IF NOT EXISTS statut VARCHAR(20) 
REFERENCES identite.statuts_utilisateurs(code) ON DELETE RESTRICT;

\echo '✓ Nouvelles colonnes ajoutées avec Foreign Keys'
\echo ''

-- =============================================================================
-- ÉTAPE 5: Restaurer les valeurs depuis les colonnes temporaires
-- =============================================================================

\echo 'Restauration des valeurs...'

-- Restaurer les valeurs sauvegardées
UPDATE identite.utilisateurs 
SET 
    type_utilisateur = COALESCE(type_utilisateur_old, 'CLIENT'),
    niveau_kyc = COALESCE(niveau_kyc_old, 0),
    statut = COALESCE(statut_old, 'ACTIF')
WHERE type_utilisateur IS NULL OR niveau_kyc IS NULL OR statut IS NULL;

\echo '✓ Valeurs restaurées'
\echo ''

-- =============================================================================
-- ÉTAPE 6: Définir les valeurs par défaut
-- =============================================================================

\echo 'Configuration des valeurs par défaut...'

-- Définir les valeurs par défaut
ALTER TABLE identite.utilisateurs 
ALTER COLUMN type_utilisateur SET DEFAULT 'CLIENT',
ALTER COLUMN niveau_kyc SET DEFAULT 0,
ALTER COLUMN statut SET DEFAULT 'ACTIF';

-- Rendre les colonnes NOT NULL
ALTER TABLE identite.utilisateurs 
ALTER COLUMN type_utilisateur SET NOT NULL,
ALTER COLUMN niveau_kyc SET NOT NULL,
ALTER COLUMN statut SET NOT NULL;

\echo '✓ Valeurs par défaut configurées'
\echo ''

-- =============================================================================
-- ÉTAPE 7: Créer les index pour améliorer les performances
-- =============================================================================

\echo 'Création des index...'

CREATE INDEX IF NOT EXISTS idx_utilisateurs_type 
ON identite.utilisateurs(type_utilisateur);

CREATE INDEX IF NOT EXISTS idx_utilisateurs_niveau_kyc 
ON identite.utilisateurs(niveau_kyc);

CREATE INDEX IF NOT EXISTS idx_utilisateurs_statut 
ON identite.utilisateurs(statut);

\echo '✓ Index créés'
\echo ''

-- =============================================================================
-- ÉTAPE 8: Nettoyer les colonnes temporaires
-- =============================================================================

\echo 'Nettoyage des colonnes temporaires...'

ALTER TABLE identite.utilisateurs 
DROP COLUMN IF EXISTS type_utilisateur_old,
DROP COLUMN IF EXISTS niveau_kyc_old,
DROP COLUMN IF EXISTS statut_old;

\echo '✓ Colonnes temporaires supprimées'
\echo ''

-- =============================================================================
-- ÉTAPE 9: Ajouter des commentaires
-- =============================================================================

\echo 'Ajout de la documentation...'

COMMENT ON COLUMN identite.utilisateurs.type_utilisateur 
IS 'Type d''utilisateur (FK vers types_utilisateurs)';

COMMENT ON COLUMN identite.utilisateurs.niveau_kyc 
IS 'Niveau de vérification KYC (FK vers niveaux_kyc)';

COMMENT ON COLUMN identite.utilisateurs.statut 
IS 'Statut du compte (FK vers statuts_utilisateurs)';

\echo '✓ Documentation ajoutée'
\echo ''

-- =============================================================================
-- ÉTAPE 10: Vérification finale
-- =============================================================================

\echo '========================================='
\echo 'VÉRIFICATION FINALE'
\echo '========================================='
\echo ''

-- Vérifier la structure des colonnes
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'identite'
  AND table_name = 'utilisateurs'
  AND column_name IN ('type_utilisateur', 'niveau_kyc', 'statut')
ORDER BY column_name;

\echo ''

-- Vérifier les Foreign Keys
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'identite'
  AND tc.table_name = 'utilisateurs'
  AND kcu.column_name IN ('type_utilisateur', 'niveau_kyc', 'statut');

\echo ''

-- Compter les utilisateurs par type, niveau et statut
\echo 'Statistiques des utilisateurs:'
\echo ''

SELECT 
    'Par type' as categorie,
    tu.libelle as valeur,
    COUNT(u.id) as nombre
FROM identite.types_utilisateurs tu
LEFT JOIN identite.utilisateurs u ON u.type_utilisateur = tu.code
GROUP BY tu.code, tu.libelle
UNION ALL
SELECT 
    'Par niveau KYC' as categorie,
    nk.libelle as valeur,
    COUNT(u.id) as nombre
FROM identite.niveaux_kyc nk
LEFT JOIN identite.utilisateurs u ON u.niveau_kyc = nk.niveau
GROUP BY nk.niveau, nk.libelle
UNION ALL
SELECT 
    'Par statut' as categorie,
    su.libelle as valeur,
    COUNT(u.id) as nombre
FROM identite.statuts_utilisateurs su
LEFT JOIN identite.utilisateurs u ON u.statut = su.code
GROUP BY su.code, su.libelle
ORDER BY categorie, valeur;

\echo ''
\echo '========================================='
\echo '✓ MODIFICATION TERMINÉE AVEC SUCCÈS!'
\echo '========================================='
\echo ''
\echo 'La table utilisateurs utilise maintenant les tables de référence.'
\echo 'Vous pouvez redémarrer Django.'
\echo ''
\echo '========================================='
