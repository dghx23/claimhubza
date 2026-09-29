"""South African insurer and employer reference lists for intake autocomplete."""

from __future__ import annotations

# NFO Life Insurance Division participants (alphabetical).
# Source: https://www.nfosa.co.za/participants/life-insurance-division/
NFO_LIFE_INSURERS: list[str] = [
    "1Life Insurance Limited",
    "3Sixty Life Insurance Limited",
    "Abacus Insurance Limited",
    "ABSA Insurance & Financial Advisers (Pty) Ltd",
    "ABSA Life Limited",
    "Acsis Limited",
    "Affinity Life Limited",
    "AIG Life South Africa Limited",
    "Alexander Forbes Investments Limited",
    "Alexander Forbes Life Limited",
    "Allan Gray Life Limited",
    "Assupol Life Limited",
    "AVBOB Mutual Assurance Society",
    "Bidvest Life Limited",
    "BrightRock Life Limited",
    "Centriq Life Insurance Company Limited",
    "Clientele Life Assurance Co Ltd",
    "Constantia Life Limited",
    "Discovery Life Limited",
    "Dotsure Life Limited",
    "Emerald Life (Pty) Ltd",
    "Fedgroup Life Limited",
    "FirstRand Life Assurance Limited",
    "Guardrisk Life Limited",
    "Hollard Life Assurance Company Limited",
    "Hollard Specialist Insurance Limited",
    "Investec Life Limited",
    "Just Retirement Life (South Africa) Limited",
    "Liberty Group Limited",
    "Metropolitan Life Limited",
    "Merritt Insurance Limited",
    "MMI Group Limited",
    "Nedbank Life Assurance Company Limited",
    "Nedgroup Life Assurance Limited",
    "Nestlife Assurance Corporation Limited",
    "New Era Life Insurance Company Limited",
    "Ninety One Assurance Life",
    "Old Mutual Alternative Solutions Limited",
    "Old Mutual Life Assurance Company (SA) Limited",
    "OUTsurance Life Insurance Company (SA) Limited",
    "Professional Provident Society Insurance Company Limited",
    "PSG Life Limited",
    "Real People Assurance Company Limited",
    "RMA Life Assurance Company Limited",
    "Santam Structured Life Limited",
    "SA Home Loans Life Limited",
    "Safrican Insurance Company Limited",
    "Sanlam Developing Markets",
    "Sanlam Life Insurance Limited",
    "Shield Life Limited",
    "Smart Life Insurance Company Limited",
    "Vodacom Life Assurance Company Limited",
    "Viva Life Insurance Limited",
    "Workerslife Assurance Company Limited",
]

SA_LIFE_INSURERS: list[str] = list(NFO_LIFE_INSURERS)

NFO_LIFE_INSURER_SET: set[str] = set(NFO_LIFE_INSURERS)

# Short names / legacy intake values → canonical NFO participant name.
INSURER_ALIASES: dict[str, str] = {
    "1life": "1Life Insurance Limited",
    "1life insurance": "1Life Insurance Limited",
    "absa life": "ABSA Life Limited",
    "alexander forbes life": "Alexander Forbes Life Limited",
    "assupol": "Assupol Life Limited",
    "assupol life": "Assupol Life Limited",
    "avbob": "AVBOB Mutual Assurance Society",
    "brightrock": "BrightRock Life Limited",
    "brightrock life": "BrightRock Life Limited",
    "clientele": "Clientele Life Assurance Co Ltd",
    "clientele life": "Clientele Life Assurance Co Ltd",
    "discovery": "Discovery Life Limited",
    "discovery life": "Discovery Life Limited",
    "fedgroup life": "Fedgroup Life Limited",
    "guardrisk life": "Guardrisk Life Limited",
    "hollard": "Hollard Life Assurance Company Limited",
    "hollard life": "Hollard Life Assurance Company Limited",
    "hollard life assurance": "Hollard Life Assurance Company Limited",
    "investec life": "Investec Life Limited",
    "liberty": "Liberty Group Limited",
    "liberty group": "Liberty Group Limited",
    "metropolitan": "Metropolitan Life Limited",
    "metropolitan life": "Metropolitan Life Limited",
    "momentum": "MMI Group Limited",
    "momentum metropolitan": "MMI Group Limited",
    "mmi": "MMI Group Limited",
    "nedbank life": "Nedbank Life Assurance Company Limited",
    "old mutual": "Old Mutual Life Assurance Company (SA) Limited",
    "old mutual life": "Old Mutual Life Assurance Company (SA) Limited",
    "old mutual life assurance company (south africa)": "Old Mutual Life Assurance Company (SA) Limited",
    "outsurance": "OUTsurance Life Insurance Company (SA) Limited",
    "outsurance life": "OUTsurance Life Insurance Company (SA) Limited",
    "pps": "Professional Provident Society Insurance Company Limited",
    "pps life": "Professional Provident Society Insurance Company Limited",
    "sanlam": "Sanlam Life Insurance Limited",
    "sanlam life": "Sanlam Life Insurance Limited",
    "sanlam life insurance": "Sanlam Life Insurance Limited",
}

SA_EMPLOYERS: list[str] = [
    "Absa Group",
    "Accenture South Africa",
    "Ackermans (Pepkor)",
    "AECI",
    "AfriSam",
    "Airports Company South Africa (ACSA)",
    "Alexander Forbes",
    "Altron",
    "Anglo American",
    "Anglo American Platinum",
    "ArcelorMittal South Africa",
    "Armscor",
    "Barloworld",
    "BHP Billiton SA",
    "Bidvest Group",
    "Blue Label Telecoms",
    "BMW South Africa",
    "BP Southern Africa",
    "Bytes Technology Group",
    "Capitec Bank",
    "Clicks Group",
    "Coca-Cola Beverages Africa",
    "Coronation Fund Managers",
    "CSIR",
    "Curro Holdings",
    "Dairy Farmers of South Africa",
    "Datacentrix",
    "Deloitte South Africa",
    "Department of Basic Education",
    "Department of Health (National)",
    "Department of Home Affairs",
    "Department of Justice and Constitutional Development",
    "Department of Public Works and Infrastructure",
    "Department of Transport",
    "Dimension Data (NTT)",
    "Discovery Limited",
    "Distell (Heineken Beverages)",
    "DP World (formerly Imperial Logistics)",
    "Eskom",
    "EY South Africa",
    "Exxaro Resources",
    "FNB / FirstRand",
    "Ford Motor Company of Southern Africa",
    "G4S South Africa",
    "Gold Fields",
    "Grindrod",
    "Harmony Gold",
    "Hollard Insurance",
    "Huawei South Africa",
    "Impala Platinum (Implats)",
    "Investec",
    "Isuzu Motors South Africa",
    "Johannesburg Stock Exchange (JSE)",
    "JSE-listed company (other)",
    "Kagiso Media",
    "KPMG South Africa",
    "Liberty Group",
    "Life Healthcare",
    "Lombard Insurance",
    "Lonmin (part of Sibanye-Stillwater)",
    "Massmart (Walmart)",
    "Mediclinic Southern Africa",
    "Mercedes-Benz South Africa",
    "Metrofile",
    "Microsoft South Africa",
    "MMI Holdings (Momentum Metropolitan)",
    "Mondi South Africa",
    "Motus Holdings",
    "MTN Group",
    "MultiChoice Group",
    "Nampak",
    "Naspers / Prosus",
    "Nedbank Group",
    "Netcare",
    "North-West University",
    "Old Mutual",
    "Oracle South Africa",
    "Pepkor Holdings",
    "Pick n Pay Stores",
    "PricewaterhouseCoopers (PwC)",
    "Primedia",
    "Private practice / self-employed",
    "Public Investment Corporation (PIC)",
    "Rand Merchant Bank (RMB)",
    "Remgro",
    "Richemont SA",
    "SABMiller (AB InBev)",
    "Sage South Africa",
    "Sanlam",
    "SAP South Africa",
    "Sasol",
    "Sappi",
    "Sasria",
    "Shoprite Holdings",
    "Sibanye-Stillwater",
    "Siemens South Africa",
    "South African Airways (SAA)",
    "South African National Defence Force (SANDF)",
    "South African Police Service (SAPS)",
    "South African Post Office",
    "South African Revenue Service (SARS)",
    "South African Social Security Agency (SASSA)",
    "South32",
    "Standard Bank Group",
    "Stellenbosch University",
    "Sun International",
    "Telkom SA",
    "Tiger Brands",
    "Transnet",
    "Tshwane University of Technology",
    "UCT (University of Cape Town)",
    "UJ (University of Johannesburg)",
    "UKZN (University of KwaZulu-Natal)",
    "Unilever South Africa",
    "University of Pretoria",
    "University of the Free State",
    "University of the Witwatersrand (Wits)",
    "Upington employers (general)",
    "Vodacom",
    "Volkswagen Group South Africa",
    "Woolworths Holdings",
    "Yum! Brands South Africa (KFC, etc.)",
    "City of Cape Town",
    "City of Johannesburg",
    "City of Tshwane",
    "eThekwini Municipality",
    "Ekurhuleni Metropolitan Municipality",
    "Buffalo City Metropolitan Municipality",
    "Nelson Mandela Bay Municipality",
    "Mangaung Metropolitan Municipality",
    "Amazon Web Services South Africa",
    "Google South Africa",
    "Takealot Group",
    "Mr Price Group",
    "Truworths International",
    "The Foschini Group (TFG)",
    "Edgars / Retailability",
    "Builders Warehouse (Massmart)",
    "Game Stores",
    "Makro",
    "Checkers / Shoprite",
    "Boxer Superstores",
    "Spar Group (franchise employer)",
    "Woolworths Financial Services",
    "OUTsurance",
    "Telesure Investment Holdings",
    "Bidvest Bank",
    "African Bank",
    "TymeBank",
    "Discovery Bank",
    "Bank Zero",
    "Grobank",
    "OM Bank (Old Mutual)",
    "Access Bank South Africa",
    "Mercantile Bank (Capitec)",
    "Grindrod Bank",
    "Sasfin Bank",
    "HBZ Bank",
    "Ubank",
    "Land and Agricultural Development Bank (Land Bank)",
    "Industrial Development Corporation (IDC)",
    "Development Bank of Southern Africa (DBSA)",
    "Council for Scientific and Industrial Research (CSIR)",
    "Denel",
    "Armscor",
    "Prasa (Passenger Rail Agency)",
    "SANRAL",
    "Road Accident Fund (RAF)",
    "Compensation Fund (COIDA)",
    "Department of Employment and Labour",
    "Department of Trade, Industry and Competition (DTIC)",
    "National Treasury",
    "Government employee (other department)",
    "State-owned enterprise (other)",
    "NGO / non-profit employer",
    "Small business (less than 50 staff)",
    "Medium enterprise (50–250 staff)",
    "Large corporate (250+ staff)",
]

# Deduplicate while preserving order
_seen: set[str] = set()
SA_EMPLOYERS = [e for e in SA_EMPLOYERS if not (e in _seen or _seen.add(e))]  # type: ignore[func-returns-value]


def resolve_insurer_name(name: str) -> str | None:
    """Return canonical NFO participant name for a free-text or legacy value."""
    raw = (name or "").strip()
    if not raw:
        return None
    if raw in NFO_LIFE_INSURER_SET:
        return raw
    alias = INSURER_ALIASES.get(raw.lower())
    if alias:
        return alias
    lower = raw.lower()
    best: str | None = None
    best_len = 0
    for official in NFO_LIFE_INSURERS:
        ol = official.lower()
        if ol in lower or lower in ol:
            if len(official) > best_len:
                best = official
                best_len = len(official)
    return best


def insurer_is_nfo_participant(name: str) -> bool:
    return resolve_insurer_name(name) is not None


def _search_list(items: list[str], query: str, limit: int = 12) -> list[dict[str, str]]:
    q = (query or "").strip().lower()
    if not q:
        return [{"name": name} for name in items[:limit]]
    matches: list[tuple[int, str]] = []
    for name in items:
        lower = name.lower()
        if q in lower:
            pos = lower.find(q)
            matches.append((pos, name))
    matches.sort(key=lambda x: (x[0], x[1]))
    return [{"name": name} for _, name in matches[:limit]]


def search_insurers(query: str, limit: int = 12) -> list[dict[str, str]]:
    q = (query or "").strip()
    if not q:
        return [{"name": name} for name in NFO_LIFE_INSURERS[:limit]]
    resolved = resolve_insurer_name(q)
    if resolved and resolved.lower().startswith(q.lower()):
        results = [{"name": resolved}]
        for name in NFO_LIFE_INSURERS:
            if name != resolved and q.lower() in name.lower():
                results.append({"name": name})
            if len(results) >= limit:
                break
        return results[:limit]
    return _search_list(NFO_LIFE_INSURERS, q, limit)


def search_employers(query: str, limit: int = 12) -> list[dict[str, str]]:
    return _search_list(SA_EMPLOYERS, query, limit)


def _longest_name_in_text(names: list[str], text: str) -> str | None:
    lower = text.lower()
    best: str | None = None
    best_len = 0
    for name in names:
        nl = name.lower()
        if nl in lower and len(name) > best_len:
            best = name
            best_len = len(name)
    return best


def match_insurer_in_text(text: str) -> str | None:
    resolved = resolve_insurer_name(text)
    if resolved:
        return resolved
    lower = text.lower()
    best: str | None = None
    best_len = 0
    for name in NFO_LIFE_INSURERS:
        nl = name.lower()
        if nl in lower and len(name) > best_len:
            best = name
            best_len = len(name)
    return best


def match_employer_in_text(text: str) -> str | None:
    return _longest_name_in_text(SA_EMPLOYERS, text)