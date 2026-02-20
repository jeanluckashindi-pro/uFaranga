-- =============================================================================
-- FIX RAPIDE - Ajouter Foreign Keys (< 3 secondes)
-- =============================================================================

SET search_path TO identite, public;

-- Supprimer les contraintes si elles existent
ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_type_utilisateur_fkey CASCADE;
ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_niveau_kyc_fkey CASCADE;
ALTER TABLE identite.utilisateurs DROP CONSTRAINT IF EXISTS utilisateurs_statut_fkey CASCADE;

-- Ajouter les Foreign Keys
ALTER TABLE identite.utilisateurs ADD CONSTRAINT utilisateurs_type_utilisateur_fkey FOREIGN KEY (type_utilisateur) REFERENCES identite.types_utilisateurs(code);
ALTER TABLE identite.utilisateurs ADD CONSTRAINT utilisateurs_niveau_kyc_fkey FOREIGN KEY (niveau_kyc) REFERENCES identite.niveaux_kyc(niveau);
ALTER TABLE identite.utilisateurs ADD CONSTRAINT utilisateurs_statut_fkey FOREIGN KEY (statut) REFERENCES identite.statuts_utilisateurs(code);

-- Créer les index
CREATE INDEX IF NOT EXISTS idx_utilisateurs_type ON identite.utilisateurs(type_utilisateur);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_niveau_kyc ON identite.utilisateurs(niveau_kyc);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_statut ON identite.utilisateurs(statut);

SELECT 'OK - Foreign Keys ajoutees!' as resultat;
