--
-- PostgreSQL database dump
--

\restrict NDEUbOfuqL8L7oQ4Pr2stVAQXYV8JnfYwgzZBnqMmf0fb93OG2a4XtpztZj98pk

-- Dumped from database version 16.13
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: active_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.active_sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token character varying(500) NOT NULL,
    ip_address character varying(45),
    user_agent character varying(500),
    created_at timestamp without time zone NOT NULL,
    expires_at timestamp without time zone NOT NULL
);


--
-- Name: ai_cache; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_cache (
    id uuid NOT NULL,
    cache_key character varying(255) NOT NULL,
    input_hash character varying(255) NOT NULL,
    output_data json,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: ai_decision_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_decision_logs (
    id uuid NOT NULL,
    model_name character varying(100) NOT NULL,
    input_data json,
    output_data json,
    confidence integer,
    execution_time_ms integer,
    user_id uuid,
    entity_type character varying(100),
    entity_id uuid,
    "timestamp" timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: ai_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_embeddings (
    id uuid NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id uuid NOT NULL,
    content text NOT NULL,
    embedding_vector text,
    model_name character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: ai_prompts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ai_prompts (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    prompt_template text NOT NULL,
    module character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    created_by uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: aml_checks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aml_checks (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    check_type character varying(50) NOT NULL,
    result character varying(50) NOT NULL,
    score integer,
    details json,
    checked_at timestamp without time zone NOT NULL,
    checked_by uuid,
    is_active boolean NOT NULL
);


--
-- Name: approval_matrices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.approval_matrices (
    id uuid NOT NULL,
    module character varying(100) NOT NULL,
    action character varying(100) NOT NULL,
    conditions json,
    approvers json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: audit_trails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_trails (
    id uuid NOT NULL,
    user_id uuid,
    action character varying(50) NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id uuid,
    old_values json,
    new_values json,
    ip_address character varying(45),
    "timestamp" timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: branches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.branches (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    code character varying(50) NOT NULL,
    address character varying(500),
    phone character varying(50),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: business_units; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.business_units (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.campaigns (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(50) NOT NULL,
    target_audience json,
    template_id uuid,
    scheduled_date timestamp without time zone,
    status character varying(50) NOT NULL,
    sent_count integer NOT NULL,
    opened_count integer NOT NULL,
    company_id uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: cities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cities (
    id uuid NOT NULL,
    country_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: collateral_releases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collateral_releases (
    id uuid NOT NULL,
    collateral_id uuid NOT NULL,
    released_by uuid NOT NULL,
    released_at timestamp without time zone NOT NULL,
    reason text,
    approved_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: collateral_valuations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collateral_valuations (
    id uuid NOT NULL,
    collateral_id uuid NOT NULL,
    valuation_date timestamp without time zone NOT NULL,
    value numeric(18,2) NOT NULL,
    methodology character varying(100),
    valuator character varying(255),
    next_valuation_date timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: collaterals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collaterals (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    type character varying(100) NOT NULL,
    description text,
    estimated_value numeric(18,2),
    assessed_value numeric(18,2),
    currency_id uuid,
    status character varying(50) NOT NULL,
    registration_number character varying(100),
    location character varying(500),
    expiry_date timestamp without time zone,
    insurance_required boolean NOT NULL,
    notes text,
    images json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: collection_activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collection_activities (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    invoice_id uuid,
    activity_type character varying(50) NOT NULL,
    direction character varying(20),
    subject character varying(255),
    content text,
    scheduled_date timestamp without time zone,
    completed_date timestamp without time zone,
    outcome character varying(100),
    next_action character varying(255),
    next_action_date timestamp without time zone,
    created_by uuid NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: collection_kpis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.collection_kpis (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    metric_name character varying(100) NOT NULL,
    metric_value numeric(18,4) NOT NULL,
    period_start timestamp without time zone NOT NULL,
    period_end timestamp without time zone NOT NULL,
    calculated_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: committee_decisions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.committee_decisions (
    id uuid NOT NULL,
    committee_id uuid NOT NULL,
    application_id uuid NOT NULL,
    decision character varying(50) NOT NULL,
    conditions json,
    voted_by uuid NOT NULL,
    vote character varying(20) NOT NULL,
    vote_date timestamp without time zone NOT NULL,
    comments text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: committee_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.committee_members (
    committee_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role_in_committee character varying(50),
    is_active boolean NOT NULL,
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: communication_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communication_logs (
    id uuid NOT NULL,
    customer_id uuid,
    type character varying(50) NOT NULL,
    direction character varying(20) NOT NULL,
    recipient character varying(255),
    subject character varying(255),
    content text,
    status character varying(50) NOT NULL,
    sent_at timestamp without time zone NOT NULL,
    delivered_at timestamp without time zone,
    read_at timestamp without time zone,
    created_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: communication_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communication_templates (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    type character varying(50) NOT NULL,
    subject character varying(255),
    body text NOT NULL,
    variables json,
    is_active boolean NOT NULL,
    company_id uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.companies (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    registration_number character varying(100),
    tax_id character varying(100),
    address character varying(500),
    phone character varying(50),
    email character varying(255),
    logo character varying(500),
    settings json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: compliance_cases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compliance_cases (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    case_type character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    priority character varying(20) NOT NULL,
    assigned_to uuid,
    due_date timestamp without time zone,
    resolution text,
    resolution_date timestamp without time zone,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: concentration_limits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.concentration_limits (
    id uuid NOT NULL,
    concentration_type character varying(50) NOT NULL,
    category character varying(100) NOT NULL,
    limit_amount numeric(18,2) NOT NULL,
    utilized_amount numeric(18,2) NOT NULL,
    currency_id uuid,
    threshold_percentage numeric(5,2),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.countries (
    id uuid NOT NULL,
    code character varying(2) NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    phone_code character varying(10),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: court_hearings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.court_hearings (
    id uuid NOT NULL,
    case_id uuid NOT NULL,
    hearing_date timestamp without time zone NOT NULL,
    hearing_time timestamp without time zone,
    judge character varying(255),
    outcome text,
    next_date timestamp without time zone,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: credit_analyses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_analyses (
    id uuid NOT NULL,
    application_id uuid NOT NULL,
    customer_id uuid NOT NULL,
    analysis_type character varying(50) NOT NULL,
    financial_data json,
    ratios json,
    cash_flow json,
    risk_rating character varying(20),
    credit_score integer,
    ai_recommendation text,
    analyst_id uuid,
    analyst_notes text,
    analyzed_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: credit_applications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_applications (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    application_type character varying(50) NOT NULL,
    requested_amount numeric(18,2) NOT NULL,
    currency_id uuid,
    purpose text,
    status character varying(50) NOT NULL,
    submitted_by uuid,
    submitted_at timestamp without time zone,
    reviewed_by uuid,
    reviewed_at timestamp without time zone,
    approved_by uuid,
    approved_at timestamp without time zone,
    rejection_reason text,
    conditions json,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: credit_committees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_committees (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    meeting_date timestamp without time zone,
    status character varying(50) NOT NULL,
    minutes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: credit_limit_histories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_limit_histories (
    id uuid NOT NULL,
    limit_id uuid NOT NULL,
    action character varying(50) NOT NULL,
    old_amount numeric(18,2),
    new_amount numeric(18,2),
    reason text,
    changed_by uuid NOT NULL,
    changed_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: credit_limits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_limits (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    limit_type character varying(50) NOT NULL,
    amount numeric(18,2) NOT NULL,
    currency_id uuid,
    utilized_amount numeric(18,2) NOT NULL,
    available_amount numeric(18,2) NOT NULL,
    reserved_amount numeric(18,2) NOT NULL,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    status character varying(50) NOT NULL,
    approved_by uuid,
    approved_at timestamp without time zone,
    parent_limit_id uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: credit_scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.credit_scores (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    score integer NOT NULL,
    factors json,
    calculated_at timestamp without time zone NOT NULL,
    methodology character varying(100),
    version character varying(20),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: currencies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.currencies (
    id uuid NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    symbol character varying(10),
    is_base boolean NOT NULL,
    exchange_rate numeric(18,6) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_addresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_addresses (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    type character varying(50),
    address_line1 character varying(255) NOT NULL,
    address_line2 character varying(255),
    city character varying(100),
    state character varying(100),
    country_id uuid,
    postal_code character varying(20),
    is_primary boolean NOT NULL,
    gps_lat numeric(10,8),
    gps_lng numeric(11,8),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_bank_accounts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_bank_accounts (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    bank_name character varying(255) NOT NULL,
    account_number character varying(100) NOT NULL,
    iban character varying(50),
    swift_code character varying(20),
    currency_id uuid,
    is_primary boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_blacklist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_blacklist (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    reason text NOT NULL,
    added_by uuid NOT NULL,
    added_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: customer_contacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_contacts (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    title character varying(100),
    phone character varying(50),
    mobile character varying(50),
    email character varying(255),
    is_primary boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_documents (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    document_type character varying(100) NOT NULL,
    document_number character varying(100),
    issue_date timestamp without time zone,
    expiry_date timestamp without time zone,
    file_path character varying(500),
    is_verified boolean NOT NULL,
    verified_by uuid,
    verified_at timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_groups (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    parent_id uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_notes (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    note text NOT NULL,
    created_by uuid NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_relationships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_relationships (
    id uuid NOT NULL,
    customer_a_id uuid NOT NULL,
    customer_b_id uuid NOT NULL,
    relationship_type character varying(50) NOT NULL,
    description text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customer_segments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_segments (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    criteria json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customers (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    customer_code character varying(50) NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    trade_name character varying(255),
    business_type character varying(100),
    classification character varying(50),
    risk_category character varying(50),
    sales_region character varying(100),
    salesman_id uuid,
    tax_id character varying(100),
    commercial_register character varying(100),
    vat_number character varying(100),
    status character varying(50) NOT NULL,
    onboarding_status character varying(50) NOT NULL,
    kyc_status character varying(50) NOT NULL,
    credit_score integer,
    ai_score integer,
    metadata json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    created_by uuid,
    updated_by uuid
);


--
-- Name: dashboard_widgets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dashboard_widgets (
    id uuid NOT NULL,
    dashboard_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(50) NOT NULL,
    config json,
    data_source character varying(255),
    "position" json,
    size json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: dashboards; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dashboards (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    layout json,
    widgets json,
    is_default boolean NOT NULL,
    company_id uuid,
    created_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: delegations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.delegations (
    id uuid NOT NULL,
    from_user_id uuid NOT NULL,
    to_user_id uuid NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    permissions json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.departments (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    code character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: digital_signatures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.digital_signatures (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    signature_image character varying(500),
    certificate_data text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: document_approvals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_approvals (
    id uuid NOT NULL,
    document_id uuid NOT NULL,
    approver_id uuid NOT NULL,
    status character varying(50) NOT NULL,
    comments text,
    approved_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: document_folders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_folders (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    parent_id uuid,
    company_id uuid,
    is_shared boolean NOT NULL,
    created_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: document_ocr; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_ocr (
    id uuid NOT NULL,
    document_id uuid NOT NULL,
    extracted_text text,
    confidence integer,
    language character varying(10),
    processed_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: document_versions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_versions (
    id uuid NOT NULL,
    document_id uuid NOT NULL,
    version integer NOT NULL,
    file_path character varying(500) NOT NULL,
    uploaded_by uuid,
    uploaded_at timestamp without time zone NOT NULL,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documents (
    id uuid NOT NULL,
    folder_id uuid,
    name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    file_type character varying(50),
    file_size integer,
    mime_type character varying(100),
    version integer NOT NULL,
    description text,
    tags json,
    metadata json,
    uploaded_by uuid,
    uploaded_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: due_diligence; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.due_diligence (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    type character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    findings json,
    risk_level character varying(20),
    conducted_by uuid,
    conducted_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: exposures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exposures (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    exposure_type character varying(50) NOT NULL,
    amount numeric(18,2) NOT NULL,
    currency_id uuid,
    calculated_at timestamp without time zone NOT NULL,
    details json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: fiscal_years; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fiscal_years (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(100) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    is_active boolean NOT NULL,
    is_closed boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: guarantor_financials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.guarantor_financials (
    id uuid NOT NULL,
    guarantor_id uuid NOT NULL,
    assets json,
    liabilities json,
    income json,
    net_worth numeric(18,2),
    assessment_date timestamp without time zone NOT NULL,
    assessed_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: guarantor_supports; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.guarantor_supports (
    id uuid NOT NULL,
    guarantor_id uuid NOT NULL,
    credit_application_id uuid,
    guarantee_type character varying(50) NOT NULL,
    amount numeric(18,2) NOT NULL,
    currency_id uuid,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    status character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: guarantors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.guarantors (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    relationship_type character varying(100),
    guarantor_type character varying(50) NOT NULL,
    is_individual boolean NOT NULL,
    national_id character varying(100),
    commercial_register character varying(100),
    phone character varying(50),
    email character varying(255),
    address character varying(500),
    status character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: holidays; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.holidays (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    date date NOT NULL,
    is_recurring boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: installment_plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.installment_plans (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    total_amount numeric(18,2) NOT NULL,
    down_payment numeric(18,2) NOT NULL,
    number_of_installments integer NOT NULL,
    frequency character varying(50) NOT NULL,
    status character varying(50) NOT NULL,
    approved_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: installments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.installments (
    id uuid NOT NULL,
    plan_id uuid NOT NULL,
    installment_number integer NOT NULL,
    due_date timestamp without time zone NOT NULL,
    amount numeric(18,2) NOT NULL,
    paid_amount numeric(18,2) NOT NULL,
    status character varying(50) NOT NULL,
    paid_date timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: insurance_claims; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insurance_claims (
    id uuid NOT NULL,
    policy_id uuid NOT NULL,
    claim_number character varying(100) NOT NULL,
    claim_date timestamp without time zone NOT NULL,
    amount numeric(18,2),
    status character varying(50) NOT NULL,
    description text,
    resolution text,
    resolved_date timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: insurance_companies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insurance_companies (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    license_number character varying(100),
    phone character varying(50),
    email character varying(255),
    address character varying(500),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: insurance_policies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.insurance_policies (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    insurance_company_id uuid NOT NULL,
    policy_number character varying(100) NOT NULL,
    policy_type character varying(100) NOT NULL,
    coverage_amount numeric(18,2),
    premium numeric(18,2),
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    status character varying(50) NOT NULL,
    documents json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: invoices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.invoices (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    invoice_number character varying(100) NOT NULL,
    invoice_date timestamp without time zone NOT NULL,
    due_date timestamp without time zone NOT NULL,
    amount numeric(18,2) NOT NULL,
    paid_amount numeric(18,2) NOT NULL,
    balance numeric(18,2) NOT NULL,
    currency_id uuid,
    status character varying(50) NOT NULL,
    aging_days integer NOT NULL,
    sales_order_id character varying(100),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: kyc_records; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kyc_records (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    type character varying(50) NOT NULL,
    status character varying(50) NOT NULL,
    verified_by uuid,
    verified_at timestamp without time zone,
    expires_at timestamp without time zone,
    documents json,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: lawyers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lawyers (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    firm_name character varying(255),
    phone character varying(50),
    email character varying(255),
    specialization character varying(100),
    license_number character varying(100),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: legal_cases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.legal_cases (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    case_number character varying(100) NOT NULL,
    case_type character varying(100) NOT NULL,
    court_name character varying(255),
    filing_date timestamp without time zone NOT NULL,
    status character varying(50) NOT NULL,
    amount_in_dispute numeric(18,2),
    currency_id uuid,
    assigned_lawyer_id uuid,
    next_hearing_date timestamp without time zone,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    created_by uuid,
    updated_by uuid
);


--
-- Name: legal_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.legal_documents (
    id uuid NOT NULL,
    case_id uuid NOT NULL,
    document_type character varying(100) NOT NULL,
    title character varying(255) NOT NULL,
    file_path character varying(500),
    uploaded_by uuid,
    uploaded_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: legal_executions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.legal_executions (
    id uuid NOT NULL,
    case_id uuid NOT NULL,
    execution_type character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    amount numeric(18,2),
    executed_date timestamp without time zone,
    notes text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: legal_judgments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.legal_judgments (
    id uuid NOT NULL,
    case_id uuid NOT NULL,
    judgment_date timestamp without time zone NOT NULL,
    judgment_type character varying(100) NOT NULL,
    amount numeric(18,2),
    description text,
    appeal_deadline timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: legal_timelines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.legal_timelines (
    id uuid NOT NULL,
    case_id uuid NOT NULL,
    event_date timestamp without time zone NOT NULL,
    event_type character varying(100) NOT NULL,
    description text,
    created_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: login_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.login_history (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    ip_address character varying(45),
    user_agent character varying(500),
    login_at timestamp without time zone NOT NULL,
    logout_at timestamp without time zone,
    is_success boolean NOT NULL
);


--
-- Name: menu_configs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.menu_configs (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    icon character varying(50),
    url character varying(255),
    parent_id uuid,
    sort_order character varying(10) NOT NULL,
    is_visible boolean NOT NULL,
    permission_required character varying(100),
    module character varying(100),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: module_configs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.module_configs (
    id uuid NOT NULL,
    module_name character varying(100) NOT NULL,
    is_enabled boolean NOT NULL,
    settings json,
    company_id uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification_preferences (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    notification_type character varying(50) NOT NULL,
    channel character varying(50) NOT NULL,
    is_enabled boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notifications (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    title_ar character varying(255),
    message text NOT NULL,
    message_ar text,
    type character varying(50) NOT NULL,
    entity_type character varying(100),
    entity_id uuid,
    is_read boolean NOT NULL,
    read_at timestamp without time zone,
    action_url character varying(500),
    created_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: pep_checks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pep_checks (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    is_pep boolean NOT NULL,
    pep_type character varying(100),
    details text,
    checked_at timestamp without time zone NOT NULL,
    checked_by uuid,
    is_active boolean NOT NULL
);


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    module character varying(100) NOT NULL,
    action character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: promises_to_pay; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.promises_to_pay (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    promise_date timestamp without time zone NOT NULL,
    amount numeric(18,2) NOT NULL,
    status character varying(50) NOT NULL,
    notes text,
    created_by uuid NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: report_executions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report_executions (
    id uuid NOT NULL,
    template_id uuid NOT NULL,
    executed_by uuid,
    parameters json,
    status character varying(50) NOT NULL,
    file_path character varying(500),
    executed_at timestamp without time zone NOT NULL,
    completed_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: report_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.report_templates (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    name_ar character varying(255),
    description text,
    module character varying(100) NOT NULL,
    query_template text NOT NULL,
    parameters json,
    format character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    company_id uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    title_en character varying(255),
    icon character varying(50),
    color character varying(50)
);


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL,
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id uuid NOT NULL,
    name character varying(100) NOT NULL,
    name_ar character varying(100),
    description text,
    is_system boolean NOT NULL,
    permissions json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sales_invoices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sales_invoices (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    invoice_number character varying(100) NOT NULL,
    customer_id uuid,
    invoice_date timestamp without time zone NOT NULL,
    due_date timestamp without time zone NOT NULL,
    amount numeric(18,2) NOT NULL,
    tax_amount numeric(18,2) DEFAULT 0,
    discount_amount numeric(18,2) DEFAULT 0,
    total_amount numeric(18,2) NOT NULL,
    paid_amount numeric(18,2) DEFAULT 0,
    balance numeric(18,2) NOT NULL,
    currency_id uuid,
    status character varying(50) DEFAULT 'draft'::character varying,
    payment_terms character varying(100),
    notes text,
    items jsonb DEFAULT '[]'::jsonb,
    company_id uuid,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    product_type character varying(255),
    quantity_tons numeric(18,2)
);


--
-- Name: sanction_checks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sanction_checks (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    is_sanctioned boolean NOT NULL,
    list_name character varying(255),
    details text,
    checked_at timestamp without time zone NOT NULL,
    checked_by uuid,
    is_active boolean NOT NULL
);


--
-- Name: sap_business_partners; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sap_business_partners (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    sap_id character varying(100) NOT NULL,
    bp_type character varying(50) NOT NULL,
    sync_status character varying(50) NOT NULL,
    last_synced_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sap_invoices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sap_invoices (
    id uuid NOT NULL,
    invoice_id uuid NOT NULL,
    sap_id character varying(100) NOT NULL,
    sync_status character varying(50) NOT NULL,
    last_synced_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sap_payments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sap_payments (
    id uuid NOT NULL,
    payment_id uuid,
    sap_id character varying(100) NOT NULL,
    sync_status character varying(50) NOT NULL,
    last_synced_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sap_sync_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sap_sync_logs (
    id uuid NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id uuid NOT NULL,
    direction character varying(20) NOT NULL,
    status character varying(50) NOT NULL,
    request_data json,
    response_data json,
    error_message text,
    synced_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: sap_sync_queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sap_sync_queue (
    id uuid NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id uuid NOT NULL,
    action character varying(50) NOT NULL,
    payload json,
    status character varying(50) NOT NULL,
    attempts integer NOT NULL,
    max_attempts integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    processed_at timestamp without time zone,
    is_active boolean,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: security_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.security_events (
    id uuid NOT NULL,
    event_type character varying(100) NOT NULL,
    user_id uuid,
    ip_address character varying(45),
    details json,
    severity character varying(20) NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: settlements; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.settlements (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    original_amount numeric(18,2) NOT NULL,
    settled_amount numeric(18,2) NOT NULL,
    discount_percentage numeric(5,2),
    discount_amount numeric(18,2),
    settlement_date timestamp without time zone NOT NULL,
    approved_by uuid,
    reason text,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: stress_tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stress_tests (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    scenario json,
    results json,
    conducted_at timestamp without time zone NOT NULL,
    conducted_by uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: system_settings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.system_settings (
    id uuid NOT NULL,
    key character varying(255) NOT NULL,
    value text,
    value_type character varying(50) NOT NULL,
    description text,
    module character varying(100),
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: team_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_members (
    team_id uuid NOT NULL,
    user_id uuid NOT NULL,
    role_in_team character varying(50),
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    leader_id uuid,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: user_branches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_branches (
    user_id uuid NOT NULL,
    branch_id uuid NOT NULL,
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: user_departments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_departments (
    user_id uuid NOT NULL,
    department_id uuid NOT NULL,
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    assigned_at timestamp without time zone NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(100) NOT NULL,
    full_name character varying(255) NOT NULL,
    full_name_ar character varying(255),
    phone character varying(50),
    password_hash character varying(255) NOT NULL,
    avatar character varying(500),
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    mfa_enabled boolean NOT NULL,
    mfa_secret character varying(255),
    last_login timestamp without time zone,
    failed_login_attempts integer NOT NULL,
    locked_until timestamp without time zone,
    preferences json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: workflow_instances; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.workflow_instances (
    id uuid NOT NULL,
    template_id uuid NOT NULL,
    entity_type character varying(100) NOT NULL,
    entity_id uuid NOT NULL,
    status character varying(50) NOT NULL,
    current_step integer NOT NULL,
    initiated_by uuid NOT NULL,
    initiated_at timestamp without time zone NOT NULL,
    completed_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: workflow_steps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.workflow_steps (
    id uuid NOT NULL,
    instance_id uuid NOT NULL,
    step_number integer NOT NULL,
    name character varying(255) NOT NULL,
    assignee_id uuid,
    status character varying(50) NOT NULL,
    action character varying(50),
    comments text,
    completed_at timestamp without time zone,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: workflow_templates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.workflow_templates (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    module character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    steps json,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: working_calendars; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.working_calendars (
    id uuid NOT NULL,
    company_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    working_days json,
    settings json,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: write_offs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.write_offs (
    id uuid NOT NULL,
    customer_id uuid NOT NULL,
    amount numeric(18,2) NOT NULL,
    reason text,
    approved_by uuid,
    approved_at timestamp without time zone,
    written_off_at timestamp without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


--
-- Name: active_sessions active_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.active_sessions
    ADD CONSTRAINT active_sessions_pkey PRIMARY KEY (id);


--
-- Name: active_sessions active_sessions_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.active_sessions
    ADD CONSTRAINT active_sessions_token_key UNIQUE (token);


--
-- Name: ai_cache ai_cache_cache_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_cache
    ADD CONSTRAINT ai_cache_cache_key_key UNIQUE (cache_key);


--
-- Name: ai_cache ai_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_cache
    ADD CONSTRAINT ai_cache_pkey PRIMARY KEY (id);


--
-- Name: ai_decision_logs ai_decision_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_decision_logs
    ADD CONSTRAINT ai_decision_logs_pkey PRIMARY KEY (id);


--
-- Name: ai_embeddings ai_embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_embeddings
    ADD CONSTRAINT ai_embeddings_pkey PRIMARY KEY (id);


--
-- Name: ai_prompts ai_prompts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_prompts
    ADD CONSTRAINT ai_prompts_pkey PRIMARY KEY (id);


--
-- Name: aml_checks aml_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aml_checks
    ADD CONSTRAINT aml_checks_pkey PRIMARY KEY (id);


--
-- Name: approval_matrices approval_matrices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.approval_matrices
    ADD CONSTRAINT approval_matrices_pkey PRIMARY KEY (id);


--
-- Name: audit_trails audit_trails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails
    ADD CONSTRAINT audit_trails_pkey PRIMARY KEY (id);


--
-- Name: branches branches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_pkey PRIMARY KEY (id);


--
-- Name: business_units business_units_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_units
    ADD CONSTRAINT business_units_pkey PRIMARY KEY (id);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: collateral_releases collateral_releases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_releases
    ADD CONSTRAINT collateral_releases_pkey PRIMARY KEY (id);


--
-- Name: collateral_valuations collateral_valuations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_valuations
    ADD CONSTRAINT collateral_valuations_pkey PRIMARY KEY (id);


--
-- Name: collaterals collaterals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collaterals
    ADD CONSTRAINT collaterals_pkey PRIMARY KEY (id);


--
-- Name: collection_activities collection_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_activities
    ADD CONSTRAINT collection_activities_pkey PRIMARY KEY (id);


--
-- Name: collection_kpis collection_kpis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_kpis
    ADD CONSTRAINT collection_kpis_pkey PRIMARY KEY (id);


--
-- Name: committee_decisions committee_decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_decisions
    ADD CONSTRAINT committee_decisions_pkey PRIMARY KEY (id);


--
-- Name: committee_members committee_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_members
    ADD CONSTRAINT committee_members_pkey PRIMARY KEY (committee_id, user_id);


--
-- Name: communication_logs communication_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_logs
    ADD CONSTRAINT communication_logs_pkey PRIMARY KEY (id);


--
-- Name: communication_templates communication_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_templates
    ADD CONSTRAINT communication_templates_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: companies companies_registration_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_registration_number_key UNIQUE (registration_number);


--
-- Name: companies companies_tax_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_tax_id_key UNIQUE (tax_id);


--
-- Name: compliance_cases compliance_cases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compliance_cases
    ADD CONSTRAINT compliance_cases_pkey PRIMARY KEY (id);


--
-- Name: concentration_limits concentration_limits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.concentration_limits
    ADD CONSTRAINT concentration_limits_pkey PRIMARY KEY (id);


--
-- Name: countries countries_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_code_key UNIQUE (code);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: court_hearings court_hearings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.court_hearings
    ADD CONSTRAINT court_hearings_pkey PRIMARY KEY (id);


--
-- Name: credit_analyses credit_analyses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_analyses
    ADD CONSTRAINT credit_analyses_pkey PRIMARY KEY (id);


--
-- Name: credit_applications credit_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_pkey PRIMARY KEY (id);


--
-- Name: credit_committees credit_committees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_committees
    ADD CONSTRAINT credit_committees_pkey PRIMARY KEY (id);


--
-- Name: credit_limit_histories credit_limit_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limit_histories
    ADD CONSTRAINT credit_limit_histories_pkey PRIMARY KEY (id);


--
-- Name: credit_limits credit_limits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limits
    ADD CONSTRAINT credit_limits_pkey PRIMARY KEY (id);


--
-- Name: credit_scores credit_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_scores
    ADD CONSTRAINT credit_scores_pkey PRIMARY KEY (id);


--
-- Name: currencies currencies_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_code_key UNIQUE (code);


--
-- Name: currencies currencies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.currencies
    ADD CONSTRAINT currencies_pkey PRIMARY KEY (id);


--
-- Name: customer_addresses customer_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_addresses
    ADD CONSTRAINT customer_addresses_pkey PRIMARY KEY (id);


--
-- Name: customer_bank_accounts customer_bank_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_bank_accounts
    ADD CONSTRAINT customer_bank_accounts_pkey PRIMARY KEY (id);


--
-- Name: customer_blacklist customer_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_blacklist
    ADD CONSTRAINT customer_blacklist_pkey PRIMARY KEY (id);


--
-- Name: customer_contacts customer_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_contacts
    ADD CONSTRAINT customer_contacts_pkey PRIMARY KEY (id);


--
-- Name: customer_documents customer_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_documents
    ADD CONSTRAINT customer_documents_pkey PRIMARY KEY (id);


--
-- Name: customer_groups customer_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_groups
    ADD CONSTRAINT customer_groups_pkey PRIMARY KEY (id);


--
-- Name: customer_notes customer_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_notes
    ADD CONSTRAINT customer_notes_pkey PRIMARY KEY (id);


--
-- Name: customer_relationships customer_relationships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_relationships
    ADD CONSTRAINT customer_relationships_pkey PRIMARY KEY (id);


--
-- Name: customer_segments customer_segments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_segments
    ADD CONSTRAINT customer_segments_pkey PRIMARY KEY (id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: dashboard_widgets dashboard_widgets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_widgets
    ADD CONSTRAINT dashboard_widgets_pkey PRIMARY KEY (id);


--
-- Name: dashboards dashboards_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_pkey PRIMARY KEY (id);


--
-- Name: delegations delegations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delegations
    ADD CONSTRAINT delegations_pkey PRIMARY KEY (id);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: digital_signatures digital_signatures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.digital_signatures
    ADD CONSTRAINT digital_signatures_pkey PRIMARY KEY (id);


--
-- Name: document_approvals document_approvals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_approvals
    ADD CONSTRAINT document_approvals_pkey PRIMARY KEY (id);


--
-- Name: document_folders document_folders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_folders
    ADD CONSTRAINT document_folders_pkey PRIMARY KEY (id);


--
-- Name: document_ocr document_ocr_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_ocr
    ADD CONSTRAINT document_ocr_pkey PRIMARY KEY (id);


--
-- Name: document_versions document_versions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: due_diligence due_diligence_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.due_diligence
    ADD CONSTRAINT due_diligence_pkey PRIMARY KEY (id);


--
-- Name: exposures exposures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exposures
    ADD CONSTRAINT exposures_pkey PRIMARY KEY (id);


--
-- Name: fiscal_years fiscal_years_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fiscal_years
    ADD CONSTRAINT fiscal_years_pkey PRIMARY KEY (id);


--
-- Name: guarantor_financials guarantor_financials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_financials
    ADD CONSTRAINT guarantor_financials_pkey PRIMARY KEY (id);


--
-- Name: guarantor_supports guarantor_supports_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_supports
    ADD CONSTRAINT guarantor_supports_pkey PRIMARY KEY (id);


--
-- Name: guarantors guarantors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantors
    ADD CONSTRAINT guarantors_pkey PRIMARY KEY (id);


--
-- Name: holidays holidays_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_pkey PRIMARY KEY (id);


--
-- Name: installment_plans installment_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.installment_plans
    ADD CONSTRAINT installment_plans_pkey PRIMARY KEY (id);


--
-- Name: installments installments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.installments
    ADD CONSTRAINT installments_pkey PRIMARY KEY (id);


--
-- Name: insurance_claims insurance_claims_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_claims
    ADD CONSTRAINT insurance_claims_pkey PRIMARY KEY (id);


--
-- Name: insurance_companies insurance_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_companies
    ADD CONSTRAINT insurance_companies_pkey PRIMARY KEY (id);


--
-- Name: insurance_policies insurance_policies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_policies
    ADD CONSTRAINT insurance_policies_pkey PRIMARY KEY (id);


--
-- Name: invoices invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);


--
-- Name: kyc_records kyc_records_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kyc_records
    ADD CONSTRAINT kyc_records_pkey PRIMARY KEY (id);


--
-- Name: lawyers lawyers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lawyers
    ADD CONSTRAINT lawyers_pkey PRIMARY KEY (id);


--
-- Name: legal_cases legal_cases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_pkey PRIMARY KEY (id);


--
-- Name: legal_documents legal_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_documents
    ADD CONSTRAINT legal_documents_pkey PRIMARY KEY (id);


--
-- Name: legal_executions legal_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_executions
    ADD CONSTRAINT legal_executions_pkey PRIMARY KEY (id);


--
-- Name: legal_judgments legal_judgments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_judgments
    ADD CONSTRAINT legal_judgments_pkey PRIMARY KEY (id);


--
-- Name: legal_timelines legal_timelines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_timelines
    ADD CONSTRAINT legal_timelines_pkey PRIMARY KEY (id);


--
-- Name: login_history login_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.login_history
    ADD CONSTRAINT login_history_pkey PRIMARY KEY (id);


--
-- Name: menu_configs menu_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.menu_configs
    ADD CONSTRAINT menu_configs_pkey PRIMARY KEY (id);


--
-- Name: module_configs module_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_configs
    ADD CONSTRAINT module_configs_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: pep_checks pep_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pep_checks
    ADD CONSTRAINT pep_checks_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_name_key UNIQUE (name);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: promises_to_pay promises_to_pay_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promises_to_pay
    ADD CONSTRAINT promises_to_pay_pkey PRIMARY KEY (id);


--
-- Name: report_executions report_executions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_executions
    ADD CONSTRAINT report_executions_pkey PRIMARY KEY (id);


--
-- Name: report_templates report_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_templates
    ADD CONSTRAINT report_templates_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: sales_invoices sales_invoices_invoice_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sales_invoices
    ADD CONSTRAINT sales_invoices_invoice_number_key UNIQUE (invoice_number);


--
-- Name: sales_invoices sales_invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sales_invoices
    ADD CONSTRAINT sales_invoices_pkey PRIMARY KEY (id);


--
-- Name: sanction_checks sanction_checks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanction_checks
    ADD CONSTRAINT sanction_checks_pkey PRIMARY KEY (id);


--
-- Name: sap_business_partners sap_business_partners_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_business_partners
    ADD CONSTRAINT sap_business_partners_pkey PRIMARY KEY (id);


--
-- Name: sap_business_partners sap_business_partners_sap_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_business_partners
    ADD CONSTRAINT sap_business_partners_sap_id_key UNIQUE (sap_id);


--
-- Name: sap_invoices sap_invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_invoices
    ADD CONSTRAINT sap_invoices_pkey PRIMARY KEY (id);


--
-- Name: sap_invoices sap_invoices_sap_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_invoices
    ADD CONSTRAINT sap_invoices_sap_id_key UNIQUE (sap_id);


--
-- Name: sap_payments sap_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_payments
    ADD CONSTRAINT sap_payments_pkey PRIMARY KEY (id);


--
-- Name: sap_payments sap_payments_sap_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_payments
    ADD CONSTRAINT sap_payments_sap_id_key UNIQUE (sap_id);


--
-- Name: sap_sync_logs sap_sync_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_sync_logs
    ADD CONSTRAINT sap_sync_logs_pkey PRIMARY KEY (id);


--
-- Name: sap_sync_queue sap_sync_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_sync_queue
    ADD CONSTRAINT sap_sync_queue_pkey PRIMARY KEY (id);


--
-- Name: security_events security_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT security_events_pkey PRIMARY KEY (id);


--
-- Name: settlements settlements_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.settlements
    ADD CONSTRAINT settlements_pkey PRIMARY KEY (id);


--
-- Name: stress_tests stress_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stress_tests
    ADD CONSTRAINT stress_tests_pkey PRIMARY KEY (id);


--
-- Name: system_settings system_settings_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT system_settings_key_key UNIQUE (key);


--
-- Name: system_settings system_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_settings
    ADD CONSTRAINT system_settings_pkey PRIMARY KEY (id);


--
-- Name: team_members team_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_pkey PRIMARY KEY (team_id, user_id);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- Name: user_branches user_branches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_branches
    ADD CONSTRAINT user_branches_pkey PRIMARY KEY (user_id, branch_id);


--
-- Name: user_departments user_departments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_departments
    ADD CONSTRAINT user_departments_pkey PRIMARY KEY (user_id, department_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: workflow_instances workflow_instances_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_instances
    ADD CONSTRAINT workflow_instances_pkey PRIMARY KEY (id);


--
-- Name: workflow_steps workflow_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_pkey PRIMARY KEY (id);


--
-- Name: workflow_templates workflow_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_templates
    ADD CONSTRAINT workflow_templates_pkey PRIMARY KEY (id);


--
-- Name: working_calendars working_calendars_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.working_calendars
    ADD CONSTRAINT working_calendars_pkey PRIMARY KEY (id);


--
-- Name: write_offs write_offs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.write_offs
    ADD CONSTRAINT write_offs_pkey PRIMARY KEY (id);


--
-- Name: ix_customers_customer_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_customers_customer_code ON public.customers USING btree (customer_code);


--
-- Name: ix_invoices_invoice_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_invoices_invoice_number ON public.invoices USING btree (invoice_number);


--
-- Name: ix_legal_cases_case_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_legal_cases_case_number ON public.legal_cases USING btree (case_number);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: active_sessions active_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.active_sessions
    ADD CONSTRAINT active_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: ai_decision_logs ai_decision_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_decision_logs
    ADD CONSTRAINT ai_decision_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: ai_prompts ai_prompts_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ai_prompts
    ADD CONSTRAINT ai_prompts_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: aml_checks aml_checks_checked_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aml_checks
    ADD CONSTRAINT aml_checks_checked_by_fkey FOREIGN KEY (checked_by) REFERENCES public.users(id);


--
-- Name: aml_checks aml_checks_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aml_checks
    ADD CONSTRAINT aml_checks_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: audit_trails audit_trails_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails
    ADD CONSTRAINT audit_trails_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: branches branches_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.branches
    ADD CONSTRAINT branches_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: business_units business_units_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.business_units
    ADD CONSTRAINT business_units_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: campaigns campaigns_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: campaigns campaigns_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.communication_templates(id);


--
-- Name: cities cities_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id);


--
-- Name: collateral_releases collateral_releases_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_releases
    ADD CONSTRAINT collateral_releases_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: collateral_releases collateral_releases_collateral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_releases
    ADD CONSTRAINT collateral_releases_collateral_id_fkey FOREIGN KEY (collateral_id) REFERENCES public.collaterals(id);


--
-- Name: collateral_releases collateral_releases_released_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_releases
    ADD CONSTRAINT collateral_releases_released_by_fkey FOREIGN KEY (released_by) REFERENCES public.users(id);


--
-- Name: collateral_valuations collateral_valuations_collateral_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collateral_valuations
    ADD CONSTRAINT collateral_valuations_collateral_id_fkey FOREIGN KEY (collateral_id) REFERENCES public.collaterals(id);


--
-- Name: collaterals collaterals_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collaterals
    ADD CONSTRAINT collaterals_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: collaterals collaterals_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collaterals
    ADD CONSTRAINT collaterals_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: collection_activities collection_activities_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_activities
    ADD CONSTRAINT collection_activities_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: collection_activities collection_activities_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_activities
    ADD CONSTRAINT collection_activities_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: collection_activities collection_activities_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_activities
    ADD CONSTRAINT collection_activities_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoices(id);


--
-- Name: collection_kpis collection_kpis_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.collection_kpis
    ADD CONSTRAINT collection_kpis_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: committee_decisions committee_decisions_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_decisions
    ADD CONSTRAINT committee_decisions_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.credit_applications(id);


--
-- Name: committee_decisions committee_decisions_committee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_decisions
    ADD CONSTRAINT committee_decisions_committee_id_fkey FOREIGN KEY (committee_id) REFERENCES public.credit_committees(id);


--
-- Name: committee_decisions committee_decisions_voted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_decisions
    ADD CONSTRAINT committee_decisions_voted_by_fkey FOREIGN KEY (voted_by) REFERENCES public.users(id);


--
-- Name: committee_members committee_members_committee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_members
    ADD CONSTRAINT committee_members_committee_id_fkey FOREIGN KEY (committee_id) REFERENCES public.credit_committees(id);


--
-- Name: committee_members committee_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.committee_members
    ADD CONSTRAINT committee_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: communication_logs communication_logs_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_logs
    ADD CONSTRAINT communication_logs_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: communication_logs communication_logs_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_logs
    ADD CONSTRAINT communication_logs_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: communication_templates communication_templates_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_templates
    ADD CONSTRAINT communication_templates_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: compliance_cases compliance_cases_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compliance_cases
    ADD CONSTRAINT compliance_cases_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);


--
-- Name: compliance_cases compliance_cases_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compliance_cases
    ADD CONSTRAINT compliance_cases_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: concentration_limits concentration_limits_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.concentration_limits
    ADD CONSTRAINT concentration_limits_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: court_hearings court_hearings_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.court_hearings
    ADD CONSTRAINT court_hearings_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.legal_cases(id);


--
-- Name: credit_analyses credit_analyses_analyst_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_analyses
    ADD CONSTRAINT credit_analyses_analyst_id_fkey FOREIGN KEY (analyst_id) REFERENCES public.users(id);


--
-- Name: credit_analyses credit_analyses_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_analyses
    ADD CONSTRAINT credit_analyses_application_id_fkey FOREIGN KEY (application_id) REFERENCES public.credit_applications(id);


--
-- Name: credit_analyses credit_analyses_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_analyses
    ADD CONSTRAINT credit_analyses_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: credit_applications credit_applications_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: credit_applications credit_applications_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: credit_applications credit_applications_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: credit_applications credit_applications_reviewed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_reviewed_by_fkey FOREIGN KEY (reviewed_by) REFERENCES public.users(id);


--
-- Name: credit_applications credit_applications_submitted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_applications
    ADD CONSTRAINT credit_applications_submitted_by_fkey FOREIGN KEY (submitted_by) REFERENCES public.users(id);


--
-- Name: credit_committees credit_committees_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_committees
    ADD CONSTRAINT credit_committees_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: credit_limit_histories credit_limit_histories_changed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limit_histories
    ADD CONSTRAINT credit_limit_histories_changed_by_fkey FOREIGN KEY (changed_by) REFERENCES public.users(id);


--
-- Name: credit_limit_histories credit_limit_histories_limit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limit_histories
    ADD CONSTRAINT credit_limit_histories_limit_id_fkey FOREIGN KEY (limit_id) REFERENCES public.credit_limits(id);


--
-- Name: credit_limits credit_limits_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limits
    ADD CONSTRAINT credit_limits_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: credit_limits credit_limits_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limits
    ADD CONSTRAINT credit_limits_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: credit_limits credit_limits_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limits
    ADD CONSTRAINT credit_limits_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: credit_limits credit_limits_parent_limit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_limits
    ADD CONSTRAINT credit_limits_parent_limit_id_fkey FOREIGN KEY (parent_limit_id) REFERENCES public.credit_limits(id);


--
-- Name: credit_scores credit_scores_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.credit_scores
    ADD CONSTRAINT credit_scores_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_addresses customer_addresses_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_addresses
    ADD CONSTRAINT customer_addresses_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id);


--
-- Name: customer_addresses customer_addresses_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_addresses
    ADD CONSTRAINT customer_addresses_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_bank_accounts customer_bank_accounts_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_bank_accounts
    ADD CONSTRAINT customer_bank_accounts_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: customer_bank_accounts customer_bank_accounts_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_bank_accounts
    ADD CONSTRAINT customer_bank_accounts_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_blacklist customer_blacklist_added_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_blacklist
    ADD CONSTRAINT customer_blacklist_added_by_fkey FOREIGN KEY (added_by) REFERENCES public.users(id);


--
-- Name: customer_blacklist customer_blacklist_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_blacklist
    ADD CONSTRAINT customer_blacklist_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_contacts customer_contacts_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_contacts
    ADD CONSTRAINT customer_contacts_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_documents customer_documents_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_documents
    ADD CONSTRAINT customer_documents_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_documents customer_documents_verified_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_documents
    ADD CONSTRAINT customer_documents_verified_by_fkey FOREIGN KEY (verified_by) REFERENCES public.users(id);


--
-- Name: customer_groups customer_groups_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_groups
    ADD CONSTRAINT customer_groups_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: customer_groups customer_groups_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_groups
    ADD CONSTRAINT customer_groups_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.customer_groups(id);


--
-- Name: customer_notes customer_notes_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_notes
    ADD CONSTRAINT customer_notes_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: customer_notes customer_notes_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_notes
    ADD CONSTRAINT customer_notes_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: customer_relationships customer_relationships_customer_a_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_relationships
    ADD CONSTRAINT customer_relationships_customer_a_id_fkey FOREIGN KEY (customer_a_id) REFERENCES public.customers(id);


--
-- Name: customer_relationships customer_relationships_customer_b_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_relationships
    ADD CONSTRAINT customer_relationships_customer_b_id_fkey FOREIGN KEY (customer_b_id) REFERENCES public.customers(id);


--
-- Name: customer_segments customer_segments_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_segments
    ADD CONSTRAINT customer_segments_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: customers customers_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: customers customers_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: customers customers_salesman_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_salesman_id_fkey FOREIGN KEY (salesman_id) REFERENCES public.users(id);


--
-- Name: customers customers_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(id);


--
-- Name: dashboard_widgets dashboard_widgets_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboard_widgets
    ADD CONSTRAINT dashboard_widgets_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- Name: dashboards dashboards_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: dashboards dashboards_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: delegations delegations_from_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delegations
    ADD CONSTRAINT delegations_from_user_id_fkey FOREIGN KEY (from_user_id) REFERENCES public.users(id);


--
-- Name: delegations delegations_to_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delegations
    ADD CONSTRAINT delegations_to_user_id_fkey FOREIGN KEY (to_user_id) REFERENCES public.users(id);


--
-- Name: departments departments_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: digital_signatures digital_signatures_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.digital_signatures
    ADD CONSTRAINT digital_signatures_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: document_approvals document_approvals_approver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_approvals
    ADD CONSTRAINT document_approvals_approver_id_fkey FOREIGN KEY (approver_id) REFERENCES public.users(id);


--
-- Name: document_approvals document_approvals_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_approvals
    ADD CONSTRAINT document_approvals_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id);


--
-- Name: document_folders document_folders_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_folders
    ADD CONSTRAINT document_folders_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: document_folders document_folders_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_folders
    ADD CONSTRAINT document_folders_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: document_folders document_folders_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_folders
    ADD CONSTRAINT document_folders_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.document_folders(id);


--
-- Name: document_ocr document_ocr_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_ocr
    ADD CONSTRAINT document_ocr_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id);


--
-- Name: document_versions document_versions_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id);


--
-- Name: document_versions document_versions_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_versions
    ADD CONSTRAINT document_versions_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id);


--
-- Name: documents documents_folder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_folder_id_fkey FOREIGN KEY (folder_id) REFERENCES public.document_folders(id);


--
-- Name: documents documents_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id);


--
-- Name: due_diligence due_diligence_conducted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.due_diligence
    ADD CONSTRAINT due_diligence_conducted_by_fkey FOREIGN KEY (conducted_by) REFERENCES public.users(id);


--
-- Name: due_diligence due_diligence_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.due_diligence
    ADD CONSTRAINT due_diligence_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: exposures exposures_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exposures
    ADD CONSTRAINT exposures_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: exposures exposures_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exposures
    ADD CONSTRAINT exposures_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: fiscal_years fiscal_years_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fiscal_years
    ADD CONSTRAINT fiscal_years_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: guarantor_financials guarantor_financials_assessed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_financials
    ADD CONSTRAINT guarantor_financials_assessed_by_fkey FOREIGN KEY (assessed_by) REFERENCES public.users(id);


--
-- Name: guarantor_financials guarantor_financials_guarantor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_financials
    ADD CONSTRAINT guarantor_financials_guarantor_id_fkey FOREIGN KEY (guarantor_id) REFERENCES public.guarantors(id);


--
-- Name: guarantor_supports guarantor_supports_credit_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_supports
    ADD CONSTRAINT guarantor_supports_credit_application_id_fkey FOREIGN KEY (credit_application_id) REFERENCES public.credit_applications(id);


--
-- Name: guarantor_supports guarantor_supports_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_supports
    ADD CONSTRAINT guarantor_supports_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: guarantor_supports guarantor_supports_guarantor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantor_supports
    ADD CONSTRAINT guarantor_supports_guarantor_id_fkey FOREIGN KEY (guarantor_id) REFERENCES public.guarantors(id);


--
-- Name: guarantors guarantors_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.guarantors
    ADD CONSTRAINT guarantors_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: holidays holidays_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.holidays
    ADD CONSTRAINT holidays_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: installment_plans installment_plans_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.installment_plans
    ADD CONSTRAINT installment_plans_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: installment_plans installment_plans_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.installment_plans
    ADD CONSTRAINT installment_plans_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: installments installments_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.installments
    ADD CONSTRAINT installments_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.installment_plans(id);


--
-- Name: insurance_claims insurance_claims_policy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_claims
    ADD CONSTRAINT insurance_claims_policy_id_fkey FOREIGN KEY (policy_id) REFERENCES public.insurance_policies(id);


--
-- Name: insurance_policies insurance_policies_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_policies
    ADD CONSTRAINT insurance_policies_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: insurance_policies insurance_policies_insurance_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.insurance_policies
    ADD CONSTRAINT insurance_policies_insurance_company_id_fkey FOREIGN KEY (insurance_company_id) REFERENCES public.insurance_companies(id);


--
-- Name: invoices invoices_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: invoices invoices_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: kyc_records kyc_records_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kyc_records
    ADD CONSTRAINT kyc_records_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: kyc_records kyc_records_verified_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kyc_records
    ADD CONSTRAINT kyc_records_verified_by_fkey FOREIGN KEY (verified_by) REFERENCES public.users(id);


--
-- Name: legal_cases legal_cases_assigned_lawyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_assigned_lawyer_id_fkey FOREIGN KEY (assigned_lawyer_id) REFERENCES public.lawyers(id);


--
-- Name: legal_cases legal_cases_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: legal_cases legal_cases_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: legal_cases legal_cases_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: legal_cases legal_cases_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_cases
    ADD CONSTRAINT legal_cases_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(id);


--
-- Name: legal_documents legal_documents_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_documents
    ADD CONSTRAINT legal_documents_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.legal_cases(id);


--
-- Name: legal_documents legal_documents_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_documents
    ADD CONSTRAINT legal_documents_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id);


--
-- Name: legal_executions legal_executions_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_executions
    ADD CONSTRAINT legal_executions_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.legal_cases(id);


--
-- Name: legal_judgments legal_judgments_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_judgments
    ADD CONSTRAINT legal_judgments_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.legal_cases(id);


--
-- Name: legal_timelines legal_timelines_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_timelines
    ADD CONSTRAINT legal_timelines_case_id_fkey FOREIGN KEY (case_id) REFERENCES public.legal_cases(id);


--
-- Name: legal_timelines legal_timelines_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.legal_timelines
    ADD CONSTRAINT legal_timelines_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: login_history login_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.login_history
    ADD CONSTRAINT login_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: menu_configs menu_configs_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.menu_configs
    ADD CONSTRAINT menu_configs_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.menu_configs(id);


--
-- Name: module_configs module_configs_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_configs
    ADD CONSTRAINT module_configs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: pep_checks pep_checks_checked_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pep_checks
    ADD CONSTRAINT pep_checks_checked_by_fkey FOREIGN KEY (checked_by) REFERENCES public.users(id);


--
-- Name: pep_checks pep_checks_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pep_checks
    ADD CONSTRAINT pep_checks_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: promises_to_pay promises_to_pay_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promises_to_pay
    ADD CONSTRAINT promises_to_pay_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- Name: promises_to_pay promises_to_pay_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promises_to_pay
    ADD CONSTRAINT promises_to_pay_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: report_executions report_executions_executed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_executions
    ADD CONSTRAINT report_executions_executed_by_fkey FOREIGN KEY (executed_by) REFERENCES public.users(id);


--
-- Name: report_executions report_executions_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_executions
    ADD CONSTRAINT report_executions_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.report_templates(id);


--
-- Name: report_templates report_templates_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.report_templates
    ADD CONSTRAINT report_templates_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: sales_invoices sales_invoices_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sales_invoices
    ADD CONSTRAINT sales_invoices_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: sales_invoices sales_invoices_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sales_invoices
    ADD CONSTRAINT sales_invoices_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currencies(id);


--
-- Name: sales_invoices sales_invoices_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sales_invoices
    ADD CONSTRAINT sales_invoices_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: sanction_checks sanction_checks_checked_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanction_checks
    ADD CONSTRAINT sanction_checks_checked_by_fkey FOREIGN KEY (checked_by) REFERENCES public.users(id);


--
-- Name: sanction_checks sanction_checks_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sanction_checks
    ADD CONSTRAINT sanction_checks_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: sap_business_partners sap_business_partners_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_business_partners
    ADD CONSTRAINT sap_business_partners_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: sap_invoices sap_invoices_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sap_invoices
    ADD CONSTRAINT sap_invoices_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoices(id);


--
-- Name: security_events security_events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT security_events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: settlements settlements_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.settlements
    ADD CONSTRAINT settlements_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: settlements settlements_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.settlements
    ADD CONSTRAINT settlements_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: stress_tests stress_tests_conducted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stress_tests
    ADD CONSTRAINT stress_tests_conducted_by_fkey FOREIGN KEY (conducted_by) REFERENCES public.users(id);


--
-- Name: team_members team_members_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id);


--
-- Name: team_members team_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_members
    ADD CONSTRAINT team_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: teams teams_leader_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_leader_id_fkey FOREIGN KEY (leader_id) REFERENCES public.users(id);


--
-- Name: user_branches user_branches_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_branches
    ADD CONSTRAINT user_branches_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.branches(id);


--
-- Name: user_branches user_branches_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_branches
    ADD CONSTRAINT user_branches_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_departments user_departments_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_departments
    ADD CONSTRAINT user_departments_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id);


--
-- Name: user_departments user_departments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_departments
    ADD CONSTRAINT user_departments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: workflow_instances workflow_instances_initiated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_instances
    ADD CONSTRAINT workflow_instances_initiated_by_fkey FOREIGN KEY (initiated_by) REFERENCES public.users(id);


--
-- Name: workflow_instances workflow_instances_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_instances
    ADD CONSTRAINT workflow_instances_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.workflow_templates(id);


--
-- Name: workflow_steps workflow_steps_assignee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_assignee_id_fkey FOREIGN KEY (assignee_id) REFERENCES public.users(id);


--
-- Name: workflow_steps workflow_steps_instance_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_instance_id_fkey FOREIGN KEY (instance_id) REFERENCES public.workflow_instances(id);


--
-- Name: working_calendars working_calendars_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.working_calendars
    ADD CONSTRAINT working_calendars_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: write_offs write_offs_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.write_offs
    ADD CONSTRAINT write_offs_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- Name: write_offs write_offs_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.write_offs
    ADD CONSTRAINT write_offs_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- PostgreSQL database dump complete
--

\unrestrict NDEUbOfuqL8L7oQ4Pr2stVAQXYV8JnfYwgzZBnqMmf0fb93OG2a4XtpztZj98pk

