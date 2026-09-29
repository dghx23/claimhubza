"""ClaimHub architecture, consent boundary, and professional workspace smoke tests."""

from __future__ import annotations

import os

os.environ.setdefault("SITE_AUTH_DISABLED", "1")

import claimhub_access
import db
from app import app


def _client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-claimhub"
    c = app.test_client()
    with c.session_transaction() as session:
        session["product_gate_ok"] = True
    return c


def test_claimhub_role_policy_requires_consent():
    assert claimhub_access.can(
        claimhub_access.CLINICIAN,
        claimhub_access.SCOPE_MEDICAL,
        [],
    ).allowed is False
    assert claimhub_access.can(
        claimhub_access.CLINICIAN,
        claimhub_access.SCOPE_MEDICAL,
        [{"scope": "case.medical", "status": "active", "revoked_at": None}],
    ).allowed is True


def test_claimhub_home_and_role_pages():
    c = _client()
    home = c.get("/claimhub")
    assert home.status_code == 200
    assert "ClaimHub" in home.get_data(as_text=True)
    assert "ClaimBuddy" in home.get_data(as_text=True)

    clinician = c.get("/claimhub/clinician")
    assert clinician.status_code == 200
    assert "ClaimHub for clinicians" in clinician.get_data(as_text=True)


def test_claimhub_case_hidden_without_consent(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "claimhub-test.db")
    monkeypatch.setattr(db, "UPLOAD_DIR", tmp_path / "uploads")
    db.init_db()
    claim_id = db.create_claim({"claimant_name": "Private Person", "employer": "Example Ltd"})

    c = _client()
    page = c.get(f"/claimhub/clinician/case/{claim_id}")
    assert page.status_code == 200
    body = page.get_data(as_text=True)
    assert "No case data is visible" in body
    assert "Private Person" not in body
    assert "Example Ltd" not in body


def test_authorised_professional_sees_only_granted_case_scope(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "claimhub-authorised.db")
    monkeypatch.setattr(db, "UPLOAD_DIR", tmp_path / "uploads")
    db.init_db()
    claim_id = db.create_claim({
        "claimant_name": "Authorised Person",
        "employer": "Example Employer",
        "occupation": "Analyst",
        "illness_summary": "Reduced concentration and stamina.",
    })
    user_id = db.create_user("clinician@example.test", "Dr Example")
    db.add_case_membership(claim_id, claimhub_access.CLINICIAN, user_id=user_id)
    db.grant_consent(claim_id, "case.summary", grantee_role=claimhub_access.CLINICIAN)
    db.grant_consent(claim_id, "case.function", grantee_role=claimhub_access.CLINICIAN)

    c = _client()
    with c.session_transaction() as session:
        session["claimhub_user_id"] = user_id
    page = c.get(f"/claimhub/clinician/case/{claim_id}")
    assert page.status_code == 200
    body = page.get_data(as_text=True)
    assert "Authorised Person" in body
    assert "Reduced concentration and stamina." in body
    assert "Authorised view" in body


def test_claimbuddy_can_create_and_accept_claimhub_invitation(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "claimhub-invite.db")
    monkeypatch.setattr(db, "UPLOAD_DIR", tmp_path / "uploads")
    db.init_db()
    claim_id = db.create_claim({"claimant_name": "Invite Person"})

    c = _client()
    made = c.post(
        f"/claim/{claim_id}/access",
        data={
            "email": "adviser@example.test",
            "role": "adviser",
            "scopes": ["case.summary", "case.timeline"],
        },
    )
    assert made.status_code == 200
    body = made.get_data(as_text=True)
    assert "Invitation ready" in body
    marker = "/claimhub/access/"
    start = body.index(marker) + len(marker)
    token = body[start:].split("<", 1)[0].split("&", 1)[0].strip()
    assert token

    accepted = c.post(
        f"/claimhub/access/{token}",
        data={"email": "adviser@example.test", "display_name": "Adviser Example"},
        follow_redirects=True,
    )
    assert accepted.status_code == 200
    accepted_body = accepted.get_data(as_text=True)
    assert "Authorised view" in accepted_body
    assert "Invite Person" in accepted_body
