--
-- TRIGGERS AUTOMATIQUES POUR GRAND LIVRE
-- Date: 2026-02-20
-- Description: Enregistrement automatique de TOUTES les opérations financières
-- PRÉCISION ET VIGILANCE EXTRÊME
--

-- ============================================================================
-- FONCTION 1: Enregistrer automatiquement dans le grand livre
-- ============================================================================

CREATE OR REPLACE FUNCTION ledger.enregistrer_operation_automatique()
RETURNS TRIGGER AS $$$
DECLARE
    v_numero_ecriture VARCHAR(50);
    v_hash VARCHAR(64);
    v_exercice INTEGER;
    v_periode VARCHAR(7);
    v_utilisateur_id UUID;
    v_utilisateur_nom VARCHAR(255);
    v_session_id UUID;
    v_ip INET;
    v_device_id VARCHAR(100);
BEGIN
    -- Générer numéro d'écriture unique
    v_numero_ecriture := ledger.generer_numero_ecriture();
    
    -- Calculer exercice et période comptable
    v_exercice := EXTRACT(YEAR FROM CURRENT_DATE);
    v_periode := TO_CHAR(CURRENT_DATE, 'YYYY-MM');
    
    -- Récupérer informations utilisateur (depuis NEW.cree_par ou contexte)
    v_utilisateur_id := COALESCE(NEW.cree_par, '00000000-0000-0000-0000-000000000000'::UUID);
    v_utilisateur_nom := COALESCE(current_setting('app.user_name', true), 'SYSTEME');
    v_session_id := COALESCE(current_setting('app.session_id', true)::UUID, NULL);
    v_ip := COALESCE(current_setting('app.ip_address', true)::INET, NULL);
    v_device_id := COALESCE(current_setting('app.device_id', true), NULL);
    
    -- Calculer hash d'intégrité
    v_hash := encode(digest(
        NEW.id::TEXT || 
        NEW.reference_transaction || 
        NEW.montant::TEXT || 
        NEW.devise || 
        CURRENT_TIMESTAMP::TEXT,
        'sha256'
    ), 'hex');
    
    IF TG_OP = 'INSERT' THEN
        -- ÉCRITURE DÉBIT (compte source)
        IF NEW.compte_source_id IS NOT NULL THEN
            INSERT INTO ledger.ecritures_comptables (
                numero_ecriture,
                transaction_id,
                reference_transaction,
                type_transaction,
                compte_id,
                numero_compte,
                sens,
                montant,
                devise,
                solde_avant,
                solde_apres,
                compte_contrepartie_id,
                numero_compte_contrepartie,
                categorie_comptable,
                sous_categorie,
                exercice_comptable,
                periode_comptable,
                date_comptable,
                date_valeur,
                qui_utilisateur_id,
                qui_nom,
                qui_type,
                quand,
                quoi,
                comment,
                pourquoi,
                adresse_ip,
                device_id,
                session_id,
                request_id,
                correlation_id,
                pays,
                statut,
                metadonnees,
                hash_integrite
            )
            SELECT
                v_numero_ecriture || '-D',
                NEW.id,
                NEW.reference_transaction,
                NEW.type_transaction,
                NEW.compte_source_id,
                c.numero_compte,
                'DEBIT',
                NEW.montant_total, -- Montant + frais
                NEW.devise,
                c.solde_actuel, -- Solde AVANT
                c.solde_actuel - NEW.montant_total, -- Solde APRÈS
                NEW.compte_destination_id,
                cd.numero_compte,
                CASE 
                    WHEN NEW.type_transaction = 'DEPOT' THEN 'ENCAISSEMENT'
                    WHEN NEW.type_transaction = 'RETRAIT' THEN 'DECAISSEMENT'
                    WHEN NEW.type_transaction = 'TRANSFERT' THEN 'VIREMENT'
                    WHEN NEW.type_transaction = 'PAIEMENT' THEN 'PAIEMENT'
                    WHEN NEW.type_transaction = 'FRAIS' THEN 'FRAIS_BANCAIRES'
                    ELSE 'AUTRE'
                END,
                NEW.type_transaction,
                v_exercice,
                v_periode,
                CURRENT_DATE,
                CURRENT_DATE,
                v_utilisateur_id,
                v_utilisateur_nom,
                c.type_utilisateur,
                CURRENT_TIMESTAMP,
                'Transaction ' || NEW.type_transaction || ' - Débit compte source',
                'SYSTEME',
                NEW.description,
                v_ip,
                v_device_id,
                v_session_id,
                NEW.id, -- request_id = transaction_id
                NEW.id, -- correlation_id = transaction_id
                c.pays_creation,
                'VALIDEE',
                jsonb_build_object(
                    'transaction_id', NEW.id,
                    'type', NEW.type_transaction,
                    'montant', NEW.montant,
                    'frais', NEW.frais,
                    'statut_transaction', NEW.statut,
                    'auto_generated', true,
                    'trigger', 'enregistrer_operation_automatique'
                ),
                v_hash
            FROM portefeuille.comptes c
            LEFT JOIN portefeuille.comptes cd ON cd.id = NEW.compte_destination_id
            WHERE c.id = NEW.compte_source_id;
        END IF;
        
        -- ÉCRITURE CRÉDIT (compte destination)
        IF NEW.compte_destination_id IS NOT NULL THEN
            INSERT INTO ledger.ecritures_comptables (
                numero_ecriture,
                transaction_id,
                reference_transaction,
                type_transaction,
                compte_id,
                numero_compte,
                sens,
                montant,
                devise,
                solde_avant,
                solde_apres,
                compte_contrepartie_id,
                numero_compte_contrepartie,
                categorie_comptable,
                sous_categorie,
                exercice_comptable,
                periode_comptable,
                date_comptable,
                date_valeur,
                qui_utilisateur_id,
                qui_nom,
                qui_type,
                quand,
                quoi,
                comment,
                pourquoi,
                adresse_ip,
                device_id,
                session_id,
                request_id,
                correlation_id,
                pays,
                statut,
                metadonnees,
                hash_integrite
            )
            SELECT
                v_numero_ecriture || '-C',
                NEW.id,
                NEW.reference_transaction,
                NEW.type_transaction,
                NEW.compte_destination_id,
                c.numero_compte,
                'CREDIT',
                NEW.montant, -- Montant sans frais
                NEW.devise,
                c.solde_actuel, -- Solde AVANT
                c.solde_actuel + NEW.montant, -- Solde APRÈS
                NEW.compte_source_id,
                cs.numero_compte,
                CASE 
                    WHEN NEW.type_transaction = 'DEPOT' THEN 'ENCAISSEMENT'
                    WHEN NEW.type_transaction = 'RETRAIT' THEN 'DECAISSEMENT'
                    WHEN NEW.type_transaction = 'TRANSFERT' THEN 'VIREMENT'
                    WHEN NEW.type_transaction = 'PAIEMENT' THEN 'PAIEMENT'
                    WHEN NEW.type_transaction = 'COMMISSION' THEN 'COMMISSION'
                    ELSE 'AUTRE'
                END,
                NEW.type_transaction,
                v_exercice,
                v_periode,
                CURRENT_DATE,
                CURRENT_DATE,
                v_utilisateur_id,
                v_utilisateur_nom,
                c.type_utilisateur,
                CURRENT_TIMESTAMP,
                'Transaction ' || NEW.type_transaction || ' - Crédit compte destination',
                'SYSTEME',
                NEW.description,
                v_ip,
                v_device_id,
                v_session_id,
                NEW.id,
                NEW.id,
                c.pays_creation,
                'VALIDEE',
                jsonb_build_object(
                    'transaction_id', NEW.id,
                    'type', NEW.type_transaction,
                    'montant', NEW.montant,
                    'frais', NEW.frais,
                    'statut_transaction', NEW.statut,
                    'auto_generated', true,
                    'trigger', 'enregistrer_operation_automatique'
                ),
                v_hash
            FROM portefeuille.comptes c
            LEFT JOIN portefeuille.comptes cs ON cs.id = NEW.compte_source_id
            WHERE c.id = NEW.compte_destination_id;
        END IF;
        
        -- ÉCRITURE FRAIS (si frais > 0)
        IF NEW.frais > 0 AND NEW.compte_source_id IS NOT NULL THEN
            INSERT INTO ledger.ecritures_comptables (
                numero_ecriture,
                transaction_id,
                reference_transaction,
                type_transaction,
                compte_id,
                numero_compte,
                sens,
                montant,
                devise,
                solde_avant,
                solde_apres,
                categorie_comptable,
                sous_categorie,
                exercice_comptable,
                periode_comptable,
                date_comptable,
                date_valeur,
                qui_utilisateur_id,
                qui_nom,
                qui_type,
                quand,
                quoi,
                comment,
                pourquoi,
                adresse_ip,
                device_id,
                session_id,
                request_id,
                correlation_id,
                statut,
                metadonnees,
                hash_integrite
            )
            SELECT
                v_numero_ecriture || '-F',
                NEW.id,
                NEW.reference_transaction,
                'FRAIS',
                NEW.compte_source_id,
                c.numero_compte,
                'DEBIT',
                NEW.frais,
                NEW.devise,
                c.solde_actuel - NEW.montant, -- Après débit principal
                c.solde_actuel - NEW.montant - NEW.frais, -- Après frais
                'FRAIS_BANCAIRES',
                'FRAIS_' || NEW.type_transaction,
                v_exercice,
                v_periode,
                CURRENT_DATE,
                CURRENT_DATE,
                v_utilisateur_id,
                v_utilisateur_nom,
                c.type_utilisateur,
                CURRENT_TIMESTAMP,
                'Frais sur transaction ' || NEW.type_transaction,
                'SYSTEME',
                'Frais: ' || NEW.frais || ' ' || NEW.devise,
                v_ip,
                v_device_id,
                v_session_id,
                NEW.id,
                NEW.id,
                'VALIDEE',
                jsonb_build_object(
                    'transaction_id', NEW.id,
                    'type', 'FRAIS',
                    'montant_frais', NEW.frais,
                    'transaction_principale', NEW.type_transaction,
                    'auto_generated', true,
                    'trigger', 'enregistrer_operation_automatique'
                ),
                v_hash
            FROM portefeuille.comptes c
            WHERE c.id = NEW.compte_source_id;
        END IF;
        
    ELSIF TG_OP = 'UPDATE' THEN
        -- Si changement de statut vers ANNULEE, créer écritures d'annulation
        IF OLD.statut != 'ANNULEE' AND NEW.statut = 'ANNULEE' THEN
            -- Annuler les écritures existantes
            UPDATE ledger.ecritures_comptables
            SET statut = 'ANNULEE',
                metadonnees = metadonnees || jsonb_build_object(
                    'annule_le', CURRENT_TIMESTAMP,
                    'annule_par', v_utilisateur_id,
                    'raison', 'Transaction annulée'
                )
            WHERE transaction_id = NEW.id
              AND statut = 'VALIDEE';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION ledger.enregistrer_operation_automatique IS 
'Enregistre automatiquement TOUTES les opérations financières dans le grand livre avec précision extrême';


-- ============================================================================
-- FONCTION 2: Enregistrer modifications de solde de compte
-- ============================================================================

CREATE OR REPLACE FUNCTION ledger.enregistrer_modification_solde()
RETURNS TRIGGER AS $$
DECLARE
    v_numero_ecriture VARCHAR(50);
    v_hash VARCHAR(64);
    v_exercice INTEGER;
    v_periode VARCHAR(7);
    v_utilisateur_id UUID;
    v_utilisateur_nom VARCHAR(255);
BEGIN
    -- Seulement si le solde change
    IF OLD.solde_actuel != NEW.solde_actuel THEN
        v_numero_ecriture := ledger.generer_numero_ecriture();
        v_exercice := EXTRACT(YEAR FROM CURRENT_DATE);
        v_periode := TO_CHAR(CURRENT_DATE, 'YYYY-MM');
        v_utilisateur_id := COALESCE(NEW.modifie_par, NEW.cree_par, '00000000-0000-0000-0000-000000000000'::UUID);
        v_utilisateur_nom := COALESCE(current_setting('app.user_name', true), 'SYSTEME');
        
        v_hash := encode(digest(
            NEW.id::TEXT || 
            NEW.numero_compte || 
            NEW.solde_actuel::TEXT || 
            CURRENT_TIMESTAMP::TEXT,
            'sha256'
        ), 'hex');
        
        INSERT INTO ledger.ecritures_comptables (
            numero_ecriture,
            transaction_id,
            reference_transaction,
            type_transaction,
            compte_id,
            numero_compte,
            sens,
            montant,
            devise,
            solde_avant,
            solde_apres,
            categorie_comptable,
            sous_categorie,
            exercice_comptable,
            periode_comptable,
            date_comptable,
            date_valeur,
            qui_utilisateur_id,
            qui_nom,
            qui_type,
            quand,
            quoi,
            comment,
            pourquoi,
            statut,
            metadonnees,
            hash_integrite
        ) VALUES (
            v_numero_ecriture,
            NEW.id, -- Utiliser compte_id comme transaction_id
            'AJUST-' || NEW.numero_compte,
            'AJUSTEMENT_SOLDE',
            NEW.id,
            NEW.numero_compte,
            CASE WHEN NEW.solde_actuel > OLD.solde_actuel THEN 'CREDIT' ELSE 'DEBIT' END,
            ABS(NEW.solde_actuel - OLD.solde_actuel),
            NEW.devise,
            OLD.solde_actuel,
            NEW.solde_actuel,
            'AJUSTEMENT',
            'MODIFICATION_SOLDE',
            v_exercice,
            v_periode,
            CURRENT_DATE,
            CURRENT_DATE,
            v_utilisateur_id,
            v_utilisateur_nom,
            NEW.type_utilisateur,
            CURRENT_TIMESTAMP,
            'Modification solde compte: ' || OLD.solde_actuel || ' -> ' || NEW.solde_actuel,
            'SYSTEME',
            'Ajustement automatique du solde',
            'VALIDEE',
            jsonb_build_object(
                'compte_id', NEW.id,
                'ancien_solde', OLD.solde_actuel,
                'nouveau_solde', NEW.solde_actuel,
                'difference', NEW.solde_actuel - OLD.solde_actuel,
                'auto_generated', true,
                'trigger', 'enregistrer_modification_solde'
            ),
            v_hash
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION ledger.enregistrer_modification_solde IS 
'Enregistre automatiquement toute modification de solde de compte dans le grand livre';

-- ============================================================================
-- FONCTION 3: Vérifier cohérence avant écriture
-- ============================================================================

CREATE OR REPLACE FUNCTION ledger.verifier_coherence_ecriture()
RETURNS TRIGGER AS $$
DECLARE
    v_solde_calcule DECIMAL(20, 2);
BEGIN
    -- Vérifier cohérence du solde
    IF NEW.sens = 'DEBIT' THEN
        v_solde_calcule := NEW.solde_avant - NEW.montant;
    ELSE
        v_solde_calcule := NEW.solde_avant + NEW.montant;
    END IF;
    
    IF v_solde_calcule != NEW.solde_apres THEN
        RAISE EXCEPTION 'ERREUR COHÉRENCE: Solde après (%) ne correspond pas au calcul (%). Sens: %, Montant: %',
            NEW.solde_apres, v_solde_calcule, NEW.sens, NEW.montant;
    END IF;
    
    -- Vérifier que le hash est présent
    IF NEW.hash_integrite IS NULL OR LENGTH(NEW.hash_integrite) != 64 THEN
        RAISE EXCEPTION 'ERREUR SÉCURITÉ: Hash d''intégrité manquant ou invalide';
    END IF;
    
    -- Vérifier que les champs obligatoires sont remplis
    IF NEW.qui_utilisateur_id IS NULL THEN
        RAISE EXCEPTION 'ERREUR TRAÇABILITÉ: Utilisateur manquant';
    END IF;
    
    IF NEW.quoi IS NULL OR LENGTH(TRIM(NEW.quoi)) = 0 THEN
        RAISE EXCEPTION 'ERREUR TRAÇABILITÉ: Description de l''action manquante';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION ledger.verifier_coherence_ecriture IS 
'Vérifie la cohérence et l''intégrité de chaque écriture avant insertion';


-- ============================================================================
-- CRÉER LES TRIGGERS SUR LES TABLES
-- ============================================================================

-- Trigger sur table transactions: Enregistrement automatique dans le grand livre
DROP TRIGGER IF EXISTS trigger_grand_livre_transaction ON transaction.transactions;
CREATE TRIGGER trigger_grand_livre_transaction
    AFTER INSERT OR UPDATE ON transaction.transactions
    FOR EACH ROW
    WHEN (NEW.statut IN ('VALIDEE', 'ANNULEE'))
    EXECUTE PROCEDURE ledger.enregistrer_operation_automatique();

COMMENT ON TRIGGER trigger_grand_livre_transaction ON transaction.transactions IS
'Enregistre automatiquement chaque transaction validée ou annulée dans le grand livre';

-- Trigger sur table comptes: Enregistrement modifications de solde
DROP TRIGGER IF EXISTS trigger_grand_livre_solde ON portefeuille.comptes;
CREATE TRIGGER trigger_grand_livre_solde
    AFTER UPDATE ON portefeuille.comptes
    FOR EACH ROW
    WHEN (OLD.solde_actuel IS DISTINCT FROM NEW.solde_actuel)
    EXECUTE PROCEDURE ledger.enregistrer_modification_solde();

COMMENT ON TRIGGER trigger_grand_livre_solde ON portefeuille.comptes IS
'Enregistre automatiquement toute modification de solde dans le grand livre';

-- Trigger de vérification avant insertion dans le grand livre
DROP TRIGGER IF EXISTS trigger_verifier_coherence ON ledger.ecritures_comptables;
CREATE TRIGGER trigger_verifier_coherence
    BEFORE INSERT ON ledger.ecritures_comptables
    FOR EACH ROW
    EXECUTE PROCEDURE ledger.verifier_coherence_ecriture();

COMMENT ON TRIGGER trigger_verifier_coherence ON ledger.ecritures_comptables IS
'Vérifie la cohérence et l''intégrité de chaque écriture avant insertion';

-- ============================================================================
-- FONCTION 4: Rapport d'intégrité du grand livre
-- ============================================================================

CREATE OR REPLACE FUNCTION ledger.verifier_integrite_grand_livre(
    p_date_debut DATE DEFAULT NULL,
    p_date_fin DATE DEFAULT NULL
)
RETURNS TABLE (
    total_ecritures BIGINT,
    total_debits DECIMAL,
    total_credits DECIMAL,
    difference DECIMAL,
    est_equilibre BOOLEAN,
    ecritures_sans_hash INTEGER,
    ecritures_incoherentes INTEGER,
    message TEXT
) AS $$
DECLARE
    v_date_debut DATE;
    v_date_fin DATE;
BEGIN
    v_date_debut := COALESCE(p_date_debut, CURRENT_DATE - INTERVAL '30 days');
    v_date_fin := COALESCE(p_date_fin, CURRENT_DATE);
    
    RETURN QUERY
    WITH stats AS (
        SELECT
            COUNT(*) as nb_ecritures,
            SUM(CASE WHEN sens = 'DEBIT' THEN montant ELSE 0 END) as sum_debits,
            SUM(CASE WHEN sens = 'CREDIT' THEN montant ELSE 0 END) as sum_credits,
            COUNT(*) FILTER (WHERE hash_integrite IS NULL OR LENGTH(hash_integrite) != 64) as nb_sans_hash,
            COUNT(*) FILTER (WHERE 
                (sens = 'DEBIT' AND solde_apres != solde_avant - montant) OR
                (sens = 'CREDIT' AND solde_apres != solde_avant + montant)
            ) as nb_incoherentes
        FROM ledger.ecritures_comptables
        WHERE date_comptable BETWEEN v_date_debut AND v_date_fin
          AND statut = 'VALIDEE'
    )
    SELECT
        nb_ecritures,
        sum_debits,
        sum_credits,
        sum_debits - sum_credits as diff,
        ABS(sum_debits - sum_credits) < 0.01 as equilibre,
        nb_sans_hash::INTEGER,
        nb_incoherentes::INTEGER,
        CASE 
            WHEN ABS(sum_debits - sum_credits) < 0.01 THEN 
                'Grand livre équilibré ✓'
            ELSE 
                'ALERTE: Grand livre déséquilibré de ' || (sum_debits - sum_credits)::TEXT
        END as msg
    FROM stats;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION ledger.verifier_integrite_grand_livre IS
'Vérifie l''intégrité et l''équilibre du grand livre sur une période donnée';

-- ============================================================================
-- FONCTION 5: Statistiques du grand livre
-- ============================================================================

CREATE OR REPLACE FUNCTION ledger.statistiques_grand_livre(
    p_periode VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    periode VARCHAR,
    nombre_ecritures BIGINT,
    nombre_transactions BIGINT,
    volume_debits DECIMAL,
    volume_credits DECIMAL,
    nombre_comptes_actifs BIGINT,
    categories JSONB
) AS $$
DECLARE
    v_periode VARCHAR;
BEGIN
    v_periode := COALESCE(p_periode, TO_CHAR(CURRENT_DATE, 'YYYY-MM'));
    
    RETURN QUERY
    SELECT
        v_periode,
        COUNT(*),
        COUNT(DISTINCT transaction_id),
        SUM(CASE WHEN sens = 'DEBIT' THEN montant ELSE 0 END),
        SUM(CASE WHEN sens = 'CREDIT' THEN montant ELSE 0 END),
        COUNT(DISTINCT compte_id),
        jsonb_object_agg(
            categorie_comptable,
            jsonb_build_object(
                'nombre', COUNT(*),
                'montant', SUM(montant)
            )
        )
    FROM ledger.ecritures_comptables
    WHERE periode_comptable = v_periode
      AND statut = 'VALIDEE'
    GROUP BY v_periode;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION ledger.statistiques_grand_livre IS
'Retourne les statistiques du grand livre pour une période donnée';

-- ============================================================================
-- VUE: Solde de tous les comptes selon le grand livre
-- ============================================================================

CREATE OR REPLACE VIEW ledger.vue_soldes_grand_livre AS
SELECT
    compte_id,
    numero_compte,
    devise,
    SUM(CASE WHEN sens = 'CREDIT' THEN montant ELSE -montant END) as solde_grand_livre,
    MAX(quand) as derniere_ecriture,
    COUNT(*) as nombre_ecritures
FROM ledger.ecritures_comptables
WHERE statut = 'VALIDEE'
GROUP BY compte_id, numero_compte, devise;

COMMENT ON VIEW ledger.vue_soldes_grand_livre IS
'Solde de chaque compte calculé depuis le grand livre (source de vérité)';

-- ============================================================================
-- VUE: Écarts entre soldes comptes et grand livre
-- ============================================================================

CREATE OR REPLACE VIEW ledger.vue_ecarts_soldes AS
SELECT
    c.id as compte_id,
    c.numero_compte,
    c.devise,
    c.solde_actuel as solde_compte,
    COALESCE(gl.solde_grand_livre, 0) as solde_grand_livre,
    c.solde_actuel - COALESCE(gl.solde_grand_livre, 0) as ecart,
    CASE 
        WHEN ABS(c.solde_actuel - COALESCE(gl.solde_grand_livre, 0)) < 0.01 THEN 'OK'
        WHEN ABS(c.solde_actuel - COALESCE(gl.solde_grand_livre, 0)) < 100 THEN 'FAIBLE'
        WHEN ABS(c.solde_actuel - COALESCE(gl.solde_grand_livre, 0)) < 1000 THEN 'MOYEN'
        ELSE 'CRITIQUE'
    END as niveau_ecart,
    c.derniere_synchronisation,
    gl.derniere_ecriture
FROM portefeuille.comptes c
LEFT JOIN ledger.vue_soldes_grand_livre gl ON gl.compte_id = c.id
WHERE c.statut = 'ACTIF';

COMMENT ON VIEW ledger.vue_ecarts_soldes IS
'Détecte les écarts entre les soldes des comptes et le grand livre';

-- ============================================================================
-- MESSAGES DE CONFIRMATION
-- ============================================================================

SELECT '========================================' AS separateur;
SELECT 'TRIGGERS AUTOMATIQUES GRAND LIVRE CRÉÉS!' AS message;
SELECT '========================================' AS separateur;
SELECT 'Triggers créés: 3' AS triggers;
SELECT '  1. trigger_grand_livre_transaction - Sur transaction.transactions' AS trigger_1;
SELECT '  2. trigger_grand_livre_solde - Sur portefeuille.comptes' AS trigger_2;
SELECT '  3. trigger_verifier_coherence - Sur ledger.ecritures_comptables' AS trigger_3;
SELECT '========================================' AS separateur;
SELECT 'Fonctions créées: 5' AS fonctions;
SELECT '  1. enregistrer_operation_automatique() - Enregistrement auto transactions' AS fonction_1;
SELECT '  2. enregistrer_modification_solde() - Enregistrement auto soldes' AS fonction_2;
SELECT '  3. verifier_coherence_ecriture() - Vérification intégrité' AS fonction_3;
SELECT '  4. verifier_integrite_grand_livre() - Rapport intégrité' AS fonction_4;
SELECT '  5. statistiques_grand_livre() - Statistiques période' AS fonction_5;
SELECT '========================================' AS separateur;
SELECT 'Vues créées: 2' AS vues;
SELECT '  1. vue_soldes_grand_livre - Soldes calculés depuis grand livre' AS vue_1;
SELECT '  2. vue_ecarts_soldes - Détection écarts comptes vs grand livre' AS vue_2;
SELECT '========================================' AS separateur;
SELECT 'TOUTES LES OPÉRATIONS FINANCIÈRES SERONT AUTOMATIQUEMENT ENREGISTRÉES!' AS important;
SELECT 'PRÉCISION ET VIGILANCE EXTRÊME ACTIVÉES!' AS vigilance;
SELECT '========================================' AS separateur;

