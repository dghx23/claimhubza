"""ClaimHub role, consent, and workspace policy."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Mapping

CLAIMANT="claimant"; CLINICIAN="clinician"; EMPLOYER="employer"; ADVISER="adviser"; REVIEWER="reviewer"; CASE_ADMIN="case_admin"
CASE_ROLES={CLAIMANT,CLINICIAN,EMPLOYER,ADVISER,REVIEWER,CASE_ADMIN}
PROFESSIONAL_ROLES={CLINICIAN,EMPLOYER,ADVISER,REVIEWER}
SCOPE_CASE_SUMMARY="case.summary"; SCOPE_POLICY="case.policy"; SCOPE_TIMELINE="case.timeline"; SCOPE_FUNCTION="case.function"; SCOPE_MEDICAL="case.medical"; SCOPE_EMPLOYMENT="case.employment"; SCOPE_DOCUMENTS="case.documents"; SCOPE_REQUESTS="case.requests"; SCOPE_TASKS="case.tasks"; SCOPE_COMMENTS="case.comments"; SCOPE_EXPORT="case.export"; SCOPE_ADMIN="case.admin"
ALL_SCOPES={SCOPE_CASE_SUMMARY,SCOPE_POLICY,SCOPE_TIMELINE,SCOPE_FUNCTION,SCOPE_MEDICAL,SCOPE_EMPLOYMENT,SCOPE_DOCUMENTS,SCOPE_REQUESTS,SCOPE_TASKS,SCOPE_COMMENTS,SCOPE_EXPORT,SCOPE_ADMIN}
ROLE_CAPABILITIES={
 CLAIMANT:set(ALL_SCOPES), CASE_ADMIN:set(ALL_SCOPES),
 CLINICIAN:{SCOPE_CASE_SUMMARY,SCOPE_TIMELINE,SCOPE_FUNCTION,SCOPE_MEDICAL,SCOPE_DOCUMENTS,SCOPE_REQUESTS,SCOPE_TASKS,SCOPE_COMMENTS},
 EMPLOYER:{SCOPE_CASE_SUMMARY,SCOPE_TIMELINE,SCOPE_EMPLOYMENT,SCOPE_DOCUMENTS,SCOPE_REQUESTS,SCOPE_TASKS,SCOPE_COMMENTS},
 ADVISER:{SCOPE_CASE_SUMMARY,SCOPE_POLICY,SCOPE_TIMELINE,SCOPE_FUNCTION,SCOPE_EMPLOYMENT,SCOPE_DOCUMENTS,SCOPE_REQUESTS,SCOPE_TASKS,SCOPE_COMMENTS,SCOPE_EXPORT},
 REVIEWER:{SCOPE_CASE_SUMMARY,SCOPE_POLICY,SCOPE_TIMELINE,SCOPE_FUNCTION,SCOPE_MEDICAL,SCOPE_EMPLOYMENT,SCOPE_DOCUMENTS,SCOPE_REQUESTS,SCOPE_TASKS,SCOPE_COMMENTS,SCOPE_EXPORT},
}
WORKSPACE_LABELS={CLAIMANT:"ClaimBuddy",CLINICIAN:"Clinical workspace",EMPLOYER:"Employer / HR workspace",ADVISER:"Adviser workspace",REVIEWER:"Claims review workspace",CASE_ADMIN:"Case administration"}

@dataclass(frozen=True)
class AccessDecision:
    allowed: bool
    reason: str

def normalize_role(role:str|None)->str:
    value=(role or "").strip().lower()
    return value if value in CASE_ROLES else ""

def role_capabilities(role:str|None)->set[str]:
    return set(ROLE_CAPABILITIES.get(normalize_role(role),set()))

def active_consent_scopes(consents:Iterable[Mapping])->set[str]:
    scopes=set()
    for consent in consents:
        if (consent.get("status") or "active")!="active" or consent.get("revoked_at"):
            continue
        raw=consent.get("scope")
        if isinstance(raw,str):
            scopes.update(x.strip() for x in raw.split(",") if x.strip())
        elif isinstance(raw,(list,tuple,set)):
            scopes.update(str(x).strip() for x in raw if str(x).strip())
    return scopes

def effective_scopes(role:str|None,consents:Iterable[Mapping]=())->set[str]:
    role=normalize_role(role); caps=role_capabilities(role)
    if role in {CLAIMANT,CASE_ADMIN}: return caps
    return caps & active_consent_scopes(consents)

def can(role:str|None,scope:str,consents:Iterable[Mapping]=())->AccessDecision:
    if scope not in ALL_SCOPES: return AccessDecision(False,"Unknown ClaimHub access scope")
    role=normalize_role(role)
    if not role: return AccessDecision(False,"No active case role")
    if scope not in role_capabilities(role): return AccessDecision(False,f"The {role} role does not include {scope}")
    if role in {CLAIMANT,CASE_ADMIN}: return AccessDecision(True,"Case owner/administrator capability")
    if scope not in active_consent_scopes(consents): return AccessDecision(False,"Claimant consent has not granted this scope")
    return AccessDecision(True,"Role capability and active claimant consent")

def can_view_document(*,role:str|None,document_id:int,consents:Iterable[Mapping]=(),permissions:Iterable[Mapping]=())->AccessDecision:
    base=can(role,SCOPE_DOCUMENTS,consents)
    if not base.allowed: return base
    role=normalize_role(role)
    if role in {CLAIMANT,CASE_ADMIN}: return base
    for permission in permissions:
        if int(permission.get("document_id") or 0)==int(document_id) and not permission.get("revoked_at") and (permission.get("permission") or "read") in {"read","write","manage"}:
            return AccessDecision(True,"Document permission and consent are active")
    return AccessDecision(False,"This document has not been shared with the professional")

def workspace_label(role:str|None)->str:
    return WORKSPACE_LABELS.get(normalize_role(role),"ClaimHub")
