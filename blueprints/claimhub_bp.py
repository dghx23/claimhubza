"""ClaimHub professional workspaces.

ClaimBuddy is the claimant-facing tool. ClaimHub is the role-based professional
coordination surface over the same claim record. These routes are still behind
the product soft-launch gate; production identity must bind an authenticated
user to a case_membership before external rollout.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

import db
from claimhub_access import (
    ADVISER,
    CLINICIAN,
    EMPLOYER,
    REVIEWER,
    PROFESSIONAL_ROLES,
    SCOPE_CASE_SUMMARY,
    SCOPE_DOCUMENTS,
    SCOPE_EMPLOYMENT,
    SCOPE_FUNCTION,
    SCOPE_MEDICAL,
    SCOPE_POLICY,
    SCOPE_TIMELINE,
    can,
    can_view_document,
    effective_scopes,
    workspace_label,
)
from claim_services import build_claim_context
from claimhub_product import PRODUCT_MODEL

bp = Blueprint("claimhub", __name__, url_prefix="/claimhub")

ROLE_META = {
    CLINICIAN: {
        "title": "ClaimHub for clinicians",
        "summary": "Respond to focused evidence requests without rewriting the claimant's own account.",
        "focus": ("functional impact", "medical evidence", "certificate and treatment dates"),
    },
    EMPLOYER: {
        "title": "ClaimHub for employers and HR",
        "summary": "Confirm employment facts, material duties and absence records around the claimant's case.",
        "focus": ("material duties", "employment records", "absence and return-to-work dates"),
    },
    ADVISER: {
        "title": "ClaimHub for advisers",
        "summary": "Review chronology, policy requirements, evidence gaps and escalation material in one case view.",
        "focus": ("policy", "chronology", "evidence gaps and escalation"),
    },
    REVIEWER: {
        "title": "ClaimHub for claims teams",
        "summary": "Receive claimant-authorised, structured evidence without altering the claimant's source record.",
        "focus": ("indexed evidence", "timeline", "outstanding requests"),
    },
}


def _role_or_404(role: str) -> str:
    role = (role or "").strip().lower()
    if role not in PROFESSIONAL_ROLES:
        abort(404)
    return role


def _consents_for_role(claim_id: int, role: str) -> list[dict]:
    return [
        row
        for row in db.list_consents(claim_id)
        if not row.get("grantee_role") or row.get("grantee_role") == role
    ]


def _document_permissions_for_role(claim_id: int, role: str) -> list[dict]:
    return [
        row
        for row in db.list_document_permissions(claim_id)
        if not row.get("grantee_role") or row.get("grantee_role") == role
    ]


def _safe_json(value: str | None, fallback):
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def _workspace_context(claim_id: int, role: str) -> dict:
    base = build_claim_context(claim_id)
    if not base:
        abort(404)
    claim = base["claim"]

    user_id = session.get("claimhub_user_id")
    membership = db.get_case_membership(claim_id, int(user_id), role) if user_id else None
    consents = _consents_for_role(claim_id, role) if membership else []
    permissions = _document_permissions_for_role(claim_id, role) if membership else []
    scopes = effective_scopes(role, consents) if membership else set()

    # Never expose claimant case fields merely because someone knows a case ID.
    # The professional needs both role capability and active claimant consent.
    summary_allowed = SCOPE_CASE_SUMMARY in scopes

    visible_documents = []
    if SCOPE_DOCUMENTS in scopes:
        for doc in base["documents"]:
            if can_view_document(
                role=role,
                document_id=doc["id"],
                consents=consents,
                permissions=permissions,
            ).allowed:
                visible_documents.append(doc)

    timeline = base["timeline"] if SCOPE_TIMELINE in scopes else []
    gaps = base["gaps"] if summary_allowed else []

    return {
        "role": role,
        "role_meta": ROLE_META[role],
        "membership": membership,
        "workspace_label": workspace_label(role),
        "claim_id": claim_id,
        "claim": claim if summary_allowed else None,
        "claim_label": (
            claim.get("claim_reference")
            or claim.get("policy_number")
            or f"Case {claim_id}"
        ) if summary_allowed else f"Case {claim_id}",
        "consents": consents,
        "scopes": sorted(scopes),
        "timeline": timeline,
        "gaps": gaps,
        "documents": visible_documents,
        "collaboration": db.case_collaboration_summary(claim_id, role),
        "medical": {
            "diagnoses": _safe_json(claim.get("medical_diagnoses_json"), []),
            "medications": _safe_json(claim.get("medical_medications_json"), []),
            "practitioners": _safe_json(claim.get("medical_practitioners_json"), []),
        } if SCOPE_MEDICAL in scopes else None,
        "functional": {
            "summary": claim.get("illness_summary"),
            "capacity": _safe_json(claim.get("functional_capacity_json"), {}),
        } if SCOPE_FUNCTION in scopes else None,
        "employment": {
            "employer": claim.get("employer"),
            "occupation": claim.get("occupation"),
            "material_duties": claim.get("material_duties"),
            "date_of_absence": claim.get("date_of_absence"),
        } if SCOPE_EMPLOYMENT in scopes else None,
        "policy": {
            "insurer": claim.get("insurer"),
            "policy_number": claim.get("policy_number"),
            "waiting_period": claim.get("waiting_period"),
            "analysis": _safe_json(claim.get("policy_analysis_json"), {}),
        } if SCOPE_POLICY in scopes else None,
        "access_notice": None if scopes else (
            "No active ClaimHub case membership and claimant-authorised scope are available "
            "for this session. Claim details remain hidden until identity, membership and consent align."
        ),
    }


@bp.route("")
@bp.route("/")
def index():
    return render_template(
        "claimhub/index.html",
        roles=ROLE_META,
        product_model=PRODUCT_MODEL,
        claimbuddy_url="/compiler",
    )


@bp.route("/<role>")
def role_home(role: str):
    role = _role_or_404(role)
    claim_id = request.args.get("claim", type=int)
    if claim_id:
        return render_template("claimhub/workspace.html", product_model=PRODUCT_MODEL, **_workspace_context(claim_id, role))
    user_id = session.get("claimhub_user_id")
    user = db.get_user(int(user_id)) if user_id else None
    cases = db.list_user_case_memberships(int(user_id), role) if user_id else []
    return render_template(
        "claimhub/role.html",
        role=role,
        role_meta=ROLE_META[role],
        workspace_label=workspace_label(role),
        claimhub_user=user,
        cases=cases,
        product_model=PRODUCT_MODEL,
    )


@bp.route("/<role>/case/<int:claim_id>")
def workspace(role: str, claim_id: int):
    role = _role_or_404(role)
    return render_template("claimhub/workspace.html", **_workspace_context(claim_id, role))


@bp.route("/access/<token>", methods=["GET", "POST"])
def accept_access(token: str):
    token_hash = hashlib.sha256((token or "").encode("utf-8")).hexdigest()
    invitation = db.get_invitation_by_hash(token_hash)
    if not invitation:
        return render_template("claimhub/invite.html", invitation=None, error="This access link is not valid."), 404

    if invitation.get("expires_at"):
        try:
            expires = datetime.fromisoformat(invitation["expires_at"])
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=timezone.utc)
            if expires < datetime.now(timezone.utc):
                return render_template("claimhub/invite.html", invitation=invitation, error="This access link has expired."), 410
        except (TypeError, ValueError):
            pass

    if invitation.get("status") == "accepted":
        return render_template("claimhub/invite.html", invitation=invitation, error="This access link has already been used."), 409

    error = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        display_name = (request.form.get("display_name") or "").strip() or None
        if email != (invitation.get("email") or "").strip().lower():
            error = "Use the email address this invitation was issued to."
        else:
            user = db.get_or_create_user(email, display_name)
            db.accept_invitation(invitation["id"], int(user["id"]))
            session["claimhub_user_id"] = int(user["id"])
            session.permanent = True
            return redirect(url_for("claimhub.workspace", role=invitation["role"], claim_id=invitation["claim_id"]))
    return render_template("claimhub/invite.html", invitation=invitation, error=error)


@bp.route("/logout")
def logout():
    session.pop("claimhub_user_id", None)
    return redirect(url_for("claimhub.index"))
