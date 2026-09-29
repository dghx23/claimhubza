"""National Financial Ombud Scheme (NFO) dispute process — resources hub."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from news_articles import link_article_text

_DATA_DIR = Path(__file__).resolve().parent / "data"

NFO_CONTACT = {
    "phone": "0860 800 900",
    "whatsapp": "076 574 8055",
    "email": "info@nfosa.co.za",
    "website": "https://nfosa.co.za/",
    "submit": "https://www.nfosa.co.za/submit-a-complaint/",
    "flowchart": "https://www.nfosa.co.za/complaints-process-flowchart/",
    "track": "https://www.nfosa.co.za/track-your-complaint/",
    "life_participants": "https://www.nfosa.co.za/participants/life-insurance-division/",
}

PROCESS_STEPS: list[dict[str, Any]] = [
    {
        "id": "step-1",
        "number": 1,
        "title": "Contact your Financial Services Provider first",
        "summary": (
            "Before submitting to the NFO, complain to your insurer in writing. "
            "You need a written internal decision with reasons if escalation is required."
        ),
        "detail": (
            "Insurers must have an internal complaints process. Under the Policyholder Protection Rules, "
            "claims must be decided in a reasonable period with written notification of repudiation or dispute. "
            "Keep all correspondence — the NFO will ask for it."
        ),
        "nfosa_note": "Mandatory first step — transfers without prior insurer contact are referred back.",
    },
    {
        "id": "step-2",
        "number": 2,
        "title": "Submit your complaint to the NFO",
        "summary": (
            "Online form (preferred), phone, WhatsApp, email, post, or walk-in. "
            "Free service in any official language."
        ),
        "detail": (
            "Provide participant name, policy/account number, contact details, factual summary, and copies of "
            "all relevant correspondence and supporting documents. Written mandate required if a representative acts for you."
        ),
        "nfosa_note": "Acknowledgement typically within one week.",
    },
    {
        "id": "step-3",
        "number": 3,
        "title": "Acknowledgement and initial assessment",
        "summary": "Jurisdiction confirmed; vulnerable complainant support offered; insurer notified.",
        "detail": (
            "The NFO logs the complaint, confirms it falls within scheme rules, and requests the participant's "
            "full response and claim file. Vulnerable complainants may receive assistance completing forms."
        ),
        "nfosa_note": "Once lodged, correspond with the NFO unless told otherwise (except during insurer transfer).",
    },
    {
        "id": "step-4",
        "number": 4,
        "title": "Investigation and information gathering",
        "summary": "Both parties submit evidence; NFO reviews policy terms, records, and regulatory compliance.",
        "detail": (
            "For disability and income protection claims, the Life Insurance Division examines whether medical "
            "evidence maps to the policy's disability definition and whether causation and materiality were fairly assessed."
        ),
        "nfosa_note": "The NFO may request further information from either party at any stage.",
    },
    {
        "id": "step-5",
        "number": 5,
        "title": "Mediation / conciliation",
        "summary": "Settlement discussions facilitated between complainant and participant.",
        "detail": (
            "Many life insurance disputes resolve here. The Life Insurance Division has recovered substantial "
            "benefits for consumers on previously declined claims through mediated settlements."
        ),
        "nfosa_note": "Confidentiality rules apply while the complaint is under investigation.",
    },
    {
        "id": "step-6",
        "number": 6,
        "title": "Formal determination or ruling",
        "summary": "Provisional then final findings — recommendations, settlements, or binding rulings where appropriate.",
        "detail": (
            "If mediation fails, a formal investigation concludes with a provisional determination. "
            "You may respond with concerns before a final determination. Leave to appeal is limited and not a full rehearing."
        ),
        "nfosa_note": "No strict monetary cap on most life insurance complaints.",
    },
    {
        "id": "step-7",
        "number": 7,
        "title": "Closure and tracking",
        "summary": "Complaint closed; track status online; complex medical cases may take longer.",
        "detail": (
            "Simple matters may resolve in weeks to a few months. Disability cases with causation disputes "
            "or specialist evidence often require extended review. Continue paying premiums unless the insurer agrees otherwise."
        ),
        "nfosa_note": "Feedback provided when there is something new to report.",
    },
]

DIVISIONS: list[dict[str, str]] = [
    {
        "id": "life-insurance",
        "name": "Life Insurance Division",
        "focus": (
            "Long-term policies: life cover, dread disease, disability, income protection (GIP), "
            "funeral, health, credit life, and hospital plans."
        ),
        "common_issues": (
            "Own/any occupation definitions, pre-existing limitations, benefit calculations, "
            "declined claims, lapsed policies, beneficiary disputes, and procedural fairness."
        ),
    },
    {
        "id": "non-life",
        "name": "Non-life Insurance Division",
        "focus": "Motor, household, travel, and other short-term insurance products.",
        "common_issues": "Claims repudiation, excess disputes, valuation, and cover interpretation.",
    },
    {
        "id": "banking-credit",
        "name": "Banking and Credit divisions",
        "focus": "Banking services, non-bank credit, and credit bureau listings.",
        "common_issues": "Account disputes, fraud, lending decisions, and bureau accuracy.",
    },
]

FAQ_HIGHLIGHTS: list[dict[str, str]] = [
    {
        "question": "When can I submit a complaint?",
        "answer": (
            "After you have raised the complaint with the insurer and they have not resolved it to your satisfaction. "
            "Complaints not previously seen by insurers are transferred to them first (six-week response period)."
        ),
    },
    {
        "question": "Does it cost anything?",
        "answer": "No — the service is free to complainants. Insurers pay case fees and an annual levy.",
    },
    {
        "question": "Is there a claim amount limit?",
        "answer": "No monetary limit on life insurance complaints handled by the Life Insurance Division.",
    },
    {
        "question": "Can I use my own language?",
        "answer": "Yes — you may correspond in any official language.",
    },
    {
        "question": "Who pays for medical reports?",
        "answer": (
            "You pay for medicals to prove your claim. If the insurer relies on an exclusion clause, "
            "the cost of additional medical reports is borne by the insurer."
        ),
    },
]

OMBUD_HISTORY: list[dict[str, str]] = [
    {
        "year": "1989",
        "title": "Short-term insurance ombud",
        "detail": (
            "The Office of the Ombudsman for Short-Term Insurance (OSTI) is established, "
            "giving consumers a free route for motor, household, and other short-term disputes."
        ),
    },
    {
        "year": "2001",
        "title": "Long-term insurance ombud",
        "detail": (
            "The Office of the Ombudsman for Long-Term Insurance (OLTI) consolidates oversight "
            "of life, disability, dread disease, funeral, and related long-term policies."
        ),
    },
    {
        "year": "2000",
        "title": "Banking Ombud",
        "detail": (
            "The Banking Ombud of South Africa provides independent resolution for banking "
            "service complaints against participating banks."
        ),
    },
    {
        "year": "2004",
        "title": "Credit Ombud",
        "detail": (
            "The Credit Ombud is created to handle non-bank credit and credit-bureau listing "
            "disputes as consumer credit markets expand."
        ),
    },
    {
        "year": "2005",
        "title": "FAIS Ombud",
        "detail": (
            "The FAIS Ombud (financial advice disputes) operates alongside sector ombuds under "
            "FSCA oversight and the Ombud Council framework."
        ),
    },
    {
        "year": "March 2024",
        "title": "National Financial Ombud Scheme (NFO)",
        "detail": (
            "Four sector ombuds — Banking, Credit, Long-Term Insurance, and Short-Term Insurance — "
            "amalgamate into a single National Financial Ombud Scheme (NFO/NFOSA). One entry point "
            "now covers most banking, credit, life, and non-life complaints."
        ),
    },
    {
        "year": "Today",
        "title": "Three NFO divisions",
        "detail": (
            "The NFO operates Banking & Credit, Life Insurance, and Non-life Insurance divisions. "
            "It remains independent, free to complainants, and accountable to the FSCA via the Ombud Council."
        ),
    },
]

NFO_STATS_INGEST_CONFIG: dict[str, Any] = {
    "method": "manual_curate_from_nfosa_press_and_annual_report",
    "primary_sources": [
        "https://nfosa.co.za/wp-json/wp/v2/posts?categories=6",
        "https://nfosa.co.za/press-releases/",
    ],
    "cache_path": "data/nfosa_press_cache.json",
    "stats_path": "data/nfosa_stats.json",
    "config_path": "data/nfosa_stats_config.json",
    "ingest_module": "news_feed.fetch_nfosa_press_releases",
    "api_route": "/api/news/nfosa?refresh=1",
    "last_curated": "2026-06-05",
    "notes": (
        "Stats manually extracted from NFO Annual Report press releases (June 2026). "
        "Refresh press cache via news_feed.fetch_nfosa_press_releases, then update nfosa_stats.json."
    ),
}


def _load_json(name: str) -> dict[str, Any]:
    path = _DATA_DIR / name
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _enrich_step(step: dict[str, Any]) -> dict[str, Any]:
    row = dict(step)
    row["summary_segments"] = link_article_text(str(step.get("summary") or ""))
    row["detail_segments"] = link_article_text(str(step.get("detail") or ""))
    row["nfosa_note_segments"] = link_article_text(str(step.get("nfosa_note") or ""))
    return row


def nfosa_dispute_hub() -> dict[str, Any]:
    intro = (
        "The National Financial Ombud Scheme (NFO) South Africa is an independent, free alternative dispute "
        "resolution body for complaints against participating banks, insurers, and credit providers. "
        "Established in March 2024 through amalgamation of the banking, credit, long-term, and short-term ombuds, "
        "it offers a single entry point for most financial disputes."
    )
    life_note = (
        "For disability and income protection claimants, the Life Insurance Division is the relevant route. "
        "ClaimBuddy's five essential principles article and the dispute resolution explainer below show how to "
        "structure evidence around policy definitions, causation, and procedural fairness before and during escalation."
    )
    stats_payload = _load_json("nfosa_stats.json")
    stats_config = _load_json("nfosa_stats_config.json") or NFO_STATS_INGEST_CONFIG
    return {
        "title": "NFO dispute process",
        "tagline": "National Financial Ombud Scheme — complaints route for life, non-life, banking, and credit",
        "intro_segments": link_article_text(intro),
        "life_note_segments": link_article_text(life_note),
        "contact": NFO_CONTACT,
        "steps": [_enrich_step(s) for s in PROCESS_STEPS],
        "divisions": DIVISIONS,
        "faq_highlights": FAQ_HIGHLIGHTS,
        "ombud_history": OMBUD_HISTORY,
        "stats": stats_payload,
        "stats_ingest_config": stats_config,
        "flowchart_images": [
            {"src": "img/nfosa-dispute-infographic.png", "alt": "NFO complaints process infographic"},
        ],
        "step_images": [
            {"src": f"img/nfosa-flowchart-{i}.png", "alt": f"NFO complaints process step {i}"}
            for i in range(1, 7)
        ],
        "resource_xrefs": [
            {"label": "Dispute resolution article", "link_kind": "news_article", "slug": "nfosa-dispute-resolution", "hover_tip": "Full explainer with disability-claim practice and practical tips."},
            {"label": "Five essential principles", "link_kind": "news_article", "slug": "five-essential-principles", "hover_tip": "Policy mapping, causation, and fair-process principles."},
            {"label": "Rejection explainer", "link_kind": "mvp_module", "slug": "rejection-explainer", "hover_tip": "Issue matrix from repudiation letters before you escalate."},
            {"label": "Claim workflow", "link_kind": "workflow", "slug": "", "hover_tip": "Nine workspace steps including ombud escalation stage."},
            {"label": "NFOSA press releases", "link_kind": "news", "slug": "nfosa-press-releases", "hover_tip": "Recoveries, case trends, and consumer warnings."},
        ],
    }