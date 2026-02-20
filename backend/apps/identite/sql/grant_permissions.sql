-- =============================================================================
-- Script SQL pour ACCORDER les permissions sur les tables de référence
-- =============================================================================
-- Ce script résout l'erreur: "permission denied for relation niveaux_kyc"
-- =============================================================================

-- Activer le schéma identite
SET search_path TO identite, public;

-- =============================================================================
-- ACCORDER LES PERMISSIONS SUR LES TABLES DE RÉFÉRENCE
-- =============================================================================

-- Remplacez 'votre_utilisateur_db' par le nom de votre utilisateur PostgreSQL
-- Pour trouver votre utilisateur, exécutez: SELECT current_user;

-- Permissions sur types_utilisateurs
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.types_utilisateurs TO PUBLIC;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA identite TO PUBLIC;

-- Permissions sur niveaux_kyc
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.niveaux_kyc TO PUBLIC;

-- Permissions sur statuts_utilisateurs
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.statuts_utilisateurs TO PUBLIC;

-- Permissions sur utilisateurs
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.utilisateurs TO PUBLIC;

-- Permissions sur profils_utilisateurs
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.profils_utilisateurs TO PUBLIC;

-- =============================================================================
-- ALTERNATIVE: Accorder les permissions à un utilisateur spécifique
-- =============================================================================
-- Décommentez et remplacez 'nom_utilisateur' par votre utilisateur DB

-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.types_utilisateurs TO nom_utilisateur;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.niveaux_kyc TO nom_utilisateur;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.statuts_utilisateurs TO nom_utilisateur;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.utilisateurs TO nom_utilisateur;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.profils_utilisateurs TO nom_utilisateur;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA identite TO nom_utilisateur;

-- =============================================================================
-- VÉRIFICATION DES PERMISSIONS
-- =============================================================================

-- Vérifier les permissions accordées
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'identite'
  AND table_name IN ('types_utilisateurs', 'niveaux_kyc', 'statuts_utilisateurs', 'utilisateurs', 'profils_utilisateurs')
ORDER BY table_name, grantee, privilege_type;

-- =============================================================================
-- FIN DU SCRIPT
-- =============================================================================

DO $$
BEGIN
    RAISE NOTICE '✓ Permissions accordées avec succès!';
    RAISE NOTICE '→ Vous pouvez maintenant vous connecter sans erreur de permission';
END $$;
