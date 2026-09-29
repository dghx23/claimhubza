"""Shared product-plan knowledge from claimguard-site."""

from __future__ import annotations

from pathlib import Path

from content_data import (  # noqa: E402
    CONSTRUCTION_FIELDS_TABLE,
    CORE_POLICY_TERMS,
    DISABILITY_TEST_QUESTIONS,
    EVIDENCE_DOMAINS_TABLE,
    MVP_MODULES_TABLE,
    POLICY_TRAPS,
    TARGET_USERS_TABLE,
    TERM_CARD_FIELDS_TABLE,
    TERM_CARD_PIPELINE,
    WORKFLOW_STEPS,
)
from content_data_extra import (  # noqa: E402
    AI_COMPONENTS,
    BETA_INTAKE_FIELDS,
    BETA_OUTPUTS,
    BETA_SUCCESS,
    CLAIM_ONTOLOGY,
    CLAIM_STAGES,
    CORE_TEMPLATES,
    FOUNDER_INSIGHTS,
    GTM_CHANNELS,
    METRICS_DETAIL,
    MVP_MODULE_DETAILS,
    PRICING_TIERS,
    PROBLEM_GAPS,
    RISKS_TABLE,
    ROADMAP_DETAIL,
    TERM_CARD_EXAMPLES,
    TRUST_GUARDRAILS,
    WEBSITE_IA,
)

from language_map import language_term_slug  # noqa: E402
from term_slugs import slugify  # noqa: E402

DOCS_SITE = Path(__file__).resolve().parent.parent / "claimguard-site" / "site"
PDF_PATH = DOCS_SITE / "assets" / "pp.pdf"

TRAP_INDEX: dict[str, int] = {name: i for i, (name, _) in enumerate(POLICY_TRAPS)}

STAGE_TRAP_NAMES: dict[str, list[str]] = {
    "preparing": [
        "Date trap",
        "Job-title trap",
        "Employer-record trap",
        "Policy-vs-guide trap",
        "Diagnosis trap",
    ],
    "waiting_period": [
        "Date trap",
        "Diagnosis trap",
        "Employer-record trap",
        "Job-title trap",
    ],
    "assessment": [
        "Diagnosis trap",
        "Date trap",
        "Threshold-shift trap",
        "Employer-record trap",
        "Specialist-evidence trap",
        "Pre-existing trap",
        "Mitigated-state trap",
    ],
    "rejected": [
        "Appeal-story trap",
        "Diagnosis trap",
        "Date trap",
        "Employer-record trap",
        "Specialist-evidence trap",
        "Pre-existing trap",
        "Policy-vs-guide trap",
        "Gross-benefit trap",
        "Mitigated-state trap",
    ],
    "internal_review": [
        "Appeal-story trap",
        "Date trap",
        "Employer-record trap",
        "Specialist-evidence trap",
        "Policy-vs-guide trap",
        "Mitigated-state trap",
    ],
    "ombud": [
        "Appeal-story trap",
        "Date trap",
        "Employer-record trap",
        "Policy-vs-guide trap",
    ],
    "record_access": [
        "Employer-record trap",
        "Date trap",
        "Policy-vs-guide trap",
    ],
    "professional": [
        "Appeal-story trap",
        "Pre-existing trap",
        "Gross-benefit trap",
    ],
}

FLAG_TRAP_NAMES: dict[str, list[str]] = {
    "hospital_admission": ["Diagnosis trap"],
    "specialist_required": ["Specialist-evidence trap"],
    "preexisting": ["Pre-existing trap"],
    "occupation": ["Job-title trap"],
}

# Extended glossary context — cross-links traps to language map, modules, and evidence.
TRAP_GLOSSARY_CONTEXT: dict[str, dict[str, str | list[str]]] = {
    "Diagnosis trap": {
        "hover": "A diagnosis label alone does not prove you cannot perform material duties.",
        "meaning": (
            "Insurers may accept your ICD-10 code or specialist diagnosis but still dispute incapacity. "
            "The policy test is whether symptoms prevent the material duties of your own occupation — "
            "not whether a condition name sounds severe on paper."
        ),
        "evidence": (
            "Functional-capacity / duty-impact matrix, employer confirmation of material duties, "
            "treating-doctor letter addressing work limits (not diagnosis alone)."
        ),
        "language_terms": ["Diagnosis", "Functional capacity", "Disability"],
        "related_modules": ["Functional-capacity builder", "Evidence-gap detector"],
    },
    "Job-title trap": {
        "hover": "Job title may understate workload, pressure, travel, supervision, and error consequences.",
        "meaning": (
            "Insurers, IME assessors, and employers often reason from a generic job title instead of how the role "
            "actually runs — client load, deadlines, cognitive demand, site travel, supervision duties, and error risk. "
            "Own-occupation cover fails when the assessed role is narrowed to sedentary admin that is not your "
            "material duties."
        ),
        "evidence": (
            "ESCO or confirmed occupation profile, material duties list, job spec, performance expectations, "
            "organogram showing supervision and client-facing load, employer letter confirming core duties."
        ),
        "language_terms": ["Own occupation", "Material duties", "Functional capacity", "Occupation"],
        "related_modules": ["Guided intake", "Functional-capacity builder", "Policy reader", "Claim-pack generator"],
        "glossary_slugs": ["own-occupation", "job-title-trap"],
        "insurer_angle": (
            "Assessors may describe your role from the certificate job title or a generic HR description — "
            "then conclude you can still perform light office work. The policy test is material duties of your "
            "own occupation, not a simplified title."
        ),
        "claim_tip": (
            "Document duties from reality: client-facing load, travel, supervision, billable targets, site work, "
            "and decision pressure — then link symptoms to each blocked duty in the functional-capacity builder."
        ),
        "examples": [
            (
                "Certificate title: Senior Manager — insurer/IME treats role as sedentary admin. "
                "Reality: 12 client workshops per month, site travel, supervising eight staff, weekly board packs."
            ),
            (
                "Title: Consultant — assessed as desk-only. Reality: 60% client-facing time, flights twice monthly, "
                "audit sign-off with material error risk."
            ),
            (
                "Title: Partner — IME notes light office duties. Reality: billable-hour targets, evening client "
                "events, and high-pressure delivery — not filing and email alone."
            ),
        ],
        "example_quote": (
            '"They said I am a manager so I should manage email — but my material duties were running on-site '
            'audits and signing off work, not sitting at a desk."'
        ),
    },
    "Date trap": {
        "hover": "DOA, notice, submission, complete claim, waiting period, and rejection dates are rarely the same day.",
        "meaning": (
            "Each date triggers different policy effects — waiting-period satisfaction, late-notice declinature, "
            "pre-existing look-back, and rejection timelines. Mixing them in one narrative gives insurers "
            "an easy administrative escape."
        ),
        "evidence": (
            "Separate fields for symptom onset, DOA, employer date, insurer-stated DOA, first notice, "
            "form submission, complete claim, rejection, and review deadlines — each with proof."
        ),
        "language_terms": ["Date of Absence", "Waiting period", "First notice"],
        "related_modules": ["Guided intake", "Policy reader", "Rejection explainer"],
    },
    "Threshold-shift trap": {
        "hover": "The standard at submission may be broader than the standard applied at rejection.",
        "meaning": (
            "Employers, guides, or claim forms may suggest a lower evidence threshold than the policy test "
            "applied later. Insurers sometimes shift from own-occupation to any-occupation reasoning without "
            "clear disclosure."
        ),
        "evidence": (
            "Policy wording on disability test, submission correspondence, guide vs policy comparison, "
            "insurer assessment notes if disclosed."
        ),
        "language_terms": ["Own occupation", "Disability", "Functional capacity"],
        "related_modules": ["Policy reader", "Rejection explainer"],
    },
    "Policy-vs-guide trap": {
        "hover": "HR emails and claim guides may use broader language than binding policy wording.",
        "meaning": (
            "Marketing brochures, employer HR packs, and claim-form checklists are not the policy contract. "
            "When wording drifts, insurers may rely on the narrowest binding clause — especially on exclusions, "
            "waiting periods, and evidence duties."
        ),
        "evidence": (
            "Uploaded policy schedule, member certificate, rejection letter citing specific clauses, "
            "side-by-side comparison of guide language vs policy text."
        ),
        "language_terms": ["Exclusion", "Waiting period", "Proof of claim"],
        "related_modules": ["Policy reader", "Rejection explainer"],
    },
    "Employer-record trap": {
        "hover": "Payroll, absence records, and employer statements may be decisive but sit with HR — not you.",
        "meaning": (
            "Insurers often rely on employer-controlled records for DOA, attendance patterns, and role confirmation. "
            "If those records were never requested or are incomplete, adverse findings may rest on silence."
        ),
        "evidence": (
            "Employer statement, payroll, leave records, sick-note register, termination/absence correspondence — "
            "use access-request letters when files are missing."
        ),
        "language_terms": ["Date of Absence", "Material duties", "Proof of claim"],
        "related_modules": ["Access-request assistant", "Evidence-gap detector", "Document vault"],
    },
    "Specialist-evidence trap": {
        "hover": "Missing specialist evidence is unsafe if you were never told what, why, who obtains it, or who pays.",
        "meaning": (
            "Insurers may reject for absent consultant reports or IME findings without a clear prior request ladder. "
            "The fairness of the rejection depends on notice, specificity, and whether occupational duties were "
            "correctly described to the assessor."
        ),
        "evidence": (
            "Specialist reports, insurer further-evidence letters, IME instructions, material duties sent to assessors."
        ),
        "language_terms": ["Further medical evidence", "Functional capacity"],
        "related_modules": ["Evidence-gap detector", "Doctor Q&A"],
    },
    "Gross-benefit trap": {
        "hover": "Benefit % is not final until earnings definition, caps, offsets, and tax are checked.",
        "meaning": (
            "Headline replacement ratios ignore offsets for other income, pension contributions, medical aid, "
            "UIF, tax treatment, and payment route. Net entitlement can differ materially from the quoted percentage."
        ),
        "evidence": (
            "Payslips, policy benefit clause, offsets schedule, tax notes, CAMAF/medical-aid contribution proof."
        ),
        "language_terms": ["Income protection benefit", "Offset"],
        "related_modules": ["Guided intake", "Policy reader", "Claim-pack generator"],
    },
    "Pre-existing trap": {
        "hover": "An old diagnosis is not the same as proving pre-existing exclusion under your policy dates.",
        "meaning": (
            "Insurers separate baseline conditions, look-back periods, treatment before cover, and post-inception "
            "deterioration. A historic label on a script does not automatically defeat cover if duties stopped after "
            "cover started for a worsening trajectory. South African group wording is often two-limb (look-back AND "
            "disablement in the first twelve months). Australian files split the PDS definition, Insurance Contracts "
            "Act s 47 awareness, and a separate non-disclosure remedy."
        ),
        "evidence": (
            "Cover start proof, look-back treating notes, occupational-health clearances, new-event records, "
            "date duties stopped, causation opinion."
        ),
        "language_terms": ["Pre-existing condition", "Cover start", "Date of Absence", "Waiting period"],
        "related_modules": ["Policy reader", "Clinical Atlas"],
        "insurer_angle": (
            "A later summary (‘chronic since 2003’) or any old ICD code is treated as look-back proof. Date of "
            "Absence may be pulled earlier so disablement falls inside the first year. A disclosure fight may be "
            "folded into the same sentence as the exclusion."
        ),
        "claim_tip": (
            "Build the clocks: cover start, look-back notes, new event, duties stopped. Ask for contemporaneous "
            "records in the contractual months. Keep exclusion and non-disclosure as separate issue cards. NFO "
            "CR403 / CR356 and AFCA’s s 47 approach are the reading guides — not a substitute for your wording."
        ),
        "example_quote": (
            "Cover 1 Nov 2016. Six-month look-back empty. Left-leg weakness from 2017. 2003 train accident is "
            "background — not the clause (NFO CR403 pattern)."
        ),
        "examples": [
            "Insurer cites a 2003 injury for a 2017 disablement with no notes in the six months before cover.",
            "Symptoms in the look-back, but duties only stopped in month 13 — typical SA group two-limb miss (CR356).",
            "Stable treated condition plus a new post-cover event; the decline attributes everything to the old label.",
            "Australian decline that skips s 47 awareness and treats a later diagnosis as proof you ‘must have known’.",
        ],
    },
    "Appeal-story trap": {
        "hover": "Emotional narrative should become a structured issue matrix with evidence and remedies.",
        "meaning": (
            "Internal review and ombud processes reward issue-by-issue responses — policy clause, insurer fact, "
            "your evidence, cure action, remedy sought. Unstructured anger or long personal essays rarely shift "
            "technical declinatures."
        ),
        "evidence": (
            "Review-ground matrix, chronology, gap table, draft review letter, record-access responses."
        ),
        "language_terms": ["Complaint / appeal / internal review", "Proof of claim"],
        "related_modules": ["Rejection explainer", "Access-request assistant", "Claim-pack generator"],
    },
    "Mitigated-state trap": {
        "hover": "Income protection usually tests function WITH treatment; discrimination law often tests WITHOUT.",
        "meaning": (
            "WHO-ICF splits capacity (unaided, standard setting) from performance (with treatment, aids, and environment). "
            "South African income-protection wording typically assesses the treated/mitigated state and requires ongoing care. "
            "The ADA, UK Equality Act, and SA EEA Code often look at the unmitigated baseline for disability status. "
            "An assessor who treats 'stable on medication' as capacity for work is using the wrong axis for an IP test — "
            "and the opposite error (demanding unaided function on an IP claim) is equally wrong."
        ),
        "evidence": (
            "Policy treatment-compliance clause, treating-practitioner notes on function with and without current treatment, "
            "side-effects that destroy residual work capacity, ICF-style capacity vs performance description."
        ),
        "language_terms": ["Disability", "Incapacity", "Functional capacity", "Impairment"],
        "related_modules": ["Functional-capacity builder", "Policy reader", "Doctor Q&A"],
        "claim_tip": (
            "State which axis was used. If treatment restores some function but creates a new work-limiting side-effect, "
            "that is still a performance failure under own-occupation IP — not proof that disability has resolved."
        ),
        "insurer_angle": (
            "Insurers may argue that because medication exists, you can work. Policies usually require you to take "
            "reasonable treatment — they do not treat the existence of treatment as the disability test."
        ),
    },
}

# Doctor / disability-test questionnaire — cross-links to language map, glossary, and modules.
DOCTOR_QUESTION_CONTEXT: dict[str, dict[str, str | list[str]]] = {
    "Which test applies now?": {
        "hover": "Initial Period is usually own-occupation; Extended Period may shift to any-occupation or partial tests.",
        "meaning": (
            "Policies rarely use one disability standard for the whole claim. The Initial Period may test own occupation "
            "while the Extended Period switches to any occupation, partial capacity, or permanent thresholds. "
            "Your doctor should answer against the test that applies on the dates you were absent — not a generic "
            "'can you work somewhere' question."
        ),
        "evidence": (
            "Policy schedule disability clauses, Initial/Extended Period dates, insurer assessment letters citing the test applied."
        ),
        "language_terms": ["Own occupation", "Disability", "Partial disability", "Waiting period"],
        "related_modules": ["Policy reader", "Rejection explainer"],
        "glossary_slugs": ["own-occupation", "disability-incapacity", "partial-disability"],
    },
    "What is the relevant occupation?": {
        "hover": "Define the actual role — not a generic title — including client load, travel, supervision, and cognitive demand.",
        "meaning": (
            "Insurers assess incapacity against your insured occupation as actually performed: contract terms, job description, "
            "utilisation, client obligations, supervision duties, site travel, safety responsibilities, and sustained cognitive load. "
            "A narrow title-based assessment is a common reason own-occupation cover fails."
        ),
        "evidence": (
            "Job spec, contract, performance reviews, organogram, client roster, ESCO or confirmed occupation profile."
        ),
        "language_terms": ["Own occupation", "Material duties", "Functional capacity"],
        "related_modules": ["Guided intake", "Functional-capacity builder"],
        "glossary_slugs": ["own-occupation", "job-title-trap"],
    },
    "What are the material duties?": {
        "hover": "Separate core duties from incidental tasks — incapacity must map to duties the policy treats as material.",
        "meaning": (
            "Material duties are the substantive tasks that define whether you can perform your occupation — not every "
            "incidental admin task. Your doctor should explain which core duties are affected, why failure in those duties "
            "matters clinically, and whether partial performance is realistic or unsafe."
        ),
        "guidance": (
            "Use the Functional-capacity builder to list core vs incidental tasks from your job description, employer records, "
            "or occupation search — then ask your doctor to address each core duty the policy wording treats as material. "
            "Pair with the Claim readiness check on material duties and the Job-title trap glossary entry so evidence maps "
            "symptoms to real work demands, not a generic title. Own-occupation policies test whether you can perform "
            "those material duties continuously during the Initial Period."
        ),
        "evidence": (
            "Material duties list from profile or employer, functional-capacity matrix, employer confirmation of core vs incidental tasks."
        ),
        "language_terms": ["Material duties", "Functional capacity", "Own occupation", "Functional limitation"],
        "related_modules": ["Functional-capacity builder", "Guided intake", "Policy reader"],
        "glossary_slugs": ["job-title-trap", "own-occupation", "readiness-material-duties"],
    },
    "What medical events changed capacity?": {
        "hover": "Build a chronology: onset, deterioration, treatment, medication changes, hospital events, specialist findings, prognosis.",
        "meaning": (
            "Insurers and doctors often talk past each other when the timeline is vague. A clear chronology links symptom onset, "
            "deterioration, treatment response, medication changes, hospital admissions, specialist findings, and prognosis "
            "to the dates you stopped performing material duties."
        ),
        "evidence": (
            "GP notes, specialist letters, hospital records, medication history, Clinical Atlas condition summaries for your diagnoses."
        ),
        "language_terms": ["Diagnosis", "Functional capacity", "Further medical evidence"],
        "related_modules": ["Document vault", "Clinical Atlas"],
        "glossary_slugs": ["diagnosis-trap"],
    },
    "How does illness affect work function?": {
        "hover": "Map symptoms to attendance, alertness, cognitive endurance, decision quality, stamina, travel, supervision, and error risk.",
        "meaning": (
            "A diagnosis label does not prove incapacity — the policy test is work-function impact. Your doctor should connect "
            "symptoms and treatment effects to concrete limits: attendance reliability, sustained concentration, decision quality "
            "under pressure, physical stamina, treatment side-effects, travel tolerance, supervision capacity, and error or safety risk."
        ),
        "evidence": (
            "Functional-capacity / duty-impact matrix, treating-doctor letter addressing work limits, employer duty list."
        ),
        "language_terms": ["Functional capacity", "Disability", "Total disability", "Partial disability"],
        "related_modules": ["Functional-capacity builder", "Evidence-gap detector"],
        "glossary_slugs": ["diagnosis-trap", "disability-incapacity"],
    },
    "Was incapacity continuous through waiting period?": {
        "hover": "Every day in the waiting period needs aligned proof — leave, sick notes, payroll, and medical records.",
        "meaning": (
            "Waiting-period satisfaction is often decided on continuity of incapacity, not just the first sick note. "
            "Gaps between medical certificates, return-to-work days, or employer records that show attendance can defeat "
            "cover even when symptoms continued. Evidence must cover every part of the waiting period."
        ),
        "evidence": (
            "Sick notes covering full waiting period, payroll/leave register, employer absence statement, aligned medical chronology."
        ),
        "language_terms": ["Waiting period", "Date of Absence", "Proof of claim"],
        "related_modules": ["Guided intake", "Evidence-gap detector", "Access-request assistant"],
        "glossary_slugs": ["date-trap", "employer-record-trap"],
    },
    "What evidence is missing?": {
        "hover": "Tag gaps as medical, occupational, employer-controlled, salary, policy, or claim-file related.",
        "meaning": (
            "Rejections often cite missing evidence without a structured gap list. Separating what is missing by domain — "
            "medical, occupational, employer-controlled, salary-related, policy-related, or claim-file-related — "
            "turns a vague declinature into actionable requests."
        ),
        "evidence": (
            "Evidence-gap report from workspace, insurer further-evidence letters, checklist against policy proof-of-claim duties."
        ),
        "language_terms": ["Proof of claim", "Further medical evidence", "Material duties"],
        "related_modules": ["Evidence-gap detector", "Document vault", "Access-request assistant"],
        "glossary_slugs": ["employer-record-trap", "specialist-evidence-trap"],
    },
    "Who controls the missing evidence?": {
        "hover": "Identify whether the claimant, employer, insurer, doctor, payroll, or fund admin holds each missing record.",
        "meaning": (
            "Not every gap is your fault to fix. Employer payroll, HR absence records, fund-admin policy schedules, "
            "and insurer claim files sit with third parties. Naming who controls each missing item supports fair "
            "record-access requests and challenges unfair 'claimant failed to prove' wording."
        ),
        "evidence": (
            "Access-request letters, employer/insurer correspondence, consent forms, complaint escalation where disclosure is refused."
        ),
        "language_terms": ["Proof of claim", "Policyholder", "Participating employer"],
        "related_modules": ["Access-request assistant", "Evidence-gap detector"],
        "glossary_slugs": ["employer-record-trap", "policy-vs-guide-trap"],
    },
    "What is the insurer's actual reason?": {
        "hover": "Translate rejection wording into issue cards: late submission, no disability, pre-existing, missing evidence, exclusion, offset.",
        "meaning": (
            "Rejection letters often blend several grounds in narrative prose. Restating the insurer's actual reason as "
            "discrete issue cards — late submission, no disability, pre-existing, missing evidence, non-disclosure, "
            "exclusion, offset, admin defect — lets your doctor and adviser respond point by point."
        ),
        "evidence": (
            "Rejection letter, policy clauses cited, issue matrix from rejection explainer, chronology aligned to each ground."
        ),
        "language_terms": ["Disability", "Pre-existing condition exclusion", "Exclusion", "Complaint / appeal / internal review"],
        "related_modules": ["Rejection explainer", "Policy reader"],
        "glossary_slugs": ["pre-existing-trap", "appeal-story-trap", "threshold-shift-trap"],
    },
    "What would cure the issue?": {
        "hover": "For each issue: request records, targeted doctor answers, occupational proof, correct dates, or disclosure escalation.",
        "meaning": (
            "Every insurer issue should have a cure path — not just complaint. That may mean specific record requests, "
            "doctor questions tied to material duties, occupational evidence, corrected dates, challenging guide-vs-policy "
            "wording drift, or escalating for disclosure when files are withheld."
        ),
        "evidence": (
            "Draft cure actions per issue card, access-request pack, updated doctor letter, corrected intake dates, review letter."
        ),
        "language_terms": ["Proof of claim", "Complaint / appeal / internal review", "Further medical evidence"],
        "related_modules": ["Rejection explainer", "Access-request assistant", "Claim-pack generator"],
        "glossary_slugs": ["appeal-story-trap", "policy-vs-guide-trap"],
    },
}

# GIP claim-profile readiness checklist — synced with dashboard and policy reader.
POLICY_CHECKLIST: list[tuple[str, str]] = [
    ("waiting_period", "Waiting period identified and continuity evidence planned"),
    ("doa", "Date of Absence recorded (user + insurer if known)"),
    ("first_notice", "First notice date and proof identified"),
    ("own_occupation", "Own-occupation / Initial Period test noted"),
    ("material_duties", "Material duties described (not job title only)"),
    ("proof_of_claim", "Proof-of-claim checklist started"),
    ("record_access", "Employer/insurer record requests planned if needed"),
    ("complaint_route", "Review / ombud deadline tracked"),
]

POLICY_CHECKLIST_CONTEXT: dict[str, dict[str, str | list[str]]] = {
    "waiting_period": {
        "hover": "Name the waiting period in days and plan sick notes, leave, and payroll proof for every day.",
        "meaning": (
            "Group income protection usually requires a defined waiting period before benefit starts. "
            "Readiness means you know the period in days, understand that continuity of incapacity must be proved "
            "for every day in it, and have planned aligned medical certificates, leave records, and payroll evidence."
        ),
        "guidance": (
            "Use Policy reader to extract the waiting-period clause and Initial Period wording, then Guided intake "
            "to record Date of Absence and first-notice dates on a personal date ladder. Run Evidence-gap detector "
            "to flag payroll, HR leave, and sick-note gaps that break continuity across the full deferred period."
        ),
        "evidence": "Policy waiting-period clause, sick notes covering full period, payroll/leave register.",
        "language_terms": ["Waiting period", "Date of Absence", "Proof of claim"],
        "related_modules": ["Guided intake", "Policy reader", "Evidence-gap detector"],
        "glossary_slugs": ["waiting-period", "date-trap"],
    },
    "doa": {
        "hover": "Record your Date of Absence and capture the insurer's DOA if it differs — conflicts are common.",
        "meaning": (
            "Date of Absence (DOA) is the anchor for waiting-period satisfaction and benefit start. "
            "Record the date you stopped performing material duties, note the insurer's stated DOA if known, "
            "and flag conflicts early — DOA disputes are a frequent declinature route."
        ),
        "evidence": "User-stated DOA in profile, insurer DOA on claim file, employer absence statement.",
        "language_terms": ["Date of Absence", "Waiting period", "First notice"],
        "related_modules": ["Guided intake", "Policy reader"],
        "glossary_slugs": ["date-trap", "employer-record-trap"],
    },
    "first_notice": {
        "hover": "Identify when you first told the employer or insurer and what proof exists (email, form, call log).",
        "meaning": (
            "Policies set notice time limits from first incapacity or first absence. Readiness means you know "
            "the date notice was given, can point to proof (email, claim form, HR ticket, call reference), "
            "and understand how that date relates to DOA and late-notice clauses."
        ),
        "evidence": "First-notice date in profile, email/form proof, employer or insurer acknowledgement.",
        "language_terms": ["First notice", "Date of Absence", "Proof of claim"],
        "related_modules": ["Guided intake", "Document vault"],
        "glossary_slugs": ["date-trap"],
    },
    "own_occupation": {
        "hover": "Note whether Initial Period own-occupation applies — not just a job title.",
        "meaning": (
            "Own-occupation cover during the Initial Period tests incapacity against your actual insured occupation. "
            "Readiness means the policy test is identified, your occupation is described beyond a generic title, "
            "and you understand when the standard may shift to any-occupation in the Extended Period."
        ),
        "evidence": "Policy disability clause, occupation profile, Initial/Extended Period dates from schedule.",
        "language_terms": ["Own occupation", "Disability", "Functional capacity"],
        "related_modules": ["Policy reader", "Functional-capacity builder"],
        "glossary_slugs": ["own-occupation", "threshold-shift-trap"],
    },
    "material_duties": {
        "hover": "List core duties — client load, travel, supervision, cognition — not just the job title.",
        "meaning": (
            "Material duties are the substantive tasks that define whether you can perform your occupation. "
            "A title-only description invites the job-title trap. Readiness means core duties are written out "
            "so medical and functional evidence can map symptoms to real work demands."
        ),
        "evidence": "Material duties in profile, job spec, functional-capacity matrix, employer duty confirmation.",
        "language_terms": ["Material duties", "Own occupation", "Functional capacity"],
        "related_modules": ["Guided intake", "Functional-capacity builder"],
        "glossary_slugs": ["job-title-trap"],
    },
    "proof_of_claim": {
        "hover": "Start the proof-of-claim checklist — forms, medical evidence, employer records, policy schedule.",
        "meaning": (
            "Policies impose proof-of-claim duties: prescribed forms, medical evidence, employer statements, "
            "and supporting documents within time limits. Readiness means you have a claim reference or active "
            "checklist tracking what is submitted, outstanding, and who holds each item."
        ),
        "evidence": "Claim reference, submitted forms, evidence-gap list, insurer acknowledgement of complete claim.",
        "language_terms": ["Proof of claim", "Further medical evidence"],
        "related_modules": ["Evidence-gap detector", "Document vault", "Claim-pack generator"],
        "glossary_slugs": ["specialist-evidence-trap", "employer-record-trap"],
    },
    "record_access": {
        "hover": "Plan access requests when employer or insurer records you need sit with HR, payroll, or the fund.",
        "meaning": (
            "Many decisive records — payroll, absence registers, claim-file notes, policy schedules — are controlled "
            "by employers or insurers. At rejection or review stages, readiness means record-access requests are "
            "planned or underway when gaps are not yours to fill alone."
        ),
        "evidence": "Access-request letters, record-access status in profile, employer/insurer disclosure responses.",
        "language_terms": ["Proof of claim", "Policyholder", "Participating employer"],
        "related_modules": ["Access-request assistant", "Evidence-gap detector"],
        "glossary_slugs": ["employer-record-trap", "policy-vs-guide-trap"],
    },
    "complaint_route": {
        "hover": "Track internal review and ombud deadlines — missing a date can end your complaint rights.",
        "meaning": (
            "After rejection, internal review and ombud complaint routes have strict deadlines. Readiness means "
            "review and ombud dates are recorded, diarised, and linked to the grounds you will raise — not left "
            "to memory once the rejection letter arrives."
        ),
        "evidence": "Rejection letter deadlines, review_deadline and ombud_deadline in profile, draft review grounds.",
        "language_terms": ["Complaint / appeal / internal review", "Proof of claim"],
        "related_modules": ["Rejection explainer", "Claim-pack generator"],
        "glossary_slugs": ["appeal-story-trap", "date-trap"],
    },
}


def policy_checklist_slug(key: str) -> str:
    return f"readiness-{key.replace('_', '-')}"


def enrich_policy_checklist_item(key: str, label: str, done: bool) -> dict:
    """Full checklist row for dashboard, policy reader, and glossary cross-reference."""
    slug = policy_checklist_slug(key)
    ctx = POLICY_CHECKLIST_CONTEXT.get(key, {})
    hover = str(ctx.get("hover") or label)
    meaning = str(ctx.get("meaning") or label)
    evidence = str(ctx.get("evidence") or "")
    language_terms = ctx.get("language_terms") or []
    if isinstance(language_terms, str):
        language_terms = [language_terms]
    related_modules = ctx.get("related_modules") or []
    if isinstance(related_modules, str):
        related_modules = [related_modules]
    glossary_slugs = ctx.get("glossary_slugs") or []
    if isinstance(glossary_slugs, str):
        glossary_slugs = [glossary_slugs]
    guidance = str(ctx.get("guidance") or "")
    return {
        "key": key,
        "label": label,
        "done": done,
        "slug": slug,
        "hover_tip": hover,
        "meaning": meaning,
        "guidance": guidance,
        "evidence": evidence,
        "kind": "checklist_item",
        "language_links": _trap_language_links(list(language_terms)),
        "related_modules": list(related_modules),
        "glossary_slugs": list(glossary_slugs),
        "glossary_slug": slug,
        "module_links": _related_module_links(list(related_modules)),
    }


_POLICY_CHECKLIST_BY_SLUG: dict[str, tuple[str, str]] = {
    policy_checklist_slug(key): (key, label) for key, label in POLICY_CHECKLIST
}


def get_policy_checklist_item(slug: str) -> dict | None:
    row = _POLICY_CHECKLIST_BY_SLUG.get(slug)
    if not row:
        return None
    key, label = row
    return enrich_policy_checklist_item(key, label, done=False)


def policy_checklist_glossary_entries() -> list[dict]:
    """Claim readiness checklist rows for resources glossary."""
    return [
        {
            "term": label,
            "slug": policy_checklist_slug(key),
            "kind": "checklist_item",
            "meaning": str(POLICY_CHECKLIST_CONTEXT.get(key, {}).get("meaning") or label),
            "summary": label,
            "evidence": str(POLICY_CHECKLIST_CONTEXT.get(key, {}).get("evidence") or ""),
            "hover_tip": str(POLICY_CHECKLIST_CONTEXT.get(key, {}).get("hover") or label),
            "key": key,
        }
        for key, label in POLICY_CHECKLIST
    ]


def _related_module_links(module_names: list[str]) -> list[dict[str, str | bool]]:
    links: list[dict[str, str | bool]] = []
    for name in module_names:
        workspace = _MODULE_WORKSPACE.get(name, {})
        endpoint = workspace.get("endpoint")
        if not endpoint:
            continue
        links.append({
            "label": name,
            "slug": slugify(name),
            "endpoint": str(endpoint),
            "claim_scoped": bool(workspace.get("claim_scoped")),
            "fallback_endpoint": str(workspace["fallback_endpoint"]) if workspace.get("fallback_endpoint") else "",
        })
    return links


def _trap_language_links(term_labels: list[str]) -> list[dict[str, str]]:
    from language_map import get_language_term

    links: list[dict[str, str]] = []
    for label in term_labels:
        slug = language_term_slug(label)
        if slug:
            related = get_language_term(slug) or {}
            links.append({
                "label": label,
                "slug": slug,
                "hover_tip": str(related.get("one_liner") or related.get("policy_note") or label),
            })
    return links


def trap_name_from_slug(slug: str) -> str:
    for name, _ in POLICY_TRAPS:
        if slugify(name) == slug:
            return name
    return slug.replace("-", " ").title()


def enrich_trap_alert(name: str, description: str) -> dict:
    """Full trap alert payload for dashboard and glossary cross-reference."""
    slug = slugify(name)
    ctx = TRAP_GLOSSARY_CONTEXT.get(name, {})
    hover = str(ctx.get("hover") or description)
    meaning = str(ctx.get("meaning") or description)
    evidence = str(ctx.get("evidence") or "")
    language_terms = ctx.get("language_terms") or []
    if isinstance(language_terms, str):
        language_terms = [language_terms]
    related_modules = ctx.get("related_modules") or []
    if isinstance(related_modules, str):
        related_modules = [related_modules]
    glossary_slugs = ctx.get("glossary_slugs") or []
    if isinstance(glossary_slugs, str):
        glossary_slugs = [glossary_slugs]
    examples = ctx.get("examples") or []
    trap_row = _TRAP_BY_SLUG.get(slug, {})
    return {
        "name": name,
        "slug": slug,
        "description": description,
        "hover_tip": hover,
        "meaning": meaning,
        "evidence": evidence,
        "kind": "trap",
        "stages": trap_row.get("stages") or [],
        "language_links": _trap_language_links(list(language_terms)),
        "related_modules": list(related_modules),
        "module_links": _related_module_links(list(related_modules)),
        "glossary_slugs": list(glossary_slugs),
        "glossary_slug": slug,
        "insurer_angle": str(ctx.get("insurer_angle") or ""),
        "claim_tip": str(ctx.get("claim_tip") or ""),
        "example_quote": str(ctx.get("example_quote") or ""),
        "examples": [str(item) for item in examples],
    }


def policy_traps_list() -> list[dict]:
    return [enrich_trap_alert(name, desc) for name, desc in POLICY_TRAPS]


def relevant_policy_traps(stage: str, flags: set[str] | None = None) -> list[dict[str, str]]:
    """Return policy traps relevant to claim stage and intake flags."""
    flags = flags or set()
    names: list[str] = list(STAGE_TRAP_NAMES.get(stage, STAGE_TRAP_NAMES["preparing"]))
    for flag, extra in FLAG_TRAP_NAMES.items():
        if flag in flags:
            for name in extra:
                if name not in names:
                    names.append(name)
    return [
        enrich_trap_alert(name, desc)
        for name, desc in POLICY_TRAPS
        if name in names
    ]


def enrich_doctor_question(index: int, question: str, purpose: str) -> dict:
    """Full doctor-question payload for workspace table and glossary cross-reference."""
    slug = slugify(question)
    ctx = DOCTOR_QUESTION_CONTEXT.get(question, {})
    hover = str(ctx.get("hover") or purpose)
    meaning = str(ctx.get("meaning") or purpose)
    evidence = str(ctx.get("evidence") or "")
    language_terms = ctx.get("language_terms") or []
    if isinstance(language_terms, str):
        language_terms = [language_terms]
    related_modules = ctx.get("related_modules") or []
    if isinstance(related_modules, str):
        related_modules = [related_modules]
    glossary_slugs = ctx.get("glossary_slugs") or []
    if isinstance(glossary_slugs, str):
        glossary_slugs = [glossary_slugs]
    guidance = str(ctx.get("guidance") or "")
    return {
        "index": index,
        "question": question,
        "purpose": purpose,
        "slug": slug,
        "hover_tip": hover,
        "meaning": meaning,
        "guidance": guidance,
        "evidence": evidence,
        "kind": "doctor_question",
        "language_links": _trap_language_links(list(language_terms)),
        "related_modules": list(related_modules),
        "glossary_slugs": list(glossary_slugs),
        "glossary_slug": slug,
        "module_links": _related_module_links(list(related_modules)),
    }


def doctor_questionnaire() -> list[dict]:
    """Disability-test / doctor questions from product plan Section 5."""
    return [
        enrich_doctor_question(i + 1, q, p)
        for i, (q, p) in enumerate(DISABILITY_TEST_QUESTIONS)
    ]


_DOCTOR_QUESTION_BY_SLUG: dict[str, dict] = {
    slugify(q): {"question": q, "purpose": p, "index": i + 1}
    for i, (q, p) in enumerate(DISABILITY_TEST_QUESTIONS)
}


def get_doctor_question(slug: str) -> dict | None:
    row = _DOCTOR_QUESTION_BY_SLUG.get(slug)
    if not row:
        return None
    return enrich_doctor_question(row["index"], row["question"], row["purpose"])


def doctor_questions_glossary_entries() -> list[dict]:
    """Doctor questionnaire rows for resources glossary — synced with workspace table."""
    return [
        {
            "term": row["question"],
            "slug": row["slug"],
            "kind": "doctor_question",
            "meaning": row["meaning"],
            "purpose": row["purpose"],
            "evidence": row["evidence"],
            "hover_tip": row["hover_tip"],
            "index": row["index"],
        }
        for row in doctor_questionnaire()
    ]


_CORE_TERM_BY_SLUG: dict[str, dict] = {
    slugify(term): {
        "term": term,
        "slug": slugify(term),
        "meaning": meaning,
        "trap": trap,
        "evidence": evidence,
        "language_slug": language_term_slug(term),
    }
    for term, meaning, trap, evidence in CORE_POLICY_TERMS
}

_TRAP_BY_SLUG: dict[str, dict] = {
    slugify(name): {
        "name": name,
        "slug": slugify(name),
        "description": desc,
        "stages": [
            stage for stage, names in STAGE_TRAP_NAMES.items() if name in names
        ],
    }
    for name, desc in POLICY_TRAPS
}


def policy_terms_preview(limit: int = 20) -> list[dict[str, str]]:
    return [
        {
            "term": row["term"],
            "slug": row["slug"],
            "meaning": row["meaning"],
            "trap": row["trap"],
        }
        for row in list(_CORE_TERM_BY_SLUG.values())[:limit]
    ]


def core_policy_terms_full() -> list[dict]:
    return list(_CORE_TERM_BY_SLUG.values())


def get_core_policy_term(slug: str) -> dict | None:
    return _CORE_TERM_BY_SLUG.get(slug)


def link_trap_detail_text(text: str) -> list[dict[str, str]]:
    """Split trap-detail copy into segments with hover tips and resource xrefs."""
    from language_map import get_language_term, link_language_detail_text

    segments = link_language_detail_text(text)
    for seg in segments:
        if seg.get("type") != "link":
            continue
        if seg.get("link_kind") == "language" and seg.get("slug"):
            related = get_language_term(seg["slug"]) or {}
            seg["hover_tip"] = str(related.get("one_liner") or seg.get("hover_tip") or seg["label"])
    return segments


def trap_resource_xrefs(slug: str) -> list[dict[str, str]]:
    """ClaimBuddy resource chips for a policy-trap detail page."""
    from language_map import _trap_hover, get_confusion_pair, get_language_term

    own_occ = get_language_term("own-occupation") or {}
    material = get_language_term("material-duties") or {}
    functional = get_language_term("functional-capacity") or {}
    confusion = get_confusion_pair("job-title-material-duties") or {}

    specific: dict[str, list[dict[str, str]]] = {
        "job-title-trap": [
            {
                "label": "Job title ≠ Material duties",
                "link_kind": "confusion",
                "slug": "job-title-material-duties",
                "hover_tip": str(confusion.get("distinction") or confusion.get("claim_tip") or ""),
            },
            {
                "label": "Own occupation",
                "link_kind": "language",
                "slug": "own-occupation",
                "hover_tip": str(own_occ.get("one_liner") or own_occ.get("policy_note") or ""),
            },
            {
                "label": "Material duties",
                "link_kind": "language",
                "slug": "material-duties",
                "hover_tip": str(material.get("one_liner") or material.get("policy_note") or ""),
            },
            {
                "label": "Functional capacity",
                "link_kind": "language",
                "slug": "functional-capacity",
                "hover_tip": str(functional.get("one_liner") or functional.get("policy_note") or ""),
            },
            {
                "label": "Relevant occupation",
                "link_kind": "glossary",
                "slug": "what-is-the-relevant-occupation",
                "hover_tip": "Doctor question — define the actual role, not a generic title.",
            },
            {
                "label": "Diagnosis trap",
                "link_kind": "trap",
                "slug": "diagnosis-trap",
                "hover_tip": _trap_hover("Diagnosis trap"),
            },
        ],
    }

    shared = [
        {
            "label": "Policy traps",
            "link_kind": "traps",
            "slug": "",
            "hover_tip": "Twelve traps insurers use — hover names on your dashboard for quick summaries.",
        },
        {
            "label": "Language map",
            "link_kind": "glossary",
            "slug": "",
            "hover_tip": "Everyday, medical, functional, and policy language — linked in one ladder.",
        },
    ]
    return list(specific.get(slug) or []) + shared


def enrich_trap_for_detail(trap: dict) -> dict:
    """Linked segments, examples, and resource xrefs for trap detail pages."""
    from language_map import confusion_pair_slug, get_confusion_pair

    slug = trap.get("slug") or ""
    examples = trap.get("examples") or []
    confusion_pairs: list[dict] = []
    if slug == "job-title-trap":
        pair = get_confusion_pair("job-title-material-duties")
        if pair:
            confusion_pairs.append({**pair, "slug": "job-title-material-duties"})
    if slug == "pre-existing-trap":
        pair = get_confusion_pair("pre-existing-condition-date-of-absence")
        if pair:
            confusion_pairs.append({**pair, "slug": "pre-existing-condition-date-of-absence"})

    module_resource_links: list[dict[str, str | bool]] = []
    for mod in trap.get("module_links") or []:
        detail_slug = _MODULE_SLUGS.get(str(mod.get("label")), "")
        module_resource_links.append({
            "label": str(mod.get("label") or ""),
            "link_kind": "module",
            "slug": detail_slug,
            "endpoint": str(mod.get("endpoint") or ""),
            "claim_scoped": bool(mod.get("claim_scoped")),
            "fallback_endpoint": str(mod.get("fallback_endpoint") or ""),
            "hover_tip": f"Open {mod.get('label')} in your claim workspace.",
        })

    return {
        **trap,
        "meaning_segments": link_trap_detail_text(trap.get("meaning") or ""),
        "description_segments": link_trap_detail_text(trap.get("description") or ""),
        "evidence_segments": link_trap_detail_text(trap.get("evidence") or ""),
        "insurer_angle_segments": link_trap_detail_text(trap.get("insurer_angle") or ""),
        "claim_tip_segments": link_trap_detail_text(trap.get("claim_tip") or ""),
        "example_quote_segments": (
            link_trap_detail_text(trap["example_quote"]) if trap.get("example_quote") else None
        ),
        "examples_linked": [link_trap_detail_text(str(item)) for item in examples],
        "resource_xrefs": trap_resource_xrefs(slug) + module_resource_links,
        "confusion_pairs": confusion_pairs,
        "confusion_slug": confusion_pair_slug,
    }


def get_policy_trap(slug: str) -> dict | None:
    row = _TRAP_BY_SLUG.get(slug)
    if not row:
        return None
    return enrich_trap_for_detail(enrich_trap_alert(row["name"], row["description"]))


def trap_glossary_entries() -> list[dict]:
    """Policy traps as glossary rows — synced with dashboard alerts."""
    return [
        {
            "term": name,
            "slug": slugify(name),
            "kind": "trap",
            "meaning": str(TRAP_GLOSSARY_CONTEXT.get(name, {}).get("meaning") or desc),
            "trap": desc,
            "evidence": str(TRAP_GLOSSARY_CONTEXT.get(name, {}).get("evidence") or ""),
            "hover_tip": str(TRAP_GLOSSARY_CONTEXT.get(name, {}).get("hover") or desc),
        }
        for name, desc in POLICY_TRAPS
    ]


def glossary_entries_combined() -> dict[str, list[dict]]:
    """Policy terms, policy traps, and doctor questions for the resources glossary."""
    terms = [
        {**row, "kind": "term"}
        for row in core_policy_terms_full()
    ]
    return {
        "terms": terms,
        "traps": trap_glossary_entries(),
        "doctor_questions": doctor_questions_glossary_entries(),
        "checklist_items": policy_checklist_glossary_entries(),
    }


def get_glossary_entry(slug: str) -> dict | None:
    """Resolve a glossary slug to a policy term or policy trap entry."""
    core = get_core_policy_term(slug)
    if core:
        return {**core, "kind": "term"}
    trap = get_policy_trap(slug)
    if trap:
        return {
            **trap,
            "term": trap["name"],
            "kind": "trap",
            "trap": trap["description"],
        }
    doctor = get_doctor_question(slug)
    if doctor:
        return {
            "term": doctor["question"],
            "slug": doctor["slug"],
            "kind": "doctor_question",
            "meaning": doctor["meaning"],
            "purpose": doctor["purpose"],
            "guidance": doctor.get("guidance") or "",
            "trap": doctor["purpose"],
            "evidence": doctor["evidence"],
            "hover_tip": doctor["hover_tip"],
            "index": doctor["index"],
            "language_links": doctor.get("language_links") or [],
            "related_modules": doctor.get("related_modules") or [],
            "module_links": doctor.get("module_links") or [],
            "glossary_slugs": doctor.get("glossary_slugs") or [],
        }
    checklist = get_policy_checklist_item(slug)
    if checklist:
        return {
            "term": checklist["label"],
            "slug": checklist["slug"],
            "kind": "checklist_item",
            "meaning": checklist["meaning"],
            "guidance": checklist.get("guidance") or "",
            "trap": checklist["label"],
            "summary": checklist["label"],
            "evidence": checklist["evidence"],
            "hover_tip": checklist["hover_tip"],
            "key": checklist["key"],
            "language_links": checklist.get("language_links") or [],
            "related_modules": checklist.get("related_modules") or [],
            "module_links": checklist.get("module_links") or [],
            "glossary_slugs": checklist.get("glossary_slugs") or [],
        }
    return None


_MODULE_SLUGS = {
    "Guided intake": "guided-intake",
    "Document vault": "document-vault",
    "Policy reader": "policy-reader",
    "Functional-capacity builder": "functional-capacity-builder",
    "Evidence-gap detector": "evidence-gap-detector",
    "Rejection explainer": "rejection-explainer",
    "Access-request assistant": "access-request-assistant",
    "Claim-pack generator": "claim-pack-generator",
}

# Live workspace routes — claim_scoped endpoints need claim_id in url_for.
_MODULE_WORKSPACE: dict[str, dict[str, str | bool]] = {
    "Guided intake": {"endpoint": "edit_claim", "claim_scoped": True, "fallback_endpoint": "intake"},
    "Document vault": {"endpoint": "vault", "claim_scoped": True},
    "Policy reader": {"endpoint": "policy_reader", "claim_scoped": True},
    "Functional-capacity builder": {"endpoint": "functional_capacity", "claim_scoped": True},
    "Evidence-gap detector": {"endpoint": "gaps", "claim_scoped": True},
    "Access-request assistant": {"endpoint": "letters", "claim_scoped": True},
    "Claim-pack generator": {"endpoint": "pack", "claim_scoped": True},
    "Rejection explainer": {"endpoint": "rejection_explainer", "claim_scoped": True},
}


def modules_with_status(claim_modules: dict[str, bool] | None = None) -> list[dict]:
    """Map MVP modules to live workspace features."""
    claim_modules = claim_modules or {}
    live = {
        "Guided intake": True,
        "Document vault": True,
        "Evidence-gap detector": True,
        "Access-request assistant": True,
        "Claim-pack generator": True,
        "Functional-capacity builder": True,
        "Policy reader": True,
        "Rejection explainer": True,
    }
    rows = []
    for name, inputs, outputs in MVP_MODULES_TABLE:
        slug = _MODULE_SLUGS.get(name, name.lower().replace(" ", "-"))
        detail = MVP_MODULE_DETAILS.get(slug, {})
        workspace = _MODULE_WORKSPACE.get(name, {})
        rows.append({
            "name": name,
            "inputs": inputs,
            "outputs": outputs,
            "live": live.get(name, False),
            "docs_slug": slug,
            "summary": detail.get("purpose", ""),
            "workspace_endpoint": workspace.get("endpoint"),
            "workspace_fallback_endpoint": workspace.get("fallback_endpoint"),
            "workspace_claim_scoped": bool(workspace.get("claim_scoped")),
        })
    return rows
