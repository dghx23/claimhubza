"""ClaimBuddy claimant workspace routes for standalone ClaimHub ZA."""

from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import abort, flash, jsonify, redirect, render_template, request, send_file, session, url_for

import db
from claim_services import build_claim_context
from claimhub_access import (
    ADVISER,
    CLINICIAN,
    EMPLOYER,
    REVIEWER,
    role_capabilities,
)
from compiler import (
    argument_view,
    clock_items,
    doa_conflict,
    file_title,
    guess_doc_type,
    parties_from_policy,
    policy_tests,
    stage_label as compiler_stage_label,
)
from engine import (
    DOC_TYPES,
    build_claim_pack,
    employer_record_letter,
    insurer_record_letter,
    review_request_letter,
    trustee_record_letter,
)
from functional_capacity_module import build_functional_capacity_view
from illness_story import (
    CONFUSION_GUARDS,
    DATE_LADDER,
    ILLNESS_DOMAINS,
    INTAKE_STORY_PHASES,
    PHASE_COACHING,
    PROMPT_CARDS,
    STORY_EXAMPLES,
    STORY_LADDER,
    STORY_PHASES,
    STORY_TYPES,
    SYMPTOM_DEFINITIONS,
    SYMPTOM_GROUPS,
    TIMELINE_CAPTURE_FIELDS,
)
from intake_options import (
    CLAIM_STAGE_TILES,
    POLICY_INSURER_TILES,
    WAITING_PERIOD_OPTIONS,
    WAITING_PERIOD_STANDARD,
)
from jurisdiction import profile as jurisdiction_profile, stage_labels as jurisdiction_stage_labels
from knowledge import WORKFLOW_STEPS, policy_traps_list
from medical_record import DOSE_FREQUENCIES, medical_aid_help, search_diagnoses, search_medications
from occupations import fetch_occupation_duties, search_occupations
from policy_processor import analyze_policy_file
from policy_reader import build_policy_reader_view, parse_policy_analysis, reanalyze_from_vault
from rejection_explainer import (
    build_rejection_explainer_view,
    parse_rejection_analysis,
    reanalyze_from_vault as reanalyze_rejection_from_vault,
)
from rejection_processor import analyze_rejection_file
from sa_reference_data import NFO_LIFE_INSURERS, resolve_insurer_name, search_employers, search_insurers

ALLOWED_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".txt", ".eml", ".msg"}
JOB_SPEC_DOC_TYPE = "job_spec"
PAYSLIP_DOC_TYPE = "payslip"
POLICY_DOC_TYPE = "policy"
REJECTION_DOC_TYPE = "rejection"
MEDICAL_AID_DOC_TYPE = "medical_aid_history"

INTAKE_FIELDS = (
    "claim_stage", "employer", "insurer", "policyholder", "policy_number",
    "claim_reference", "claimant_name", "occupation", "material_duties",
    "illness_summary", "waiting_period", "benefit_percent", "date_of_absence",
    "insurer_doa", "symptom_onset", "cover_start", "first_medical_cert",
    "first_notice", "form_submission", "complete_claim", "rejection_date",
    "review_deadline", "ombud_deadline", "record_access_status", "notes",
    "gross_salary", "net_salary", "pay_frequency", "earnings_basis",
    "tax_deductions", "pension_deductions", "medical_aid_deductions",
    "uif_deductions", "other_deductions", "salary_notes", "policy_analysis_json",
    "medical_diagnoses_json", "medical_medications_json", "medical_aid_history_note",
    "medical_practitioners_json", "medical_aids_json", "occupation_profile_json",
    "functional_capacity_json", "rejection_analysis_json", "policy_plan_type",
    "jurisdiction", "cover_type",
)

FILE_FIELDS = (
    "claimant_name", "employer", "insurer", "policyholder", "policy_number",
    "claim_reference", "occupation", "claim_stage", "date_of_absence",
    "insurer_doa", "waiting_period", "review_deadline", "ombud_deadline",
    "material_duties", "illness_summary", "jurisdiction", "cover_type",
)


def _parse_intake_form() -> dict:
    flags = []
    for key in ("hospital_admission", "specialist_required", "workers_comp"):
        if request.form.get(key):
            flags.append(key)
    data = {key: request.form.get(key) or None for key in INTAKE_FIELDS}
    data["jurisdiction"] = "za"
    insurer = data.get("insurer")
    if insurer == "__other__":
        data["insurer"] = (request.form.get("insurer_other") or "").strip() or None
    elif insurer:
        data["insurer"] = resolve_insurer_name(insurer) or insurer
    data["flags"] = flags
    return data


def _save_upload(claim_id: int, storage, doc_type: str, notes: str = "") -> str | None:
    if not storage or not storage.filename:
        return None
    ext = Path(storage.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return f"File type {ext} not allowed for {storage.filename}"
    stored = f"{uuid.uuid4().hex}{ext}"
    db.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    storage.save(db.UPLOAD_DIR / stored)
    db.add_document(claim_id, storage.filename, stored, doc_type, notes)
    return None


def _save_typed_uploads(claim_id: int, field: str, doc_type: str, note_field: str) -> list[str]:
    errors = []
    note = (request.form.get(note_field) or "").strip()
    for storage in request.files.getlist(field):
        err = _save_upload(claim_id, storage, doc_type, note)
        if err:
            errors.append(err)
    return errors


def _save_policy_uploads(claim_id: int) -> tuple[list[str], dict | None]:
    errors: list[str] = []
    analysis = None
    note = (request.form.get("policy_note") or "").strip()
    for storage in request.files.getlist("policy"):
        if not storage or not storage.filename:
            continue
        ext = Path(storage.filename).suffix.lower()
        if ext not in ALLOWED_EXT:
            errors.append(f"File type {ext} not allowed for {storage.filename}")
            continue
        stored = f"{uuid.uuid4().hex}{ext}"
        db.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        path = db.UPLOAD_DIR / stored
        storage.save(path)
        db.add_document(claim_id, storage.filename, stored, POLICY_DOC_TYPE, note)
        if analysis is None:
            analysis = analyze_policy_file(path, storage.filename)
    return errors, analysis


def _save_rejection_uploads(claim_id: int) -> tuple[list[str], dict | None]:
    errors: list[str] = []
    analysis = None
    note = (request.form.get("rejection_note") or "").strip()
    for storage in request.files.getlist("rejection"):
        if not storage or not storage.filename:
            continue
        ext = Path(storage.filename).suffix.lower()
        if ext not in ALLOWED_EXT:
            errors.append(f"File type {ext} not allowed for {storage.filename}")
            continue
        stored = f"{uuid.uuid4().hex}{ext}"
        db.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        path = db.UPLOAD_DIR / stored
        storage.save(path)
        db.add_document(claim_id, storage.filename, stored, REJECTION_DOC_TYPE, note)
        if analysis is None:
            analysis = analyze_rejection_file(path, storage.filename)
    return errors, analysis


def _merge_policy_analysis(data: dict, server_analysis: dict | None) -> None:
    if (data.get("policy_analysis_json") or "").strip():
        return
    if server_analysis and server_analysis.get("processed"):
        data["policy_analysis_json"] = json.dumps(server_analysis)


def _ingest_files(claim_id: int, files) -> tuple[int, dict | None, dict | None]:
    saved = 0
    policy_analysis = None
    rejection_analysis = None
    for storage in files:
        if not storage or not storage.filename:
            continue
        ext = Path(storage.filename).suffix.lower()
        if ext not in ALLOWED_EXT:
            flash(f"File type {ext} not allowed for {storage.filename}", "error")
            continue
        stored = f"{uuid.uuid4().hex}{ext}"
        db.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        path = db.UPLOAD_DIR / stored
        storage.save(path)
        doc_type = guess_doc_type(storage.filename)
        db.add_document(claim_id, storage.filename, stored, doc_type, "")
        saved += 1
        if doc_type in {"policy", "schedule"} and policy_analysis is None:
            policy_analysis = analyze_policy_file(path, storage.filename)
        if doc_type == "rejection" and rejection_analysis is None:
            rejection_analysis = analyze_rejection_file(path, storage.filename)
    return saved, policy_analysis, rejection_analysis


def _apply_scans(claim_id: int, policy_analysis: dict | None, rejection_analysis: dict | None) -> None:
    updates = {}
    claim = db.get_claim(claim_id) or {}
    if policy_analysis and policy_analysis.get("processed"):
        updates["policy_analysis_json"] = json.dumps(policy_analysis)
        merged = {**claim, **updates}
        for key, value in parties_from_policy(merged).items():
            if not (claim.get(key) or "").strip():
                updates[key] = value
    if rejection_analysis and rejection_analysis.get("processed"):
        updates["rejection_analysis_json"] = json.dumps(rejection_analysis)
        if not claim.get("claim_stage") or claim.get("claim_stage") == "preparing":
            updates["claim_stage"] = "rejected"
    if updates:
        db.update_claim(claim_id, updates)


def _workflow() -> list[tuple[str, str]]:
    return list(WORKFLOW_STEPS)


def _decorate_claim_row(claim: dict) -> dict:
    row = dict(claim)
    row["juris"] = jurisdiction_profile("za")
    row["stage_label"] = compiler_stage_label(row)
    return row


def _claim_context(claim_id: int) -> dict:
    context = build_claim_context(claim_id)
    if context is None:
        abort(404)
    return context


def register_claimbuddy_routes(app) -> None:
    @app.route("/compiler", methods=["GET", "POST"])
    @app.route("/inbox", methods=["GET", "POST"])
    def inbox():
        if request.method == "POST":
            claim_id = db.create_claim({
                "claimant_name": (request.form.get("claimant_name") or "").strip() or None,
                "cover_type": (request.form.get("cover_type") or "").strip() or None,
                "claim_stage": "preparing",
                "jurisdiction": "za",
            })
            saved, policy_analysis, rejection_analysis = _ingest_files(claim_id, request.files.getlist("files"))
            _apply_scans(claim_id, policy_analysis, rejection_analysis)
            session["owned_claim_ids"] = [*session.get("owned_claim_ids", []), claim_id]
            session.permanent = True
            if saved:
                flash(f"Compiled {saved} document{'s' if saved != 1 else ''} into a claim file.", "success")
            return redirect(url_for("dashboard", claim_id=claim_id))
        ids = session.get("owned_claim_ids", [])
        claims = [_decorate_claim_row(c) for cid in ids if (c := db.get_claim(cid))]
        return render_template(
            "compiler/inbox.html",
            claims=claims,
            product_model=app.config.get("PRODUCT_MODEL"),
            stage_labels=jurisdiction_stage_labels("za"),
            inbox_juris=jurisdiction_profile("za"),
            confusion_pairs=[],
            traps=policy_traps_list(),
            workflow=_workflow(),
            lang_term_count=0,
        )

    @app.route("/intake", methods=["GET", "POST"])
    def intake():
        if request.method == "POST":
            data = _parse_intake_form()
            claim_id = db.create_claim(data)
            session["owned_claim_ids"] = [*session.get("owned_claim_ids", []), claim_id]
            session.permanent = True
            for err in _save_typed_uploads(claim_id, "job_spec", JOB_SPEC_DOC_TYPE, "job_spec_note"):
                flash(err, "error")
            for err in _save_typed_uploads(claim_id, "payslip", PAYSLIP_DOC_TYPE, "payslip_note"):
                flash(err, "error")
            policy_errors, policy_analysis = _save_policy_uploads(claim_id)
            for err in policy_errors:
                flash(err, "error")
            for err in _save_typed_uploads(claim_id, "medical_aid_history", MEDICAL_AID_DOC_TYPE, "medical_aid_history_note"):
                flash(err, "error")
            _merge_policy_analysis(data, policy_analysis)
            if data.get("policy_analysis_json"):
                db.update_claim(claim_id, {"policy_analysis_json": data["policy_analysis_json"]})
            return redirect(url_for("dashboard", claim_id=claim_id))
        return render_template(
            "intake.html",
            juris=jurisdiction_profile("za"),
            stages=jurisdiction_stage_labels("za"),
            claim_stage_tiles=CLAIM_STAGE_TILES,
            job_specs=[], payslips=[], policies=[], policy_analysis=None,
            waiting_period_options=WAITING_PERIOD_OPTIONS,
            waiting_period_standard=WAITING_PERIOD_STANDARD,
            story_types=STORY_TYPES, story_phases=INTAKE_STORY_PHASES,
            story_ladder=STORY_LADDER, illness_prompts=PROMPT_CARDS,
            symptom_groups=SYMPTOM_GROUPS, symptom_definitions=SYMPTOM_DEFINITIONS,
            confusion_guards=CONFUSION_GUARDS, date_ladder=DATE_LADDER,
            timeline_capture_fields=TIMELINE_CAPTURE_FIELDS, illness_domains=ILLNESS_DOMAINS,
            phase_coaching=PHASE_COACHING, story_examples=STORY_EXAMPLES,
            medical_aid_help=medical_aid_help("za"), medical_aid_docs=[],
            policy_insurer_tiles=POLICY_INSURER_TILES, nfo_life_insurers=NFO_LIFE_INSURERS,
            fc_view=build_functional_capacity_view({}),
        )

    @app.route("/claim/<int:claim_id>", methods=["GET", "POST"])
    def dashboard(claim_id: int):
        if request.method == "POST":
            claim = db.get_claim(claim_id)
            if not claim:
                abort(404)
            data = {key: (request.form.get(key) or "").strip() or None for key in FILE_FIELDS}
            db.update_claim(claim_id, data)
            flash("File saved.", "success")
            return redirect(url_for("dashboard", claim_id=claim_id))
        ctx = _claim_context(claim_id)
        claim = ctx["claim"]
        return render_template(
            "compiler/file.html", **ctx, file_title=file_title(claim),
            conflict=doa_conflict(claim), clock=clock_items(claim),
            argument=argument_view(claim), policy_found=policy_tests(claim),
        )

    @app.route("/claim/<int:claim_id>/edit", methods=["GET", "POST"])
    def edit_claim(claim_id: int):
        claim = db.get_claim(claim_id)
        if not claim:
            abort(404)
        if request.method == "POST":
            data = _parse_intake_form()
            db.update_claim(claim_id, data)
            for err in _save_typed_uploads(claim_id, "job_spec", JOB_SPEC_DOC_TYPE, "job_spec_note"):
                flash(err, "error")
            for err in _save_typed_uploads(claim_id, "payslip", PAYSLIP_DOC_TYPE, "payslip_note"):
                flash(err, "error")
            policy_errors, policy_analysis = _save_policy_uploads(claim_id)
            for err in policy_errors:
                flash(err, "error")
            _merge_policy_analysis(data, policy_analysis)
            if data.get("policy_analysis_json"):
                db.update_claim(claim_id, {"policy_analysis_json": data["policy_analysis_json"]})
            flash("Claim updated.", "success")
            return redirect(url_for("dashboard", claim_id=claim_id))
        raw = claim.get("policy_analysis_json") or ""
        try:
            policy_analysis = json.loads(raw) if raw.strip() else None
        except json.JSONDecodeError:
            policy_analysis = None
        return render_template(
            "intake.html",
            juris=jurisdiction_profile("za"), stages=jurisdiction_stage_labels("za"),
            claim_stage_tiles=CLAIM_STAGE_TILES, claim=claim,
            flags=json.loads(claim.get("flags_json") or "[]"), editing=True,
            job_specs=db.list_documents_by_type(claim_id, JOB_SPEC_DOC_TYPE),
            payslips=db.list_documents_by_type(claim_id, PAYSLIP_DOC_TYPE),
            policies=db.list_documents_by_type(claim_id, POLICY_DOC_TYPE),
            policy_analysis=policy_analysis,
            waiting_period_options=WAITING_PERIOD_OPTIONS,
            waiting_period_standard=WAITING_PERIOD_STANDARD,
            story_types=STORY_TYPES, story_phases=INTAKE_STORY_PHASES,
            story_ladder=STORY_LADDER, illness_prompts=PROMPT_CARDS,
            symptom_groups=SYMPTOM_GROUPS, symptom_definitions=SYMPTOM_DEFINITIONS,
            confusion_guards=CONFUSION_GUARDS, date_ladder=DATE_LADDER,
            timeline_capture_fields=TIMELINE_CAPTURE_FIELDS, illness_domains=ILLNESS_DOMAINS,
            phase_coaching=PHASE_COACHING, story_examples=STORY_EXAMPLES,
            medical_aid_help=medical_aid_help("za"),
            medical_aid_docs=db.list_documents_by_type(claim_id, MEDICAL_AID_DOC_TYPE),
            policy_insurer_tiles=POLICY_INSURER_TILES, nfo_life_insurers=NFO_LIFE_INSURERS,
            fc_view=build_functional_capacity_view(claim),
        )

    @app.route("/claim/<int:claim_id>/vault", methods=["GET", "POST"])
    def vault(claim_id: int):
        ctx = _claim_context(claim_id)
        if request.method == "POST":
            files = [f for f in request.files.getlist("files") if f and f.filename]
            if not files:
                storage = request.files.get("file")
                files = [storage] if storage and storage.filename else []
            saved, policy_analysis, rejection_analysis = _ingest_files(claim_id, files)
            _apply_scans(claim_id, policy_analysis, rejection_analysis)
            if saved:
                flash(f"Added {saved} document{'s' if saved != 1 else ''}.", "success")
            return redirect(url_for("vault", claim_id=claim_id))
        return render_template("vault.html", **ctx, doc_types=DOC_TYPES)

    @app.route("/claim/<int:claim_id>/policy", methods=["GET", "POST"])
    def policy_reader(claim_id: int):
        ctx = _claim_context(claim_id)
        if request.method == "POST":
            if (request.form.get("action") or "upload") == "reanalyze":
                analysis = reanalyze_from_vault(claim_id, db.UPLOAD_DIR)
            else:
                errors, analysis = _save_policy_uploads(claim_id)
                for err in errors:
                    flash(err, "error")
            if analysis and analysis.get("processed"):
                db.update_claim(claim_id, {"policy_analysis_json": json.dumps(analysis)})
            return redirect(url_for("policy_reader", claim_id=claim_id))
        claim = ctx["claim"]
        analysis = parse_policy_analysis(claim)
        return render_template("policy.html", **ctx, reader=build_policy_reader_view(claim, ctx["documents"], analysis))

    @app.route("/claim/<int:claim_id>/functional")
    def functional_capacity(claim_id: int):
        ctx = _claim_context(claim_id)
        claim = ctx["claim"]
        return render_template(
            "functional.html", **ctx, fc_view=build_functional_capacity_view(claim),
            story_types=STORY_TYPES, story_phases=STORY_PHASES, story_ladder=STORY_LADDER,
            illness_prompts=PROMPT_CARDS, illness_domains=ILLNESS_DOMAINS,
            phase_coaching=PHASE_COACHING, story_examples=STORY_EXAMPLES,
            symptom_definitions=SYMPTOM_DEFINITIONS,
        )

    @app.route("/api/claim/<int:claim_id>/functional-capacity", methods=["POST"])
    def api_functional_capacity(claim_id: int):
        claim = db.get_claim(claim_id)
        if not claim:
            return jsonify({"error": "Claim not found"}), 404
        data = request.get_json(silent=True) or {}
        updates = {}
        if "functional_capacity_json" in data:
            updates["functional_capacity_json"] = data.get("functional_capacity_json") or ""
        if "illness_summary" in data:
            updates["illness_summary"] = data.get("illness_summary") or ""
        if updates:
            db.update_claim(claim_id, updates)
        fc_view = build_functional_capacity_view({**claim, **updates})
        return jsonify({"ok": True, "row_count": fc_view["row_count"], "statement": fc_view["statement"]})

    @app.route("/claim/<int:claim_id>/rejection", methods=["GET", "POST"])
    def rejection_explainer(claim_id: int):
        ctx = _claim_context(claim_id)
        if request.method == "POST":
            if (request.form.get("action") or "upload") == "reanalyze":
                analysis = reanalyze_rejection_from_vault(claim_id, db.UPLOAD_DIR)
            else:
                errors, analysis = _save_rejection_uploads(claim_id)
                for err in errors:
                    flash(err, "error")
            if analysis and analysis.get("processed"):
                db.update_claim(claim_id, {"rejection_analysis_json": json.dumps(analysis)})
            return redirect(url_for("rejection_explainer", claim_id=claim_id))
        claim = ctx["claim"]
        analysis = parse_rejection_analysis(claim)
        explainer = build_rejection_explainer_view(claim, ctx["documents"], analysis, gaps=ctx["gaps"], timeline=ctx["timeline"])
        return render_template("rejection.html", **ctx, explainer=explainer)

    @app.route("/claim/<int:claim_id>/gaps")
    def gaps(claim_id: int):
        return render_template("gaps.html", **_claim_context(claim_id))

    @app.route("/claim/<int:claim_id>/letters")
    def letters(claim_id: int):
        ctx = _claim_context(claim_id)
        claim, gaps_list, timeline = ctx["claim"], ctx["gaps"], ctx["timeline"]
        return render_template(
            "letters.html", **ctx,
            employer_letter=employer_record_letter(claim, gaps_list),
            insurer_letter=insurer_record_letter(claim),
            review_letter=review_request_letter(claim, gaps_list, timeline),
            trustee_letter=trustee_record_letter(claim),
        )

    @app.route("/claim/<int:claim_id>/doctor")
    def doctor(claim_id: int):
        return render_template("doctor.html", **_claim_context(claim_id))

    @app.route("/claim/<int:claim_id>/pack")
    def pack(claim_id: int):
        ctx = _claim_context(claim_id)
        content = build_claim_pack(ctx["claim"], ctx["timeline"], ctx["gaps"], ctx["checklist"], ctx["documents"])
        return render_template("pack.html", **ctx, pack_content=content)

    @app.route("/claim/<int:claim_id>/pack/download")
    def pack_download(claim_id: int):
        ctx = _claim_context(claim_id)
        content = build_claim_pack(ctx["claim"], ctx["timeline"], ctx["gaps"], ctx["checklist"], ctx["documents"])
        path = db.DATA_DIR / f"pack-{claim_id}.md"
        path.write_text(content, encoding="utf-8")
        return send_file(path, as_attachment=True, download_name=f"claimbuddy-pack-{claim_id}.md")

    @app.route("/claim/<int:claim_id>/access", methods=["GET", "POST"])
    def claim_access(claim_id: int):
        claim = db.get_claim(claim_id)
        if not claim:
            abort(404)
        role_labels = {CLINICIAN:"Clinician", EMPLOYER:"Employer / HR", ADVISER:"Adviser", REVIEWER:"Claims reviewer"}
        documents = db.list_documents(claim_id)
        invite_url = None
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            role = (request.form.get("role") or "").strip().lower()
            requested_scopes = request.form.getlist("scopes")
            if not email or role not in role_labels:
                flash("Enter an email address and choose a valid ClaimHub role.", "error")
            else:
                scopes = [scope for scope in requested_scopes if scope in role_capabilities(role)]
                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
                expires_at = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
                db.create_invitation(claim_id, email, role, token_hash, expires_at=expires_at)
                for scope in scopes:
                    db.grant_consent(claim_id, scope, grantee_role=role, expires_at=expires_at)
                if "case.documents" in scopes:
                    valid_ids = {doc["id"] for doc in documents}
                    for value in request.form.getlist("documents"):
                        if value.isdigit() and int(value) in valid_ids:
                            db.grant_document_permission(claim_id, int(value), grantee_role=role, permission="read")
                invite_url = url_for("claimhub.accept_access", token=token, _external=True)
                flash("ClaimHub access invitation created.", "success")
        return render_template(
            "claim_access.html", claim=claim, documents=documents,
            invitations=db.list_invitations(claim_id), role_labels=role_labels,
            role_scopes={role: sorted(role_capabilities(role)) for role in role_labels},
            invite_url=invite_url,
        )

    @app.route("/claim/<int:claim_id>/delete", methods=["POST"])
    def delete_claim(claim_id: int):
        db.delete_claim(claim_id)
        owned = [cid for cid in session.get("owned_claim_ids", []) if cid != claim_id]
        session["owned_claim_ids"] = owned
        return redirect(url_for("inbox"))

    @app.route("/documents/<int:doc_id>/delete", methods=["POST"])
    def delete_document(doc_id: int):
        with db.get_connection() as conn:
            row = conn.execute("SELECT claim_id FROM documents WHERE id = ?", (doc_id,)).fetchone()
        if not row or int(row["claim_id"]) not in session.get("owned_claim_ids", []):
            abort(404)
        doc = db.delete_document(doc_id)
        if not doc:
            abort(404)
        (db.UPLOAD_DIR / doc["stored_name"]).unlink(missing_ok=True)
        return redirect(url_for("vault", claim_id=doc["claim_id"]))

    @app.route("/api/occupations/search")
    def api_occupation_search():
        q = request.args.get("q", "")
        return jsonify({"query": q, "results": search_occupations(q, limit=10), "source": "ESCO"})

    @app.route("/api/occupations/duties")
    def api_occupation_duties():
        result = fetch_occupation_duties(request.args.get("uri", ""))
        return (jsonify(result) if result else (jsonify({"error":"Occupation not found"}), 404))

    @app.route("/api/insurers/search")
    def api_insurer_search():
        q = request.args.get("q", "")
        return jsonify({"query": q, "results": search_insurers(q), "source": "za"})

    @app.route("/api/employers/search")
    def api_employer_search():
        q = request.args.get("q", "")
        return jsonify({"query": q, "results": search_employers(q), "source": "za"})

    @app.route("/api/diagnoses/search")
    def api_diagnosis_search():
        q = request.args.get("q", "")
        return jsonify({"query": q, "results": search_diagnoses(q)})

    @app.route("/api/medications/search")
    def api_medication_search():
        q = request.args.get("q", "")
        return jsonify({"query": q, "results": search_medications(q)})

    @app.route("/api/medications/meta")
    def api_medication_meta():
        return jsonify({"frequencies": DOSE_FREQUENCIES})
