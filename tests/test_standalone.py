"""Standalone host, privacy, and claims-family smoke tests."""

from __future__ import annotations

import db
from app import create_app


def test_public_hosts_and_health():
    app = create_app({"TESTING": True, "SECRET_KEY": "test", "CLAIMHUB_ENABLE_CASES": False})
    client = app.test_client()
    assert client.get("/health").json == {
        "status": "ok", "service": "claimhubza", "cases_enabled": False,
    }
    claimhub = client.get("/", headers={"Host": "claimhub.co.za"})
    buddy = client.get("/", headers={"Host": "buddy.claimhub.co.za"})
    assert claimhub.status_code == buddy.status_code == 200
    assert b"ClaimHub" in claimhub.data
    assert b"ClaimBuddy" in buddy.data
    assert client.get("/claimhub/employer").status_code == 200
    assert client.get("/inbox", headers={"Host": "buddy.claimhub.co.za"}).status_code == 200
    assert client.post("/inbox", data={"claimant_name": "Person"}).status_code == 503


def test_reference_links_leave_claimhub():
    app = create_app({"TESTING": True, "SECRET_KEY": "test"})
    response = app.test_client().get("/claims/resources/workflow")
    assert response.status_code == 302
    assert response.location == "https://riskatlas.co.za/resources/workflow"


def test_claims_are_session_scoped(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "claims.db")
    monkeypatch.setattr(db, "UPLOAD_DIR", tmp_path / "uploads")
    app = create_app({"TESTING": True, "SECRET_KEY": "test", "CLAIMHUB_ENABLE_CASES": True})
    claimant = app.test_client()
    created = claimant.post("/inbox", data={"claimant_name": "Private Person"})
    assert created.status_code == 302
    assert created.location == "/claim/1"
    assert b"Private Person" in claimant.get("/claim/1").data
    outsider = app.test_client()
    assert outsider.get("/claim/1").status_code == 404
    assert b"Private Person" not in outsider.get("/claimhub/clinician/case/1").data
