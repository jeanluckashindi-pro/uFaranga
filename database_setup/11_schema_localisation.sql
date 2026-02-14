-- =====================================================
-- SCRIPT 11: SCHÉMA LOCALISATION
-- Hiérarchie géographique avec coordonnées et autorisation système
-- Pays → Province/Région → District/Ville → Quartier/Zone → Point de service/Agent
-- Liaison à identite.utilisateurs pour localiser une personne
-- =====================================================

\c ufaranga

-- =====================================================
-- PAYS
-- =====================================================
CREATE TABLE localisation.pays (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code_iso_2 CHAR(2) UNIQUE NOT NULL,
    code_iso_3 CHAR(3),
    nom VARCHAR(100) NOT NULL,
    nom_anglais VARCHAR(100),
    -- Coordonnées du centre (pour affichage carte)
    latitude_centre DECIMAL(10, 7),
    longitude_centre DECIMAL(10, 7),
    -- La zone (pays) est-elle autorisée à utiliser le système ?
    autorise_systeme BOOLEAN DEFAULT TRUE,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    metadonnees JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_pays_code ON localisation.pays(code_iso_2);
CREATE INDEX idx_pays_autorise ON localisation.pays(autorise_systeme) WHERE autorise_systeme = TRUE;
COMMENT ON TABLE localisation.pays IS 'Pays - niveau 1 de la hiérarchie géographique';

-- =====================================================
-- PROVINCES / RÉGIONS (rattachées à un pays)
-- =====================================================
CREATE TABLE localisation.provinces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pays_id UUID NOT NULL REFERENCES localisation.pays(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    latitude_centre DECIMAL(10, 7),
    longitude_centre DECIMAL(10, 7),
    autorise_systeme BOOLEAN DEFAULT TRUE,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    metadonnees JSONB DEFAULT '{}'::jsonb,
    UNIQUE(pays_id, code)
);

CREATE INDEX idx_provinces_pays ON localisation.provinces(pays_id);
CREATE INDEX idx_provinces_autorise ON localisation.provinces(autorise_systeme) WHERE autorise_systeme = TRUE;
COMMENT ON TABLE localisation.provinces IS 'Régions / Provinces - niveau 2';

-- =====================================================
-- DISTRICTS / VILLES (rattachés à une province)
-- =====================================================
CREATE TABLE localisation.districts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    province_id UUID NOT NULL REFERENCES localisation.provinces(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    latitude_centre DECIMAL(10, 7),
    longitude_centre DECIMAL(10, 7),
    autorise_systeme BOOLEAN DEFAULT TRUE,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    metadonnees JSONB DEFAULT '{}'::jsonb,
    UNIQUE(province_id, code)
);

CREATE INDEX idx_districts_province ON localisation.districts(province_id);
CREATE INDEX idx_districts_autorise ON localisation.districts(autorise_systeme) WHERE autorise_systeme = TRUE;
COMMENT ON TABLE localisation.districts IS 'Villes / Districts - niveau 3';

-- =====================================================
-- QUARTIERS / ZONES (rattachés à un district)
-- =====================================================
CREATE TABLE localisation.quartiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id UUID NOT NULL REFERENCES localisation.districts(id) ON DELETE CASCADE,
    code VARCHAR(20) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    latitude_centre DECIMAL(10, 7),
    longitude_centre DECIMAL(10, 7),
    -- La zone est-elle autorisée à utiliser le système ?
    autorise_systeme BOOLEAN DEFAULT TRUE,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    metadonnees JSONB DEFAULT '{}'::jsonb,
    UNIQUE(district_id, code)
);

CREATE INDEX idx_quartiers_district ON localisation.quartiers(district_id);
CREATE INDEX idx_quartiers_autorise ON localisation.quartiers(autorise_systeme) WHERE autorise_systeme = TRUE;
COMMENT ON TABLE localisation.quartiers IS 'Quartiers / Zones - niveau 4';

-- =====================================================
-- POINTS DE SERVICE / AGENTS (rattachés à un quartier, optionnellement à un agent)
-- =====================================================
CREATE TABLE localisation.points_de_service (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    quartier_id UUID NOT NULL REFERENCES localisation.quartiers(id) ON DELETE CASCADE,
    code VARCHAR(30) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    type_point VARCHAR(20) DEFAULT 'AGENT' CHECK (type_point IN ('AGENT', 'GUICHET', 'PARTENAIRE', 'AUTRE')),
    -- Agent (personne identite) rattachée à ce point
    agent_utilisateur_id UUID REFERENCES identite.utilisateurs(id) ON DELETE SET NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    adresse_complementaire TEXT,
    autorise_systeme BOOLEAN DEFAULT TRUE,
    est_actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    metadonnees JSONB DEFAULT '{}'::jsonb,
    UNIQUE(quartier_id, code)
);

CREATE INDEX idx_points_de_service_quartier ON localisation.points_de_service(quartier_id);
CREATE INDEX idx_points_de_service_agent ON localisation.points_de_service(agent_utilisateur_id);
CREATE INDEX idx_points_de_service_autorise ON localisation.points_de_service(autorise_systeme) WHERE autorise_systeme = TRUE;
COMMENT ON TABLE localisation.points_de_service IS 'Points de service / Agents - niveau 5, relié à un utilisateur (agent)';

-- =====================================================
-- LIAISON IDENTITÉ → LOCALISATION (adresse de la personne)
-- Colonnes ajoutées à identite.utilisateurs pour marquer la localisation
-- =====================================================
ALTER TABLE identite.utilisateurs
    ADD COLUMN IF NOT EXISTS pays_id UUID REFERENCES localisation.pays(id) ON DELETE SET NULL;
ALTER TABLE identite.utilisateurs
    ADD COLUMN IF NOT EXISTS province_id UUID REFERENCES localisation.provinces(id) ON DELETE SET NULL;
ALTER TABLE identite.utilisateurs
    ADD COLUMN IF NOT EXISTS district_id UUID REFERENCES localisation.districts(id) ON DELETE SET NULL;
ALTER TABLE identite.utilisateurs
    ADD COLUMN IF NOT EXISTS quartier_id UUID REFERENCES localisation.quartiers(id) ON DELETE SET NULL;
ALTER TABLE identite.utilisateurs
    ADD COLUMN IF NOT EXISTS point_de_service_id UUID REFERENCES localisation.points_de_service(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_utilisateurs_pays ON identite.utilisateurs(pays_id);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_province ON identite.utilisateurs(province_id);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_district ON identite.utilisateurs(district_id);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_quartier ON identite.utilisateurs(quartier_id);
CREATE INDEX IF NOT EXISTS idx_utilisateurs_point_de_service ON identite.utilisateurs(point_de_service_id);

COMMENT ON COLUMN identite.utilisateurs.pays_id IS 'Référence localisation : pays de résidence';
COMMENT ON COLUMN identite.utilisateurs.province_id IS 'Référence localisation : province / région';
COMMENT ON COLUMN identite.utilisateurs.district_id IS 'Référence localisation : district / ville';
COMMENT ON COLUMN identite.utilisateurs.quartier_id IS 'Référence localisation : quartier / zone';
COMMENT ON COLUMN identite.utilisateurs.point_de_service_id IS 'Référence localisation : point de service (ex. agent d’attachement)';

-- =====================================================
-- DROITS pour l'utilisateur Django (ufaranga)
-- =====================================================
GRANT USAGE ON SCHEMA localisation TO ufaranga;
GRANT SELECT, INSERT, UPDATE, DELETE ON localisation.pays TO ufaranga;
GRANT SELECT, INSERT, UPDATE, DELETE ON localisation.provinces TO ufaranga;
GRANT SELECT, INSERT, UPDATE, DELETE ON localisation.districts TO ufaranga;
GRANT SELECT, INSERT, UPDATE, DELETE ON localisation.quartiers TO ufaranga;
GRANT SELECT, INSERT, UPDATE, DELETE ON localisation.points_de_service TO ufaranga;
