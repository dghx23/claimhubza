"""Canonical ClaimHub / ClaimBuddy product model for South Africa.

This module is presentation-safe shared product architecture. It keeps the
marketing site, ClaimBuddy, ClaimHub professional portal and Sentrix backend
aligned around the same concepts without moving live case state out of db.py.
"""

MARKET_CHALLENGES = [
    {
        "id": "scattered",
        "label": "Information is scattered",
        "summary": "Policy wording, medical evidence, employment records and correspondence can live in different places.",
    },
    {
        "id": "roles",
        "label": "Roles are disconnected",
        "summary": "Claimants, employers, advisers, clinicians and claims teams may each hold a different part of the case.",
    },
    {
        "id": "translation",
        "label": "Evidence is hard to translate",
        "summary": "Medical facts do not automatically explain functional impact, material duties or the policy test.",
    },
    {
        "id": "process",
        "label": "Processes are hard to follow",
        "summary": "Requests, deadlines and decisions can become difficult to track across email and separate systems.",
    },
]

ZA_COVER_CONTEXT = [
    {
        "id": "group",
        "label": "Group income protection",
        "summary": "Cover linked to employment or another group arrangement.",
        "holders": "Employer / HR may hold policy, payroll, duties and absence records.",
    },
    {
        "id": "individual",
        "label": "Individual income protection",
        "summary": "A policy arranged for the individual.",
        "holders": "The claimant or adviser may hold the starting policy information.",
    },
]

INITIATION_PATHS = [
    {
        "id": "claimant",
        "label": "Claimant",
        "title": "Starts in ClaimBuddy",
        "summary": "Creates the claim workspace, adds records and invites professionals when needed.",
        "surface": "claimbuddy",
    },
    {
        "id": "employer",
        "label": "Employer / HR",
        "title": "Starts from employment and group-cover information",
        "summary": "May begin with duties, absence, payroll or group-policy information. The claimant is then connected through ClaimBuddy.",
        "surface": "claimhub",
        "role": "employer",
    },
    {
        "id": "adviser",
        "label": "Adviser",
        "title": "Starts from policy, chronology or an existing decision",
        "summary": "May begin organising the case for a client. The claimant remains visible in the same case through ClaimBuddy.",
        "surface": "claimhub",
        "role": "adviser",
    },
    {
        "id": "existing",
        "label": "Existing claim",
        "title": "Bring an already-open claim into one record",
        "summary": "A submitted or declined claim can be organised without starting the insurance process again.",
        "surface": "claimbuddy",
    },
]

CLAIM_RECORD_DOMAINS = [
    "Policy",
    "Timeline",
    "Function",
    "Evidence",
    "Requests",
    "Decision",
]

CLAIMBUDDY_MODULES = [
    "Guided intake",
    "Documents",
    "Policy reader",
    "Timeline",
    "Function & duties",
    "Clinical questions",
    "Evidence gaps",
    "Decision / rejection",
    "Letters",
    "Claim pack",
    "Share access",
]

CLAIMHUB_WORKSPACES = [
    {
        "role": "clinician",
        "label": "Clinician",
        "summary": "Medical and functional evidence.",
    },
    {
        "role": "employer",
        "label": "Employer / HR",
        "summary": "Employment facts, material duties and absence records.",
    },
    {
        "role": "adviser",
        "label": "Adviser",
        "summary": "Policy, chronology, evidence gaps and review support.",
    },
    {
        "role": "reviewer",
        "label": "Claims team",
        "summary": "Claimant-authorised evidence, requests and decisions.",
    },
]

RESOURCE_GROUPS = [
    {
        "id": "understand",
        "label": "Understand the claim",
        "items": [
            ("Workflow & claim stages", "resources_workflow"),
            ("Claim glossary", "resources_glossary"),
            ("Language map", "resources_language_map"),
            ("Core policy terms", "resources_terms"),
            ("Disability definitions", "resources_disability_definitions"),
            ("Policy traps", "resources_traps"),
        ],
    },
    {
        "id": "evidence",
        "label": "Build the evidence",
        "items": [
            ("Evidence-gap library", "resources_evidence_gaps"),
            ("ClinicalAtlas ZA", "resources_clinical_atlas"),
            ("Clinician directory", "resources_clinical_atlas_clinicians"),
            ("Medical scheme reference", "resources_clinical_atlas_medical_aids"),
            ("Medicine schedules", "resources_medicine_schedules"),
            ("Claim modules", "resources_modules"),
        ],
    },
    {
        "id": "institutions",
        "label": "Know the institutions",
        "items": [
            ("Life insurer directory", "resources_life_insurers"),
            ("Reference catalogue", "reference_index"),
            ("News & updates", "resources_news"),
            ("Reference wiki", "resources_wiki"),
        ],
    },
    {
        "id": "review",
        "label": "Review, dispute & escalation",
        "items": [
            ("NFO dispute pathway", "resources_nfosa_dispute"),
            ("Ombud guidance & precedent", "resources_precedent"),
            ("Decision and process traps", "resources_traps"),
            ("Evidence gaps", "resources_evidence_gaps"),
        ],
    },
]

PRODUCT_SURFACES = [
    {
        "id": "marketing",
        "label": "Marketing site",
        "domain": "claimhub.co.za",
        "purpose": "Explain the model, cover context, entry paths and resources.",
    },
    {
        "id": "claimbuddy",
        "label": "ClaimBuddy",
        "domain": "buddy.claimhub.co.za",
        "purpose": "Claimant application and claimant visibility into every case.",
    },
    {
        "id": "claimhub",
        "label": "ClaimHub",
        "domain": "claimhub.co.za",
        "purpose": "Professional role workspaces around the same shared case.",
    },
]

INTERNAL_LAYERS = [
    {
        "id": "riskatlas",
        "label": "RiskAtlas / Core ZA",
        "purpose": "Reference intelligence for policy, clinical, occupational, regulatory and dispute context.",
    },
    {
        "id": "sentrix",
        "label": "Sentrix Digital",
        "purpose": "Builds and operates RiskAtlas, ClaimHub and ClaimBuddy, and provides the internal operational/control-room layer.",
    },
]

PRODUCT_PRINCIPLES = {
    "headline": "Different ways in. One shared claim. Claimant always included.",
    "claimant_visibility": (
        "ClaimBuddy is the claimant-facing side of every case, regardless of who initiates it."
    ),
    "shared_record": (
        "ClaimBuddy and ClaimHub are views over the same case record, not separate copies."
    ),
    "access": (
        "Professional participation is bounded by case membership, role capability, claimant-authorised scope and explicit document sharing."
    ),
    "riskatlas": (
        "RiskAtlas supplies the policy, clinical, occupational, insurer and dispute intelligence used by ClaimHub Resources, ClaimBuddy and ClaimHub."
    ),
    "sentrix": (
        "Sentrix Digital builds and operates RiskAtlas, ClaimHub and ClaimBuddy."
    ),
}

PRODUCT_MODEL = {
    "market": "South Africa",
    "market_challenges": MARKET_CHALLENGES,
    "cover_context": ZA_COVER_CONTEXT,
    "initiation_paths": INITIATION_PATHS,
    "record_domains": CLAIM_RECORD_DOMAINS,
    "claimbuddy_modules": CLAIMBUDDY_MODULES,
    "claimhub_workspaces": CLAIMHUB_WORKSPACES,
    "resource_groups": RESOURCE_GROUPS,
    "surfaces": PRODUCT_SURFACES,
    "internal_layers": INTERNAL_LAYERS,
    "principles": PRODUCT_PRINCIPLES,
}
