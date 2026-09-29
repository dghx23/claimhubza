"""Merge medical record items into claims and append illness story lines."""

from __future__ import annotations

import json
import re
from typing import Any


def _parse_list(raw: str | None) -> list[dict]:
    try:
        data = json.loads(raw or "[]")
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def format_clinician_display(item: dict) -> str:
    name = (item.get("clinician_name") or "").strip()
    spec = (item.get("clinician_specialty") or "").strip()
    reg = (item.get("clinician_reg") or "").strip()
    out = name
    if spec:
        out = f"{out} ({spec})" if out else spec
    if reg and name:
        out += f" [{reg}]"
    return out or (item.get("clinician") or "").strip()


def format_medication_dose(med: dict) -> str:
    parts: list[str] = []
    strength = (
        (med.get("strength_custom") or "").strip()
        if med.get("strength_manual")
        else (med.get("strength") or "").strip()
    )
    if strength:
        parts.append(strength)
    if med.get("frequency") == "other":
        other = (med.get("frequency_other") or "").strip()
        if other:
            parts.append(other)
    elif med.get("frequency_label"):
        parts.append(str(med["frequency_label"]).lower())
    elif med.get("frequency"):
        parts.append(str(med["frequency"]))
    comment = (med.get("dose_comment") or "").strip()
    if comment:
        parts.append(f"({comment})")
    return " ".join(parts) or (med.get("dose") or "").strip()


def format_diagnosis_story_line(item: dict) -> str:
    name = (item.get("name") or "").strip()
    if not name:
        return ""
    icd = (item.get("icd10") or item.get("code") or "").strip()
    line = "Diagnosis"
    if icd:
        line += f" ({icd})"
    line += f": {name}"
    clinician = format_clinician_display(item) or (item.get("clinician") or "").strip()
    if clinician:
        line += f" — {clinician}"
    date = (item.get("date") or item.get("first_diagnosed") or "").strip()
    if date:
        line += f" ({date})"
    notes = (item.get("additional_notes") or item.get("notes") or "").strip()
    if notes:
        line += f" — {notes}"
    return line + "."


def format_medication_story_line(item: dict) -> str:
    name = (item.get("name") or "").strip()
    if not name:
        return ""
    line = f"Medication: {name}"
    dose = format_medication_dose(item)
    if dose:
        line += f" — {dose}"
    first = (item.get("first_prescribed") or "").strip()
    if first:
        line += f"; first prescribed {first}"
    prescriber = (item.get("prescriber") or "").strip()
    if prescriber:
        line += f"; prescriber: {prescriber}"
    notes = (item.get("additional_notes") or "").strip()
    if notes:
        line += f"; {notes}"
    return line + "."


def append_illness_story(existing: str | None, paragraph: str) -> str:
    text = (existing or "").strip()
    block = (paragraph or "").strip()
    if not block:
        return text
    return f"{text}\n\n{block}" if text else block


def _symptom_already_in_story(story: str, symptom: str) -> bool:
    if not symptom:
        return True
    return bool(re.search(rf"\b{re.escape(symptom)}\b", story, re.IGNORECASE))


def merge_symptom_into_story(existing: str | None, symptom: str) -> str:
    """Append a symptom to the illness story, merging into an existing Symptoms line when present."""
    name = (symptom or "").strip()
    if not name:
        return (existing or "").strip()
    text = (existing or "").strip()
    if _symptom_already_in_story(text, name):
        return text

    lines = text.split("\n") if text else []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.lower().startswith("symptoms:"):
            continue
        body = stripped[len("symptoms:") :].strip().rstrip(".")
        parts = [p.strip() for p in body.split(",") if p.strip()]
        if any(p.lower() == name.lower() for p in parts):
            return text
        parts.append(name)
        lines[i] = "Symptoms: " + ", ".join(parts) + "."
        return "\n".join(lines)

    block = f"Symptoms: {name}."
    return append_illness_story(text, block)


def format_symptom_story_line(item: dict) -> str:
    name = (item.get("name") or item.get("label") or "").strip()
    if not name:
        return ""
    return f"Symptoms: {name}."


def merge_diagnosis(existing: list[dict], item: dict) -> list[dict]:
    name = (item.get("name") or "").strip().lower()
    rows = [dict(r) for r in existing]
    for i, row in enumerate(rows):
        if (row.get("name") or "").strip().lower() == name and name:
            merged = {**row, **item}
            merged["clinician"] = format_clinician_display(merged)
            rows[i] = merged
            return rows
    new_item = dict(item)
    new_item["clinician"] = format_clinician_display(new_item)
    if not any(r.get("primary") for r in rows):
        new_item["primary"] = True
    rows.append(new_item)
    return rows


def merge_practitioner(existing: list[dict], item: dict) -> list[dict]:
    rows = [dict(r) for r in existing]
    reg = (item.get("registration_number") or "").strip().lower()
    name = (item.get("name") or "").strip().lower()
    for i, row in enumerate(rows):
        row_reg = (row.get("registration_number") or "").strip().lower()
        row_name = (row.get("name") or "").strip().lower()
        if reg and row_reg == reg:
            rows[i] = {**row, **item}
            return rows
        if name and row_name == name and not reg and not row_reg:
            rows[i] = {**row, **item}
            return rows
    rows.append(dict(item))
    return rows


def merge_medical_aid(existing: list[dict], item: dict) -> list[dict]:
    rows = [dict(r) for r in existing]
    slug = (item.get("slug") or "").strip().lower()
    name = (item.get("display_name") or item.get("name") or "").strip().lower()
    for i, row in enumerate(rows):
        row_slug = (row.get("slug") or "").strip().lower()
        if slug and row_slug == slug:
            rows[i] = {**row, **item}
            return rows
        row_name = (row.get("display_name") or row.get("name") or "").strip().lower()
        if name and row_name == name and not slug:
            rows[i] = {**row, **item}
            return rows
    rows.append(dict(item))
    return rows


def format_practitioner_story_line(item: dict) -> str:
    name = (item.get("name") or "").strip()
    if not name:
        return ""
    line = f"Practitioner: {name}"
    reg = (item.get("registration_number") or "").strip()
    if reg:
        line += f" [{reg}]"
    register = (item.get("register") or "").strip()
    if register:
        line += f" — {register}"
    notes = (item.get("additional_notes") or "").strip()
    if notes:
        line += f"; {notes}"
    return line + "."


def format_medical_aid_story_line(item: dict) -> str:
    display = (item.get("display_name") or item.get("name") or "").strip()
    if not display:
        return ""
    line = f"Medical aid: {display}"
    scheme_type = (item.get("type") or "").strip()
    if scheme_type:
        line += f" ({scheme_type})"
    notes = (item.get("additional_notes") or "").strip()
    if notes:
        line += f" — {notes}"
    return line + "."


def merge_medication(existing: list[dict], item: dict) -> list[dict]:
    name = (item.get("name") or "").strip().lower()
    rows = [dict(r) for r in existing]
    item = dict(item)
    item["dose"] = format_medication_dose(item)
    for i, row in enumerate(rows):
        if (row.get("name") or "").strip().lower() == name and name:
            rows[i] = {**row, **item}
            return rows
    rows.append(item)
    return rows


def add_to_medical_record(
    claim: dict,
    *,
    kind: str,
    item: dict[str, Any],
    sync_story: bool = True,
) -> dict[str, Any]:
    """Return claim field updates after adding a diagnosis or medication."""
    updates: dict[str, Any] = {}
    story_bits: list[str] = []

    if kind == "diagnosis":
        diagnoses = _parse_list(claim.get("medical_diagnoses_json"))
        merged = merge_diagnosis(diagnoses, item)
        updates["medical_diagnoses_json"] = json.dumps(merged)
        line = format_diagnosis_story_line(item)
        if line:
            story_bits.append(line)
    elif kind in ("medication", "therapy"):
        medications = _parse_list(claim.get("medical_medications_json"))
        merged = merge_medication(medications, item)
        updates["medical_medications_json"] = json.dumps(merged)
        line = format_medication_story_line(item)
        if line:
            story_bits.append(line)
    elif kind == "symptom":
        if sync_story:
            updates["illness_summary"] = merge_symptom_into_story(
                claim.get("illness_summary"),
                (item.get("name") or item.get("label") or "").strip(),
            )
        return updates
    elif kind == "practitioner":
        practitioners = _parse_list(claim.get("medical_practitioners_json"))
        merged = merge_practitioner(practitioners, item)
        updates["medical_practitioners_json"] = json.dumps(merged)
        line = format_practitioner_story_line(item)
        if sync_story and line:
            updates["illness_summary"] = append_illness_story(claim.get("illness_summary"), line)
        return updates
    elif kind == "medical_aid":
        aids = _parse_list(claim.get("medical_aids_json"))
        merged = merge_medical_aid(aids, item)
        updates["medical_aids_json"] = json.dumps(merged)
        line = format_medical_aid_story_line(item)
        if line:
            updates["medical_aid_history_note"] = append_illness_story(
                claim.get("medical_aid_history_note"),
                line,
            )
        if sync_story and line:
            updates["illness_summary"] = append_illness_story(
                claim.get("illness_summary"),
                line,
            )
        return updates
    else:
        raise ValueError(f"Unknown medical record kind: {kind}")

    if sync_story and story_bits:
        if kind == "therapy" and len(story_bits) == 1:
            prefix = "Therapy: "
        elif kind == "medication" and len(story_bits) == 1:
            prefix = "Treatment: "
        else:
            prefix = ""
        block = prefix + (" ".join(story_bits) if kind in ("medication", "therapy") else "\n".join(story_bits))
        updates["illness_summary"] = append_illness_story(claim.get("illness_summary"), block)

    return updates