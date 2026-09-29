"""Full standalone ClaimBuddy runtime smoke tests."""

from __future__ import annotations

import db
from app import create_app


def _app(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "claimhub.db")
    monkeypatch.setattr(db, "UPLOAD_DIR", tmp_path / "uploads")
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "CLAIMHUB_ENABLE_CASES": True,
    })


def test_guided_intake_and_claim_modules_render(tmp_path, monkeypatch):
    app = _app(tmp_path, monkeypatch)
    client = app.test_client()

    intake = client.get("/intake")
    assert intake.status_code == 200
    assert b"Claim" in intake.data

    created = client.post(
        "/inbox",
        data={"claimant_name": "Standalone Person", "cover_type": "group"},
        follow_redirects=False,
    )
    assert created.status_code == 302
    assert created.location.endswith("/claim/1")

    dashboard = client.get("/claim/1")
    assert dashboard.status_code == 200
    assert b"Standalone Person" in dashboard.data

    for path in (
        "/claim/1/vault",
        "/claim/1/policy",
        "/claim/1/functional",
        "/claim/1/rejection",
        "/claim/1/gaps",
        "/claim/1/letters",
        "/claim/1/doctor",
        "/claim/1/pack",
        "/claim/1/access",
    ):
        response = client.get(path)
        assert response.status_code == 200, path


def test_claimhub_invitation_round_trip(tmp_path, monkeypatch):
    app = _app(tmp_path, monkeypatch)
    claimant = app.test_client()
    claimant.post("/inbox", data={"claimant_name": "Invite Person"})

    response = claimant.post(
        "/claim/1/access",
        data={
            "email": "adviser@example.test",
            "role": "adviser",
            "scopes": ["case.summary", "case.timeline"],
        },
    )
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    marker = "/claimhub/access/"
    assert marker in body
    token = body.split(marker, 1)[1].split("<", 1)[0].split("&", 1)[0].strip()
    assert token

    professional = app.test_client()
    accepted = professional.post(
        f"/claimhub/access/{token}",
        data={"email": "adviser@example.test", "display_name": "Adviser Example"},
        follow_redirects=True,
    )
    assert accepted.status_code == 200
    assert b"Invite Person" in accepted.data


def test_other_browser_cannot_open_claimant_case(tmp_path, monkeypatch):
    app = _app(tmp_path, monkeypatch)
    owner = app.test_client()
    owner.post("/inbox", data={"claimant_name": "Private Person"})

    outsider = app.test_client()
    assert outsider.get("/claim/1").status_code == 404
