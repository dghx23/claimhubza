"""Duty-impact matrix — functional-capacity builder output."""

from __future__ import annotations

import json
import re

_DUTY_LINK_RE = re.compile(
    r"Duty link \(([^)]+)\):\s*cannot perform (.+?) because (.+?)\.",
    re.IGNORECASE | re.DOTALL,
)
_WORK_IMPACT_RE = re.compile(
    r"Work impact:\s*cannot perform (.+?) because (.+?)\s*[—–-]\s*(.+?) capacity affected\.",
    re.IGNORECASE | re.DOTALL,
)


def parse_duty_links_from_story(text: str) -> list[dict[str, str]]:
    """Extract symptom → duty rows from illness summary text."""
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for block in re.split(r"\n\s*\n+", text or ""):
        block = block.strip()
        if not block:
            continue
        m = _DUTY_LINK_RE.search(block)
        if m:
            domain_label, duty, symptom = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            key = "|".join((domain_label.lower(), symptom.lower(), duty.lower()))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "domain": "",
                "domain_label": domain_label,
                "symptom": symptom,
                "duty": duty,
                "line": block if block.endswith(".") else block + ".",
            })
            continue
        w = _WORK_IMPACT_RE.search(block)
        if w:
            duty, symptom, domain_label = w.group(1).strip(), w.group(2).strip(), w.group(3).strip()
            key = "|".join((domain_label.lower(), symptom.lower(), duty.lower()))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "domain": "",
                "domain_label": domain_label,
                "symptom": symptom,
                "duty": duty,
                "line": block if block.endswith(".") else block + ".",
            })
    return rows


def load_functional_capacity(raw_json: str | None, illness_summary: str | None) -> dict:
    """Load matrix from saved JSON or parse from story."""
    if raw_json and raw_json.strip():
        try:
            data = json.loads(raw_json)
            if isinstance(data, dict) and isinstance(data.get("rows"), list):
                return data
        except json.JSONDecodeError:
            pass
    rows = parse_duty_links_from_story(illness_summary or "")
    return {"rows": rows, "statement": build_functional_capacity_statement(rows)}


def build_functional_capacity_statement(rows: list[dict]) -> str:
    if not rows:
        return ""
    lines = [
        "FUNCTIONAL-CAPACITY / DUTY-IMPACT MATRIX",
        "Symptom → material duty links (insurer functional test):",
        "",
    ]
    for i, row in enumerate(rows, 1):
        domain = row.get("domain_label") or row.get("domain") or "Work"
        symptom = row.get("symptom", "")
        duty = row.get("duty", "")
        lines.append(f"{i}. [{domain}] Cannot perform: {duty}")
        lines.append(f"   Because: {symptom}")
        lines.append("")
    lines.append(
        "Diagnosis trap check: each row links symptoms to material duties — not diagnosis labels alone."
    )
    return "\n".join(lines).strip()


def functional_capacity_for_claim(claim: dict) -> str:
    """Combined statement for claim pack — matrix plus occupation duties."""
    fc = load_functional_capacity(
        claim.get("functional_capacity_json"),
        claim.get("illness_summary"),
    )
    parts: list[str] = []
    statement = (fc.get("statement") or "").strip()
    if statement:
        parts.append(statement)
    duties = (claim.get("material_duties") or "").strip()
    if duties:
        parts.append("")
        parts.append("MATERIAL DUTIES (occupation profile):")
        parts.append(duties)
    if parts:
        return "\n".join(parts)
    return "_Not yet completed — use the Functional capacity workspace module._"