# ClaimHub resource migration

## Public ownership

The mature reference guides and tools that were previously presented through the RiskAtlas application shell are now public ClaimHub resources.

Canonical public entry point:

- `/claims/resources`

Canonical detail paths are also available under `/claims/resources/...` for workflow, glossary, language map, policy terms, policy traps, evidence gaps, disability definitions, life insurers, NFO material, ombud guidance, news, wiki, medical-scheme reference, medicine schedules and related detail pages.

Legacy `/resources/...` URLs remain available for backwards compatibility. The old `/resources` and `/reference` catalogue entry points redirect to ClaimHub Resources.

## What moved vs what remains a source layer

The public presentation and navigation ownership moved to ClaimHub. The underlying mature reference engines already existed in SentrixDigital and were checked against the RiskAtlas implementation before this migration.

The following reference modules are present in SentrixDigital and feed ClaimHub/ClaimBuddy:

- `knowledge.py`
- `language_map.py`
- `evidence_gaps.py`
- `disability_definitions.py`
- `life_insurers.py`
- `nfosa_dispute.py`
- `ombud_guidance.py`
- `news_articles.py`
- `library_wiki.py`
- `clinical_atlas.py`
- `clinical_atlas_clinicians.py`
- `clinical_atlas_medical_aids.py`
- `medicine_schedules.py`
- `sa_reference_data.py`
- `engine.py`

Core reference modules compared during the migration were either identical to RiskAtlas or SentrixDigital already contained the newer local version. This avoids copying an older RiskAtlas application shell over the newer ClaimHub branch.

RiskAtlas/Core remains the reference-intelligence boundary: authority feeds, curated datasets and reusable knowledge logic can continue to be maintained there or progressively exposed as reusable interfaces. It no longer owns the public claims-resource experience.

## Visual shell

All public `templates/resources/*.html` pages now use `templates/claimsite/resource_base.html`, which places the mature resource pages inside the standalone ClaimHub visual system rather than the Sentrix/RiskAtlas public shell.

## Architecture rule

The intended flow is:

    RiskAtlas / Core ZA reference intelligence
                 ↓
          ClaimHub Resources
            ↙           ↘
     ClaimBuddy        ClaimHub
     claimant app      professional portal
            ↘           ↙
             shared live case

ClaimHub Resources does not own live case state. ClaimBuddy and ClaimHub operate on the shared case record; RiskAtlas/Core supplies reference intelligence.

## Verification

`tests/test_claimhub_resources.py` covers the marketing/resource entry points, canonical ClaimHub resource URLs and legacy catalogue redirects. The tests are committed but still need to run in CI/local execution before a production release.
