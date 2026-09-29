"""Claim file compiler — ingest, classify, File-view helpers.

Keeps engine.py / policy processors as the brain. This module is the thin
adapter between unsorted uploads and The File.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from functional_capacity import load_functional_capacity
from jurisdiction import profile, stage_labels
from policy_reader import parse_policy_analysis

_TYPE_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("rejection", ("reject", "declin", "decline", "unsuccessful")),
    ("pds", ("pds", "product disclosure")),
    ("workers_comp", ("workcover", "workers comp", "workers compensation", "icare")),
    ("super", ("member statement", "member-statement", "super fund", "superfund", "superannuation")),
    ("policy", ("policy", "wording", "member cert", "certificate of membership")),
    ("schedule", ("schedule", "benefit schedule")),
    ("payslip", ("payslip", "pay slip", "salary slip", "payroll")),
    ("hospital", ("hospital", "discharge", "admission")),
    ("medical", ("sick note", "sicknote", "medical cert", "script", "prescription", "specialist", "gp letter")),
    ("job_spec", ("job spec", "job description", "role profile", "organogram")),
    ("employer", ("employer", "hr letter", "absence record", "leave record")),
    ("claim_form", ("claim form", "claimform", "application form")),
    ("insurer", ("insurer", "claim file", "assessment", "ime")),
    ("correspondence", ("email", "correspond", "letter")),
]


def guess_doc_type(filename: str) -> str:
    name = (filename or "").lower().replace("_", " ").replace("-", " ")
    for doc_type, keys in _TYPE_KEYWORDS:
        if any(k in name for k in keys):
            return doc_type
    ext = Path(filename or "").suffix.lower()
    if ext in {".eml", ".msg"}:
        return "correspondence"
    return "other"


def doa_conflict(claim: dict) -> dict[str, str] | None:
    user = (claim.get("date_of_absence") or "").strip()
    insurer = (claim.get("insurer_doa") or "").strip()
    if user and insurer and user != insurer:
        j = profile(claim.get("jurisdiction"))
        label = j["disablement_label"]
        return {
            "user": user,
            "insurer": insurer,
            "label": f"{label} conflict — you: {user}; insurer: {insurer}",
            "date_label": label,
        }
    return None


def clock_items(claim: dict) -> list[dict[str, str]]:
    j = profile(claim.get("jurisdiction"))
    fields = [
        ("cover_start", "Cover start", "policy"),
        ("date_of_absence", f"{j['disablement_label']} (yours)", "policy"),
        ("insurer_doa", f"{j['disablement_label']} (insurer)", "policy"),
        ("waiting_period", "Waiting period", "policy"),
        ("first_notice", "First notice", "claim"),
        ("form_submission", "Form submitted", "claim"),
        ("rejection_date", "Rejection date", "claim"),
        ("review_deadline", f"{j['idr_label']} deadline", "clock"),
        ("ombud_deadline", f"{j['complaint_stage_label']} deadline", "clock"),
    ]
    items = []
    for key, label, kind in fields:
        value = (claim.get(key) or "").strip()
        if value:
            items.append({"key": key, "label": label, "value": value, "kind": kind})
    return items


def policy_tests(claim: dict) -> list[dict[str, Any]]:
    analysis = parse_policy_analysis(claim)
    if not analysis:
        return []
    found = []
    for term in analysis.get("terms") or []:
        if term.get("found"):
            found.append(term)
    return found


def argument_view(claim: dict) -> dict[str, Any]:
    fc = load_functional_capacity(
        claim.get("functional_capacity_json"),
        claim.get("illness_summary"),
    )
    rows = fc.get("rows") or []
    return {
        "illness": (claim.get("illness_summary") or "").strip(),
        "occupation": (claim.get("occupation") or "").strip(),
        "duties": (claim.get("material_duties") or "").strip(),
        "rows": rows,
        "statement": (fc.get("statement") or "").strip(),
        "has_argument": bool(rows or claim.get("illness_summary") or claim.get("material_duties")),
    }


def parties_from_policy(claim: dict) -> dict[str, str]:
    analysis = parse_policy_analysis(claim)
    if not analysis:
        return {}
    parties = analysis.get("parties") or {}
    out: dict[str, str] = {}
    if isinstance(parties, dict):
        for key in ("employer", "insurer", "policyholder"):
            val = parties.get(key)
            if isinstance(val, str) and val.strip() and not (claim.get(key) or "").strip():
                out[key] = val.strip()
    ref = analysis.get("policy_reference")
    if isinstance(ref, str) and ref.strip() and not (claim.get("policy_number") or "").strip():
        out["policy_number"] = ref.strip()
    return out


def file_title(claim: dict) -> str:
    name = (claim.get("claimant_name") or "").strip()
    if name:
        return name
    ref = (claim.get("claim_reference") or claim.get("policy_number") or "").strip()
    if ref:
        return f"Claim {ref}"
    return f"Claim file #{claim.get('id')}"


def stage_label(claim: dict) -> str:
    stage = claim.get("claim_stage") or "preparing"
    return stage_labels(claim.get("jurisdiction")).get(stage, stage)


def flags_list(claim: dict) -> list[str]:
    raw = claim.get("flags_json") or "[]"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return [str(x) for x in data] if isinstance(data, list) else []
