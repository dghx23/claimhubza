# ClaimHub ZA extraction record

Source reviewed: `dghx23/SentrixDigital` local `main` at `45b660fbf4850f8cac65ba58916cf9fbd0742672` (2026-09-30 03:21 +10). The local `claimhub-platform` branch is older (`627989f`, 2026-09-19); its ClaimHub files match main apart from changes in the shared database. The local RiskAtlas checkout points at `SentrixDigital` as its remote and has the same ClaimHub file set in `origin/main`, `origin/migration/riskatlas-canonical-host`, and `origin/split/au-za-domains`. No separate `dghx23/riskatlas` remote content could be verified during this run.

## Source inventory

| Area | Extracted files |
| --- | --- |
| ClaimHub routes and access | `blueprints/claimhub_bp.py`, `claimhub_access.py`, `claimhub_product.py`, `claim_services.py`, `db.py` |
| ClaimBuddy processing | `compiler.py`, `engine.py`, `functional_capacity.py`, `functional_capacity_module.py`, `functional_map.py`, `illness_story.py`, `intake_options.py`, `medical_record.py`, `policy_processor.py`, `policy_reader.py` |
| Supporting claim knowledge | `content_data.py`, `content_data_extra.py`, `knowledge.py`, `language_map.py`, `term_slugs.py`, `sa_reference_data.py`, `jurisdiction.py` |
| Templates | `templates/claimsite/*`, `templates/claimhub/*`, `templates/claimbuddy/*`, `templates/compiler/*`, `templates/claim_access.html`, `templates/intake.html`, `templates/vault.html`, `templates/policy.html`, `templates/functional.html`, `templates/_workspace_nav.html`, `templates/_functional_capacity_builder.html`, `templates/_policy_checklist.html` |
| Styles and scripts | `static/css/claim*`, `static/css/compiler.css`, `static/css/riskatlas.css`, `static/js/claim*`, `static/js/compiler-inbox.js` |
| Design and architecture | `docs/claimhub-architecture.md`, `docs/claimhub-resource-migration.md`, `docs/claimbuddy-frontend-spec.md` |

Source tests identified: `tests/test_claimhub.py`, `tests/test_claimhub_resources.py`, `tests/test_claimhub_technical_map.py`, and `tests/test_compiler.py`. They target the monolith route map and cannot yet be carried over unchanged. The standalone host, privacy, and resource behaviour is covered by `tests/test_standalone.py`.

No tracked ClaimHub case records, uploads, or claim-specific data files were found under `data/`. The SQLite database and uploads are runtime state and were intentionally excluded from the code extraction.

## Standalone changes

`app.py` and `Procfile` are new. The app serves ClaimHub at the root of `claimhub.co.za`, ClaimBuddy at the root of `buddy.claimhub.co.za`, and a JSON health response at `/health`. Existing ClaimHub marketing, resources, professional role templates, and ClaimBuddy home render. The database initializer no longer starts Core AU ingestion. RiskAtlas resources redirect to `https://riskatlas.co.za` and older Render links in the public templates were updated.

The original `app.py` was not copied: it contains unrelated Sentrix, RiskAtlas, ClinicalAtlas, SchemeBook, Compass, and Core routes, and the local main file ends partway through `functional_capacity`. The new app intentionally keeps case creation off by default. With the local development flag enabled, a signed claimant browser session can create and view its own case; this is only a development smoke path, not a production identity design.

## Production blockers

1. Complete claimant and professional identity, recovery, invitation verification, CSRF protection, and claimant consent flows. The source invitation accepts an email string with a token and is not sufficient proof of email ownership.
2. Port and test the full ClaimBuddy guided intake, document upload, editing, evidence modules, and professional invitation UI. Extracted legacy templates remain available for that work but are not active routes in this staging app.
3. Provision encrypted persistent case and upload storage with backup and migration from any existing live records. The current SQLite path can be changed with `CLAIMHUB_DATA_DIR`, but no production volume is configured.
4. Run the full source and standalone test suites, then smoke test a Railway preview URL and both intended host mappings before any DNS change.
5. Publish to `dghx23/claimhubza` and preserve selected file history when GitHub connectivity permits. The source is a partial clone; `git-filter-repo` failed on a missing historic blob, and direct GitHub access failed DNS resolution. This checkout records the exact source commit as provenance.

Deployment state: **not deployed**. DNS and the existing monolith routes have not been changed, so the current live setup remains the rollback.


## 2026-09-30 standalone completion pass

The standalone repository now also contains the previously missing claimant runtime dependencies and modules: occupation lookup, medical-record synchronisation, rejection processing/explainer, evidence-gap and disability-definition logic, insurer/NFO guidance, clinician lookup helpers, the remaining ClaimBuddy workspace templates, and supporting browser scripts. `claimbuddy_runtime.py` owns the extracted claimant routes while `blueprints/claimhub_bp.py` owns professional ClaimHub access. GitHub Actions now runs standalone public-host and full-runtime smoke tests; the latest completed suite is green. A dedicated Railway service has been created, with the existing monolith retained as rollback while deployment/domain validation completes.
