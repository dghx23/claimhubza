"""Library directory of life insurers — ZA (NFO participants) and AU (APRA writers).

Names stay in sa_reference_data / au_reference_data for intake autocomplete.
This module adds slugs, kinds, notes, and complaint-path copy for the Library.
Full register ingest is recorded on Core ZA (NFO) and Core AU (APRA).
"""

from __future__ import annotations

from typing import Any

from au_reference_data import AU_LIFE_INSURERS
from sa_reference_data import NFO_LIFE_INSURERS
from term_slugs import slugify

_AU_META: dict[str, dict[str, str]] = {
    "AIA Australia": {
        "kind": "Writer",
        "note": "Large retail and group IP / TPD writer. Holds some CommInsure legacy books.",
    },
    "TAL Life": {
        "kind": "Writer",
        "note": "Major group and retail writer. Holds Asteron / Suncorp Life books.",
    },
    "MLC Life Insurance": {
        "kind": "Writer",
        "note": "Retail and group. Book sits with Resolution Life Australasia.",
    },
    "Resolution Life Australasia": {
        "kind": "Writer",
        "note": "Closed and in-force books including AMP Life and MLC Life.",
    },
    "Zurich Australia": {"kind": "Writer", "note": "Retail and group life, IP, and TPD."},
    "MetLife Australia": {"kind": "Writer", "note": "Often seen on group IP / TPD via super."},
    "OnePath Life": {
        "kind": "Writer",
        "note": "Insignia Financial life company — retail and group.",
    },
    "ClearView Life": {"kind": "Writer", "note": "Retail advice-led life and IP."},
    "NobleOak Life": {"kind": "Writer", "note": "Direct / advice retail life and IP."},
    "NEOS Life": {"kind": "Writer", "note": "Retail life and IP, often via advisers."},
    "Integrity Life": {"kind": "Writer", "note": "Retail life and IP."},
    "Asteron Life": {
        "kind": "Legacy brand",
        "note": "Suncorp life brand; in-force book with TAL.",
    },
    "Hallmark Life": {"kind": "Writer", "note": "Consumer credit and related life cover."},
    "Westpac Life": {"kind": "Writer", "note": "Bank-distributed life and IP."},
    "BT Life": {"kind": "Writer", "note": "Westpac / BT distributed life cover."},
    "CommInsure": {
        "kind": "Legacy brand",
        "note": "CBA life brand; in-force book largely with AIA Australia.",
    },
    "AMP Life": {
        "kind": "Legacy brand",
        "note": "In-force book with Resolution Life Australasia.",
    },
    "Suncorp Life": {
        "kind": "Legacy brand",
        "note": "Life book transferred to TAL.",
    },
    "Allianz Australia Life": {"kind": "Writer", "note": "Retail life alongside general insurance."},
    "Challenger Life": {"kind": "Writer", "note": "Annuities and related life company."},
    "HCF Life": {"kind": "Writer", "note": "Life cover associated with HCF membership."},
    "Australian Unity Life": {"kind": "Writer", "note": "Friendly-society / advice retail life."},
    "QInsure": {
        "kind": "Writer",
        "note": "Group life / TPD / IP inside Australian Retirement Trust (ex QSuper).",
    },
    "St Andrew's Life": {"kind": "Writer", "note": "BOQ group life company."},
    "Insuranceline": {"kind": "Brand", "note": "Direct brand in the TAL group."},
    "Hannover Life Re of Australasia": {"kind": "Reinsurer", "note": "Life reinsurance — not a retail claim brand."},
    "Swiss Re Life & Health Australia": {"kind": "Reinsurer", "note": "Life reinsurance."},
    "Munich Re of Australasia": {"kind": "Reinsurer", "note": "Life reinsurance."},
    "RGA Australia": {"kind": "Reinsurer", "note": "Life reinsurance."},
    "General Reinsurance Life Australia": {"kind": "Reinsurer", "note": "Life reinsurance (Gen Re)."},
    "Pacific Life Re Australia": {"kind": "Reinsurer", "note": "Life reinsurance."},
}

_ZA_META: dict[str, dict[str, str]] = {
    "Discovery Life Limited": {
        "kind": "Writer",
        "note": "Large retail and group IP writer.",
    },
    "Old Mutual Life Assurance Company (SA) Limited": {
        "kind": "Writer",
        "note": "Retail and group life / IP / disability.",
    },
    "Sanlam Life Insurance Limited": {
        "kind": "Writer",
        "note": "Retail and group life / IP / disability.",
    },
    "Liberty Group Limited": {
        "kind": "Writer",
        "note": "Retail and group; Stanlib / Standard Bank distribution.",
    },
    "Metropolitan Life Limited": {
        "kind": "Writer",
        "note": "Momentum Metropolitan retail life brand.",
    },
    "MMI Group Limited": {
        "kind": "Writer",
        "note": "Momentum Metropolitan holding / group life.",
    },
    "Professional Provident Society Insurance Company Limited": {
        "kind": "Writer",
        "note": "PPS — professional occupation IP and sickness cover.",
    },
    "Hollard Life Assurance Company Limited": {"kind": "Writer", "note": "Retail and group life."},
    "Guardrisk Life Limited": {"kind": "Writer", "note": "Cell-captive / group life structures."},
    "BrightRock Life Limited": {"kind": "Writer", "note": "Needs-matched retail life and IP."},
    "Assupol Life Limited": {"kind": "Writer", "note": "Retail life, often entry-level and group."},
    "Clientele Life Assurance Co Ltd": {"kind": "Writer", "note": "Direct retail life."},
    "1Life Insurance Limited": {"kind": "Writer", "note": "Direct retail life."},
    "OUTsurance Life Insurance Company (SA) Limited": {"kind": "Writer", "note": "Direct retail life."},
    "ABSA Life Limited": {"kind": "Writer", "note": "Bank-distributed life and IP."},
    "FirstRand Life Assurance Limited": {"kind": "Writer", "note": "FNB / FirstRand life company."},
    "Nedbank Life Assurance Company Limited": {"kind": "Writer", "note": "Bank-distributed life."},
    "Allan Gray Life Limited": {"kind": "Writer", "note": "Linked-investment life company."},
    "Investec Life Limited": {"kind": "Writer", "note": "Private-client life company."},
    "AVBOB Mutual Assurance Society": {"kind": "Writer", "note": "Mutual; funeral and life."},
}

_PACKS: dict[str, dict[str, Any]] = {
    "za": {
        "code": "za",
        "title": "South African life insurers",
        "lead": (
            "NFO Life Insurance Division participants — the writers that sit on "
            "South African income-protection and life files, and the body that "
            "hears complaints after internal review."
        ),
        "source": "National Financial Ombud Scheme — Life Insurance Division participants",
        "source_url": "https://www.nfosa.co.za/participants/life-insurance-division/",
        "complaint": "Internal review, then the National Financial Ombud (NFO).",
        "names": NFO_LIFE_INSURERS,
        "meta": _ZA_META,
    },
    "au": {
        "code": "au",
        "title": "Australian life insurers",
        "lead": (
            "Life companies and brands commonly seen on Australian IP / TPD files — "
            "retail, group inside super, and reinsurers. The APRA register is the "
            "canonical list; it is recorded on Core AU for ingest."
        ),
        "source": "APRA Register of Life Companies (curated working list)",
        "source_url": "https://www.apra.gov.au/register-of-life-insurance-companies",
        "complaint": "Insurer or trustee IDR, then AFCA.",
        "names": AU_LIFE_INSURERS,
        "meta": _AU_META,
    },
}


def _entry(code: str, name: str) -> dict[str, Any]:
    pack = _PACKS[code]
    meta = pack["meta"].get(name) or {}
    return {
        "name": name,
        "slug": slugify(name),
        "code": code,
        "kind": meta.get("kind") or "Writer",
        "note": meta.get("note") or "",
        "source": pack["source"],
        "source_url": pack["source_url"],
        "complaint": pack["complaint"],
    }


def directory_meta(code: str) -> dict[str, Any]:
    key = "au" if (code or "").lower() == "au" else "za"
    pack = _PACKS[key]
    entries = list_life_insurers(key)
    kinds: dict[str, int] = {}
    for row in entries:
        kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1
    return {
        "code": key,
        "title": pack["title"],
        "lead": pack["lead"],
        "source": pack["source"],
        "source_url": pack["source_url"],
        "complaint": pack["complaint"],
        "count": len(entries),
        "kinds": kinds,
        "other_code": "za" if key == "au" else "au",
        "other_title": _PACKS["za" if key == "au" else "au"]["title"],
    }


def list_life_insurers(code: str) -> list[dict[str, Any]]:
    key = "au" if (code or "").lower() == "au" else "za"
    return [_entry(key, name) for name in _PACKS[key]["names"]]


def get_life_insurer(code: str, slug: str) -> dict[str, Any] | None:
    slug = (slug or "").strip().lower()
    for row in list_life_insurers(code):
        if row["slug"] == slug:
            return row
    return None


def search_life_insurers(code: str, query: str) -> list[dict[str, Any]]:
    needle = (query or "").strip().lower()
    rows = list_life_insurers(code)
    if not needle:
        return rows
    return [r for r in rows if needle in r["name"].lower() or needle in r["kind"].lower()]
