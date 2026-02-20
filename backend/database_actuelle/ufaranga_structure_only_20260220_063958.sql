--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: audit; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA audit;


ALTER SCHEMA audit OWNER TO postgres;

--
-- Name: SCHEMA audit; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA audit IS 'Audit et traçabilité - TABLES IMMUABLES (APPEND-ONLY)';


--
-- Name: bancaire; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA bancaire;


ALTER SCHEMA bancaire OWNER TO postgres;

--
-- Name: SCHEMA bancaire; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA bancaire IS 'Intégration avec le système bancaire - Comptes réels et mouvements';


--
-- Name: commission; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA commission;


ALTER SCHEMA commission OWNER TO postgres;

--
-- Name: SCHEMA commission; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA commission IS 'Commissions, frais et rémunérations';


--
-- Name: compliance; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA compliance;


ALTER SCHEMA compliance OWNER TO postgres;

--
-- Name: SCHEMA compliance; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA compliance IS 'KYC, AML, documents et vérifications réglementaires';


--
-- Name: configuration; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA configuration;


ALTER SCHEMA configuration OWNER TO postgres;

--
-- Name: SCHEMA configuration; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA configuration IS 'Configuration système et données de référence';


--
-- Name: developpeurs; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA developpeurs;


ALTER SCHEMA developpeurs OWNER TO postgres;

--
-- Name: SCHEMA developpeurs; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA developpeurs IS 'Gestion des comptes développeurs et accès API';


--
-- Name: identite; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA identite;


ALTER SCHEMA identite OWNER TO postgres;

--
-- Name: SCHEMA identite; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA identite IS 'Gestion des identités, authentification et profils utilisateurs';


--
-- Name: localisation; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA localisation;


ALTER SCHEMA localisation OWNER TO postgres;

--
-- Name: SCHEMA localisation; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA localisation IS 'Hiérarchie géographique : Pays → Province → District → Quartier → Point de service / Agent';


--
-- Name: notification; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA notification;


ALTER SCHEMA notification OWNER TO postgres;

--
-- Name: SCHEMA notification; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA notification IS 'File de notifications et alertes';


--
-- Name: portefeuille; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA portefeuille;


ALTER SCHEMA portefeuille OWNER TO postgres;

--
-- Name: SCHEMA portefeuille; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA portefeuille IS 'Portefeuilles virtuels uFaranga - Interface utilisateur';


--
-- Name: transaction; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA transaction;


ALTER SCHEMA transaction OWNER TO postgres;

--
-- Name: SCHEMA transaction; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA transaction IS 'Transactions financières et traitement';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: btree_gist; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS btree_gist WITH SCHEMA public;


--
-- Name: EXTENSION btree_gist; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION btree_gist IS 'support for indexing common datatypes in GiST';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: proteger_journaux(); Type: FUNCTION; Schema: audit; Owner: postgres
--

CREATE FUNCTION audit.proteger_journaux() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: Les journaux d''événements ne peuvent pas être modifiés ou supprimés (TABLE IMMUABLE)';
    RETURN NULL;
END;
$$;


ALTER FUNCTION audit.proteger_journaux() OWNER TO postgres;

--
-- Name: proteger_mouvements_bancaires(); Type: FUNCTION; Schema: bancaire; Owner: postgres
--

CREATE FUNCTION bancaire.proteger_mouvements_bancaires() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION
        'INTERDIT : Les mouvements bancaires réels sont IMMUABLES (UPDATE / DELETE bloqués)';
    RETURN NULL;
END;
$$;


ALTER FUNCTION bancaire.proteger_mouvements_bancaires() OWNER TO postgres;

--
-- Name: proteger_verifications(); Type: FUNCTION; Schema: compliance; Owner: postgres
--

CREATE FUNCTION compliance.proteger_verifications() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: Les vérifications KYC ne peuvent pas être modifiées ou supprimées (TABLE IMMUABLE)';
    RETURN NULL;
END;
$$;


ALTER FUNCTION compliance.proteger_verifications() OWNER TO postgres;

--
-- Name: generer_cle_api(uuid, character varying); Type: FUNCTION; Schema: developpeurs; Owner: postgres
--

CREATE FUNCTION developpeurs.generer_cle_api(p_compte_id uuid, p_environnement character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_prefixe VARCHAR;
    v_random VARCHAR;
    v_cle_complete VARCHAR;
BEGIN
    -- Définir le préfixe selon l'environnement
    IF p_environnement = 'PRODUCTION' THEN
        v_prefixe := 'ufar_live_';
    ELSE
        v_prefixe := 'ufar_test_';
    END IF;
    
    -- Générer une partie aléatoire (32 caractères)
    v_random := encode(gen_random_bytes(24), 'base64');
    v_random := REPLACE(REPLACE(REPLACE(v_random, '+', ''), '/', ''), '=', '');
    v_random := SUBSTRING(v_random, 1, 32);
    
    -- Clé complète
    v_cle_complete := v_prefixe || v_random;
    
    RETURN v_cle_complete;
END;
$$;


ALTER FUNCTION developpeurs.generer_cle_api(p_compte_id uuid, p_environnement character varying) OWNER TO postgres;

--
-- Name: FUNCTION generer_cle_api(p_compte_id uuid, p_environnement character varying); Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON FUNCTION developpeurs.generer_cle_api(p_compte_id uuid, p_environnement character varying) IS 'Génère une clé API unique avec préfixe';


--
-- Name: proteger_logs_api(); Type: FUNCTION; Schema: developpeurs; Owner: postgres
--

CREATE FUNCTION developpeurs.proteger_logs_api() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: Les logs d''utilisation API ne peuvent pas être modifiés ou supprimés (TABLE IMMUABLE)';
    RETURN NULL;
END;
$$;


ALTER FUNCTION developpeurs.proteger_logs_api() OWNER TO postgres;

--
-- Name: enregistrer_historique_numero(); Type: FUNCTION; Schema: identite; Owner: ufaranga
--

CREATE FUNCTION identite.enregistrer_historique_numero() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                INSERT INTO identite.historique_numeros_telephone
                (numero_telephone_id, utilisateur_id, action, nouveau_statut)
                VALUES (NEW.id, NEW.utilisateur_id, 'AJOUT', NEW.statut);
            ELSIF TG_OP = 'UPDATE' THEN
                IF OLD.statut != NEW.statut THEN
                    INSERT INTO identite.historique_numeros_telephone
                    (numero_telephone_id, utilisateur_id, action, ancien_statut, nouveau_statut)
                    VALUES (NEW.id, NEW.utilisateur_id, 'MODIFICATION', OLD.statut, NEW.statut);
                END IF;
            END IF;
            RETURN NEW;
        END;
        $$;


ALTER FUNCTION identite.enregistrer_historique_numero() OWNER TO ufaranga;

--
-- Name: proteger_grand_livre(); Type: FUNCTION; Schema: transaction; Owner: postgres
--

CREATE FUNCTION transaction.proteger_grand_livre() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    RAISE EXCEPTION 'INTERDIT: Le grand livre comptable ne peut pas être modifié ou supprimé (TABLE IMMUABLE)';
    RETURN NULL;
END;
$$;


ALTER FUNCTION transaction.proteger_grand_livre() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: historique_modifications; Type: TABLE; Schema: audit; Owner: postgres
--

CREATE TABLE audit.historique_modifications (
    id bigint NOT NULL,
    nom_table character varying(100) NOT NULL,
    nom_schema character varying(50) NOT NULL,
    id_enregistrement character varying(100) NOT NULL,
    operation character varying(10) NOT NULL,
    utilisateur_id uuid,
    donnees_avant jsonb,
    donnees_apres jsonb,
    champs_modifies text[],
    raison_modification text,
    id_requete uuid,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT historique_modifications_operation_check CHECK (((operation)::text = ANY ((ARRAY['INSERT'::character varying, 'UPDATE'::character varying, 'DELETE'::character varying])::text[])))
);


ALTER TABLE audit.historique_modifications OWNER TO postgres;

--
-- Name: TABLE historique_modifications; Type: COMMENT; Schema: audit; Owner: postgres
--

COMMENT ON TABLE audit.historique_modifications IS 'Historique des modifications - TABLE IMMUABLE';


--
-- Name: historique_modifications_id_seq; Type: SEQUENCE; Schema: audit; Owner: postgres
--

CREATE SEQUENCE audit.historique_modifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE audit.historique_modifications_id_seq OWNER TO postgres;

--
-- Name: historique_modifications_id_seq; Type: SEQUENCE OWNED BY; Schema: audit; Owner: postgres
--

ALTER SEQUENCE audit.historique_modifications_id_seq OWNED BY audit.historique_modifications.id;


--
-- Name: journaux_evenements; Type: TABLE; Schema: audit; Owner: postgres
--

CREATE TABLE audit.journaux_evenements (
    id bigint NOT NULL,
    id_requete uuid NOT NULL,
    id_correlation uuid,
    utilisateur_id uuid,
    session_id uuid,
    categorie_evenement character varying(50) NOT NULL,
    action character varying(100) NOT NULL,
    type_ressource character varying(50),
    id_ressource character varying(100),
    description text NOT NULL,
    resultat character varying(20),
    nom_service character varying(50),
    nom_module character varying(100),
    nom_fonction character varying(100),
    point_terminaison character varying(255),
    methode_http character varying(10),
    statut_http integer,
    temps_execution_ms integer,
    adresse_ip character varying(45),
    agent_utilisateur text,
    id_appareil character varying(255),
    pays character varying(2),
    ville character varying(100),
    corps_requete jsonb,
    corps_reponse jsonb,
    code_erreur character varying(50),
    message_erreur text,
    trace_erreur text,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_evenement timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT journaux_evenements_categorie_evenement_check CHECK (((categorie_evenement)::text = ANY ((ARRAY['AUTHENTIFICATION'::character varying, 'AUTORISATION'::character varying, 'TRANSACTION_FINANCIERE'::character varying, 'MODIFICATION_DONNEES'::character varying, 'CONSULTATION_DONNEES'::character varying, 'CONFIGURATION_SYSTEME'::character varying, 'SECURITE'::character varying, 'ERREUR'::character varying, 'ALERTE'::character varying, 'SYNCHRONISATION_BANCAIRE'::character varying, 'NOTIFICATION'::character varying, 'KYC_COMPLIANCE'::character varying])::text[]))),
    CONSTRAINT journaux_evenements_resultat_check CHECK (((resultat)::text = ANY ((ARRAY['SUCCES'::character varying, 'ECHEC'::character varying, 'PARTIEL'::character varying, 'EN_COURS'::character varying])::text[])))
);


ALTER TABLE audit.journaux_evenements OWNER TO postgres;

--
-- Name: TABLE journaux_evenements; Type: COMMENT; Schema: audit; Owner: postgres
--

COMMENT ON TABLE audit.journaux_evenements IS 'Journal COMPLET des événements - TABLE IMMUABLE';


--
-- Name: journaux_evenements_id_seq; Type: SEQUENCE; Schema: audit; Owner: postgres
--

CREATE SEQUENCE audit.journaux_evenements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE audit.journaux_evenements_id_seq OWNER TO postgres;

--
-- Name: journaux_evenements_id_seq; Type: SEQUENCE OWNED BY; Schema: audit; Owner: postgres
--

ALTER SEQUENCE audit.journaux_evenements_id_seq OWNED BY audit.journaux_evenements.id;


--
-- Name: sessions_utilisateurs; Type: TABLE; Schema: audit; Owner: postgres
--

CREATE TABLE audit.sessions_utilisateurs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    cle_session character varying(255) NOT NULL,
    jeton_rafraichissement text,
    adresse_ip character varying(45) NOT NULL,
    agent_utilisateur text,
    type_appareil character varying(20),
    id_appareil character varying(255),
    empreinte_appareil character varying(255),
    pays_connexion character varying(2),
    ville_connexion character varying(100),
    latitude numeric(10,8),
    longitude numeric(11,8),
    fournisseur_internet character varying(100),
    est_active boolean DEFAULT true,
    date_connexion timestamp with time zone DEFAULT now() NOT NULL,
    date_deconnexion timestamp with time zone,
    derniere_activite timestamp with time zone DEFAULT now() NOT NULL,
    date_expiration timestamp with time zone NOT NULL,
    duree_session_secondes integer,
    raison_deconnexion character varying(50),
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT sessions_utilisateurs_raison_deconnexion_check CHECK (((raison_deconnexion)::text = ANY ((ARRAY['UTILISATEUR'::character varying, 'EXPIRATION'::character varying, 'SYSTEME'::character varying, 'SECURITE'::character varying, 'FORCEE'::character varying])::text[]))),
    CONSTRAINT sessions_utilisateurs_type_appareil_check CHECK (((type_appareil)::text = ANY ((ARRAY['MOBILE'::character varying, 'WEB'::character varying, 'TABLETTE'::character varying, 'API'::character varying])::text[])))
);


ALTER TABLE audit.sessions_utilisateurs OWNER TO postgres;

--
-- Name: TABLE sessions_utilisateurs; Type: COMMENT; Schema: audit; Owner: postgres
--

COMMENT ON TABLE audit.sessions_utilisateurs IS 'Sessions utilisateurs';


--
-- Name: banques_partenaires; Type: TABLE; Schema: bancaire; Owner: postgres
--

CREATE TABLE bancaire.banques_partenaires (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    code_banque character varying(20) NOT NULL,
    nom_banque character varying(200) NOT NULL,
    code_swift character varying(11),
    code_bic character varying(11),
    pays character varying(2) DEFAULT 'BI'::character varying NOT NULL,
    adresse_siege text,
    telephone character varying(50),
    email character varying(255),
    site_web character varying(255),
    api_endpoint character varying(500),
    api_version character varying(20),
    cle_api_chiffree text,
    certificat_ssl text,
    supporte_temps_reel boolean DEFAULT false,
    delai_traitement_heures integer DEFAULT 24,
    frais_integration numeric(18,2) DEFAULT 0.00,
    est_active boolean DEFAULT true,
    date_partenariat date NOT NULL,
    date_fin_partenariat date,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE bancaire.banques_partenaires OWNER TO postgres;

--
-- Name: TABLE banques_partenaires; Type: COMMENT; Schema: bancaire; Owner: postgres
--

COMMENT ON TABLE bancaire.banques_partenaires IS 'Banques partenaires';


--
-- Name: comptes_bancaires_reels; Type: TABLE; Schema: bancaire; Owner: postgres
--

CREATE TABLE bancaire.comptes_bancaires_reels (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    banque_id uuid NOT NULL,
    numero_compte_bancaire character varying(50) NOT NULL,
    rib character varying(50),
    iban character varying(34),
    swift_bic character varying(11),
    type_compte character varying(30) NOT NULL,
    nom_titulaire character varying(200) NOT NULL,
    prenom_titulaire character varying(200),
    solde_reel numeric(18,2) DEFAULT 0.00 NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying NOT NULL,
    derniere_synchronisation timestamp with time zone,
    frequence_synchronisation_minutes integer DEFAULT 5,
    erreur_derniere_sync text,
    est_compte_principal boolean DEFAULT false,
    statut character varying(20) DEFAULT 'ACTIF'::character varying,
    compte_verifie boolean DEFAULT false,
    date_verification timestamp with time zone,
    methode_verification character varying(50),
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    cree_par uuid,
    modifie_par uuid,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT comptes_bancaires_reels_statut_check CHECK (((statut)::text = ANY ((ARRAY['ACTIF'::character varying, 'SUSPENDU'::character varying, 'FERME'::character varying, 'EN_VERIFICATION'::character varying])::text[]))),
    CONSTRAINT comptes_bancaires_reels_type_compte_check CHECK (((type_compte)::text = ANY ((ARRAY['COMPTE_COURANT'::character varying, 'COMPTE_EPARGNE'::character varying, 'COMPTE_DEPOT'::character varying, 'COMPTE_PROFESSIONNEL'::character varying])::text[])))
);


ALTER TABLE bancaire.comptes_bancaires_reels OWNER TO postgres;

--
-- Name: TABLE comptes_bancaires_reels; Type: COMMENT; Schema: bancaire; Owner: postgres
--

COMMENT ON TABLE bancaire.comptes_bancaires_reels IS 'Comptes bancaires réels des utilisateurs';


--
-- Name: mouvements_bancaires_reels; Type: TABLE; Schema: bancaire; Owner: postgres
--

CREATE TABLE bancaire.mouvements_bancaires_reels (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    compte_bancaire_id uuid NOT NULL,
    reference_banque character varying(100) NOT NULL,
    reference_externe character varying(100),
    type_mouvement character varying(30) NOT NULL,
    montant numeric(18,2) NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying NOT NULL,
    solde_avant numeric(18,2) NOT NULL,
    solde_apres numeric(18,2) NOT NULL,
    libelle text NOT NULL,
    description_detaillee text,
    compte_contrepartie character varying(50),
    nom_contrepartie character varying(200),
    banque_contrepartie character varying(100),
    date_operation date NOT NULL,
    date_valeur date NOT NULL,
    heure_operation time without time zone,
    statut character varying(20) DEFAULT 'COMPLETE'::character varying,
    date_importation timestamp with time zone DEFAULT now() NOT NULL,
    importe_par character varying(50) DEFAULT 'SYSTEME'::character varying,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT mouvements_bancaires_reels_montant_check CHECK ((montant <> (0)::numeric)),
    CONSTRAINT mouvements_bancaires_reels_statut_check CHECK (((statut)::text = ANY ((ARRAY['COMPLETE'::character varying, 'EN_ATTENTE'::character varying, 'ANNULE'::character varying, 'REJETE'::character varying])::text[]))),
    CONSTRAINT mouvements_bancaires_reels_type_mouvement_check CHECK (((type_mouvement)::text = ANY ((ARRAY['CREDIT'::character varying, 'DEBIT'::character varying, 'FRAIS'::character varying, 'INTERET'::character varying, 'VIREMENT'::character varying, 'PRELEVEMENT'::character varying, 'CHEQUE'::character varying, 'CARTE'::character varying])::text[])))
);


ALTER TABLE bancaire.mouvements_bancaires_reels OWNER TO postgres;

--
-- Name: TABLE mouvements_bancaires_reels; Type: COMMENT; Schema: bancaire; Owner: postgres
--

COMMENT ON TABLE bancaire.mouvements_bancaires_reels IS 'Mouvements bancaires réels - table immuable';


--
-- Name: commissions; Type: TABLE; Schema: commission; Owner: postgres
--

CREATE TABLE commission.commissions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    transaction_id uuid NOT NULL,
    beneficiaire_id uuid,
    type_beneficiaire character varying(20),
    grille_commission_id uuid,
    type_commission character varying(50) NOT NULL,
    montant_commission numeric(18,2) NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying,
    base_calcul numeric(18,2),
    pourcentage_applique numeric(5,2),
    montant_fixe_applique numeric(18,2),
    statut_paiement character varying(20) DEFAULT 'EN_ATTENTE'::character varying,
    date_paiement timestamp with time zone,
    reference_paiement character varying(100),
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT commissions_montant_commission_check CHECK ((montant_commission >= (0)::numeric)),
    CONSTRAINT commissions_statut_paiement_check CHECK (((statut_paiement)::text = ANY ((ARRAY['EN_ATTENTE'::character varying, 'PAYEE'::character varying, 'SUSPENDUE'::character varying, 'ANNULEE'::character varying])::text[]))),
    CONSTRAINT commissions_type_beneficiaire_check CHECK (((type_beneficiaire)::text = ANY ((ARRAY['AGENT'::character varying, 'MARCHAND'::character varying, 'PARRAIN'::character varying, 'PLATEFORME'::character varying])::text[])))
);


ALTER TABLE commission.commissions OWNER TO postgres;

--
-- Name: TABLE commissions; Type: COMMENT; Schema: commission; Owner: postgres
--

COMMENT ON TABLE commission.commissions IS 'Commissions calculées et payées';


--
-- Name: grilles_commissions; Type: TABLE; Schema: commission; Owner: postgres
--

CREATE TABLE commission.grilles_commissions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    type_transaction character varying(30) NOT NULL,
    type_utilisateur character varying(20),
    niveau_kyc integer,
    montant_min numeric(18,2) DEFAULT 0.00,
    montant_max numeric(18,2),
    type_commission character varying(20) NOT NULL,
    montant_fixe numeric(18,2) DEFAULT 0.00,
    pourcentage numeric(5,2) DEFAULT 0.00,
    commission_min numeric(18,2),
    commission_max numeric(18,2),
    priorite integer DEFAULT 0,
    date_debut_validite date DEFAULT CURRENT_DATE NOT NULL,
    date_fin_validite date,
    est_active boolean DEFAULT true,
    description text,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    cree_par uuid,
    modifie_par uuid,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT grilles_commissions_niveau_kyc_check CHECK (((niveau_kyc >= 0) AND (niveau_kyc <= 3))),
    CONSTRAINT grilles_commissions_type_commission_check CHECK (((type_commission)::text = ANY ((ARRAY['FIXE'::character varying, 'POURCENTAGE'::character varying, 'MIXTE'::character varying])::text[])))
);


ALTER TABLE commission.grilles_commissions OWNER TO postgres;

--
-- Name: TABLE grilles_commissions; Type: COMMENT; Schema: commission; Owner: postgres
--

COMMENT ON TABLE commission.grilles_commissions IS 'Grilles de tarification des commissions';


--
-- Name: documents_kyc; Type: TABLE; Schema: compliance; Owner: postgres
--

CREATE TABLE compliance.documents_kyc (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    type_document character varying(50) NOT NULL,
    numero_document character varying(100),
    date_emission date,
    date_expiration date,
    autorite_emission character varying(200),
    pays_emission character varying(2) NOT NULL,
    url_fichier_recto character varying(500) NOT NULL,
    url_fichier_verso character varying(500),
    url_fichier_selfie character varying(500),
    hash_fichier_recto character varying(255),
    hash_fichier_verso character varying(255),
    statut_verification character varying(20) DEFAULT 'EN_ATTENTE'::character varying,
    verifie_par uuid,
    date_verification timestamp with time zone,
    methode_verification character varying(50),
    score_confiance integer,
    donnees_extraites jsonb,
    raison_rejet text,
    commentaire_verificateur text,
    alerte_expiration_envoyee boolean DEFAULT false,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT documents_kyc_score_confiance_check CHECK (((score_confiance >= 0) AND (score_confiance <= 100))),
    CONSTRAINT documents_kyc_statut_verification_check CHECK (((statut_verification)::text = ANY ((ARRAY['EN_ATTENTE'::character varying, 'EN_COURS'::character varying, 'APPROUVE'::character varying, 'REJETE'::character varying, 'EXPIRE'::character varying, 'SUSPENDU'::character varying])::text[]))),
    CONSTRAINT documents_kyc_type_document_check CHECK (((type_document)::text = ANY ((ARRAY['CNI'::character varying, 'PASSEPORT'::character varying, 'PERMIS_CONDUIRE'::character varying, 'CARTE_ELECTEUR'::character varying, 'SELFIE'::character varying, 'SELFIE_AVEC_DOCUMENT'::character varying, 'JUSTIFICATIF_DOMICILE'::character varying, 'ATTESTATION_RESIDENCE'::character varying, 'EXTRAIT_NAISSANCE'::character varying, 'AUTRE'::character varying])::text[])))
);


ALTER TABLE compliance.documents_kyc OWNER TO postgres;

--
-- Name: TABLE documents_kyc; Type: COMMENT; Schema: compliance; Owner: postgres
--

COMMENT ON TABLE compliance.documents_kyc IS 'Documents KYC';


--
-- Name: screening_aml; Type: TABLE; Schema: compliance; Owner: postgres
--

CREATE TABLE compliance.screening_aml (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    type_screening character varying(50) NOT NULL,
    resultat character varying(20) NOT NULL,
    score_risque integer,
    niveau_risque character varying(20),
    donnees_match jsonb,
    listes_matchees text[],
    action_requise boolean DEFAULT false,
    action_prise text,
    prise_en_charge_par uuid,
    date_prise_en_charge timestamp with time zone,
    fournisseur_screening character varying(100),
    reference_externe character varying(100),
    date_screening timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT screening_aml_niveau_risque_check CHECK (((niveau_risque)::text = ANY ((ARRAY['FAIBLE'::character varying, 'MOYEN'::character varying, 'ELEVE'::character varying, 'CRITIQUE'::character varying])::text[]))),
    CONSTRAINT screening_aml_resultat_check CHECK (((resultat)::text = ANY ((ARRAY['CLEAN'::character varying, 'MATCH_POSSIBLE'::character varying, 'MATCH_CONFIRME'::character varying, 'ERREUR'::character varying])::text[]))),
    CONSTRAINT screening_aml_score_risque_check CHECK (((score_risque >= 0) AND (score_risque <= 100))),
    CONSTRAINT screening_aml_type_screening_check CHECK (((type_screening)::text = ANY ((ARRAY['SANCTIONS'::character varying, 'PEP'::character varying, 'ADVERSE_MEDIA'::character varying, 'WATCHLIST'::character varying, 'COMPLET'::character varying])::text[])))
);


ALTER TABLE compliance.screening_aml OWNER TO postgres;

--
-- Name: TABLE screening_aml; Type: COMMENT; Schema: compliance; Owner: postgres
--

COMMENT ON TABLE compliance.screening_aml IS 'Screening AML - TABLE IMMUABLE';


--
-- Name: verifications_kyc; Type: TABLE; Schema: compliance; Owner: postgres
--

CREATE TABLE compliance.verifications_kyc (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    type_verification character varying(50) NOT NULL,
    resultat character varying(20) NOT NULL,
    score integer,
    fournisseur_verification character varying(100),
    reference_externe character varying(100),
    donnees_verification jsonb,
    raison_echec text,
    recommandations text,
    date_verification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT verifications_kyc_resultat_check CHECK (((resultat)::text = ANY ((ARRAY['SUCCES'::character varying, 'ECHEC'::character varying, 'PARTIEL'::character varying, 'EN_ATTENTE'::character varying])::text[]))),
    CONSTRAINT verifications_kyc_score_check CHECK (((score >= 0) AND (score <= 100))),
    CONSTRAINT verifications_kyc_type_verification_check CHECK (((type_verification)::text = ANY ((ARRAY['IDENTITE'::character varying, 'ADRESSE'::character varying, 'TELEPHONE'::character varying, 'EMAIL'::character varying, 'BIOMETRIE_FACIALE'::character varying, 'BIOMETRIE_EMPREINTE'::character varying, 'LIVENESS_CHECK'::character varying, 'VERIFICATION_BANCAIRE'::character varying, 'VERIFICATION_CREDIT'::character varying, 'AML_SCREENING'::character varying])::text[])))
);


ALTER TABLE compliance.verifications_kyc OWNER TO postgres;

--
-- Name: TABLE verifications_kyc; Type: COMMENT; Schema: compliance; Owner: postgres
--

COMMENT ON TABLE compliance.verifications_kyc IS 'Vérifications KYC - TABLE IMMUABLE';


--
-- Name: blacklist; Type: TABLE; Schema: configuration; Owner: postgres
--

CREATE TABLE configuration.blacklist (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    type_entree character varying(20) NOT NULL,
    valeur character varying(255) NOT NULL,
    raison text NOT NULL,
    categorie character varying(50),
    gravite character varying(20),
    ajoute_par uuid NOT NULL,
    date_debut timestamp with time zone DEFAULT now() NOT NULL,
    date_fin timestamp with time zone,
    est_permanent boolean DEFAULT false,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT blacklist_gravite_check CHECK (((gravite)::text = ANY ((ARRAY['FAIBLE'::character varying, 'MOYENNE'::character varying, 'ELEVEE'::character varying, 'CRITIQUE'::character varying])::text[]))),
    CONSTRAINT blacklist_type_entree_check CHECK (((type_entree)::text = ANY ((ARRAY['UTILISATEUR'::character varying, 'TELEPHONE'::character varying, 'EMAIL'::character varying, 'IP'::character varying, 'DEVICE'::character varying, 'COMPTE_BANCAIRE'::character varying])::text[])))
);


ALTER TABLE configuration.blacklist OWNER TO postgres;

--
-- Name: TABLE blacklist; Type: COMMENT; Schema: configuration; Owner: postgres
--

COMMENT ON TABLE configuration.blacklist IS 'Liste noire - Utilisateurs, IPs, appareils bloqués';


--
-- Name: limites_transactions; Type: TABLE; Schema: configuration; Owner: postgres
--

CREATE TABLE configuration.limites_transactions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    niveau_kyc integer NOT NULL,
    type_utilisateur character varying(20) NOT NULL,
    type_transaction character varying(30) NOT NULL,
    montant_min numeric(18,2) DEFAULT 0.00,
    montant_max_unitaire numeric(18,2) NOT NULL,
    montant_max_quotidien numeric(18,2) NOT NULL,
    montant_max_hebdomadaire numeric(18,2),
    montant_max_mensuel numeric(18,2) NOT NULL,
    montant_max_annuel numeric(18,2),
    nombre_max_quotidien integer,
    nombre_max_hebdomadaire integer,
    nombre_max_mensuel integer,
    est_active boolean DEFAULT true,
    date_debut_validite date DEFAULT CURRENT_DATE NOT NULL,
    date_fin_validite date,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT limites_transactions_niveau_kyc_check CHECK (((niveau_kyc >= 0) AND (niveau_kyc <= 3)))
);


ALTER TABLE configuration.limites_transactions OWNER TO postgres;

--
-- Name: TABLE limites_transactions; Type: COMMENT; Schema: configuration; Owner: postgres
--

COMMENT ON TABLE configuration.limites_transactions IS 'Limites de transaction par profil utilisateur';


--
-- Name: parametres_systeme; Type: TABLE; Schema: configuration; Owner: postgres
--

CREATE TABLE configuration.parametres_systeme (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    cle character varying(100) NOT NULL,
    valeur text NOT NULL,
    type_valeur character varying(20) DEFAULT 'STRING'::character varying,
    description text,
    categorie character varying(50),
    est_sensible boolean DEFAULT false,
    est_modifiable boolean DEFAULT true,
    modifie_par uuid,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT parametres_systeme_type_valeur_check CHECK (((type_valeur)::text = ANY ((ARRAY['STRING'::character varying, 'INTEGER'::character varying, 'DECIMAL'::character varying, 'BOOLEAN'::character varying, 'JSON'::character varying, 'ARRAY'::character varying])::text[])))
);


ALTER TABLE configuration.parametres_systeme OWNER TO postgres;

--
-- Name: TABLE parametres_systeme; Type: COMMENT; Schema: configuration; Owner: postgres
--

COMMENT ON TABLE configuration.parametres_systeme IS 'Configuration globale du système';


--
-- Name: taux_change; Type: TABLE; Schema: configuration; Owner: postgres
--

CREATE TABLE configuration.taux_change (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    devise_source character varying(3) NOT NULL,
    devise_cible character varying(3) NOT NULL,
    taux numeric(18,6) NOT NULL,
    source character varying(50),
    date_debut_validite timestamp with time zone DEFAULT now() NOT NULL,
    date_fin_validite timestamp with time zone,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT taux_change_taux_check CHECK ((taux > (0)::numeric))
);


ALTER TABLE configuration.taux_change OWNER TO postgres;

--
-- Name: TABLE taux_change; Type: COMMENT; Schema: configuration; Owner: postgres
--

COMMENT ON TABLE configuration.taux_change IS 'Taux de change avec historique';


--
-- Name: applications; Type: TABLE; Schema: developpeurs; Owner: postgres
--

CREATE TABLE developpeurs.applications (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    compte_developpeur_id uuid NOT NULL,
    nom_application character varying(200) NOT NULL,
    description text,
    url_application character varying(500),
    url_logo character varying(500),
    type_application character varying(30),
    urls_callback jsonb DEFAULT '[]'::jsonb,
    urls_webhook jsonb DEFAULT '[]'::jsonb,
    statut character varying(20) DEFAULT 'BROUILLON'::character varying,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT applications_statut_check CHECK (((statut)::text = ANY ((ARRAY['BROUILLON'::character varying, 'EN_REVISION'::character varying, 'APPROUVE'::character varying, 'REJETE'::character varying, 'SUSPENDU'::character varying])::text[]))),
    CONSTRAINT applications_type_application_check CHECK (((type_application)::text = ANY ((ARRAY['WEB'::character varying, 'MOBILE_IOS'::character varying, 'MOBILE_ANDROID'::character varying, 'BACKEND'::character varying, 'PLUGIN'::character varying, 'AUTRE'::character varying])::text[])))
);


ALTER TABLE developpeurs.applications OWNER TO postgres;

--
-- Name: TABLE applications; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON TABLE developpeurs.applications IS 'Applications enregistrées par les développeurs';


--
-- Name: cles_api; Type: TABLE; Schema: developpeurs; Owner: postgres
--

CREATE TABLE developpeurs.cles_api (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    compte_developpeur_id uuid NOT NULL,
    cle_api character varying(64) NOT NULL,
    prefixe_cle character varying(20) NOT NULL,
    hash_cle text NOT NULL,
    nom_cle character varying(100) NOT NULL,
    description text,
    environnement character varying(20) DEFAULT 'SANDBOX'::character varying,
    scopes jsonb DEFAULT '["public:read"]'::jsonb,
    adresses_ip_autorisees jsonb DEFAULT '[]'::jsonb,
    domaines_autorises jsonb DEFAULT '[]'::jsonb,
    limite_requetes_minute integer,
    limite_requetes_jour integer,
    est_active boolean DEFAULT true,
    date_expiration timestamp with time zone,
    derniere_utilisation timestamp with time zone,
    nombre_utilisations bigint DEFAULT 0,
    est_revoquee boolean DEFAULT false,
    date_revocation timestamp with time zone,
    revoquee_par uuid,
    raison_revocation text,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT cles_api_environnement_check CHECK (((environnement)::text = ANY ((ARRAY['SANDBOX'::character varying, 'PRODUCTION'::character varying])::text[])))
);


ALTER TABLE developpeurs.cles_api OWNER TO postgres;

--
-- Name: TABLE cles_api; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON TABLE developpeurs.cles_api IS 'Clés API pour authentification des développeurs';


--
-- Name: comptes_developpeurs; Type: TABLE; Schema: developpeurs; Owner: postgres
--

CREATE TABLE developpeurs.comptes_developpeurs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid,
    nom_entreprise character varying(200) NOT NULL,
    nom_contact character varying(200) NOT NULL,
    prenom_contact character varying(200),
    courriel_contact character varying(255) NOT NULL,
    telephone_contact character varying(20),
    pays character varying(2) DEFAULT 'BI'::character varying,
    ville character varying(100),
    adresse_complete text,
    type_compte character varying(30) DEFAULT 'SANDBOX'::character varying,
    statut character varying(20) DEFAULT 'EN_ATTENTE'::character varying,
    raison_statut text,
    courriel_verifie boolean DEFAULT false,
    date_verification_courriel timestamp with time zone,
    approuve_par uuid,
    date_approbation timestamp with time zone,
    quota_requetes_jour integer DEFAULT 1000,
    quota_requetes_mois integer DEFAULT 30000,
    limite_taux_par_minute integer DEFAULT 60,
    url_webhook character varying(500),
    secret_webhook character varying(255),
    notifications_email boolean DEFAULT true,
    notifications_sms boolean DEFAULT false,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    cree_par uuid,
    modifie_par uuid,
    CONSTRAINT comptes_developpeurs_statut_check CHECK (((statut)::text = ANY ((ARRAY['EN_ATTENTE'::character varying, 'ACTIF'::character varying, 'SUSPENDU'::character varying, 'BLOQUE'::character varying, 'FERME'::character varying])::text[]))),
    CONSTRAINT comptes_developpeurs_type_compte_check CHECK (((type_compte)::text = ANY ((ARRAY['SANDBOX'::character varying, 'PRODUCTION'::character varying, 'PARTENAIRE'::character varying, 'INTERNE'::character varying])::text[])))
);


ALTER TABLE developpeurs.comptes_developpeurs OWNER TO postgres;

--
-- Name: TABLE comptes_developpeurs; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON TABLE developpeurs.comptes_developpeurs IS 'Comptes développeurs pour accès API';


--
-- Name: logs_utilisation_api; Type: TABLE; Schema: developpeurs; Owner: postgres
--

CREATE TABLE developpeurs.logs_utilisation_api (
    id bigint NOT NULL,
    cle_api_id uuid NOT NULL,
    compte_developpeur_id uuid NOT NULL,
    methode_http character varying(10) NOT NULL,
    endpoint character varying(500) NOT NULL,
    chemin_complet text,
    parametres_query jsonb DEFAULT '{}'::jsonb,
    statut_http integer NOT NULL,
    temps_reponse_ms integer,
    taille_reponse_bytes integer,
    code_erreur character varying(50),
    message_erreur text,
    adresse_ip character varying(45) NOT NULL,
    user_agent text,
    referer text,
    pays character varying(2),
    date_requete timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE developpeurs.logs_utilisation_api OWNER TO postgres;

--
-- Name: TABLE logs_utilisation_api; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON TABLE developpeurs.logs_utilisation_api IS 'Logs d''utilisation des API - TABLE IMMUABLE';


--
-- Name: logs_utilisation_api_id_seq; Type: SEQUENCE; Schema: developpeurs; Owner: postgres
--

CREATE SEQUENCE developpeurs.logs_utilisation_api_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE developpeurs.logs_utilisation_api_id_seq OWNER TO postgres;

--
-- Name: logs_utilisation_api_id_seq; Type: SEQUENCE OWNED BY; Schema: developpeurs; Owner: postgres
--

ALTER SEQUENCE developpeurs.logs_utilisation_api_id_seq OWNED BY developpeurs.logs_utilisation_api.id;


--
-- Name: quotas_utilisation; Type: TABLE; Schema: developpeurs; Owner: postgres
--

CREATE TABLE developpeurs.quotas_utilisation (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    compte_developpeur_id uuid NOT NULL,
    cle_api_id uuid,
    date_periode date NOT NULL,
    type_periode character varying(10),
    nombre_requetes integer DEFAULT 0,
    nombre_requetes_succes integer DEFAULT 0,
    nombre_requetes_erreur integer DEFAULT 0,
    requetes_2xx integer DEFAULT 0,
    requetes_4xx integer DEFAULT 0,
    requetes_5xx integer DEFAULT 0,
    temps_reponse_moyen_ms integer,
    temps_reponse_max_ms integer,
    bande_passante_bytes bigint DEFAULT 0,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT quotas_utilisation_type_periode_check CHECK (((type_periode)::text = ANY ((ARRAY['JOUR'::character varying, 'MOIS'::character varying])::text[])))
);


ALTER TABLE developpeurs.quotas_utilisation OWNER TO postgres;

--
-- Name: TABLE quotas_utilisation; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON TABLE developpeurs.quotas_utilisation IS 'Statistiques et quotas d''utilisation API';


--
-- Name: vue_stats_developpeurs; Type: VIEW; Schema: developpeurs; Owner: postgres
--

CREATE VIEW developpeurs.vue_stats_developpeurs AS
SELECT
    NULL::uuid AS id,
    NULL::character varying(200) AS nom_entreprise,
    NULL::character varying(255) AS courriel_contact,
    NULL::character varying(30) AS type_compte,
    NULL::character varying(20) AS statut,
    NULL::bigint AS nombre_cles_api,
    NULL::bigint AS cles_actives,
    NULL::bigint AS nombre_applications,
    NULL::bigint AS total_requetes_mois,
    NULL::integer AS quota_requetes_mois,
    NULL::timestamp with time zone AS date_creation;


ALTER TABLE developpeurs.vue_stats_developpeurs OWNER TO postgres;

--
-- Name: VIEW vue_stats_developpeurs; Type: COMMENT; Schema: developpeurs; Owner: postgres
--

COMMENT ON VIEW developpeurs.vue_stats_developpeurs IS 'Statistiques agrégées par compte développeur';


--
-- Name: historique_numeros_telephone; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.historique_numeros_telephone (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    numero_telephone_id uuid NOT NULL,
    utilisateur_id uuid NOT NULL,
    action character varying(50) NOT NULL,
    ancien_statut character varying(20),
    nouveau_statut character varying(20),
    raison text,
    details jsonb DEFAULT '{}'::jsonb,
    date_action timestamp with time zone DEFAULT now(),
    effectue_par uuid,
    adresse_ip inet,
    user_agent text
);


ALTER TABLE identite.historique_numeros_telephone OWNER TO ufaranga;

--
-- Name: TABLE historique_numeros_telephone; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.historique_numeros_telephone IS 'Historique de tous les changements sur les numéros';


--
-- Name: limites_numeros_par_pays; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.limites_numeros_par_pays (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    pays_code_iso_2 character(2) NOT NULL,
    type_utilisateur character varying(20) NOT NULL,
    nombre_max_numeros integer DEFAULT 3 NOT NULL,
    nombre_max_numeros_verifies integer DEFAULT 2 NOT NULL,
    autorise_numeros_etrangers boolean DEFAULT false,
    pays_autorises_codes character(2)[],
    date_creation timestamp with time zone DEFAULT now(),
    date_modification timestamp with time zone DEFAULT now()
);


ALTER TABLE identite.limites_numeros_par_pays OWNER TO ufaranga;

--
-- Name: TABLE limites_numeros_par_pays; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.limites_numeros_par_pays IS 'Limites de numéros par pays et type d''utilisateur';


--
-- Name: niveaux_kyc; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.niveaux_kyc (
    niveau integer NOT NULL,
    libelle character varying(50) NOT NULL,
    description text DEFAULT ''::text,
    limite_transaction_journaliere numeric(15,2),
    limite_solde_maximum numeric(15,2),
    documents_requis jsonb DEFAULT '[]'::jsonb,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now(),
    date_modification timestamp with time zone DEFAULT now()
);


ALTER TABLE identite.niveaux_kyc OWNER TO ufaranga;

--
-- Name: TABLE niveaux_kyc; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.niveaux_kyc IS 'Niveaux de vérification KYC (Know Your Customer)';


--
-- Name: COLUMN niveaux_kyc.niveau; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.niveaux_kyc.niveau IS 'Niveau KYC (0=Non vérifié, 1=Basique, 2=Complet, 3=Premium)';


--
-- Name: COLUMN niveaux_kyc.limite_transaction_journaliere; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.niveaux_kyc.limite_transaction_journaliere IS 'Limite de transaction journalière en BIF';


--
-- Name: COLUMN niveaux_kyc.limite_solde_maximum; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.niveaux_kyc.limite_solde_maximum IS 'Solde maximum autorisé en BIF';


--
-- Name: COLUMN niveaux_kyc.documents_requis; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.niveaux_kyc.documents_requis IS 'Documents requis pour ce niveau (format JSON)';


--
-- Name: numeros_telephone; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.numeros_telephone (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    utilisateur_id uuid NOT NULL,
    pays_code_iso_2 character(2) NOT NULL,
    code_pays character varying(10) NOT NULL,
    numero_national character varying(20) NOT NULL,
    numero_complet character varying(30) NOT NULL,
    numero_formate character varying(30),
    type_numero character varying(20) DEFAULT 'MOBILE'::character varying,
    usage character varying(20) DEFAULT 'PERSONNEL'::character varying,
    est_principal boolean DEFAULT false,
    est_verifie boolean DEFAULT false,
    date_verification timestamp with time zone,
    methode_verification character varying(50),
    code_verification_hash character varying(255),
    tentatives_verification integer DEFAULT 0,
    derniere_tentative_verification timestamp with time zone,
    statut character varying(20) DEFAULT 'ACTIF'::character varying,
    raison_statut text,
    date_changement_statut timestamp with time zone,
    nombre_connexions_reussies integer DEFAULT 0,
    nombre_connexions_echouees integer DEFAULT 0,
    derniere_connexion timestamp with time zone,
    derniere_connexion_ip inet,
    operateur character varying(100),
    type_ligne character varying(20),
    date_creation timestamp with time zone DEFAULT now(),
    date_modification timestamp with time zone DEFAULT now(),
    date_suppression timestamp with time zone,
    cree_par uuid,
    modifie_par uuid,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT numeros_telephone_statut_check CHECK (((statut)::text = ANY ((ARRAY['ACTIF'::character varying, 'SUSPENDU'::character varying, 'BLOQUE'::character varying, 'SUPPRIME'::character varying])::text[]))),
    CONSTRAINT numeros_telephone_type_ligne_check CHECK (((type_ligne)::text = ANY ((ARRAY['PREPAYE'::character varying, 'POSTPAYE'::character varying, NULL::character varying])::text[]))),
    CONSTRAINT numeros_telephone_type_numero_check CHECK (((type_numero)::text = ANY ((ARRAY['MOBILE'::character varying, 'FIXE'::character varying, 'VOIP'::character varying])::text[]))),
    CONSTRAINT numeros_telephone_usage_check CHECK (((usage)::text = ANY ((ARRAY['PERSONNEL'::character varying, 'PROFESSIONNEL'::character varying, 'URGENCE'::character varying])::text[])))
);


ALTER TABLE identite.numeros_telephone OWNER TO ufaranga;

--
-- Name: TABLE numeros_telephone; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.numeros_telephone IS 'Numéros de téléphone des utilisateurs avec validation et limites';


--
-- Name: COLUMN numeros_telephone.pays_code_iso_2; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.numeros_telephone.pays_code_iso_2 IS 'Code ISO du pays (ex: BI, RW, CD)';


--
-- Name: COLUMN numeros_telephone.numero_complet; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.numeros_telephone.numero_complet IS 'Numéro au format international (ex: +25762046725)';


--
-- Name: COLUMN numeros_telephone.est_principal; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.numeros_telephone.est_principal IS 'Numéro principal de l''utilisateur (un seul par utilisateur)';


--
-- Name: profils_utilisateurs; Type: TABLE; Schema: identite; Owner: postgres
--

CREATE TABLE identite.profils_utilisateurs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    url_avatar character varying(500),
    url_photo_couverture character varying(500),
    biographie text,
    langue character varying(5) DEFAULT 'fr'::character varying,
    devise_preferee character varying(3) DEFAULT 'BIF'::character varying,
    fuseau_horaire character varying(50) DEFAULT 'Africa/Bujumbura'::character varying,
    format_date character varying(20) DEFAULT 'DD/MM/YYYY'::character varying,
    format_heure character varying(10) DEFAULT '24h'::character varying,
    notifications_courriel boolean DEFAULT true,
    notifications_sms boolean DEFAULT true,
    notifications_push boolean DEFAULT true,
    notifications_transactions boolean DEFAULT true,
    notifications_marketing boolean DEFAULT false,
    profil_public boolean DEFAULT false,
    afficher_telephone boolean DEFAULT false,
    afficher_courriel boolean DEFAULT false,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT profils_utilisateurs_langue_check CHECK (((langue)::text = ANY ((ARRAY['fr'::character varying, 'en'::character varying, 'sw'::character varying, 'rn'::character varying])::text[])))
);


ALTER TABLE identite.profils_utilisateurs OWNER TO postgres;

--
-- Name: TABLE profils_utilisateurs; Type: COMMENT; Schema: identite; Owner: postgres
--

COMMENT ON TABLE identite.profils_utilisateurs IS 'Profils et préférences des utilisateurs';


--
-- Name: statuts_utilisateurs; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.statuts_utilisateurs (
    code character varying(20) NOT NULL,
    libelle character varying(100) NOT NULL,
    description text DEFAULT ''::text,
    couleur character varying(7) DEFAULT '#000000'::character varying,
    permet_connexion boolean DEFAULT true,
    permet_transactions boolean DEFAULT true,
    ordre_affichage integer DEFAULT 0,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now(),
    date_modification timestamp with time zone DEFAULT now()
);


ALTER TABLE identite.statuts_utilisateurs OWNER TO ufaranga;

--
-- Name: TABLE statuts_utilisateurs; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.statuts_utilisateurs IS 'Statuts des comptes utilisateurs';


--
-- Name: COLUMN statuts_utilisateurs.code; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.statuts_utilisateurs.code IS 'Code unique du statut (ACTIF, SUSPENDU, BLOQUE, etc.)';


--
-- Name: COLUMN statuts_utilisateurs.couleur; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.statuts_utilisateurs.couleur IS 'Couleur hexadécimale pour l''affichage (#28a745)';


--
-- Name: COLUMN statuts_utilisateurs.permet_connexion; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.statuts_utilisateurs.permet_connexion IS 'Autorise ou non la connexion utilisateur';


--
-- Name: COLUMN statuts_utilisateurs.permet_transactions; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.statuts_utilisateurs.permet_transactions IS 'Autorise ou non les transactions';


--
-- Name: types_utilisateurs; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.types_utilisateurs (
    code character varying(20) NOT NULL,
    libelle character varying(100) NOT NULL,
    description text DEFAULT ''::text,
    ordre_affichage integer DEFAULT 0,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now(),
    date_modification timestamp with time zone DEFAULT now()
);


ALTER TABLE identite.types_utilisateurs OWNER TO ufaranga;

--
-- Name: TABLE types_utilisateurs; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.types_utilisateurs IS 'Types d''utilisateurs de la plateforme';


--
-- Name: COLUMN types_utilisateurs.code; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.types_utilisateurs.code IS 'Code unique du type (CLIENT, AGENT, ADMIN, etc.)';


--
-- Name: COLUMN types_utilisateurs.libelle; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.types_utilisateurs.libelle IS 'Libellé affiché';


--
-- Name: COLUMN types_utilisateurs.ordre_affichage; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.types_utilisateurs.ordre_affichage IS 'Ordre d''affichage dans les listes';


--
-- Name: utilisateurs; Type: TABLE; Schema: identite; Owner: ufaranga
--

CREATE TABLE identite.utilisateurs (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    courriel character varying(255) NOT NULL,
    numero_telephone character varying(20) NOT NULL,
    hash_mot_de_passe character varying(255) NOT NULL,
    prenom character varying(100) NOT NULL,
    nom_famille character varying(100) NOT NULL,
    date_naissance date NOT NULL,
    lieu_naissance character varying(100),
    nationalite character varying(2) DEFAULT 'BI'::character varying,
    pays_residence character varying(2) DEFAULT 'BI'::character varying NOT NULL,
    province character varying(100),
    ville character varying(100),
    commune character varying(100),
    quartier character varying(100),
    avenue character varying(100),
    numero_maison character varying(50),
    adresse_complete text,
    code_postal character varying(20),
    telephone_verifie boolean DEFAULT false,
    telephone_verifie_le timestamp with time zone,
    courriel_verifie boolean DEFAULT false,
    courriel_verifie_le timestamp with time zone,
    date_validation_kyc timestamp with time zone,
    validateur_kyc_id uuid,
    raison_statut text,
    nombre_tentatives_connexion integer DEFAULT 0,
    bloque_jusqua timestamp with time zone,
    double_auth_activee boolean DEFAULT false,
    secret_2fa character varying(255),
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    derniere_connexion timestamp with time zone,
    derniere_modification_mdp timestamp with time zone,
    cree_par uuid,
    modifie_par uuid,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    is_superuser boolean DEFAULT false NOT NULL,
    is_staff boolean DEFAULT false NOT NULL,
    pays_id uuid,
    province_id uuid,
    district_id uuid,
    quartier_id uuid,
    point_de_service_id uuid,
    type_utilisateur character varying(20) DEFAULT 'CLIENT'::character varying NOT NULL,
    niveau_kyc integer DEFAULT 0 NOT NULL,
    statut character varying(20) DEFAULT 'ACTIF'::character varying NOT NULL
);


ALTER TABLE identite.utilisateurs OWNER TO ufaranga;

--
-- Name: TABLE utilisateurs; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON TABLE identite.utilisateurs IS 'Table principale des utilisateurs';


--
-- Name: COLUMN utilisateurs.pays_id; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.pays_id IS 'Référence localisation : pays de résidence';


--
-- Name: COLUMN utilisateurs.province_id; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.province_id IS 'Référence localisation : province / région';


--
-- Name: COLUMN utilisateurs.district_id; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.district_id IS 'Référence localisation : district / ville';


--
-- Name: COLUMN utilisateurs.quartier_id; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.quartier_id IS 'Référence localisation : quartier / zone';


--
-- Name: COLUMN utilisateurs.point_de_service_id; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.point_de_service_id IS 'Référence localisation : point de service (ex. agent d’attachement)';


--
-- Name: COLUMN utilisateurs.type_utilisateur; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.type_utilisateur IS 'Type d''utilisateur (FK vers types_utilisateurs)';


--
-- Name: COLUMN utilisateurs.niveau_kyc; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.niveau_kyc IS 'Niveau de vérification KYC (FK vers niveaux_kyc)';


--
-- Name: COLUMN utilisateurs.statut; Type: COMMENT; Schema: identite; Owner: ufaranga
--

COMMENT ON COLUMN identite.utilisateurs.statut IS 'Statut du compte (FK vers statuts_utilisateurs)';


--
-- Name: districts; Type: TABLE; Schema: localisation; Owner: postgres
--

CREATE TABLE localisation.districts (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    province_id uuid NOT NULL,
    code character varying(20) NOT NULL,
    nom character varying(100) NOT NULL,
    latitude_centre numeric(10,7),
    longitude_centre numeric(10,7),
    autorise_systeme boolean DEFAULT true,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE localisation.districts OWNER TO postgres;

--
-- Name: TABLE districts; Type: COMMENT; Schema: localisation; Owner: postgres
--

COMMENT ON TABLE localisation.districts IS 'Villes / Districts - niveau 3';


--
-- Name: pays; Type: TABLE; Schema: localisation; Owner: postgres
--

CREATE TABLE localisation.pays (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    code_iso_2 character(2) NOT NULL,
    code_iso_3 character(3),
    nom character varying(100) NOT NULL,
    nom_anglais character varying(100),
    latitude_centre numeric(10,7),
    longitude_centre numeric(10,7),
    autorise_systeme boolean DEFAULT true,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    continent character varying(50),
    sous_region character varying(100)
);


ALTER TABLE localisation.pays OWNER TO postgres;

--
-- Name: TABLE pays; Type: COMMENT; Schema: localisation; Owner: postgres
--

COMMENT ON TABLE localisation.pays IS 'Pays - niveau 1 de la hiérarchie géographique';


--
-- Name: points_de_service; Type: TABLE; Schema: localisation; Owner: postgres
--

CREATE TABLE localisation.points_de_service (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    quartier_id uuid NOT NULL,
    code character varying(30) NOT NULL,
    nom character varying(100) NOT NULL,
    type_point character varying(20) DEFAULT 'AGENT'::character varying,
    agent_utilisateur_id uuid,
    latitude numeric(10,7),
    longitude numeric(10,7),
    adresse_complementaire text,
    autorise_systeme boolean DEFAULT true,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT points_de_service_type_point_check CHECK (((type_point)::text = ANY ((ARRAY['AGENT'::character varying, 'GUICHET'::character varying, 'PARTENAIRE'::character varying, 'AUTRE'::character varying])::text[])))
);


ALTER TABLE localisation.points_de_service OWNER TO postgres;

--
-- Name: TABLE points_de_service; Type: COMMENT; Schema: localisation; Owner: postgres
--

COMMENT ON TABLE localisation.points_de_service IS 'Points de service / Agents - niveau 5, relié à un utilisateur (agent)';


--
-- Name: provinces; Type: TABLE; Schema: localisation; Owner: postgres
--

CREATE TABLE localisation.provinces (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    pays_id uuid NOT NULL,
    code character varying(20) NOT NULL,
    nom character varying(100) NOT NULL,
    latitude_centre numeric(10,7),
    longitude_centre numeric(10,7),
    autorise_systeme boolean DEFAULT true,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE localisation.provinces OWNER TO postgres;

--
-- Name: TABLE provinces; Type: COMMENT; Schema: localisation; Owner: postgres
--

COMMENT ON TABLE localisation.provinces IS 'Régions / Provinces - niveau 2';


--
-- Name: quartiers; Type: TABLE; Schema: localisation; Owner: postgres
--

CREATE TABLE localisation.quartiers (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    district_id uuid NOT NULL,
    code character varying(20) NOT NULL,
    nom character varying(100) NOT NULL,
    latitude_centre numeric(10,7),
    longitude_centre numeric(10,7),
    autorise_systeme boolean DEFAULT true,
    est_actif boolean DEFAULT true,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE localisation.quartiers OWNER TO postgres;

--
-- Name: TABLE quartiers; Type: COMMENT; Schema: localisation; Owner: postgres
--

COMMENT ON TABLE localisation.quartiers IS 'Quartiers / Zones - niveau 4';


--
-- Name: notifications; Type: TABLE; Schema: notification; Owner: postgres
--

CREATE TABLE notification.notifications (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    type_notification character varying(50) NOT NULL,
    canal character varying(20) NOT NULL,
    destinataire character varying(255) NOT NULL,
    sujet character varying(255),
    message text NOT NULL,
    message_html text,
    template_id character varying(100),
    variables_template jsonb,
    priorite character varying(20) DEFAULT 'NORMALE'::character varying,
    statut_envoi character varying(20) DEFAULT 'EN_ATTENTE'::character varying,
    nombre_tentatives integer DEFAULT 0,
    max_tentatives integer DEFAULT 3,
    date_envoi timestamp with time zone,
    date_lecture timestamp with time zone,
    erreur_envoi text,
    code_erreur character varying(50),
    date_planification timestamp with time zone,
    fournisseur character varying(50),
    id_externe character varying(100),
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT notifications_priorite_check CHECK (((priorite)::text = ANY ((ARRAY['FAIBLE'::character varying, 'NORMALE'::character varying, 'HAUTE'::character varying, 'URGENTE'::character varying])::text[]))),
    CONSTRAINT notifications_statut_envoi_check CHECK (((statut_envoi)::text = ANY ((ARRAY['EN_ATTENTE'::character varying, 'ENVOYE'::character varying, 'ECHEC'::character varying, 'ANNULE'::character varying])::text[]))),
    CONSTRAINT notifications_type_notification_check CHECK (((type_notification)::text = ANY ((ARRAY['EMAIL'::character varying, 'SMS'::character varying, 'PUSH'::character varying, 'IN_APP'::character varying, 'WEBHOOK'::character varying])::text[])))
);


ALTER TABLE notification.notifications OWNER TO postgres;

--
-- Name: TABLE notifications; Type: COMMENT; Schema: notification; Owner: postgres
--

COMMENT ON TABLE notification.notifications IS 'File de notifications';


--
-- Name: portefeuilles_virtuels; Type: TABLE; Schema: portefeuille; Owner: postgres
--

CREATE TABLE portefeuille.portefeuilles_virtuels (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    utilisateur_id uuid NOT NULL,
    compte_bancaire_reel_id uuid NOT NULL,
    numero_portefeuille character varying(20) NOT NULL,
    type_portefeuille character varying(20) NOT NULL,
    nom_portefeuille character varying(100),
    description text,
    couleur_interface character varying(7),
    icone character varying(50),
    solde_affiche numeric(18,2) DEFAULT 0.00 NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying NOT NULL,
    solde_disponible numeric(18,2) DEFAULT 0.00 NOT NULL,
    solde_en_attente numeric(18,2) DEFAULT 0.00 NOT NULL,
    solde_bloque numeric(18,2) DEFAULT 0.00 NOT NULL,
    solde_float numeric(18,2) DEFAULT 0.00,
    solde_especes numeric(18,2) DEFAULT 0.00,
    limite_quotidienne numeric(18,2),
    limite_mensuelle numeric(18,2),
    limite_par_transaction numeric(18,2),
    derniere_synchronisation timestamp with time zone,
    en_cours_synchronisation boolean DEFAULT false,
    statut character varying(20) DEFAULT 'ACTIF'::character varying,
    raison_statut text,
    est_portefeuille_principal boolean DEFAULT false,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    cree_par uuid,
    modifie_par uuid,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT chk_solde_coherent CHECK ((solde_affiche = ((solde_disponible + solde_en_attente) + solde_bloque))),
    CONSTRAINT portefeuilles_virtuels_statut_check CHECK (((statut)::text = ANY ((ARRAY['ACTIF'::character varying, 'GELE'::character varying, 'SUSPENDU'::character varying, 'FERME'::character varying, 'EN_VERIFICATION'::character varying])::text[]))),
    CONSTRAINT portefeuilles_virtuels_type_portefeuille_check CHECK (((type_portefeuille)::text = ANY ((ARRAY['PERSONNEL'::character varying, 'PROFESSIONNEL'::character varying, 'MARCHAND'::character varying, 'AGENT'::character varying, 'EPARGNE'::character varying])::text[])))
);


ALTER TABLE portefeuille.portefeuilles_virtuels OWNER TO postgres;

--
-- Name: TABLE portefeuilles_virtuels; Type: COMMENT; Schema: portefeuille; Owner: postgres
--

COMMENT ON TABLE portefeuille.portefeuilles_virtuels IS 'Portefeuilles virtuels uFaranga';


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO ufaranga;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO ufaranga;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO ufaranga;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: currencies; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.currencies (
    code character varying(3) NOT NULL,
    name character varying(100) NOT NULL,
    symbol character varying(10) NOT NULL,
    decimal_places integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.currencies OWNER TO ufaranga;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO ufaranga;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO ufaranga;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO ufaranga;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO ufaranga;

--
-- Name: exchange_rates; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.exchange_rates (
    id bigint NOT NULL,
    rate numeric(19,8) NOT NULL,
    inverse_rate numeric(19,8) NOT NULL,
    source character varying(50) NOT NULL,
    valid_from timestamp with time zone NOT NULL,
    valid_until timestamp with time zone,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    from_currency_id character varying(3) NOT NULL,
    to_currency_id character varying(3) NOT NULL
);


ALTER TABLE public.exchange_rates OWNER TO ufaranga;

--
-- Name: exchange_rates_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.exchange_rates ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.exchange_rates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_accesstoken; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.oauth2_provider_accesstoken (
    id bigint NOT NULL,
    token character varying(255) NOT NULL,
    expires timestamp with time zone NOT NULL,
    scope text NOT NULL,
    application_id bigint,
    user_id uuid,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    source_refresh_token_id bigint,
    id_token_id bigint
);


ALTER TABLE public.oauth2_provider_accesstoken OWNER TO ufaranga;

--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.oauth2_provider_accesstoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oauth2_provider_accesstoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_application; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.oauth2_provider_application (
    id bigint NOT NULL,
    client_id character varying(100) NOT NULL,
    redirect_uris text NOT NULL,
    client_type character varying(32) NOT NULL,
    authorization_grant_type character varying(32) NOT NULL,
    client_secret character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    user_id uuid,
    skip_authorization boolean NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    algorithm character varying(5) NOT NULL,
    post_logout_redirect_uris text NOT NULL
);


ALTER TABLE public.oauth2_provider_application OWNER TO ufaranga;

--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.oauth2_provider_application ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oauth2_provider_application_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_grant; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.oauth2_provider_grant (
    id bigint NOT NULL,
    code character varying(255) NOT NULL,
    expires timestamp with time zone NOT NULL,
    redirect_uri text NOT NULL,
    scope text NOT NULL,
    application_id bigint NOT NULL,
    user_id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    code_challenge character varying(128) NOT NULL,
    code_challenge_method character varying(10) NOT NULL,
    nonce character varying(255) NOT NULL,
    claims text NOT NULL
);


ALTER TABLE public.oauth2_provider_grant OWNER TO ufaranga;

--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.oauth2_provider_grant ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oauth2_provider_grant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_idtoken; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.oauth2_provider_idtoken (
    id bigint NOT NULL,
    jti uuid NOT NULL,
    expires timestamp with time zone NOT NULL,
    scope text NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    application_id bigint,
    user_id uuid
);


ALTER TABLE public.oauth2_provider_idtoken OWNER TO ufaranga;

--
-- Name: oauth2_provider_idtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.oauth2_provider_idtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oauth2_provider_idtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_refreshtoken; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.oauth2_provider_refreshtoken (
    id bigint NOT NULL,
    token character varying(255) NOT NULL,
    access_token_id bigint,
    application_id bigint NOT NULL,
    user_id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    revoked timestamp with time zone
);


ALTER TABLE public.oauth2_provider_refreshtoken OWNER TO ufaranga;

--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.oauth2_provider_refreshtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oauth2_provider_refreshtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: token_blacklist_blacklistedtoken; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.token_blacklist_blacklistedtoken (
    id bigint NOT NULL,
    blacklisted_at timestamp with time zone NOT NULL,
    token_id bigint NOT NULL
);


ALTER TABLE public.token_blacklist_blacklistedtoken OWNER TO ufaranga;

--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.token_blacklist_blacklistedtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.token_blacklist_blacklistedtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: token_blacklist_outstandingtoken; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.token_blacklist_outstandingtoken (
    id bigint NOT NULL,
    token text NOT NULL,
    created_at timestamp with time zone,
    expires_at timestamp with time zone NOT NULL,
    user_id uuid,
    jti character varying(255) NOT NULL
);


ALTER TABLE public.token_blacklist_outstandingtoken OWNER TO ufaranga;

--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.token_blacklist_outstandingtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.token_blacklist_outstandingtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.user_profiles (
    id bigint NOT NULL,
    avatar character varying(100),
    bio text NOT NULL,
    language character varying(10) NOT NULL,
    currency character varying(3) NOT NULL,
    timezone character varying(50) NOT NULL,
    email_notifications boolean NOT NULL,
    sms_notifications boolean NOT NULL,
    push_notifications boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.user_profiles OWNER TO ufaranga;

--
-- Name: user_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.user_profiles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.user_sessions (
    id bigint NOT NULL,
    session_key character varying(40) NOT NULL,
    ip_address inet NOT NULL,
    user_agent text NOT NULL,
    device_info jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    last_activity timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.user_sessions OWNER TO ufaranga;

--
-- Name: user_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.user_sessions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.user_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.users (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    email character varying(254) NOT NULL,
    phone_number character varying(15),
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    date_of_birth date,
    country character varying(100) NOT NULL,
    city character varying(100) NOT NULL,
    address text NOT NULL,
    is_phone_verified boolean NOT NULL,
    is_email_verified boolean NOT NULL,
    kyc_level integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_login_ip inet
);


ALTER TABLE public.users OWNER TO ufaranga;

--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.users_groups (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_groups OWNER TO ufaranga;

--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.users_user_permissions (
    id bigint NOT NULL,
    user_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_permissions OWNER TO ufaranga;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: wallet_limits; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.wallet_limits (
    id bigint NOT NULL,
    limit_type character varying(20) NOT NULL,
    amount numeric(19,2) NOT NULL,
    used_amount numeric(19,2) NOT NULL,
    valid_from timestamp with time zone NOT NULL,
    valid_until timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    wallet_id uuid NOT NULL
);


ALTER TABLE public.wallet_limits OWNER TO ufaranga;

--
-- Name: wallet_limits_id_seq; Type: SEQUENCE; Schema: public; Owner: ufaranga
--

ALTER TABLE public.wallet_limits ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.wallet_limits_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: wallet_transactions; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.wallet_transactions (
    id uuid NOT NULL,
    transaction_type character varying(10) NOT NULL,
    amount numeric(19,2) NOT NULL,
    balance_before numeric(19,2) NOT NULL,
    balance_after numeric(19,2) NOT NULL,
    external_transaction_id uuid NOT NULL,
    reference character varying(100) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    wallet_id uuid NOT NULL
);


ALTER TABLE public.wallet_transactions OWNER TO ufaranga;

--
-- Name: wallets; Type: TABLE; Schema: public; Owner: ufaranga
--

CREATE TABLE public.wallets (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    wallet_type character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    balance numeric(19,2) NOT NULL,
    daily_limit numeric(19,2),
    monthly_limit numeric(19,2),
    name character varying(100) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_transaction_at timestamp with time zone,
    currency_id character varying(3) NOT NULL
);


ALTER TABLE public.wallets OWNER TO ufaranga;

--
-- Name: grand_livre_comptable; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.grand_livre_comptable (
    id bigint NOT NULL,
    transaction_id uuid NOT NULL,
    portefeuille_id uuid,
    compte_bancaire_id uuid,
    type_ecriture character varying(10) NOT NULL,
    montant numeric(18,2) NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying NOT NULL,
    solde_avant numeric(18,2) NOT NULL,
    solde_apres numeric(18,2) NOT NULL,
    libelle text NOT NULL,
    reference character varying(100),
    compte_contrepartie_id uuid,
    type_compte_contrepartie character varying(20),
    date_ecriture timestamp with time zone DEFAULT now() NOT NULL,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT chk_compte_specifie CHECK (((portefeuille_id IS NOT NULL) OR (compte_bancaire_id IS NOT NULL))),
    CONSTRAINT chk_solde_coherence CHECK (((((type_ecriture)::text = 'DEBIT'::text) AND (solde_apres = (solde_avant - montant))) OR (((type_ecriture)::text = 'CREDIT'::text) AND (solde_apres = (solde_avant + montant))))),
    CONSTRAINT grand_livre_comptable_montant_check CHECK ((montant > (0)::numeric)),
    CONSTRAINT grand_livre_comptable_type_compte_contrepartie_check CHECK (((type_compte_contrepartie)::text = ANY ((ARRAY['PORTEFEUILLE'::character varying, 'COMPTE_BANCAIRE'::character varying, 'AUTRE'::character varying])::text[]))),
    CONSTRAINT grand_livre_comptable_type_ecriture_check CHECK (((type_ecriture)::text = ANY ((ARRAY['DEBIT'::character varying, 'CREDIT'::character varying])::text[])))
);


ALTER TABLE transaction.grand_livre_comptable OWNER TO postgres;

--
-- Name: TABLE grand_livre_comptable; Type: COMMENT; Schema: transaction; Owner: postgres
--

COMMENT ON TABLE transaction.grand_livre_comptable IS 'Grand livre comptable - TABLE IMMUABLE';


--
-- Name: grand_livre_comptable_id_seq; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.grand_livre_comptable_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transaction.grand_livre_comptable_id_seq OWNER TO postgres;

--
-- Name: grand_livre_comptable_id_seq; Type: SEQUENCE OWNED BY; Schema: transaction; Owner: postgres
--

ALTER SEQUENCE transaction.grand_livre_comptable_id_seq OWNED BY transaction.grand_livre_comptable.id;


--
-- Name: transactions; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transactions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    reference_transaction character varying(50) NOT NULL,
    type_transaction character varying(30) NOT NULL,
    portefeuille_source_id uuid,
    portefeuille_destination_id uuid,
    utilisateur_source_id uuid,
    utilisateur_destination_id uuid,
    compte_bancaire_source_id uuid,
    compte_bancaire_dest_id uuid,
    montant numeric(18,2) NOT NULL,
    devise character varying(3) DEFAULT 'BIF'::character varying NOT NULL,
    montant_frais numeric(18,2) DEFAULT 0.00,
    montant_commission numeric(18,2) DEFAULT 0.00,
    montant_total numeric(18,2) NOT NULL,
    taux_change numeric(18,6),
    devise_destination character varying(3),
    montant_destination numeric(18,2),
    description text NOT NULL,
    description_detaillee text,
    motif character varying(200),
    statut character varying(20) DEFAULT 'EN_ATTENTE'::character varying,
    date_initiation timestamp with time zone DEFAULT now() NOT NULL,
    date_validation timestamp with time zone,
    date_debut_traitement timestamp with time zone,
    date_completion timestamp with time zone,
    date_echec timestamp with time zone,
    date_annulation timestamp with time zone,
    duree_traitement_ms integer,
    code_erreur character varying(50),
    raison_echec text,
    raison_annulation text,
    annulee_par uuid,
    score_fraude integer,
    raison_score_fraude text,
    flagged_fraude boolean DEFAULT false,
    date_flag_fraude timestamp with time zone,
    reference_banque character varying(100),
    reference_externe character varying(100),
    latitude numeric(10,8),
    longitude numeric(11,8),
    adresse_ip character varying(45),
    pays_origine character varying(2),
    ville_origine character varying(100),
    id_appareil character varying(255),
    type_appareil character varying(20),
    agent_utilisateur text,
    canal character varying(30) DEFAULT 'APP_MOBILE'::character varying,
    metadonnees jsonb DEFAULT '{}'::jsonb,
    date_creation timestamp with time zone DEFAULT now() NOT NULL,
    date_modification timestamp with time zone DEFAULT now() NOT NULL,
    cree_par uuid,
    modifie_par uuid,
    CONSTRAINT chk_montant_total CHECK ((montant_total = ((montant + montant_frais) + montant_commission))),
    CONSTRAINT transactions_canal_check CHECK (((canal)::text = ANY ((ARRAY['APP_MOBILE'::character varying, 'APP_WEB'::character varying, 'USSD'::character varying, 'API'::character varying, 'AGENT'::character varying, 'GUICHET'::character varying])::text[]))),
    CONSTRAINT transactions_montant_check CHECK ((montant > (0)::numeric)),
    CONSTRAINT transactions_montant_commission_check CHECK ((montant_commission >= (0)::numeric)),
    CONSTRAINT transactions_montant_frais_check CHECK ((montant_frais >= (0)::numeric)),
    CONSTRAINT transactions_score_fraude_check CHECK (((score_fraude >= 0) AND (score_fraude <= 100))),
    CONSTRAINT transactions_statut_check CHECK (((statut)::text = ANY ((ARRAY['EN_ATTENTE'::character varying, 'VALIDATION'::character varying, 'TRAITEMENT'::character varying, 'COMPLETE'::character varying, 'ECHEC'::character varying, 'ANNULEE'::character varying, 'REMBOURSEE'::character varying, 'SUSPENDUE'::character varying])::text[]))),
    CONSTRAINT transactions_type_appareil_check CHECK (((type_appareil)::text = ANY ((ARRAY['MOBILE'::character varying, 'WEB'::character varying, 'TABLETTE'::character varying, 'USSD'::character varying, 'API'::character varying])::text[]))),
    CONSTRAINT transactions_type_transaction_check CHECK (((type_transaction)::text = ANY ((ARRAY['P2P'::character varying, 'DEPOT'::character varying, 'RETRAIT'::character varying, 'PAIEMENT_MARCHAND'::character varying, 'PAIEMENT_FACTURE'::character varying, 'RECHARGE_TELEPHONIQUE'::character varying, 'VIREMENT_BANCAIRE'::character varying, 'TRANSFERT_INTERNATIONAL'::character varying, 'COMMISSION'::character varying, 'FRAIS'::character varying, 'REMBOURSEMENT'::character varying, 'AJUSTEMENT'::character varying, 'INTEREST'::character varying])::text[])))
);


ALTER TABLE transaction.transactions OWNER TO postgres;

--
-- Name: TABLE transactions; Type: COMMENT; Schema: transaction; Owner: postgres
--

COMMENT ON TABLE transaction.transactions IS 'Transactions financières';


--
-- Name: historique_modifications id; Type: DEFAULT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.historique_modifications ALTER COLUMN id SET DEFAULT nextval('audit.historique_modifications_id_seq'::regclass);


--
-- Name: journaux_evenements id; Type: DEFAULT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.journaux_evenements ALTER COLUMN id SET DEFAULT nextval('audit.journaux_evenements_id_seq'::regclass);


--
-- Name: logs_utilisation_api id; Type: DEFAULT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.logs_utilisation_api ALTER COLUMN id SET DEFAULT nextval('developpeurs.logs_utilisation_api_id_seq'::regclass);


--
-- Name: grand_livre_comptable id; Type: DEFAULT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.grand_livre_comptable ALTER COLUMN id SET DEFAULT nextval('transaction.grand_livre_comptable_id_seq'::regclass);


--
-- Name: historique_modifications historique_modifications_pkey; Type: CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.historique_modifications
    ADD CONSTRAINT historique_modifications_pkey PRIMARY KEY (id);


--
-- Name: journaux_evenements journaux_evenements_pkey; Type: CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.journaux_evenements
    ADD CONSTRAINT journaux_evenements_pkey PRIMARY KEY (id);


--
-- Name: sessions_utilisateurs sessions_utilisateurs_cle_session_key; Type: CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.sessions_utilisateurs
    ADD CONSTRAINT sessions_utilisateurs_cle_session_key UNIQUE (cle_session);


--
-- Name: sessions_utilisateurs sessions_utilisateurs_pkey; Type: CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.sessions_utilisateurs
    ADD CONSTRAINT sessions_utilisateurs_pkey PRIMARY KEY (id);


--
-- Name: banques_partenaires banques_partenaires_code_banque_key; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.banques_partenaires
    ADD CONSTRAINT banques_partenaires_code_banque_key UNIQUE (code_banque);


--
-- Name: banques_partenaires banques_partenaires_code_swift_key; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.banques_partenaires
    ADD CONSTRAINT banques_partenaires_code_swift_key UNIQUE (code_swift);


--
-- Name: banques_partenaires banques_partenaires_pkey; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.banques_partenaires
    ADD CONSTRAINT banques_partenaires_pkey PRIMARY KEY (id);


--
-- Name: comptes_bancaires_reels comptes_bancaires_reels_pkey; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.comptes_bancaires_reels
    ADD CONSTRAINT comptes_bancaires_reels_pkey PRIMARY KEY (id);


--
-- Name: mouvements_bancaires_reels mouvements_bancaires_reels_pkey; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.mouvements_bancaires_reels
    ADD CONSTRAINT mouvements_bancaires_reels_pkey PRIMARY KEY (id);


--
-- Name: mouvements_bancaires_reels mouvements_bancaires_reels_reference_banque_key; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.mouvements_bancaires_reels
    ADD CONSTRAINT mouvements_bancaires_reels_reference_banque_key UNIQUE (reference_banque);


--
-- Name: comptes_bancaires_reels unique_compte_utilisateur; Type: CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.comptes_bancaires_reels
    ADD CONSTRAINT unique_compte_utilisateur UNIQUE (utilisateur_id, numero_compte_bancaire);


--
-- Name: commissions commissions_pkey; Type: CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.commissions
    ADD CONSTRAINT commissions_pkey PRIMARY KEY (id);


--
-- Name: commissions commissions_transaction_id_key; Type: CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.commissions
    ADD CONSTRAINT commissions_transaction_id_key UNIQUE (transaction_id);


--
-- Name: grilles_commissions grilles_commissions_pkey; Type: CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.grilles_commissions
    ADD CONSTRAINT grilles_commissions_pkey PRIMARY KEY (id);


--
-- Name: documents_kyc documents_kyc_pkey; Type: CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.documents_kyc
    ADD CONSTRAINT documents_kyc_pkey PRIMARY KEY (id);


--
-- Name: screening_aml screening_aml_pkey; Type: CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.screening_aml
    ADD CONSTRAINT screening_aml_pkey PRIMARY KEY (id);


--
-- Name: verifications_kyc verifications_kyc_pkey; Type: CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.verifications_kyc
    ADD CONSTRAINT verifications_kyc_pkey PRIMARY KEY (id);


--
-- Name: blacklist blacklist_pkey; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (id);


--
-- Name: blacklist blacklist_type_entree_valeur_key; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.blacklist
    ADD CONSTRAINT blacklist_type_entree_valeur_key UNIQUE (type_entree, valeur);


--
-- Name: limites_transactions limites_transactions_niveau_kyc_type_utilisateur_type_trans_key; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.limites_transactions
    ADD CONSTRAINT limites_transactions_niveau_kyc_type_utilisateur_type_trans_key UNIQUE (niveau_kyc, type_utilisateur, type_transaction, date_debut_validite);


--
-- Name: limites_transactions limites_transactions_pkey; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.limites_transactions
    ADD CONSTRAINT limites_transactions_pkey PRIMARY KEY (id);


--
-- Name: parametres_systeme parametres_systeme_cle_key; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.parametres_systeme
    ADD CONSTRAINT parametres_systeme_cle_key UNIQUE (cle);


--
-- Name: parametres_systeme parametres_systeme_pkey; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.parametres_systeme
    ADD CONSTRAINT parametres_systeme_pkey PRIMARY KEY (id);


--
-- Name: taux_change taux_change_devise_source_devise_cible_date_debut_validite_key; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.taux_change
    ADD CONSTRAINT taux_change_devise_source_devise_cible_date_debut_validite_key UNIQUE (devise_source, devise_cible, date_debut_validite);


--
-- Name: taux_change taux_change_pkey; Type: CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.taux_change
    ADD CONSTRAINT taux_change_pkey PRIMARY KEY (id);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: cles_api cles_api_cle_api_key; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.cles_api
    ADD CONSTRAINT cles_api_cle_api_key UNIQUE (cle_api);


--
-- Name: cles_api cles_api_pkey; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.cles_api
    ADD CONSTRAINT cles_api_pkey PRIMARY KEY (id);


--
-- Name: comptes_developpeurs comptes_developpeurs_courriel_contact_key; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.comptes_developpeurs
    ADD CONSTRAINT comptes_developpeurs_courriel_contact_key UNIQUE (courriel_contact);


--
-- Name: comptes_developpeurs comptes_developpeurs_pkey; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.comptes_developpeurs
    ADD CONSTRAINT comptes_developpeurs_pkey PRIMARY KEY (id);


--
-- Name: logs_utilisation_api logs_utilisation_api_pkey; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.logs_utilisation_api
    ADD CONSTRAINT logs_utilisation_api_pkey PRIMARY KEY (id);


--
-- Name: quotas_utilisation quotas_utilisation_compte_developpeur_id_cle_api_id_date_pe_key; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.quotas_utilisation
    ADD CONSTRAINT quotas_utilisation_compte_developpeur_id_cle_api_id_date_pe_key UNIQUE (compte_developpeur_id, cle_api_id, date_periode, type_periode);


--
-- Name: quotas_utilisation quotas_utilisation_pkey; Type: CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.quotas_utilisation
    ADD CONSTRAINT quotas_utilisation_pkey PRIMARY KEY (id);


--
-- Name: historique_numeros_telephone historique_numeros_telephone_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.historique_numeros_telephone
    ADD CONSTRAINT historique_numeros_telephone_pkey PRIMARY KEY (id);


--
-- Name: limites_numeros_par_pays limites_numeros_par_pays_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.limites_numeros_par_pays
    ADD CONSTRAINT limites_numeros_par_pays_pkey PRIMARY KEY (id);


--
-- Name: niveaux_kyc niveaux_kyc_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.niveaux_kyc
    ADD CONSTRAINT niveaux_kyc_pkey PRIMARY KEY (niveau);


--
-- Name: numeros_telephone numeros_telephone_numero_complet_key; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.numeros_telephone
    ADD CONSTRAINT numeros_telephone_numero_complet_key UNIQUE (numero_complet);


--
-- Name: numeros_telephone numeros_telephone_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.numeros_telephone
    ADD CONSTRAINT numeros_telephone_pkey PRIMARY KEY (id);


--
-- Name: profils_utilisateurs profils_utilisateurs_pkey; Type: CONSTRAINT; Schema: identite; Owner: postgres
--

ALTER TABLE ONLY identite.profils_utilisateurs
    ADD CONSTRAINT profils_utilisateurs_pkey PRIMARY KEY (id);


--
-- Name: profils_utilisateurs profils_utilisateurs_utilisateur_id_key; Type: CONSTRAINT; Schema: identite; Owner: postgres
--

ALTER TABLE ONLY identite.profils_utilisateurs
    ADD CONSTRAINT profils_utilisateurs_utilisateur_id_key UNIQUE (utilisateur_id);


--
-- Name: statuts_utilisateurs statuts_utilisateurs_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.statuts_utilisateurs
    ADD CONSTRAINT statuts_utilisateurs_pkey PRIMARY KEY (code);


--
-- Name: types_utilisateurs types_utilisateurs_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.types_utilisateurs
    ADD CONSTRAINT types_utilisateurs_pkey PRIMARY KEY (code);


--
-- Name: limites_numeros_par_pays uq_limite_pays_type; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.limites_numeros_par_pays
    ADD CONSTRAINT uq_limite_pays_type UNIQUE (pays_code_iso_2, type_utilisateur);


--
-- Name: utilisateurs utilisateurs_courriel_key; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_courriel_key UNIQUE (courriel);


--
-- Name: utilisateurs utilisateurs_numero_telephone_key; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_numero_telephone_key UNIQUE (numero_telephone);


--
-- Name: utilisateurs utilisateurs_pkey; Type: CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_pkey PRIMARY KEY (id);


--
-- Name: districts districts_pkey; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.districts
    ADD CONSTRAINT districts_pkey PRIMARY KEY (id);


--
-- Name: districts districts_province_id_code_key; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.districts
    ADD CONSTRAINT districts_province_id_code_key UNIQUE (province_id, code);


--
-- Name: pays pays_code_iso_2_key; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.pays
    ADD CONSTRAINT pays_code_iso_2_key UNIQUE (code_iso_2);


--
-- Name: pays pays_pkey; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.pays
    ADD CONSTRAINT pays_pkey PRIMARY KEY (id);


--
-- Name: points_de_service points_de_service_pkey; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.points_de_service
    ADD CONSTRAINT points_de_service_pkey PRIMARY KEY (id);


--
-- Name: points_de_service points_de_service_quartier_id_code_key; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.points_de_service
    ADD CONSTRAINT points_de_service_quartier_id_code_key UNIQUE (quartier_id, code);


--
-- Name: provinces provinces_pays_id_code_key; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.provinces
    ADD CONSTRAINT provinces_pays_id_code_key UNIQUE (pays_id, code);


--
-- Name: provinces provinces_pkey; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.provinces
    ADD CONSTRAINT provinces_pkey PRIMARY KEY (id);


--
-- Name: quartiers quartiers_district_id_code_key; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.quartiers
    ADD CONSTRAINT quartiers_district_id_code_key UNIQUE (district_id, code);


--
-- Name: quartiers quartiers_pkey; Type: CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.quartiers
    ADD CONSTRAINT quartiers_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: notification; Owner: postgres
--

ALTER TABLE ONLY notification.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: portefeuilles_virtuels portefeuilles_virtuels_numero_portefeuille_key; Type: CONSTRAINT; Schema: portefeuille; Owner: postgres
--

ALTER TABLE ONLY portefeuille.portefeuilles_virtuels
    ADD CONSTRAINT portefeuilles_virtuels_numero_portefeuille_key UNIQUE (numero_portefeuille);


--
-- Name: portefeuilles_virtuels portefeuilles_virtuels_pkey; Type: CONSTRAINT; Schema: portefeuille; Owner: postgres
--

ALTER TABLE ONLY portefeuille.portefeuilles_virtuels
    ADD CONSTRAINT portefeuilles_virtuels_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: currencies currencies_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_pkey PRIMARY KEY (code);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: exchange_rates exchange_rates_from_currency_id_to_curr_02b3e686_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.exchange_rates
    ADD CONSTRAINT exchange_rates_from_currency_id_to_curr_02b3e686_uniq UNIQUE (from_currency_id, to_currency_id, valid_from);


--
-- Name: exchange_rates exchange_rates_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.exchange_rates
    ADD CONSTRAINT exchange_rates_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_id_token_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_id_token_id_key UNIQUE (id_token_id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_source_refresh_token_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_source_refresh_token_id_key UNIQUE (source_refresh_token_id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_token_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_token_key UNIQUE (token);


--
-- Name: oauth2_provider_application oauth2_provider_application_client_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_client_id_key UNIQUE (client_id);


--
-- Name: oauth2_provider_application oauth2_provider_application_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_grant oauth2_provider_grant_code_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_code_key UNIQUE (code);


--
-- Name: oauth2_provider_grant oauth2_provider_grant_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_jti_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_idtoken
    ADD CONSTRAINT oauth2_provider_idtoken_jti_key UNIQUE (jti);


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_idtoken
    ADD CONSTRAINT oauth2_provider_idtoken_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_access_token_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_access_token_id_key UNIQUE (access_token_id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq UNIQUE (token, revoked);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_token_id_key UNIQUE (token_id);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq UNIQUE (jti);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_key UNIQUE (user_id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_session_key_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_session_key_key UNIQUE (session_key);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_user_id_group_id_fc7788e8_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq UNIQUE (user_id, group_id);


--
-- Name: users users_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_number_key UNIQUE (phone_number);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_user_id_permission_id_3b86cbdf_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq UNIQUE (user_id, permission_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: wallet_limits wallet_limits_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallet_limits
    ADD CONSTRAINT wallet_limits_pkey PRIMARY KEY (id);


--
-- Name: wallet_limits wallet_limits_wallet_id_limit_type_valid_from_87aaad3d_uniq; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallet_limits
    ADD CONSTRAINT wallet_limits_wallet_id_limit_type_valid_from_87aaad3d_uniq UNIQUE (wallet_id, limit_type, valid_from);


--
-- Name: wallet_transactions wallet_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallet_transactions
    ADD CONSTRAINT wallet_transactions_pkey PRIMARY KEY (id);


--
-- Name: wallets wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_pkey PRIMARY KEY (id);


--
-- Name: grand_livre_comptable grand_livre_comptable_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.grand_livre_comptable
    ADD CONSTRAINT grand_livre_comptable_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_reference_transaction_key; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_reference_transaction_key UNIQUE (reference_transaction);


--
-- Name: idx_audit_evenements_action; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_action ON audit.journaux_evenements USING btree (action);


--
-- Name: idx_audit_evenements_categorie; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_categorie ON audit.journaux_evenements USING btree (categorie_evenement);


--
-- Name: idx_audit_evenements_date; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_date ON audit.journaux_evenements USING btree (date_evenement DESC);


--
-- Name: idx_audit_evenements_requete; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_requete ON audit.journaux_evenements USING btree (id_requete);


--
-- Name: idx_audit_evenements_resultat; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_resultat ON audit.journaux_evenements USING btree (resultat);


--
-- Name: idx_audit_evenements_session; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_session ON audit.journaux_evenements USING btree (session_id);


--
-- Name: idx_audit_evenements_utilisateur; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_evenements_utilisateur ON audit.journaux_evenements USING btree (utilisateur_id);


--
-- Name: idx_audit_historique_date; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_historique_date ON audit.historique_modifications USING btree (date_modification DESC);


--
-- Name: idx_audit_historique_enregistrement; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_historique_enregistrement ON audit.historique_modifications USING btree (id_enregistrement);


--
-- Name: idx_audit_historique_operation; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_historique_operation ON audit.historique_modifications USING btree (operation);


--
-- Name: idx_audit_historique_table; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_historique_table ON audit.historique_modifications USING btree (nom_schema, nom_table);


--
-- Name: idx_audit_historique_utilisateur; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_historique_utilisateur ON audit.historique_modifications USING btree (utilisateur_id);


--
-- Name: idx_audit_sessions_active; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_sessions_active ON audit.sessions_utilisateurs USING btree (est_active) WHERE (est_active = true);


--
-- Name: idx_audit_sessions_date_connexion; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_sessions_date_connexion ON audit.sessions_utilisateurs USING btree (date_connexion DESC);


--
-- Name: idx_audit_sessions_ip; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_sessions_ip ON audit.sessions_utilisateurs USING btree (adresse_ip);


--
-- Name: idx_audit_sessions_utilisateur; Type: INDEX; Schema: audit; Owner: postgres
--

CREATE INDEX idx_audit_sessions_utilisateur ON audit.sessions_utilisateurs USING btree (utilisateur_id);


--
-- Name: idx_banques_active; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_banques_active ON bancaire.banques_partenaires USING btree (est_active) WHERE (est_active = true);


--
-- Name: idx_banques_code; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_banques_code ON bancaire.banques_partenaires USING btree (code_banque);


--
-- Name: idx_banques_swift; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_banques_swift ON bancaire.banques_partenaires USING btree (code_swift);


--
-- Name: idx_comptes_banque; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_comptes_banque ON bancaire.comptes_bancaires_reels USING btree (banque_id);


--
-- Name: idx_comptes_numero; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_comptes_numero ON bancaire.comptes_bancaires_reels USING btree (numero_compte_bancaire);


--
-- Name: idx_comptes_utilisateur; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_comptes_utilisateur ON bancaire.comptes_bancaires_reels USING btree (utilisateur_id);


--
-- Name: idx_mouvements_compte; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_mouvements_compte ON bancaire.mouvements_bancaires_reels USING btree (compte_bancaire_id);


--
-- Name: idx_mouvements_date; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_mouvements_date ON bancaire.mouvements_bancaires_reels USING btree (date_operation DESC);


--
-- Name: idx_mouvements_reference; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_mouvements_reference ON bancaire.mouvements_bancaires_reels USING btree (reference_banque);


--
-- Name: idx_mouvements_type; Type: INDEX; Schema: bancaire; Owner: postgres
--

CREATE INDEX idx_mouvements_type ON bancaire.mouvements_bancaires_reels USING btree (type_mouvement);


--
-- Name: idx_commission_grilles_active; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commission_grilles_active ON commission.grilles_commissions USING btree (est_active) WHERE (est_active = true);


--
-- Name: idx_commission_grilles_type; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commission_grilles_type ON commission.grilles_commissions USING btree (type_transaction);


--
-- Name: idx_commission_grilles_validite; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commission_grilles_validite ON commission.grilles_commissions USING btree (date_debut_validite, date_fin_validite);


--
-- Name: idx_commissions_beneficiaire; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commissions_beneficiaire ON commission.commissions USING btree (beneficiaire_id);


--
-- Name: idx_commissions_date; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commissions_date ON commission.commissions USING btree (date_creation DESC);


--
-- Name: idx_commissions_statut; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commissions_statut ON commission.commissions USING btree (statut_paiement);


--
-- Name: idx_commissions_transaction; Type: INDEX; Schema: commission; Owner: postgres
--

CREATE INDEX idx_commissions_transaction ON commission.commissions USING btree (transaction_id);


--
-- Name: idx_compliance_aml_action; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_aml_action ON compliance.screening_aml USING btree (action_requise) WHERE (action_requise = true);


--
-- Name: idx_compliance_aml_date; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_aml_date ON compliance.screening_aml USING btree (date_screening DESC);


--
-- Name: idx_compliance_aml_niveau_risque; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_aml_niveau_risque ON compliance.screening_aml USING btree (niveau_risque);


--
-- Name: idx_compliance_aml_resultat; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_aml_resultat ON compliance.screening_aml USING btree (resultat);


--
-- Name: idx_compliance_aml_utilisateur; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_aml_utilisateur ON compliance.screening_aml USING btree (utilisateur_id);


--
-- Name: idx_compliance_documents_expiration; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_documents_expiration ON compliance.documents_kyc USING btree (date_expiration) WHERE (date_expiration IS NOT NULL);


--
-- Name: idx_compliance_documents_statut; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_documents_statut ON compliance.documents_kyc USING btree (statut_verification);


--
-- Name: idx_compliance_documents_type; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_documents_type ON compliance.documents_kyc USING btree (type_document);


--
-- Name: idx_compliance_documents_utilisateur; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_documents_utilisateur ON compliance.documents_kyc USING btree (utilisateur_id);


--
-- Name: idx_compliance_verif_date; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_verif_date ON compliance.verifications_kyc USING btree (date_verification DESC);


--
-- Name: idx_compliance_verif_resultat; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_verif_resultat ON compliance.verifications_kyc USING btree (resultat);


--
-- Name: idx_compliance_verif_type; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_verif_type ON compliance.verifications_kyc USING btree (type_verification);


--
-- Name: idx_compliance_verif_utilisateur; Type: INDEX; Schema: compliance; Owner: postgres
--

CREATE INDEX idx_compliance_verif_utilisateur ON compliance.verifications_kyc USING btree (utilisateur_id);


--
-- Name: idx_blacklist_actif; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_blacklist_actif ON configuration.blacklist USING btree (est_actif) WHERE (est_actif = true);


--
-- Name: idx_blacklist_gravite; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_blacklist_gravite ON configuration.blacklist USING btree (gravite);


--
-- Name: idx_blacklist_type; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_blacklist_type ON configuration.blacklist USING btree (type_entree);


--
-- Name: idx_blacklist_valeur; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_blacklist_valeur ON configuration.blacklist USING btree (valeur);


--
-- Name: idx_limites_active; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_limites_active ON configuration.limites_transactions USING btree (est_active) WHERE (est_active = true);


--
-- Name: idx_limites_kyc; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_limites_kyc ON configuration.limites_transactions USING btree (niveau_kyc);


--
-- Name: idx_limites_type_user; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_limites_type_user ON configuration.limites_transactions USING btree (type_utilisateur);


--
-- Name: idx_parametres_categorie; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_parametres_categorie ON configuration.parametres_systeme USING btree (categorie);


--
-- Name: idx_parametres_cle; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_parametres_cle ON configuration.parametres_systeme USING btree (cle);


--
-- Name: idx_taux_actif; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_taux_actif ON configuration.taux_change USING btree (est_actif, date_debut_validite DESC) WHERE (est_actif = true);


--
-- Name: idx_taux_devises; Type: INDEX; Schema: configuration; Owner: postgres
--

CREATE INDEX idx_taux_devises ON configuration.taux_change USING btree (devise_source, devise_cible);


--
-- Name: idx_applications_compte; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_applications_compte ON developpeurs.applications USING btree (compte_developpeur_id);


--
-- Name: idx_applications_statut; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_applications_statut ON developpeurs.applications USING btree (statut);


--
-- Name: idx_cles_api_active; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_cles_api_active ON developpeurs.cles_api USING btree (est_active) WHERE (est_active = true);


--
-- Name: idx_cles_api_cle; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_cles_api_cle ON developpeurs.cles_api USING btree (cle_api);


--
-- Name: idx_cles_api_compte; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_cles_api_compte ON developpeurs.cles_api USING btree (compte_developpeur_id);


--
-- Name: idx_cles_api_environnement; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_cles_api_environnement ON developpeurs.cles_api USING btree (environnement);


--
-- Name: idx_cles_api_prefixe; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_cles_api_prefixe ON developpeurs.cles_api USING btree (prefixe_cle);


--
-- Name: idx_comptes_dev_courriel; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_comptes_dev_courriel ON developpeurs.comptes_developpeurs USING btree (courriel_contact);


--
-- Name: idx_comptes_dev_statut; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_comptes_dev_statut ON developpeurs.comptes_developpeurs USING btree (statut);


--
-- Name: idx_comptes_dev_type; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_comptes_dev_type ON developpeurs.comptes_developpeurs USING btree (type_compte);


--
-- Name: idx_comptes_dev_utilisateur; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_comptes_dev_utilisateur ON developpeurs.comptes_developpeurs USING btree (utilisateur_id);


--
-- Name: idx_logs_api_cle; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_cle ON developpeurs.logs_utilisation_api USING btree (cle_api_id);


--
-- Name: idx_logs_api_compte; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_compte ON developpeurs.logs_utilisation_api USING btree (compte_developpeur_id);


--
-- Name: idx_logs_api_date; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_date ON developpeurs.logs_utilisation_api USING btree (date_requete DESC);


--
-- Name: idx_logs_api_endpoint; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_endpoint ON developpeurs.logs_utilisation_api USING btree (endpoint);


--
-- Name: idx_logs_api_ip; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_ip ON developpeurs.logs_utilisation_api USING btree (adresse_ip);


--
-- Name: idx_logs_api_statut; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_logs_api_statut ON developpeurs.logs_utilisation_api USING btree (statut_http);


--
-- Name: idx_quotas_cle; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_quotas_cle ON developpeurs.quotas_utilisation USING btree (cle_api_id);


--
-- Name: idx_quotas_compte; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_quotas_compte ON developpeurs.quotas_utilisation USING btree (compte_developpeur_id);


--
-- Name: idx_quotas_date; Type: INDEX; Schema: developpeurs; Owner: postgres
--

CREATE INDEX idx_quotas_date ON developpeurs.quotas_utilisation USING btree (date_periode DESC);


--
-- Name: idx_historique_date; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_historique_date ON identite.historique_numeros_telephone USING btree (date_action DESC);


--
-- Name: idx_historique_numero; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_historique_numero ON identite.historique_numeros_telephone USING btree (numero_telephone_id);


--
-- Name: idx_historique_utilisateur; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_historique_utilisateur ON identite.historique_numeros_telephone USING btree (utilisateur_id);


--
-- Name: idx_niveaux_kyc_actif; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_niveaux_kyc_actif ON identite.niveaux_kyc USING btree (est_actif);


--
-- Name: idx_numeros_complet; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_complet ON identite.numeros_telephone USING btree (numero_complet);


--
-- Name: idx_numeros_pays_code; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_pays_code ON identite.numeros_telephone USING btree (pays_code_iso_2);


--
-- Name: idx_numeros_principal; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_principal ON identite.numeros_telephone USING btree (utilisateur_id, est_principal) WHERE (est_principal = true);


--
-- Name: idx_numeros_statut; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_statut ON identite.numeros_telephone USING btree (statut);


--
-- Name: idx_numeros_utilisateur; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_utilisateur ON identite.numeros_telephone USING btree (utilisateur_id);


--
-- Name: idx_numeros_verifie; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_numeros_verifie ON identite.numeros_telephone USING btree (est_verifie);


--
-- Name: idx_profils_utilisateur; Type: INDEX; Schema: identite; Owner: postgres
--

CREATE INDEX idx_profils_utilisateur ON identite.profils_utilisateurs USING btree (utilisateur_id);


--
-- Name: idx_statuts_utilisateurs_actif; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_statuts_utilisateurs_actif ON identite.statuts_utilisateurs USING btree (est_actif);


--
-- Name: idx_statuts_utilisateurs_ordre; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_statuts_utilisateurs_ordre ON identite.statuts_utilisateurs USING btree (ordre_affichage);


--
-- Name: idx_types_utilisateurs_actif; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_types_utilisateurs_actif ON identite.types_utilisateurs USING btree (est_actif);


--
-- Name: idx_types_utilisateurs_ordre; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_types_utilisateurs_ordre ON identite.types_utilisateurs USING btree (ordre_affichage);


--
-- Name: idx_utilisateurs_courriel; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_courriel ON identite.utilisateurs USING btree (courriel);


--
-- Name: idx_utilisateurs_date_creation; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_date_creation ON identite.utilisateurs USING btree (date_creation DESC);


--
-- Name: idx_utilisateurs_district; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_district ON identite.utilisateurs USING btree (district_id);


--
-- Name: idx_utilisateurs_niveau_kyc; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_niveau_kyc ON identite.utilisateurs USING btree (niveau_kyc);


--
-- Name: idx_utilisateurs_pays; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_pays ON identite.utilisateurs USING btree (pays_id);


--
-- Name: idx_utilisateurs_point_de_service; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_point_de_service ON identite.utilisateurs USING btree (point_de_service_id);


--
-- Name: idx_utilisateurs_province; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_province ON identite.utilisateurs USING btree (province_id);


--
-- Name: idx_utilisateurs_quartier; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_quartier ON identite.utilisateurs USING btree (quartier_id);


--
-- Name: idx_utilisateurs_statut; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_statut ON identite.utilisateurs USING btree (statut);


--
-- Name: idx_utilisateurs_telephone; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_telephone ON identite.utilisateurs USING btree (numero_telephone);


--
-- Name: idx_utilisateurs_type; Type: INDEX; Schema: identite; Owner: ufaranga
--

CREATE INDEX idx_utilisateurs_type ON identite.utilisateurs USING btree (type_utilisateur);


--
-- Name: idx_districts_autorise; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_districts_autorise ON localisation.districts USING btree (autorise_systeme) WHERE (autorise_systeme = true);


--
-- Name: idx_districts_province; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_districts_province ON localisation.districts USING btree (province_id);


--
-- Name: idx_pays_autorise; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_pays_autorise ON localisation.pays USING btree (autorise_systeme) WHERE (autorise_systeme = true);


--
-- Name: idx_pays_code; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_pays_code ON localisation.pays USING btree (code_iso_2);


--
-- Name: idx_pays_continent; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_pays_continent ON localisation.pays USING btree (continent);


--
-- Name: idx_pays_sous_region; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_pays_sous_region ON localisation.pays USING btree (sous_region);


--
-- Name: idx_points_de_service_agent; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_points_de_service_agent ON localisation.points_de_service USING btree (agent_utilisateur_id);


--
-- Name: idx_points_de_service_autorise; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_points_de_service_autorise ON localisation.points_de_service USING btree (autorise_systeme) WHERE (autorise_systeme = true);


--
-- Name: idx_points_de_service_quartier; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_points_de_service_quartier ON localisation.points_de_service USING btree (quartier_id);


--
-- Name: idx_provinces_autorise; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_provinces_autorise ON localisation.provinces USING btree (autorise_systeme) WHERE (autorise_systeme = true);


--
-- Name: idx_provinces_pays; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_provinces_pays ON localisation.provinces USING btree (pays_id);


--
-- Name: idx_quartiers_autorise; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_quartiers_autorise ON localisation.quartiers USING btree (autorise_systeme) WHERE (autorise_systeme = true);


--
-- Name: idx_quartiers_district; Type: INDEX; Schema: localisation; Owner: postgres
--

CREATE INDEX idx_quartiers_district ON localisation.quartiers USING btree (district_id);


--
-- Name: idx_notifications_en_attente; Type: INDEX; Schema: notification; Owner: postgres
--

CREATE INDEX idx_notifications_en_attente ON notification.notifications USING btree (statut_envoi, nombre_tentatives, date_planification) WHERE ((statut_envoi)::text = 'EN_ATTENTE'::text);


--
-- Name: idx_notifications_statut; Type: INDEX; Schema: notification; Owner: postgres
--

CREATE INDEX idx_notifications_statut ON notification.notifications USING btree (statut_envoi);


--
-- Name: idx_notifications_type; Type: INDEX; Schema: notification; Owner: postgres
--

CREATE INDEX idx_notifications_type ON notification.notifications USING btree (type_notification);


--
-- Name: idx_notifications_utilisateur; Type: INDEX; Schema: notification; Owner: postgres
--

CREATE INDEX idx_notifications_utilisateur ON notification.notifications USING btree (utilisateur_id);


--
-- Name: idx_portefeuilles_compte_bancaire; Type: INDEX; Schema: portefeuille; Owner: postgres
--

CREATE INDEX idx_portefeuilles_compte_bancaire ON portefeuille.portefeuilles_virtuels USING btree (compte_bancaire_reel_id);


--
-- Name: idx_portefeuilles_numero; Type: INDEX; Schema: portefeuille; Owner: postgres
--

CREATE INDEX idx_portefeuilles_numero ON portefeuille.portefeuilles_virtuels USING btree (numero_portefeuille);


--
-- Name: idx_portefeuilles_statut; Type: INDEX; Schema: portefeuille; Owner: postgres
--

CREATE INDEX idx_portefeuilles_statut ON portefeuille.portefeuilles_virtuels USING btree (statut);


--
-- Name: idx_portefeuilles_type; Type: INDEX; Schema: portefeuille; Owner: postgres
--

CREATE INDEX idx_portefeuilles_type ON portefeuille.portefeuilles_virtuels USING btree (type_portefeuille);


--
-- Name: idx_portefeuilles_utilisateur; Type: INDEX; Schema: portefeuille; Owner: postgres
--

CREATE INDEX idx_portefeuilles_utilisateur ON portefeuille.portefeuilles_virtuels USING btree (utilisateur_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: currencies_code_169576e8_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX currencies_code_169576e8_like ON public.currencies USING btree (code varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: exchange_ra_from_cu_72b998_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX exchange_ra_from_cu_72b998_idx ON public.exchange_rates USING btree (from_currency_id, to_currency_id, is_active);


--
-- Name: exchange_rates_from_currency_id_474db0e8; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX exchange_rates_from_currency_id_474db0e8 ON public.exchange_rates USING btree (from_currency_id);


--
-- Name: exchange_rates_from_currency_id_474db0e8_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX exchange_rates_from_currency_id_474db0e8_like ON public.exchange_rates USING btree (from_currency_id varchar_pattern_ops);


--
-- Name: exchange_rates_to_currency_id_e433e1d1; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX exchange_rates_to_currency_id_e433e1d1 ON public.exchange_rates USING btree (to_currency_id);


--
-- Name: exchange_rates_to_currency_id_e433e1d1_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX exchange_rates_to_currency_id_e433e1d1_like ON public.exchange_rates USING btree (to_currency_id varchar_pattern_ops);


--
-- Name: oauth2_provider_accesstoken_application_id_b22886e1; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_accesstoken_application_id_b22886e1 ON public.oauth2_provider_accesstoken USING btree (application_id);


--
-- Name: oauth2_provider_accesstoken_token_8af090f8_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_accesstoken_token_8af090f8_like ON public.oauth2_provider_accesstoken USING btree (token varchar_pattern_ops);


--
-- Name: oauth2_provider_accesstoken_user_id_6e4c9a65; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_accesstoken_user_id_6e4c9a65 ON public.oauth2_provider_accesstoken USING btree (user_id);


--
-- Name: oauth2_provider_application_client_id_03f0cc84_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_application_client_id_03f0cc84_like ON public.oauth2_provider_application USING btree (client_id varchar_pattern_ops);


--
-- Name: oauth2_provider_application_client_secret_53133678; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_application_client_secret_53133678 ON public.oauth2_provider_application USING btree (client_secret);


--
-- Name: oauth2_provider_application_client_secret_53133678_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_application_client_secret_53133678_like ON public.oauth2_provider_application USING btree (client_secret varchar_pattern_ops);


--
-- Name: oauth2_provider_application_user_id_79829054; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_application_user_id_79829054 ON public.oauth2_provider_application USING btree (user_id);


--
-- Name: oauth2_provider_grant_application_id_81923564; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_grant_application_id_81923564 ON public.oauth2_provider_grant USING btree (application_id);


--
-- Name: oauth2_provider_grant_code_49ab4ddf_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_grant_code_49ab4ddf_like ON public.oauth2_provider_grant USING btree (code varchar_pattern_ops);


--
-- Name: oauth2_provider_grant_user_id_e8f62af8; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_grant_user_id_e8f62af8 ON public.oauth2_provider_grant USING btree (user_id);


--
-- Name: oauth2_provider_idtoken_application_id_08c5ff4f; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_idtoken_application_id_08c5ff4f ON public.oauth2_provider_idtoken USING btree (application_id);


--
-- Name: oauth2_provider_idtoken_user_id_dd512b59; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_idtoken_user_id_dd512b59 ON public.oauth2_provider_idtoken USING btree (user_id);


--
-- Name: oauth2_provider_refreshtoken_application_id_2d1c311b; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_refreshtoken_application_id_2d1c311b ON public.oauth2_provider_refreshtoken USING btree (application_id);


--
-- Name: oauth2_provider_refreshtoken_user_id_da837fce; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX oauth2_provider_refreshtoken_user_id_da837fce ON public.oauth2_provider_refreshtoken USING btree (user_id);


--
-- Name: token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like ON public.token_blacklist_outstandingtoken USING btree (jti varchar_pattern_ops);


--
-- Name: token_blacklist_outstandingtoken_user_id_83bc629a; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX token_blacklist_outstandingtoken_user_id_83bc629a ON public.token_blacklist_outstandingtoken USING btree (user_id);


--
-- Name: user_sessions_session_key_5c5616a8_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX user_sessions_session_key_5c5616a8_like ON public.user_sessions USING btree (session_key varchar_pattern_ops);


--
-- Name: user_sessions_user_id_43ce9642; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX user_sessions_user_id_43ce9642 ON public.user_sessions USING btree (user_id);


--
-- Name: users_email_0ea73cca_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_email_0ea73cca_like ON public.users USING btree (email varchar_pattern_ops);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_groups_user_id_f500bee5; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_groups_user_id_f500bee5 ON public.users_groups USING btree (user_id);


--
-- Name: users_phone_number_b4cde146_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_phone_number_b4cde146_like ON public.users USING btree (phone_number varchar_pattern_ops);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: users_user_permissions_user_id_92473840; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_user_permissions_user_id_92473840 ON public.users_user_permissions USING btree (user_id);


--
-- Name: users_username_e8658fc8_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX users_username_e8658fc8_like ON public.users USING btree (username varchar_pattern_ops);


--
-- Name: wallet_limits_wallet_id_93267c56; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallet_limits_wallet_id_93267c56 ON public.wallet_limits USING btree (wallet_id);


--
-- Name: wallet_tran_externa_3a6c4a_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallet_tran_externa_3a6c4a_idx ON public.wallet_transactions USING btree (external_transaction_id);


--
-- Name: wallet_tran_wallet__3d47ad_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallet_tran_wallet__3d47ad_idx ON public.wallet_transactions USING btree (wallet_id, created_at DESC);


--
-- Name: wallet_transactions_wallet_id_8cb3251a; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallet_transactions_wallet_id_8cb3251a ON public.wallet_transactions USING btree (wallet_id);


--
-- Name: wallets_currenc_796236_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallets_currenc_796236_idx ON public.wallets USING btree (currency_id);


--
-- Name: wallets_currency_id_9e8036e4; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallets_currency_id_9e8036e4 ON public.wallets USING btree (currency_id);


--
-- Name: wallets_currency_id_9e8036e4_like; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallets_currency_id_9e8036e4_like ON public.wallets USING btree (currency_id varchar_pattern_ops);


--
-- Name: wallets_status_5720bd_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallets_status_5720bd_idx ON public.wallets USING btree (status);


--
-- Name: wallets_user_id_9fb6cf_idx; Type: INDEX; Schema: public; Owner: ufaranga
--

CREATE INDEX wallets_user_id_9fb6cf_idx ON public.wallets USING btree (user_id);


--
-- Name: idx_grand_livre_compte_bancaire; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_grand_livre_compte_bancaire ON transaction.grand_livre_comptable USING btree (compte_bancaire_id);


--
-- Name: idx_grand_livre_date; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_grand_livre_date ON transaction.grand_livre_comptable USING btree (date_ecriture DESC);


--
-- Name: idx_grand_livre_portefeuille; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_grand_livre_portefeuille ON transaction.grand_livre_comptable USING btree (portefeuille_id);


--
-- Name: idx_grand_livre_transaction; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_grand_livre_transaction ON transaction.grand_livre_comptable USING btree (transaction_id);


--
-- Name: idx_grand_livre_type; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_grand_livre_type ON transaction.grand_livre_comptable USING btree (type_ecriture);


--
-- Name: idx_transactions_date_completion; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_date_completion ON transaction.transactions USING btree (date_completion DESC);


--
-- Name: idx_transactions_date_initiation; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_date_initiation ON transaction.transactions USING btree (date_initiation DESC);


--
-- Name: idx_transactions_dest_user; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_dest_user ON transaction.transactions USING btree (utilisateur_destination_id);


--
-- Name: idx_transactions_dest_wallet; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_dest_wallet ON transaction.transactions USING btree (portefeuille_destination_id);


--
-- Name: idx_transactions_fraude; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_fraude ON transaction.transactions USING btree (score_fraude) WHERE (score_fraude >= 70);


--
-- Name: idx_transactions_reference; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_reference ON transaction.transactions USING btree (reference_transaction);


--
-- Name: idx_transactions_source_user; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_source_user ON transaction.transactions USING btree (utilisateur_source_id);


--
-- Name: idx_transactions_source_wallet; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_source_wallet ON transaction.transactions USING btree (portefeuille_source_id);


--
-- Name: idx_transactions_statut; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_statut ON transaction.transactions USING btree (statut);


--
-- Name: idx_transactions_type; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_transactions_type ON transaction.transactions USING btree (type_transaction);


--
-- Name: vue_stats_developpeurs _RETURN; Type: RULE; Schema: developpeurs; Owner: postgres
--

CREATE OR REPLACE VIEW developpeurs.vue_stats_developpeurs AS
 SELECT cd.id,
    cd.nom_entreprise,
    cd.courriel_contact,
    cd.type_compte,
    cd.statut,
    count(DISTINCT ca.id) AS nombre_cles_api,
    count(DISTINCT ca.id) FILTER (WHERE (ca.est_active = true)) AS cles_actives,
    count(DISTINCT a.id) AS nombre_applications,
    COALESCE(sum(qu.nombre_requetes), (0)::bigint) AS total_requetes_mois,
    cd.quota_requetes_mois,
    cd.date_creation
   FROM (((developpeurs.comptes_developpeurs cd
     LEFT JOIN developpeurs.cles_api ca ON ((cd.id = ca.compte_developpeur_id)))
     LEFT JOIN developpeurs.applications a ON ((cd.id = a.compte_developpeur_id)))
     LEFT JOIN developpeurs.quotas_utilisation qu ON (((cd.id = qu.compte_developpeur_id) AND ((qu.type_periode)::text = 'MOIS'::text) AND (qu.date_periode = (date_trunc('month'::text, (CURRENT_DATE)::timestamp with time zone))::date))))
  GROUP BY cd.id;


--
-- Name: historique_modifications trigger_proteger_delete_historique; Type: TRIGGER; Schema: audit; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_historique BEFORE DELETE ON audit.historique_modifications FOR EACH ROW EXECUTE PROCEDURE audit.proteger_journaux();


--
-- Name: journaux_evenements trigger_proteger_delete_journaux; Type: TRIGGER; Schema: audit; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_journaux BEFORE DELETE ON audit.journaux_evenements FOR EACH ROW EXECUTE PROCEDURE audit.proteger_journaux();


--
-- Name: historique_modifications trigger_proteger_update_historique; Type: TRIGGER; Schema: audit; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_historique BEFORE UPDATE ON audit.historique_modifications FOR EACH ROW EXECUTE PROCEDURE audit.proteger_journaux();


--
-- Name: journaux_evenements trigger_proteger_update_journaux; Type: TRIGGER; Schema: audit; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_journaux BEFORE UPDATE ON audit.journaux_evenements FOR EACH ROW EXECUTE PROCEDURE audit.proteger_journaux();


--
-- Name: mouvements_bancaires_reels trigger_mouvements_no_update; Type: TRIGGER; Schema: bancaire; Owner: postgres
--

CREATE TRIGGER trigger_mouvements_no_update BEFORE UPDATE ON bancaire.mouvements_bancaires_reels FOR EACH ROW EXECUTE PROCEDURE bancaire.proteger_mouvements_bancaires();


--
-- Name: screening_aml trigger_proteger_delete_aml; Type: TRIGGER; Schema: compliance; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_aml BEFORE DELETE ON compliance.screening_aml FOR EACH ROW EXECUTE PROCEDURE compliance.proteger_verifications();


--
-- Name: verifications_kyc trigger_proteger_delete_verif; Type: TRIGGER; Schema: compliance; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_verif BEFORE DELETE ON compliance.verifications_kyc FOR EACH ROW EXECUTE PROCEDURE compliance.proteger_verifications();


--
-- Name: screening_aml trigger_proteger_update_aml; Type: TRIGGER; Schema: compliance; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_aml BEFORE UPDATE ON compliance.screening_aml FOR EACH ROW EXECUTE PROCEDURE compliance.proteger_verifications();


--
-- Name: verifications_kyc trigger_proteger_update_verif; Type: TRIGGER; Schema: compliance; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_verif BEFORE UPDATE ON compliance.verifications_kyc FOR EACH ROW EXECUTE PROCEDURE compliance.proteger_verifications();


--
-- Name: logs_utilisation_api trigger_proteger_delete_logs_api; Type: TRIGGER; Schema: developpeurs; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_logs_api BEFORE DELETE ON developpeurs.logs_utilisation_api FOR EACH ROW EXECUTE PROCEDURE developpeurs.proteger_logs_api();


--
-- Name: logs_utilisation_api trigger_proteger_update_logs_api; Type: TRIGGER; Schema: developpeurs; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_logs_api BEFORE UPDATE ON developpeurs.logs_utilisation_api FOR EACH ROW EXECUTE PROCEDURE developpeurs.proteger_logs_api();


--
-- Name: numeros_telephone trg_historique_numero; Type: TRIGGER; Schema: identite; Owner: ufaranga
--

CREATE TRIGGER trg_historique_numero AFTER INSERT OR UPDATE ON identite.numeros_telephone FOR EACH ROW EXECUTE PROCEDURE identite.enregistrer_historique_numero();


--
-- Name: grand_livre_comptable trigger_proteger_delete_grand_livre; Type: TRIGGER; Schema: transaction; Owner: postgres
--

CREATE TRIGGER trigger_proteger_delete_grand_livre BEFORE DELETE ON transaction.grand_livre_comptable FOR EACH ROW EXECUTE PROCEDURE transaction.proteger_grand_livre();


--
-- Name: grand_livre_comptable trigger_proteger_update_grand_livre; Type: TRIGGER; Schema: transaction; Owner: postgres
--

CREATE TRIGGER trigger_proteger_update_grand_livre BEFORE UPDATE ON transaction.grand_livre_comptable FOR EACH ROW EXECUTE PROCEDURE transaction.proteger_grand_livre();


--
-- Name: historique_modifications historique_modifications_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.historique_modifications
    ADD CONSTRAINT historique_modifications_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: journaux_evenements journaux_evenements_session_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.journaux_evenements
    ADD CONSTRAINT journaux_evenements_session_id_fkey FOREIGN KEY (session_id) REFERENCES audit.sessions_utilisateurs(id) ON DELETE SET NULL;


--
-- Name: journaux_evenements journaux_evenements_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.journaux_evenements
    ADD CONSTRAINT journaux_evenements_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: sessions_utilisateurs sessions_utilisateurs_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: audit; Owner: postgres
--

ALTER TABLE ONLY audit.sessions_utilisateurs
    ADD CONSTRAINT sessions_utilisateurs_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: comptes_bancaires_reels comptes_bancaires_reels_banque_id_fkey; Type: FK CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.comptes_bancaires_reels
    ADD CONSTRAINT comptes_bancaires_reels_banque_id_fkey FOREIGN KEY (banque_id) REFERENCES bancaire.banques_partenaires(id) ON DELETE RESTRICT;


--
-- Name: comptes_bancaires_reels comptes_bancaires_reels_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.comptes_bancaires_reels
    ADD CONSTRAINT comptes_bancaires_reels_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE RESTRICT;


--
-- Name: mouvements_bancaires_reels mouvements_bancaires_reels_compte_bancaire_id_fkey; Type: FK CONSTRAINT; Schema: bancaire; Owner: postgres
--

ALTER TABLE ONLY bancaire.mouvements_bancaires_reels
    ADD CONSTRAINT mouvements_bancaires_reels_compte_bancaire_id_fkey FOREIGN KEY (compte_bancaire_id) REFERENCES bancaire.comptes_bancaires_reels(id) ON DELETE RESTRICT;


--
-- Name: commissions commissions_beneficiaire_id_fkey; Type: FK CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.commissions
    ADD CONSTRAINT commissions_beneficiaire_id_fkey FOREIGN KEY (beneficiaire_id) REFERENCES identite.utilisateurs(id);


--
-- Name: commissions commissions_grille_commission_id_fkey; Type: FK CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.commissions
    ADD CONSTRAINT commissions_grille_commission_id_fkey FOREIGN KEY (grille_commission_id) REFERENCES commission.grilles_commissions(id);


--
-- Name: commissions commissions_transaction_id_fkey; Type: FK CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.commissions
    ADD CONSTRAINT commissions_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES transaction.transactions(id) ON DELETE RESTRICT;


--
-- Name: grilles_commissions grilles_commissions_cree_par_fkey; Type: FK CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.grilles_commissions
    ADD CONSTRAINT grilles_commissions_cree_par_fkey FOREIGN KEY (cree_par) REFERENCES identite.utilisateurs(id);


--
-- Name: grilles_commissions grilles_commissions_modifie_par_fkey; Type: FK CONSTRAINT; Schema: commission; Owner: postgres
--

ALTER TABLE ONLY commission.grilles_commissions
    ADD CONSTRAINT grilles_commissions_modifie_par_fkey FOREIGN KEY (modifie_par) REFERENCES identite.utilisateurs(id);


--
-- Name: documents_kyc documents_kyc_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.documents_kyc
    ADD CONSTRAINT documents_kyc_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: documents_kyc documents_kyc_verifie_par_fkey; Type: FK CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.documents_kyc
    ADD CONSTRAINT documents_kyc_verifie_par_fkey FOREIGN KEY (verifie_par) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: screening_aml screening_aml_prise_en_charge_par_fkey; Type: FK CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.screening_aml
    ADD CONSTRAINT screening_aml_prise_en_charge_par_fkey FOREIGN KEY (prise_en_charge_par) REFERENCES identite.utilisateurs(id);


--
-- Name: screening_aml screening_aml_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.screening_aml
    ADD CONSTRAINT screening_aml_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: verifications_kyc verifications_kyc_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: compliance; Owner: postgres
--

ALTER TABLE ONLY compliance.verifications_kyc
    ADD CONSTRAINT verifications_kyc_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: blacklist blacklist_ajoute_par_fkey; Type: FK CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.blacklist
    ADD CONSTRAINT blacklist_ajoute_par_fkey FOREIGN KEY (ajoute_par) REFERENCES identite.utilisateurs(id) ON DELETE RESTRICT;


--
-- Name: parametres_systeme parametres_systeme_modifie_par_fkey; Type: FK CONSTRAINT; Schema: configuration; Owner: postgres
--

ALTER TABLE ONLY configuration.parametres_systeme
    ADD CONSTRAINT parametres_systeme_modifie_par_fkey FOREIGN KEY (modifie_par) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: applications applications_compte_developpeur_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.applications
    ADD CONSTRAINT applications_compte_developpeur_id_fkey FOREIGN KEY (compte_developpeur_id) REFERENCES developpeurs.comptes_developpeurs(id) ON DELETE CASCADE;


--
-- Name: cles_api cles_api_compte_developpeur_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.cles_api
    ADD CONSTRAINT cles_api_compte_developpeur_id_fkey FOREIGN KEY (compte_developpeur_id) REFERENCES developpeurs.comptes_developpeurs(id) ON DELETE CASCADE;


--
-- Name: comptes_developpeurs comptes_developpeurs_approuve_par_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.comptes_developpeurs
    ADD CONSTRAINT comptes_developpeurs_approuve_par_fkey FOREIGN KEY (approuve_par) REFERENCES identite.utilisateurs(id);


--
-- Name: comptes_developpeurs comptes_developpeurs_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.comptes_developpeurs
    ADD CONSTRAINT comptes_developpeurs_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: logs_utilisation_api logs_utilisation_api_cle_api_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.logs_utilisation_api
    ADD CONSTRAINT logs_utilisation_api_cle_api_id_fkey FOREIGN KEY (cle_api_id) REFERENCES developpeurs.cles_api(id) ON DELETE CASCADE;


--
-- Name: logs_utilisation_api logs_utilisation_api_compte_developpeur_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.logs_utilisation_api
    ADD CONSTRAINT logs_utilisation_api_compte_developpeur_id_fkey FOREIGN KEY (compte_developpeur_id) REFERENCES developpeurs.comptes_developpeurs(id) ON DELETE CASCADE;


--
-- Name: quotas_utilisation quotas_utilisation_cle_api_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.quotas_utilisation
    ADD CONSTRAINT quotas_utilisation_cle_api_id_fkey FOREIGN KEY (cle_api_id) REFERENCES developpeurs.cles_api(id) ON DELETE CASCADE;


--
-- Name: quotas_utilisation quotas_utilisation_compte_developpeur_id_fkey; Type: FK CONSTRAINT; Schema: developpeurs; Owner: postgres
--

ALTER TABLE ONLY developpeurs.quotas_utilisation
    ADD CONSTRAINT quotas_utilisation_compte_developpeur_id_fkey FOREIGN KEY (compte_developpeur_id) REFERENCES developpeurs.comptes_developpeurs(id) ON DELETE CASCADE;


--
-- Name: historique_numeros_telephone historique_numeros_telephone_numero_telephone_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.historique_numeros_telephone
    ADD CONSTRAINT historique_numeros_telephone_numero_telephone_id_fkey FOREIGN KEY (numero_telephone_id) REFERENCES identite.numeros_telephone(id);


--
-- Name: historique_numeros_telephone historique_numeros_telephone_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.historique_numeros_telephone
    ADD CONSTRAINT historique_numeros_telephone_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id);


--
-- Name: limites_numeros_par_pays limites_numeros_par_pays_type_utilisateur_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.limites_numeros_par_pays
    ADD CONSTRAINT limites_numeros_par_pays_type_utilisateur_fkey FOREIGN KEY (type_utilisateur) REFERENCES identite.types_utilisateurs(code);


--
-- Name: numeros_telephone numeros_telephone_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.numeros_telephone
    ADD CONSTRAINT numeros_telephone_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: profils_utilisateurs profils_utilisateurs_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: postgres
--

ALTER TABLE ONLY identite.profils_utilisateurs
    ADD CONSTRAINT profils_utilisateurs_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: utilisateurs utilisateurs_district_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_district_id_fkey FOREIGN KEY (district_id) REFERENCES localisation.districts(id) ON DELETE SET NULL;


--
-- Name: utilisateurs utilisateurs_niveau_kyc_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_niveau_kyc_fkey FOREIGN KEY (niveau_kyc) REFERENCES identite.niveaux_kyc(niveau);


--
-- Name: utilisateurs utilisateurs_pays_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_pays_id_fkey FOREIGN KEY (pays_id) REFERENCES localisation.pays(id) ON DELETE SET NULL;


--
-- Name: utilisateurs utilisateurs_point_de_service_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_point_de_service_id_fkey FOREIGN KEY (point_de_service_id) REFERENCES localisation.points_de_service(id) ON DELETE SET NULL;


--
-- Name: utilisateurs utilisateurs_province_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_province_id_fkey FOREIGN KEY (province_id) REFERENCES localisation.provinces(id) ON DELETE SET NULL;


--
-- Name: utilisateurs utilisateurs_quartier_id_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_quartier_id_fkey FOREIGN KEY (quartier_id) REFERENCES localisation.quartiers(id) ON DELETE SET NULL;


--
-- Name: utilisateurs utilisateurs_statut_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_statut_fkey FOREIGN KEY (statut) REFERENCES identite.statuts_utilisateurs(code);


--
-- Name: utilisateurs utilisateurs_type_utilisateur_fkey; Type: FK CONSTRAINT; Schema: identite; Owner: ufaranga
--

ALTER TABLE ONLY identite.utilisateurs
    ADD CONSTRAINT utilisateurs_type_utilisateur_fkey FOREIGN KEY (type_utilisateur) REFERENCES identite.types_utilisateurs(code);


--
-- Name: districts districts_province_id_fkey; Type: FK CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.districts
    ADD CONSTRAINT districts_province_id_fkey FOREIGN KEY (province_id) REFERENCES localisation.provinces(id) ON DELETE CASCADE;


--
-- Name: points_de_service points_de_service_agent_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.points_de_service
    ADD CONSTRAINT points_de_service_agent_utilisateur_id_fkey FOREIGN KEY (agent_utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE SET NULL;


--
-- Name: points_de_service points_de_service_quartier_id_fkey; Type: FK CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.points_de_service
    ADD CONSTRAINT points_de_service_quartier_id_fkey FOREIGN KEY (quartier_id) REFERENCES localisation.quartiers(id) ON DELETE CASCADE;


--
-- Name: provinces provinces_pays_id_fkey; Type: FK CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.provinces
    ADD CONSTRAINT provinces_pays_id_fkey FOREIGN KEY (pays_id) REFERENCES localisation.pays(id) ON DELETE CASCADE;


--
-- Name: quartiers quartiers_district_id_fkey; Type: FK CONSTRAINT; Schema: localisation; Owner: postgres
--

ALTER TABLE ONLY localisation.quartiers
    ADD CONSTRAINT quartiers_district_id_fkey FOREIGN KEY (district_id) REFERENCES localisation.districts(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: notification; Owner: postgres
--

ALTER TABLE ONLY notification.notifications
    ADD CONSTRAINT notifications_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE CASCADE;


--
-- Name: portefeuilles_virtuels portefeuilles_virtuels_compte_bancaire_reel_id_fkey; Type: FK CONSTRAINT; Schema: portefeuille; Owner: postgres
--

ALTER TABLE ONLY portefeuille.portefeuilles_virtuels
    ADD CONSTRAINT portefeuilles_virtuels_compte_bancaire_reel_id_fkey FOREIGN KEY (compte_bancaire_reel_id) REFERENCES bancaire.comptes_bancaires_reels(id) ON DELETE RESTRICT;


--
-- Name: portefeuilles_virtuels portefeuilles_virtuels_utilisateur_id_fkey; Type: FK CONSTRAINT; Schema: portefeuille; Owner: postgres
--

ALTER TABLE ONLY portefeuille.portefeuilles_virtuels
    ADD CONSTRAINT portefeuilles_virtuels_utilisateur_id_fkey FOREIGN KEY (utilisateur_id) REFERENCES identite.utilisateurs(id) ON DELETE RESTRICT;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exchange_rates exchange_rates_from_currency_id_474db0e8_fk_currencies_code; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.exchange_rates
    ADD CONSTRAINT exchange_rates_from_currency_id_474db0e8_fk_currencies_code FOREIGN KEY (from_currency_id) REFERENCES public.currencies(code) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: exchange_rates exchange_rates_to_currency_id_e433e1d1_fk_currencies_code; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.exchange_rates
    ADD CONSTRAINT exchange_rates_to_currency_id_e433e1d1_fk_currencies_code FOREIGN KEY (to_currency_id) REFERENCES public.currencies(code) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr FOREIGN KEY (id_token_id) REFERENCES public.oauth2_provider_idtoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr FOREIGN KEY (source_refresh_token_id) REFERENCES public.oauth2_provider_refreshtoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_user_id_6e4c9a65_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_application oauth2_provider_application_user_id_79829054_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_user_id_79829054_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth2_provider_gran_application_id_81923564_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_gran_application_id_81923564_fk_oauth2_pr FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth2_provider_grant_user_id_e8f62af8_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_user_id_e8f62af8_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_idtoken oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_idtoken
    ADD CONSTRAINT oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_user_id_dd512b59_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_idtoken
    ADD CONSTRAINT oauth2_provider_idtoken_user_id_dd512b59_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr FOREIGN KEY (access_token_id) REFERENCES public.oauth2_provider_accesstoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_user_id_da837fce_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_user_id_da837fce_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk FOREIGN KEY (token_id) REFERENCES public.token_blacklist_outstandingtoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_profiles user_profiles_user_id_8c5ab5fe_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_8c5ab5fe_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_sessions user_sessions_user_id_43ce9642_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_43ce9642_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_user_id_f500bee5_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_f500bee5_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_user_id_92473840_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_92473840_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wallet_limits wallet_limits_wallet_id_93267c56_fk_wallets_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallet_limits
    ADD CONSTRAINT wallet_limits_wallet_id_93267c56_fk_wallets_id FOREIGN KEY (wallet_id) REFERENCES public.wallets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wallet_transactions wallet_transactions_wallet_id_8cb3251a_fk_wallets_id; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallet_transactions
    ADD CONSTRAINT wallet_transactions_wallet_id_8cb3251a_fk_wallets_id FOREIGN KEY (wallet_id) REFERENCES public.wallets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: wallets wallets_currency_id_9e8036e4_fk_currencies_code; Type: FK CONSTRAINT; Schema: public; Owner: ufaranga
--

ALTER TABLE ONLY public.wallets
    ADD CONSTRAINT wallets_currency_id_9e8036e4_fk_currencies_code FOREIGN KEY (currency_id) REFERENCES public.currencies(code) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: grand_livre_comptable grand_livre_comptable_compte_bancaire_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.grand_livre_comptable
    ADD CONSTRAINT grand_livre_comptable_compte_bancaire_id_fkey FOREIGN KEY (compte_bancaire_id) REFERENCES bancaire.comptes_bancaires_reels(id) ON DELETE RESTRICT;


--
-- Name: grand_livre_comptable grand_livre_comptable_portefeuille_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.grand_livre_comptable
    ADD CONSTRAINT grand_livre_comptable_portefeuille_id_fkey FOREIGN KEY (portefeuille_id) REFERENCES portefeuille.portefeuilles_virtuels(id) ON DELETE RESTRICT;


--
-- Name: grand_livre_comptable grand_livre_comptable_transaction_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.grand_livre_comptable
    ADD CONSTRAINT grand_livre_comptable_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES transaction.transactions(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_annulee_par_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_annulee_par_fkey FOREIGN KEY (annulee_par) REFERENCES identite.utilisateurs(id);


--
-- Name: transactions transactions_compte_bancaire_dest_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_compte_bancaire_dest_id_fkey FOREIGN KEY (compte_bancaire_dest_id) REFERENCES bancaire.comptes_bancaires_reels(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_compte_bancaire_source_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_compte_bancaire_source_id_fkey FOREIGN KEY (compte_bancaire_source_id) REFERENCES bancaire.comptes_bancaires_reels(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_portefeuille_destination_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_portefeuille_destination_id_fkey FOREIGN KEY (portefeuille_destination_id) REFERENCES portefeuille.portefeuilles_virtuels(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_portefeuille_source_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_portefeuille_source_id_fkey FOREIGN KEY (portefeuille_source_id) REFERENCES portefeuille.portefeuilles_virtuels(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_utilisateur_destination_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_utilisateur_destination_id_fkey FOREIGN KEY (utilisateur_destination_id) REFERENCES identite.utilisateurs(id) ON DELETE RESTRICT;


--
-- Name: transactions transactions_utilisateur_source_id_fkey; Type: FK CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactions
    ADD CONSTRAINT transactions_utilisateur_source_id_fkey FOREIGN KEY (utilisateur_source_id) REFERENCES identite.utilisateurs(id) ON DELETE RESTRICT;


--
-- Name: SCHEMA identite; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA identite TO ufaranga;


--
-- Name: SCHEMA localisation; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA localisation TO ufaranga;


--
-- Name: SCHEMA notification; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA notification TO ufaranga;


--
-- Name: TABLE niveaux_kyc; Type: ACL; Schema: identite; Owner: ufaranga
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE identite.niveaux_kyc TO PUBLIC;


--
-- Name: TABLE profils_utilisateurs; Type: ACL; Schema: identite; Owner: postgres
--

GRANT ALL ON TABLE identite.profils_utilisateurs TO ufaranga;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE identite.profils_utilisateurs TO PUBLIC;


--
-- Name: TABLE statuts_utilisateurs; Type: ACL; Schema: identite; Owner: ufaranga
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE identite.statuts_utilisateurs TO PUBLIC;


--
-- Name: TABLE types_utilisateurs; Type: ACL; Schema: identite; Owner: ufaranga
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE identite.types_utilisateurs TO PUBLIC;


--
-- Name: TABLE utilisateurs; Type: ACL; Schema: identite; Owner: ufaranga
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE identite.utilisateurs TO PUBLIC;


--
-- Name: TABLE districts; Type: ACL; Schema: localisation; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE localisation.districts TO ufaranga;


--
-- Name: TABLE pays; Type: ACL; Schema: localisation; Owner: postgres
--

GRANT ALL ON TABLE localisation.pays TO ufaranga;


--
-- Name: TABLE points_de_service; Type: ACL; Schema: localisation; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE localisation.points_de_service TO ufaranga;


--
-- Name: TABLE provinces; Type: ACL; Schema: localisation; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE localisation.provinces TO ufaranga;


--
-- Name: TABLE quartiers; Type: ACL; Schema: localisation; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE localisation.quartiers TO ufaranga;


--
-- Name: TABLE notifications; Type: ACL; Schema: notification; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE notification.notifications TO ufaranga;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: identite; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA identite REVOKE ALL ON SEQUENCES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA identite GRANT ALL ON SEQUENCES  TO ufaranga;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: identite; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA identite REVOKE ALL ON TABLES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA identite GRANT ALL ON TABLES  TO ufaranga;


--
-- PostgreSQL database dump complete
--

