# ClaimHub ZA

Standalone Flask extraction for the South African claims family:

- `claimhub.co.za`: ClaimHub public site, resources landing, and professional role pages.
- `buddy.claimhub.co.za`: claimant-facing ClaimBuddy home.
- `/health`: service health response for smoke checks.

ClaimBuddy and the professional portal share the same case database and consent model. RiskAtlas reference pages remain external links.

## Current readiness

This checkout is a **staging extraction**, not yet a production cutover. Public pages and professional role pages render locally. Case creation is disabled by default because production claimant identity, professional identity, durable storage, and the complete claim editing/upload flows are not yet ready. Setting `CLAIMHUB_ENABLE_CASES=1` enables local development only; it uses a signed browser session to scope claimant case access and must not be used as production authentication.

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
