"""ClaimBuddy functional-capacity module — shared view model for standalone workspace."""

from __future__ import annotations

import json
from typing import Any

from functional_capacity import load_functional_capacity


def _parse_occupation_profile(raw: str | None) -> dict | None:
    if not raw or not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def build_functional_capacity_view(claim: dict) -> dict[str, Any]:
    """View model for the standalone functional-capacity workspace."""
    fc = load_functional_capacity(
        claim.get("functional_capacity_json"),
        claim.get("illness_summary"),
    )
    rows = fc.get("rows") or []
    profile = _parse_occupation_profile(claim.get("occupation_profile_json"))
    occupation = (claim.get("occupation") or "").strip()
    duties = (claim.get("material_duties") or "").strip()

    return {
        "rows": rows,
        "row_count": len(rows),
        "statement": (fc.get("statement") or "").strip(),
        "has_occupation": bool(profile or occupation or duties),
        "has_profile": bool(profile),
        "occupation": occupation or None,
        "material_duties": duties or None,
        "occupation_title": (profile or {}).get("title") or occupation or None,
        "illness_summary": (claim.get("illness_summary") or "").strip(),
        "functional_capacity_json": (claim.get("functional_capacity_json") or "").strip(),
    }