"""Rejection letter text extraction and review-ground scanning."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from policy_processor import extract_text

REJECTION_GROUND_TERMS: list[dict[str, Any]] = [
    {
        "id": "preexisting",
        "ground": "Pre-existing condition",
        "patterns": [
            r"pre-?existing",
            r"prior to (?:the )?(?:commencement|inception|effective date|cover)",
            r"existed before (?:cover|commencement)",
            r"condition (?:was|is) excluded",
        ],
        "trap": "Pre-existing trap",
        "cure": "Separate baseline history from post-cover deterioration; gather cover-start proof and treating-doctor timeline.",
    },
    {
        "id": "waiting_period",
        "ground": "Waiting period",
        "patterns": [
            r"waiting period",
            r"qualifying period",
            r"within the first \d+ (?:day|month)",
            r"not satisfied the waiting",
        ],
        "trap": "Date trap",
        "cure": "Line up symptom onset, cover start, and first certificate against policy waiting-period wording.",
    },
    {
        "id": "not_disabled",
        "ground": "Not disabled / able to work",
        "patterns": [
            r"not (?:totally |)disabled",
            r"able to (?:perform|carry out|undertake)",
            r"no incapacity",
            r"fit for (?:work|duty|duties)",
            r"can (?:still )?(?:perform|do) (?:your|the) (?:duties|occupation|work)",
        ],
        "trap": "Diagnosis trap",
        "cure": "Respond with duty-impact matrix — symptoms blocking material duties, not diagnosis label alone.",
    },
    {
        "id": "own_occupation",
        "ground": "Own-occupation / material duties test",
        "patterns": [
            r"own occupation",
            r"material dut",
            r"essential dut",
            r"any occupation",
            r"modified dut",
            r"alternative employment",
        ],
        "trap": "Job-title trap",
        "cure": "Confirm policy test applied to actual duties; complete functional-capacity builder and employer role statement.",
    },
    {
        "id": "doa",
        "ground": "Date of Absence",
        "patterns": [
            r"date of absence",
            r"\bdoa\b",
            r"absence (?:date|commenced)",
            r"first day (?:of|you were) absent",
            r"incapacity (?:commenced|began)",
        ],
        "trap": "Date trap",
        "cure": "Request insurer DOA calculation notes; compare employer date, certificate date, and insurer-stated DOA.",
    },
    {
        "id": "notice",
        "ground": "Late notice / submission",
        "patterns": [
            r"late notice",
            r"failed to notify",
            r"outside the notice period",
            r"claim (?:was )?submitted late",
            r"did not (?:notify|advise) (?:us|the insurer)",
        ],
        "trap": "Date trap",
        "cure": "Capture first notice, form submission, and complete-claim dates separately with proof of send/receipt.",
    },
    {
        "id": "insufficient_evidence",
        "ground": "Insufficient evidence",
        "patterns": [
            r"insufficient (?:medical )?evidence",
            r"further (?:medical )?information",
            r"incomplete (?:information|documentation)",
            r"unable to assess",
            r"did not provide",
        ],
        "trap": "Specialist-evidence trap",
        "cure": "Run evidence-gap detector; request specific records list from insurer and obtain employer-held files.",
    },
    {
        "id": "specialist",
        "ground": "Specialist-level evidence",
        "patterns": [
            r"specialist(?:'s)? (?:report|evidence|opinion)",
            r"consultant(?:'s)? (?:report|letter)",
            r"independent medical examination",
            r"\bime\b",
        ],
        "trap": "Specialist-evidence trap",
        "cure": "Obtain specialist report addressing occupational incapacity; challenge IME if duties misstated.",
    },
    {
        "id": "exclusion",
        "ground": "Policy exclusion",
        "patterns": [
            r"excluded (?:under|from)",
            r"general exclusion",
            r"not covered (?:under|by)",
            r"falls outside (?:the )?cover",
        ],
        "trap": "Pre-existing trap",
        "cure": "Match cited exclusion clause to policy wording; check schedule vs rejection language drift.",
    },
    {
        "id": "non_disclosure",
        "ground": "Non-disclosure / misrepresentation",
        "patterns": [
            r"non-?disclosure",
            r"misrepresentation",
            r"failed to disclose",
            r"material fact",
        ],
        "trap": "Appeal-story trap",
        "cure": "Request exact questions asked at application; compare to disclosed medical aid and employment records.",
    },
    {
        "id": "threshold_shift",
        "ground": "Threshold / standard shift",
        "patterns": [
            r"reasonable accommodation",
            r"light dut",
            r"lesser occupation",
            r"earning capacity",
            r"partial disability",
        ],
        "trap": "Threshold-shift trap",
        "cure": "Compare guide/form language to policy test; document any shift from submission standard to rejection standard.",
    },
    {
        "id": "appeal_process",
        "ground": "Internal review / appeal rights",
        "patterns": [
            r"internal review",
            r"appeal",
            r"reconsideration",
            r"complaint procedure",
            r"ombud",
        ],
        "trap": "Appeal-story trap",
        "cure": "Diary review and ombud deadlines; structure response as issue-by-issue matrix not narrative alone.",
    },
]

_REASON_BLOCK_RE = re.compile(
    r"(?:"
    r"(?:reason|ground)s?\s*(?:for\s+(?:the\s+)?(?:decision|rejection))?|"
    r"we\s+(?:have\s+)?(?:declined|rejected)|"
    r"decision\s*:"
    r")"
    r"[\s:–-]*(.{40,400}?)(?=\n\n|\n(?:reason|ground|\d+\.)|$)",
    re.IGNORECASE | re.DOTALL,
)


def _clean_snippet(text: str, limit: int = 240) -> str:
    chunk = re.sub(r"\s+", " ", (text or "").strip())
    if len(chunk) <= limit:
        return chunk
    return chunk[: limit - 1].rsplit(" ", 1)[0] + "…"


def _snippet(text: str, match: re.Match, width: int = 160) -> str:
    start = max(0, match.start() - 40)
    end = min(len(text), match.end() + width)
    chunk = text[start:end]
    sent_m = re.search(r"([A-Z][^.!?]{20,}(?:\.|!|\?))", chunk)
    return _clean_snippet(sent_m.group(1) if sent_m else chunk, 260)


def _scan_ground(text: str, entry: dict[str, Any]) -> dict[str, Any]:
    lower = text.lower()
    best: re.Match | None = None
    for pattern in entry["patterns"]:
        m = re.search(pattern, lower, re.I)
        if m and (best is None or m.start() < best.start()):
            best = m
    found = best is not None
    return {
        "id": entry["id"],
        "ground": entry["ground"],
        "found": found,
        "snippet": _snippet(text, best) if best else "",
        "trap": entry.get("trap", ""),
        "cure": entry.get("cure", ""),
        "confidence": "high" if found and best and len(best.group()) > 8 else ("medium" if found else "none"),
    }


def _extract_decision_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    seen: set[str] = set()
    for m in _REASON_BLOCK_RE.finditer(text):
        block = _clean_snippet(m.group(1), 320)
        key = block.lower()[:80]
        if block and key not in seen:
            seen.add(key)
            blocks.append(block)
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\d+[\).\]]\s+\S", stripped) and len(stripped) > 35:
            block = _clean_snippet(stripped, 320)
            key = block.lower()[:80]
            if key not in seen:
                seen.add(key)
                blocks.append(block)
    return blocks[:8]


def analyze_rejection_text(text: str, filename: str = "") -> dict[str, Any]:
    normalized = re.sub(r"\r\n?", "\n", text or "")
    grounds = [_scan_ground(normalized, entry) for entry in REJECTION_GROUND_TERMS]
    matched = [g for g in grounds if g["found"]]
    decision_blocks = _extract_decision_blocks(normalized)

    return {
        "processed": bool(normalized.strip()),
        "filename": filename,
        "char_count": len(normalized),
        "grounds_matched": len(matched),
        "grounds": grounds,
        "decision_blocks": decision_blocks,
        "extracted": bool(normalized.strip()),
    }


def analyze_rejection_file(path: Path, filename: str = "") -> dict[str, Any]:
    text, pages = extract_text(path)
    result = analyze_rejection_text(text, filename or path.name)
    result["pages"] = pages
    if not result["processed"]:
        result["error"] = "Could not extract text — try PDF or text file."
    return result