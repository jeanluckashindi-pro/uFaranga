-- Script pour ajouter les colonnes en tant que postgres
-- Connexion: psql -U postgres -d ufaranga -f ajouter_colonnes_postgres.sql

BEGIN;

-- Ajouter les colonnes
ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS continent VARCHAR(50);

ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS sous_region VARCHAR(100);

-- Créer les index
CREATE INDEX IF NOT EXISTS idx_pays_continent ON localisation.pays(continent);
CREATE INDEX IF NOT EXISTS idx_pays_sous_region ON localisation.pays(sous_region);

-- Donner les droits à ufaranga
GRANT ALL PRIVILEGES ON localisation.pays TO ufaranga;

COMMIT;

-- Vérifier
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'localisation' 
AND table_name = 'pays'
AND column_name IN ('continent', 'sous_region');
