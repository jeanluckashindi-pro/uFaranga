-- Migration du schéma localisation vers PostGIS
-- Remplace les colonnes latitude/longitude et GeoJSON par des types geometry natifs

-- ============================================================================
-- 1. PAYS - Ajouter colonnes PostGIS
-- ============================================================================

-- Ajouter colonne geometry pour le centre du pays (POINT)
ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326);

-- Ajouter colonne geometry pour les frontières (POLYGON/MULTIPOLYGON)
ALTER TABLE localisation.pays 
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

-- Migrer les données existantes
UPDATE localisation.pays 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

-- Migrer GeoJSON vers geometry (si présent) - ignorer les erreurs
-- UPDATE localisation.pays 
-- SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
-- WHERE geometrie_geojson IS NOT NULL;

-- Créer index spatiaux
CREATE INDEX IF NOT EXISTS idx_pays_centre_geo ON localisation.pays USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_pays_geometrie ON localisation.pays USING GIST (geometrie);

-- ============================================================================
-- 2. PROVINCES - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.provinces 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.provinces 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.provinces 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_provinces_centre_geo ON localisation.provinces USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_provinces_geometrie ON localisation.provinces USING GIST (geometrie);

-- ============================================================================
-- 3. DISTRICTS - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.districts 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.districts 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.districts 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_districts_centre_geo ON localisation.districts USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_districts_geometrie ON localisation.districts USING GIST (geometrie);

-- ============================================================================
-- 4. COMMUNES - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.communes 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.communes 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.communes 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_communes_centre_geo ON localisation.communes USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_communes_geometrie ON localisation.communes USING GIST (geometrie);

-- ============================================================================
-- 5. QUARTIERS - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.quartiers 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.quartiers 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.quartiers 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_quartiers_centre_geo ON localisation.quartiers USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_quartiers_geometrie ON localisation.quartiers USING GIST (geometrie);

-- ============================================================================
-- 6. COLLINES - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.collines 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.collines 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.collines 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_collines_centre_geo ON localisation.collines USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_collines_geometrie ON localisation.collines USING GIST (geometrie);

-- ============================================================================
-- 7. SECTEURS - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.secteurs 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.secteurs 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.secteurs 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_secteurs_centre_geo ON localisation.secteurs USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_secteurs_geometrie ON localisation.secteurs USING GIST (geometrie);

-- ============================================================================
-- 8. ZONES - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.zones 
ADD COLUMN IF NOT EXISTS centre_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.zones 
SET centre_geo = ST_SetSRID(ST_MakePoint(centre_longitude, centre_latitude), 4326)
WHERE centre_longitude IS NOT NULL AND centre_latitude IS NOT NULL;

UPDATE localisation.zones 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_zones_centre_geo ON localisation.zones USING GIST (centre_geo);
CREATE INDEX IF NOT EXISTS idx_zones_geometrie ON localisation.zones USING GIST (geometrie);

-- ============================================================================
-- 9. POINTS DE SERVICE - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.points_de_service 
ADD COLUMN IF NOT EXISTS position_geo geometry(Point, 4326),
ADD COLUMN IF NOT EXISTS zone_couverture geometry(Polygon, 4326);

-- Migrer position
UPDATE localisation.points_de_service 
SET position_geo = ST_SetSRID(ST_MakePoint(longitude, latitude, altitude_m), 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;

-- Migrer zone de couverture (buffer circulaire si rayon défini)
UPDATE localisation.points_de_service 
SET zone_couverture = ST_Buffer(position_geo::geography, rayon_couverture_km * 1000)::geometry
WHERE position_geo IS NOT NULL AND rayon_couverture_km IS NOT NULL;

-- Ou depuis GeoJSON si présent
UPDATE localisation.points_de_service 
SET zone_couverture = ST_GeomFromGeoJSON(zone_couverture_geojson::text)
WHERE zone_couverture_geojson IS NOT NULL AND zone_couverture IS NULL;

CREATE INDEX IF NOT EXISTS idx_points_service_position ON localisation.points_de_service USING GIST (position_geo);
CREATE INDEX IF NOT EXISTS idx_points_service_zone ON localisation.points_de_service USING GIST (zone_couverture);

-- ============================================================================
-- 10. ZONES DE RISQUE - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.zones_risque 
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.zones_risque 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_zones_risque_geometrie ON localisation.zones_risque USING GIST (geometrie);

-- ============================================================================
-- 11. RESTRICTIONS GÉOGRAPHIQUES - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.restrictions_geographiques 
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiPolygon, 4326);

UPDATE localisation.restrictions_geographiques 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_restrictions_geo_geometrie ON localisation.restrictions_geographiques USING GIST (geometrie);

-- ============================================================================
-- 12. CORRIDORS DE PAIEMENT - Ajouter colonnes PostGIS
-- ============================================================================

ALTER TABLE localisation.corridors_paiement 
ADD COLUMN IF NOT EXISTS geometrie geometry(MultiLineString, 4326);

UPDATE localisation.corridors_paiement 
SET geometrie = ST_Multi(ST_GeomFromGeoJSON(geometrie_geojson::text)::geometry(LineString, 4326))
WHERE geometrie_geojson IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_corridors_geometrie ON localisation.corridors_paiement USING GIST (geometrie);

-- ============================================================================
-- VÉRIFICATION
-- ============================================================================

SELECT 'Migration PostGIS terminée!' as message;

SELECT 
    'pays' as table_name,
    COUNT(*) as total,
    COUNT(centre_geo) as avec_centre,
    COUNT(geometrie) as avec_geometrie
FROM localisation.pays
UNION ALL
SELECT 
    'provinces',
    COUNT(*),
    COUNT(centre_geo),
    COUNT(geometrie)
FROM localisation.provinces
UNION ALL
SELECT 
    'points_de_service',
    COUNT(*),
    COUNT(position_geo),
    COUNT(zone_couverture)
FROM localisation.points_de_service;
