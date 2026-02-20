-- =============================================================================
-- REQUÊTES SQL INDIVIDUELLES POUR LES DONNÉES DE RÉFÉRENCE
-- =============================================================================
-- Vous pouvez copier-coller ces requêtes une par une selon vos besoins
-- =============================================================================

-- =============================================================================
-- TYPES D'UTILISATEURS (une par une)
-- =============================================================================

-- Type: CLIENT
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('CLIENT', 'Client', 'Client standard de la plateforme', 1, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Type: AGENT
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('AGENT', 'Agent', 'Agent de service (dépôt, retrait, etc.)', 2, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Type: MARCHAND
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('MARCHAND', 'Marchand', 'Commerçant acceptant les paiements', 3, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Type: ADMIN
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('ADMIN', 'Administrateur', 'Administrateur de la plateforme', 4, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Type: SUPER_ADMIN
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('SUPER_ADMIN', 'Super Administrateur', 'Super administrateur avec tous les droits', 5, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Type: SYSTEME
INSERT INTO identite.types_utilisateurs (code, libelle, description, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('SYSTEME', 'Système', 'Compte système pour les opérations automatiques', 6, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();


-- =============================================================================
-- NIVEAUX KYC (une par une)
-- =============================================================================

-- Niveau 0: Non vérifié
INSERT INTO identite.niveaux_kyc (niveau, libelle, description, limite_transaction_journaliere, limite_solde_maximum, documents_requis, est_actif, date_creation, date_modification)
VALUES (0, 'Non vérifié', 'Aucune vérification effectuée', 0, 0, '[]'::jsonb, true, NOW(), NOW())
ON CONFLICT (niveau) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Niveau 1: Basique
INSERT INTO identite.niveaux_kyc (niveau, libelle, description, limite_transaction_journaliere, limite_solde_maximum, documents_requis, est_actif, date_creation, date_modification)
VALUES (1, 'Basique', 'Vérification basique (téléphone + email)', 50000, 100000, '["telephone", "email"]'::jsonb, true, NOW(), NOW())
ON CONFLICT (niveau) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Niveau 2: Complet
INSERT INTO identite.niveaux_kyc (niveau, libelle, description, limite_transaction_journaliere, limite_solde_maximum, documents_requis, est_actif, date_creation, date_modification)
VALUES (2, 'Complet', 'Vérification complète (pièce d''identité)', 500000, 2000000, '["telephone", "email", "piece_identite", "selfie"]'::jsonb, true, NOW(), NOW())
ON CONFLICT (niveau) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Niveau 3: Premium
INSERT INTO identite.niveaux_kyc (niveau, libelle, description, limite_transaction_journaliere, limite_solde_maximum, documents_requis, est_actif, date_creation, date_modification)
VALUES (3, 'Premium', 'Vérification premium (justificatif de domicile)', 5000000, 20000000, '["telephone", "email", "piece_identite", "selfie", "justificatif_domicile"]'::jsonb, true, NOW(), NOW())
ON CONFLICT (niveau) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();


-- =============================================================================
-- STATUTS UTILISATEURS (une par une)
-- =============================================================================

-- Statut: ACTIF
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('ACTIF', 'Actif', 'Compte actif et opérationnel', '#28a745', true, true, 1, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Statut: EN_VERIFICATION
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('EN_VERIFICATION', 'En vérification', 'Compte en cours de vérification KYC', '#ffc107', true, false, 2, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Statut: SUSPENDU
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('SUSPENDU', 'Suspendu', 'Compte temporairement suspendu', '#fd7e14', false, false, 3, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Statut: BLOQUE
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('BLOQUE', 'Bloqué', 'Compte bloqué pour raisons de sécurité', '#dc3545', false, false, 4, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();

-- Statut: FERME
INSERT INTO identite.statuts_utilisateurs (code, libelle, description, couleur, permet_connexion, permet_transactions, ordre_affichage, est_actif, date_creation, date_modification)
VALUES ('FERME', 'Fermé', 'Compte définitivement fermé', '#6c757d', false, false, 5, true, NOW(), NOW())
ON CONFLICT (code) DO UPDATE SET libelle = EXCLUDED.libelle, date_modification = NOW();


-- =============================================================================
-- REQUÊTES DE CONSULTATION
-- =============================================================================

-- Voir tous les types d'utilisateurs
SELECT * FROM identite.types_utilisateurs ORDER BY ordre_affichage;

-- Voir tous les niveaux KYC
SELECT * FROM identite.niveaux_kyc ORDER BY niveau;

-- Voir tous les statuts
SELECT * FROM identite.statuts_utilisateurs ORDER BY ordre_affichage;

-- Compter les enregistrements
SELECT 
    (SELECT COUNT(*) FROM identite.types_utilisateurs) as nb_types,
    (SELECT COUNT(*) FROM identite.niveaux_kyc) as nb_niveaux,
    (SELECT COUNT(*) FROM identite.statuts_utilisateurs) as nb_statuts;


-- =============================================================================
-- REQUÊTES DE SUPPRESSION (À UTILISER AVEC PRÉCAUTION)
-- =============================================================================

-- Supprimer tous les types (ATTENTION: peut causer des erreurs si des utilisateurs existent)
-- DELETE FROM identite.types_utilisateurs;

-- Supprimer tous les niveaux KYC
-- DELETE FROM identite.niveaux_kyc;

-- Supprimer tous les statuts
-- DELETE FROM identite.statuts_utilisateurs;


-- =============================================================================
-- REQUÊTES DE MISE À JOUR
-- =============================================================================

-- Modifier un type d'utilisateur
-- UPDATE identite.types_utilisateurs 
-- SET libelle = 'Nouveau libellé', date_modification = NOW()
-- WHERE code = 'CLIENT';

-- Modifier un niveau KYC
-- UPDATE identite.niveaux_kyc 
-- SET limite_transaction_journaliere = 100000, date_modification = NOW()
-- WHERE niveau = 1;

-- Modifier un statut
-- UPDATE identite.statuts_utilisateurs 
-- SET couleur = '#FF0000', date_modification = NOW()
-- WHERE code = 'ACTIF';
