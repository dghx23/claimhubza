"""ClaimBuddy rejection explainer — review-ground matrix and cure plan."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engine import detect_gaps, review_request_letter
from knowledge import get_policy_trap
from rejection_processor import analyze_rejection_file
from term_slugs import slugify


def parse_rejection_analysis(claim: dict) -> dict | None:
    raw = (claim.get("rejection_analysis_json") or "").strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def rejection_documents(documents: list[dict]) -> list[dict]:
    return [d for d in documents if d.get("doc_type") == "rejection"]


def reanalyze_from_vault(claim_id: int, upload_dir: Path) -> dict | None:
    import db

    docs = rejection_documents(db.list_documents(claim_id))
    if not docs:
        return None
    latest = max(docs, key=lambda d: d.get("uploaded_at") or "")
    path = upload_dir / latest["stored_name"]
    if not path.is_file():
        return None
    return analyze_rejection_file(path, latest["original_name"])


def build_ground_cards(analysis: dict | None, claim: dict, gaps: list[dict]) -> list[dict[str, Any]]:
    if not analysis:
        return []

    high_gaps = [g for g in gaps if g.get("urgency") == "high"][:3]
    gap_hint = high_gaps[0]["item"] if high_gaps else "Run evidence-gap detector"

    cards: list[dict[str, Any]] = []
    for row in analysis.get("grounds") or []:
        trap_name = row.get("trap") or ""
        trap = get_policy_trap(slugify(trap_name)) if trap_name else None
        cards.append({
            "id": row.get("id"),
            "ground": row.get("ground"),
            "found": bool(row.get("found")),
            "snippet": (row.get("snippet") or "").strip(),
            "trap": trap["description"] if trap else trap_name,
            "trap_slug": (trap or {}).get("slug"),
            "cure": row.get("cure") or f"Address via evidence: {gap_hint}.",
            "confidence": row.get("confidence") or "none",
            "status": "sourced" if row.get("snippet") else ("detected" if row.get("found") else "not_found"),
        })

    for i, block in enumerate(analysis.get("decision_blocks") or [], 1):
        cards.append({
            "id": f"decision_block_{i}",
            "ground": f"Decision paragraph {i}",
            "found": True,
            "snippet": block,
            "trap": "",
            "trap_slug": None,
            "cure": "Map each sentence to a policy clause, factual response, and supporting document.",
            "confidence": "high",
            "status": "decision_block",
            "is_decision_block": True,
        })

    return cards


def build_analysis_summary(analysis: dict | None) -> dict[str, Any]:
    if not analysis or not analysis.get("processed"):
        return {
            "has_analysis": False,
            "filename": None,
            "pages": None,
            "grounds_matched": 0,
            "char_count": 0,
        }
    return {
        "has_analysis": True,
        "filename": analysis.get("filename"),
        "pages": analysis.get("pages"),
        "grounds_matched": analysis.get("grounds_matched", 0),
        "char_count": analysis.get("char_count", 0),
        "decision_blocks": analysis.get("decision_blocks") or [],
    }


def build_rejection_explainer_view(
    claim: dict,
    documents: list[dict],
    analysis: dict | None,
    *,
    gaps: list[dict] | None = None,
    timeline: list[dict] | None = None,
) -> dict[str, Any]:
    gap_list = gaps if gaps is not None else detect_gaps(claim, documents)
    cards = build_ground_cards(analysis, claim, gap_list)
    matched = [c for c in cards if c["found"] and not c.get("is_decision_block")]
    decision_cards = [c for c in cards if c.get("is_decision_block")]
    review_draft = review_request_letter(claim, gap_list, timeline or [])

    return {
        "rejection_documents": rejection_documents(documents),
        "analysis": build_analysis_summary(analysis),
        "ground_cards": cards,
        "ground_cards_matched": matched,
        "decision_cards": decision_cards,
        "has_rejection_upload": bool(rejection_documents(documents)),
        "has_analysis": bool(analysis and analysis.get("processed")),
        "review_draft": review_draft,
        "rejection_date": claim.get("rejection_date"),
        "review_deadline": claim.get("review_deadline"),
    }