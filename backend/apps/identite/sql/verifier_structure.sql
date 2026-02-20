-- =============================================================================
-- Script de VÉRIFICATION de la structure de la table utilisateurs
-- =============================================================================
-- Vérifie que la table utilisateurs est bien reliée aux tables de référence
-- =============================================================================

SET search_path TO identite, public;

\echo '========================================='
\echo 'VÉRIFICATION DE LA STRUCTURE'
\echo '========================================='
\echo ''

-- =============================================================================
-- 1. VÉRIFIER L'EXISTENCE DES TABLES
-- =============================================================================

\echo '1. Vérification de l''existence des tables...'
\echo ''

SELECT 
    table_name,
    CASE 
        WHEN table_name IN (
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'identite'
        ) THEN '✓ Existe'
        ELSE '✗ N''existe pas'
    END as statut
FROM (
    VALUES 
        ('utilisateurs'),
        ('types_utilisateurs'),
        ('niveaux_kyc'),
        ('statuts_utilisateurs')
) AS t(table_name);

\echo ''

-- =============================================================================
-- 2. VÉRIFIER LES COLONNES DE LA TABLE UTILISATEURS
-- =============================================================================

\echo '2. Vérification des colonnes de la table utilisateurs...'
\echo ''

SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    CASE 
        WHEN column_name IN ('type_utilisateur', 'niveau_kyc', 'statut') 
        THEN '⭐ Colonne de référence'
        ELSE ''
    END as note
FROM information_schema.columns
WHERE table_schema = 'identite'
  AND table_name = 'utilisateurs'
  AND column_name IN ('type_utilisateur', 'niveau_kyc', 'statut')
ORDER BY 
    CASE column_name
        WHEN 'type_utilisateur' THEN 1
        WHEN 'niveau_kyc' THEN 2
        WHEN 'statut' THEN 3
    END;

\echo ''

-- =============================================================================
-- 3. VÉRIFIER LES FOREIGN KEYS (RELATIONS)
-- =============================================================================

\echo '3. Vérification des Foreign Keys (relations)...'
\echo ''

SELECT
    tc.constraint_name as "Nom Contrainte",
    kcu.column_name as "Colonne Source",
    ccu.table_name as "Table Cible",
    ccu.column_name as "Colonne Cible",
    '✓ Relation active' as "Statut"
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
  AND kcu.column_name IN ('type_utilisateur', 'niveau_kyc', 'statut')
ORDER BY kcu.column_name;

\echo ''

-- =============================================================================
-- 4. VÉRIFIER LES INDEX
-- =============================================================================

\echo '4. Vérification des index...'
\echo ''

SELECT
    indexname as "Nom Index",
    indexdef as "Définition"
FROM pg_indexes
WHERE schemaname = 'identite'
  AND tablename = 'utilisateurs'
  AND indexname IN (
      'idx_utilisateurs_type',
      'idx_utilisateurs_niveau_kyc',
      'idx_utilisateurs_statut'
  )
ORDER BY indexname;

\echo ''

-- =============================================================================
-- 5. COMPTER LES DONNÉES DANS LES TABLES DE RÉFÉRENCE
-- =============================================================================

\echo '5. Vérification des données dans les tables de référence...'
\echo ''

SELECT 
    'types_utilisateurs' as "Table",
    COUNT(*) as "Nombre d''enregistrements",
    CASE 
        WHEN COUNT(*) = 6 THEN '✓ OK (6 attendus)'
        ELSE '✗ Problème (6 attendus)'
    END as "Statut"
FROM identite.types_utilisateurs
UNION ALL
SELECT 
    'niveaux_kyc' as "Table",
    COUNT(*) as "Nombre d''enregistrements",
    CASE 
        WHEN COUNT(*) = 4 THEN '✓ OK (4 attendus)'
        ELSE '✗ Problème (4 attendus)'
    END as "Statut"
FROM identite.niveaux_kyc
UNION ALL
SELECT 
    'statuts_utilisateurs' as "Table",
    COUNT(*) as "Nombre d''enregistrements",
    CASE 
        WHEN COUNT(*) = 5 THEN '✓ OK (5 attendus)'
        ELSE '✗ Problème (5 attendus)'
    END as "Statut"
FROM identite.statuts_utilisateurs;

\echo ''

-- =============================================================================
-- 6. VÉRIFIER LES VALEURS DANS LA TABLE UTILISATEURS
-- =============================================================================

\echo '6. Vérification des valeurs dans la table utilisateurs...'
\echo ''

-- Compter les utilisateurs par type
SELECT 
    'Par type' as "Catégorie",
    tu.code as "Code",
    tu.libelle as "Libellé",
    COUNT(u.id) as "Nombre Utilisateurs"
FROM identite.types_utilisateurs tu
LEFT JOIN identite.utilisateurs u ON u.type_utilisateur = tu.code
GROUP BY tu.code, tu.libelle
ORDER BY tu.ordre_affichage;

\echo ''

-- Compter les utilisateurs par niveau KYC
SELECT 
    'Par niveau KYC' as "Catégorie",
    nk.niveau as "Niveau",
    nk.libelle as "Libellé",
    COUNT(u.id) as "Nombre Utilisateurs"
FROM identite.niveaux_kyc nk
LEFT JOIN identite.utilisateurs u ON u.niveau_kyc = nk.niveau
GROUP BY nk.niveau, nk.libelle
ORDER BY nk.niveau;

\echo ''

-- Compter les utilisateurs par statut
SELECT 
    'Par statut' as "Catégorie",
    su.code as "Code",
    su.libelle as "Libellé",
    COUNT(u.id) as "Nombre Utilisateurs"
FROM identite.statuts_utilisateurs su
LEFT JOIN identite.utilisateurs u ON u.statut = su.code
GROUP BY su.code, su.libelle
ORDER BY su.ordre_affichage;

\echo ''

-- =============================================================================
-- 7. TESTER LES RELATIONS (JOINTURES)
-- =============================================================================

\echo '7. Test des jointures (5 premiers utilisateurs)...'
\echo ''

SELECT 
    u.id,
    u.courriel,
    u.prenom,
    u.nom_famille,
    tu.libelle as "Type",
    nk.libelle as "Niveau KYC",
    su.libelle as "Statut",
    su.couleur as "Couleur Statut"
FROM identite.utilisateurs u
LEFT JOIN identite.types_utilisateurs tu ON u.type_utilisateur = tu.code
LEFT JOIN identite.niveaux_kyc nk ON u.niveau_kyc = nk.niveau
LEFT JOIN identite.statuts_utilisateurs su ON u.statut = su.code
LIMIT 5;

\echo ''

-- =============================================================================
-- 8. VÉRIFIER LES VALEURS INVALIDES
-- =============================================================================

\echo '8. Vérification des valeurs invalides...'
\echo ''

-- Utilisateurs avec type_utilisateur invalide
SELECT 
    'Types invalides' as "Problème",
    COUNT(*) as "Nombre",
    CASE 
        WHEN COUNT(*) = 0 THEN '✓ Aucun problème'
        ELSE '✗ Valeurs invalides trouvées'
    END as "Statut"
FROM identite.utilisateurs u
WHERE u.type_utilisateur NOT IN (SELECT code FROM identite.types_utilisateurs);

-- Utilisateurs avec niveau_kyc invalide
SELECT 
    'Niveaux KYC invalides' as "Problème",
    COUNT(*) as "Nombre",
    CASE 
        WHEN COUNT(*) = 0 THEN '✓ Aucun problème'
        ELSE '✗ Valeurs invalides trouvées'
    END as "Statut"
FROM identite.utilisateurs u
WHERE u.niveau_kyc NOT IN (SELECT niveau FROM identite.niveaux_kyc);

-- Utilisateurs avec statut invalide
SELECT 
    'Statuts invalides' as "Problème",
    COUNT(*) as "Nombre",
    CASE 
        WHEN COUNT(*) = 0 THEN '✓ Aucun problème'
        ELSE '✗ Valeurs invalides trouvées'
    END as "Statut"
FROM identite.utilisateurs u
WHERE u.statut NOT IN (SELECT code FROM identite.statuts_utilisateurs);

\echo ''

-- =============================================================================
-- 9. RÉSUMÉ FINAL
-- =============================================================================

\echo '========================================='
\echo 'RÉSUMÉ DE LA VÉRIFICATION'
\echo '========================================='
\echo ''

DO $$
DECLARE
    nb_fk INTEGER;
    nb_index INTEGER;
    nb_types INTEGER;
    nb_niveaux INTEGER;
    nb_statuts INTEGER;
    nb_utilisateurs INTEGER;
BEGIN
    -- Compter les Foreign Keys
    SELECT COUNT(*) INTO nb_fk
    FROM information_schema.table_constraints
    WHERE constraint_type = 'FOREIGN KEY'
      AND table_schema = 'identite'
      AND table_name = 'utilisateurs'
      AND constraint_name LIKE '%type_utilisateur%'
         OR constraint_name LIKE '%niveau_kyc%'
         OR constraint_name LIKE '%statut%';
    
    -- Compter les index
    SELECT COUNT(*) INTO nb_index
    FROM pg_indexes
    WHERE schemaname = 'identite'
      AND tablename = 'utilisateurs'
      AND indexname IN (
          'idx_utilisateurs_type',
          'idx_utilisateurs_niveau_kyc',
          'idx_utilisateurs_statut'
      );
    
    -- Compter les données
    SELECT COUNT(*) INTO nb_types FROM identite.types_utilisateurs;
    SELECT COUNT(*) INTO nb_niveaux FROM identite.niveaux_kyc;
    SELECT COUNT(*) INTO nb_statuts FROM identite.statuts_utilisateurs;
    SELECT COUNT(*) INTO nb_utilisateurs FROM identite.utilisateurs;
    
    RAISE NOTICE '📊 STATISTIQUES:';
    RAISE NOTICE '  • Foreign Keys: % (3 attendues)', nb_fk;
    RAISE NOTICE '  • Index: % (3 attendus)', nb_index;
    RAISE NOTICE '  • Types utilisateurs: % (6 attendus)', nb_types;
    RAISE NOTICE '  • Niveaux KYC: % (4 attendus)', nb_niveaux;
    RAISE NOTICE '  • Statuts: % (5 attendus)', nb_statuts;
    RAISE NOTICE '  • Utilisateurs: %', nb_utilisateurs;
    RAISE NOTICE '';
    
    IF nb_fk >= 3 AND nb_index >= 3 AND nb_types = 6 AND nb_niveaux = 4 AND nb_statuts = 5 THEN
        RAISE NOTICE '✓ STRUCTURE CORRECTE!';
        RAISE NOTICE '  La table utilisateurs est bien reliée aux tables de référence.';
    ELSE
        RAISE NOTICE '✗ PROBLÈME DÉTECTÉ!';
        IF nb_fk < 3 THEN
            RAISE NOTICE '  → Foreign Keys manquantes (% trouvées, 3 attendues)', nb_fk;
        END IF;
        IF nb_index < 3 THEN
            RAISE NOTICE '  → Index manquants (% trouvés, 3 attendus)', nb_index;
        END IF;
        IF nb_types != 6 THEN
            RAISE NOTICE '  → Types utilisateurs incorrects (% trouvés, 6 attendus)', nb_types;
        END IF;
        IF nb_niveaux != 4 THEN
            RAISE NOTICE '  → Niveaux KYC incorrects (% trouvés, 4 attendus)', nb_niveaux;
        END IF;
        IF nb_statuts != 5 THEN
            RAISE NOTICE '  → Statuts incorrects (% trouvés, 5 attendus)', nb_statuts;
        END IF;
    END IF;
END $$;

\echo ''
\echo '========================================='
\echo 'FIN DE LA VÉRIFICATION'
\echo '========================================='
