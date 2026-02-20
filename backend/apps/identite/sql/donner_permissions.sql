-- =============================================================================
-- DONNER LES PERMISSIONS À L'UTILISATEUR ufaranga
-- =============================================================================
-- À exécuter en tant que postgres (superuser)
-- =============================================================================

-- Donner tous les droits sur le schéma
GRANT ALL PRIVILEGES ON SCHEMA identite TO ufaranga;

-- Donner tous les droits sur toutes les tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA identite TO ufaranga;

-- Donner tous les droits sur toutes les séquences
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA identite TO ufaranga;

-- Donner les droits par défaut pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA identite GRANT ALL ON TABLES TO ufaranga;
ALTER DEFAULT PRIVILEGES IN SCHEMA identite GRANT ALL ON SEQUENCES TO ufaranga;

-- Rendre ufaranga propriétaire de la table utilisateurs
ALTER TABLE identite.utilisateurs OWNER TO ufaranga;
ALTER TABLE identite.types_utilisateurs OWNER TO ufaranga;
ALTER TABLE identite.niveaux_kyc OWNER TO ufaranga;
ALTER TABLE identite.statuts_utilisateurs OWNER TO ufaranga;

SELECT 'OK - Permissions donnees!' as resultat;
