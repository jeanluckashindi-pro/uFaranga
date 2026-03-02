-- Restructuration du schéma localisation selon la nomenclature GADM
-- GADM utilise: ADM0 (Pays) → ADM1 (Provinces/Régions) → ADM2 (Territoires/Districts) → ADM3 (Communes) → ADM4 (Secteurs/Quartiers)

BEGIN;

-- ============================================================================
-- ÉTAPE 1: Renommer les tables selon la nomenclature GADM (en français)
-- ============================================================================

-- ADM0 = Pays (déjà correct)
-- Pas de changement pour 'pays'

-- ADM1 = Divisions administratives niveau 1
-- Burundi: Provinces | RDC: Provinces
-- Renommer 'provinces' → 'divisions_admin_1'
ALTER TABLE localisation.provinces RENAME TO divisions_admin_1;

-- ADM2 = Divisions administratives niveau 2  
-- Burundi: Communes | RDC: Territoires
-- Renommer 'districts' → 'divisions_admin_2'
ALTER TABLE localisation.districts RENAME TO divisions_admin_2;

-- ADM3 = Divisions administratives niveau 3
-- Burundi: Collines/Zones | RDC: Secteurs/Chefferies
-- Renommer 'communes' → 'divisions_admin_3'
ALTER TABLE localisation.communes RENAME TO divisions_admin_3;

-- ADM4 = Divisions administratives niveau 4
-- Burundi: Sous-collines | RDC: Groupements
-- Renommer 'quartiers' → 'divisions_admin_4'
ALTER TABLE localisation.quartiers RENAME TO divisions_admin_4;

-- ADM5 = Divisions administratives niveau 5 (optionnel)
-- Renommer 'collines' → 'divisions_admin_5'
ALTER TABLE localisation.collines RENAME TO divisions_admin_5;

-- ============================================================================
-- ÉTAPE 2: Ajouter une colonne 'type_division' pour identifier le type local
-- ============================================================================

-- Pour ADM1
ALTER TABLE localisation.divisions_admin_1 
ADD COLUMN IF NOT EXISTS type_division VARCHAR(50);

UPDATE localisation.divisions_admin_1 d
SET type_division = CASE 
    WHEN p.code_iso_2 = 'BI' THEN 'Province'
    WHEN p.code_iso_2 = 'CD' THEN 'Province'
    ELSE 'Province'
END
FROM localisation.pays p
WHERE d.pays_id = p.id;

-- Pour ADM2
ALTER TABLE localisation.divisions_admin_2 
ADD COLUMN IF NOT EXISTS type_division VARCHAR(50);

UPDATE localisation.divisions_admin_2 d
SET type_division = CASE 
    WHEN p.code_iso_2 = 'BI' THEN 'Commune'
    WHEN p.code_iso_2 = 'CD' THEN 'Territoire'
    ELSE 'District'
END
FROM localisation.divisions_admin_1 d1
JOIN localisation.pays p ON d1.pays_id = p.id
WHERE d.province_id = d1.id;

-- Pour ADM3
ALTER TABLE localisation.divisions_admin_3 
ADD COLUMN IF NOT EXISTS type_division VARCHAR(50);

UPDATE localisation.divisions_admin_3 d
SET type_division = CASE 
    WHEN p.code_iso_2 = 'BI' THEN 'Zone'
    WHEN p.code_iso_2 = 'CD' THEN 'Secteur'
    ELSE 'Commune'
END
FROM localisation.divisions_admin_2 d2
JOIN localisation.divisions_admin_1 d1 ON d2.province_id = d1.id
JOIN localisation.pays p ON d1.pays_id = p.id
WHERE d.province_id = d2.id;

-- Pour ADM4
ALTER TABLE localisation.divisions_admin_4 
ADD COLUMN IF NOT EXISTS type_division VARCHAR(50);

UPDATE localisation.divisions_admin_4 d
SET type_division = CASE 
    WHEN p.code_iso_2 = 'BI' THEN 'Colline'
    WHEN p.code_iso_2 = 'CD' THEN 'Groupement'
    ELSE 'Quartier'
END
FROM localisation.divisions_admin_3 d3
JOIN localisation.divisions_admin_2 d2 ON d3.province_id = d2.id
JOIN localisation.divisions_admin_1 d1 ON d2.province_id = d1.id
JOIN localisation.pays p ON d1.pays_id = p.id
WHERE d.commune_id = d3.id;

-- Pour ADM5
ALTER TABLE localisation.divisions_admin_5 
ADD COLUMN IF NOT EXISTS type_division VARCHAR(50);

UPDATE localisation.divisions_admin_5 d
SET type_division = CASE 
    WHEN p.code_iso_2 = 'BI' THEN 'Sous-colline'
    WHEN p.code_iso_2 = 'CD' THEN 'Village'
    ELSE 'Sous-localité'
END
FROM localisation.divisions_admin_4 d4
JOIN localisation.divisions_admin_3 d3 ON d4.commune_id = d3.id
JOIN localisation.divisions_admin_2 d2 ON d3.province_id = d2.id
JOIN localisation.divisions_admin_1 d1 ON d2.province_id = d1.id
JOIN localisation.pays p ON d1.pays_id = p.id
WHERE d.quartier_id = d4.id;

-- ============================================================================
-- ÉTAPE 3: Renommer les colonnes de clés étrangères pour cohérence
-- ============================================================================

-- Dans divisions_admin_2: province_id → division_admin_1_id
ALTER TABLE localisation.divisions_admin_2 
RENAME COLUMN province_id TO division_admin_1_id;

-- Dans divisions_admin_3: province_id → division_admin_2_id
ALTER TABLE localisation.divisions_admin_3 
RENAME COLUMN province_id TO division_admin_2_id;

-- Dans divisions_admin_4: commune_id → division_admin_3_id
ALTER TABLE localisation.divisions_admin_4 
RENAME COLUMN commune_id TO division_admin_3_id;

-- Dans divisions_admin_5: quartier_id → division_admin_4_id
ALTER TABLE localisation.divisions_admin_5 
RENAME COLUMN quartier_id TO division_admin_4_id;

-- Dans points_de_service: quartier_id → division_admin_4_id
ALTER TABLE localisation.points_de_service 
RENAME COLUMN quartier_id TO division_admin_4_id;

-- ============================================================================
-- ÉTAPE 4: Créer des vues pour compatibilité avec l'ancien schéma
-- ============================================================================

-- Vue pour 'provinces' (compatibilité)
CREATE OR REPLACE VIEW localisation.provinces AS
SELECT * FROM localisation.divisions_admin_1;

-- Vue pour 'districts' (compatibilité)
CREATE OR REPLACE VIEW localisation.districts AS
SELECT * FROM localisation.divisions_admin_2;

-- Vue pour 'communes' (compatibilité)
CREATE OR REPLACE VIEW localisation.communes AS
SELECT * FROM localisation.divisions_admin_3;

-- Vue pour 'quartiers' (compatibilité)
CREATE OR REPLACE VIEW localisation.quartiers AS
SELECT * FROM localisation.divisions_admin_4;

-- Vue pour 'collines' (compatibilité)
CREATE OR REPLACE VIEW localisation.collines AS
SELECT * FROM localisation.divisions_admin_5;

-- ============================================================================
-- ÉTAPE 5: Ajouter des index sur les nouvelles colonnes
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_div_adm1_type ON localisation.divisions_admin_1(type_division);
CREATE INDEX IF NOT EXISTS idx_div_adm2_type ON localisation.divisions_admin_2(type_division);
CREATE INDEX IF NOT EXISTS idx_div_adm3_type ON localisation.divisions_admin_3(type_division);
CREATE INDEX IF NOT EXISTS idx_div_adm4_type ON localisation.divisions_admin_4(type_division);
CREATE INDEX IF NOT EXISTS idx_div_adm5_type ON localisation.divisions_admin_5(type_division);

COMMIT;

-- ============================================================================
-- VÉRIFICATION
-- ============================================================================

SELECT 'Restructuration terminée!' as message;

-- Afficher la nouvelle structure
SELECT 
    'ADM0' as niveau,
    'pays' as table_name,
    COUNT(*) as nb_enregistrements
FROM localisation.pays
WHERE code_iso_2 IN ('BI', 'CD')

UNION ALL

SELECT 
    'ADM1',
    'divisions_admin_1',
    COUNT(*)
FROM localisation.divisions_admin_1
WHERE pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 IN ('BI', 'CD'))

UNION ALL

SELECT 
    'ADM2',
    'divisions_admin_2',
    COUNT(*)
FROM localisation.divisions_admin_2
WHERE division_admin_1_id IN (
    SELECT id FROM localisation.divisions_admin_1 
    WHERE pays_id IN (SELECT id FROM localisation.pays WHERE code_iso_2 IN ('BI', 'CD'))
)

UNION ALL

SELECT 
    'ADM3',
    'divisions_admin_3',
    COUNT(*)
FROM localisation.divisions_admin_3

UNION ALL

SELECT 
    'ADM4',
    'divisions_admin_4',
    COUNT(*)
FROM localisation.divisions_admin_4

UNION ALL

SELECT 
    'ADM5',
    'divisions_admin_5',
    COUNT(*)
FROM localisation.divisions_admin_5;

-- Afficher les types de divisions par pays
SELECT 
    p.nom as pays,
    d1.type_division,
    COUNT(*) as nombre
FROM localisation.pays p
JOIN localisation.divisions_admin_1 d1 ON d1.pays_id = p.id
WHERE p.code_iso_2 IN ('BI', 'CD')
GROUP BY p.nom, d1.type_division
ORDER BY p.nom;
