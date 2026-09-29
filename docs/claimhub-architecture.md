# ClaimHub / RiskAtlas platform boundary

## Product roles

**Sentrix Digital** is the parent organisation, portfolio website, and internal product/backend environment. It may describe ClaimHub, surface architecture/status information, and administer shared systems, but the public ClaimHub product experience is standalone.

**ClaimHub** is the claims coordination platform. It owns case identity, professional participation, permissions, consent, information requests, responses, tasks, comments, disclosure events and audit history.

**ClaimBuddy** is the claimant-facing experience inside the ClaimHub product family. Claimants organise their own evidence, timeline, functional impact, policy requirements, evidence gaps and claim pack. Public treatment: **ClaimBuddy — by claimhub.co.za**.

**RiskAtlas** is shared reference intelligence. It supplies country cores, clinical knowledge, occupations, terminology, insurer/scheme directories, policy/dispute pathways and social-security reference data. RiskAtlas does not own live multi-party claim collaboration.

## Case boundary

The existing `claims` row remains the case nucleus. ClaimHub adds participants and permissions around that row.

A professional must not gain access merely by knowing a case ID or by holding a professional role. Effective access is the intersection of:

1. an authenticated user;
2. an active case membership;
3. the role capability ceiling;
4. active claimant consent; and
5. document-level permission where a specific document is involved.

Claimants and case administrators manage the case boundary. Clinicians, employers, advisers and claims reviewers contribute responses or source evidence; they do not overwrite the claimant's own narrative.

## Workspace roles

- Clinician: medical evidence, functional impact, certificate/treatment dates.
- Employer / HR: employment facts, material duties, absence and return-to-work dates.
- Adviser: chronology, policy, evidence gaps and escalation material.
- Claims reviewer / insurer: claimant-authorised indexed evidence, timeline and outstanding requests.
- Claimant: ClaimBuddy, not the professional ClaimHub UI.

## Repository direction

ClaimHub should deploy as its own standalone public product surface at claimhub.co.za. SentrixDigital remains the portfolio/informational site and internal backend environment. RiskAtlas should progressively become the source/reference package or service consumed by ClaimHub/Sentrix services rather than a second independently evolving copy of the product application.

Do not remove duplicated runtime code in a single destructive migration. Move shared reference modules in controlled slices, add tests at each boundary, and keep imports backwards-compatible until consumers have moved.

## Privacy / analytics

Any future system-level analytics must use appropriately de-identified/aggregated data and must not expose claimant-level information. Analytics is downstream of the consent and audit model, not a substitute for it.


## Private-beta participation flow

The branch now includes an end-to-end private-beta access path:

1. The claimant-side ClaimBuddy workspace exposes an **Access** screen on a claim.
2. A participant is invited by email address and role.
3. The claimant selects permitted scopes and, where document access is granted, the specific documents to share.
4. ClaimHub stores only a hash of the raw invitation token and creates a seven-day acceptance link.
5. The participant accepts through ClaimHub, which creates or links their professional user record and activates a case membership.
6. The professional workspace resolves case data only when session identity, active membership, role capability and claimant consent all align.
7. Individual documents additionally require an explicit document permission.

This flow is deliberately still labelled private beta because ClaimBuddy claimant identity is still protected by the product gate rather than a production claimant account/session model, and invitation delivery is manual rather than connected to an email provider.


## Public-site separation

The public web architecture is intentionally split:

- **sentrixdigital.com** — organisation, portfolio, product information, thought leadership, architecture/status views, and internal/admin backend surfaces.
- **claimhub.co.za** — standalone ClaimHub marketing front door explaining the cover context, initiation paths, product family and resources.
- **ClaimBuddy** — claimant-facing application branded **ClaimBuddy — by claimhub.co.za**. It is the claimant view of the shared case.
- **ClaimHub professional portal** — role-specific clinician, employer/HR, adviser and claims-team workspaces around that same case.
- **RiskAtlas / Core ZA** — reference/intelligence layer that remains separate from live collaboration and is consumed by ClaimBuddy/ClaimHub at runtime.

The Sentrix site may link to ClaimHub and explain how it works, but ClaimHub should not inherit Sentrix's public visual shell.


## Integrated public / product / backend surfaces

The ClaimHub family now has three deliberately connected surfaces:

- **Marketing front door (`/claims`, root of claimhub.co.za):** explains the product family and routes visitors by role.
- **ClaimBuddy (`/compiler`, `/intake`, `/claim/...`):** claimant-facing South African claim workspace.
- **ClaimHub (`/claimhub/...`):** professional role workspaces connected to claimant-authorised access.
- **Sentrix backend (`/backend/claimhub`):** authenticated operational/control-room view over claims, documents, memberships, invitations, requests and product links.

The public marketing site does not own case state. ClaimBuddy and ClaimHub operate over the same backend case model. Sentrix retains the internal operational and architecture view, while RiskAtlas/Core remain the reference/intelligence sources consumed by the product.


## Multi-party case initiation

A ClaimHub case does not have to be initiated by the claimant. The product model supports multiple initiation paths, including claimant-led, employer/HR-led, adviser-led, and the organisation of an already-open claim. The initiation source must not create a professional-only shadow file.

**ClaimBuddy is the claimant-facing side of every case.** When a professional initiates or imports a case, the intended production flow is to create the shared case record and activate/link the claimant into ClaimBuddy so the claimant can see the case, understand its status, and control ongoing participation and sharing. Professional initiation therefore changes who starts the workflow, not who owns visibility of the claimant record.

For South Africa, intake must also distinguish the broad cover context early: **group cover** connected to employment or another group arrangement, versus **individual cover** arranged for the individual. The exact rights, parties, evidence requirements and policy tests remain driven by the actual wording and facts of the specific claim.

The current private-beta code has claimant-created workspaces and professional invitation acceptance. Full production-grade professional-led initiation plus authenticated claimant activation/linking remains an implementation step; marketing copy should describe the product model without implying that the production identity handoff is already complete.


## Poster-aligned canonical architecture

The canonical presentation model lives in `claimhub_product.py` and is intentionally the same across the public site, product navigation, backend control room and architecture map.

1. **Context:** South African income protection can begin from group cover or individual cover.
2. **Initiation:** claimant, employer/HR, adviser, or an already-open claim can be the first entry point.
3. **Shared case:** all paths converge on one case record containing policy, timeline, function, evidence, requests and decisions.
4. **Connected products:** ClaimBuddy is the claimant workspace; ClaimHub is the professional workspace layer.
5. **Resources:** workflow, policy terms, language, evidence gaps, disability definitions, ClinicalAtlas and NFO/ombud material explain the reference context behind the case.
6. **Product surfaces:** claimhub.co.za marketing front door → ClaimBuddy claimant application / ClaimHub professional portal.
7. **Internal layer:** Sentrix backend is the operational/control-room surface; RiskAtlas/Core ZA is reference intelligence.

The data boundary remains important: the marketing site owns no live claim state, RiskAtlas owns no live collaboration state, and ClaimBuddy/ClaimHub are different authorised views over the same live case model.


## Technical cross-reference map

The Sentrix backend exposes an interactive backend twin of the marketing poster at `/backend/claimhub/technical-map`.

It is generated from `PRODUCT_MODEL["technical_references"]` in `claimhub_product.py`, so the numbered marketing poster sections and the internal implementation view share the same canonical reference model. Clicking a poster section opens its routes, templates, code owners, data/state and verification references.

For each public visual section the backend records:

- public route/anchor;
- canonical templates;
- code owners;
- live data/state tables or domains;
- supporting documentation/tests;
- implementation status.

The seven canonical poster sections are:

1. market challenge / why claims become difficult;
2. income-protection cover context;
3. claim initiation paths;
4. one shared case / ClaimBuddy + ClaimHub;
5. ClaimHub Resources;
6. RiskAtlas intelligence;
7. Sentrix Digital builder/operator layer.

When a public section changes materially, update its `TECHNICAL_REFERENCE_MAP` entry in the same change. The broader ingestion topology remains in `templates/backend/architecture.html`; the technical map is the product-facing cross-reference layer.
