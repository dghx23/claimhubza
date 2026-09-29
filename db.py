"""SQLite persistence for ClaimBuddy MVP."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("CLAIMHUB_DATA_DIR", str(ROOT / "data")))
DB_PATH = DATA_DIR / "claimguard.db"
UPLOAD_DIR = DATA_DIR / "uploads"

SCHEMA = """
CREATE TABLE IF NOT EXISTS claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    claim_stage TEXT DEFAULT 'preparing',
    employer TEXT,
    insurer TEXT,
    policyholder TEXT,
    policy_number TEXT,
    claim_reference TEXT,
    claimant_name TEXT,
    occupation TEXT,
    material_duties TEXT,
    illness_summary TEXT,
    waiting_period TEXT,
    benefit_percent TEXT,
    date_of_absence TEXT,
    insurer_doa TEXT,
    symptom_onset TEXT,
    cover_start TEXT,
    first_medical_cert TEXT,
    first_notice TEXT,
    form_submission TEXT,
    complete_claim TEXT,
    rejection_date TEXT,
    review_deadline TEXT,
    ombud_deadline TEXT,
    record_access_status TEXT,
    flags_json TEXT DEFAULT '[]',
    notes TEXT,
    gross_salary TEXT,
    net_salary TEXT,
    pay_frequency TEXT,
    earnings_basis TEXT,
    tax_deductions TEXT,
    pension_deductions TEXT,
    medical_aid_deductions TEXT,
    uif_deductions TEXT,
    other_deductions TEXT,
    salary_notes TEXT,
    policy_analysis_json TEXT,
    medical_diagnoses_json TEXT,
    medical_medications_json TEXT,
    medical_aid_history_note TEXT,
    medical_practitioners_json TEXT,
    medical_aids_json TEXT,
    occupation_profile_json TEXT,
    functional_capacity_json TEXT,
    rejection_analysis_json TEXT,
    policy_plan_type TEXT,
    jurisdiction TEXT DEFAULT 'za',
    cover_type TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    original_name TEXT NOT NULL,
    stored_name TEXT NOT NULL,
    doc_type TEXT DEFAULT 'other',
    notes TEXT,
    uploaded_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    last_seen_at TEXT
);
CREATE TABLE IF NOT EXISTS organisations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    org_type TEXT NOT NULL,
    jurisdiction TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS organisation_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organisation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    org_role TEXT NOT NULL DEFAULT 'member',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    UNIQUE (organisation_id, user_id),
    FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS case_memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    user_id INTEGER,
    organisation_id INTEGER,
    role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    invited_by_user_id INTEGER,
    created_at TEXT NOT NULL,
    accepted_at TEXT,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (organisation_id) REFERENCES organisations(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_case_memberships_claim ON case_memberships(claim_id);

CREATE TABLE IF NOT EXISTS invitations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL,
    organisation_id INTEGER,
    token_hash TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'pending',
    expires_at TEXT,
    created_at TEXT NOT NULL,
    accepted_at TEXT,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS consents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    grantee_user_id INTEGER,
    grantee_organisation_id INTEGER,
    grantee_role TEXT,
    scope TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    starts_at TEXT NOT NULL,
    expires_at TEXT,
    revoked_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_consents_claim ON consents(claim_id);

CREATE TABLE IF NOT EXISTS document_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    grantee_user_id INTEGER,
    grantee_organisation_id INTEGER,
    grantee_role TEXT,
    permission TEXT NOT NULL DEFAULT 'read',
    granted_by_user_id INTEGER,
    granted_at TEXT NOT NULL,
    revoked_at TEXT,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_document_permissions_claim ON document_permissions(claim_id);

CREATE TABLE IF NOT EXISTS information_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    requested_by_membership_id INTEGER,
    assigned_role TEXT,
    assigned_user_id INTEGER,
    assigned_organisation_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    due_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_information_requests_claim ON information_requests(claim_id);

CREATE TABLE IF NOT EXISTS information_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    responder_membership_id INTEGER,
    response_text TEXT,
    document_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES information_requests(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS case_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assigned_role TEXT,
    assigned_membership_id INTEGER,
    status TEXT NOT NULL DEFAULT 'open',
    due_at TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS case_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    author_membership_id INTEGER,
    body TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'case',
    created_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER,
    actor_user_id INTEGER,
    actor_membership_id INTEGER,
    event_type TEXT NOT NULL,
    target_type TEXT,
    target_id TEXT,
    details_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_audit_events_claim ON audit_events(claim_id, created_at);
CREATE TABLE IF NOT EXISTS disclosure_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    actor_membership_id INTEGER,
    recipient TEXT NOT NULL,
    purpose TEXT,
    scope_json TEXT DEFAULT '[]',
    created_at TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id) ON DELETE CASCADE
);
"""


_CLAIM_MIGRATIONS = [
    "gross_salary TEXT",
    "net_salary TEXT",
    "pay_frequency TEXT",
    "earnings_basis TEXT",
    "tax_deductions TEXT",
    "pension_deductions TEXT",
    "medical_aid_deductions TEXT",
    "uif_deductions TEXT",
    "other_deductions TEXT",
    "salary_notes TEXT",
    "policy_analysis_json TEXT",
    "medical_diagnoses_json TEXT",
    "medical_medications_json TEXT",
    "medical_aid_history_note TEXT",
    "medical_practitioners_json TEXT",
    "medical_aids_json TEXT",
    "occupation_profile_json TEXT",
    "functional_capacity_json TEXT",
    "rejection_analysis_json TEXT",
    "policy_plan_type TEXT",
    "jurisdiction TEXT DEFAULT 'za'",
    "cover_type TEXT",
]


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)
        existing = {row[1] for row in conn.execute("PRAGMA table_info(claims)")}
        for col_def in _CLAIM_MIGRATIONS:
            col_name = col_def.split()[0]
            if col_name not in existing:
                conn.execute(f"ALTER TABLE claims ADD COLUMN {col_def}")
        conn.commit()


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def list_claims() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, created_at, updated_at, claim_stage, employer, insurer, claim_reference, claimant_name, jurisdiction FROM claims ORDER BY updated_at DESC"
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_claim(claim_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
    return _row_to_dict(row) if row else None


def create_claim(data: dict) -> int:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    fields = {
        "created_at": now,
        "updated_at": now,
        **{k: data.get(k) for k in (
            "claim_stage", "employer", "insurer", "policyholder", "policy_number",
            "claim_reference", "claimant_name", "occupation", "material_duties",
            "illness_summary", "waiting_period", "benefit_percent", "date_of_absence",
            "insurer_doa", "symptom_onset", "cover_start", "first_medical_cert",
            "first_notice", "form_submission", "complete_claim", "rejection_date",
            "review_deadline", "ombud_deadline", "record_access_status", "notes",
            "gross_salary", "net_salary", "pay_frequency", "earnings_basis",
            "tax_deductions", "pension_deductions", "medical_aid_deductions",
            "uif_deductions", "other_deductions", "salary_notes",
            "policy_analysis_json",
            "medical_diagnoses_json", "medical_medications_json", "medical_aid_history_note",
            "medical_practitioners_json", "medical_aids_json",
            "occupation_profile_json",
            "functional_capacity_json",
            "rejection_analysis_json",
            "policy_plan_type",
            "jurisdiction",
            "cover_type",
        )},
        "flags_json": json.dumps(data.get("flags") or []),
    }
    if not fields.get("jurisdiction"):
        fields["jurisdiction"] = "za"
    cols = ", ".join(fields)
    placeholders = ", ".join("?" for _ in fields)
    with get_connection() as conn:
        cur = conn.execute(
            f"INSERT INTO claims ({cols}) VALUES ({placeholders})",
            list(fields.values()),
        )
        conn.commit()
        return int(cur.lastrowid)


def update_claim(claim_id: int, data: dict) -> None:
    from datetime import datetime, timezone

    allowed = {
        "claim_stage", "employer", "insurer", "policyholder", "policy_number",
        "claim_reference", "claimant_name", "occupation", "material_duties",
        "illness_summary", "waiting_period", "benefit_percent", "date_of_absence",
        "insurer_doa", "symptom_onset", "cover_start", "first_medical_cert",
        "first_notice", "form_submission", "complete_claim", "rejection_date",
        "review_deadline", "ombud_deadline", "record_access_status", "notes",
        "gross_salary", "net_salary", "pay_frequency", "earnings_basis",
        "tax_deductions", "pension_deductions", "medical_aid_deductions",
        "uif_deductions", "other_deductions", "salary_notes",
        "policy_analysis_json",
        "medical_diagnoses_json", "medical_medications_json", "medical_aid_history_note",
        "medical_practitioners_json", "medical_aids_json",
        "occupation_profile_json",
        "functional_capacity_json",
        "rejection_analysis_json",
        "policy_plan_type",
        "jurisdiction",
        "cover_type",
    }
    parts = ["updated_at = ?"]
    values: list[Any] = [datetime.now(timezone.utc).isoformat()]
    for key, val in data.items():
        if key == "flags":
            parts.append("flags_json = ?")
            values.append(json.dumps(val))
        elif key in allowed:
            parts.append(f"{key} = ?")
            values.append(val)
    values.append(claim_id)
    with get_connection() as conn:
        conn.execute(f"UPDATE claims SET {', '.join(parts)} WHERE id = ?", values)
        conn.commit()


def delete_claim(claim_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM claims WHERE id = ?", (claim_id,))
        conn.commit()


def list_documents(claim_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM documents WHERE claim_id = ? ORDER BY uploaded_at DESC",
            (claim_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_documents_by_type(claim_id: int, doc_type: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM documents WHERE claim_id = ? AND doc_type = ? ORDER BY uploaded_at DESC",
            (claim_id, doc_type),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def update_document_type(doc_id: int, doc_type: str, notes: str | None = None) -> None:
    with get_connection() as conn:
        if notes is None:
            conn.execute("UPDATE documents SET doc_type = ? WHERE id = ?", (doc_type, doc_id))
        else:
            conn.execute(
                "UPDATE documents SET doc_type = ?, notes = ? WHERE id = ?",
                (doc_type, notes, doc_id),
            )
        conn.commit()


def add_document(claim_id: int, original_name: str, stored_name: str, doc_type: str, notes: str = "") -> int:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO documents (claim_id, original_name, stored_name, doc_type, notes, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)",
            (claim_id, original_name, stored_name, doc_type, notes, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def delete_document(doc_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
        if row:
            conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            conn.commit()
            return _row_to_dict(row)
    return None

# ---------------------------------------------------------------------------
# ClaimHub identity / collaboration write helpers
# ---------------------------------------------------------------------------

def get_user(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return _row_to_dict(row) if row else None


def get_user_by_email(email: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE lower(email) = lower(?)",
            ((email or "").strip(),),
        ).fetchone()
    return _row_to_dict(row) if row else None


def get_or_create_user(email: str, display_name: str | None = None) -> dict:
    existing = get_user_by_email(email)
    if existing:
        if display_name and not existing.get("display_name"):
            with get_connection() as conn:
                conn.execute(
                    "UPDATE users SET display_name = ?, last_seen_at = ? WHERE id = ?",
                    (display_name, datetime.now(timezone.utc).isoformat(), existing["id"]),
                )
                conn.commit()
            return get_user(existing["id"]) or existing
        return existing
    user_id = create_user(email, display_name)
    return get_user(user_id) or {"id": user_id, "email": email, "display_name": display_name}


def create_user(email: str, display_name: str | None = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO users (email, display_name, status, created_at) VALUES (?, ?, 'active', ?)",
            (email.strip().lower(), display_name, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)


def create_invitation(
    claim_id: int,
    email: str,
    role: str,
    token_hash: str,
    *,
    organisation_id: int | None = None,
    expires_at: str | None = None,
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO invitations
               (claim_id, email, role, organisation_id, token_hash, status, expires_at, created_at)
               VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)""",
            (
                claim_id,
                email.strip().lower(),
                role,
                organisation_id,
                token_hash,
                expires_at,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_invitations(claim_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM invitations WHERE claim_id = ? ORDER BY created_at DESC",
            (claim_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_invitation_by_hash(token_hash: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM invitations WHERE token_hash = ? LIMIT 1",
            (token_hash,),
        ).fetchone()
    return _row_to_dict(row) if row else None


def accept_invitation(invitation_id: int, user_id: int) -> int:
    with get_connection() as conn:
        invitation = conn.execute(
            "SELECT * FROM invitations WHERE id = ?",
            (invitation_id,),
        ).fetchone()
        if not invitation:
            raise ValueError("Invitation not found")
        if invitation["status"] != "pending":
            existing = conn.execute(
                """SELECT id FROM case_memberships
                   WHERE claim_id = ? AND user_id = ? AND role = ?
                   ORDER BY id DESC LIMIT 1""",
                (invitation["claim_id"], user_id, invitation["role"]),
            ).fetchone()
            if existing:
                return int(existing["id"])
            raise ValueError("Invitation is no longer pending")
        now = datetime.now(timezone.utc).isoformat()
        cur = conn.execute(
            """INSERT INTO case_memberships
               (claim_id, user_id, organisation_id, role, status, created_at, accepted_at)
               VALUES (?, ?, ?, ?, 'active', ?, ?)""",
            (
                invitation["claim_id"],
                user_id,
                invitation["organisation_id"],
                invitation["role"],
                now,
                now,
            ),
        )
        conn.execute(
            "UPDATE invitations SET status = 'accepted', accepted_at = ? WHERE id = ?",
            (now, invitation_id),
        )
        conn.execute("UPDATE users SET last_seen_at = ? WHERE id = ?", (now, user_id))
        conn.commit()
        return int(cur.lastrowid)


def list_user_case_memberships(user_id: int, role: str | None = None) -> list[dict]:
    sql = """SELECT cm.*, c.claim_stage, c.claim_reference, c.policy_number,
                    c.claimant_name, c.employer, c.insurer, c.jurisdiction
             FROM case_memberships cm
             JOIN claims c ON c.id = cm.claim_id
             WHERE cm.user_id = ? AND cm.status = 'active'"""
    params: list[Any] = [user_id]
    if role:
        sql += " AND cm.role = ?"
        params.append(role)
    sql += " ORDER BY c.updated_at DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_dict(r) for r in rows]


def create_organisation(name: str, org_type: str, jurisdiction: str | None = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO organisations (name, org_type, jurisdiction, created_at) VALUES (?, ?, ?, ?)",
            (name, org_type, jurisdiction, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)


def add_case_membership(
    claim_id: int,
    role: str,
    *,
    user_id: int | None = None,
    organisation_id: int | None = None,
    invited_by_user_id: int | None = None,
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO case_memberships
               (claim_id, user_id, organisation_id, role, status, invited_by_user_id, created_at)
               VALUES (?, ?, ?, ?, 'active', ?, ?)""",
            (claim_id, user_id, organisation_id, role, invited_by_user_id, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)


def grant_consent(
    claim_id: int,
    scope: str,
    *,
    grantee_role: str | None = None,
    grantee_user_id: int | None = None,
    grantee_organisation_id: int | None = None,
    expires_at: str | None = None,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO consents
               (claim_id, grantee_user_id, grantee_organisation_id, grantee_role,
                scope, status, starts_at, expires_at, created_at)
               VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?)""",
            (claim_id, grantee_user_id, grantee_organisation_id, grantee_role, scope, now, expires_at, now),
        )
        conn.commit()
        return int(cur.lastrowid)


def grant_document_permission(
    claim_id: int,
    document_id: int,
    *,
    grantee_role: str | None = None,
    grantee_user_id: int | None = None,
    grantee_organisation_id: int | None = None,
    permission: str = "read",
    granted_by_user_id: int | None = None,
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO document_permissions
               (claim_id, document_id, grantee_user_id, grantee_organisation_id,
                grantee_role, permission, granted_by_user_id, granted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (claim_id, document_id, grantee_user_id, grantee_organisation_id,
             grantee_role, permission, granted_by_user_id, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)


# ---------------------------------------------------------------------------
# ClaimHub collaboration read model
# ---------------------------------------------------------------------------

def get_case_membership(claim_id: int, user_id: int, role: str | None = None) -> dict | None:
    sql = """SELECT cm.*, u.email, u.display_name, o.name AS organisation_name,
                    o.org_type AS organisation_type
             FROM case_memberships cm
             LEFT JOIN users u ON u.id = cm.user_id
             LEFT JOIN organisations o ON o.id = cm.organisation_id
             WHERE cm.claim_id = ? AND cm.user_id = ? AND cm.status = 'active'"""
    params: list[Any] = [claim_id, user_id]
    if role:
        sql += " AND cm.role = ?"
        params.append(role)
    sql += " ORDER BY cm.created_at DESC LIMIT 1"
    with get_connection() as conn:
        row = conn.execute(sql, params).fetchone()
    return _row_to_dict(row) if row else None


def list_case_memberships(claim_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT cm.*, u.email, u.display_name, o.name AS organisation_name,
                      o.org_type AS organisation_type
               FROM case_memberships cm
               LEFT JOIN users u ON u.id = cm.user_id
               LEFT JOIN organisations o ON o.id = cm.organisation_id
               WHERE cm.claim_id = ?
               ORDER BY cm.created_at ASC""",
            (claim_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_consents(claim_id: int, active_only: bool = True) -> list[dict]:
    sql = "SELECT * FROM consents WHERE claim_id = ?"
    if active_only:
        sql += " AND status = 'active' AND revoked_at IS NULL"
    sql += " ORDER BY created_at DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, (claim_id,)).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_document_permissions(claim_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM document_permissions WHERE claim_id = ? AND revoked_at IS NULL ORDER BY granted_at DESC",
            (claim_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_information_requests(claim_id: int, audience_role: str | None = None) -> list[dict]:
    sql = "SELECT * FROM information_requests WHERE claim_id = ?"
    params: list[Any] = [claim_id]
    if audience_role:
        sql += " AND (assigned_role IS NULL OR assigned_role = ?)"
        params.append(audience_role)
    sql += " ORDER BY CASE status WHEN 'open' THEN 0 ELSE 1 END, created_at DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_case_tasks(claim_id: int, audience_role: str | None = None) -> list[dict]:
    sql = "SELECT * FROM case_tasks WHERE claim_id = ?"
    params: list[Any] = [claim_id]
    if audience_role:
        sql += " AND (assigned_role IS NULL OR assigned_role = ?)"
        params.append(audience_role)
    sql += " ORDER BY CASE status WHEN 'open' THEN 0 ELSE 1 END, created_at DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_audit_events(claim_id: int, limit: int = 30) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_events WHERE claim_id = ? ORDER BY created_at DESC LIMIT ?",
            (claim_id, max(1, min(int(limit), 200))),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def case_collaboration_summary(claim_id: int, role: str | None = None) -> dict:
    return {
        "memberships": list_case_memberships(claim_id),
        "consents": list_consents(claim_id),
        "document_permissions": list_document_permissions(claim_id),
        "requests": list_information_requests(claim_id, role),
        "tasks": list_case_tasks(claim_id, role),
        "audit": list_audit_events(claim_id),
    }


# ---------------------------------------------------------------------------
# ClaimHub internal/admin snapshot
# ---------------------------------------------------------------------------

def claimhub_admin_snapshot() -> dict:
    """Small operational read model for the authenticated Sentrix backend."""
    with get_connection() as conn:
        counts = {}
        for table in (
            "claims",
            "documents",
            "users",
            "organisations",
            "case_memberships",
            "invitations",
            "consents",
            "document_permissions",
            "information_requests",
            "case_tasks",
            "audit_events",
            "disclosure_events",
        ):
            counts[table] = int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

        za_claims = int(
            conn.execute(
                "SELECT COUNT(*) FROM claims WHERE COALESCE(jurisdiction, 'za') = 'za'"
            ).fetchone()[0]
        )
        active_memberships = int(
            conn.execute(
                "SELECT COUNT(*) FROM case_memberships WHERE status = 'active'"
            ).fetchone()[0]
        )
        pending_invitations = int(
            conn.execute(
                "SELECT COUNT(*) FROM invitations WHERE status = 'pending'"
            ).fetchone()[0]
        )
        open_requests = int(
            conn.execute(
                "SELECT COUNT(*) FROM information_requests WHERE status = 'open'"
            ).fetchone()[0]
        )
        open_tasks = int(
            conn.execute(
                "SELECT COUNT(*) FROM case_tasks WHERE status = 'open'"
            ).fetchone()[0]
        )
        recent_claims = conn.execute(
            """SELECT id, claimant_name, claim_reference, insurer, claim_stage,
                      jurisdiction, updated_at
               FROM claims
               ORDER BY updated_at DESC
               LIMIT 10"""
        ).fetchall()
        recent_invitations = conn.execute(
            """SELECT id, claim_id, email, role, status, expires_at, created_at
               FROM invitations
               ORDER BY created_at DESC
               LIMIT 10"""
        ).fetchall()

    return {
        "counts": counts,
        "za_claims": za_claims,
        "active_memberships": active_memberships,
        "pending_invitations": pending_invitations,
        "open_requests": open_requests,
        "open_tasks": open_tasks,
        "recent_claims": [_row_to_dict(r) for r in recent_claims],
        "recent_invitations": [_row_to_dict(r) for r in recent_invitations],
    }
