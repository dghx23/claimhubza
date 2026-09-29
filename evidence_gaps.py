"""Six evidence gaps — resources hub with linked explainers and module xrefs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent.parent / "claimguard-site" / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from content_data_extra import MVP_MODULE_DETAILS, PROBLEM_GAPS  # noqa: E402
from term_slugs import slugify

_MODULE_PHRASES: tuple[tuple[str, str], ...] = (
    ("Stage triage", "guided-intake"),
    ("Guided intake", "guided-intake"),
    ("policy checklist", "policy-reader"),
    ("Policy checklist", "policy-reader"),
    ("term cards", "policy-reader"),
    ("plain-language policy reader", "policy-reader"),
    ("Policy reader", "policy-reader"),
    ("Functional-capacity builder", "functional-capacity-builder"),
    ("functional-capacity builder", "functional-capacity-builder"),
    ("doctor questionnaire", "functional-capacity-builder"),
    ("Evidence-gap detector", "evidence-gap-detector"),
    ("evidence-gap detector", "evidence-gap-detector"),
    ("Access-request assistant", "access-request-assistant"),
    ("access-request assistant", "access-request-assistant"),
    ("Rejection explainer", "rejection-explainer"),
    ("rejection explainer", "rejection-explainer"),
    ("Claim-pack generator", "claim-pack-generator"),
    ("claim-pack generator", "claim-pack-generator"),
    ("Document vault", "document-vault"),
    ("chronology", "guided-intake"),
    ("issue matrix", "rejection-explainer"),
    ("notice ladder", "guided-intake"),
    ("contradiction detection", "rejection-explainer"),
    ("structured issue matrix", "rejection-explainer"),
    ("date-trap alerts", "date-trap"),
    ("Date trap", "date-trap"),
    ("threshold-shift trap", "threshold-shift-trap"),
    ("Employer-record trap", "employer-record-trap"),
    ("Diagnosis trap", "diagnosis-trap"),
    ("Appeal-story trap", "appeal-story-trap"),
)

EVIDENCE_GAP_DETAILS: dict[str, dict[str, Any]] = {
    "claim-process-knowledge-gap": {
        "overview": (
            "Income-protection claims run on a ladder of different thresholds — notice, forms, complete submission, "
            "Date of Absence, waiting period, Initial Period, Extended Period, and complaint deadlines are not interchangeable. "
            "Claimants are rarely told which rung they are on until something goes wrong."
        ),
        "what_goes_wrong": (
            "Employers, HR, and insurers each use everyday words that sound like the same deadline. A sick note may feel "
            "like 'notice', a claim form like 'submission', and a hospital admission like proof of disability — but policy "
            "wording separates actual notice, prescribed-form submission, complete claim, DOA, and waiting-period continuity. "
            "Missing one threshold can delay payment or anchor a rejection."
        ),
        "claim_tip": (
            "Build a personal date ladder early: first symptom, first medical certificate, first notice to employer/insurer, "
            "form submission, complete claim, insurer DOA, waiting-period start/end, rejection, and complaint deadlines. "
            "ClaimBuddy stage triage maps your position on that ladder before you upload."
        ),
        "related_modules": ["Guided intake", "Policy reader"],
        "related_traps": ["Date trap", "Policy-vs-guide trap"],
        "related_terms": ["Date of Absence", "Waiting period", "First notice", "Complete claim"],
    },
    "functional-evidence-gap": {
        "overview": (
            "Medical records describe what is wrong with the body; disability policies ask whether you can perform material duties. "
            "That translation gap is where many technically 'good' files still fail."
        ),
        "what_goes_wrong": (
            "Treating notes may list diagnoses, scripts, and hospital events without connecting symptoms to attendance, cognitive "
            "endurance, decision quality, stamina, reliability, treatment side-effects, travel, supervision load, or safety risk. "
            "Insurers then apply the diagnosis trap — accepting the label while disputing incapacity for your own occupation."
        ),
        "claim_tip": (
            "Pair every diagnosis with a duty-impact line: which material duties are blocked, how often, and with what work consequences. "
            "Use the functional-capacity builder and doctor questionnaire so your practitioner answers the policy test, not just the ICD-10 label."
        ),
        "related_modules": ["Functional-capacity builder", "Policy reader"],
        "related_traps": ["Diagnosis trap", "Job-title trap"],
        "related_terms": ["Functional capacity", "Material duties", "Disability", "Own occupation"],
    },
    "record-control-gap": {
        "overview": (
            "The records that decide your claim are often held by someone else — employer payroll, HR absence data, insurer claim-file "
            "notes, DOA worksheets, and medical-review memoranda may never reach you unless you request them."
        ),
        "what_goes_wrong": (
            "Claimants submit what they personally hold while decisive files sit with the participating employer, policyholder, insurer, "
            "or fund administrator. Rejections then cite missing employer statements, incomplete salary proof, undisclosed DOA reasoning, "
            "or absent specialist reports the claimant was never told how to obtain."
        ),
        "claim_tip": (
            "For every missing item, name the holder and the legal/policy basis for access. Run the evidence-gap detector, then generate "
            "targeted employer and insurer record requests — do not wait for a rejection to discover what they relied on."
        ),
        "related_modules": ["Evidence-gap detector", "Access-request assistant", "Document vault"],
        "related_traps": ["Employer-record trap", "Specialist-evidence trap"],
        "related_terms": ["Proof of claim", "Further medical evidence", "Record access"],
    },
    "timing-gap": {
        "overview": (
            "A claim can feel 'started' when an employer accepts a sick note or HR forwards a form — then fail later when the insurer "
            "applies a stricter disability test, different Date of Absence, or a deadline you were never shown."
        ),
        "what_goes_wrong": (
            "Threshold-shift trap dynamics appear when initiation evidence satisfies the employer but the insurer demands more. "
            "Date trap risk spikes when DOA, first notice, waiting-period continuity, and rejection dates are calculated differently "
            "across payroll, medical certificates, and insurer emails — often disclosed only after rejection."
        ),
        "claim_tip": (
            "Capture every threshold statement in writing: who said what was 'enough', on what date, and under which policy clause. "
            "Use contradiction detection and date-trap alerts to flag employer vs insurer standard drift before you rely on verbal assurances."
        ),
        "related_modules": ["Guided intake", "Policy reader", "Rejection explainer"],
        "related_traps": ["Date trap", "Threshold-shift trap"],
        "related_terms": ["Date of Absence", "Waiting period", "First notice"],
    },
    "language-gap": {
        "overview": (
            "Rejection letters blend policy wording, medical-review jargon, and administrative shorthand. Without translation, "
            "claimants cannot tell which ground is decisive, what evidence would cure it, or which deadline applies."
        ),
        "what_goes_wrong": (
            "A lay reader sees emotional conclusions — 'not disabled', 'pre-existing', 'late submission' — without a structured map "
            "to policy clauses, missing records, or unfair process. The appeal-story trap follows when narrative replaces an issue matrix "
            "with evidence, holder, clause, and remedy columns."
        ),
        "claim_tip": (
            "Turn each sentence in the rejection into an issue card: ground stated, evidence relied on, policy clause cited, record missing, "
            "and cure action. Pair rejection explainer output with term cards and plain-language policy reader so every insurer phrase links "
            "to a defined test."
        ),
        "related_modules": ["Rejection explainer", "Policy reader"],
        "related_traps": ["Appeal-story trap", "Policy-vs-guide trap"],
        "related_terms": ["Decision ground", "Disability", "Pre-existing condition"],
    },
    "power-gap": {
        "overview": (
            "Insurers and employers run claims repeatedly; most claimants face the process once while unwell. Administrative asymmetry "
            "shows up in template rejections, slow record access, and issue framing that assumes you already know the rules."
        ),
        "what_goes_wrong": (
            "Without chronology, source-linked assertions, and a structured issue matrix, the claimant's file looks anecdotal beside "
            "the insurer's process narrative. Gaps in packaging — missing attachment index, unclear remedy sought, or undated exhibits — "
            "make fair reassessment harder even when the underlying facts are strong."
        ),
        "claim_tip": (
            "Level the field with the same artefacts professionals use: verified chronology, evidence index, issue matrix, and an editable "
            "claim pack where every assertion points to a source. Claim-pack generator assembles workspace outputs so you submit administration, "
            "not just story."
        ),
        "related_modules": ["Claim-pack generator", "Document vault", "Guided intake"],
        "related_traps": ["Appeal-story trap", "Employer-record trap"],
        "related_terms": ["Proof of claim", "Complaint/appeal", "Record access"],
    },
}


def _gap_slug(name: str) -> str:
    return slugify(name)


def _module_hover(slug: str) -> str:
    detail = MVP_MODULE_DETAILS.get(slug) or {}
    return str(detail.get("purpose") or detail.get("title") or slug.replace("-", " ").title())


def _evidence_gap_phrase_table() -> list[tuple[str, str, str]]:
    from language_map import _detail_phrase_table

    seen: set[str] = set()
    rows: list[tuple[str, str, str]] = []
    for phrase, slug, kind in _detail_phrase_table():
        key = phrase.lower()
        if key not in seen:
            rows.append((phrase, slug, kind))
            seen.add(key)
    for phrase, slug in _MODULE_PHRASES:
        key = phrase.lower()
        if key not in seen:
            if slug.endswith("-trap"):
                rows.append((phrase, slug, "trap"))
            else:
                rows.append((phrase, slug, "mvp_module"))
            seen.add(key)
    return sorted(rows, key=lambda x: len(x[0]), reverse=True)


def link_evidence_gap_text(text: str) -> list[dict[str, str]]:
    """Split gap copy into segments with hover tips and resource xrefs."""
    from language_map import _trap_hover, get_confusion_pair, get_language_term

    if not text:
        return [{"type": "text", "value": ""}]

    table = _evidence_gap_phrase_table()
    pattern = re.compile("|".join(re.escape(phrase) for phrase, _, _ in table), re.IGNORECASE)
    meta = {phrase.lower(): (slug, kind) for phrase, slug, kind in table}

    segments: list[dict[str, str]] = []
    last = 0
    for match in pattern.finditer(text):
        if match.start() > last:
            segments.append({"type": "text", "value": text[last : match.start()]})
        matched = match.group(0)
        slug, kind = meta[matched.lower()]
        hover = matched
        if kind == "language":
            term = get_language_term(slug) or {}
            hover = str(term.get("one_liner") or term.get("policy_note") or matched)
        elif kind == "trap":
            from knowledge import trap_name_from_slug

            hover = _trap_hover(trap_name_from_slug(slug), matched)
        elif kind == "confusion":
            pair = get_confusion_pair(slug)
            hover = str((pair or {}).get("tip") or (pair or {}).get("distinction") or matched)
        elif kind == "mvp_module":
            hover = _module_hover(slug)
        segments.append({
            "type": "link",
            "label": matched,
            "slug": slug,
            "link_kind": kind,
            "hover_tip": hover,
        })
        last = match.end()
    if last < len(text):
        segments.append({"type": "text", "value": text[last:]})
    return segments or [{"type": "text", "value": text}]


def _module_xref(name: str) -> dict[str, str]:
    from knowledge import _MODULE_SLUGS, _MODULE_WORKSPACE

    slug = _MODULE_SLUGS.get(name, slugify(name))
    detail = MVP_MODULE_DETAILS.get(slug) or {}
    workspace = _MODULE_WORKSPACE.get(name, {})
    return {
        "label": name,
        "link_kind": "mvp_module",
        "slug": slug,
        "hover_tip": str(detail.get("purpose") or name),
        "endpoint": str(workspace.get("endpoint") or ""),
        "claim_scoped": bool(workspace.get("claim_scoped")),
        "fallback_endpoint": str(workspace.get("fallback_endpoint") or ""),
    }


def _term_xref(term_name: str) -> dict[str, str] | None:
    from language_map import get_language_term, language_term_slug

    slug = language_term_slug(term_name)
    if not slug:
        return None
    term = get_language_term(slug) or {}
    return {
        "label": term_name,
        "link_kind": "language",
        "slug": slug,
        "hover_tip": str(term.get("one_liner") or term.get("policy_note") or term_name),
    }


def _trap_xref(trap_name: str) -> dict[str, str]:
    from language_map import _trap_hover

    return {
        "label": trap_name,
        "link_kind": "trap",
        "slug": slugify(trap_name),
        "hover_tip": _trap_hover(trap_name),
    }


def _gap_resource_xrefs(extra: dict[str, Any]) -> list[dict[str, str]]:
    xrefs: list[dict[str, str]] = []
    for name in extra.get("related_modules") or []:
        xrefs.append(_module_xref(str(name)))
    for term in extra.get("related_terms") or []:
        row = _term_xref(str(term))
        if row:
            xrefs.append(row)
    for trap in extra.get("related_traps") or []:
        xrefs.append(_trap_xref(str(trap)))
    xrefs.append({
        "label": "Evidence domains",
        "link_kind": "evidence_domains",
        "slug": "",
        "hover_tip": "Six evidence domains — policy, employment, medical, functional, claim handling, record access.",
    })
    xrefs.append({
        "label": "All evidence gaps",
        "link_kind": "evidence_gaps",
        "slug": "",
        "hover_tip": "Six structural gaps ClaimBuddy is designed to close.",
    })
    return xrefs


def enrich_evidence_gap(name: str, problem: str, solution: str) -> dict[str, Any]:
    slug = _gap_slug(name)
    extra = EVIDENCE_GAP_DETAILS.get(slug, {})
    return {
        "name": name,
        "slug": slug,
        "summary": problem,
        "why_it_matters": problem,
        "claimbuddy_response": solution,
        "overview": str(extra.get("overview") or problem),
        "what_goes_wrong": str(extra.get("what_goes_wrong") or problem),
        "claim_tip": str(extra.get("claim_tip") or ""),
        "why_segments": link_evidence_gap_text(problem),
        "overview_segments": link_evidence_gap_text(str(extra.get("overview") or problem)),
        "what_goes_wrong_segments": link_evidence_gap_text(str(extra.get("what_goes_wrong") or problem)),
        "claim_tip_segments": link_evidence_gap_text(str(extra.get("claim_tip") or "")),
        "response_segments": link_evidence_gap_text(solution),
        "response_xrefs": [_module_xref(m) for m in (extra.get("related_modules") or [])],
        "resource_xrefs": _gap_resource_xrefs(extra),
        "related_gaps": [],
    }


_GAP_BY_SLUG: dict[str, dict[str, Any]] | None = None


def _ensure_gap_index() -> dict[str, dict[str, Any]]:
    global _GAP_BY_SLUG
    if _GAP_BY_SLUG is not None:
        return _GAP_BY_SLUG
    rows = [enrich_evidence_gap(name, problem, solution) for name, problem, solution in PROBLEM_GAPS]
    for row in rows:
        row["related_gaps"] = [
            {"name": other["name"], "slug": other["slug"]}
            for other in rows
            if other["slug"] != row["slug"]
        ][:3]
    _GAP_BY_SLUG = {row["slug"]: row for row in rows}
    return _GAP_BY_SLUG


def evidence_gaps_list() -> list[dict[str, Any]]:
    return list(_ensure_gap_index().values())


def get_evidence_gap(slug: str) -> dict[str, Any] | None:
    return _ensure_gap_index().get(slug)