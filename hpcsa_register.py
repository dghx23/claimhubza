"""Search the public HPCSA i-register listing (live API)."""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

HPCSA_SEARCH_URL = "https://hpcsaonline.custhelp.com/cc/ReportController/getDataFromRnow"
TIMEOUT = 14
_CACHE_TTL = 300
_cache: dict[str, tuple[float, list[dict[str, str]]]] = {}

_REGISTER_HINTS: dict[str, str] = {
    "MP": "Medical practitioner",
    "DP": "Dentist",
    "MW": "Medical technologist",
    "SDR": "Student doctor",
    "PC": "Psychologist",
    "PN": "Registered nurse",
    "PT": "Physiotherapist",
    "OT": "Occupational therapist",
    "DT": "Dietitian",
    "SW": "Social worker",
}


def _fetch_search(params: dict[str, str]) -> dict[str, Any]:
    body = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(
        HPCSA_SEARCH_URL,
        data=body,
        method="POST",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "ClaimBuddy/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _cell(row: list[Any], order: int) -> str:
    if order >= len(row):
        return ""
    val = row[order]
    return str(val).strip() if val is not None else ""


def _register_code(reg_number: str) -> str:
    m = re.match(r"([A-Za-z]{2,4})", reg_number.replace(" ", ""))
    return m.group(1).upper() if m else ""


def _display_name(title: str, firstname: str, surname: str) -> str:
    parts = [p for p in (title, firstname, surname) if p]
    name = " ".join(parts).strip()
    return re.sub(r"\s+", " ", name)


def _parse_results(payload: dict[str, Any]) -> list[dict[str, str]]:
    headers = payload.get("headers") or []
    order_by_heading = {h.get("heading"): h.get("order", 0) for h in headers if h.get("heading")}
    rows = payload.get("data") or []
    results: list[dict[str, str]] = []

    for row in rows:
        title = _cell(row, order_by_heading.get("Title", 0))
        surname = _cell(row, order_by_heading.get("Surname", 1))
        firstname = _cell(row, order_by_heading.get("Fullname", 2))
        reg = _cell(row, order_by_heading.get("Registration", 3))
        city = _cell(row, order_by_heading.get("City", 4))
        postcode = _cell(row, order_by_heading.get("Postal Code", 5))
        category = _cell(row, order_by_heading.get("Category", 6))
        status = _cell(row, order_by_heading.get("Status", 7))
        reg_code = _register_code(reg)
        register_hint = _REGISTER_HINTS.get(reg_code, reg_code or "HPCSA")

        display = _display_name(title, firstname, surname)
        description = (
            f"HPCSA {reg} — {register_hint}. "
            f"{category or 'Category not listed'}. "
            f"{city}{', ' + postcode if postcode else ''}. "
            f"Status: {status}."
        )
        results.append({
            "name": display,
            "title": title,
            "firstname": firstname,
            "surname": surname,
            "registration_number": reg,
            "register": register_hint,
            "category": category,
            "city": city,
            "postcode": postcode,
            "status": status,
            "description": description,
        })
    return results


def _split_query(query: str) -> tuple[str, str, str]:
    q = (query or "").strip()
    if not q:
        return "", "", ""
    if re.match(r"^[A-Za-z]{2,4}\s*\d", q):
        return q, "", ""
    parts = q.split()
    if len(parts) == 1:
        return "", "", parts[0]
    if len(parts) == 2:
        return "", parts[0], parts[1]
    return "", parts[0], " ".join(parts[1:])


def search_practitioners(query: str, limit: int = 25) -> list[dict[str, str]]:
    """Search HPCSA public register by name or registration number."""
    q = (query or "").strip()
    if len(q) < 2:
        return []

    cache_key = q.lower()
    cached = _cache.get(cache_key)
    if cached and time.time() - cached[0] < _CACHE_TTL:
        return cached[1][:limit]

    reg_number, firstname, surname = _split_query(q)
    params = {
        "regNumber": reg_number,
        "firstName": firstname,
        "surName": surname,
        "city": "",
        "postalCode": "",
        "register": "",
        "category": "",
    }
    try:
        payload = _fetch_search(params)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return []

    parsed = _parse_results(payload)
    active = [r for r in parsed if r.get("status", "").upper() == "ACTIVE"]
    other = [r for r in parsed if r.get("status", "").upper() != "ACTIVE"]
    ordered = active + other
    _cache[cache_key] = (time.time(), ordered)
    return ordered[:limit]