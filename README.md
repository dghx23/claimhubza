# ClaimHub ZA

Standalone Flask extraction for the South African claims family:

- `claimhub.co.za`: ClaimHub public site, resources landing, and professional role pages.
- `buddy.claimhub.co.za`: claimant-facing ClaimBuddy home.
- `/health`: service health response for smoke checks.

ClaimBuddy and the professional portal share the same case database and consent model. RiskAtlas reference pages remain external links.

## Current readiness

This repository is now the standalone ClaimHub ZA / ClaimBuddy codebase. Public pages, professional role pages, guided claimant intake, document vault, policy reader, functional-capacity module, rejection explainer, evidence gaps, letters, doctor questionnaire, claim pack, and claimant-controlled professional invitations are present. Case creation remains disabled by default in deployed environments until production identity and durable private storage are configured. Setting `CLAIMHUB_ENABLE_CASES=1` enables local development only; it uses a signed browser session to scope claimant case access and must not be used as production authentication.

The source monolith remains the live rollback. No DNS or monolith route changes are part of this extraction.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
SECRET_KEY=development-only .venv/bin/python app.py
```

Run tests with `python3 -m pytest tests/test_standalone.py`. Set `CLAIMHUB_DATA_DIR` to a persistent, private directory before enabling case records in a deployed service.

## Source provenance

Extracted from `dghx23/SentrixDigital` commit `45b660fbf4850f8cac65ba58916cf9fbd0742672` (2026-09-30 03:21 +10). See `EXTRACTION.md` for the files, dependency decisions, and remaining work. The source repository is a partial clone with missing historic blobs, so its full file history could not be filtered into this checkout while GitHub connectivity was unavailable.


## Separation status

Standalone CI covers both public hosts, claimant-session isolation, the full claimant module route set, and the ClaimBuddy-to-ClaimHub invitation round trip. RiskAtlas intelligence is linked externally rather than imported as live case-state code. The existing monolith remains available only as rollback until the Railway preview and final domain cutover are complete.
