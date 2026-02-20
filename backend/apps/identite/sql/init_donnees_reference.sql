-- =============================================================================
-- Script SQL pour initialiser les données de référence du module IDENTITE
-- =============================================================================
-- Usage: Exécuter ce script dans PostgreSQL après avoir créé les tables
-- =============================================================================

-- Activer le schéma identite
SET search_path TO identite, public;

-- =============================================================================
-- 1. TYPES D'UTILISATEURS
-- =============================================================================
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES 
    ('CLIENT', 'Client', 'Client standard de la plateforme', 1, true, NOW(), NOW()),
    ('AGENT', 'Agent', 'Agent de service (dépôt, retrait, etc.)', 2, true, NOW(), NOW()),
    ('MARCHAND', 'Marchand', 'Commerçant acceptant les paiements', 3, true, NOW(), NOW()),
    ('ADMIN', 'Administrateur', 'Administrateur de la plateforme', 4, true, NOW(), NOW()),
    ('SUPER_ADMIN', 'Super Administrateur', 'Super administrateur avec tous les droits', 5, true, NOW(), NOW()),
    ('SYSTEME', 'Système', 'Compte système pour les opérations automatiques', 6, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    ordre_affichage = EXCLUDED.ordre_affichage,
    date_modification = NOW();

-- =============================================================================
-- 2. NIVEAUX KYC
-- =============================================================================
INSERT INTO identite.niveaux_kyc (
    niveau, 
    libelle, 
    description, 
    limite_transaction_journaliere, 
    limite_solde_maximum, 
    documents_requis, 
    est_actif, 
    date_creation, 
    date_modification
)
VALUES 
    (
        0, 
        'Non vérifié', 
        'Aucune vérification effectuée', 
        0, 
        0, 
        '[]'::jsonb, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        1, 
        'Basique', 
        'Vérification basique (téléphone + email)', 
        50000, 
        100000, 
        '["telephone", "email"]'::jsonb, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        2, 
        'Complet', 
        'Vérification complète (pièce d''identité)', 
        500000, 
        2000000, 
        '["telephone", "email", "piece_identite", "selfie"]'::jsonb, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        3, 
        'Premium', 
        'Vérification premium (justificatif de domicile)', 
        5000000, 
        20000000, 
        '["telephone", "email", "piece_identite", "selfie", "justificatif_domicile"]'::jsonb, 
        true, 
        NOW(), 
        NOW()
    )
ON CONFLICT (niveau) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    limite_transaction_journaliere = EXCLUDED.limite_transaction_journaliere,
    limite_solde_maximum = EXCLUDED.limite_solde_maximum,
    documents_requis = EXCLUDED.documents_requis,
    date_modification = NOW();

-- =============================================================================
-- 3. STATUTS UTILISATEURS
-- =============================================================================
INSERT INTO identite.statuts_utilisateurs (
    code, 
    libelle, 
    description, 
    couleur, 
    permet_connexion, 
    permet_transactions, 
    ordre_affichage, 
    est_actif, 
    date_creation, 
    date_modification
)
VALUES 
    (
        'ACTIF', 
        'Actif', 
        'Compte actif et opérationnel', 
        '#28a745', 
        true, 
        true, 
        1, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        'EN_VERIFICATION', 
        'En vérification', 
        'Compte en cours de vérification KYC', 
        '#ffc107', 
        true, 
        false, 
        2, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        'SUSPENDU', 
        'Suspendu', 
        'Compte temporairement suspendu', 
        '#fd7e14', 
        false, 
        false, 
        3, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        'BLOQUE', 
        'Bloqué', 
        'Compte bloqué pour raisons de sécurité', 
        '#dc3545', 
        false, 
        false, 
        4, 
        true, 
        NOW(), 
        NOW()
    ),
    (
        'FERME', 
        'Fermé', 
        'Compte définitivement fermé', 
        '#6c757d', 
        false, 
        false, 
        5, 
        true, 
        NOW(), 
        NOW()
    )
ON CONFLICT (code) DO UPDATE SET
    libelle = EXCLUDED.libelle,
    description = EXCLUDED.description,
    couleur = EXCLUDED.couleur,
    permet_connexion = EXCLUDED.permet_connexion,
    permet_transactions = EXCLUDED.permet_transactions,
    ordre_affichage = EXCLUDED.ordre_affichage,
    date_modification = NOW();

-- =============================================================================
-- VÉRIFICATION DES DONNÉES INSÉRÉES
-- =============================================================================

-- Compter les types d'utilisateurs
SELECT COUNT(*) as nb_types FROM identite.types_utilisateurs;

-- Compter les niveaux KYC
SELECT COUNT(*) as nb_niveaux FROM identite.niveaux_kyc;

-- Compter les statuts
SELECT COUNT(*) as nb_statuts FROM identite.statuts_utilisateurs;

-- Afficher tous les types
SELECT code, libelle, ordre_affichage FROM identite.types_utilisateurs ORDER BY ordre_affichage;

-- Afficher tous les niveaux KYC
SELECT niveau, libelle, limite_transaction_journaliere, limite_solde_maximum FROM identite.niveaux_kyc ORDER BY niveau;

-- Afficher tous les statuts
SELECT code, libelle, couleur, permet_connexion, permet_transactions FROM identite.statuts_utilisateurs ORDER BY ordre_affichage;

-- =============================================================================
-- FIN DU SCRIPT
-- =============================================================================
