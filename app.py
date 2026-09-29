"""Standalone South African ClaimHub and ClaimBuddy Flask application."""

from __future__ import annotations

import os
import secrets
from datetime import timedelta

from flask import Flask, abort, redirect, render_template, request, session, url_for

import db
from blueprints.claimhub_bp import bp as claimhub_bp
from claimbuddy_runtime import register_claimbuddy_routes
from claimhub_product import PRODUCT_MODEL


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
        PRODUCT_MODEL=PRODUCT_MODEL,
    )
    if test_config:
        app.config.update(test_config)

    if app.config["CLAIMHUB_ENABLE_CASES"]:
        db.init_db()

    app.register_blueprint(claimhub_bp)
    register_claimbuddy_routes(app)

    @app.before_request
    def protect_case_data():
        path = request.path
        case_path = path.startswith("/claim/") or path.startswith("/documents/") or path.startswith("/api/claim/")
        case_write = path in {"/intake", "/compiler", "/inbox"} and request.method != "GET"
        professional_case = path.startswith("/claimhub/access/") or (
            path.startswith("/claimhub/") and "/case/" in path
        )
        if (case_path or case_write or professional_case) and not app.config["CLAIMHUB_ENABLE_CASES"]:
            abort(503, "Claim workspaces are awaiting production identity and storage setup.")

        if path.startswith("/claim/") or path.startswith("/api/claim/"):
            parts = path.split("/")
            try:
                claim_id = int(parts[2] if path.startswith("/claim/") else parts[3])
            except (IndexError, ValueError):
                return
            if claim_id not in session.get("owned_claim_ids", []):
                abort(404)

    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "service": "claimhubza",
            "cases_enabled": app.config["CLAIMHUB_ENABLE_CASES"],
        }

    @app.route("/")
    def claimsite_home():
        host = request.host.split(":", 1)[0].lower()
        if host in {"buddy.claimhub.co.za", "www.buddy.claimhub.co.za"}:
            return app.view_functions["inbox"]()
        return render_template("claimsite/home.html", product_model=PRODUCT_MODEL)

    @app.route("/claims")
    def legacy_claims():
        return redirect(url_for("claimsite_home"), code=308)

    @app.route("/claimbuddy")
    def claimbuddy_landing():
        return redirect(url_for("inbox"), code=302)

    @app.route("/claims/resources")
    def claimsite_resources():
        return render_template("claimsite/resources.html", product_model=PRODUCT_MODEL)

    # RiskAtlas owns reference intelligence. ClaimHub keeps compatibility
    # endpoint names so extracted templates can link out without importing
    # the RiskAtlas runtime or datasets.
    def riskatlas_redirect(path: str):
        def view(**values):
            rendered = path
            for key, value in values.items():
                rendered = rendered.replace(f"<{key}>", str(value))
            return redirect("https://riskatlas.co.za" + rendered, code=302)
        return view

    resource_rules = [
        ("/claims/resources/workflow", "resources_workflow", "/resources/workflow"),
        ("/claims/resources/evidence-gaps", "resources_evidence_gaps", "/resources/evidence-gaps"),
        ("/claims/resources/language", "resources_language_map", "/resources/language"),
        ("/claims/resources/language/<slug>", "resources_language_term", "/resources/language/<slug>"),
        ("/claims/resources/confusion/<slug>", "resources_confusion_detail", "/resources/confusion/<slug>"),
        ("/claims/resources/terms", "resources_terms", "/resources/terms"),
        ("/claims/resources/terms/<slug>", "resources_term_detail", "/resources/terms/<slug>"),
        ("/claims/resources/glossary", "resources_glossary", "/resources/glossary"),
        ("/claims/resources/glossary/<slug>", "resources_glossary_detail", "/resources/glossary/<slug>"),
        ("/claims/resources/traps", "resources_traps", "/resources/traps"),
        ("/claims/resources/traps/<slug>", "resources_trap_detail", "/resources/traps/<slug>"),
        ("/claims/resources/clinical-atlas", "resources_clinical_atlas", "/clinical-atlas/"),
        ("/claims/resources/life-insurers", "resources_life_insurers", "/resources/life-insurers"),
        ("/claims/resources/nfosa-dispute", "resources_nfosa_dispute", "/resources/nfosa-dispute"),
        ("/claims/resources/disability-definitions", "resources_disability_definitions", "/resources/disability-definitions"),
        ("/claims/resources/news", "resources_news", "/resources/news"),
        ("/claims/resources/precedent", "resources_precedent", "/resources/precedent"),
    ]
    for rule, endpoint, target in resource_rules:
        app.add_url_rule(rule, endpoint, riskatlas_redirect(target))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
