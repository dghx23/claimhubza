# ClaimHub resource migration

## Product boundary

ClaimHub Resources owns the claims knowledge experience: policy wording, claim stages, evidence gaps, functional impact, insurer context and dispute guidance. ClaimBuddy applies that guidance in the claimant workspace, while the ClaimHub professional portal uses the same case record. Separate products such as ClinicalAtlas, Compass and RiskAtlas may be linked for wider reference context.

## Current standalone state

The standalone repository serves the public ClaimHub Resources landing page at `/claims/resources`. It also carries several claim-related knowledge modules and assets. Some detail paths under `/claims/resources/...` currently redirect to legacy pages on `riskatlas.co.za`; they have not yet been migrated into local ClaimHub routes. Treat these as transitional outbound links. The standalone repo does not contain the monolith's full `templates/resources/` tree.

Before either public domain is cut over, migrate or explicitly label those detail links, verify the destination and content of every resource card, and test that claim-specific guides stay within the intended ClaimHub experience. Keep separate clinical and social-support links clearly identified as external references.

ClaimHub Resources does not store live case state. ClaimBuddy and the professional portal work with the shared case record, subject to the production identity, consent and storage controls documented elsewhere.
