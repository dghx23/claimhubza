"""ESCO occupation search — European standard occupation & skills database."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

from functional_map import build_functional_map

ESCO_SEARCH = "https://ec.europa.eu/esco/api/search"
ESCO_OCCUPATION = "https://ec.europa.eu/esco/api/resource/occupation"
TIMEOUT = 12


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "ClaimBuddy/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _localized_literal(block: dict | str | None, lang: str = "en") -> str:
    if not block:
        return ""
    if isinstance(block, str):
        return block.strip()
    for key in (lang, "en-us", "en-gb"):
        entry = block.get(key)
        if isinstance(entry, dict):
            return (entry.get("literal") or "").strip()
        if isinstance(entry, str):
            return entry.strip()
    for entry in block.values():
        if isinstance(entry, dict) and entry.get("literal"):
            return entry["literal"].strip()
    return ""


def search_occupations(query: str, limit: int = 10) -> list[dict]:
    """Search ESCO occupations by keyword."""
    q = (query or "").strip()
    if len(q) < 2:
        return []
    params = urllib.parse.urlencode({
        "language": "en",
        "text": q,
        "type": "occupation",
        "limit": min(limit, 20),
        "offset": 0,
    })
    try:
        data = _fetch_json(f"{ESCO_SEARCH}?{params}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []
    results = []
    for item in data.get("_embedded", {}).get("results", []):
        title = (
            (item.get("preferredLabel") or {}).get("en")
            or item.get("title")
            or item.get("searchHit")
            or ""
        ).strip()
        if not title:
            continue
        results.append({
            "uri": item.get("uri", ""),
            "title": title,
            "code": item.get("code") or "",
            "hint": (item.get("searchHit") or title).strip(),
        })
    return results


_VERB_STARTS = frozenset({
    "advise", "analyse", "analyze", "arrange", "assess", "audit", "calculate", "check",
    "compile", "conduct", "coordinate", "create", "debug", "design", "develop", "draft",
    "ensure", "establish", "evaluate", "examine", "follow", "handle", "identify",
    "implement", "inspect", "install", "interpret", "investigate", "liaise", "maintain",
    "manage", "monitor", "negotiate", "operate", "organise", "organize", "perform",
    "plan", "pose", "prepare", "present", "process", "provide", "record", "report",
    "resolve", "review", "supervise", "support", "test", "track", "train", "update",
    "use", "verify", "write",
})


def _looks_like_verb_phrase(skill: str) -> bool:
    first = skill.split()[0].lower() if skill else ""
    if first in _VERB_STARTS:
        return True
    return len(first) > 4 and first.endswith(("ate", "ute", "ify", "ise", "ize"))


def _skill_to_plain_phrase(skill: str) -> str:
    """Turn an ESCO skill label into plain 'you …' language."""
    s = skill.strip().rstrip(".")
    if not s:
        return ""
    lower = s.lower()
    if lower.startswith("you "):
        return lower
    if " " not in s:
        return f"you apply knowledge of {lower}"
    if _looks_like_verb_phrase(s):
        return f"you {lower}"
    return f"you work with {lower}"


def _join_plain_phrases(phrases: list[str]) -> str:
    if not phrases:
        return ""
    if len(phrases) == 1:
        return phrases[0]
    if len(phrases) == 2:
        return f"{phrases[0]} and {phrases[1]}"
    return ", ".join(phrases[:-1]) + f", and {phrases[-1]}"


_COGNITIVE_KW = (
    "analyse", "analyze", "plan", "decide", "report", "review", "calculate", "design",
    "develop", "interpret", "assess", "evaluate", "research", "draft", "compile",
)
_PHYSICAL_KW = (
    "lift", "stand", "operate", "install", "inspect", "travel", "drive", "manual",
    "physical", "site", "field", "equipment", "machinery",
)
_PEOPLE_KW = (
    "client", "customer", "team", "supervis", "present", "negotiat", "liaise",
    "consult", "stakeholder", "meeting", "communicat", "advise", "train",
)
_PRESSURE_KW = ("deadline", "pressure", "shift", "hour", "overtime", "urgent", "risk", "safety")


def _skill_matches(skills: list[str], keywords: tuple[str, ...]) -> list[str]:
    hits = []
    for skill in skills:
        lower = skill.lower()
        if any(kw in lower for kw in keywords):
            hits.append(skill)
    return hits[:4]


_ROLE_CATEGORY_META: tuple[tuple[str, str, str, str, tuple[str, ...]], ...] = (
    ("cognitive", "🧠", "Cognitive & analytical", "Focus, analysis, problem-solving", _COGNITIVE_KW),
    ("people", "👥", "People & communication", "Clients, teams, meetings, persuasion", _PEOPLE_KW),
    ("physical", "🏗️", "Physical & mobility", "Standing, travel, equipment, site work", _PHYSICAL_KW),
    ("pace", "⏱️", "Pace & reliability", "Deadlines, hours, safety, consistency", _PRESSURE_KW),
)


def _clean_skill_items(skills: list[str], limit: int = 4) -> list[str]:
    return [s.strip().rstrip(".") for s in skills[:limit] if s.strip()]


def _flatten_role_requirements(
    title: str,
    categories: list[dict],
    footer: str,
    *,
    fallback: str = "",
) -> str:
    lines = [
        f"Role requirements for {title}:",
        "Broadly, this role typically requires sustained capacity in:",
    ]
    for cat in categories:
        items = "; ".join(cat.get("items") or [])
        if items:
            lines.append(f"{cat['label']} — {items}.")
    if fallback:
        lines.append(fallback)
    lines.append(footer)
    return " ".join(lines)


def build_role_requirements(title: str, description: str, essential: list[str]) -> dict:
    """Structured summary of what performing this role typically demands."""
    categories: list[dict] = []
    for cat_id, icon, label, hint, keywords in _ROLE_CATEGORY_META:
        items = _clean_skill_items(_skill_matches(essential, keywords))
        if items:
            categories.append(
                {
                    "id": cat_id,
                    "icon": icon,
                    "label": label,
                    "hint": hint,
                    "items": items,
                }
            )

    fallback = ""
    if description and not categories:
        snippet = description.strip().rstrip(".")
        if len(snippet) > 220:
            snippet = snippet[:217] + "…"
        fallback = f"Role context: {snippet}."
    elif not categories and essential:
        categories.append(
            {
                "id": "core",
                "icon": "📋",
                "label": "Core task demands",
                "hint": "Typical essential skills from the occupation profile",
                "items": _clean_skill_items(essential, limit=5),
            }
        )

    footer = (
        "Confirm whether this matches your actual role — insurers compare your confirmed "
        "duties against medical certificates and functional limits."
    )
    return {
        "title": title,
        "intro": "Typical insurer-facing demands for this occupation — edit if your role differs.",
        "categories": categories,
        "fallback": fallback,
        "footer": footer,
        "text": _flatten_role_requirements(title, categories, footer, fallback=fallback),
    }


def build_plain_summary(title: str, description: str, essential: list[str], optional: list[str]) -> dict:
    """Plain-language paraphrase: 'this means you do X, Y, and Z'."""
    core = [_skill_to_plain_phrase(s) for s in essential if s.strip()]
    extra = [_skill_to_plain_phrase(s) for s in optional[:4] if s.strip()]

    lead = f"In plain terms, as a {title}, this role generally means:"
    bullets = core[:10]
    paragraph_parts = []
    if core:
        paragraph_parts.append(
            f"In plain terms, working as a {title} means {_join_plain_phrases(core[:7])}."
        )
    elif description:
        paragraph_parts.append(
            f"In plain terms, working as a {title} means: {description.rstrip('.')}."
        )
    if extra:
        paragraph_parts.append(f"You may also {', '.join(e.replace('you ', '', 1) for e in extra[:3])}.")

    return {
        "lead": lead,
        "bullets": bullets,
        "paragraph": " ".join(paragraph_parts).strip(),
        "optional_bullets": extra[:4],
        "role_requirements": build_role_requirements(title, description, essential),
    }


def _skill_titles(links: list[dict] | None, max_items: int = 12) -> list[str]:
    if not links:
        return []
    titles = []
    for link in links:
        title = (link.get("title") or "").strip()
        if title and title not in titles:
            titles.append(title)
        if len(titles) >= max_items:
            break
    return titles


def fetch_occupation_duties(uri: str) -> dict | None:
    """Fetch occupation profile and format material-duty draft text."""
    if not uri or not uri.startswith("http://data.europa.eu/esco/occupation/"):
        return None
    params = urllib.parse.urlencode({"uri": uri, "language": "en"})
    try:
        data = _fetch_json(f"{ESCO_OCCUPATION}?{params}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    title = (
        (data.get("preferredLabel") or {}).get("en")
        or data.get("title")
        or "Occupation"
    ).strip()
    description = _localized_literal(data.get("description"))
    scope = _localized_literal(data.get("scopeNote"))
    links = data.get("_links") or {}
    essential = _skill_titles(links.get("hasEssentialSkill"))
    optional = _skill_titles(links.get("hasOptionalSkill"), max_items=8)
    isco = ""
    for grp in links.get("broaderIscoGroup") or []:
        code = grp.get("code") or ""
        grp_title = grp.get("title") or ""
        if code or grp_title:
            isco = f"{grp_title} (ISCO {code})".strip() if code else grp_title
            break

    lines = [
        f"Role profile: {title}",
        "Source: ESCO (European Skills, Competences, Qualifications and Occupations) — edit to match your actual job.",
    ]
    if isco:
        lines.append(f"Classification: {isco}")
    lines.append("")
    if description:
        lines.append("Role overview:")
        lines.append(description)
        lines.append("")
    if essential:
        lines.append("Typical material duties / essential skills:")
        for skill in essential:
            lines.append(f"• {skill}")
        lines.append("")
    if optional:
        lines.append("May also involve:")
        for skill in optional:
            lines.append(f"• {skill}")
        lines.append("")
    if scope:
        lines.append("Scope note:")
        lines.append(scope)
        lines.append("")
    lines.append(
        "— Add your real-world detail: client pressure, hours, travel, supervision, "
        "cognitive load, safety risk, and how illness affects these duties."
    )

    plain = build_plain_summary(title, description, essential, optional)
    functional_map = build_functional_map(essential, optional, description, title)

    return {
        "title": title,
        "uri": uri,
        "code": data.get("code") or "",
        "isco": isco,
        "duties_text": "\n".join(lines).strip(),
        "essential_count": len(essential),
        "optional_count": len(optional),
        "plain_summary": plain,
        "functional_map": functional_map,
    }