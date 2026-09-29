"""Plain-language map: sickness, illness, injury, functional, disability, etc."""

from __future__ import annotations

import re

from term_slugs import slugify

LANES: list[dict[str, str]] = [
    {
        "id": "everyday",
        "label": "What people say",
        "tagline": "Everyday words — loose, emotional, not policy tests",
        "color": "#01579b",
        "bg": "#e1f5fe",
    },
    {
        "id": "medical",
        "label": "What doctors write",
        "tagline": "Clinical record language — facts about health, not your job",
        "color": "#7b1fa2",
        "bg": "#f3e5f5",
    },
    {
        "id": "functional",
        "label": "What work needs",
        "tagline": "The bridge insurers actually care about — can you do the job?",
        "color": "#bf360c",
        "bg": "#fff3e0",
    },
    {
        "id": "policy",
        "label": "What policies test",
        "tagline": "Binding claim language — definitions in your policy wording",
        "color": "#1e56d4",
        "bg": "#e8f1ff",
    },
]

TERMS: list[dict] = [
    {
        "term": "Sickness",
        "lane": "everyday",
        "emoji": "🤒",
        "one_liner": "Feeling unwell or off work for health reasons — often short and vague.",
        "is": ["A casual way to say you cannot work today", "May appear on sick notes or HR forms"],
        "is_not": ["A policy disability test", "Proof that benefits are payable"],
        "policy_note": "Policies rarely define 'sickness' on its own. Look for incapacity, disability, or inability to perform duties.",
        "evidence": "Sick note, HR absence record",
        "confused_with": ["Illness", "Incapacity"],
        "example": '"I have been off sick for two weeks."',
        "how_you_know": [
            "You feel too unwell to attend work — today, this week, or for a short stretch.",
            "HR accepts a sick note without asking whether core duties are impossible.",
            "You or others describe it in everyday language: 'off sick', 'not feeling well'.",
        ],
        "triggers": [
            "Calling in sick to your manager or HR.",
            "A GP issues a brief medical certificate ('sick leave').",
            "Usually no insurer waiting-period or disability test — unless absence becomes prolonged.",
        ],
        "check_questions": [
            "Am I describing a few days off, or weeks/months unable to do my real job?",
            "Has anyone linked my sickness to material duties — or only to attendance?",
            "If I returned to light duties, would HR still call it 'sick leave'?",
        ],
        "term_links": [
            {"term": "Illness", "relation": "May become", "note": "Short sickness can develop into a longer illness with ongoing health impact."},
            {"term": "Incapacity", "relation": "Not the same as", "note": "HR may accept sickness while the insurer disputes policy incapacity."},
            {"term": "Waiting period", "relation": "Does not start", "note": "Brief sickness alone does not satisfy a group IP waiting period."},
            {"term": "Date of Absence", "relation": "Earlier than", "note": "First sick day is often not your policy DOA — that comes when duties stop."},
        ],
    },
    {
        "term": "Illness",
        "slug": "illness",
        "lane": "everyday",
        "emoji": "🩺",
        "one_liner": "A health problem — usually disease or disorder, mental or physical, often ongoing.",
        "is": ["Broader than a single sick day", "Covers depression, cancer, chronic pain, autoimmune disease, etc."],
        "is_not": ["Automatically the same as 'injury'", "The same as policy 'disability'"],
        "policy_note": "People say 'illness'; policies say 'incapacity' or 'disability'. The policy tests work impact, not the word illness.",
        "evidence": "Diagnosis, treatment records, specialist letters",
        "confused_with": ["Condition", "Diagnosis", "Disability"],
        "example": '"My illness started after a stressful project period."',
        "how_you_know": [
            "Symptoms persist beyond a short sick spell — weeks, months, or episodic relapse.",
            "A doctor names or treats a condition (even before formal diagnosis).",
            "Health affects daily life, not only one missed shift.",
        ],
        "triggers": [
            "Referral to specialist, starting long-term medication, or ongoing therapy.",
            "Gradual worsening at work — concentration, stamina, attendance, reliability.",
            "Illness alone does not trigger IP benefits — duty incapacity does.",
        ],
        "check_questions": [
            "When did I first notice symptoms — and when did core job tasks become impossible?",
            "Am I describing the health problem, or whether I can still do my occupation?",
            "Could I still do my job on good days even while 'ill'?",
        ],
        "term_links": [
            {"term": "Sickness", "relation": "Broader than", "note": "Illness is ongoing health; sickness is often short and casual."},
            {"term": "Diagnosis", "relation": "Documented as", "note": "Doctors give diagnoses; you may feel ill before or without a label."},
            {"term": "Incapacity", "relation": "Precedes", "note": "You can be ill before policy incapacity begins — capture both dates."},
            {"term": "Symptom", "relation": "Felt as", "note": "Symptoms are what you experience; illness is how you describe the problem."},
            {"term": "Functional capacity", "relation": "Proved via", "note": "Insurers need illness linked to duties — not illness alone."},
        ],
        "date_ladder": [
            {"label": "Symptom onset", "note": "When you first noticed the health problem"},
            {"label": "Stopped performing duties", "note": "When illness stopped you doing core work — often your DOA"},
            {"label": "First diagnosis", "note": "Medical label may come weeks or months later"},
        ],
    },
    {
        "term": "Injury",
        "lane": "everyday",
        "emoji": "🩹",
        "one_liner": "Harm from a specific event — accident, fall, surgery, assault, sport trauma.",
        "is": ["Usually has a when/where/how story", "Often documented in hospital or casualty records"],
        "is_not": ["Every medical problem (many illnesses have no single injury event)", "Automatically excluded or covered — check policy"],
        "policy_note": "Some policies split accident vs illness benefits or apply conduct exclusions to self-inflicted injury. Read exact wording.",
        "evidence": "Hospital report, ICD external-cause codes, employer incident report",
        "confused_with": ["Illness", "Condition"],
        "example": '"Back injury after lifting equipment on site."',
    },
    {
        "term": "Condition",
        "lane": "everyday",
        "emoji": "📋",
        "one_liner": "Neutral umbrella for any diagnosed or reported health issue.",
        "is": ["Useful when you are unsure of illness vs injury", "Common on forms and medical certificates"],
        "is_not": ["A substitute for explaining work impact", "A policy-defined claim ground by itself"],
        "policy_note": "Insurers may latch onto a condition label (e.g. 'anxiety') without assessing duty impact — that is the diagnosis trap.",
        "evidence": "Medical certificate, specialist report",
        "confused_with": ["Diagnosis", "Pre-existing condition"],
        "example": "A form may say 'pre-existing condition' — that does not automatically defeat post-cover deterioration.",
    },
    {
        "term": "Diagnosis",
        "lane": "medical",
        "emoji": "🏷️",
        "one_liner": "The medical label a doctor assigns — a name for what they think you have.",
        "is": ["ICD-10/11 code, specialist opinion, hospital discharge summary", "Starting point for medical chronology"],
        "is_not": ["Proof you cannot work", "The insurer's final decision"],
        "policy_note": "Strongest trap in IP claims: rejection because 'diagnosis not severe enough' when the real test is occupational function.",
        "evidence": "Consultation notes, specialist report, hospital summary",
        "confused_with": ["Disability", "Incapacity", "Symptom"],
        "example": '"Major depressive disorder" on a script is a diagnosis, not a disability finding.',
        "how_you_know": [
            "A clinician writes a named condition on a certificate, script, or specialist letter.",
            "Hospital discharge summary or ICD code appears in records.",
            "It describes what you have — not whether you can work.",
        ],
        "triggers": [
            "Specialist consultation, hospital admission, or formal assessment.",
            "Insurer medical review may accept diagnosis but still dispute disability.",
            "Pre-existing condition arguments often turn on diagnosis dates vs cover start.",
        ],
        "check_questions": [
            "Does my certificate only list a diagnosis, or does it link to work duties?",
            "Is the insurer rejecting the diagnosis — or rejecting duty impact?",
            "When was this diagnosis first recorded vs when did duties stop?",
        ],
        "term_links": [
            {"term": "Symptom", "relation": "Labels", "note": "Diagnosis names the condition; symptoms are what you feel day to day."},
            {"term": "Disability", "relation": "Not the same as", "note": "Serious diagnosis ≠ automatic disability under policy wording."},
            {"term": "Functional limitation", "relation": "Must pair with", "note": "Pair every diagnosis with at least one duty it prevents."},
            {"term": "Illness", "relation": "Documents", "note": "Illness is everyday language; diagnosis is the medical record label."},
            {"term": "Incapacity", "relation": "Does not prove", "note": "Diagnosis on a sick note does not equal policy incapacity."},
        ],
    },
    {
        "term": "Symptom",
        "lane": "medical",
        "emoji": "💫",
        "one_liner": "What you experience — pain, fatigue, brain fog, panic, nausea, weakness.",
        "is": ["Subjective but real", "Often what makes duties impossible day to day"],
        "is_not": ["Always visible on tests", "Less important than diagnosis — symptoms drive function"],
        "policy_note": "Mental illness and pain clauses sometimes demand 'objective' evidence. Functional mapping still links symptoms to duties.",
        "evidence": "Your symptom log, doctor notes, medication side-effect record",
        "confused_with": ["Diagnosis", "Functional limitation"],
        "example": '"Cannot concentrate for more than 20 minutes" is a symptom with direct work impact.',
    },
    {
        "term": "Impairment",
        "lane": "medical",
        "emoji": "📉",
        "one_liner": "Medical loss or reduction of body or mind function — clinical, not occupational.",
        "is": ["Used in reports, RFC forms, disability assessments", "Can exist without total work absence"],
        "is_not": ["The same as policy disability", "Only about job title"],
        "policy_note": "Impairment % from a medical board does not automatically equal IP benefit entitlement under own-occupation wording.",
        "evidence": "Functional assessment, specialist impairment rating",
        "confused_with": ["Functional limitation", "Disability"],
        "example": "30% whole-person impairment may still prevent your specific consulting role.",
    },
    {
        "term": "Prognosis",
        "lane": "medical",
        "emoji": "🔭",
        "one_liner": "Doctor's view of likely future course — recovery, stability, or deterioration.",
        "is": ["Supports waiting-period and benefit-duration arguments", "Needed when insurer expects return to work"],
        "is_not": ["A guarantee of outcome", "Optional fluff — it shapes benefit period disputes"],
        "policy_note": "Temporary vs permanent disability clauses hinge on prognosis language — capture exact doctor wording.",
        "evidence": "Specialist letter, treating practitioner opinion",
        "confused_with": ["Diagnosis", "Functional capacity"],
        "example": '"Guarded prognosis with episodic relapse" affects return-to-work expectations.',
    },
    {
        "term": "Functional capacity",
        "lane": "functional",
        "emoji": "⚙️",
        "one_liner": "What you can and cannot do in real life — especially material work duties.",
        "is": ["Attendance, stamina, cognition, safety, reliability, travel tolerance", "The evidence insurers often say is 'missing'"],
        "is_not": ["A diagnosis", "Your job title", "A generic sick note alone"],
        "policy_note": "Own-occupation IP claims live or die here. This is the bridge from medical notes to policy test.",
        "evidence": "Duty-impact statement, OT report, detailed doctor questionnaire",
        "confused_with": ["Diagnosis", "Disability", "Activities of daily living"],
        "example": '"Cannot manage client deadlines, supervision, or site travel" = functional, not just medical.',
        "how_you_know": [
            "You can list specific duties you cannot perform — with frequency and severity.",
            "Symptoms map to tasks: fatigue → full workday; panic → client meetings.",
            "Employer or colleague observations match your functional limits.",
        ],
        "triggers": [
            "Insurer requests occupational questionnaire or IME focused on duties.",
            "Own-occupation test requires proof you cannot do your actual role.",
            "Building the duty-impact matrix in ClaimBuddy links symptoms to material duties.",
        ],
        "check_questions": [
            "Can I name five material duties and say which I cannot do — and why?",
            "Would a stranger understand my role from duties, not just my job title?",
            "Is my evidence about home tasks (ADL) or about work tasks?",
        ],
        "term_links": [
            {"term": "Material duties", "relation": "Measured against", "note": "Functional capacity is always tied to what your job actually requires."},
            {"term": "Functional limitation", "relation": "Built from", "note": "Each limitation links one symptom to one blocked duty."},
            {"term": "Diagnosis", "relation": "Bridges from", "note": "Medical facts mean little until translated into duty impact."},
            {"term": "Incapacity", "relation": "Proves", "note": "Functional evidence shows why you are incapacitated for policy purposes."},
            {"term": "Disability", "relation": "Proves", "note": "Under own-occupation wording, disability is shown through functional failure."},
            {"term": "Activities of daily living (ADL)", "relation": "Not the same as", "note": "ADL tests home tasks; IP usually needs work-function proof."},
        ],
    },
    {
        "term": "Material duties",
        "lane": "functional",
        "emoji": "🎯",
        "one_liner": "Core tasks that actually matter in your role — not incidental admin.",
        "is": ["Client delivery, decision-making, safety oversight, billable hours, error risk", "Defined from contract, JD, and reality"],
        "is_not": ["Job title alone", "Every minor task in a long HR description"],
        "policy_note": "Job-title trap: 'manager' understates cognitive load, client pressure, or travel demands.",
        "evidence": "Job description, performance reviews, your own duty list, employer statement",
        "confused_with": ["Occupation", "Own occupation"],
        "example": "Job title 'Partner' on a letterhead is not sedentary admin if the role needs client-facing pressure.",
    },
    {
        "term": "Functional limitation",
        "lane": "functional",
        "emoji": "🚧",
        "one_liner": "A specific barrier — X symptom stops Y duty, with severity and frequency.",
        "is": ["Structured links: fatigue → cannot finish workday; anxiety → cannot present to clients", "Feeds doctor questionnaire and claim pack"],
        "is_not": ["Vague 'I feel terrible'", "A diagnosis restated without duty link"],
        "policy_note": "Build a limitation matrix: limitation → duty affected → medical source → still missing evidence.",
        "evidence": "Symptom log mapped to duties, OT/psych report, employer observation",
        "confused_with": ["Symptom", "Impairment"],
        "example": '"Medication morning sedation prevents 08:00 client meetings three days per week."',
    },
    {
        "term": "Activities of daily living (ADL)",
        "lane": "functional",
        "emoji": "🏠",
        "one_liner": "Basic self-care and home tasks — dressing, bathing, cooking, mobility.",
        "is": ["Common in severe disability and lump-sum policy tests", "Sometimes used in medical assessments"],
        "is_not": ["The main test for own-occupation income protection", "A substitute for work-duty evidence"],
        "policy_note": "ADL-focused evidence may not answer whether you can perform your occupation — know which test applies.",
        "evidence": "OT ADL assessment, hospital rehab notes",
        "confused_with": ["Functional capacity", "Material duties"],
        "example": "Can shower independently but still cannot sustain a full consulting day — different tests.",
    },
    {
        "term": "Disability",
        "lane": "policy",
        "emoji": "📜",
        "one_liner": "Policy-defined inability to meet the insured disability test — not a medical opinion.",
        "is": ["Defined in policy wording — own occupation, any occupation, partial, etc.", "What the insurer must decide"],
        "is_not": ["Whatever a doctor wrote on a certificate", "A universal medical status"],
        "policy_note": "Always ask: which test applies now — Initial Period own occupation vs Extended Period any occupation?",
        "evidence": "Policy clause, functional-duty proof, insurer assessment file",
        "confused_with": ["Diagnosis", "Impairment", "Incapacity"],
        "example": "Policy may require inability to perform material duties of own occupation for 6+ months.",
        "how_you_know": [
            "You meet the specific test in your policy — own occupation, suited occupation, or any occupation.",
            "Functional evidence shows material duties are impossible for the required duration.",
            "The insurer accepts (or you dispute) their assessment that the policy definition is met.",
        ],
        "triggers": [
            "Incapacity continuing through the waiting period without recovery gaps.",
            "Claim submitted with medical + duty-impact evidence after waiting period.",
            "Initial Period own-occupation test — may shift to any/suitable occupation later.",
            "Partial/residual clause if you still earn but below pre-disability level.",
        ],
        "check_questions": [
            "Which disability test applies today — own occupation or any occupation?",
            "Has the Initial Period ended, changing the test?",
            "Am I totally unable to work, or partially disabled with reduced earnings?",
            "Is the insurer arguing diagnosis severity instead of duty impact?",
        ],
        "term_links": [
            {"term": "Incapacity", "relation": "Builds on", "note": "Incapacity is the ongoing state; disability is the policy outcome if tests are met."},
            {"term": "Diagnosis", "relation": "Not decided by", "note": "A certificate diagnosis does not automatically trigger disability."},
            {"term": "Own occupation", "relation": "Tested via", "note": "Initial Period usually applies the own-occupation disability test."},
            {"term": "Functional capacity", "relation": "Proved by", "note": "Duty-impact evidence is how you demonstrate disability under own-occupation policies."},
            {"term": "Total vs partial disability", "relation": "May be", "note": "Residual clauses pay proportionate benefits if some work continues."},
            {"term": "Waiting period", "relation": "After", "note": "Benefits usually start only once waiting period and disability test align."},
            {"term": "Impairment", "relation": "Not the same as", "note": "Medical impairment ratings use a different scale than policy disability."},
        ],
        "library_note": (
            "The same word is used in everyday talk, medical models, employment-equity statutes, COIDA, and IP policies. "
            "Income protection usually tests treated performance of material duties — not a dictionary or ADA-style label."
        ),
    },
    {
        "term": "Cover start",
        "slug": "cover-start",
        "lane": "policy",
        "emoji": "📅",
        "one_liner": "When your group income protection membership or benefit cover began.",
        "is": [
            "Date on policy schedule, member certificate, or HR benefits confirmation",
            "Used for pre-existing condition and eligibility arguments",
            "May differ from employment start date",
        ],
        "is_not": [
            "The same as symptom onset or Date of Absence",
            "Automatically the day you joined the employer",
            "Proof that a claim must be accepted",
        ],
        "policy_note": "Commencement of cover clauses often require you to be actively at work. Insurers use this date for look-back and pre-existing exclusions.",
        "evidence": "Policy schedule, member certificate, HR benefits pack, employer confirmation",
        "confused_with": ["Employment start", "Symptom onset", "Waiting period"],
        "example": "Cover from 1 Mar 2022 on schedule — insurer may argue symptoms before that date are pre-existing.",
    },
    {
        "term": "Waiting period",
        "slug": "waiting-period",
        "lane": "policy",
        "emoji": "⏳",
        "one_liner": "Deferred or elimination period — continuous absence/incapacity before benefits start.",
        "is": [
            "A fixed period defined in policy wording (days or months)",
            "Measured from Date of Absence or first day of incapacity — check your clause",
            "Requires continuity evidence across the whole period",
        ],
        "is_not": [
            "The same as symptom onset or your first sick note",
            "Optional — most group IP policies have one",
            "Automatically over because HR accepted absence",
        ],
        "policy_note": "Also called deferred period or elimination period. Benefits usually start only after you satisfy this period without recovery gaps that reset the clock.",
        "evidence": "Policy schedule, absence register, medical certificates covering full period, employer statement",
        "confused_with": ["Symptom onset", "Date of Absence", "Sickness", "Incapacity"],
        "example": "3-month waiting period from DOA — insurer may dispute if you returned to light duties for one week mid-period.",
        "how_you_know": [
            "Your policy schedule states a deferred/elimination period (e.g. 3 months).",
            "Benefits are not payable until that period of continuous incapacity ends.",
            "Insurer correspondence references 'waiting period not yet satisfied'.",
        ],
        "triggers": [
            "DOA or first incapacity day starts the clock — per your clause wording.",
            "Any return to material duties may reset the period to zero.",
            "End of waiting period + ongoing disability test = benefit commencement.",
        ],
        "check_questions": [
            "Is my waiting period measured from DOA or from first consultation?",
            "Did I work light duties at any point — even one day?",
            "Do certificates cover the full period without gaps?",
        ],
        "term_links": [
            {"term": "Date of Absence", "relation": "Measured from", "note": "Clock usually starts at DOA or first incapacity day."},
            {"term": "Incapacity", "relation": "Requires", "note": "Continuous incapacity across the whole period."},
            {"term": "Sickness", "relation": "Not the same as", "note": "Short sickness spells do not satisfy a 3-month waiting period."},
            {"term": "Disability", "relation": "Before", "note": "You must still meet disability test when waiting period ends."},
        ],
        "date_ladder": [
            {"label": "DOA / incapacity start", "note": "Day one of the waiting period"},
            {"label": "Mid-period checks", "note": "Any work or light duties may reset the clock"},
            {"label": "Waiting period end", "note": "Benefits may start if disability test still met"},
        ],
    },
    {
        "term": "Incapacity",
        "slug": "incapacity",
        "lane": "policy",
        "emoji": "⛔",
        "one_liner": "Unable to work (or meet earnings) as defined by the policy — close cousin to disability.",
        "is": ["Common label in SA group income protection policies", "Often tied to Date of Absence and waiting period"],
        "is_not": ["Any day you feel too ill to attend", "Automatic because HR accepted a sick note"],
        "policy_note": "Date of Absence usually marks when incapacity began for benefit purposes — a different date from symptom onset or first sick note.",
        "evidence": "Policy definition, chronology, employer statement, medical records",
        "confused_with": ["Sickness", "Disability", "Date of Absence"],
        "example": "Incapacity for policy purposes may start when you cannot perform material duties, not first mild symptoms.",
        "how_you_know": [
            "You cannot perform material duties of your occupation — not merely feeling unwell.",
            "Absence or earnings drop is consistent with that inability, not convenience.",
            "Medical support links health to work incapacity (not only 'patient is sick').",
            "The day core duties became impossible is usually your Date of Absence.",
        ],
        "triggers": [
            "Stopping work or dropping below policy earnings threshold because of health.",
            "Doctor certifying inability to perform your occupation — exact wording matters.",
            "Employer recording formal absence from material duties.",
            "Waiting period clock starting from DOA or first continuous day of incapacity.",
            "Insurer claim form asking for 'date incapacity commenced'.",
        ],
        "check_questions": [
            "Can I still do the core tasks that define my role — or only attend in name?",
            "Is my absence continuous, or did a return to light duties reset the waiting period?",
            "Does my certificate say unfit for my occupation — or only generic sick leave?",
            "Is my DOA the first symptom day, first sick note, or when duties actually stopped?",
        ],
        "term_links": [
            {"term": "Sickness", "relation": "Not the same as", "note": "HR sick leave ≠ policy incapacity — employers and insurers use different tests."},
            {"term": "Illness", "relation": "Upstream", "note": "Illness describes health; incapacity is when health stops you working under policy rules."},
            {"term": "Functional capacity", "relation": "Proved by", "note": "Duty-impact evidence bridges medical facts to incapacity."},
            {"term": "Date of Absence", "relation": "Anchored on", "note": "DOA usually marks when incapacity began for benefit purposes."},
            {"term": "Disability", "relation": "May lead to", "note": "Sustained incapacity through the policy test period supports a disability finding."},
            {"term": "Waiting period", "relation": "Clock starts", "note": "Continuous incapacity must run across the full waiting period."},
            {"term": "Material duties", "relation": "Tested against", "note": "Incapacity means inability to perform these — not your job title."},
        ],
        "date_ladder": [
            {"label": "Symptom onset", "note": "When you first felt unwell — usually not your DOA"},
            {"label": "Stopped performing duties", "note": "When core tasks became impossible — often your DOA"},
            {"label": "First sick note", "note": "May be days after DOA; insurers may argue earlier or later"},
            {"label": "First notice to employer/insurer", "note": "Separate date insurers track for notice clauses"},
            {"label": "Waiting period satisfied", "note": "Continuous incapacity from DOA through deferred period"},
        ],
    },
    {
        "term": "Date of Absence",
        "slug": "date-of-absence",
        "lane": "policy",
        "emoji": "📆",
        "one_liner": "The date incapacity began for policy purposes — often when material duties stopped, not first symptoms.",
        "is": [
            "Anchor date for waiting period and benefit chronology",
            "Recorded by you, employer, and insurer — may differ between them",
            "Often the day you could no longer perform core occupational duties",
        ],
        "is_not": [
            "The same as symptom onset or first mild sick day",
            "Automatically the date on your first medical certificate",
            "Chosen by you alone — insurers calculate and may dispute it",
        ],
        "policy_note": "DOA disputes are common. Insurers may select an earlier date (pre-existing) or later date (light duties). Build a date ladder with evidence for each rung.",
        "evidence": "Employer absence register, medical certificates, duty-impact statement, insurer claim file",
        "confused_with": ["Symptom onset", "Incapacity", "Waiting period", "Cover start"],
        "example": "Symptoms from March; stopped client-facing duties 12 June (your DOA); first certificate 14 June.",
        "how_you_know": [
            "You identify the first day you could not perform material duties — not just felt unwell.",
            "Employer absence system shows continuous absence from that date.",
            "Insurer may state a different DOA on assessment — flag the conflict early.",
        ],
        "triggers": [
            "Formal stop-work or reduced duties below policy threshold.",
            "Waiting period measured from DOA or first incapacity day per clause.",
            "Pre-existing look-back may compare DOA to cover start and symptom history.",
            "Notice-to-insurer deadlines may run from DOA or first medical consultation.",
        ],
        "check_questions": [
            "What is my DOA vs insurer-stated DOA — and what evidence supports mine?",
            "Did I perform any light duties after my stated DOA (resets waiting period)?",
            "When did symptoms start vs when did duties become impossible?",
        ],
        "term_links": [
            {"term": "Incapacity", "relation": "Marks start of", "note": "DOA is when policy incapacity is deemed to have begun."},
            {"term": "Waiting period", "relation": "Measured from", "note": "Deferred period usually runs from DOA or first incapacity day."},
            {"term": "Illness", "relation": "Later than", "note": "You can be ill before DOA — illness onset ≠ incapacity onset."},
            {"term": "Sickness", "relation": "Later than", "note": "First sick day is often before true duty incapacity."},
            {"term": "Cover start", "relation": "Compared to", "note": "Insurers compare DOA and symptom history against cover commencement."},
        ],
        "date_ladder": [
            {"label": "Symptom onset", "note": "Earliest health signs — not DOA"},
            {"label": "Stopped performing duties", "note": "Your best candidate for DOA"},
            {"label": "First sick note", "note": "Supporting evidence — may not define DOA"},
            {"label": "Insurer-stated DOA", "note": "Capture if different — request calculation method"},
        ],
    },
    {
        "term": "Total vs partial disability",
        "lane": "policy",
        "emoji": "◐",
        "one_liner": (
            "Two policy doors, not two medical grades: total usually means you cannot perform "
            "the insured occupation; partial (residual) means some work continues and earnings or hours have dropped."
        ),
        "is": [
            "A wording choice in the policy — total, partial, residual, or proportionate",
            "Often an earnings or hours formula once some work continues",
            "Still a duty test: residual usually requires that you cannot do one or more material duties",
            "Capable of flipping over time — total in month one, residual on a graded return",
        ],
        "is_not": [
            "A medical severity score (mild / moderate / severe is not the test)",
            "The same as temporary versus permanent",
            "Automatically total because you have a serious diagnosis",
            "Automatically partial because you answered an email from the sofa",
        ],
        "policy_note": (
            "Read the residual / partial clause before you accept a total-disability frame — or before you "
            "volunteer light duties. Many Australian and South African IP wordings pay a proportion of the "
            "total benefit when current earnings sit below the baseline the formula uses (sometimes with a "
            "minimum drop, often 20%). Hours-based formulae exist too. Offsets, the waiting period, and "
            "own occupation versus any occupation still apply. This is organisation of the test, not a "
            "calculation of your claim."
        ),
        "evidence": (
            "Pre-disability payslips and hours, current payslips and hours, duty list of what stopped versus "
            "what continues, employer confirmation of light duties, policy residual clause and definition of "
            "pre-disability earnings"
        ),
        "confused_with": [
            "Temporary disability",
            "Functional limitation",
            "Own occupation",
            "Material duties",
            "Disability",
        ],
        "example": (
            "Reduced from five client days to two, earnings at 40% of the old figure — that is often argued "
            "as partial / residual, not as a failed total-disability claim."
        ),
        "how_you_know": [
            "You have stopped the occupation entirely, including light versions of it — total is the usual door.",
            "You still do some of the job, or a reduced-hours version, and you earn less than before — partial / residual is the usual door.",
            "The policy names a formula: earnings drop, hours drop, or both, sometimes with a minimum percentage.",
            "The insurer is treating 'you sent one email' as proof you can do the occupation — that is a duty argument, not a residual calculation.",
        ],
        "triggers": [
            "Graded return to work, light duties, or fewer days after the waiting period.",
            "A residual / partial / proportionate clause in the wording.",
            "Earnings or hours falling below the policy's pre-disability baseline.",
            "Initial Period own-occupation total test, then a later residual if some work resumes.",
            "An employer keeping you on in a stripped-down role so the file never looks 'total'.",
        ],
        "check_questions": [
            "Am I still performing any material duties of this occupation — or only incidental tasks?",
            "What are pre-disability earnings, and what are they now, in the same currency and period?",
            "Does my wording use earnings, hours, or both for residual?",
            "Is there a minimum drop (for example 20%) before residual pays?",
            "Has the test shifted from own occupation to any occupation while I was on a graded return?",
            "Would volunteering two light days this week reset the waiting period or close the total door?",
        ],
        "term_links": [
            {"term": "Disability", "relation": "Splits", "note": "Disability is the policy outcome; total vs partial is which benefit formula applies."},
            {"term": "Own occupation", "relation": "Tested first", "note": "Total under own occupation means you cannot do that job — not that you could never do any job."},
            {"term": "Material duties", "relation": "Split into", "note": "Partial often keeps some duties and loses others; list both sides."},
            {"term": "Functional limitation", "relation": "Feeds", "note": "Map each limitation to a duty that stopped, and a duty that continues if any."},
            {"term": "Incapacity", "relation": "May be", "note": "You can be incapacitated for the occupation and still do a few hours — that is residual, not recovery."},
            {"term": "Waiting period", "relation": "Must still run", "note": "Residual usually still needs continuous incapacity through the deferred period."},
        ],
        "date_ladder": [
            {"label": "Pre-disability baseline", "note": "Earnings and hours used by the residual formula — often a 12-month average, not last week's pay"},
            {"label": "Stopped material duties", "note": "When core work became impossible — often your DOA / date of disablement"},
            {"label": "Any light or reduced work", "note": "First day you did something the insurer may call 'work' — capture it even if unpaid"},
            {"label": "Current earnings / hours", "note": "What you actually receive and work now, same period as the baseline"},
        ],
        "guidance_topics": ["total-partial"],
        "illustrations": {
            "kind": "total-partial",
            "disclaimer": (
                "Illustrative only. Your policy may use a different formula, a minimum earnings drop, "
                "offsets, a 10-hour deeming rule, or a duty test that residual still has to meet. "
                "Not a benefit calculation."
            ),
            "pre_earn": 10000,
            "cur_earn": 4000,
            "pre_hours": 40,
            "cur_hours": 16,
            "hours_threshold": 10,
            "min_drop": 0.2,
            "currency_za": "R",
            "currency_au": "$",
            "scenarios": [
                {
                    "id": "consultant",
                    "title": "Consultant, two days left",
                    "role": "Management consultant",
                    "story": (
                        "Used to bill five days of client workshops. Panic and fatigue mean two short days "
                        "of emails and one internal meeting. Earnings about 40% of the old average."
                    ),
                    "duties_lost": "Client workshops, travel, full-day facilitation",
                    "duties_kept": "Email, internal catch-ups on two mornings",
                    "pre_earn": 18000,
                    "cur_earn": 7200,
                    "pre_hours": 50,
                    "cur_hours": 16,
                    "framing": "partial",
                    "explain": (
                        "Some work continues and earnings have dropped. Residual / partial is usually the "
                        "honest door — arguing total can fail if the insurer points at the two days."
                    ),
                },
                {
                    "id": "teacher",
                    "title": "Teacher, classes only",
                    "role": "Secondary teacher",
                    "story": (
                        "Still takes her own classes three days a week. Cannot do playground duty, sport, "
                        "camps, or after-school concerts. Pay is reduced for the two days off."
                    ),
                    "duties_lost": "Playground duty, sport, camps, concerts, five-day week",
                    "duties_kept": "Classroom teaching on three days",
                    "pre_earn": 8500,
                    "cur_earn": 5100,
                    "pre_hours": 45,
                    "cur_hours": 24,
                    "framing": "partial",
                    "explain": (
                        "Material duties of teaching are not only the timetable. Residual still needs the "
                        "lost duties named. If the policy treats 'can teach' as total-failure, that is a "
                        "duty argument — capture the extras."
                    ),
                },
                {
                    "id": "nurse",
                    "title": "Nurse, no nights or lifts",
                    "role": "Ward nurse",
                    "story": (
                        "Cannot do night shifts or patient lifts after surgery. Hospital offers a weekday "
                        "clinic admin desk at lower pay."
                    ),
                    "duties_lost": "Nights, heavy lifts, emergency bay",
                    "duties_kept": "Clinic admin, some seated observations",
                    "pre_earn": 7200,
                    "cur_earn": 3800,
                    "pre_hours": 38,
                    "cur_hours": 24,
                    "framing": "mixed",
                    "explain": (
                        "Own-occupation total may still be arguable if nights and lifts were material. "
                        "Accepting the admin desk without recording that it is not the occupation can "
                        "push the file into residual — or into 'you can work'."
                    ),
                },
                {
                    "id": "driver",
                    "title": "Driver who cannot drive",
                    "role": "Heavy-vehicle driver",
                    "story": (
                        "Seizure risk: licence suspended. Employer offers a dispatcher radio job. He has "
                        "not taken it. No earnings from driving."
                    ),
                    "duties_lost": "Driving, loading, night runs",
                    "duties_kept": "None of the occupation",
                    "pre_earn": 9000,
                    "cur_earn": 0,
                    "pre_hours": 45,
                    "cur_hours": 0,
                    "framing": "total",
                    "explain": (
                        "Under own occupation this is usually total — he cannot perform the job. A "
                        "dispatcher offer is a suited / any-occupation question for a later period, not "
                        "proof that driving duties continue."
                    ),
                },
                {
                    "id": "return",
                    "title": "Graded return, three half-days",
                    "role": "Analyst",
                    "story": (
                        "After the waiting period she tries three mornings a week. Output is slow; "
                        "earnings about 30% of baseline. Some weeks she cannot attend at all."
                    ),
                    "duties_lost": "Full-time analysis, deadlines, late reporting",
                    "duties_kept": "Limited morning analysis when well",
                    "pre_earn": 12000,
                    "cur_earn": 3600,
                    "pre_hours": 40,
                    "cur_hours": 12,
                    "framing": "partial",
                    "explain": (
                        "A graded return is the classic residual file. Capture weeks she cannot attend — "
                        "gaps can be used to say incapacity was not continuous, or to support that the "
                        "occupation is still not being performed."
                    ),
                },
                {
                    "id": "ten-hour",
                    "title": "Nine hours, Australian 10-hour rule",
                    "role": "Accountant",
                    "story": (
                        "Retail IP. She manages three short mornings — nine hours in total — and "
                        "earns about a quarter of pre-disability income. Some Australian PDS wordings "
                        "treat not working more than 10 hours as still totalling, or deem a 100% loss."
                    ),
                    "duties_lost": "Month-end, client meetings, full-time review",
                    "duties_kept": "Three short mornings of file notes",
                    "pre_earn": 14000,
                    "cur_earn": 3500,
                    "pre_hours": 40,
                    "cur_hours": 9,
                    "framing": "mixed",
                    "explain": (
                        "Toggle the 10-hour deeming rule below. Under that common Australian pattern "
                        "this can still be Door A (total / deemed 100% loss). Without it, nine hours "
                        "and a 75% earnings drop is residual. The PDS, not the diagnosis, picks the door."
                    ),
                },
            ],
        },
    },
    {
        "term": "Pre-existing condition",
        "slug": "pre-existing-condition",
        "lane": "policy",
        "emoji": "🕰️",
        "one_liner": (
            "A policy exclusion with clocks and causation — not ‘anything a doctor ever wrote’. "
            "Look-back window, disablement window, and what actually caused duties to stop."
        ),
        "is": [
            "A clause that can exclude disablement caused by a condition known, treated, or symptomatic in a defined period before cover",
            "Often two clocks on South African group wording: look-back (commonly six months) and first twelve months of cover",
            "In Australia, a PDS definition plus Insurance Contracts Act s 47 (awareness) — and a separate non-disclosure remedy",
            "A matter the insurer usually has to prove, with contemporaneous notes, not a later summary",
        ],
        "is_not": [
            "Every old diagnosis on a script or medical-aid history",
            "Automatically the same as non-disclosure or a retrospective exclusion added at claim stage",
            "Proved by a historic injury years before the look-back (NFO CR403)",
            "Still alive on typical SA group wording if disablement falls after the first twelve months (NFO CR356)",
        ],
        "policy_note": (
            "Read the actual exclusion: whose knowledge, which months, whether symptoms without treatment count, "
            "and whether disablement must fall inside a first-year window. Separate a stable baseline from a new "
            "post-cover event. South African group files often follow NFO CR356 (two limbs) and CR403 (onus and "
            "causation). Australian files split PDS wording, s 47 awareness, and ICA s 29 disclosure. This is "
            "organisation of the test — not a decision on your claim."
        ),
        "evidence": (
            "Cover start / entry date, look-back medical notes, occupational-health or fitness clearances just "
            "before cover, first advice or treatment dates, new-event records, date duties stopped, treating "
            "opinion on causation"
        ),
        "confused_with": [
            "Diagnosis",
            "Cover start",
            "Date of Absence",
            "Illness",
            "Waiting period",
        ],
        "example": (
            "Back injury in 2003, cover in 2016, leg weakness from 2017 — the 2003 label is not the six-month "
            "look-back the clause asked for."
        ),
        "how_you_know": [
            "The decline letter says ‘pre-existing’ but quotes a diagnosis from years before the look-back months.",
            "You were treated for something in the look-back, then a different acute event after cover stopped the job.",
            "Disablement (duties stopped) is more than twelve months after group entry — many SA clauses then fall away.",
            "In Australia, you had symptoms but no investigations before inception — s 47 awareness is the live question.",
            "The same letter also says you failed to disclose: that is a second ground, with different proof.",
        ],
        "triggers": [
            "Any decline that uses ‘related to’, ‘traceable to’, or ‘directly or indirectly’ a history before cover.",
            "Automatic group or super cover issued without medical questions — the exclusion is doing the underwriting.",
            "A stable chronic condition plus a new post-cover event (infection, injury, acute psychiatric episode).",
            "Date-of-absence disputes that pull the disablement date back into the first twelve months.",
            "Retail application forms: later s 29 variation or a retrospective exclusion instead of the PDS clause.",
        ],
        "check_questions": [
            "What is the cover start or fund entry date on the schedule — not the day I joined the employer?",
            "Which months are the look-back, and is there a first-year disablement window?",
            "What contemporaneous notes exist in those months — advice, treatment, investigations, symptoms?",
            "When did material duties actually stop, and is that inside the disablement window?",
            "What caused the stop: the look-back condition, or a new event / material change after cover?",
            "If this is Australia: was I aware, and would a reasonable person have been aware, of that condition before entry?",
        ],
        "term_links": [
            {"term": "Cover start", "relation": "Measured from", "note": "Look-back and first-year windows run from entry / commencement, not first symptom."},
            {"term": "Date of Absence", "relation": "Compared to", "note": "Disablement date is the second clock — pulling it earlier can wrongly trigger the exclusion."},
            {"term": "Diagnosis", "relation": "Not the same as", "note": "A historic label is not look-back proof and not automatically the cause of disablement."},
            {"term": "Illness", "relation": "May pre-date", "note": "You can be ill before cover; the clause asks whether that illness caused this disablement in the window."},
            {"term": "Waiting period", "relation": "Different clock", "note": "Waiting period is about when benefits start; pre-existing is about whether the claim is excluded."},
            {"term": "Disability", "relation": "Must still meet", "note": "Beating the exclusion does not win the claim — the occupational test remains."},
        ],
        "date_ladder": [
            {"label": "Look-back opens", "note": "Usually a fixed number of months before cover start — six is common on SA group files"},
            {"label": "Cover start / entry", "note": "Member certificate or schedule, not employment start if they differ"},
            {"label": "First-year window closes", "note": "On typical SA group wording, disablement after this date is outside the exclusion"},
            {"label": "New event (if any)", "note": "Post-cover injury, infection, or acute change — the usual causation split"},
            {"label": "Duties stopped (DOA)", "note": "The disablement clock — not first symptom and not the diagnosis stamp"},
        ],
        "guidance_topics": ["pre-existing"],
        "illustrations": {
            "kind": "pre-existing",
            "disclaimer": (
                "Illustrative clocks, not your clause. Typical South African group pattern: six-month "
                "look-back and a first-twelve-months disablement window, plus causation. Australian "
                "PDS windows and s 47 awareness differ. Not a decision on a claim."
            ),
            "lookback_months": 6,
            "window_months": 12,
            "range_start": -18,
            "range_end": 24,
            "scenarios": [
                {
                    "id": "historic",
                    "title": "Old injury, empty look-back",
                    "juris": "za",
                    "role": "Long-haul driver (CR403 pattern)",
                    "story": (
                        "Train accident years before cover. Cover starts. Months later, new left-leg "
                        "weakness stops driving. The insurer points at ‘chronic since 2003’."
                    ),
                    "lookback_months": 6,
                    "window_months": 12,
                    "symptoms": 4,
                    "treatment": 4,
                    "new_event": 4,
                    "doa": 8,
                    "historic_note": "Injury 13 years before cover — outside every clock on this sketch.",
                    "explain": (
                        "Look-back is empty: first treatment and the new weakness sit after cover. "
                        "Even though disablement is inside year one, the exclusion still needs a "
                        "look-back condition and a causal link. Historic pain is not that proof."
                    ),
                },
                {
                    "id": "two-limb",
                    "title": "Symptoms in look-back, disablement after year one",
                    "juris": "za",
                    "role": "Employee, group IP (CR356 pattern)",
                    "story": (
                        "Memory and balance already under investigation in the six months before "
                        "entry. He keeps working past the first anniversary. Duties stop in month 13."
                    ),
                    "lookback_months": 6,
                    "window_months": 12,
                    "symptoms": -4,
                    "treatment": -3,
                    "new_event": None,
                    "doa": 13,
                    "historic_note": "Limb 1 (look-back) is on; limb 2 (first twelve months) is off.",
                    "explain": (
                        "NFO CR356: both limbs are required. Symptoms before entry do not keep the "
                        "exclusion alive once disablement falls after month twelve. Pin the duty-stop "
                        "date — a later diagnosis does not move it."
                    ),
                },
                {
                    "id": "new-event",
                    "title": "Stable chronic plus a new event",
                    "juris": "za",
                    "role": "Consultant",
                    "story": (
                        "A managed chronic condition was treated in the look-back and did not stop "
                        "the job. After cover, an acute post-inception event (infection, injury) "
                        "changes function. The insurer attributes everything to the old label."
                    ),
                    "lookback_months": 6,
                    "window_months": 12,
                    "symptoms": -2,
                    "treatment": -2,
                    "new_event": 3,
                    "doa": 5,
                    "historic_note": "Look-back treatment is real. Causation is the fight.",
                    "explain": (
                        "Time windows may be on. The live question is cause: did the look-back "
                        "condition disable, or did the new event produce a material change? NFO "
                        "CR351 / CR403: historic disease in the background is not automatically "
                        "‘directly or indirectly’ the cause."
                    ),
                },
                {
                    "id": "applies",
                    "title": "All three limbs on",
                    "juris": "za",
                    "role": "Group member",
                    "story": (
                        "Treated for the same condition in the look-back. Duties stop in month five "
                        "from that condition. No new event."
                    ),
                    "lookback_months": 6,
                    "window_months": 12,
                    "symptoms": -3,
                    "treatment": -3,
                    "new_event": None,
                    "doa": 5,
                    "historic_note": "This is the pattern the typical SA group clause was written for.",
                    "explain": (
                        "Look-back, first-year disablement, and causation all line up. The exclusion "
                        "is in play — the remaining fight is whether the occupational test is met "
                        "and whether the notes actually match the clause (knowledge, treatment, symptoms)."
                    ),
                },
                {
                    "id": "s47",
                    "title": "Australia — symptoms, no diagnosis yet",
                    "juris": "au",
                    "role": "Retail life / IP applicant",
                    "story": (
                        "Headaches before inception. No scan, no specialist, no diagnosis. After "
                        "cover a serious condition is found and a claim is made. The insurer runs "
                        "the pre-existing exclusion."
                    ),
                    "lookback_months": 12,
                    "window_months": None,
                    "symptoms": -1,
                    "treatment": 2,
                    "new_event": None,
                    "doa": 3,
                    "historic_note": "s 47 asks about awareness, not the later label.",
                    "explain": (
                        "AFCA’s s 47 approach: was the person aware, and would a reasonable person "
                        "have been aware, of that condition before the contract? A stray symptom "
                        "is not automatically awareness; a GP, a same-day CT, and surgery the next "
                        "week usually is. Contemporaneous notes decide it."
                    ),
                },
            ],
        },
    },
    {
        "term": "Own occupation",
        "lane": "policy",
        "emoji": "👔",
        "one_liner": "Policy test: cannot perform material duties of the job you actually do.",
        "is": ["Usually applies in Initial Period", "Needs real duty evidence, not generic title"],
        "is_not": ["Any job you could theoretically do", "A medical impairment percentage"],
        "policy_note": "Extended Period may shift to any/suitable occupation — track when the test changes.",
        "evidence": "Material duties list, functional statement, employer role confirmation",
        "confused_with": ["Material duties", "Suitable occupation"],
        "example": "Cannot perform your actual consulting role even if you could do sedentary admin elsewhere.",
    },
]

CONFUSION_PAIRS: list[dict] = [
    {
        "left": "Diagnosis",
        "right": "Disability",
        "left_meaning": "Medical label — what the condition is called",
        "right_meaning": "Policy outcome — whether you meet the insured work test",
        "distinction": "A serious diagnosis does not automatically win; a modest diagnosis can still support disability if duties are impossible.",
        "claim_tip": "Always pair each diagnosis with duty-impact evidence.",
        "intake_tip": "A label on a form is not the claim — pair every diagnosis with duty impact evidence.",
        "insurer_angle": "Insurers may accept the diagnosis on a certificate but still dispute whether it causes disability under your policy wording (own occupation, suited occupation, or activities of daily living).",
        "capture_steps": [
            {"label": "Record each diagnosis", "text": "ICD-10 if known, treating clinician, and date.", "term": "Diagnosis"},
            {"label": "Name material duties blocked", "text": "For each diagnosis, at least one duty it prevents you performing.", "term": "Material duties"},
            {"label": "Separate medical from policy test", "text": "Doctors diagnose; policies test work function.", "term": "Disability"},
        ],
        "story_format": "Diagnosis (F32.1): major depressive disorder — cannot perform client-facing workshops because of panic and poor concentration.",
    },
    {
        "left": "Illness",
        "right": "Incapacity",
        "left_meaning": "Everyday health problem language",
        "right_meaning": "Policy trigger word for when benefits logic starts",
        "distinction": "You can be ill before policy incapacity begins — dates matter.",
        "claim_tip": "Build a date ladder: symptom onset → cannot perform duties → DOA → first notice.",
        "intake_tip": "You can feel ill before policy incapacity begins — capture when duties became impossible, not just first symptoms.",
        "insurer_angle": "Waiting periods, pre-existing condition clauses, and date-of-absence disputes often turn on when you became unable to perform material duties — not when you first felt unwell.",
        "capture_steps": [
            {"label": "Symptom onset", "text": "When you first noticed symptoms (may be approximate).", "term": "Illness"},
            {"label": "Stopped performing duties", "text": "When core job tasks became impossible (often your DOA).", "term": "Date of Absence"},
            {"label": "First medical certificate", "text": "May differ from both dates above.", "term": "Diagnosis"},
            {"label": "First notice to employer or insurer", "text": "Another date insurers track separately.", "term": "Incapacity"},
        ],
        "story_format": "Timeline: symptoms from March 2024; stopped performing duties 12 June 2024; first medical certificate 14 June 2024.",
    },
    {
        "left": "Total disability",
        "right": "Partial disability",
        "left_meaning": "Usually: cannot perform the insured occupation (or no work/earnings from it)",
        "right_meaning": "Some work continues; benefit often a proportion of the total benefit from an earnings or hours drop",
        "distinction": (
            "These are policy doors, not medical grades. A serious diagnosis can sit in residual if two days of "
            "work continue. A driver who cannot drive can be total under own occupation even if a desk job exists."
        ),
        "claim_tip": (
            "List duties that stopped and duties that continue. Capture pre-disability versus current earnings "
            "and hours. Do not volunteer light duties without reading the residual clause."
        ),
        "intake_tip": (
            "If you are still doing some of the job, say so and map it — residual is often the honest frame, "
            "and hiding two days of work is how total claims collapse."
        ),
        "insurer_angle": (
            "Insurers use leftover tasks to deny total, and leftover earnings to cap residual. They may also "
            "treat a graded return as recovery. Keep the formula and the duty list in the same file."
        ),
        "capture_steps": [
            {"label": "Pre-disability baseline", "text": "Earnings and hours the residual formula will use.", "term": "Total vs partial disability"},
            {"label": "Duties that stopped", "text": "Material duties you cannot perform.", "term": "Material duties"},
            {"label": "Duties that continue", "text": "Even two hours a week — name them.", "term": "Own occupation"},
            {"label": "Current earnings and hours", "text": "Same period as the baseline.", "term": "Total vs partial disability"},
        ],
        "story_format": (
            "Pre-disability: 5 client days, R18 000/month. Now: 2 mornings of email, R7 200. "
            "Lost: workshops and travel. Residual / partial — not a failed total claim."
        ),
    },
    {
        "left": "Pre-existing condition",
        "right": "Date of Absence",
        "left_meaning": "Exclusion clocks and causation — look-back, first-year window, what caused disablement",
        "right_meaning": "When policy incapacity / duties-stopped is deemed to have begun",
        "distinction": (
            "A historic diagnosis is not the disablement date. Pulling Date of Absence back into "
            "the first twelve months can wrongly switch a pre-existing exclusion on; leaving it "
            "on the day duties actually stopped can switch the same clause off (NFO CR356)."
        ),
        "claim_tip": (
            "Build both clocks: look-back notes versus the day material duties stopped. Do not "
            "let a later diagnosis or an earlier ache move DOA without evidence."
        ),
        "intake_tip": (
            "Capture cover start, first advice/treatment, any new event, and the day you stopped "
            "the job — four dates, not one story."
        ),
        "insurer_angle": (
            "Insurers may pick an early DOA to fit the first-year window, or treat any old label "
            "as look-back proof. NFO CR403 requires contemporaneous notes and causation."
        ),
        "capture_steps": [
            {"label": "Cover start / entry", "text": "Schedule or member certificate.", "term": "Cover start"},
            {"label": "Look-back notes", "text": "Advice, treatment, investigations in the contractual months.", "term": "Pre-existing condition"},
            {"label": "New event if any", "text": "Post-cover change that actually altered function.", "term": "Illness"},
            {"label": "Duties stopped", "text": "Your best candidate for Date of Absence.", "term": "Date of Absence"},
        ],
        "story_format": (
            "Cover 1 Nov 2016. Look-back empty. New left-leg weakness March 2017. Duties stopped "
            "1 July 2017. Historic 2003 injury is background, not the clause."
        ),
    },
    {
        "left": "Injury",
        "right": "Illness",
        "left_meaning": "Event-based harm",
        "right_meaning": "Disease, disorder, or deterioration — often no single accident",
        "distinction": "Policies may treat causation, exclusions, and evidence differently.",
        "claim_tip": "Document the story: sudden event vs gradual onset.",
    },
    {
        "left": "Symptom",
        "right": "Functional limitation",
        "left_meaning": "What you feel",
        "right_meaning": "What you cannot do at work because of it",
        "distinction": "Insurers need the second. Symptoms are the raw material.",
        "claim_tip": 'Use format: "Because of [symptom], I cannot [duty]."',
        "intake_tip": "Translate each symptom into a material duty it blocks — that is what insurers argue about.",
        "insurer_angle": "Medical certificates list symptoms; claim decisions turn on whether those symptoms stop you performing the insured occupation's material duties.",
        "capture_steps": [
            {"label": "Name symptoms", "text": "Everyday language first (fatigue, brain fog, panic, pain).", "term": "Symptom"},
            {"label": "Pick functional area", "text": "From your occupation map (cognitive, travel, people, physical).", "term": "Functional capacity"},
            {"label": "Link symptom to duty", "text": "Cannot perform X because of Y.", "term": "Functional limitation"},
            {"label": "Repeat for each pair", "text": "Every symptom–duty link that matters to your role.", "term": "Functional limitation"},
        ],
        "story_format": "Duty link (cognitive): cannot perform client analysis workshops because brain fog and poor concentration.",
    },
    {
        "left": "Capacity (unaided)",
        "right": "Performance (with treatment)",
        "left_meaning": "WHO-ICF: what you can do without aids in a standard setting",
        "right_meaning": "WHO-ICF: what you actually do with treatment, aids, and environment",
        "distinction": "Income-protection policies usually assess treated performance. Discrimination statutes often look at the unmitigated baseline. Mixing those axes is the mitigated-state trap.",
        "claim_tip": "Write both: function without current treatment, and function on the treatment you actually take — including side-effects.",
        "intake_tip": "Do not let 'stable on medication' stand in for 'can perform material duties'.",
        "insurer_angle": "Assessors may treat the existence of treatment as proof of work capacity, or demand unaided function on a policy that tests the treated state.",
    },
    {
        "left": "Functional capacity",
        "right": "Activities of daily living",
        "left_meaning": "Work-duty performance",
        "right_meaning": "Home/self-care tasks",
        "distinction": "IP own-occupation claims usually need work-function proof, not only ADL.",
        "claim_tip": "Confirm which test your policy clause actually uses.",
    },
    {
        "left": "Impairment",
        "right": "Disability (policy)",
        "left_meaning": "Clinical reduction in function",
        "right_meaning": "Contractual benefit entitlement test",
        "distinction": "Medical ratings and policy tests use different scales.",
        "claim_tip": "Translate impairment findings into material-duty language.",
    },
    {
        "left": "Sickness",
        "right": "Incapacity",
        "left_meaning": "Colloquial absence from work",
        "right_meaning": "Defined policy concept with date and test consequences",
        "distinction": "HR may accept sickness while insurer disputes incapacity under policy.",
        "claim_tip": "Do not assume employer sick-note acceptance equals insurer incapacity acceptance.",
        "intake_tip": "A sick note gets you off work with HR — incapacity is when you cannot perform material duties under policy wording.",
        "insurer_angle": "Employers track sick leave; insurers test whether you are incapacitated for your occupation, when that started (DOA), and whether it continued through the waiting period.",
        "capture_steps": [
            {"label": "HR sick days", "text": "Note each sick day HR recorded — separate from policy incapacity.", "term": "Sickness"},
            {"label": "Material duties stopped", "text": "When duties became impossible — your likely DOA.", "term": "Date of Absence"},
            {"label": "Certificate wording", "text": "'Sick' vs 'unfit for occupation'.", "term": "Incapacity"},
            {"label": "Light duty returns", "text": "Any return may reset the waiting period.", "term": "Waiting period"},
        ],
        "story_format": "HR sickness: off 3–10 June with sick note. Policy incapacity: could not perform client workshops from 12 June (DOA).",
    },
    {
        "left": "Job title",
        "right": "Material duties",
        "left_meaning": "Label on contract or email signature",
        "right_meaning": "Tasks that actually define whether you can work",
        "distinction": "Senior titles often hide cognitive, client, and safety demands.",
        "claim_tip": "Describe duties from reality, not business card.",
    },
]

LADDER_STEPS: list[dict[str, str]] = [
    {
        "step": "1",
        "title": "What happened",
        "terms": "Sickness · Illness · Injury · Condition",
        "question": "What words do you naturally use to describe it?",
    },
    {
        "step": "2",
        "title": "What medicine records",
        "terms": "Diagnosis · Symptom · Impairment · Prognosis",
        "question": "What has a doctor documented?",
    },
    {
        "step": "3",
        "title": "What work requires",
        "terms": "Functional capacity · Material duties · Limitations",
        "question": "Which duties can you no longer perform, and why?",
    },
    {
        "step": "4",
        "title": "What the policy pays on",
        "terms": "Incapacity · Disability · Own occupation · Partial/total",
        "question": "Which policy test applies at your claim stage?",
    },
]

_LADDER_ALIASES: dict[str, str] = {
    "limitations": "functional limitation",
    "partial/total": "total vs partial disability",
    "partial": "total vs partial disability",
    "total": "total vs partial disability",
}


def _ensure_term_slugs() -> None:
    for term in TERMS:
        term.setdefault("slug", slugify(term["term"]))


_ensure_term_slugs()

_TERM_BY_SLUG: dict[str, dict] = {t["slug"]: t for t in TERMS}
_TERM_BY_NAME: dict[str, str] = {t["term"].lower(): t["slug"] for t in TERMS}


def language_term_slug(name: str) -> str | None:
    """Resolve a display name to a language-map term slug."""
    key = name.strip().lower()
    if key in _TERM_BY_NAME:
        return _TERM_BY_NAME[key]
    alias = _LADDER_ALIASES.get(key)
    if alias and alias in _TERM_BY_NAME:
        return _TERM_BY_NAME[alias]
    for term_name, slug in _TERM_BY_NAME.items():
        if key in term_name or term_name in key:
            return slug
    return None


def get_language_term(slug: str) -> dict | None:
    return _TERM_BY_SLUG.get(slug)


def term_confusion_pairs_for(name: str) -> list[dict]:
    pairs: list[dict] = []
    for pair in CONFUSION_PAIRS:
        if pair["left"] == name or pair["right"] == name:
            pairs.append(enrich_confusion_pair(pair))
    return pairs


_EXTRA_LINK_PHRASES: tuple[tuple[str, str], ...] = (
    ("core job tasks", "Material duties"),
    ("core tasks", "Material duties"),
    ("occupational incapacity", "Incapacity"),
    ("diagnosis label", "Diagnosis"),
    ("material duties", "Material duties"),
    ("stopped performing duties", "Date of Absence"),
    ("symptom onset", "Illness"),
    ("first noticed symptoms", "Symptom"),
    ("symptoms", "Symptom"),
    ("health problem", "Illness"),
    ("'ill'", "Illness"),
    ("sick leave", "Sickness"),
    ("sick note", "Sickness"),
    ("waiting period", "Waiting period"),
    ("date of absence", "Date of Absence"),
    ("insurer-stated doa", "Date of Absence"),
    ("light duties", "Functional capacity"),
    ("duty impact", "Functional limitation"),
    ("own occupation", "Own occupation"),
    ("own-occupation", "Own occupation"),
    ("any occupation", "Own occupation"),
    ("occupation", "Own occupation"),
    ("partial disability", "Total vs partial disability"),
    ("partially disabled", "Total vs partial disability"),
    ("residual disability", "Total vs partial disability"),
    ("proportionate benefit", "Total vs partial disability"),
    ("10-hour", "Total vs partial disability"),
    ("pre-existing exclusion", "Pre-existing condition"),
    ("pre-existing condition", "Pre-existing condition"),
    ("look-back window", "Pre-existing condition"),
    ("look-back", "Pre-existing condition"),
    ("section 47", "Pre-existing condition"),
    ("s 47", "Pre-existing condition"),
    ("job title", "Material duties"),
    ("home tasks", "Activities of daily living (ADL)"),
    ("first consultation", "Diagnosis"),
    ("certificates", "Diagnosis"),
    ("certificate", "Diagnosis"),
    ("illness vs injury", "Illness"),
    ("work impact", "Functional capacity"),
    ("duty impact", "Functional limitation"),
    ("post-cover deterioration", "Cover start"),
    ("medical certificates", "Diagnosis"),
    ("condition label", "Condition"),
)

# Resource xrefs (traps, confusion pairs, atlas) inside language-map detail copy.
_LANG_DETAIL_RESOURCE_PHRASES: tuple[tuple[str, str, str], ...] = (
    ("diagnosis trap", "diagnosis-trap", "trap"),
    ("pre-existing trap", "pre-existing-trap", "trap"),
    ("job-title trap", "job-title-trap", "trap"),
    ("job title trap", "job-title-trap", "trap"),
    ("illness vs injury", "injury-illness", "confusion"),
    ("illness ≠ injury", "injury-illness", "confusion"),
    ("job title ≠ material duties", "job-title-material-duties", "confusion"),
    ("job title vs material duties", "job-title-material-duties", "confusion"),
    ("light office work", "functional-capacity", "language"),
    ("sedentary admin", "functional-capacity", "language"),
    ("IME assessors", "functional-capacity", "language"),
)


def _link_phrase_table() -> list[tuple[str, str]]:
    seen: set[str] = set()
    rows: list[tuple[str, str]] = []
    for phrase, term_name in _EXTRA_LINK_PHRASES:
        slug = language_term_slug(term_name)
        key = phrase.lower()
        if slug and key not in seen:
            rows.append((phrase, slug))
            seen.add(key)
    for term in TERMS:
        key = term["term"].lower()
        if key not in seen:
            rows.append((term["term"], term["slug"]))
            seen.add(key)
    return sorted(rows, key=lambda x: len(x[0]), reverse=True)


def link_terms_in_text(text: str) -> list[dict[str, str]]:
    """Split text into plain and linkable segments for language-map explainers."""
    table = _link_phrase_table()
    if not text or not table:
        return [{"type": "text", "value": text or ""}]

    pattern = re.compile("|".join(re.escape(phrase) for phrase, _ in table), re.IGNORECASE)
    slug_by_lower = {phrase.lower(): slug for phrase, slug in table}

    segments: list[dict[str, str]] = []
    last = 0
    for match in pattern.finditer(text):
        if match.start() > last:
            segments.append({"type": "text", "value": text[last : match.start()]})
        matched = match.group(0)
        segments.append(
            {
                "type": "link",
                "label": matched,
                "slug": slug_by_lower[matched.lower()],
            }
        )
        last = match.end()
    if last < len(text):
        segments.append({"type": "text", "value": text[last:]})
    return segments or [{"type": "text", "value": text}]


def _trap_hover(trap_name: str, fallback: str = "") -> str:
    from knowledge import TRAP_GLOSSARY_CONTEXT

    ctx = TRAP_GLOSSARY_CONTEXT.get(trap_name, {})
    return str(ctx.get("hover") or ctx.get("meaning") or fallback)


def _trap_name_from_slug(slug: str) -> str:
    from knowledge import trap_name_from_slug

    return trap_name_from_slug(slug)


def _detail_phrase_table() -> list[tuple[str, str, str]]:
    """Phrase table for detail pages: resource links + language-map terms."""
    seen: set[str] = set()
    rows: list[tuple[str, str, str]] = []
    for phrase, slug, kind in _LANG_DETAIL_RESOURCE_PHRASES:
        key = phrase.lower()
        if key not in seen:
            rows.append((phrase, slug, kind))
            seen.add(key)
    for phrase, slug in _link_phrase_table():
        key = phrase.lower()
        if key not in seen:
            rows.append((phrase, slug, "language"))
            seen.add(key)
    return sorted(rows, key=lambda x: len(x[0]), reverse=True)


def link_language_detail_text(text: str) -> list[dict[str, str]]:
    """Split term-detail copy into segments with hover tips and resource xrefs."""
    if not text:
        return [{"type": "text", "value": ""}]

    table = _detail_phrase_table()
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
            trap_name = _trap_name_from_slug(slug)
            hover = _trap_hover(trap_name, matched)
        elif kind == "confusion":
            pair = get_confusion_pair(slug)
            hover = str((pair or {}).get("tip") or (pair or {}).get("distinction") or matched)
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


def _confused_with_chip(name: str) -> dict[str, str]:
    key = name.strip().lower()
    exact_slug = _TERM_BY_NAME.get(key)
    if exact_slug:
        related = get_language_term(exact_slug) or {}
        return {
            "name": name,
            "slug": exact_slug,
            "link_kind": "language",
            "hover_tip": str(related.get("one_liner") or name),
        }
    slug = language_term_slug(name)
    if slug:
        related = get_language_term(slug) or {}
        return {
            "name": name,
            "slug": slug,
            "link_kind": "language",
            "hover_tip": str(related.get("one_liner") or name),
        }
    core_slug = slugify(name)
    return {
        "name": name,
        "slug": core_slug,
        "link_kind": "glossary",
        "hover_tip": f"Policy vocabulary — see glossary for “{name}”.",
    }


def term_resource_xrefs(term: dict) -> list[dict[str, str]]:
    """ClaimBuddy resource chips for a language-map term detail page."""
    term_slug = term.get("slug") or ""
    atlas_hover = "Clinical Atlas — ICD-10 conditions and SA medications for intake."
    try:
        from clinical_atlas import atlas_stats

        stats = atlas_stats()
        atlas_hover = (
            f"{stats['conditions']} conditions · {stats['medication_categories']} medication types · "
            "cross-linked in Clinical Atlas."
        )
    except Exception:
        pass

    specific: dict[str, list[dict[str, str]]] = {
        "condition": [
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "illnesses-injuries",
                "hover_tip": atlas_hover,
            },
            {
                "label": "Diagnosis trap",
                "link_kind": "trap",
                "slug": "diagnosis-trap",
                "hover_tip": _trap_hover("Diagnosis trap"),
            },
            {
                "label": "Illness ≠ Injury",
                "link_kind": "confusion",
                "slug": "injury-illness",
                "hover_tip": "Policies may treat accident vs disease differently — document your story shape.",
            },
        ],
        "diagnosis": [
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "illnesses-injuries",
                "hover_tip": atlas_hover,
            },
            {
                "label": "Diagnosis trap",
                "link_kind": "trap",
                "slug": "diagnosis-trap",
                "hover_tip": _trap_hover("Diagnosis trap"),
            },
            {
                "label": "Symptom → duty",
                "link_kind": "confusion",
                "slug": "symptom-functional-limitation",
                "hover_tip": "Insurers need what you cannot do at work — not just what you feel.",
            },
        ],
        "symptom": [
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "illnesses-injuries",
                "hover_tip": "Common symptoms per condition — add to health story from atlas pages.",
            },
            {
                "label": "Symptom → duty",
                "link_kind": "confusion",
                "slug": "symptom-functional-limitation",
                "hover_tip": "Translate each symptom into a blocked material duty.",
            },
        ],
        "illness": [
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "illnesses-injuries",
                "hover_tip": atlas_hover,
            },
            {
                "label": "Illness ≠ Injury",
                "link_kind": "confusion",
                "slug": "injury-illness",
                "hover_tip": "Separate story threads when both physical and mental impact apply.",
            },
        ],
        "injury": [
            {
                "label": "Injury conditions",
                "link_kind": "atlas_category",
                "slug": "injury",
                "hover_tip": "Injury category — ICD-10 trauma and MSK conditions in Clinical Atlas.",
            },
            {
                "label": "Illness ≠ Injury",
                "link_kind": "confusion",
                "slug": "injury-illness",
                "hover_tip": "Event-based harm vs gradual disease — evidence paths differ.",
            },
        ],
        "functional-capacity": [
            {
                "label": "Functional capacity",
                "link_kind": "module",
                "slug": "functional",
                "hover_tip": "Duty-impact matrix — map symptoms to material duties in your workspace.",
            },
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "",
                "hover_tip": atlas_hover,
            },
        ],
        "functional-limitation": [
            {
                "label": "Functional capacity",
                "link_kind": "module",
                "slug": "functional",
                "hover_tip": "Build limitation rows: symptom → duty blocked.",
            },
        ],
        "incapacity": [
            {
                "label": "Clinical Atlas",
                "link_kind": "atlas",
                "slug": "",
                "hover_tip": atlas_hover,
            },
            {
                "label": "Date trap",
                "link_kind": "trap",
                "slug": "date-trap",
                "hover_tip": _trap_hover("Date trap"),
            },
        ],
        "disability": [
            {
                "label": "Policy terms",
                "link_kind": "terms",
                "slug": "",
                "hover_tip": "Own occupation, waiting period, and disability tests in policy wording.",
            },
            {
                "label": "Diagnosis trap",
                "link_kind": "trap",
                "slug": "diagnosis-trap",
                "hover_tip": _trap_hover("Diagnosis trap"),
            },
        ],
        "total-vs-partial-disability": [
            {
                "label": "NFO / AFCA precedent",
                "link_kind": "precedent",
                "slug": "",
                "hover_tip": "CR72, CR276, CR259 and AFCA IP wording patterns — total and partial as separate doors.",
            },
            {
                "label": "Own occupation",
                "link_kind": "language",
                "slug": "own-occupation",
                "hover_tip": "Total under own occupation is the job you actually do — not any desk work.",
            },
            {
                "label": "Total ≠ Partial",
                "link_kind": "confusion",
                "slug": "total-disability-partial-disability",
                "hover_tip": "Policy doors, not medical grades.",
            },
        ],
        "pre-existing-condition": [
            {
                "label": "Pre-existing trap",
                "link_kind": "trap",
                "slug": "pre-existing-trap",
                "hover_tip": _trap_hover("Pre-existing trap"),
            },
            {
                "label": "NFO / AFCA precedent",
                "link_kind": "precedent",
                "slug": "",
                "hover_tip": "CR403, CR356, CR351 and AFCA s 47 — clocks, onus, awareness.",
            },
            {
                "label": "Cover start",
                "link_kind": "language",
                "slug": "cover-start",
                "hover_tip": "Look-back and first-year windows run from entry, not first symptom.",
            },
            {
                "label": "Pre-existing ≠ Date of Absence",
                "link_kind": "confusion",
                "slug": "pre-existing-condition-date-of-absence",
                "hover_tip": "Historic diagnosis is not the disablement date.",
            },
        ],
        "cover-start": [
            {
                "label": "Pre-existing condition",
                "link_kind": "language",
                "slug": "pre-existing-condition",
                "hover_tip": "Look-back and first-year windows are measured from this date.",
            },
            {
                "label": "Pre-existing trap",
                "link_kind": "trap",
                "slug": "pre-existing-trap",
                "hover_tip": _trap_hover("Pre-existing trap"),
            },
        ],
    }

    shared = [
        {
            "label": "Glossary",
            "link_kind": "glossary",
            "slug": "",
            "hover_tip": "Policy terms, traps, doctor questions, and checklist items.",
        },
        {
            "label": "Policy traps",
            "link_kind": "traps",
            "slug": "",
            "hover_tip": "Twelve traps insurers use — hover names on your dashboard for quick summaries.",
        },
        {
            "label": "Policy terms",
            "link_kind": "terms",
            "slug": "",
            "hover_tip": "Core policy vocabulary from the product plan.",
        },
    ]
    return list(specific.get(term_slug) or []) + shared


RELATION_ICONS: dict[str, str] = {
    "Broader than": "📏",
    "Documented as": "📝",
    "Precedes": "⏩",
    "Felt as": "💭",
    "Proved via": "🔗",
    "Proved by": "✅",
    "May become": "🌱",
    "Not the same as": "≠",
    "Does not start": "⏸️",
    "Earlier than": "⏪",
    "Later than": "⏩",
    "Labels": "🏷️",
    "Must pair with": "🤝",
    "Documents": "📄",
    "Does not prove": "🚫",
    "Measured against": "📊",
    "Measured from": "📅",
    "Compared to": "↔️",
    "Different clock": "⏱️",
    "Must still meet": "☑️",
    "Splits": "◐",
    "Built from": "🧱",
    "Bridges from": "🌉",
    "Proves": "✅",
    "Builds on": "📶",
    "Not decided by": "⛔",
    "Tested via": "🔬",
    "Tested against": "🎯",
    "May be": "❓",
    "After": "⏭️",
    "Requires": "‼️",
    "Upstream": "⬆️",
    "May lead to": "➡️",
    "Clock starts": "⏱️",
    "Marks start of": "📍",
    "Measured from": "📐",
    "Compared to": "⚖️",
    "Anchored on": "⚓",
    "Before": "⏳",
}


def relation_icon(relation: str) -> str:
    return RELATION_ICONS.get(relation.strip(), "↗️")


def term_ladder_step(term_name: str) -> dict | None:
    for step in LADDER_STEPS:
        for part in step["terms"].split("·"):
            label = part.strip()
            if not label:
                continue
            if language_term_slug(label) == language_term_slug(term_name):
                return step
    return None


def enrich_term_for_detail(term: dict) -> dict:
    resolved_links: list[dict] = []
    for link in term.get("term_links", []):
        slug = language_term_slug(link["term"])
        related = get_language_term(slug) if slug else {}
        resolved_links.append({
            **link,
            "slug": slug,
            "relation_icon": relation_icon(str(link.get("relation") or "")),
            "target_emoji": str(related.get("emoji") or "📎"),
            "hover_tip": str(related.get("one_liner") or link.get("note") or link["term"]),
        })
    check_questions = term.get("check_questions")
    check_linked = None
    if check_questions:
        check_linked = []
        for q in check_questions:
            segments = link_language_detail_text(q)
            for seg in segments:
                if seg.get("type") == "link" and seg.get("link_kind") == "language":
                    related = get_language_term(seg["slug"]) or {}
                    seg["hover_tip"] = str(related.get("one_liner") or seg["label"])
            check_linked.append(segments)
    topics = list(term.get("guidance_topics") or [])
    juris_guides: list[dict] = []
    precedents: list[dict] = []
    if topics:
        from ombud_guidance import guides_for_topics, precedents_for_topics

        juris_guides = guides_for_topics(topics)
        precedents = precedents_for_topics(topics)
    return {
        **term,
        "resolved_links": resolved_links,
        "confusion_pairs": term_confusion_pairs_for(term["term"]),
        "ladder": term_ladder_step(term["term"]),
        "check_questions_linked": check_linked,
        "policy_note_segments": link_language_detail_text(term.get("policy_note") or ""),
        "evidence_segments": link_language_detail_text(term.get("evidence") or ""),
        "one_liner_segments": link_language_detail_text(term.get("one_liner") or ""),
        "example_segments": (
            link_language_detail_text(term["example"]) if term.get("example") else None
        ),
        "is_linked": [link_language_detail_text(item) for item in term.get("is") or []],
        "is_not_linked": [link_language_detail_text(item) for item in term.get("is_not") or []],
        "confused_with_enriched": [_confused_with_chip(name) for name in term.get("confused_with") or []],
        "resource_xrefs": term_resource_xrefs(term),
        "juris_guides": juris_guides,
        "precedents": precedents,
    }


def ladder_with_term_links() -> list[dict]:
    rows = []
    for step in LADDER_STEPS:
        links = []
        for part in step["terms"].split("·"):
            label = part.strip()
            if not label:
                continue
            links.append({"label": label, "slug": language_term_slug(label)})
        rows.append({**step, "term_links": links})
    return rows


def terms_by_lane() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {lane["id"]: [] for lane in LANES}
    for term in TERMS:
        out[term["lane"]].append(term)
    return out


INTAKE_CONFUSION_PAIR_KEYS: tuple[tuple[str, str], ...] = (
    ("Illness", "Incapacity"),
    ("Diagnosis", "Disability"),
    ("Symptom", "Functional limitation"),
)


def confusion_pair_slug(left: str, right: str) -> str:
    return slugify(f"{left}-{right}")


def _resolve_capture_step(step: str | dict) -> dict:
    if isinstance(step, dict):
        label = step.get("label", "")
        text = step.get("text", "")
        slug = step.get("slug") or language_term_slug(step.get("term", ""))
        return {"label": label, "text": text, "slug": slug}
    if " — " in step:
        label, text = step.split(" — ", 1)
    else:
        label, text = step, ""
    label = label.strip()
    text = text.strip()
    slug = language_term_slug(label)
    return {"label": label, "text": text, "slug": slug}


def resolve_capture_steps(steps: list) -> list[dict]:
    return [_resolve_capture_step(step) for step in steps]


def enrich_confusion_pair(pair: dict) -> dict:
    slug = confusion_pair_slug(pair["left"], pair["right"])
    capture_steps = pair.get("capture_steps")
    return {
        **pair,
        "slug": slug,
        "tip": pair.get("intake_tip") or pair.get("claim_tip", ""),
        "capture_steps": resolve_capture_steps(capture_steps) if capture_steps else None,
    }


def get_confusion_pair(slug: str) -> dict | None:
    for pair in CONFUSION_PAIRS:
        if confusion_pair_slug(pair["left"], pair["right"]) == slug:
            return enrich_confusion_pair(pair)
    return None


def intake_confusion_guards() -> list[dict]:
    by_key = {(p["left"], p["right"]): enrich_confusion_pair(p) for p in CONFUSION_PAIRS}
    return [by_key[key] for key in INTAKE_CONFUSION_PAIR_KEYS if key in by_key]