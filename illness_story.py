"""Guided illness / injury story builder for intake."""

from __future__ import annotations

from functional_map import FUNCTIONAL_DOMAINS
from language_map import intake_confusion_guards

STORY_TYPES: list[dict[str, str]] = [
    {
        "id": "gradual",
        "label": "Gradual illness",
        "emoji": "📉",
        "hint": "Worsened over weeks or months — no single accident.",
        "tagline": "Symptoms built up over time",
        "good_if": "Fatigue, pain, or burnout worsened week by week — no single fall or accident",
        "capture": "Symptom onset → how it worsened → when core duties became impossible",
        "insurer_angle": "Insurers compare symptom onset, cover start, and the date duties stopped — these are rarely the same day.",
    },
    {
        "id": "sudden",
        "label": "Sudden injury",
        "emoji": "⚡",
        "hint": "Clear event — fall, accident, acute episode.",
        "tagline": "One event changed everything",
        "good_if": "Fall, accident, assault, or acute episode — you can name when and where",
        "capture": "What happened → immediate symptoms → first certificate → stopped work",
        "insurer_angle": "Event date, hospital/ER records, and employer incident reports matter — causation and exclusions may apply.",
    },
    {
        "id": "mental",
        "label": "Mental health",
        "emoji": "🧠",
        "hint": "Anxiety, depression, burnout, PTSD, etc.",
        "tagline": "Mood, anxiety, or burnout at work",
        "good_if": "Depression, anxiety, panic, burnout, PTSD — often linked to pressure, trauma, or workload",
        "capture": "Trigger or stressor → symptoms → diagnosis/treatment → duties you cannot face",
        "insurer_angle": "Functional impact on client-facing, cognitive, and travel duties matters more than the diagnosis label alone.",
    },
    {
        "id": "mixed",
        "label": "Mixed",
        "emoji": "🔀",
        "hint": "Physical and mental, or injury plus complications.",
        "tagline": "Physical and mental together",
        "good_if": "Injury plus depression in recovery, or migraines plus anxiety — two threads affect the same role",
        "capture": "Separate each thread — physical event/illness and mental symptoms — both linked to duties",
        "insurer_angle": "Tell two clear stories that meet in duty impact — do not let the insurer collapse everything into one label.",
    },
    {
        "id": "unsure",
        "label": "Not sure yet",
        "emoji": "❓",
        "hint": "Start with symptoms — refine later.",
        "tagline": "Start with symptoms — refine later",
        "good_if": "You know how you feel and what stopped you working, but not the right category yet",
        "capture": "List symptoms and dates first — story shape can be updated when medical records arrive",
        "insurer_angle": "A rough honest start is fine — ClaimBuddy helps you sharpen the frame as evidence arrives.",
    },
]

STORY_PHASES: list[dict[str, str]] = [
    {"id": "shape", "label": "1. Story shape", "icon": "🧩"},
    {"id": "onset", "label": "2. Onset & symptoms", "icon": "🤒"},
    {"id": "medical", "label": "3. Medical record", "icon": "🩺"},
    {"id": "bridge", "label": "4. Functional capacity", "icon": "🔗"},
    {"id": "compose", "label": "5. Review", "icon": "✓"},
]

INTAKE_STORY_PHASES: list[dict[str, str]] = [
    {"id": "shape", "label": "1. Story shape", "icon": "🧩"},
    {"id": "onset", "label": "2. Onset & symptoms", "icon": "🤒"},
    {"id": "medical", "label": "3. Medical record", "icon": "🩺"},
    {"id": "compose", "label": "4. Review", "icon": "✓"},
]

STORY_LADDER: list[dict[str, str]] = [
    {"step": "1", "lane": "everyday", "title": "What happened", "question": "Your words — onset, symptoms, story"},
    {"step": "2", "lane": "medical", "title": "Medical record", "question": "Diagnosis, treatment, certificates"},
    {"step": "3", "lane": "functional", "title": "Work impact", "question": "Which duties became impossible?"},
    {"step": "4", "lane": "policy", "title": "Policy test", "question": "Incapacity / disability — insurer decision"},
]

SYMPTOM_DEFINITIONS: dict[str, str] = {
    "Fatigue": "Persistent exhaustion not relieved by rest — limits stamina for full workdays and travel.",
    "Chronic pain": "Ongoing pain beyond normal healing time — may be localised or widespread.",
    "Headaches": "Recurrent head pain — migraine or tension types affect screen work and concentration.",
    "Nausea": "Feeling sick or vomiting — can limit travel, client meals, and medication tolerance.",
    "Dizziness": "Light-headedness or vertigo — safety risk for driving, sites, and machinery.",
    "Weakness": "Reduced physical strength — lifting, standing, and endurance duties suffer.",
    "Reduced stamina": "Runs out of energy before a normal workday ends — pacing and breaks needed.",
    "Fever": "Elevated body temperature — may signal infection and limit attendance or travel.",
    "Brain fog": "Clouded thinking — hard to track detail, emails, and multi-step tasks.",
    "Poor concentration": "Cannot sustain focus on reading, analysis, or meetings.",
    "Memory problems": "Forgetting instructions, appointments, or recent conversations at work.",
    "Slowed thinking": "Takes longer to process information — deadlines and client responses slip.",
    "Decision fatigue": "Overwhelmed by choices — paralysis on important work decisions.",
    "Anxiety": "Persistent worry or dread — often worse before presentations, travel, or scrutiny.",
    "Panic attacks": "Sudden intense fear with physical symptoms — may prevent leaving home or attending work.",
    "Low mood": "Depressed mood, hopelessness, or loss of interest — motivation for duties drops.",
    "Burnout": "Exhaustion and cynicism from sustained work stress — common in high-pressure roles.",
    "Emotional overwhelm": "Feelings too intense to manage in professional settings.",
    "Irritability": "Short temper and low frustration tolerance — affects teamwork and client relations.",
    "Insomnia": "Difficulty falling or staying asleep — next-day cognitive and safety impact.",
    "Broken sleep": "Waking repeatedly — non-restorative sleep even if total hours seem adequate.",
    "Hypersomnia": "Excessive sleepiness or sleeping too much — still unrefreshed for work.",
    "Night sweats": "Sleep disruption from sweating — may signal infection, hormones, or medication.",
    "Early waking": "Waking hours before alarm and unable to return to sleep — cuts restorative sleep.",
    "Cannot face meetings": "Avoidance of meetings due to anxiety, fatigue, or cognitive overload.",
    "Missed deadlines": "Work output falls behind schedule — objective sign of reduced capacity.",
    "Reduced hours attempted": "Tried part-time or shortened days but still cannot sustain role.",
    "Stopped completely": "Unable to perform any material duties — full work cessation.",
}


def _symptom_chips(labels: list[str]) -> list[dict[str, str]]:
    return [
        {"label": label, "description": SYMPTOM_DEFINITIONS.get(label, label)}
        for label in labels
    ]


SYMPTOM_GROUPS: list[dict] = [
    {
        "id": "physical",
        "label": "Physical & pain",
        "chips": _symptom_chips(["Fatigue", "Chronic pain", "Headaches", "Nausea", "Dizziness", "Weakness", "Reduced stamina"]),
    },
    {
        "id": "cognitive",
        "label": "Cognitive",
        "chips": _symptom_chips(["Brain fog", "Poor concentration", "Memory problems", "Slowed thinking", "Decision fatigue"]),
    },
    {
        "id": "emotional",
        "label": "Emotional & mental",
        "chips": _symptom_chips(["Anxiety", "Panic attacks", "Low mood", "Burnout", "Emotional overwhelm", "Irritability"]),
    },
    {
        "id": "sleep",
        "label": "Sleep & arousal",
        "chips": _symptom_chips(["Insomnia", "Broken sleep", "Hypersomnia", "Night sweats", "Early waking"]),
    },
    {
        "id": "work",
        "label": "Work-facing signs",
        "chips": _symptom_chips(["Cannot face meetings", "Missed deadlines", "Reduced hours attempted", "Stopped completely"]),
    },
]

CONFUSION_GUARDS: list[dict] = intake_confusion_guards()

DATE_LADDER: list[dict[str, str]] = [
    {
        "id": "symptom_onset",
        "label": "Symptom onset",
        "hint": "When you first noticed symptoms — often weeks or months before you stopped work. Insurers use this to test whether illness predates cover or waiting periods.",
    },
    {
        "id": "date_of_absence",
        "label": "Stopped performing duties",
        "hint": "When you could no longer perform core material duties — your Date of Absence (DOA). This is the main policy test date and may differ from your first sick note.",
    },
    {
        "id": "first_medical_cert",
        "label": "First medical certificate",
        "hint": "Date on your first GP or specialist sick note. Employers and insurers sometimes treat this as the ‘official’ start even if symptoms began earlier.",
    },
    {"id": "first_notice", "label": "First notice", "hint": "When employer or insurer was first formally notified."},
]

TIMELINE_CAPTURE_FIELDS: list[dict[str, str]] = [
    {
        "id": "symptom_onset",
        "label": "Symptom onset",
        "sync_field": "symptom_onset",
        "hint": DATE_LADDER[0]["hint"],
        "default_precision": "month",
    },
    {
        "id": "date_of_absence",
        "label": "Stopped performing duties",
        "sync_field": "date_of_absence",
        "hint": DATE_LADDER[1]["hint"],
        "default_precision": "exact",
    },
    {
        "id": "first_medical_cert",
        "label": "First medical certificate",
        "sync_field": "first_medical_cert",
        "hint": DATE_LADDER[2]["hint"],
        "default_precision": "exact",
    },
]

PHASE_COACHING: dict[str, str] = {
    "shape": "Pick the narrative frame first — gradual illness, sudden injury, and mental health claims need different timelines and evidence.",
    "onset": "Describe symptoms in your own words before medical labels. Name when things started and how they changed week to week.",
    "medical": "Layer in what clinicians wrote — diagnosis, treatment, certificates. Keep this separate from everyday symptom language.",
    "bridge": "Functional-capacity builder — map each symptom to a material duty using your occupation functional map. This is the insurer test.",
    "compose": "Read aloud — does a stranger see onset → medical record → duty impact? Fill gaps until story strength is high.",
    "functional": "Open the functional-capacity module to map symptoms to material duties — synced with this health story.",
}

STORY_EXAMPLES: dict[str, list[str]] = {
    "gradual": [
        "Fatigue built over 8 weeks after a merger — initially manageable, then could not complete full client days.",
        "Chronic back pain worsened with travel — GP diagnosis after MRI; stopped site supervision in September.",
    ],
    "sudden": [
        "Fell on stairs at client site — immediate lumbar injury; ER same day; off work from first certificate.",
        "Acute panic during board presentation — admitted overnight; psychiatrist diagnosis within 10 days.",
    ],
    "mental": [
        "Burnout after sustained 70-hour weeks — insomnia, dread before meetings; psychologist diagnosis; cannot lead client workshops.",
        "PTSD after workplace assault — flashbacks block open-plan office; psychiatrist off-work certificate from June.",
    ],
    "mixed": [
        "Hand injury from fall plus depression during recovery — cannot type at pace required for audit deadlines.",
        "Migraines plus anxiety — physical pain triggers cognitive fog; both block technical review duties.",
    ],
    "unsure": [
        "Multiple symptoms over months — start with fatigue and poor sleep, refine diagnosis as records arrive.",
    ],
}

PROMPT_CARDS: list[dict] = [
    {
        "id": "onset",
        "phase": "onset",
        "lane": "everyday",
        "title": "When it started",
        "template": "Symptoms began around {when} — initially {severity} and then {progression}.",
        "placeholder": "e.g. March 2024 after intense project period",
        "fields": [
            {"key": "when", "label": "When (approx.)", "placeholder": "e.g. March 2024"},
            {"key": "severity", "label": "Initial severity", "placeholder": "e.g. mild"},
            {"key": "progression", "label": "How it progressed", "placeholder": "e.g. worsened over 6 weeks"},
        ],
    },
    {
        "id": "trigger",
        "phase": "onset",
        "lane": "everyday",
        "title": "Trigger / context",
        "template": "Context: {context}. Trigger or stressor: {trigger}.",
        "placeholder": "e.g. post-merger workload, injury at site",
        "fields": [
            {"key": "context", "label": "Situation at work/home", "placeholder": "e.g. 70-hour weeks, client loss"},
            {"key": "trigger", "label": "Trigger event (if any)", "placeholder": "e.g. fall on stairs / none — gradual"},
        ],
    },
    {
        "id": "symptoms",
        "phase": "onset",
        "lane": "everyday",
        "title": "Symptom picture",
        "template": "Main symptoms: {symptoms}. Day-to-day effect: {daily}.",
        "placeholder": "e.g. fatigue, panic before client calls",
        "fields": [
            {"key": "symptoms", "label": "Symptoms (list)", "placeholder": "e.g. crushing fatigue, insomnia"},
            {"key": "daily", "label": "Daily life impact", "placeholder": "e.g. cannot get through a work day"},
        ],
    },
    {
        "id": "diagnosis",
        "phase": "medical",
        "lane": "medical",
        "title": "Diagnosis",
        "template": "Treating doctor ({clinician}): diagnosis / working diagnosis — {diagnosis} ({date}).",
        "placeholder": "e.g. MDD, lumbar disc prolapse",
        "fields": [
            {"key": "clinician", "label": "Clinician", "placeholder": "e.g. Dr Naidoo (GP)"},
            {"key": "diagnosis", "label": "Diagnosis", "placeholder": "e.g. major depressive disorder"},
            {"key": "date", "label": "Date of diagnosis (if known)", "placeholder": "e.g. Jun 2024"},
        ],
    },
    {
        "id": "treatment",
        "phase": "medical",
        "lane": "medical",
        "title": "Treatment & referrals",
        "template": "Treatment: {treatment}. Referrals / tests: {referrals}.",
        "placeholder": "e.g. SSRI, psychotherapy, MRI lumbar spine",
        "fields": [
            {"key": "treatment", "label": "Medication / therapy", "placeholder": "e.g. Cipralex 20mg, weekly therapy"},
            {"key": "referrals", "label": "Referrals / investigations", "placeholder": "e.g. psychiatrist, occupational therapist"},
        ],
    },
    {
        "id": "certificates",
        "phase": "medical",
        "lane": "medical",
        "title": "Certificates & admissions",
        "template": "Medical certificates: {certs}. Hospital / ER: {hospital}.",
        "placeholder": "e.g. off work from 12 Jun; admitted 3 nights Aug",
        "fields": [
            {"key": "certs", "label": "Sick notes / certificates", "placeholder": "e.g. continuous from 12 Jun 2024"},
            {"key": "hospital", "label": "Hospital / ER (if any)", "placeholder": "e.g. none / 3 nights Aug 2024"},
        ],
    },
    {
        "id": "work_impact",
        "phase": "bridge",
        "lane": "functional",
        "title": "Duty impact",
        "template": "Work impact: cannot perform {duty} because {symptom} — {domain} capacity affected.",
        "placeholder": "e.g. cannot run client workshops due to anxiety",
        "fields": [
            {"key": "duty", "label": "Material duty blocked", "placeholder": "e.g. client workshops, site visits"},
            {"key": "symptom", "label": "Symptom / limitation", "placeholder": "e.g. panic, fatigue"},
            {"key": "domain", "label": "Functional area", "placeholder": "e.g. interpersonal, cognitive"},
        ],
    },
    {
        "id": "attempted_return",
        "phase": "bridge",
        "lane": "functional",
        "title": "Attempted return / reduced duties",
        "template": "Attempted return / reduced duties: {attempt} — outcome: {outcome}.",
        "placeholder": "e.g. tried 2 days/week — failed after week 2",
        "fields": [
            {"key": "attempt", "label": "What was tried", "placeholder": "e.g. half days, admin only"},
            {"key": "outcome", "label": "Outcome", "placeholder": "e.g. symptoms flared, stopped again"},
        ],
    },
    {
        "id": "pattern",
        "phase": "bridge",
        "lane": "functional",
        "title": "Pattern & prognosis",
        "template": "Pattern: {pattern}. Doctor prognosis / expected course: {prognosis}.",
        "placeholder": "e.g. worse Mon–Thu; doctor says uncertain return date",
        "fields": [
            {"key": "pattern", "label": "Symptom pattern", "placeholder": "e.g. unpredictable flare-ups"},
            {"key": "prognosis", "label": "Prognosis (if stated)", "placeholder": "e.g. off work at least 3 months"},
        ],
    },
    {
        "id": "flare",
        "phase": "onset",
        "lane": "everyday",
        "title": "Flare-ups & variability",
        "template": "Symptoms are {pattern} — worst on {worst_days}; better on {better_days}.",
        "placeholder": "e.g. unpredictable; Mon–Wed; weekends only",
        "fields": [
            {"key": "pattern", "label": "Overall pattern", "placeholder": "e.g. unpredictable / cyclical"},
            {"key": "worst_days", "label": "Worst days / triggers", "placeholder": "e.g. Mon–Thu after poor sleep"},
            {"key": "better_days", "label": "When slightly better", "placeholder": "e.g. weekends, after rest"},
        ],
    },
    {
        "id": "workplace",
        "phase": "bridge",
        "lane": "functional",
        "title": "Workplace stressor",
        "template": "Work context: {stressor} — this intensified {symptom} and made {duty} impossible.",
        "placeholder": "e.g. restructure; anxiety; client presentations",
        "fields": [
            {"key": "stressor", "label": "Work stressor / change", "placeholder": "e.g. new manager, client loss"},
            {"key": "symptom", "label": "Symptom intensified", "placeholder": "e.g. panic, fatigue"},
            {"key": "duty", "label": "Duty that became impossible", "placeholder": "e.g. leading team meetings"},
        ],
    },
    {
        "id": "medication_fx",
        "phase": "medical",
        "lane": "medical",
        "title": "Medication side effects",
        "template": "Medication ({med}) caused {side_effect}, which further limited {limitation}.",
        "placeholder": "e.g. sedating antidepressant; daytime drowsiness; driving to sites",
        "fields": [
            {"key": "med", "label": "Medication", "placeholder": "e.g. Amitriptyline 25mg"},
            {"key": "side_effect", "label": "Side effect", "placeholder": "e.g. sedation, nausea"},
            {"key": "limitation", "label": "Extra work limitation", "placeholder": "e.g. cannot drive, concentrate"},
        ],
    },
    {
        "id": "timeline",
        "phase": "onset",
        "lane": "everyday",
        "title": "Timeline snapshot",
        "template": "Timeline: symptoms from {symptom_onset}; stopped performing duties {stopped}; first medical certificate {first_cert}.",
        "placeholder": "e.g. Mar 2024; 12 Jun 2024; 14 Jun 2024",
        "fields": [
            {"key": "symptom_onset", "label": "Symptom onset (approx.)", "placeholder": "e.g. March 2024"},
            {"key": "stopped", "label": "Stopped performing duties", "placeholder": "e.g. 12 June 2024"},
            {"key": "first_cert", "label": "First medical certificate", "placeholder": "e.g. 14 June 2024"},
        ],
    },
]

QUALITY_CHECKS: list[dict[str, str]] = [
    {"id": "onset", "label": "Onset / when", "pattern": r"(began|started|onset|since|from|around|\d{4}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"},
    {"id": "symptoms", "label": "Symptoms named", "pattern": r"(symptom|pain|fatigue|anxiety|depress|insomnia|panic|cannot|unable|brain fog)"},
    {"id": "work", "label": "Duty impact", "pattern": r"(work|duty|job|client|office|shift|perform|attend|meeting|travel|supervis|cannot perform)"},
    {"id": "medical", "label": "Medical source", "pattern": r"(doctor|dr\.|gp|psychiat|psycholog|diagnos|treat|medication|hospital|specialist|certificate)"},
    {"id": "bridge", "label": "Symptom → duty link", "pattern": r"(because|due to|prevents|stops|blocks|affects|linked to)"},
    {"id": "timeline", "label": "Timeline clue", "pattern": r"(week|month|day|year|\d{4}|first|then|after|before|continuous)"},
    {"id": "severity", "label": "Severity / course", "pattern": r"(worsen|improv|stable|flare|chronic|acute|severe|mild|deteriorat)"},
    {"id": "prognosis", "label": "Return / prognosis", "pattern": r"(return|prognos|recover|off work|absent|unable to work|fit for)"},
]

ILLNESS_DOMAINS: list[dict] = [
    {
        "id": d["id"],
        "label": d["label"],
        "icon": d["icon"],
        "illness_link": d["illness_link"],
        "keywords": list(d.get("keywords") or ()),
    }
    for d in FUNCTIONAL_DOMAINS
]