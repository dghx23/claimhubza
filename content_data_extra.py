"""Fallback stand-in for the (never committed) claimguard-site content data.

See ``content_data.py`` for why this exists — the real tables live in a
sibling ``claimguard-site`` project that was never part of this repo.
"""

from __future__ import annotations

AI_COMPONENTS: list[tuple[str, str]] = []
BETA_INTAKE_FIELDS: list[tuple[str, str]] = []
BETA_OUTPUTS: list[tuple[str, str]] = []
BETA_SUCCESS: list[tuple[str, str]] = []
CLAIM_ONTOLOGY: list[tuple[str, str]] = []
CLAIM_STAGES: list[tuple[str, str]] = [
    ("preparing", "Building the file before first complete submission"),
    ("waiting_period", "Continuous incapacity running towards benefit start"),
    ("assessment", "Insurer assessing the file they hold"),
    ("rejected", "Adverse decision received"),
    ("internal_review", "Reassessment requested"),
    ("ombud", "NFO / ombud complaint"),
    ("record_access", "Records held by employer or insurer still missing"),
    ("professional", "Advocate, attorney, or independent review"),
]
CORE_TEMPLATES: list[tuple[str, str]] = []
FOUNDER_INSIGHTS: list[tuple[str, str]] = []
GTM_CHANNELS: list[tuple[str, str]] = []
METRICS_DETAIL: list[tuple[str, str]] = []
MVP_MODULE_DETAILS: dict[str, dict] = {}
PRICING_TIERS: list[tuple[str, str]] = []
PROBLEM_GAPS: list[tuple[str, str, str]] = [
    (
        "Claim-process knowledge gap",
        "Notice, forms, complete submission, Date of Absence, and waiting period are different rungs — treated as one.",
        "Stage the file on a date ladder before you argue the medicine.",
    ),
    (
        "Functional evidence gap",
        "Medical records describe the body; policies ask whether you can perform material duties.",
        "Duty-impact matrix: symptom → blocked duty, not diagnosis labels.",
    ),
    (
        "Record-control gap",
        "Decisive files sit with HR, payroll, or the insurer's claim file — not with you.",
        "Name the holder and send the access request; do not wait for rejection.",
    ),
    (
        "Timing gap",
        "Employer 'enough' is not insurer 'enough'. Deadlines surface after the clock has started.",
        "Capture who said what was enough, on which date, under which clause.",
    ),
    (
        "Language gap",
        "Everyday, medical, functional, and policy words are treated as synonyms.",
        "Language map: illness ≠ incapacity; diagnosis ≠ disability.",
    ),
    (
        "Power gap",
        "Insurers run this process every day; you run it once while unwell.",
        "Same artefacts they use: chronology, index, issue matrix, numbered pack.",
    ),
]
RISKS_TABLE: list[tuple[str, str]] = []
ROADMAP_DETAIL: list[tuple[str, str]] = []
TERM_CARD_EXAMPLES: list[tuple[str, str]] = []
TRUST_GUARDRAILS: list[tuple[str, str]] = []
WEBSITE_IA: list[tuple[str, str]] = []
