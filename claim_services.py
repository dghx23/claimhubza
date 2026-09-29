"""Shared claim read model used by ClaimBuddy and ClaimHub.

Domain processors stay in their existing modules. This module provides the
service boundary so claimant and professional surfaces read the same claim,
chronology, evidence gaps and policy/doctor guidance without duplicating the
domain rules.
"""
from __future__ import annotations

import json

import db
from compiler import stage_label as compiler_stage_label
from engine import (
    build_checklist,
    build_chronology,
    build_doctor_questionnaire,
    build_policy_alerts,
    completeness_score,
    detect_gaps,
)
from jurisdiction import profile as jurisdiction_profile, stage_labels as jurisdiction_stage_labels


def build_claim_context(claim_id: int) -> dict | None:
    claim = db.get_claim(claim_id)
    if not claim:
        return None
    documents = db.list_documents(claim_id)
    timeline = build_chronology(claim)
    gaps = detect_gaps(claim, documents)
    checklist = build_checklist(claim)
    score = completeness_score(claim, documents, gaps)
    flags = json.loads(claim.get("flags_json") or "[]")
    j = jurisdiction_profile(claim.get("jurisdiction"))
    return {
        "claim": claim,
        "documents": documents,
        "timeline": timeline,
        "gaps": gaps,
        "checklist": checklist,
        "score": score,
        "stage_label": compiler_stage_label(claim),
        "policy_alerts": build_policy_alerts(claim),
        "doctor_questions": build_doctor_questionnaire(claim),
        "claim_juris": j,
        "stages": jurisdiction_stage_labels(j["code"]),
        "workers_comp": "workers_comp" in flags,
    }
