"""NFO and AFCA guidance and published holdings used by the Library.

Curated — not a live ingest of every determination. Core ZA / Core AU
record the source feeds. Product pages consume this module.
"""

from __future__ import annotations

from typing import Any

from term_slugs import slugify

# Topics attach to language-map terms via guidance_topics.
TOPIC_PREEXISTING = "pre-existing"
TOPIC_TOTAL_PARTIAL = "total-partial"


PRECEDENTS: list[dict[str, Any]] = [
    {
        "slug": "nfo-cr403-pre-existing",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR403",
        "year": "2024",
        "title": "Pre-existing condition clause — onus and look-back proof",
        "url": "https://nfosa.co.za/cr403-pre-existing-condition-clause-in-disability-benefit/",
        "topics": [TOPIC_PREEXISTING],
        "related_terms": [
            "Pre-existing condition",
            "Cover start",
            "Date of Absence",
            "Diagnosis",
        ],
        "outcome": "Claim paid after the office put the insurer to proof.",
        "facts": (
            "A long-haul truck driver joined group risk cover on 1 November 2016. "
            "Date of disability 1 July 2017: anterolisthesis and spondylosis with "
            "left-leg weakness. The insurer declined on a six-month look-back, pointing "
            "at a 2003 train accident and a later doctor’s line that he had had chronic "
            "lower-back pain ‘since 2003’."
        ),
        "holding": (
            "The insurer must prove, on a balance of probabilities, both that the "
            "look-back condition existed in the contractual window and that it caused "
            "the disablement. A historic injury and a broad ‘chronic since 2003’ "
            "sentence are not enough. First consultation in the file was 8 March 2017; "
            "a June 2016 heavy-vehicle medical had given a clean bill of health; the "
            "leg weakness the insurer relied on started in 2017, after cover."
        ),
        "practice": (
            "Ask for contemporaneous notes in the look-back months — not a later "
            "summary. Capture fitness-to-drive / occupational-health clearances just "
            "before cover. Separate the old injury from the symptoms that actually "
            "stopped the job."
        ),
    },
    {
        "slug": "nfo-cr356-pre-existing",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR356",
        "year": "2014",
        "title": "Two-limb pre-existing exclusion — look-back and first twelve months",
        "url": "https://nfosa.co.za/cr356-interpretation-insurance-policy-contract/",
        "topics": [TOPIC_PREEXISTING],
        "related_terms": [
            "Pre-existing condition",
            "Cover start",
            "Date of Absence",
            "Disability",
        ],
        "outcome": "Insurer accepted the office’s reading and paid.",
        "facts": (
            "Group disability income. Entry 1 February 2012. Cognitive and balance "
            "symptoms were already being investigated in the six months before entry. "
            "He was advised to stop work on 4 February 2013 and diagnosed with senile "
            "dementia on 20 February 2013 — just after the first twelve months of cover."
        ),
        "holding": (
            "Typical South African group wording is conjunctive. The insurer needed "
            "(a) knowledge, diagnosis, treatment or symptoms of the claiming condition "
            "in the six months before entry, AND (b) disablement in the first twelve "
            "months after entry. Limb (a) was met; limb (b) was not. Symptoms in the "
            "look-back do not keep the exclusion alive once disablement falls outside "
            "the first year."
        ),
        "practice": (
            "Read the clause as two clocks, not one story. Date of disablement is the "
            "second clock — often last day able to perform duties, not first symptom "
            "and not the diagnosis date. A diagnosis after month twelve can still "
            "describe a disablement that started earlier; pin the duty-stop date."
        ),
    },
    {
        "slug": "nfo-cr351-causation",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR351",
        "year": "2014",
        "title": "Pre-existing exclusion — proximate cause, not every historic diagnosis",
        "url": "https://nfosa.co.za/category/topics-cases/page/9/",
        "topics": [TOPIC_PREEXISTING],
        "related_terms": ["Pre-existing condition", "Diagnosis", "Illness"],
        "outcome": "Office distinguished the pre-existing cardiac history from later cancer as the cause of death.",
        "facts": (
            "Credit life. Pre-existing cardiac history. The insured later developed "
            "cancer diagnosed after cover. The insurer argued the pre-existing "
            "conditions directly or indirectly caused death."
        ),
        "holding": (
            "The exclusion turns on whether the pre-existing condition caused the "
            "claim event, not on whether any old diagnosis exists. Medical evidence "
            "at cancer diagnosis recorded no cardiac involvement. Historic disease "
            "in the background is not automatically ‘directly or indirectly’ the cause."
        ),
        "practice": (
            "When the file has two conditions, build a causation map: what stopped "
            "work (or caused death), when, and which treating notes say so. Do not "
            "let a disclosed or recorded history swallow a new post-cover event."
        ),
    },
    {
        "slug": "nfo-cr72-part-time",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR72",
        "year": "2005",
        "title": "Total disability — part-time capacity is not automatically ‘not total’",
        "url": "https://nfosa.co.za/cr72-disability-claim-whether-complainant-can-be-considered-totally-disabled-if-he-is-capable-of-performing-a-part-time-occupation-only/",
        "topics": [TOPIC_TOTAL_PARTIAL],
        "related_terms": [
            "Total vs partial disability",
            "Own occupation",
            "Material duties",
            "Functional capacity",
        ],
        "outcome": "Insurer made an ex gratia offer of half the claim after ambiguous handling.",
        "facts": (
            "Clerical occupation. Severe sciatica. An occupational therapist said "
            "that even with pain-management and ergonomic changes he could probably "
            "only work part-time. The insurer treated leftover capacity as defeating "
            "total disability."
        ),
        "holding": (
            "The useful question is whether, in normal times and most places, an "
            "employer would consider the person capable of playing a worthwhile part "
            "in the business — performing the substantial and material clerical duties "
            "with reasonable regularity and continuity — and would pay more than a "
            "nominal gain. Part-time leftovers are not, by themselves, the occupation."
        ),
        "practice": (
            "If the insurer points at two hours of email, ask whether that is a "
            "worthwhile, regular performance of material duties for real pay. Capture "
            "unreliability: leaving early, unpredictable pain, days that cannot be "
            "rostered."
        ),
    },
    {
        "slug": "nfo-cr276-partial",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR276",
        "year": "2009",
        "title": "Partial permanent incapacity — residual other work is not the insured occupation",
        "url": "https://nfosa.co.za/cr276-disability-disability-partial-permanent-incapacity-claim-declined/",
        "topics": [TOPIC_TOTAL_PARTIAL],
        "related_terms": [
            "Total vs partial disability",
            "Own occupation",
            "Material duties",
        ],
        "outcome": "Provisional ruling: 20% partial permanent incapacity benefit; insurer abided.",
        "facts": (
            "Attorney with severe IBS claimed partial permanent incapacity. He was "
            "doing a ‘token’ sheriff role. The insurer stacked technical defences "
            "(late submission, non-disclosure, termination) and disputed the merits."
        ),
        "holding": (
            "The sheriff work was not the professional duties he trained for as an "
            "attorney, was not full-time, and was only residual income. He could not "
            "carry out attorney duties with regularity; a limited, low-stress remnant "
            "might remain. Impact was significant but assessed at 20% partial, not "
            "a nil claim and not a 50% scaling on the gastroenterologist’s suggestion "
            "alone."
        ),
        "practice": (
            "Name the occupation the policy actually insured. A stripped-down or "
            "unrelated job used to stay occupied is evidence of residual function, "
            "not proof that own-occupation duties continue. Partial percentages in "
            "lump-sum products are a different door from IP residual formulae."
        ),
    },
    {
        "slug": "nfo-cr259-own-occupation",
        "forum": "NFO",
        "forum_label": "National Financial Ombud (South Africa)",
        "jurisdiction": "za",
        "kind": "case",
        "citation": "CR259",
        "year": "2009",
        "title": "Total under own occupation — employing others to do the labour",
        "url": "https://nfosa.co.za/cr259-disability-insured-running-a-business-in-which-he-contributed-70-labour/",
        "topics": [TOPIC_TOTAL_PARTIAL],
        "related_terms": [
            "Total vs partial disability",
            "Own occupation",
            "Material duties",
        ],
        "outcome": "Insurer accepted total and permanent incapacity on the occupational definition.",
        "facts": (
            "Back injury. The insured kept the business running only by employing "
            "people to do the manual work he used to contribute (about 70% labour). "
            "The insurer treated continuation of the business as capacity."
        ),
        "holding": (
            "Keeping a business alive by substituting other people’s labour is not "
            "performing the insured occupation. On the policy definition he was "
            "totally and permanently incapacitated. (A separate occupation-change "
            "notification clause still mattered for prejudice.)"
        ),
        "practice": (
            "If the person ‘still has a company’, list who now does each material "
            "duty. Ownership or supervision is not the labour the wording insured "
            "unless the occupation was already managerial."
        ),
    },
    {
        "slug": "afca-s47-pre-existing",
        "forum": "AFCA",
        "forum_label": "Australian Financial Complaints Authority",
        "jurisdiction": "au",
        "kind": "approach",
        "citation": "AFCA Approach — ICA s 47",
        "year": "2024",
        "title": "Section 47: awareness of a pre-existing condition, not the diagnosis label",
        "url": "https://www.afca.org.au/media/594/download",
        "topics": [TOPIC_PREEXISTING],
        "related_terms": [
            "Pre-existing condition",
            "Cover start",
            "Diagnosis",
            "Symptom",
        ],
        "outcome": "Approach document — applied in published determinations.",
        "facts": (
            "Insurance Contracts Act 1984 (Cth) s 47 limits an insurer’s use of a "
            "pre-existing condition exclusion. AFCA’s worked examples include a life "
            "policy where a brain tumour was excised days after inception: there was "
            "no formal diagnosis at application, but GP review, a same-day CT, and "
            "surgery the next day meant a reasonable person would have been aware "
            "of a serious sickness."
        ),
        "holding": (
            "If, before the contract, the consumer was not aware of the condition "
            "and a reasonable person in those circumstances could not be expected "
            "to have been aware of it, s 47 stops the exclusion. Awareness sits "
            "between a stray symptom and a stamped diagnosis: consultations, "
            "investigations, and contemporaneous GP notes carry the weight. Later "
            "recollection that ‘it was nothing’ is often discounted. Awareness of "
            "the condition at any time before entry defeats s 47, even if the person "
            "reasonably believed they no longer had it."
        ),
        "practice": (
            "Build a pre-inception window from the records, not from the claim form. "
            "s 47 is not a duty-of-disclosure fight (that is ICA s 29 / s 21 / "
            "reasonable-care not to misrepresent). Keep exclusion and non-disclosure "
            "as separate issue cards. Super automatic cover often uses a 12-month "
            "pre-existing limitation — still read the PDS, and still test awareness."
        ),
    },
    {
        "slug": "afca-life-nondisclosure",
        "forum": "AFCA",
        "forum_label": "Australian Financial Complaints Authority",
        "jurisdiction": "au",
        "kind": "approach",
        "citation": "AFCA Approach — life insurance non-disclosure",
        "year": "2025",
        "title": "Non-disclosure remedies are not a substitute pre-existing clause",
        "url": "https://www.afca.org.au/media/2077/download",
        "topics": [TOPIC_PREEXISTING],
        "related_terms": ["Pre-existing condition", "Cover start"],
        "outcome": "Approach document — ICA s 29 variation is a different tool from an exclusion.",
        "facts": (
            "Insurers sometimes decline a claim on a pre-existing story and, in the "
            "same letter, try to vary or avoid the contract for non-disclosure or "
            "misrepresentation, including a retrospective mental-health exclusion."
        ),
        "holding": (
            "A s 29(6) variation must put the insurer in the position a reasonable "
            "and prudent insurer would have been in at entry. AFCA may narrow or "
            "strip a retrospective exclusion that other prudent insurers would not "
            "have applied. Declining the claim and varying the contract are two "
            "decisions; each needs its own proof. An exclusion that does not cover "
            "the claimed condition does not save a bad variation."
        ),
        "practice": (
            "If the letter mixes ‘pre-existing’, ‘you didn’t tell us’, and ‘we have "
            "added an exclusion from day one’, split the grounds. Ask what a "
            "prudent insurer would actually have done with the omitted fact."
        ),
    },
    {
        "slug": "afca-ip-total-partial-wording",
        "forum": "AFCA",
        "forum_label": "Australian Financial Complaints Authority",
        "jurisdiction": "au",
        "kind": "approach",
        "citation": "AFCA published IP determinations",
        "year": "2024–2026",
        "title": "Total and partial are separate benefits — AFCA applies the PDS as written",
        "url": "https://my.afca.org.au/searchpublisheddecisions/",
        "topics": [TOPIC_TOTAL_PARTIAL],
        "related_terms": [
            "Total vs partial disability",
            "Own occupation",
            "Material duties",
            "Waiting period",
        ],
        "outcome": "Recurring pattern across published income-protection determinations.",
        "facts": (
            "Retail and group IP product disclosure statements that AFCA reproduces "
            "in determinations typically split Total Disability and Partial "
            "(or residual) Disability. Common retail patterns include a 10-hour "
            "week threshold, an important-duties test, and a residual formula "
            "(A − B) / A × insured monthly benefit. Some wordings require a stretch "
            "of total disablement inside the waiting period before partial can pay. "
            "Offsets and ‘income you could reasonably earn’ clauses sit on top."
        ),
        "holding": (
            "AFCA does not grade medical severity as ‘total’ or ‘partial’. It asks "
            "which definition the person met in each month: hours actually worked, "
            "important income-producing duties, and earnings against pre-disability "
            "income. Working more than the hours threshold usually takes the file "
            "out of total and into partial — if the earnings drop and duty test are "
            "also met. Not working, but still able to do the important duties, fails "
            "total. A graded return is often residual, not recovery and not a failed "
            "total claim. Where the PDS deems a ≤10-hour week to be a 100% loss, "
            "AFCA applies that deeming."
        ),
        "practice": (
            "Export hours and pay for the same periods the PDS uses. List important "
            "duties that generate income (some wordings use a 20% income-producing "
            "duty). Do not hide two days of work; do not accept ‘you sent email’ as "
            "the occupation. Check whether partial needs total days in the waiting "
            "period first."
        ),
    },
]


GUIDES: list[dict[str, Any]] = [
    {
        "slug": "za-pre-existing-guidance",
        "jurisdiction": "za",
        "jurisdiction_label": "South Africa",
        "forum": "NFO",
        "topic": TOPIC_PREEXISTING,
        "title": "South Africa — how pre-existing exclusions usually work",
        "summary": (
            "Group IP in South Africa is often a two-limb, time-limited exclusion. "
            "The insurer carries the onus. Historic labels are not the test."
        ),
        "paragraphs": [
            (
                "Most South African group income-protection and lump-sum disability "
                "wordings do not exclude every illness you ever had. They exclude "
                "disablement that is caused by a condition you knew about, were "
                "treated for, or had symptoms of in a short look-back (commonly six "
                "months before entry), and — on many group contracts — only if that "
                "disablement happens in the first twelve months of cover (NFO CR356)."
            ),
            (
                "Retail policies and credit life can be harsher: some exclude a "
                "pre-existing condition for the life of the benefit, or use ‘directly "
                "or indirectly’. Even then the NFO still asks for proof of the "
                "condition in the defined window and a causal link to the claim event "
                "(CR403, CR351). Policyholder Protection Rules require reasonable "
                "steps to gather information and fair treatment — asserting an old "
                "script without investigating post-cover change is the usual fight."
            ),
            (
                "Underwriting path matters. If the insurer asked medical questions "
                "and issued cover, a later ‘pre-existing’ decline may really be a "
                "non-disclosure argument, which has its own rules. If cover was "
                "automatic (fund / union) with no questions, the exclusion clause "
                "is doing the underwriting after the fact — read it strictly."
            ),
        ],
        "limbs": [
            {
                "label": "Limb 1 — look-back",
                "text": (
                    "Did the person know of, receive advice or treatment for, or have "
                    "symptoms of the claiming condition in the look-back months before "
                    "cover? Contemporaneous notes, not a later narrative."
                ),
            },
            {
                "label": "Limb 2 — disablement window",
                "text": (
                    "On typical group wording: did disablement occur in the first "
                    "twelve months after entry? If duties stopped after that window, "
                    "the exclusion often falls away even if limb 1 is true."
                ),
            },
            {
                "label": "Limb 3 — causation",
                "text": (
                    "Was the disablement caused by that look-back condition, or by a "
                    "new post-cover event / material deterioration that the clause "
                    "does not capture? Historic injury ≠ proof (CR403)."
                ),
            },
            {
                "label": "Onus",
                "text": (
                    "The insurer must prove the exclusion on a balance of probabilities. "
                    "Gaps in the look-back file are the insurer’s problem if it could "
                    "have obtained the notes (CR403)."
                ),
            },
        ],
        "dispute": "Internal review at the insurer, then the NFO Life Insurance Division (free).",
    },
    {
        "slug": "au-pre-existing-guidance",
        "jurisdiction": "au",
        "jurisdiction_label": "Australia",
        "forum": "AFCA",
        "topic": TOPIC_PREEXISTING,
        "title": "Australia — PDS exclusion, s 47 awareness, and disclosure",
        "summary": (
            "Three different tools: the PDS pre-existing wording, Insurance Contracts "
            "Act s 47 (awareness), and non-disclosure / misrepresentation remedies."
        ),
        "paragraphs": [
            (
                "Retail life and IP policies define ‘pre-existing’ in the PDS — often "
                "awareness, symptoms a reasonable person would notice, treatment, "
                "investigation, or a chronic illness in a 12-month (sometimes longer) "
                "window. Group cover inside super frequently applies a 12-month "
                "pre-existing limitation on automatic acceptance. AFCA applies the "
                "PDS words, then tests whether the Act stops the insurer using them."
            ),
            (
                "Section 47 ICA: the insurer cannot rely on a pre-existing exclusion "
                "if, before entry, the person was not aware of the condition and a "
                "reasonable person in those circumstances could not be expected to "
                "have been aware of it. AFCA’s approach is that awareness is not the "
                "diagnosis stamp and not a fleeting ache — GP notes, referrals, and "
                "scans in the pre-inception window decide it."
            ),
            (
                "A different fight is duty of disclosure (older contracts) or the duty "
                "to take reasonable care not to make a misrepresentation (from 5 "
                "October 2021 for consumer contracts). Remedies live in ICA s 29: "
                "avoid, vary, or reduce. AFCA will not let a retrospective exclusion "
                "go further than a prudent insurer would have gone. Do not collapse "
                "these into one ‘they said it was pre-existing’ paragraph."
            ),
        ],
        "limbs": [
            {
                "label": "PDS definition",
                "text": (
                    "Does the claimed condition meet the policy’s own definition "
                    "(treatment, investigation, reasonable-person symptoms, chronic "
                    "illness) in the stated window?"
                ),
            },
            {
                "label": "s 47 awareness",
                "text": (
                    "Even if the PDS is met, was the person actually aware, and would "
                    "a reasonable person have been aware, of that condition before "
                    "the contract? If both answers are no, the exclusion is blocked."
                ),
            },
            {
                "label": "Causation",
                "text": (
                    "Is the claim ‘arising from’ that condition, or from a new injury "
                    "or illness after cover? Aggravation clauses are common — read "
                    "them; they are not automatic."
                ),
            },
            {
                "label": "Disclosure / s 29",
                "text": (
                    "If the insurer is really saying ‘you didn’t tell us’, that is not "
                    "the exclusion. It is a separate remedy with its own onus and "
                    "time limits."
                ),
            },
        ],
        "dispute": "Internal dispute resolution (RG 271), then AFCA. Super claims often need the trustee as well as the insurer.",
    },
    {
        "slug": "za-total-partial-guidance",
        "jurisdiction": "za",
        "jurisdiction_label": "South Africa",
        "forum": "NFO",
        "topic": TOPIC_TOTAL_PARTIAL,
        "title": "South Africa — total, partial, and leftover tasks",
        "summary": (
            "Own-occupation total is about material duties with continuity, not a "
            "medical grade. Partial is a different benefit (or a percentage of a "
            "lump sum), not a consolation prize for a failed total claim."
        ),
        "paragraphs": [
            (
                "South African group IP usually pays a monthly benefit if, after the "
                "waiting period, you cannot perform the material and substantial "
                "duties of your own occupation with reasonable continuity (initial "
                "period, often 12 or 24 months). Later the test may shift to any "
                "or suited occupation. ‘Partial’ on a lump-sum disability rider is "
                "often a scheduled percentage of impairment or occupational "
                "incapacity (see NFO CR276) — a different product from IP residual."
            ),
            (
                "The NFO has repeatedly refused to treat leftover or substituted work "
                "as the occupation. CR72: part-time clerical leftovers are not a "
                "worthwhile, regular performance of material duties. CR259: employing "
                "others to do the labour while the business continues can still be "
                "total. CR276: a token second job is residual income, not attorney "
                "duties. Light duties and ‘still a director’ need a duty list."
            ),
            (
                "Some group contracts have an explicit partial / proportionate income "
                "benefit when you return at reduced earnings. If they do not, the "
                "insurer may argue that any work ends total — that is a wording fight, "
                "not a medical one. Waiting period, offsets (including other disability "
                "income), and employer boarding are separate clocks."
            ),
        ],
        "limbs": [
            {
                "label": "Own-occupation total",
                "text": (
                    "Cannot perform material and substantial duties of the job you "
                    "actually did, with reasonable continuity — not ‘any desk work’."
                ),
            },
            {
                "label": "Leftover tasks",
                "text": (
                    "Would an employer pay more than a nominal amount for this as "
                    "the real job, regularly? If not, it is usually still total "
                    "(CR72), unless the wording has a residual clause."
                ),
            },
            {
                "label": "Partial / proportionate",
                "text": (
                    "Only if the policy names it. Then capture pre-disability versus "
                    "current earnings. Lump-sum ‘partial permanent incapacity’ is a "
                    "percentage assessment, not an IP formula."
                ),
            },
            {
                "label": "Threshold shift",
                "text": (
                    "Initial own occupation may later become any / suited occupation. "
                    "Date that shift. A graded return in month 14 can be judged on "
                    "a harder test than month 3."
                ),
            },
        ],
        "dispute": "Insurer review, then NFO Life Insurance Division. Pension Funds Adjudicator if the decision-maker is a fund.",
    },
    {
        "slug": "au-total-partial-guidance",
        "jurisdiction": "au",
        "jurisdiction_label": "Australia",
        "forum": "AFCA",
        "topic": TOPIC_TOTAL_PARTIAL,
        "title": "Australia — total vs partial as two PDS benefits",
        "summary": (
            "AFCA applies hours, important duties, and the residual formula in the "
            "PDS. Medical severity is not the scale."
        ),
        "paragraphs": [
            (
                "Australian retail IP almost always defines Total Disability and "
                "Partial Disability separately. A widely used pattern (reproduced in "
                "AFCA determinations) is: total if, solely due to sickness or injury, "
                "you are not working more than 10 hours a week in your usual or a "
                "gainful occupation and cannot perform the important income-producing "
                "duties for more than 10 hours; or you are not working at all and "
                "cannot perform one or more important duties. Partial if you are "
                "working more than that hours threshold (or in reduced capacity) and "
                "earnings are below pre-disability income, under regular medical care."
            ),
            (
                "The partial amount is typically (A − B) / A × C, where A is "
                "pre-disability (or pre-disablement) income, B is income while "
                "partially disabled, and C is the insured monthly benefit. Some "
                "Premier-style wordings deem a ≤10-hour week to be a 100% loss so "
                "the total benefit still pays. B may be replaced by what the insurer "
                "says you could reasonably earn if you are not working to capacity. "
                "Offsets (sick leave, workers compensation, other IP) still apply."
            ),
            (
                "Waiting periods often require a block of total disablement (for "
                "example 14 of the first 19 days, or 7 of 12) before partial can "
                "accrue. Returning to work during the waiting period can reset or "
                "complicate that. After the waiting period, AFCA looks month by "
                "month: this month total, next month partial, a later month off "
                "claim if earnings recover. A graded return is the classic partial "
                "file — not evidence that you were never disabled."
            ),
        ],
        "limbs": [
            {
                "label": "Hours threshold",
                "text": (
                    "Count hours in the usual or any gainful occupation. Crossing "
                    "the PDS threshold (often 10 a week) usually moves the file from "
                    "total to partial."
                ),
            },
            {
                "label": "Important duties",
                "text": (
                    "Not the job title. Duties that produce income — some group "
                    "wordings say a duty generating 20% or more of monthly income. "
                    "Unable to do one such duty can still be total if you are not working."
                ),
            },
            {
                "label": "Residual formula",
                "text": (
                    "(Pre-disability income − current income) ÷ pre-disability income "
                    "× monthly benefit. Minimum drop (often 20%) appears on some "
                    "contracts. Same currency, same period."
                ),
            },
            {
                "label": "Capable of earning",
                "text": (
                    "If you are not working to capacity for reasons other than "
                    "sickness or injury, some PDS replace actual earnings with a "
                    "reasonable estimate. That is a medical and vocational argument, "
                    "not a payslip."
                ),
            },
        ],
        "dispute": "IDR with the insurer (and trustee if the cover sits in super), then AFCA.",
    },
]


def _with_slugs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        item.setdefault("slug", slugify(str(item.get("citation") or item.get("title") or "item")))
        out.append(item)
    return out


PRECEDENTS = _with_slugs(PRECEDENTS)
GUIDES = _with_slugs(GUIDES)

_PRECEDENT_BY_SLUG = {p["slug"]: p for p in PRECEDENTS}
_GUIDE_BY_SLUG = {g["slug"]: g for g in GUIDES}


def list_precedents(*, topic: str | None = None, jurisdiction: str | None = None) -> list[dict[str, Any]]:
    rows = PRECEDENTS
    if topic:
        rows = [p for p in rows if topic in (p.get("topics") or [])]
    if jurisdiction:
        rows = [p for p in rows if p.get("jurisdiction") == jurisdiction]
    return rows


def list_guides(*, topic: str | None = None, jurisdiction: str | None = None) -> list[dict[str, Any]]:
    rows = GUIDES
    if topic:
        rows = [g for g in rows if g.get("topic") == topic]
    if jurisdiction:
        rows = [g for g in rows if g.get("jurisdiction") == jurisdiction]
    return rows


def get_precedent(slug: str) -> dict[str, Any] | None:
    return _PRECEDENT_BY_SLUG.get(slug)


def get_guide(slug: str) -> dict[str, Any] | None:
    return _GUIDE_BY_SLUG.get(slug)


def get_guidance_entry(slug: str) -> dict[str, Any] | None:
    return get_precedent(slug) or get_guide(slug)


def precedents_for_topics(topics: list[str]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for topic in topics:
        for row in list_precedents(topic=topic):
            if row["slug"] in seen:
                continue
            seen.add(row["slug"])
            rows.append(row)
    return rows


def guides_for_topics(topics: list[str]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for topic in topics:
        for row in list_guides(topic=topic):
            if row["slug"] in seen:
                continue
            seen.add(row["slug"])
            rows.append(row)
    return rows


def hub() -> dict[str, Any]:
    return {
        "title": "Ombud guidance and precedent",
        "lead": (
            "NFO case reports (South Africa) and AFCA approach documents plus "
            "recurring patterns from published determinations (Australia). "
            "Illustrative of how the offices read typical wording — not advice "
            "on your policy, and not a complete digest of every decision."
        ),
        "precedents": PRECEDENTS,
        "guides": GUIDES,
        "za": [p for p in PRECEDENTS if p["jurisdiction"] == "za"],
        "au": [p for p in PRECEDENTS if p["jurisdiction"] == "au"],
    }
