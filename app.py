"""Standalone South African ClaimHub and ClaimBuddy Flask application."""

from __future__ import annotations

import os
import secrets
from datetime import timedelta

from flask import Flask, abort, redirect, render_template, request, session, url_for

import db
from blueprints.claimhub_bp import bp as claimhub_bp
from claimhub_product import PRODUCT_MODEL
from jurisdiction import profile, stage_labels


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        MAX_CONTENT_LENGTH=32 * 1024 * 1024,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production",
        CLAIMHUB_ENABLE_CASES=os.environ.get("CLAIMHUB_ENABLE_CASES") == "1",
    )
    if test_config:
        app.config.update(test_config)
    if app.config["CLAIMHUB_ENABLE_CASES"]:
        db.init_db()
    app.register_blueprint(claimhub_bp)

    @app.before_request
    def protect_case_data():
        path = request.path
        if path.startswith("/claim/") or path == "/intake" or (path in {"/compiler", "/inbox"} and request.method != "GET"):
            if not app.config["CLAIMHUB_ENABLE_CASES"]:
                abort(503, "Claim workspaces are awaiting production identity and storage setup.")
        if path.startswith("/claimhub/access/") or "/case/" in path and path.startswith("/claimhub/"):
            if not app.config["CLAIMHUB_ENABLE_CASES"]:
                abort(503, "Professional case access is awaiting production identity and storage setup.")
        if path.startswith("/claim/"):
            try:
                claim_id = int(path.split("/")[2])
            except (IndexError, ValueError):
                abort(404)
            if claim_id not in session.get("owned_claim_ids", []):
                abort(404)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "claimhubza", "cases_enabled": app.config["CLAIMHUB_ENABLE_CASES"]}

    @app.route("/")
    def claimsite_home():
        if request.host.split(":", 1)[0].lower() in {"buddy.claimhub.co.za", "www.buddy.claimhub.co.za"}:
            return inbox()
        return render_template("claimsite/home.html", product_model=PRODUCT_MODEL)

    @app.route("/claims")
    def legacy_claims():
        return redirect(url_for("claimsite_home"), code=308)

    @app.route("/claims/resources")
    def claimsite_resources():
        return render_template("claimsite/resources.html", product_model=PRODUCT_MODEL)

    @app.route("/compiler", methods=["GET", "POST"])
    @app.route("/inbox", methods=["GET", "POST"])
    def inbox():
        if not app.config["CLAIMHUB_ENABLE_CASES"] and request.method != "GET":
            abort(503, "Claim workspaces are awaiting production identity and storage setup.")
        if request.method == "POST":
            claim_id = db.create_claim({
                "claimant_name": (request.form.get("claimant_name") or "").strip() or None,
                "cover_type": (request.form.get("cover_type") or "").strip() or None,
                "claim_stage": "preparing",
                "jurisdiction": "za",
            })
            session["owned_claim_ids"] = [*session.get("owned_claim_ids", []), claim_id]
            session.permanent = True
            return redirect(url_for("dashboard", claim_id=claim_id))
        ids = session.get("owned_claim_ids", []) if app.config["CLAIMHUB_ENABLE_CASES"] else []
        claims = [db.get_claim(cid) for cid in ids]
        return render_template(
            "compiler/inbox.html", claims=[c for c in claims if c],
            product_model=PRODUCT_MODEL, stage_labels=stage_labels("za"),
            inbox_juris=profile("za"), confusion_pairs=[], traps=[],
            workflow=[], lang_term_count=0,
        )

    @app.route("/intake", methods=["GET", "POST"])
    def intake():
        if request.method == "POST":
            return inbox()
        return redirect(url_for("inbox") + "#upload")

    @app.route("/claim/<int:claim_id>")
    def dashboard(claim_id: int):
        from claim_services import build_claim_context
        context = build_claim_context(claim_id)
        if context is None:
            abort(404)
        return render_template("claimbuddy/case.html", **context)

    @app.route("/claim/<int:claim_id>/access")
    def claim_access(claim_id: int):
        return render_template("claimbuddy/case.html", **_case_context(claim_id))

    @app.route("/claim/<int:claim_id>/vault")
    def vault(claim_id: int):
        return render_template("claimbuddy/case.html", **_case_context(claim_id))

    @app.route("/claim/<int:claim_id>/policy")
    def policy_reader(claim_id: int):
        return render_template("claimbuddy/case.html", **_case_context(claim_id))

    @app.route("/claim/<int:claim_id>/functional")
    def functional_capacity(claim_id: int):
        return render_template("claimbuddy/case.html", **_case_context(claim_id))

    def _case_context(claim_id: int) -> dict:
        from claim_services import build_claim_context
        context = build_claim_context(claim_id)
        if context is None:
            abort(404)
        return context

    @app.route("/claimbuddy")
    def claimbuddy_landing():
        return redirect(url_for("inbox"))

    # The reference library remains owned by RiskAtlas. Preserve product links
    # without copying its datasets or exposing Sentrix administrative routes.
    resource_paths = {
        "resources_clinical_atlas": "clinical-atlas",
        "resources_disability_definitions": "disability-definitions",
        "resources_evidence_gaps": "evidence-gaps",
        "resources_language_map": "language",
        "resources_life_insurers": "life-insurers",
        "resources_nfosa_dispute": "nfosa-dispute",
        "resources_terms": "terms",
        "resources_workflow": "workflow",
        "resources_glossary": "glossary",
        "resources_news": "news",
        "resources_precedent": "precedent",
        "resources_traps": "traps",
    }
    for endpoint, suffix in resource_paths.items():
        app.add_url_rule(
            f"/claims/resources/{suffix}", endpoint,
            lambda suffix=suffix: redirect(f"https://riskatlas.co.za/resources/{suffix}", code=302),
        )
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
