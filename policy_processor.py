"""Lightweight policy document text extraction and cross-link analysis."""

from __future__ import annotations

import re
from pathlib import Path

from sa_reference_data import match_employer_in_text, match_insurer_in_text

POLICY_SCAN_TERMS: list[dict] = [
    {
        "id": "waiting_period",
        "term": "Waiting period",
        "definition_term": "Waiting Period",
        "fields": ["waiting_period"],
        "section": "Parties & key dates",
        "patterns": [r"waiting\s+period", r"deferred\s+period", r"elimination\s+period"],
    },
    {
        "id": "doa",
        "term": "Date of Absence",
        "definition_term": "Date of Absence",
        "fields": ["date_of_absence", "insurer_doa"],
        "section": "Key dates",
        "patterns": [r"date\s+of\s+absence", r"\bDOA\b", r"disability\s+date"],
    },
    {
        "id": "benefit",
        "term": "Income protection benefit",
        "definition_term": "Income Protection Benefit",
        "fields": ["benefit_percent", "gross_salary"],
        "section": "Salary & deductions",
        "patterns": [r"income\s+protection\s+benefit", r"disability\s+benefit", r"monthly\s+benefit", r"benefit\s+percentage"],
    },
    {
        "id": "own_occupation",
        "term": "Own occupation / disability test",
        "definition_term": "Own Occupation",
        "clause_patterns": [
            r"During the Initial Period\s+The Insured Person is totally incapable of performing his Own Occupation[^.]+\.",
            r"totally incapable of performing his Own Occupation with Any Employer[^.]+\.",
        ],
        "fields": ["occupation", "material_duties"],
        "section": "Occupation",
        "patterns": [r"own\s+occupation", r"regular\s+occupation", r"initial\s+period", r"extended\s+period", r"any\s+occupation"],
    },
    {
        "id": "notice",
        "term": "Notice & submission",
        "fields": ["first_notice", "form_submission", "complete_claim"],
        "section": "Key dates",
        "patterns": [r"first\s+notice", r"notify\s+old\s+mutual", r"prescribed\s+form", r"complete\s+claim", r"proof\s+of\s+claim"],
    },
    {
        "id": "preexisting",
        "term": "Pre-existing condition",
        "definition_term": "Pre-existing",
        "fields": ["illness_summary"],
        "section": "Health story",
        "patterns": [r"pre-?existing", r"look[- ]back", r"prior\s+condition"],
    },
    {
        "id": "specialist_evidence",
        "term": "Specialist evidence",
        "definition_term": "Specialist",
        "fields": ["specialist_required"],
        "section": "Health story",
        "patterns": [
            r"specialist\s+(?:report|evidence|opinion|certificate)",
            r"consultant\s+(?:report|evidence|opinion)",
            r"independent\s+medical\s+(?:examination|examiner|assessment|report)",
            r"\bIME\b",
            r"second\s+opinion",
            r"medical\s+practitioner\s+of\s+(?:our|the\s+insurer)",
            r"psychiatrist|psychologist|neurologist|orthopaedic\s+surgeon",
            r"objective\s+(?:medical\s+)?evidence",
            r"specialist\s+confirmation",
        ],
    },
    {
        "id": "hospital_admission",
        "term": "Hospital admission",
        "definition_term": "Hospital",
        "fields": ["hospital_admission"],
        "section": "Health story",
        "patterns": [
            r"hospitalis(?:ed|ation|ed)",
            r"hospital\s+admission",
            r"inpatient|in-patient",
            r"ward\s+admission",
            r"admitted\s+to\s+(?:a\s+)?hospital",
        ],
    },
    {
        "id": "offset",
        "term": "Offsets & deductions",
        "fields": ["other_deductions", "salary_notes"],
        "section": "Salary & deductions",
        "patterns": [r"offset", r"deductible\s+income", r"integration", r"other\s+income"],
    },
    {
        "id": "complaint",
        "term": "Review & complaint route",
        "fields": ["review_deadline", "ombud_deadline"],
        "section": "Key dates",
        "patterns": [r"internal\s+review", r"ombud", r"complaint", r"reassessment", r"appeal"],
    },
    {
        "id": "exclusion",
        "term": "Exclusions",
        "fields": ["illness_summary", "notes"],
        "section": "Notes",
        "patterns": [r"\bexclusions?\b", r"self[- ]inflicted", r"intoxication", r"criminal\s+act"],
    },
    {
        "id": "cover",
        "term": "Cover & eligibility",
        "definition_term": "Actively at Work",
        "fields": ["cover_start", "policy_number"],
        "section": "Parties & key dates",
        "patterns": [r"commencement\s+of\s+cover", r"commencement\s+date", r"eligible\s+employee", r"member\s+class", r"actively\s+at\s+work"],
    },
]

_EMPLOYER_ALIASES: dict[str, str] = {
    "deloitte & touche": "Deloitte South Africa",
    "deloitte and touche": "Deloitte South Africa",
    "pwc south africa": "PwC South Africa",
    "ernst & young": "EY South Africa",
    "ernst and young": "EY South Africa",
    "kpmg south africa": "KPMG South Africa",
}

_PDF_JUNK = re.compile(
    r"91855/LC/EB\s*[\d\s]+|(?:\n|^)\s*1\s+March\s+2023\s*(?:\n|Page\s+\d+)|\bPage\s+\d+\b",
    re.I,
)

_SECTION_ORDER = [
    "Parties & key dates",
    "Occupation",
    "Health story",
    "Salary & deductions",
    "Key dates",
    "Notes",
]

POLICY_FIELD_HINTS: list[dict] = [
    {
        "id": "medical_aid",
        "fields": ["medical_aid_deductions"],
        "topic": "Medical aid",
        "patterns": [
            r"medical\s+aid",
            r"health\s+benefit",
            r"medical\s+scheme",
            r"hospital\s+plan",
            r"gap\s+cover",
        ],
    },
    {
        "id": "pension",
        "fields": ["pension_deductions"],
        "topic": "Pension / provident fund",
        "patterns": [
            r"pension\s+fund",
            r"provident\s+fund",
            r"retirement\s+fund",
            r"retirement\s+annuit",
            r"RA\s+contribution",
        ],
    },
    {
        "id": "uif",
        "fields": ["uif_deductions"],
        "topic": "UIF",
        "patterns": [r"\bUIF\b", r"unemployment\s+insurance", r"unemployment\s+benefit"],
    },
    {
        "id": "tax",
        "fields": ["tax_deductions"],
        "topic": "PAYE / tax",
        "patterns": [r"\bPAYE\b", r"tax\s+deduct", r"income\s+tax\s+deduction"],
    },
    {
        "id": "hospital",
        "fields": ["hospital_admission"],
        "topic": "Hospital admission",
        "patterns": [r"hospitalis", r"hospital\s+admission", r"inpatient", r"ward\s+admission"],
    },
    {
        "id": "specialist",
        "fields": ["specialist_required"],
        "topic": "Specialist evidence",
        "patterns": [
            r"specialist\s+(?:report|evidence|opinion|certificate)",
            r"consultant\s+(?:report|evidence|opinion)",
            r"independent\s+medical\s+(?:examination|examiner|assessment|report)",
            r"\bIME\b",
            r"second\s+opinion",
            r"medical\s+practitioner\s+of\s+(?:our|the\s+insurer)",
            r"objective\s+(?:medical\s+)?evidence",
            r"specialist\s+confirmation",
        ],
    },
    {
        "id": "residual",
        "fields": ["gross_salary", "benefit_percent"],
        "topic": "Residual / partial disability",
        "patterns": [r"residual\s+disability", r"partial\s+disability", r"proportionate\s+benefit"],
    },
]

_STATUS_PATTERNS: list[tuple[str, str, list[str]]] = [
    ("excluded", "Not covered / excluded", [r"exclud", r"not\s+covered", r"no\s+benefit", r"shall\s+not\s+pay"]),
    ("offset", "May offset or integrate with benefit", [r"offset", r"deduct", r"integration", r"reduce\s+the\s+benefit", r"other\s+income"]),
    ("covered", "Referenced as covered benefit", [r"covered", r"included", r"benefit\s+payable", r"we\s+will\s+pay"]),
    ("employer_paid", "Employer-paid / fringe benefit", [r"employer\s+(?:pays|paid|contribution)", r"company\s+contribution", r"fringe\s+benefit"]),
]


def _normalize_policy_text(text: str) -> str:
    """Collapse PDF line-break artefacts and strip repeated headers/footers."""
    if not text:
        return ""
    t = text.replace("\uf0b7", "· ").replace("\r\n", "\n")
    t = _PDF_JUNK.sub(" ", t)
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)
    lines = t.split("\n")
    merged: list[str] = []
    buf = ""
    for raw in lines:
        line = raw.strip()
        if not line:
            if buf:
                merged.append(buf)
                buf = ""
            continue
        if buf:
            continues = (
                not re.search(r"[.;:]$", buf)
                and not re.match(r"^\d+\.\s", line)
                and (line[0].islower() or len(line) < 72)
            )
            if continues:
                buf += " " + line
            else:
                merged.append(buf)
                buf = line
        else:
            buf = line
    if buf:
        merged.append(buf)
    return re.sub(r"[ \t]+", " ", "\n".join(merged))


def _clean_snippet(snippet: str, max_len: int = 280) -> str:
    s = re.sub(r"\s+", " ", (snippet or "").strip())
    s = _PDF_JUNK.sub(" ", s).strip()
    if not s:
        return ""
    if s[0].islower() or s[0].isdigit():
        m = re.search(r"(?:^|[.;]\s+)([A-Z][a-z].*)", s)
        if m:
            s = m.group(1).strip()
        else:
            m2 = re.search(r"\b([A-Z][a-z]{2,})", s)
            if m2:
                s = s[m2.start() :]
    s = re.sub(r"\s+", " ", s).strip()
    if re.search(r"(?:www\.|https?://)\s*$", s, re.I):
        s = re.sub(r"[^.!?]*(?:www\.|https?://)\s*$", "", s).strip()
    if len(s) > max_len:
        cut = s[:max_len]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        s = cut.rstrip(".,;:") + "…"
    return s


def _extract_glossary_definition(text: str, term: str) -> str:
    """Pull a glossary-style definition where the term sits on its own line or inline."""
    if not term:
        return ""
    term_re = re.escape(term.strip())
    patterns = [
        rf"(?:^|\n){term_re}\s*\n+([A-Z0-9].{{20,400}}?)(?=\n[A-Z][a-z]{{2,}}(?:\s|\n)|\n\d+\.\s|\Z)",
        rf"{term_re}\s+((?:The|A|An|Being)\s+.+?)(?=\n[A-Z][a-z]{{2,}}\s|\n\d+\.\s|\Z)",
        rf"{term_re}\s*\n\s*([A-Z].{{20,400}}?)(?=\n[A-Z][a-z]{{2,}}|\Z)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.I | re.M | re.S)
        if m:
            defn = re.sub(r"\s+", " ", m.group(1)).strip()
            cleaned = _clean_snippet(defn, 320)
            if len(cleaned) >= 24:
                return cleaned
    return ""


def _strip_policy_number(raw: str) -> str | None:
    val = re.split(r"\s+Effective\b", raw, maxsplit=1, flags=re.I)[0]
    val = re.split(r"\s+(?:Policy|Master\s+Policy)\b", val, maxsplit=1, flags=re.I)[0]
    return _valid_policy_number(val)


def _clause_snippet(text: str, entry: dict) -> tuple[bool, str]:
    """Prefer glossary definitions; fall back to best in-context sentence."""
    defn_terms = [
        entry.get("definition_term"),
        *(entry.get("definition_alternatives") or []),
        entry.get("term"),
    ]
    for defn_term in defn_terms:
        if not defn_term:
            continue
        defn = _extract_glossary_definition(text, defn_term)
        if defn:
            return True, defn

    for cp in entry.get("clause_patterns", []):
        m = re.search(cp, text, re.I | re.S)
        if m:
            snippet = _clean_snippet(m.group(0))
            if len(snippet) >= 24:
                return True, snippet

    lower = text.lower()
    best: tuple[int, str] | None = None
    for pattern in entry.get("patterns", []):
        for m in re.finditer(pattern, lower, re.I):
            start = max(0, m.start() - 20)
            end = min(len(text), m.end() + 260)
            chunk = text[start:end]
            sent_m = re.search(
                r"([A-Z][^.!?]{20,}(?:\.|!|\?))",
                chunk,
            )
            snippet = _clean_snippet(sent_m.group(1) if sent_m else chunk)
            if len(snippet) < 20:
                continue
            score = m.start()
            if "definition" in snippet.lower() or defn_term.lower() in snippet.lower():
                score -= 5000
            if _PDF_JUNK.search(snippet):
                score += 2000
            if best is None or score < best[0]:
                best = (score, snippet)
    if best:
        return True, best[1]
    return False, ""


def extract_text(path: Path) -> tuple[str, int]:
    """Return document text and approximate page count."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import fitz  # type: ignore

        doc = fitz.open(path)
        pages = len(doc)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text, pages
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace"), 1
    return "", 0


def _snippet(text: str, match: re.Match, width: int = 140) -> str:
    start = max(0, match.start() - 30)
    end = min(len(text), match.end() + width)
    chunk = text[start:end]
    sent_m = re.search(r"([A-Z][^.!?]{15,}(?:\.|!|\?))", chunk)
    return _clean_snippet(sent_m.group(1) if sent_m else chunk, 220)


def _wider_snippet(text: str, match: re.Match, width: int = 220) -> str:
    return _snippet(text, match, width)


def _infer_coverage_status(snippet: str) -> tuple[str, str]:
    lower = snippet.lower()
    for status_id, label, patterns in _STATUS_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, lower, re.I):
                return status_id, label
    return "mentioned", "Mentioned in policy — check exact wording"


def _build_field_hints(text: str) -> dict[str, dict]:
    """Map form field ids to hover tooltip content from policy text."""
    hints: dict[str, dict] = {}
    lower = text.lower()

    guidance_map = {
        "medical_aid": "Confirm whether medical aid contributions or benefits are offset against your income protection payment.",
        "pension": "Pension and provident fund contributions may affect benefit calculations or offsets — match payslip deductions to policy wording.",
        "uif": "UIF receipts can integrate with disability benefits under some policies.",
        "tax": "Tax treatment of benefits may differ from salary — note any PAYE references in the policy.",
        "hospital": "Hospital admission clauses may trigger different evidence rules or waiting-period treatment.",
        "specialist": (
            "Your policy references specialist-level evidence — tick the flag below and gather "
            "consultant reports, IME findings, or insurer-requested specialist letters."
        ),
        "residual": "Residual disability wording affects partial return-to-work scenarios and benefit percentage.",
    }

    for entry in POLICY_FIELD_HINTS:
        best_match: re.Match | None = None
        for pattern in entry["patterns"]:
            m = re.search(pattern, lower, re.I)
            if m and (best_match is None or m.start() < best_match.start()):
                best_match = m
        if not best_match:
            continue
        snippet = _wider_snippet(text, best_match)
        status_id, status_label = _infer_coverage_status(snippet)
        guidance = guidance_map.get(entry["id"], "Review this clause against your payslips and claim stage.")
        for field_id in entry["fields"]:
            hints[field_id] = {
                "found": True,
                "topic": entry["topic"],
                "status": status_id,
                "status_label": status_label,
                "detail": snippet[:320],
                "guidance": guidance,
            }

    for term in POLICY_SCAN_TERMS:
        matched, snippet = _clause_snippet(text, term)
        if not matched:
            continue
        status_id, status_label = _infer_coverage_status(snippet)
        for field_id in term["fields"]:
            if field_id in hints:
                continue
            hints[field_id] = {
                "found": True,
                "topic": term["term"],
                "status": status_id,
                "status_label": status_label,
                "detail": snippet[:320],
                "guidance": f"Policy references {term['term'].lower()} — complete the linked field using this wording.",
            }

    return hints


_INVALID_POLICY_TOKENS = frozenset({
    "which", "under", "means", "the", "this", "that", "shall", "will", "may", "must",
    "when", "where", "such", "each", "any", "all", "being", "been", "have", "has",
    "with", "from", "into", "upon", "your", "our", "their", "assigned", "referred",
})

_PARTY_BOILERPLATE = re.compile(
    r"\b(?:employment|contract|legal|document|specifies|specified|means|shall|defined|"
    r"definition|hereinafter|whereas|pursuant|accordance|including|excluding|agreement|"
    r"schedule|annexure|appendix|clause|section|paragraph)\b",
    re.I,
)

_PARTY_STOP = re.compile(
    r"\s+(?:and\s+(?:any|all|other|each|every)\b|or\s+any\b|"
    r"policy\s*(?:no|number|#)|master\s+policy|group\s+policy|employer|insurer|"
    r"underwritten|waiting\s+period|member(?:ship)?|certificate|claim)\b",
    re.I,
)

_LABELLED_LINE = re.compile(
    r"^\s*(?P<label>policy\s*(?:no|number|#)|master\s+policy\s*(?:no|number)?|"
    r"group\s+policy\s*(?:no|number)?|certificate\s*(?:no|number)?|"
    r"membership\s*(?:no|number)?|policyholder|policy\s+holder|master\s+policyholder|"
    r"group\s+policyholder|principal\s+employer|participating\s+employer|"
    r"employer|employing\s+company|name\s+of\s+employer|insurer|life\s+assurer|"
    r"underwritten\s+by|administered\s+by|effective|commencement\s+date)\s*"
    r"\n?\s*:\s*(?P<value>.+?)\s*$",
    re.I | re.M,
)

_LABEL_KEY_MAP = {
    "policy no": "policy_number",
    "policy number": "policy_number",
    "policy #": "policy_number",
    "master policy no": "policy_number",
    "master policy number": "policy_number",
    "group policy no": "policy_number",
    "group policy number": "policy_number",
    "certificate no": "policy_number",
    "certificate number": "policy_number",
    "membership no": "policy_number",
    "membership number": "policy_number",
    "policyholder": "policyholder",
    "policy holder": "policyholder",
    "master policyholder": "policyholder",
    "group policyholder": "policyholder",
    "principal employer": "employer",
    "participating employer": "employer",
    "employer": "employer",
    "employing company": "employer",
    "name of employer": "employer",
    "insurer": "insurer",
    "life assurer": "insurer",
    "underwritten by": "insurer",
    "administered by": "insurer",
    "effective": "group_policy_effective",
    "commencement date": "group_policy_effective",
}


def _trim_party_fragment(value: str, max_len: int = 70) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    for splitter in (
        _PARTY_STOP,
        re.compile(r"\.\s+(?:Employment|The|A|An|This|That|Which|Any)\b"),
        re.compile(r"\s+[-–—]\s+"),
    ):
        m = splitter.search(cleaned)
        if m:
            cleaned = cleaned[: m.start()].strip()
    cleaned = cleaned.strip(" \t.,;:\"'")
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rsplit(" ", 1)[0]
    return cleaned


def _valid_policy_number(value: str) -> str | None:
    v = _trim_party_fragment(value, 40)
    v = re.sub(r"\s+", " ", v).strip()
    if len(v) < 4 or len(v) > 40:
        return None
    if v.lower() in _INVALID_POLICY_TOKENS:
        return None
    if not re.search(r"\d", v):
        return None
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9\s\-/.]*", v, re.I):
        return None
    if re.fullmatch(r"[a-zA-Z]+", v):
        return None
    return v


def _resolve_employer_name(value: str) -> str | None:
    v = _valid_party_name(value)
    if not v:
        return None
    alias = _EMPLOYER_ALIASES.get(v.lower())
    if alias:
        return alias
    known = match_employer_in_text(v)
    return known or v


def _valid_party_name(value: str, *, allow_short: bool = False) -> str | None:
    v = _trim_party_fragment(value, 70)
    if not allow_short and len(v) < 4:
        return None
    if allow_short and len(v) < 2:
        return None
    if v.lower() in _INVALID_POLICY_TOKENS:
        return None
    if _PARTY_BOILERPLATE.search(v):
        return None
    if re.match(r"^(?:and|or|the|any|which|under|means)\b", v, re.I):
        return None
    words = v.split()
    if len(words) > 7:
        return None
    if len(words) == 1 and words[0].lower() in _INVALID_POLICY_TOKENS:
        return None
    return v


def _normalise_label(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def _extract_labelled_lines(text: str) -> dict[str, str]:
    """Prefer single-line Label: Value rows from schedules and certificates."""
    found: dict[str, str] = {}
    for m in _LABELLED_LINE.finditer(text):
        label = _normalise_label(m.group("label"))
        key = _LABEL_KEY_MAP.get(label)
        if not key:
            continue
        raw = m.group("value")
        if key == "policy_number":
            val = _strip_policy_number(raw)
        elif key == "insurer":
            val = _valid_party_name(raw) or match_insurer_in_text(raw)
        elif key == "employer":
            val = _resolve_employer_name(raw)
        elif key == "group_policy_effective":
            val = _trim_party_fragment(raw, 40)
            if not val or not re.search(r"\d", val):
                val = None
        else:
            val = _valid_party_name(raw)
        if val and key not in found:
            found[key] = val
    return found


def _extract_cover_page_parties(text: str) -> dict[str, str]:
    """Read schedule-style cover blocks common in SA group GIP policies."""
    found: dict[str, str] = {}
    pn = re.search(
        r"Policy\s+Number\s*:\s*([A-Z0-9][A-Z0-9\s\-/.]{2,28}?)(?:\s+Effective\b|\s*\n)",
        text,
        re.I,
    )
    if pn:
        val = _strip_policy_number(pn.group(1))
        if val:
            found["policy_number"] = val

    eff = re.search(
        r"Effective\s*:\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        text,
        re.I,
    )
    if eff:
        found["group_policy_effective"] = eff.group(1).strip()

    employer_m = re.search(
        r"(?:^|\n)\s*([A-Z][A-Z0-9&'.][A-Z0-9&'. ]{2,48})\s*\n\s*GROUP\s+INCOME\s+PROTECTION",
        text,
        re.I | re.M,
    )
    if employer_m:
        emp = _resolve_employer_name(employer_m.group(1))
        if emp:
            found["employer"] = emp
            found.setdefault("policyholder", emp)

    insurer_m = re.search(
        r"(OLD\s+MUTUAL[^\n]{0,80}|SANLAM[^\n]{0,60}|LIBERTY[^\n]{0,60}|"
        r"MOMENTUM[^\n]{0,60}|DISCOVERY\s+LIFE[^\n]{0,60})",
        text,
        re.I,
    )
    if insurer_m:
        insurer = match_insurer_in_text(insurer_m.group(1)) or _valid_party_name(insurer_m.group(1))
        if insurer:
            found["insurer"] = insurer

    return found


def _extract_parties(text: str) -> dict[str, str]:
    """Extract insurer, policyholder, policy number, and employer from policy text."""
    parties = _extract_labelled_lines(text)
    for key, value in _extract_cover_page_parties(text).items():
        parties.setdefault(key, value)

    if not parties.get("policy_number"):
        for pattern in (
            r"policy\s*(?:no|number)\s*\n?\s*:\s*([A-Z0-9][A-Z0-9\s\-/.]{3,32})",
            r"master\s+policy\s*(?:no|number)\s*\n?\s*:\s*([A-Z0-9][A-Z0-9\s\-/.]{3,32})",
            r"group\s+policy\s*(?:no|number)\s*\n?\s*:\s*([A-Z0-9][A-Z0-9\s\-/.]{3,32})",
            r"POLICY\s+([A-Z]{1,4}\s*[\d\s]{4,12})",
        ):
            m = re.search(pattern, text, re.I)
            if m:
                val = _strip_policy_number(m.group(1))
                if val:
                    parties["policy_number"] = val
                    break

    insurer = parties.get("insurer") or match_insurer_in_text(text)
    if insurer:
        parties["insurer"] = insurer

    policyholder = parties.get("policyholder")
    if policyholder:
        known_employer = match_employer_in_text(policyholder)
        if known_employer and not parties.get("employer"):
            parties["employer"] = known_employer

    return {k: v for k, v in parties.items() if v}


def _extract_waiting_period(text: str) -> str | None:
    defn = _extract_glossary_definition(text, "Waiting Period")
    if defn:
        m = re.search(r"(\d+)\s*[- ]?\s*month", defn, re.I)
        if m:
            n = m.group(1)
            return f"{n} month{'s' if n != '1' else ''}"
        m = re.search(r"(\d+)\s*[- ]?\s*day", defn, re.I)
        if m:
            n = m.group(1)
            return f"{n} day{'s' if n != '1' else ''}"
    return None


def _extract_member_cover_start(text: str) -> str | None:
    """Member-specific cover commencement — not the master/group policy effective date."""
    patterns = (
        r"member(?:ship)?\s+(?:commencement|entry)\s+(?:date|date\s+of\s+entry)?\s*"
        r"(?:\n?\s*:\s*|\s+)([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        r"commencement\s+of\s+(?:your\s+)?(?:member\s+)?cover\s*"
        r"(?:\n?\s*:\s*|\s+)([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        r"date\s+(?:you\s+)?joined\s+(?:the\s+)?(?:scheme|benefit|cover)\s*"
        r"(?:\n?\s*:\s*|\s+)([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        r"member\s+certificate[^\n]{0,80}commencement[^\n]{0,40}"
        r"([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
    )
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            return m.group(1).strip()
    return None


def _suggest_values(text: str) -> dict[str, str]:
    suggested: dict[str, str] = {}
    parties = _extract_parties(text)
    for key, value in parties.items():
        if key == "group_policy_effective":
            continue
        suggested[key] = value

    member_cover = _extract_member_cover_start(text)
    if member_cover:
        suggested["cover_start"] = member_cover

    benefit = re.search(r"(\d{1,3})\s*%\s*(?:of|benefit|income|salary)", text, re.I)
    if benefit:
        suggested["benefit_percent"] = f"{benefit.group(1)}%"
    waiting = _extract_waiting_period(text)
    if waiting:
        suggested["waiting_period"] = waiting
    return suggested


def analyze_policy_text(text: str, filename: str = "") -> dict:
    """Scan policy text and build cross-links to intake form areas."""
    normalized = _normalize_policy_text(text or "")
    terms_found: list[dict] = []

    for entry in POLICY_SCAN_TERMS:
        matched, snippet = _clause_snippet(normalized, entry)
        terms_found.append({
            "id": entry["id"],
            "term": entry["term"],
            "found": matched,
            "fields": entry["fields"],
            "section": entry["section"],
            "snippet": snippet,
        })

    cross_links: list[dict] = []
    for section in _SECTION_ORDER:
        items = [t for t in terms_found if t["found"] and t["section"] == section]
        if items:
            cross_links.append({
                "section": section,
                "items": [
                    {
                        "term": i["term"],
                        "fields": i["fields"],
                        "snippet": i["snippet"][:200],
                    }
                    for i in items
                ],
            })

    suggested = _suggest_values(normalized)
    parties = _extract_parties(normalized)
    field_hints = _build_field_hints(normalized)
    party_labels = {
        "policy_number": "Policy number",
        "policyholder": "Policyholder",
        "insurer": "Insurer",
        "employer": "Employer",
        "cover_start": "Your cover start",
    }
    for field_id, value in parties.items():
        if field_id == "group_policy_effective":
            continue
        field_hints.setdefault(field_id, {
            "found": True,
            "topic": party_labels.get(field_id, field_id.replace("_", " ").title()),
            "status": "mentioned",
            "status_label": "Extracted from uploaded policy",
            "detail": f"{party_labels.get(field_id, field_id)}: {value}",
            "guidance": "Auto-filled from policy upload — confirm against your schedule or member certificate.",
        })
    if suggested.get("cover_start"):
        field_hints["cover_start"] = {
            "found": True,
            "topic": "Your cover start",
            "status": "mentioned",
            "status_label": "Member cover date detected",
            "detail": f"Your cover start: {suggested['cover_start']}",
            "guidance": (
                "This looks like a member-specific commencement date. "
                "Confirm on your member certificate or HR benefits confirmation — "
                "not the group/master policy effective date."
            ),
        }

    policy_reference: dict[str, dict] = {}
    if parties.get("group_policy_effective"):
        policy_reference["group_policy_effective"] = {
            "label": "Group policy effective",
            "value": parties["group_policy_effective"],
            "note": (
                "Master/group policy commencement from the uploaded document. "
                "This is not necessarily when your personal membership cover started — "
                "use your member certificate or HR schedule for your own cover start."
            ),
        }

    traps: list[str] = []
    if parties.get("group_policy_effective"):
        traps.append(
            "Group policy effective date found — that is the master scheme date, not automatically "
            "your personal cover start. Check your member certificate."
        )
    if sum(1 for t in terms_found if t["id"] in ("doa", "notice", "waiting_period") and t["found"]) >= 2:
        traps.append("Date trap — policy defines several different dates; capture each separately in Key dates.")
    if any(t["found"] for t in terms_found if t["id"] == "own_occupation"):
        traps.append("Own-occupation test found — complete Material duties, not job title alone.")
    if any(t["found"] for t in terms_found if t["id"] == "preexisting"):
        traps.append("Pre-existing wording found — separate baseline condition from post-cover deterioration.")
    if "medical_aid_deductions" in field_hints:
        traps.append("Medical aid mentioned — check offset/integration clauses before accepting net-benefit figures.")
    if "pension_deductions" in field_hints:
        traps.append("Pension/provident mentioned — confirm whether retirement fund contributions affect benefit base.")
    if field_hints.get("specialist_required", {}).get("found"):
        traps.append(
            "Specialist-evidence trap — policy or assessor may require consultant-level reports. "
            "Clarify what was requested and whether your treating specialist already covered it."
        )
    if field_hints.get("hospital_admission", {}).get("found"):
        traps.append(
            "Hospital admission wording found — admission records may be required; "
            "do not let diagnosis labels replace duty-impact evidence."
        )

    evidence_flags: dict[str, bool] = {}
    if field_hints.get("specialist_required", {}).get("found"):
        evidence_flags["specialist_required"] = True
    if field_hints.get("hospital_admission", {}).get("found"):
        evidence_flags["hospital_admission"] = True

    return {
        "processed": bool(normalized.strip()),
        "filename": filename,
        "char_count": len(normalized),
        "terms": terms_found,
        "cross_links": cross_links,
        "suggested": suggested,
        "parties": parties,
        "policy_reference": policy_reference,
        "field_hints": field_hints,
        "evidence_flags": evidence_flags,
        "traps": traps,
        "terms_matched": sum(1 for t in terms_found if t["found"]),
    }


def analyze_policy_file(path: Path, filename: str = "") -> dict:
    text, pages = extract_text(path)
    result = analyze_policy_text(text, filename or path.name)
    result["pages"] = pages
    result["extracted"] = bool(text.strip())
    if not text.strip():
        result["error"] = "Could not extract text — try PDF or text file, or enter details manually."
    return result