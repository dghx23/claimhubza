"""Fallback stand-in for the (never committed) claimguard-site content data.

The real content lives in a sibling ``claimguard-site`` project that isn't
part of this repository, so ``knowledge.py`` couldn't import it anywhere
this app is deployed. These are empty placeholders with the same shapes so
the app boots instead of crashing; the pages that render this content will
simply show nothing until the real tables are restored.
"""

from __future__ import annotations

CONSTRUCTION_FIELDS_TABLE: list[tuple[str, str]] = []

# Seeded from the language map + trap glossary so /reference is a real catalog
# even without the sibling claimguard-site project.
CORE_POLICY_TERMS: list[tuple[str, str, str, str]] = [
    (
        "Disability",
        "The policy outcome if you meet the disability test — usually inability to perform material duties of your own occupation.",
        "Diagnosis trap — a certificate label is not the test.",
        "Duty-impact matrix, occupation profile, treating-doctor answers to the policy test.",
    ),
    (
        "Waiting period",
        "Continuous incapacity that must run before benefits start — often measured from Date of Absence.",
        "Date trap — mixing sick days with DOA resets or fails the period.",
        "Absence records, sick notes covering the full period, insurer DOA.",
    ),
    (
        "Date of Absence",
        "The date the policy treats incapacity as having begun — often not the first sick day.",
        "Date trap — employer, doctor, and insurer frequently pick different dates.",
        "Separate fields for symptom onset, first sick note, your DOA, insurer DOA.",
    ),
    (
        "Incapacity",
        "Ongoing inability to perform insured duties under policy rules — not the same as HR sick leave.",
        "Illness vs incapacity confusion.",
        "Functional-capacity statement mapped to material duties.",
    ),
    (
        "Disablement",
        "The process or state of becoming unable to function as before — in COIDA and some funds a rated percentage; in everyday talk a gradual collapse of capacity.",
        "Not the same as the policy disability test, and not the same as a discrimination-law 'person with a disability'.",
        "Policy wording, COIDA vs IP distinction, ICF capacity vs performance.",
    ),
    (
        "Capacity vs performance",
        "WHO-ICF: capacity is what you can do unaided in a standard setting; performance is what you actually do with treatment, aids, and environment.",
        "Mitigated-state trap — IP usually assesses treated performance; ADA/UK/EEA guidance often looks at the unmitigated baseline.",
        "State which axis the assessor used, and keep both scores if they differ.",
    ),
    (
        "Own occupation",
        "Initial-period test: can you do the material duties of your actual role, not any job.",
        "Job-title trap — generic titles understate the role.",
        "Job spec, duty list, employer confirmation.",
    ),
    (
        "Cover start",
        "When cover commenced — compared to symptom history and pre-existing look-back.",
        "Pre-existing trap.",
        "Member certificate, scheme start date.",
    ),
    (
        "Total vs partial disability",
        "Two policy doors: total usually means you cannot perform the insured occupation; "
        "partial / residual means some work continues and a formula (earnings or hours drop) "
        "pays a proportion of the total benefit. Not a medical severity score.",
        "Threshold-shift trap if the test changes after the Initial Period; also using leftover "
        "tasks to deny total without applying the residual clause.",
        "Pre-disability vs current payslips and hours, duty list (stopped vs continues), residual clause.",
    ),
]

DISABILITY_TEST_QUESTIONS: list[tuple[str, str]] = [
    ("Which test applies now?", "Initial Period is usually own-occupation; Extended Period may shift."),
    ("What is the relevant occupation?", "Define the actual role — not a generic title."),
    ("What are the material duties?", "Separate core duties from incidental tasks."),
    ("What medical events changed capacity?", "Onset, deterioration, treatment, side-effects."),
    ("How does illness affect work function?", "Map symptoms to duties, stamina, and reliability."),
    ("Was incapacity continuous through waiting period?", "Breaks in incapacity can reset the clock."),
    ("What evidence is missing?", "Name the gap and the holder."),
    ("Who controls the missing evidence?", "Employer, insurer, hospital, specialist."),
    ("What is the insurer's actual reason?", "Quoted clause vs everyday language in the letter."),
    ("What would cure the issue?", "Specific record, specialist answer, or duty-impact line."),
]

EVIDENCE_DOMAINS_TABLE: list[tuple[str, str, str]] = [
    ("Policy", "Wording, schedule, member certificate, guides", "What test actually applies"),
    ("Employment", "Job spec, duties, payslips, absence, employer statement", "Role and earnings as lived"),
    ("Medical", "Certificates, specialist reports, hospital notes, scripts", "Health facts, not the policy test"),
    ("Functional", "Duty-impact matrix, OT/FC reports, stamina evidence", "Bridge from symptoms to duties"),
    ("Claim handling", "Forms, notices, rejection, claim-file notes", "Process and stated grounds"),
    ("Record access", "PAIA/POPIA requests, employer/insurer disclosures", "Files you do not hold"),
]

MVP_MODULES_TABLE: list[tuple[str, str, str]] = [
    ("Guided intake", "live", "Profile fields the compiler did not extract"),
    ("Document vault", "live", "Inbox / classify / store"),
    ("Policy reader", "live", "Clause scan of uploaded wording"),
    ("Functional-capacity builder", "live", "Symptom → duty matrix"),
    ("Evidence-gap detector", "live", "Missing items + holders"),
    ("Rejection explainer", "live", "Grounds from a rejection letter"),
    ("Access-request assistant", "live", "Draft employer/insurer letters"),
    ("Claim-pack generator", "live", "Numbered Markdown pack"),
]

POLICY_TRAPS: list[tuple[str, str]] = [
    ("Diagnosis trap", "A diagnosis label alone does not prove you cannot perform material duties."),
    ("Job-title trap", "Job title may understate workload, pressure, travel, supervision, and error consequences."),
    ("Date trap", "DOA, notice, submission, complete claim, waiting period, and rejection dates are rarely the same day."),
    ("Threshold-shift trap", "The standard at submission may be broader than the standard applied at rejection."),
    ("Policy-vs-guide trap", "HR emails and claim guides may use broader language than binding policy wording."),
    ("Employer-record trap", "Payroll, absence records, and employer statements may be decisive but sit with HR — not you."),
    ("Specialist-evidence trap", "Missing specialist evidence is unsafe if you were never told what, why, who obtains it, or who pays."),
    ("Gross-benefit trap", "Benefit % is not final until earnings definition, caps, offsets, and tax are checked."),
    ("Pre-existing trap", "An old diagnosis is not the same as proving a pre-existing exclusion under your policy dates."),
    ("Appeal-story trap", "Emotional narrative should become a structured issue matrix with evidence and remedies."),
    (
        "Mitigated-state trap",
        "Discrimination law often tests function WITHOUT treatment or aids; income-protection policies usually test WITH ongoing treatment. Mixing those tests is how a claim is argued as if the person is 'fine on meds'.",
    ),
]

TARGET_USERS_TABLE: list[tuple[str, str]] = []
TERM_CARD_FIELDS_TABLE: list[tuple[str, str]] = []
TERM_CARD_PIPELINE: list[tuple[str, str]] = []
WORKFLOW_STEPS: list[tuple[str, str]] = [
    ("Symptoms begin", "Health changes; work still attempted or reduced."),
    ("Work impact", "Material duties start to fail — often the true Date of Absence."),
    ("Notice", "Employer and/or insurer notified. Not the same as a complete claim."),
    ("Waiting period", "Continuous incapacity must run; breaks can reset the clock."),
    ("Assessment", "Insurer applies the policy test to the file they hold."),
    ("Rejection", "Grounds stated — often dates, duties, or missing specialist evidence."),
    ("Internal review", "Issue-by-issue response with a cure plan."),
    ("Ombud / NFO", "Complaint route with its own deadline."),
    ("Record access", "PAIA/POPIA for files held by employer or insurer."),
]
