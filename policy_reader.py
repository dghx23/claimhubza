"""ClaimBuddy policy reader — term cards, checklist, and analysis view for a claim."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engine import POLICY_CHECKLIST, build_checklist
from knowledge import get_core_policy_term, get_policy_trap
from language_map import language_term_slug
from policy_processor import POLICY_SCAN_TERMS, analyze_policy_file
from term_slugs import slugify

_SCAN_CORE_MAP: dict[str, str] = {
    "waiting_period": "Waiting period",
    "doa": "Date of Absence",
    "benefit": "Income protection benefit",
    "own_occupation": "Own occupation",
    "notice": "First notice",
    "preexisting": "Pre-existing condition exclusion",
    "specialist_evidence": "Further medical evidence",
    "hospital_admission": "Further medical evidence",
    "offset": "Offset",
    "complaint": "Complaint / appeal / internal review",
    "exclusion": "Exclusion",
    "cover": "Actively at Work",
}

_TRAP_NAME_MAP: dict[str, str] = {
    "waiting_period": "Date trap",
    "doa": "Date trap",
    "notice": "Date trap",
    "own_occupation": "Job-title trap",
    "preexisting": "Pre-existing trap",
    "specialist_evidence": "Specialist-evidence trap",
    "benefit": "Gross-benefit trap",
    "offset": "Gross-benefit trap",
    "complaint": "Appeal-story trap",
    "exclusion": "Pre-existing trap",
}


def parse_policy_analysis(claim: dict) -> dict | None:
    raw = (claim.get("policy_analysis_json") or "").strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def policy_documents(documents: list[dict]) -> list[dict]:
    return [d for d in documents if d.get("doc_type") == "policy"]


def reanalyze_from_vault(claim_id: int, upload_dir: Path) -> dict | None:
    """Re-run analysis on the most recently uploaded policy document."""
    import db

    docs = policy_documents(db.list_documents(claim_id))
    if not docs:
        return None
    latest = max(docs, key=lambda d: d.get("uploaded_at") or "")
    path = upload_dir / latest["stored_name"]
    if not path.is_file():
        return None
    return analyze_policy_file(path, latest["original_name"])


def _next_action(term_id: str, fields: list[str]) -> str:
    actions = {
        "waiting_period": "Upload absence records and sick notes covering the full waiting period.",
        "doa": "Record your DOA, employer date, and insurer-stated DOA separately in Key dates.",
        "benefit": "Confirm benefit %, earnings definition, and offsets against payslips.",
        "own_occupation": "Complete material duties — not job title alone — in Occupation.",
        "notice": "Capture first notice, form submission, and complete-claim dates separately.",
        "preexisting": "Separate baseline condition from post-cover deterioration in your health story.",
        "specialist_evidence": "Tick specialist evidence and gather consultant reports or IME findings.",
        "offset": "List other income and deductions that may reduce net benefit.",
        "complaint": "Track internal review and ombud deadlines in Key dates.",
    }
    if term_id in actions:
        return actions[term_id]
    if fields:
        return f"Complete linked intake fields: {', '.join(f.replace('_', ' ') for f in fields[:3])}."
    return "Confirm this clause against your schedule and member certificate."


def build_term_cards(analysis: dict | None) -> list[dict[str, Any]]:
    """Merge scan results with core policy-term knowledge into term cards."""
    if not analysis:
        return []

    by_id = {t["id"]: t for t in analysis.get("terms") or []}
    cards: list[dict[str, Any]] = []

    for entry in POLICY_SCAN_TERMS:
        hit = by_id.get(entry["id"], {})
        found = bool(hit.get("found"))
        core_name = _SCAN_CORE_MAP.get(entry["id"])
        core = get_core_policy_term(slugify(core_name)) if core_name else None
        lang_slug = language_term_slug(core_name or entry["term"]) if core_name else None

        trap_name = _TRAP_NAME_MAP.get(entry["id"])
        trap = get_policy_trap(slugify(trap_name)) if trap_name else None

        cards.append({
            "id": entry["id"],
            "term": entry["term"],
            "found": found,
            "section": entry.get("section", ""),
            "fields": entry.get("fields", []),
            "snippet": (hit.get("snippet") or "").strip(),
            "plain": (core or {}).get("meaning", ""),
            "trap": trap["description"] if trap else (core or {}).get("trap", ""),
            "evidence": (core or {}).get("evidence", ""),
            "action": _next_action(entry["id"], entry.get("fields", [])),
            "core_term_slug": (core or {}).get("slug"),
            "language_slug": lang_slug,
            "trap_slug": (trap or {}).get("slug"),
            "status": "sourced" if found and hit.get("snippet") else ("missing" if not found else "mentioned"),
        })

    return cards


def build_analysis_summary(analysis: dict | None) -> dict[str, Any]:
    if not analysis or not analysis.get("processed"):
        return {
            "has_analysis": False,
            "filename": None,
            "pages": None,
            "terms_matched": 0,
            "char_count": 0,
        }
    return {
        "has_analysis": True,
        "filename": analysis.get("filename"),
        "pages": analysis.get("pages"),
        "terms_matched": analysis.get("terms_matched", 0),
        "char_count": analysis.get("char_count", 0),
        "parties": analysis.get("parties") or {},
        "suggested": analysis.get("suggested") or {},
        "policy_reference": analysis.get("policy_reference") or {},
        "traps": analysis.get("traps") or [],
        "cross_links": analysis.get("cross_links") or [],
        "field_hints": analysis.get("field_hints") or {},
    }


def build_policy_reader_view(
    claim: dict,
    documents: list[dict],
    analysis: dict | None,
) -> dict[str, Any]:
    """Full context for the policy reader workspace page."""
    pol_docs = policy_documents(documents)
    cards = build_term_cards(analysis)
    matched = [c for c in cards if c["found"]]
    missing = [c for c in cards if not c["found"]]

    return {
        "policy_documents": pol_docs,
        "analysis": build_analysis_summary(analysis),
        "term_cards": cards,
        "term_cards_matched": matched,
        "term_cards_missing": missing,
        "checklist": build_checklist(claim),
        "checklist_labels": dict(POLICY_CHECKLIST),
        "has_policy_upload": bool(pol_docs),
        "has_analysis": bool(analysis and analysis.get("processed")),
    }