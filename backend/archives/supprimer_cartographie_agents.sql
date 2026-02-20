-- Supprimer la table CartographieAgents
-- Connexion: psql -U postgres -d ufaranga -f supprimer_cartographie_agents.sql

BEGIN;

DROP TABLE IF EXISTS localisation.cartographie_agents CASCADE;

COMMIT;

-- Vérifier la suppression
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'localisation' 
AND table_name = 'cartographie_agents';
