"""Dropdown and preset options for intake form fields."""

from __future__ import annotations

WAITING_PERIOD_OPTIONS: list[tuple[str, str]] = [
    ("", "— Not sure — check policy"),
    ("7 days", "7 days"),
    ("14 days", "14 days"),
    ("1 month", "1 month"),
    ("2 months", "2 months"),
    ("3 months", "3 months"),
    ("6 months", "6 months"),
    ("12 months", "12 months (1 year)"),
    ("__other__", "Other — specify below"),
]

WAITING_PERIOD_STANDARD = {value for value, _ in WAITING_PERIOD_OPTIONS if value and value != "__other__"}

# Main insurers shown as logo tiles on the private-plan policy screen.
# nfo_name matches NFO Life Insurance Division participant list.
POLICY_INSURER_TILES: list[dict[str, str]] = [
    {
        "id": "old_mutual",
        "name": "Old Mutual",
        "nfo_name": "Old Mutual Life Assurance Company (SA) Limited",
        "mark": "OM",
        "accent": "#009677",
    },
    {
        "id": "sanlam",
        "name": "Sanlam",
        "nfo_name": "Sanlam Life Insurance Limited",
        "mark": "S",
        "accent": "#0033A0",
    },
    {
        "id": "liberty",
        "name": "Liberty",
        "nfo_name": "Liberty Group Limited",
        "mark": "L",
        "accent": "#E31837",
    },
    {
        "id": "momentum",
        "name": "Momentum",
        "nfo_name": "MMI Group Limited",
        "mark": "M",
        "accent": "#00A9A5",
    },
    {
        "id": "discovery",
        "name": "Discovery",
        "nfo_name": "Discovery Life Limited",
        "mark": "D",
        "accent": "#582C83",
    },
    {
        "id": "hollard",
        "name": "Hollard",
        "nfo_name": "Hollard Life Assurance Company Limited",
        "mark": "H",
        "accent": "#F36F21",
    },
    {
        "id": "absa",
        "name": "Absa Life",
        "nfo_name": "ABSA Life Limited",
        "mark": "A",
        "accent": "#F03333",
    },
    {
        "id": "pps",
        "name": "PPS",
        "nfo_name": "Professional Provident Society Insurance Company Limited",
        "mark": "PPS",
        "accent": "#1B365D",
    },
    {"id": "other", "name": "Other", "nfo_name": "", "mark": "…", "accent": "#64748b"},
]

# Large card tiles for the claim-stage intake screen (keys match engine.CLAIM_STAGES).
CLAIM_STAGE_TILES: list[dict[str, str]] = [
    {
        "id": "preparing",
        "label": "Preparing claim",
        "icon": "📋",
        "accent": "#2563eb",
        "focus": "Gathering policy, medical, and employment records before first submission",
        "tools": "Guided intake · document vault · policy reader · evidence gaps",
    },
    {
        "id": "waiting_period",
        "label": "Waiting-period evidence",
        "icon": "⏳",
        "accent": "#0891b2",
        "focus": "Proving continuous incapacity through your policy waiting period",
        "tools": "Timeline · functional-capacity builder · absence continuity",
    },
    {
        "id": "assessment",
        "label": "Insurer assessment",
        "icon": "🔍",
        "accent": "#7c3aed",
        "focus": "Claim lodged with insurer — awaiting decision or further evidence requests",
        "tools": "Access requests · further-medical-evidence tracking",
    },
    {
        "id": "rejected",
        "label": "Rejected claim",
        "icon": "✋",
        "accent": "#dc2626",
        "focus": "Rejection received — preparing internal review or escalation",
        "tools": "Rejection explainer · review-ground matrix · record access",
    },
    {
        "id": "internal_review",
        "label": "Internal review",
        "icon": "📝",
        "accent": "#ea580c",
        "focus": "Challenging the decision through the insurer's internal review process",
        "tools": "Review pack · issue matrix · cure evidence plan",
    },
    {
        "id": "ombud",
        "label": "Ombud complaint",
        "icon": "⚖️",
        "accent": "#4f46e5",
        "focus": "Escalating to NFOSA, FSCA, or industry ombud after insurer review",
        "tools": "Escalation pack · prejudice summary · deadline tracker",
    },
    {
        "id": "record_access",
        "label": "Record-access dispute",
        "icon": "📂",
        "accent": "#0d9488",
        "focus": "POPIA/PAIA non-response or inadequate disclosure from insurer or employer",
        "tools": "Access-request follow-ups · non-response notices",
    },
    {
        "id": "professional",
        "label": "Professional review",
        "icon": "👥",
        "accent": "#64748b",
        "focus": "Attorney, OT, doctor, or adviser actively assisting your claim",
        "tools": "Shared workspace · reviewer routing · export pack",
    },
]