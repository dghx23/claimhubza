"""Map occupation duties / skills to functional capacity domains."""

from __future__ import annotations

FUNCTIONAL_DOMAINS: list[dict] = [
    {
        "id": "physical",
        "label": "Physical & stamina",
        "icon": "💪",
        "hint": "Standing, mobility, manual tasks, travel, endurance, physical presence on site.",
        "illness_link": "Fatigue, pain, medication sedation, reduced stamina.",
        "keywords": (
            "lift", "carry", "stand", "walk", "manual", "physical", "stamina", "endurance",
            "mobility", "climb", "drive", "travel", "site", "operate equipment", "assembly",
            "installation", "construction", "warehouse", "shift",
        ),
    },
    {
        "id": "cognitive",
        "label": "Cognitive & focus",
        "icon": "🧠",
        "hint": "Concentration, analysis, planning, memory, problem-solving, decision quality under pressure.",
        "illness_link": "Brain fog, anxiety, depression, sleep disruption, slowed thinking.",
        "keywords": (
            "analyse", "analyze", "plan", "decide", "calculate", "research", "think", "memory",
            "concentrate", "assess", "evaluate", "interpret", "solve", "strategy", "forecast",
            "economics", "financial analysis", "audit", "review", "investigate",
        ),
    },
    {
        "id": "technical",
        "label": "Technical & specialist",
        "icon": "⚙️",
        "hint": "Tools, systems, software, specialist methods, precision work, technical accuracy.",
        "illness_link": "Cannot sustain technical accuracy, side effects, vision or coordination issues.",
        "keywords": (
            "software", "debug", "program", "engineer", "technical", "system", "equipment",
            "tool", "code", "develop", "design", "install", "maintain", "laboratory",
            "laboratory", "science", "technique", "method", "specialist",
        ),
    },
    {
        "id": "interpersonal",
        "label": "Interpersonal & client-facing",
        "icon": "🤝",
        "hint": "Clients, meetings, presentations, supervision, negotiation, teamwork, conflict.",
        "illness_link": "Social anxiety, emotional overload, cannot face clients or lead teams.",
        "keywords": (
            "client", "liaise", "present", "negotiate", "supervise", "team", "communicate",
            "customer", "stakeholder", "meeting", "consult", "advise", "sales", "service",
            "relationship", "collaborate", "train", "mentor", "lead",
        ),
    },
    {
        "id": "reliability",
        "label": "Reliability, safety & pace",
        "icon": "⏱️",
        "hint": "Deadlines, attendance, error risk, safety-critical work, consistent output, shift patterns.",
        "illness_link": "Unpredictable attendance, missed deadlines, safety risk if impaired.",
        "keywords": (
            "deadline", "safety", "inspect", "monitor", "quality", "compliance", "risk",
            "reliable", "attendance", "shift", "schedule", "urgent", "accuracy", "control",
            "verify", "ensure", "follow procedure",
        ),
    },
    {
        "id": "administrative",
        "label": "Administrative & processing",
        "icon": "📋",
        "hint": "Records, reporting, documentation, payroll, forms, correspondence, routine processing.",
        "illness_link": "Cannot keep up with admin load, errors in routine tasks.",
        "keywords": (
            "record", "report", "document", "organise", "organize", "process", "admin",
            "correspondence", "file", "register", "entry", "paperwork", "schedule",
            "payroll", "invoice", "data entry",
        ),
    },
]


def _classify_item(text: str) -> str | None:
    lower = text.lower()
    best_id = None
    best_score = 0
    for domain in FUNCTIONAL_DOMAINS:
        score = sum(1 for kw in domain["keywords"] if kw in lower)
        if score > best_score:
            best_score = score
            best_id = domain["id"]
    return best_id


def build_functional_map(
    essential: list[str],
    optional: list[str],
    description: str = "",
    title: str = "",
) -> dict:
    """Group identified duties/skills into functional domains for claim evidence."""
    buckets: dict[str, list[str]] = {d["id"]: [] for d in FUNCTIONAL_DOMAINS}
    seen: set[str] = set()

    for raw in essential + optional[:8]:
        item = raw.strip()
        if not item or item.lower() in seen:
            continue
        seen.add(item.lower())
        domain_id = _classify_item(item)
        if not domain_id:
            domain_id = _classify_item(description) or "cognitive"
        buckets[domain_id].append(item)

    if description:
        for domain in FUNCTIONAL_DOMAINS:
            if any(kw in description.lower() for kw in domain["keywords"]):
                tag = f"Role overview suggests {domain['label'].lower()}"
                if tag not in buckets[domain["id"]]:
                    buckets[domain["id"]].append(tag)

    title_lower = (title or "").lower()
    if "consult" in title_lower or "manager" in title_lower:
        for hint in ("Client-facing work likely", "Decision-making under pressure likely"):
            if hint not in buckets["interpersonal"]:
                buckets["interpersonal"].append(hint)
    if "developer" in title_lower or "engineer" in title_lower:
        if "Technical systems work likely" not in buckets["technical"]:
            buckets["technical"].append("Technical systems work likely")

    domains_out = []
    active_count = 0
    for domain in FUNCTIONAL_DOMAINS:
        items = buckets[domain["id"]][:8]
        active = len(items) > 0
        if active:
            active_count += 1
        domains_out.append({
            "id": domain["id"],
            "label": domain["label"],
            "icon": domain["icon"],
            "hint": domain["hint"],
            "illness_link": domain["illness_link"],
            "items": items,
            "active": active,
        })

    return {
        "title": title,
        "intro": (
            "Income protection claims often turn on whether illness affects these functional areas "
            "at work — not just your diagnosis. Map symptoms to the domains that matter in your role."
        ),
        "domains": domains_out,
        "active_count": active_count,
    }