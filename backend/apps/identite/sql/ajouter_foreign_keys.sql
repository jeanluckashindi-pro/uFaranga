-- =============================================================================
-- AJOUTER LES FOREIGN KEYS - Version Ultra-Rapide
-- =============================================================================
-- Ajoute uniquement les Foreign Keys sans vérifications complexes
-- Temps: < 5 secondes
-- =============================================================================

SET search_path TO identite, public;

\echo 'Ajout des Foreign Keys...'

-- Supprimer les Foreign Keys si elles existent déjà (pour éviter les erreurs)
ALTER TABLE identite.utilisateurs 
DROP CONSTRAINT IF EXISTS utilisateurs_type_utilisateur_fkey,
DROP CONSTRAINT IF EXISTS utilisateurs_niveau_kyc_fkey,
DROP CONSTRAINT IF EXISTS utilisateurs_statut_fkey;

-- Ajouter les Foreign Keys
ALTER TABLE identite.utilisateurs 
ADD CONSTRAINT utilisateurs_type_utilisateur_fkey 
    FOREIGN KEY (type_utilisateur) 
    REFERENCES identite.types_utilisateurs(code) 
    ON DELETE RESTRICT;

ALTER TABLE identite.utilisateurs 
ADD CONSTRAINT utilisateurs_niveau_kyc_fkey 
    FOREIGN KEY (niveau_kyc) 
    REFERENCES identite.niveaux_kyc(niveau) 
    ON DELETE RESTRICT;

ALTER TABLE identite.utilisateurs 
ADD CONSTRAINT utilisateurs_statut_fkey 
    FOREIGN KEY (statut) 
    REFERENCES identite.statuts_utilisateurs(code) 
    ON DELETE RESTRICT;

\echo '✓ Foreign Keys ajoutées!'

-- Vérification rapide
SELECT 
    COUNT(*) as "Nombre de Foreign Keys (3 attendues)"
FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY'
  AND table_schema = 'identite'
  AND table_name = 'utilisateurs'
  AND constraint_name LIKE 'utilisateurs_%_fkey';
