-- =============================================================================
-- VÉRIFICATION RAPIDE - Structure Table Utilisateurs
-- =============================================================================
-- Version simplifiée et rapide (< 5 secondes)
-- =============================================================================

SET search_path TO identite, public;

\echo '========================================='
\echo 'VÉRIFICATION RAPIDE'
\echo '========================================='
\echo ''

-- 1. Tables existent?
\echo '1. Tables:'
SELECT COUNT(*) as "Nombre de tables (4 attendues)"
FROM information_schema.tables 
WHERE table_schema = 'identite' 
  AND table_name IN ('utilisateurs', 'types_utilisateurs', 'niveaux_kyc', 'statuts_utilisateurs');

\echo ''

-- 2. Foreign Keys existent?
\echo '2. Foreign Keys (Relations):'
SELECT 
    kcu.column_name as "Colonne",
    ccu.table_name as "→ Table Cible"
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'identite'
  AND tc.table_name = 'utilisateurs'
  AND kcu.column_name IN ('type_utilisateur', 'niveau_kyc', 'statut');

\echo ''

-- 3. Données présentes?
\echo '3. Données:'
SELECT 
    (SELECT COUNT(*) FROM identite.types_utilisateurs) as "Types (6 attendus)",
    (SELECT COUNT(*) FROM identite.niveaux_kyc) as "Niveaux (4 attendus)",
    (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as "Statuts (5 attendus)",
    (SELECT COUNT(*) FROM identite.utilisateurs) as "Utilisateurs";

\echo ''

-- 4. Test jointure
\echo '4. Test Jointure (1 utilisateur):'
SELECT 
    u.courriel,
    tu.libelle as "Type",
    nk.libelle as "Niveau KYC",
    su.libelle as "Statut"
FROM identite.utilisateurs u
LEFT JOIN identite.types_utilisateurs tu ON u.type_utilisateur = tu.code
LEFT JOIN identite.niveaux_kyc nk ON u.niveau_kyc = nk.niveau
LEFT JOIN identite.statuts_utilisateurs su ON u.statut = su.code
LIMIT 1;

\echo ''
\echo '========================================='
\echo 'Si vous voyez des données ci-dessus:'
\echo '✓ La structure est CORRECTE'
\echo ''
\echo 'Si vous voyez des erreurs ou 0 résultats:'
\echo '✗ Exécuter: setup_complet_avec_alter.sql'
\echo '========================================='
