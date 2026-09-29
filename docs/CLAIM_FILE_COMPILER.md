# ClaimBuddy — claim file compiler

**Product:** one job. Documents in, review-ready claim file out.  
**Parent:** RiskAtlas International (ZA live, AU forthcoming).  
**Repo version:** 0.11.0  
**Dogfood test:** a pack you would actually send.

This replaces the four-layer Risk Atlas hub as the front door. AtlasCore, ClinicalAtlas, ClaimGuard chrome, and the 8-step wizard are no longer the product. The engine (`engine.py`, policy scan, duty-impact, gaps, letters) is unchanged.

The directory, glossary, language map, and cross-links live at `/reference` and are specified in [REFERENCE_CATALOG.md](REFERENCE_CATALOG.md). They are a later, separately sellable catalogue — not this compiler.

---

## Job to be done

Insurers rarely kill a valid income-protection claim on the medicine. They kill it on **dates, language, and missing paper**.

The compiler:

1. Accepts an unsorted dump of documents.
2. Classifies them (you correct misses).
3. Builds **the File** — chronology, Date-of-Absence / Date-of-disablement conflicts, duty-impact, policy tests found in *this* wording, evidence gaps with holders, deadline clock. ZA and AU share this page; labels, letters, and holders follow the file's country.
4. Emits a numbered **pack** plus three draft letters and a treating-doctor questionnaire.

Questions appear only for what the documents did not give.

---

## Surfaces

| Route | Name | Role |
|-------|------|------|
| `/` | Inbox | Drop files or open an existing file. Creates a claim. |
| `/claim/<id>` | The File | One page. The product. |
| `/claim/<id>/vault` | Documents | Classify, add, remove. |
| `/claim/<id>/pack` | Pack | Markdown preview + download. Letters and doctor Q linked here. |
| `/reference` | Reference catalogue | Glossary, language map, directories. Separate product. |
| `/ecosystem` | Legacy hub | Old four-layer map. Kept, not linked as home. |
| `/intake` | Profile editor | Full wizard still exists for deep edits. Not the front door. |

Workspace modules (policy reader, functional capacity, rejection explainer, gaps, letters, doctor Q) remain as side doors from The File. They are not a hub.

---

## The File — six panels

1. **Parties** — claimant, employer, insurer, policy / claim refs, stage. Inline save.
2. **Chronology** — extracted and user-stated dates. Date-of-Absence conflicts in red.
3. **The argument** — illness → functional limitation → material duties.
4. **Policy tests** — only clauses the scanner found in uploaded wording, cross-linked to the language map / glossary.
5. **Missing** — each gap: what, who holds it, draft request. Links into `/reference`.
6. **Clock** — waiting period, notice, review, ombud, rejection dates.

---

## Rules

- Documents in, pack out. If a screen does not serve that, it is not the compiler.
- One claim, one user until a pack is good enough to send.
- Not advice. Organisation and drafting. You approve every output.
- POPIA by shape: the file lives with you.
- Catalog cross-links stay live on The File (traps, terms, confusion pairs) so the compiler and the reference product reinforce each other.

---

## What we did not delete

- `engine.py`, policy/rejection processors, functional capacity, language map, clinical atlas, CMS schemes, HPCSA lookup.
- `/resources/*` routes and xref partials.
- AtlasCore / ClinicalAtlas blueprints (reachable from `/reference` and `/ecosystem`).

The 8-step intake is demoted to **Edit profile**, not removed.
