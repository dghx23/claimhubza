"""Sentrix Digital / RiskAtlas — product and jurisdiction configuration.

SentrixDigital is the Australian public identity. RiskAtlas is the South African public identity.
The shared codebase remains an internal implementation detail.

Core maintains reusable structured data. RiskAtlas is the reference-intelligence
layer. Domain products such as ClinicalAtlas, SchemeBook and Social Security
Compass consume that intelligence. ClaimHub owns live claims coordination;
ClaimBuddy is the claimant-facing experience within ClaimHub.

The studio is based in Melbourne and serves Australia and South Africa.
Jurisdiction packs keep local law, insurance, health-system and social-security
context separate rather than treating countries as interchangeable.
"""

from __future__ import annotations

from typing import Any

ORG = {
    "name": "Sentrix Digital",
    "short": "Sentrix",
    "tagline": "Sentrix Digital",
    "tool": "RiskAtlas",
    "tool_role": "Reference intelligence",
    "address": "Melbourne",
    "place": "Australia | Melbourne",
    "email": "info@sentrixdigital.com",
    "phone": "+61 (03) 9088 1341",
    "abn": "29 203 554 753",
}

PRODUCTS = [
    {
        "id": "riskatlas",
        "name": "RiskAtlas",
        "kicker": "Reference intelligence",
        "icon": "●◌●",
        "blurb": "Connected policy, clinical, occupational, regulatory and social-support intelligence with clear source provenance.",
        "endpoint": "riskatlas",
        "cta": "Explore RiskAtlas →",
        "links": [],
    },
    {
        "id": "claimhub",
        "name": "ClaimHub",
        "kicker": "Claims coordination platform",
        "icon": "👥",
        "blurb": "A live claims platform connecting claimants and authorised professionals around one shared case record.",
        "endpoint": "claimsite_home",
        "cta": "Explore ClaimHub →",
        "links": [],
    },
    {
        "id": "claimbuddy",
        "name": "ClaimBuddy",
        "kicker": "ClaimHub claimant experience",
        "icon": "👤",
        "blurb": "The claimant-facing side of ClaimHub: understand, organise and prepare a claim while staying connected to the shared case.",
        "endpoint": "inbox",
        "cta": "Open ClaimBuddy →",
        "links": [],
    },
    {
        "id": "clinicalatlas",
        "name": "ClinicalAtlas",
        "kicker": "Clinical reference",
        "icon": "⚕",
        "blurb": "Conditions, medicines, therapies, clinicians and health-system reference context. South Africa is live; Australia remains a developing data layer.",
        "endpoint": "clinicalatlas",
        "cta": "Explore ClinicalAtlas →",
        "links": [
            {"label": "ZA", "endpoint": "clinical_atlas_za.index"},
            {"label": "AU", "endpoint": "clinical_atlas_au.index"},
        ],
    },
    {
        "id": "schemebook",
        "name": "SchemeBook",
        "kicker": "South African medical schemes",
        "icon": "▥",
        "blurb": "Medical-scheme directory, benefit context and plain-language terminology grounded in official South African sources.",
        "endpoint": "schemebook_home",
        "cta": "Explore SchemeBook →",
        "links": [],
    },
    {
        "id": "compass",
        "name": "Social Security Compass",
        "kicker": "Social support navigation",
        "icon": "⌖",
        "blurb": "Government grants, benefits, eligibility, processes and support pathways presented in practical language.",
        "endpoint": "compass",
        "cta": "Explore Compass →",
        "links": [],
    },
]

# AfterDuty is a different product — personal-import price, not claims or training.
# Live at afterduty.co.za; Sentrix only lists it.
PRODUCT_DESTINATIONS = {
    # Public links use the product's current live/preview home for now.
    # Keep future custom-domain targets separately so they can be switched
    # without touching templates when DNS / hosting is ready.
    "riskatlas": {
        "label": "RiskAtlas",
        "url": "https://riskatlas.co.za/",
        "future_url": "https://riskatlas.co.za/",
        "status": "custom_domain_ready",
    },
    "schemebook": {
        "label": "SchemeBook",
        "url": "https://schemebook.riskatlas.co.za/",
        "future_url": "https://schemebook.riskatlas.co.za/",
        "status": "custom_domain_ready",
    },
    "clinicalatlas_za": {
        "label": "ClinicalAtlas ZA",
        "url": "https://riskatlas.co.za/clinical-atlas/",
        "future_url": "https://clinical.riskatlas.co.za/",
        "status": "live_sentrix_za",
    },
    "claimhub": {
        "label": "ClaimHub",
        "url": "https://riskatlas.co.za/claims#connected",
        "future_url": "https://claimhub.co.za/",
        "status": "live_sentrix_za",
    },
    "claimbuddy": {
        "label": "ClaimBuddy",
        "url": "https://riskatlas.co.za/claimbuddy",
        "future_url": "https://buddy.claimhub.co.za/",
        "status": "live_sentrix_za",
    },
    "afterduty": {
        "label": "AfterDuty",
        "url": "https://www.afterduty.co.za/",
        "future_url": "https://www.afterduty.co.za/",
        "status": "live",
    },
    "compass_za": {
        "label": "Social Security Compass ZA",
        "url": "https://compass.riskatlas.co.za/",
        "future_url": "https://compass.riskatlas.co.za/",
        "status": "live_sentrix_za",
    },
    "disability_employment_sa": {
        "label": "Disability Employment SA",
        "url": "https://tools.riskatlas.co.za/disability",
        "future_url": "https://tools.riskatlas.co.za/disability",
        "status": "development",
    },
    "compass_au": {
        "label": "Social Security Compass AU",
        "url": "https://sentrixdigital.com.au/compass/au",
        "future_url": "https://sentrixdigital.com.au/compass/au",
        "status": "live_sentrix_au",
    },
}

OTHER_PRODUCTS = [
    {
        "id": "afterduty",
        "name": "AfterDuty",
        "kicker": "A different product",
        "blurb": (
            "The price after duty versus buying it here. Personal imports into South Africa "
            "and Botswana — duty, VAT on ATV, clearance and courier next to a local listing. "
            "Not a customs broker. SARS and BURS have the last word."
        ),
        "endpoint": "afterduty",
        "cta": "Open AfterDuty.co.za →",
        "external_url": "https://www.afterduty.co.za/",
    },
]

SERVICES = [
    {
        "id": "consulting",
        "name": "Consulting and Advisory",
        "kicker": "Service",
        "icon": "🧾",
        "blurb": (
            "Institutional diagnosis and advisory — tracing the fault lines "
            "between what is documented and what actually functions."
        ),
        "endpoint": "consulting",
        "cta": "Consulting →",
        "links": [
            {"label": "About", "endpoint": "about"},
        ],
    },
]

JURISDICTIONS: dict[str, dict[str, Any]] = {
    "za": {
        "code": "za",
        "name": "South Africa",
        "short": "ZA",
        "domain": "riskatlas.co.za",
        "domain_status": "migration_pending",
        "currency": "ZAR",
        "currency_symbol": "R",
        "currency_pattern_symbol": "R",
        "privacy_law": "POPIA",
        "privacy_access": "POPIA and PAIA",
        "complaint_body": "NFO",
        "complaint_body_full": "National Financial Ombud Scheme of South Africa",
        "complaint_stage_label": "Ombud complaint",
        "idr_label": "Internal review",
        "disablement_label": "Date of Absence",
        "disablement_short": "DOA",
        "occupation_system": "ESCO (SA overlay)",
        "clinician_regulator": "HPCSA",
        "financial_regulator": "FSCA",
        "scheme_label": "Medical scheme",
        "policyholder_label": "Policyholder / participating employer",
        "trustee_label": None,
        "cover_types": [
            ("group_ip", "Group income protection"),
            ("individual_ip", "Individual income protection"),
            ("disability", "Disability / lump-sum"),
        ],
        "catalog_blocks": ("language", "glossary", "traps", "clinical_atlas", "cms_schemes", "nfo", "life_insurers"),
        "disclaimer": (
            "Not medical, legal, or financial advice. Organisation and drafting only. "
            "Verify with clinicians, schemes, and policy documents. South African complaints: "
            "insurer internal review, then the National Financial Ombud (NFO)."
        ),
        "letter_access_basis": "POPIA and, where it applies, PAIA",
        "external_complaint_next": "NFO complaint after internal review",
        "salary_labels": {
            "gross": "Gross earnings",
            "net": "Net pay",
            "tax": "PAYE / tax",
            "pension": "Pension / provident",
            "health": "Medical aid",
            "statutory": "UIF",
        },
    },
    "au": {
        "code": "au",
        "name": "Australia",
        "short": "AU",
        "domain": "sentrixdigital.com.au",
        "domain_status": "live",
        "currency": "AUD",
        "currency_symbol": "$",
        "currency_pattern_symbol": "\\$",
        "privacy_law": "Privacy Act 1988 (Cth)",
        "privacy_access": "APP 12 access to personal information",
        "complaint_body": "AFCA",
        "complaint_body_full": "Australian Financial Complaints Authority",
        "complaint_stage_label": "AFCA complaint",
        "idr_label": "Internal dispute resolution (IDR)",
        "disablement_label": "Date of disablement",
        "disablement_short": "DOD",
        "occupation_system": "ANZSCO (ESCO fallback until native feed)",
        "clinician_regulator": "AHPRA",
        "financial_regulator": "ASIC / APRA",
        "scheme_label": "Super fund",
        "policyholder_label": "Policy owner / super trustee",
        "trustee_label": "Super trustee",
        "cover_types": [
            ("ip_super", "Income protection inside super"),
            ("ip_retail", "Income protection (retail / outside super)"),
            ("tpd_super", "TPD inside super"),
            ("tpd_retail", "TPD (retail / outside super)"),
        ],
        "catalog_blocks": ("language", "glossary", "traps", "super_funds", "life_insurers", "afca"),
        "disclaimer": (
            "Not medical, legal, or financial advice. Organisation and drafting only. "
            "Verify with treating practitioners, the PDS, and the trustee/insurer. "
            "Australian complaints: insurer/trustee IDR, then AFCA."
        ),
        "letter_access_basis": "the Privacy Act 1988 (Cth), including APP 12",
        "external_complaint_next": "AFCA after IDR",
        "salary_labels": {
            "gross": "Gross earnings",
            "net": "Net pay",
            "tax": "PAYG / tax",
            "pension": "Super contributions",
            "health": "Health insurance",
            "statutory": "WorkCover / Centrelink offsets",
        },
    },
}

DEFAULT_CODE = "au"
COOKIE = "ra_jurisdiction"


def normalize(code: str | None) -> str:
    raw = (code or "").strip().lower()
    if raw in ("au", "australia", "aus"):
        return "au"
    if raw in ("za", "south africa", "rsa", "sa"):
        return "za"
    return DEFAULT_CODE


def profile(code: str | None = None) -> dict[str, Any]:
    return dict(JURISDICTIONS[normalize(code)])


def all_profiles() -> list[dict[str, Any]]:
    return [profile(code) for code in ("za", "au")]


_BASE_STAGE_LABELS = {
    "preparing": "Preparing claim",
    "waiting_period": "Waiting-period evidence",
    "assessment": "Insurer assessment",
    "rejected": "Rejected claim",
    "internal_review": "Internal review",
    "ombud": "External complaint",
    "record_access": "Record-access dispute",
    "professional": "Professional review",
}


def stage_labels(code: str | None = None) -> dict[str, str]:
    labels = dict(_BASE_STAGE_LABELS)
    j = profile(code)
    labels["internal_review"] = j["idr_label"]
    labels["ombud"] = j["complaint_stage_label"]
    labels["record_access"] = f"{j['privacy_law']} access"
    return labels


def applies(item: dict[str, Any], code: str | None) -> bool:
    allowed = item.get("jurisdictions")
    if not allowed:
        return True
    return normalize(code) in allowed


def shows_block(block: str, code: str | None) -> bool:
    return block in profile(code)["catalog_blocks"]


ZA_HOST_MARKERS = (".co.za",)
SENTRIX_ZA_HOSTS = {"riskatlas.co.za", "www.riskatlas.co.za", "riskatlas-0iob.onrender.com"}
SENTRIX_AU_HOSTS = {
    "sentrixdigital.com", "www.sentrixdigital.com",
    "sentrixdigital.com.au", "www.sentrixdigital.com.au",
}


def _canonical_sentrix_host_jurisdiction(host: str | None) -> str | None:
    host = (host or "").split(":")[0].strip().lower()
    if host in SENTRIX_ZA_HOSTS:
        return "za"
    if host in SENTRIX_AU_HOSTS:
        return "au"
    return None


def _host_suggests_za(host: str | None) -> bool:
    host = (host or "").lower()
    return any(marker in host for marker in ZA_HOST_MARKERS)


def _geo_country_suggests_za(geo_country: str | None) -> bool:
    return (geo_country or "").strip().upper() == "ZA"


def from_values(
    *,
    cookie: str | None = None,
    arg: str | None = None,
    form: str | None = None,
    claim_code: str | None = None,
    host: str | None = None,
    geo_country: str | None = None,
) -> str:
    """Canonical public hosts define market boundaries during the brand migration:
    riskatlas.co.za serves RiskAtlas ZA; sentrixdigital.com and sentrixdigital.com.au serve SentrixDigital AU. Claim-specific
    jurisdiction still wins for stored claim data, while query/form/cookie
    switching remains available only on non-canonical development hosts.
    """
    if claim_code:
        return normalize(claim_code)
    canonical_host = _canonical_sentrix_host_jurisdiction(host)
    if canonical_host:
        return canonical_host
    if form:
        return normalize(form)
    if arg:
        return normalize(arg)
    if cookie:
        return normalize(cookie)
    if _host_suggests_za(host):
        return "za"
    if _geo_country_suggests_za(geo_country):
        return "za"
    return DEFAULT_CODE


def attach_cookie(response: Any, code: str) -> Any:
    response.set_cookie(
        COOKIE,
        normalize(code),
        max_age=400 * 24 * 3600,
        samesite="Lax",
        path="/",
    )
    return response


def cover_type_label(code: str | None, cover_type: str | None) -> str:
    j = profile(code)
    for key, label in j["cover_types"]:
        if key == cover_type:
            return label
    return cover_type or ""


def employer_letter(claim: dict, gaps: list[dict]) -> str:
    j = profile(claim.get("jurisdiction"))
    employer = claim.get("employer") or "[Employer]"
    records = [
        g["item"]
        for g in gaps
        if "Employer" in g.get("holder", "") or "payroll" in g.get("holder", "").lower()
    ]
    if not records:
        records = ["Employer statement", "Absence / leave records", "Payslips", "Role / duty description"]
        if j["code"] == "au":
            records.append("Workers compensation / income-protection interaction notes (if any)")
    body = "\n".join(f"- {r}" for r in records)
    return f"""EMPLOYER RECORD REQUEST (DRAFT — review before sending)

To: Human Resources / Benefits / Payroll
{employer}

Re: Income protection / disability claim — record request
Policy / claim ref: {claim.get('policy_number') or 'N/A'} / {claim.get('claim_reference') or 'N/A'}
Jurisdiction: {j['name']}

Dear Sir/Madam,

I request copies of the following records held by the employer for the purpose of my claim, under {j['letter_access_basis']}:

{body}

Please confirm receipt and expected turnaround. Electronic copies are preferred.

Yours faithfully,
[Claimant name]
[Date]
"""


def insurer_letter(claim: dict) -> str:
    j = profile(claim.get("jurisdiction"))
    date_label = j["disablement_label"]
    extra = ""
    if j["code"] == "au":
        extra = (
            "\n- Product Disclosure Statement and policy schedule relied upon\n"
            "- Whether cover is held inside super, and the trustee's role in the decision\n"
            "- Any occupation / own occupation / ETE test applied, and from which date"
        )
    return f"""INSURER RECORD REQUEST (DRAFT — review before sending)

To: Claims Department
{claim.get('insurer') or '[Insurer]'}

Re: Claim {claim.get('claim_reference') or '[reference]'} — claim file and {date_label} disclosure
Jurisdiction: {j['name']}

Dear Sir/Madam,

I request access to the following records relating to my claim, under {j['letter_access_basis']}:

- Complete claim-file notes and assessment memoranda
- {date_label} calculation methodology and selected date
- Medical reviewer instructions and the evidence index relied upon
- Copy of any employer statement received
- Any further-evidence requests and responses{extra}

My stated {date_label}: {claim.get('date_of_absence') or 'see medical records'}
Insurer-stated date (if any): {claim.get('insurer_doa') or 'not yet disclosed'}

This request is to enable a fair reassessment / {j['idr_label']}.

Yours faithfully,
[Claimant name]
[Date]
"""


def trustee_letter(claim: dict) -> str | None:
    j = profile(claim.get("jurisdiction"))
    if not j.get("trustee_label"):
        return None
    return f"""SUPER TRUSTEE RECORD REQUEST (DRAFT — review before sending)

To: Trustee / claims administrator
{claim.get('policyholder') or claim.get('insurer') or '[Super fund]'}

Re: Superannuation insurance claim {claim.get('claim_reference') or '[reference]'}
Jurisdiction: Australia

Dear Sir/Madam,

Cover held through super has two decision-makers: the insurer and the trustee. I request, under the Privacy Act 1988 (Cth) and as a fund member:

- Confirmation of the insured benefit (IP and/or TPD) and whether it is held inside this fund
- The PDS and insurance policy the trustee relied on
- The trustee's claim file, including any recommendation to the insurer and the trustee's own decision
- Date of disablement used by the trustee, if different from the insurer
- IDR outcome letter and AFCA-ready reasons

Member / claim ref: {claim.get('policy_number') or 'N/A'} / {claim.get('claim_reference') or 'N/A'}

Yours faithfully,
[Claimant name]
[Date]
"""


def review_letter(claim: dict, gaps: list[dict], timeline: list[dict]) -> str:
    j = profile(claim.get("jurisdiction"))
    high = [g for g in gaps if g.get("urgency") == "high"][:5]
    gap_text = "\n".join(f"- {g['item']} ({g['holder']}): {g['request']}" for g in high) or "- See evidence-gap report"
    heading = j["idr_label"].upper()
    next_step = j["external_complaint_next"]
    date_label = j["disablement_label"]
    return f"""{heading} REQUEST (DRAFT — review before sending)

To: {claim.get('insurer') or '[Insurer]'} — {j['idr_label']}
Claim: {claim.get('claim_reference') or '[reference]'}
Policy: {claim.get('policy_number') or 'N/A'}
Rejection date: {claim.get('rejection_date') or 'N/A'}
Jurisdiction: {j['name']}

I request reassessment of the decision. This submission is organised by issue and evidence, not narrative alone.

## Chronology
{len(timeline)} dated events in the attached file chronology.

## Issues
1. Whether the disability / TPD / IP test was applied to the material duties of: {claim.get('occupation') or '[occupation]'}
2. Whether {date_label} and notice dates were calculated consistently with the policy / PDS
3. Whether employer-controlled (and, if applicable, trustee-controlled) records were obtained before the adverse finding

## Evidence cure plan
{gap_text}

## Remedy sought
Reassessment, disclosure of the claim file, and preservation of complaint rights ({next_step}).

Yours faithfully,
[Claimant name]
"""