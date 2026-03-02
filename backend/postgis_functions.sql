-- Fonctions PostGIS utiles pour le schéma localisation

-- ============================================================================
-- 1. Trouver les pays voisins (dans un rayon de X km)
-- ============================================================================
CREATE OR REPLACE FUNCTION localisation.pays_voisins(
    p_pays_id UUID,
    p_rayon_km NUMERIC DEFAULT 1000
)
RETURNS TABLE (
    pays_id UUID,
    nom VARCHAR,
    distance_km NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p2.id,
        p2.nom,
        ROUND((ST_Distance(p1.centre_geo::geography, p2.centre_geo::geography) / 1000)::numeric, 2) as distance_km
    FROM localisation.pays p1
    CROSS JOIN localisation.pays p2
    WHERE p1.id = p_pays_id
      AND p2.id != p_pays_id
      AND p1.centre_geo IS NOT NULL
      AND p2.centre_geo IS NOT NULL
      AND ST_DWithin(p1.centre_geo::geography, p2.centre_geo::geography, p_rayon_km * 1000)
    ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 2. Trouver les provinces dans un rayon
-- ============================================================================
CREATE OR REPLACE FUNCTION localisation.provinces_dans_rayon(
    p_latitude NUMERIC,
    p_longitude NUMERIC,
    p_rayon_km NUMERIC DEFAULT 100
)
RETURNS TABLE (
    province_id UUID,
    nom VARCHAR,
    pays_nom VARCHAR,
    distance_km NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pr.id,
        pr.nom,
        pa.nom,
        ROUND((ST_Distance(
            ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography,
            pr.centre_geo::geography
        ) / 1000)::numeric, 2) as distance_km
    FROM localisation.provinces pr
    JOIN localisation.pays pa ON pr.pays_id = pa.id
    WHERE pr.centre_geo IS NOT NULL
      AND ST_DWithin(
          ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography,
          pr.centre_geo::geography,
          p_rayon_km * 1000
      )
    ORDER BY distance_km;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3. Vérifier si un point est dans une zone de couverture
-- ============================================================================
CREATE OR REPLACE FUNCTION localisation.point_dans_zone_couverture(
    p_latitude NUMERIC,
    p_longitude NUMERIC,
    p_point_service_id UUID
)
RETURNS BOOLEAN AS $$
DECLARE
    v_result BOOLEAN;
BEGIN
    SELECT ST_Contains(
        zone