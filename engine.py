"""ClaimBuddy MVP — chronology, gaps, checklist, letters, pack generation."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from functional_capacity import functional_capacity_for_claim
from knowledge import (
    POLICY_CHECKLIST,
    doctor_questionnaire,
    enrich_policy_checklist_item,
    relevant_policy_traps,
)


def _functional_capacity_section(claim: dict) -> str:
    return functional_capacity_for_claim(claim)

CLAIM_STAGES = [
    "preparing",
    "waiting_period",
    "assessment",
    "rejected",
    "internal_review",
    "ombud",
    "record_access",
    "professional",
]

STAGE_LABELS = {
    "preparing": "Preparing claim",
    "waiting_period": "Waiting-period evidence",
    "assessment": "Insurer assessment",
    "rejected": "Rejected claim",
    "internal_review": "Internal review",
    "ombud": "Ombud complaint",
    "record_access": "Record-access dispute",
    "professional": "Professional review",
}

DOC_TYPES = [
    "policy",
    "schedule",
    "medical",
    "hospital",
    "employer",
    "job_spec",
    "insurer",
    "rejection",
    "payslip",
    "claim_form",
    "correspondence",
    "pds",
    "super",
    "workers_comp",
    "other",
]

EVIDENCE_REQUIREMENTS: list[dict[str, Any]] = [
    {"id": "policy_wording", "item": "Policy wording / schedule", "holder": "Employer / policyholder", "domains": ["policy"], "always": True, "urgency": "high"},
    {"id": "employer_statement", "item": "Employer statement", "holder": "Employer HR", "domains": ["employment"], "stages": ["preparing", "assessment", "rejected", "internal_review"], "urgency": "high"},
    {"id": "payslips", "item": "Payslips (6–12 months)", "holder": "Employer payroll", "domains": ["employment"], "always": True, "urgency": "high"},
    {"id": "absence_records", "item": "Absence / leave records", "holder": "Employer HR", "domains": ["employment"], "always": True, "urgency": "high"},
    {"id": "medical_certificate", "item": "Treating practitioner records", "holder": "Claimant / doctor", "domains": ["medical"], "always": True, "urgency": "high"},
    {"id": "hospital_records", "item": "Hospital discharge / admission records", "holder": "Hospital", "domains": ["medical"], "flags": ["hospital_admission"], "urgency": "medium"},
    {"id": "specialist_report", "item": "Specialist report", "holder": "Specialist", "domains": ["medical"], "stages": ["rejected", "internal_review", "assessment"], "flags": ["specialist_required"], "urgency": "high"},
    {"id": "rejection_letter", "item": "Rejection letter", "holder": "Insurer", "domains": ["claim_handling"], "stages": ["rejected", "internal_review", "ombud"], "urgency": "high"},
    {"id": "claim_file", "item": "Insurer claim-file notes / DOA calculation", "holder": "Insurer", "domains": ["claim_handling", "record_access"], "stages": ["rejected", "internal_review", "record_access", "assessment"], "urgency": "high"},
    {"id": "functional_capacity", "item": "Functional-capacity / duty-impact statement", "holder": "Claimant / OT", "domains": ["functional"], "always": True, "urgency": "high"},
    {"id": "job_description", "item": "Job description / role profile", "holder": "Employer", "domains": ["employment"], "always": True, "urgency": "medium"},
    {"id": "claim_forms", "item": "Submitted claim forms", "holder": "Claimant / employer", "domains": ["claim_handling"], "stages": ["preparing", "assessment", "rejected", "internal_review"], "urgency": "medium"},
    {"id": "pds", "item": "PDS / insurance-in-super schedule", "holder": "Super fund / insurer", "domains": ["policy"], "always": True, "urgency": "high", "jurisdictions": ["au"]},
    {"id": "trustee_file", "item": "Super trustee claim file", "holder": "Super trustee", "domains": ["claim_handling", "record_access"], "stages": ["assessment", "rejected", "internal_review", "ombud"], "urgency": "high", "jurisdictions": ["au"]},
    {"id": "member_statement", "item": "Super member statement", "holder": "Super fund", "domains": ["policy"], "always": True, "urgency": "medium", "jurisdictions": ["au"]},
    {"id": "workers_comp", "item": "Workers compensation file (if a claim exists)", "holder": "State WorkCover / insurer", "domains": ["claim_handling"], "flags": ["workers_comp"], "urgency": "medium", "jurisdictions": ["au"]},
]

def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value.strip()[:10], fmt)
        except ValueError:
            continue
    return None


def build_chronology(claim: dict) -> list[dict]:
    from jurisdiction import profile

    j = profile(claim.get("jurisdiction"))
    date_label = j["disablement_label"]
    short = j["disablement_short"]
    events: list[tuple[datetime | None, str, str, str]] = []
    mapping = [
        ("symptom_onset", "Symptom onset", "medical", "user"),
        ("cover_start", "Cover / membership start", "policy", "user"),
        ("date_of_absence", f"{date_label} (user-stated)", "policy", "user"),
        ("first_medical_cert", "First medical certificate", "medical", "user"),
        ("first_notice", "First notice to employer/insurer", "claim_handling", "user"),
        ("form_submission", "Prescribed-form submission", "claim_handling", "user"),
        ("complete_claim", "Complete claim confirmation", "claim_handling", "user"),
        ("rejection_date", "Rejection date", "claim_handling", "insurer"),
        ("review_deadline", f"{j['idr_label']} deadline", "claim_handling", "user"),
        ("ombud_deadline", f"{j['complaint_stage_label']} deadline", "claim_handling", "user"),
    ]
    for key, label, domain, source in mapping:
        dt = _parse_date(claim.get(key))
        if dt:
            events.append((dt, label, domain, source))
    if claim.get("insurer_doa") and claim.get("insurer_doa") != claim.get("date_of_absence"):
        dt = _parse_date(claim.get("date_of_absence"))
        events.append(
            (dt, f"{short} conflict flagged — insurer states: {claim['insurer_doa']}", "policy", "insurer")
        )

    events.sort(key=lambda x: x[0] or datetime.min)
    return [
        {
            "date": e[0].strftime("%Y-%m-%d") if e[0] else "",
            "event": e[1],
            "domain": e[2],
            "source": e[3],
            "verified": False,
        }
        for e in events
    ]


def _doc_covers(requirement: dict, documents: list[dict]) -> bool:
    domains = set(requirement.get("domains", []))
    for doc in documents:
        dtype = doc.get("doc_type", "other")
        if requirement["id"] == "policy_wording" and dtype in ("policy", "schedule"):
            return True
        if requirement["id"] == "medical_certificate" and dtype == "medical":
            return True
        if requirement["id"] == "hospital_records" and dtype == "hospital":
            return True
        if requirement["id"] == "rejection_letter" and dtype == "rejection":
            return True
        if requirement["id"] == "payslips" and dtype == "payslip":
            return True
        if requirement["id"] == "employer_statement" and dtype == "employer":
            return True
        if requirement["id"] == "claim_forms" and dtype == "claim_form":
            return True
        if requirement["id"] == "job_description" and dtype == "job_spec":
            return True
        if requirement["id"] == "pds" and dtype in ("pds", "policy", "schedule"):
            return True
        if requirement["id"] == "trustee_file" and dtype in ("super", "insurer"):
            return True
        if requirement["id"] == "member_statement" and dtype == "super":
            return True
        if requirement["id"] == "workers_comp" and dtype == "workers_comp":
            return True
        if requirement["id"] == "claim_file" and dtype == "insurer" and "claim" in (doc.get("notes") or "").lower():
            return True
        if domains & {"claim_handling", "correspondence"} and dtype in ("insurer", "correspondence"):
            if requirement["id"] == "claim_file":
                continue
    return False


def detect_gaps(claim: dict, documents: list[dict]) -> list[dict]:
    from jurisdiction import applies, normalize

    stage = claim.get("claim_stage", "preparing")
    flags = set(json.loads(claim.get("flags_json") or "[]"))
    juris = normalize(claim.get("jurisdiction"))
    gaps = []
    for req in EVIDENCE_REQUIREMENTS:
        if not applies(req, juris):
            continue
        if req.get("always"):
            pass
        elif "stages" in req and stage not in req["stages"]:
            continue
        elif req.get("flags") and not flags.intersection(req["flags"]):
            continue

        if _doc_covers(req, documents):
            continue

        if req["id"] == "functional_capacity":
            from functional_capacity import load_functional_capacity

            fc = load_functional_capacity(
                claim.get("functional_capacity_json"),
                claim.get("illness_summary"),
            )
            if fc.get("rows") or claim.get("material_duties"):
                continue

        if req["id"] == "job_description" and claim.get("material_duties"):
            continue

        if req["id"] == "payslips" and (
            claim.get("gross_salary") or claim.get("net_salary") or claim.get("salary_notes")
        ):
            continue

        gaps.append({
            "id": req["id"],
            "item": req["item"],
            "holder": req["holder"],
            "urgency": req["urgency"],
            "reason": _gap_reason(req, claim, stage),
            "request": _request_wording(req, claim),
            "status": "open",
        })
    gaps.sort(key=lambda g: (0 if g["urgency"] == "high" else 1, g["item"]))
    return gaps


def _gap_reason(req: dict, claim: dict, stage: str) -> str:
    from jurisdiction import profile

    j = profile(claim.get("jurisdiction"))
    reasons = {
        "policy_wording": "Defines claim test, waiting period, exclusions, and evidence duties.",
        "employer_statement": "Employer-controlled record often decisive for group IP claims.",
        "claim_file": f"Insurer holds {j['disablement_short']} reasoning and assessment notes not in rejection letter alone.",
        "rejection_letter": "Required to build review-ground matrix.",
        "specialist_report": "Insurer may expect specialist evidence — clarify what and who pays.",
        "pds": "Super claims are decided against the PDS and the insurance schedule, not a brochure.",
        "trustee_file": "Cover inside super has two decision-makers: insurer and trustee.",
        "member_statement": "Confirms the insured benefit and whether cover is held inside this fund.",
        "workers_comp": "WorkCover / workers compensation can offset IP and change the evidence file.",
    }
    base = reasons.get(req["id"], "Required for a connected evidence record.")
    if stage == "rejected":
        base += f" Critical for {j['idr_label'].lower()} or reassessment."
    return base


def _request_wording(req: dict, claim: dict) -> str:
    from jurisdiction import profile

    j = profile(claim.get("jurisdiction"))
    employer = claim.get("employer") or "[Employer]"
    insurer = claim.get("insurer") or "[Insurer]"
    trustee = claim.get("policyholder") or "[Super fund]"
    ref = claim.get("claim_reference") or "[Claim reference]"
    templates = {
        "employer_statement": f"Request employer statement, absence records, and payroll from {employer}.",
        "payslips": f"Request payslips and earnings definition confirmation from {employer} payroll.",
        "absence_records": f"Request leave/absence register from {employer} HR for waiting-period period.",
        "claim_file": (
            f"Request complete claim file, {j['disablement_short']} calculation, "
            f"and medical-review notes from {insurer} (ref {ref})."
        ),
        "rejection_letter": f"Obtain formal rejection letter and cited policy clauses from {insurer}.",
        "specialist_report": "Ask treating doctor what specialist report is needed and whether policy funds it.",
        "pds": f"Request the PDS and insurance-in-super schedule from {trustee} / {insurer}.",
        "trustee_file": f"Request the trustee claim file and the trustee's own decision from {trustee}.",
        "member_statement": f"Request a current member statement showing insured IP/TPD benefits from {trustee}.",
        "workers_comp": f"Request the workers compensation file (if a claim exists) from the relevant state scheme / {employer}.",
    }
    return templates.get(req["id"], f"Request: {req['item']} from {req['holder']}.")


def build_checklist(claim: dict) -> list[dict]:
    items = []
    for key, label in POLICY_CHECKLIST:
        done = False
        if key == "waiting_period" and claim.get("waiting_period"):
            done = True
        elif key == "doa" and claim.get("date_of_absence"):
            done = True
        elif key == "first_notice" and claim.get("first_notice"):
            done = True
        elif key == "own_occupation" and claim.get("occupation"):
            done = True
        elif key == "material_duties" and claim.get("material_duties"):
            done = True
        elif key == "proof_of_claim" and claim.get("claim_reference"):
            done = True
        elif key == "record_access" and claim.get("claim_stage") in ("record_access", "rejected", "internal_review"):
            done = bool(claim.get("record_access_status"))
        elif key == "complaint_route" and (claim.get("review_deadline") or claim.get("ombud_deadline")):
            done = True
        items.append(enrich_policy_checklist_item(key, label, done))
    return items


def build_policy_alerts(claim: dict) -> list[dict[str, str]]:
    flags = set(json.loads(claim.get("flags_json") or "[]"))
    return relevant_policy_traps(claim.get("claim_stage") or "preparing", flags)


def build_doctor_questionnaire(claim: dict) -> list[dict]:
    return doctor_questionnaire()


def completeness_score(claim: dict, documents: list[dict], gaps: list[dict]) -> int:
    fields = [
        "claim_stage", "employer", "insurer", "policy_number", "claim_reference",
        "date_of_absence", "occupation", "material_duties", "first_notice",
        "gross_salary", "net_salary", "benefit_percent",
    ]
    filled = sum(1 for f in fields if claim.get(f))
    doc_bonus = min(len(documents) * 3, 15)
    gap_penalty = min(len(gaps) * 2, 20)
    return max(5, min(100, int((filled / len(fields)) * 70 + doc_bonus - gap_penalty)))


def employer_record_letter(claim: dict, gaps: list[dict]) -> str:
    from jurisdiction import employer_letter

    return employer_letter(claim, gaps)


def insurer_record_letter(claim: dict) -> str:
    from jurisdiction import insurer_letter

    return insurer_letter(claim)


def review_request_letter(claim: dict, gaps: list[dict], timeline: list[dict]) -> str:
    from jurisdiction import review_letter

    return review_letter(claim, gaps, timeline)


def trustee_record_letter(claim: dict) -> str | None:
    from jurisdiction import trustee_letter

    return trustee_letter(claim)


def build_claim_pack(claim: dict, timeline: list[dict], gaps: list[dict], checklist: list[dict], documents: list[dict]) -> str:
    from jurisdiction import cover_type_label, profile, stage_labels as juris_stage_labels

    j = profile(claim.get("jurisdiction"))
    labels = juris_stage_labels(j["code"])
    stage = labels.get(claim.get("claim_stage", ""), claim.get("claim_stage", ""))
    cover = cover_type_label(j["code"], claim.get("cover_type")) or "—"
    pay = j["salary_labels"]
    lines = [
        f"# RiskAtlas claim pack (DRAFT) — {j['name']}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Status:** User review required before any submission",
        f"**Studio:** Sentrix Digital",
        f"**Product:** RiskAtlas compiler",
        f"**Jurisdiction:** {j['name']} ({j['domain']})",
        f"**Currency:** {j['currency']}",
        "",
        "## 1. Claim profile",
        f"- **Stage:** {stage}",
        f"- **Cover type:** {cover}",
        f"- **Employer:** {claim.get('employer') or '—'}",
        f"- **Insurer:** {claim.get('insurer') or '—'}",
        f"- **{j['policyholder_label']}:** {claim.get('policyholder') or '—'}",
        f"- **Policy:** {claim.get('policy_number') or '—'}",
        f"- **Claim ref:** {claim.get('claim_reference') or '—'}",
        f"- **{j['disablement_label']} (yours):** {claim.get('date_of_absence') or '—'}",
        f"- **{j['disablement_label']} (insurer):** {claim.get('insurer_doa') or '—'}",
        f"- **Completeness:** {completeness_score(claim, documents, gaps)}%",
        "",
        "## 2. Salary & deductions",
        f"- **{pay['gross']}:** {claim.get('gross_salary') or '—'} ({claim.get('pay_frequency') or 'frequency not stated'})",
        f"- **{pay['net']}:** {claim.get('net_salary') or '—'}",
        f"- **Earnings basis:** {claim.get('earnings_basis') or '—'}",
        f"- **Insured benefit %:** {claim.get('benefit_percent') or '—'}",
        f"- **{pay['tax']}:** {claim.get('tax_deductions') or '—'}",
        f"- **{pay['pension']}:** {claim.get('pension_deductions') or '—'}",
        f"- **{pay['health']}:** {claim.get('medical_aid_deductions') or '—'}",
        f"- **{pay['statutory']}:** {claim.get('uif_deductions') or '—'}",
        f"- **Other deductions:** {claim.get('other_deductions') or '—'}",
        f"- **Notes:** {claim.get('salary_notes') or '—'}",
        "",
        "## 3. Chronology",
    ]
    for ev in timeline:
        lines.append(f"- **{ev['date']}** — {ev['event']} _(source: {ev['source']})_")
    lines += ["", "## 4. Policy checklist", ""]
    for item in checklist:
        mark = "x" if item["done"] else " "
        lines.append(f"- [{mark}] {item['label']}")
    lines += ["", "## 5. Evidence gaps", ""]
    for g in gaps:
        lines.append(f"- **{g['urgency'].upper()}** — {g['item']} | Holder: {g['holder']} | {g['request']}")
    lines += ["", "## 6. Document vault index", ""]
    for d in documents:
        lines.append(f"- {d.get('original_name')} ({d.get('doc_type')}) — uploaded {d.get('uploaded_at', '')[:10]}")
    lines += [
        "",
        "## 7. Functional capacity (user-provided)",
        _functional_capacity_section(claim),
        "",
        "---",
        f"_{j['disclaimer']}_",
    ]
    return "\n".join(lines)