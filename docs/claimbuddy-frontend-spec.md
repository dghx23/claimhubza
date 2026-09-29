# ClaimBuddy public front-end — full build spec

Implementation-ready spec: exact routes, exact template markup, exact
CSS, exact JS. Follow §7 (build order) and this becomes a mechanical
port, not a design exercise.

## 1. Why this exists

The user supplied five standalone marketing HTML files for ClaimBuddy
(`index.html`, `about.html`, `how-it-works.html`, `claim-stages.html`,
`demo.html`) built as a separate static site — own CSS (`css/site.css`,
`css/demo.css`), own JS (`config.js`, `site-header.js`, `site-links.js`,
`site.js`, `claim-stages.js`, `demo.js`), hardcoded links to
`http://127.0.0.1:8004/...`. None of the referenced CSS/JS files were
provided — only the HTML shells.

Goal: bring this content into the live Flask app as new pages, **without
removing anything that exists today** (`/claimbuddy` workspace launcher,
`templates/landing.html`, the intake/dashboard/vault/etc. workspace
routes all stay untouched), and **harmonised** with the app's existing
design system rather than the prototype's bespoke CSS.

Reference for "harmonised": the `/claimguard` hub page
(`templates/risk_atlas/claimguard.html`) and the Risk Atlas home page
(`templates/risk_atlas/index.html`) — blue gradient header, single row
nav, breadcrumb, white bordered cards in a grid, teal links. That's
`hero` / `hero-actions` / `hub-card` / `btn` / `card` — all classes
already defined once in `static/css/app.css` (Classic colors) and
re-skinned by `static/css/platform.css` under `[data-ui-style="atlascore"]`
(Editorial colors). New pages must reuse these classes, not invent a
parallel component system.

## 2. Design-system ground truth (read before touching CSS)

Three stylesheets, always loaded together, in this order, on every page
via `templates/platform_base.html`:

1. **`riskatlas.css`** — `:root` design tokens (`--ink`, `--rule`,
   `--teal`, `--bg-elevated`, `--serif`, `--mono`, `--radius`,
   `--shadow`, …) *and* the `ra-*` component family (`ra-panel`,
   `ra-hero`, `ra-stat`, `ra-card-grid`, `ra-cat-list`, `ra-search`, …)
   used by AtlasCore ZA / ClinicalAtlas ZA browse & detail pages. No
   other stylesheet defines `--ink` etc., so this must never be
   disabled.
2. **`atlascore.css`** — structural layout with **no `:root` of its
   own** (header grid, `.ac-nav`, `.ac-panel`, `.ac-stat-card`,
   `.ac-table`, `.ac-site-bar`, breadcrumbs). Depends on #1's tokens.
   Never disabled.
3. **`app.css`** — the *only* toggled sheet. Defines Classic-era
   `:root` tokens (`--primary`, `--muted`, `--border`, …) and redefines
   a specific set of generic classnames with Classic colors: `.hero`,
   `.btn` / `.btn-primary` / `.btn-secondary`, `.card`, `.hub-card`,
   `.hub-grid`, `.risk-atlas-hero`, `.risk-atlas-grid`,
   `.risk-atlas-card`. Because it loads last, when enabled
   (`data-ui-style="legacy"`, the default) it wins the cascade for
   exactly those classes; when disabled, `atlascore.css`/
   `riskatlas.css`'s own defaults show through (Editorial look).
4. **`platform.css`** — always loaded, unconditional. Cross-cutting
   header colors and `[data-ui-style="legacy"|"atlascore"]`-scoped
   overrides for markup shared between both themes (`.hero`,
   `.hub-card`, `.risk-atlas-*`, `.ac-header`, nav links, disclaimer).

**Rule for any new page**: use `.hero` / `.hero-actions` / `.btn*` /
`.card` / `.hub-grid` + `.hub-card` / breadcrumb markup for anything
hub/grid-shaped. Only introduce new classnames for markup that has no
existing equivalent (§5), and when you do, style them with literal,
theme-neutral values (not tokens from either system) so they don't
silently break under one theme the way `ra-*` did before this session's
fixes.

Toggle mechanics live in `templates/platform_base.html` (bootstrap
script) and `static/js/ui-style.js` (button handler), both keyed on
`localStorage["claimguard-ui-style"]` (`"legacy"` default, or
`"atlascore"`). Never disable `ss-riskatlas` or `ss-atlascore` in that
logic — that regression has already been fixed twice this session.

Existing reusable class reference (from `static/css/app.css`, already
bridged for Editorial mode in `platform.css`):

```
.hero            block wrapper, h1/p styled, margin-bottom
.hero-actions    flex row, gap 0.75rem, wrap
.btn             base button/link, padding 0.6rem 1.1rem, radius, weight 600
.btn-primary     solid primary color
.btn-secondary   tinted secondary
.card            bordered panel, radius, padding, shadow
.hub-grid        (see risk-atlas-grid / hub pattern below) CSS grid, auto-fit minmax(240px,1fr), gap
.hub-card        bordered card, hover border-color change, icon+h3+p+cta slot
.hub-card-primary  accent border/background variant
.hub-cta         small bold link-styled span, used as "Open X →"
.hub-icon        emoji-sized leading icon span inside hub-card
.risk-atlas-hero / .risk-atlas-eyebrow / .risk-atlas-grid / .risk-atlas-card
                 the exact pattern used on the Risk Atlas home page
```

`templates/risk_atlas/claimguard.html` and
`templates/risk_atlas/index.html` are the two best copy-paste references
for hero + card-grid markup.

## 3. Routes to add

All in `app.py`, immediately after the existing `/claimbuddy` route
(around line 503-511). Existing `claimbuddy_landing` (`/claimbuddy`) is
**not modified** — it stays the in-app workspace launcher. New routes
are the public-facing marketing/education layer:

```python
@app.route("/claimbuddy/home")
def claimbuddy_home():
    return render_template("claimbuddy/home.html")


@app.route("/claimbuddy/about")
def claimbuddy_about():
    return render_template("claimbuddy/about.html")


@app.route("/claimbuddy/how-it-works")
def claimbuddy_how_it_works():
    return render_template("claimbuddy/how_it_works.html")


@app.route("/claimbuddy/claim-stages")
def claimbuddy_claim_stages():
    return render_template("claimbuddy/claim_stages.html")


@app.route("/claimbuddy/demo")
def claimbuddy_demo():
    return render_template("claimbuddy/demo.html")
```

No new imports needed — these are static content pages, no DB/query
params. Place `templates/claimbuddy/` as a new subdirectory (mirrors the
existing `templates/atlascore/`, `templates/risk_atlas/` pattern).

### Cross-linking

- `templates/landing.html` (existing `/claimbuddy`): add **one** line
  near the top of the hero panel (after the existing "Start claim
  readiness check" / "Resources hub" buttons), don't touch anything
  else:

  ```html
  <p class="ac-meta" style="margin-top:0.75rem;">
    New here? <a href="{{ url_for('claimbuddy_how_it_works') }}">See how ClaimBuddy works</a>
    · <a href="{{ url_for('claimbuddy_demo') }}">Try the interactive demo</a>
  </p>
  ```

- Every new template's top nav row (see §4 shared partial) links to all
  five: Home, About, How it works, Claim stages, Demo, plus "Open
  workspace" → `url_for('claimbuddy_landing')`.

All five templates `{% extends "risk_atlas_base.html" %}` (→
`platform_base.html`), giving them the header/nav/site-bar/theme-toggle
for free.

## 4. Shared sub-nav partial

Add `templates/claimbuddy/_subnav.html`, included at the top of
`{% block content %}` in all five templates (right after the
breadcrumb):

```html
<nav class="resource-nav" aria-label="ClaimBuddy pages">
  <a href="{{ url_for('claimbuddy_home') }}" {% if active=='home' %}class="is-active"{% endif %}>Home</a>
  <a href="{{ url_for('claimbuddy_about') }}" {% if active=='about' %}class="is-active"{% endif %}>About</a>
  <a href="{{ url_for('claimbuddy_how_it_works') }}" {% if active=='how' %}class="is-active"{% endif %}>How it works</a>
  <a href="{{ url_for('claimbuddy_claim_stages') }}" {% if active=='stages' %}class="is-active"{% endif %}>Claim stages</a>
  <a href="{{ url_for('claimbuddy_demo') }}" {% if active=='demo' %}class="is-active"{% endif %}>Demo</a>
  <a href="{{ url_for('claimbuddy_landing') }}" class="ac-nav-risk-atlas" style="margin-left:auto;">Open workspace →</a>
</nav>
```

`.resource-nav` already exists (bridged in `platform.css` for both
themes, used by the resources hub) — reuse it verbatim, no new CSS.

Each page includes it with its own `active` value:

```jinja
{% include "claimbuddy/_subnav.html" with context %}
```

and each route passes `active="home"` / `"about"` / `"how"` /
`"stages"` / `"demo"` into its `render_template(...)` call (add this
kwarg to each of the 5 route functions in §3).

## 5. Per-page templates (full markup)

### 5.1 `templates/claimbuddy/home.html` (from `cc8c9ef4-index.html`)

```jinja
{% extends "risk_atlas_base.html" %}
{% block title %}ClaimBuddy — Review-ready claim packs{% endblock %}
{% block meta_description %}ClaimBuddy — turn scattered medical records into a review-ready claim pack. Privacy-first evidence organisation for SA income protection claims.{% endblock %}
{% block content %}
<nav class="ac-breadcrumb">
  <a href="{{ url_for('risk_atlas_index') }}">Risk Atlas</a>
  <span>›</span>
  <span>ClaimBuddy</span>
</nav>
{% include "claimbuddy/_subnav.html" with context %}

<section class="hero">
  <h1>Turn scattered records into a review-ready claim pack</h1>
  <p>
    Organise medical evidence, employer records, policy wording, and timelines —
    so procedural gaps do not cost you fairness on a claim you were entitled to pursue.
  </p>
  <div class="hero-actions">
    <a href="{{ url_for('intake') }}" class="btn btn-primary">Start free triage</a>
    <a href="#tools-demo" class="btn btn-secondary">Try browser tools</a>
  </div>
  <p class="field-hint" style="margin-top:0.75rem;">
    Client-side processing · POPIA-aligned design · Human review required
  </p>
</section>

<section class="ac-block">
  <h2>Five gaps that sink valid claims</h2>
  <p class="ac-hero-lead">The sickest people face the hardest administration. ClaimBuddy maps each failure mode before it becomes a rejection reason.</p>
  <div class="hub-grid">
    <div class="hub-card"><h3>Knowledge</h3><p>Policyholder duties, actual notice, Date of Absence, and waiting periods — rarely explained in one place.</p></div>
    <div class="hub-card"><h3>Evidence</h3><p>Medical notes exist, but insurers need functional impact mapped to material duties and stamina.</p></div>
    <div class="hub-card"><h3>Record access</h3><p>Employers and insurers hold memos, DOA calculations, and internal reasoning you cannot see.</p></div>
    <div class="hub-card"><h3>Power &amp; language</h3><p>Rejection letters use standards ordinary claimants cannot translate into an actionable plan.</p></div>
    <div class="hub-card"><h3>Timing</h3><p>Appeal deadlines often surface only after rejection — or when time has already run out.</p></div>
  </div>
</section>

<section class="ac-block">
  <h2>Structured path to submission</h2>
  <p class="ac-hero-lead">Five workspace steps on the homepage — eight in the full intake. You stay in control at every stage.</p>
  <div class="disclaimer" style="margin-top:0;">
    <strong>Disclaimer:</strong> Organisation and drafting support only — not legal or medical advice. You approve every output.
  </div>
  <div class="hub-grid" style="margin-top:1rem;">
    <div class="hub-card"><span class="hub-icon">1</span><h3>Triage your stage</h3><p>Preparing, waiting period, assessment, rejected, review, ombud, or record-access dispute.</p></div>
    <div class="hub-card"><span class="hub-icon">2</span><h3>Upload documents</h3><p>Policy wording, certificates, specialist reports, employer letters, payslips.</p></div>
    <div class="hub-card"><span class="hub-icon">3</span><h3>Build chronology</h3><p>Extract dates, events, and actors. DoA conflicts between employer and insurer are flagged.</p></div>
    <div class="hub-card"><span class="hub-icon">4</span><h3>Evidence gap report</h3><p>12 gap types — who holds each record, urgency, and request wording.</p></div>
    <div class="hub-card"><span class="hub-icon">5</span><h3>Pack &amp; review</h3><p>Seven-section export plus draft letters. Edit before anything is sent.</p></div>
  </div>
  <p class="text-center" style="margin-top:1.5rem;">
    <a href="{{ url_for('claimbuddy_how_it_works') }}">Full eight-step workflow →</a>
  </p>
</section>

<section class="ac-block" id="tools-demo">
  <h2>Browser workbench</h2>
  <p class="ac-hero-lead">Run timeline and gap demos here. <a href="{{ url_for('claimbuddy_demo') }}">Open full workspace demo →</a></p>
  <div class="tools-widget">
    <div class="tool-tabs" role="tablist">
      <button type="button" class="tool-tab active" data-tool="timeline" role="tab">Timeline</button>
      <button type="button" class="tool-tab" data-tool="policy" role="tab">Policy reader</button>
      <button type="button" class="tool-tab" data-tool="gaps" role="tab">Evidence gaps</button>
      <button type="button" class="tool-tab" data-tool="rejection" role="tab">Rejection</button>
    </div>

    <div class="tools-panel active" data-tool-panel="timeline">
      <div class="tool-app-bar">
        <div>
          <div class="tool-app-title">claim-timeline-builder</div>
          <div class="tool-app-sub">Guided chronology — enter key facts, flag obvious gaps</div>
        </div>
        <button type="button" class="btn btn-secondary" id="fill-sample">Sample data</button>
      </div>
      <form class="tool-form" id="timeline-form">
        <div class="grid-2" style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
          <div class="field"><label for="tf-employer">Employer / scheme</label><input type="text" id="tf-employer" placeholder="e.g. Deloitte — Group Risk"></div>
          <div class="field"><label for="tf-insurer">Insurer / ref</label><input type="text" id="tf-insurer" placeholder="e.g. Old Mutual — Pol 123"></div>
        </div>
        <div class="field"><label for="tf-doa">Date of absence</label><input type="date" id="tf-doa"></div>
        <div class="field"><label for="tf-impact">Functional impact summary</label><textarea id="tf-impact" placeholder="How symptoms affect material duties…"></textarea></div>
        <button type="submit" class="btn btn-primary">Generate timeline report</button>
      </form>
      <div class="tool-output" id="timeline-output"></div>
    </div>

    <div class="tools-panel" data-tool-panel="policy">
      <p>Upload your schedule — ClaimBuddy extracts waiting period, own-occupation test, Date of Absence, notice ladder, exclusions, and offsets with policy wording snippets.</p>
      <p><a href="{{ url_for('intake') }}" class="btn btn-secondary">Start intake →</a></p>
    </div>

    <div class="tools-panel" data-tool-panel="gaps">
      <p><strong>High priority (sample)</strong></p>
      <ul>
        <li>Insurer claim-file &amp; DoA memo</li>
        <li>Employer statement</li>
        <li>Functional-capacity / duty-impact statement</li>
      </ul>
      <p><a href="{{ url_for('claimbuddy_demo') }}" class="btn btn-secondary">Full demo →</a></p>
    </div>

    <div class="tools-panel" data-tool-panel="rejection">
      <div class="flash error">
        <strong>Sample rejection:</strong> "Insufficient specialist evidence on Date of Absence (20 May 2025)."<br>
        <strong>Flagged:</strong> Employer HR records DoA 15 Mar 2025 — 65-day shift. PAIA request recommended.
      </div>
      <p><a href="{{ url_for('claimbuddy_demo') }}" class="btn btn-secondary">Preview PAIA draft →</a></p>
    </div>
  </div>
</section>

<section class="ac-block">
  <h2>Function, not diagnosis</h2>
  <p class="ac-hero-lead">Insurers argue about duty impact. ClaimBuddy bridges symptoms to material duties — then drafts questionnaires and PAIA requests you approve.</p>
  <div class="hub-grid">
    <div class="hub-card"><span class="hub-icon">📅</span><h3>DoA contradictions</h3><p>Spot date shifts between rejection letters, employer HR, and treating-doctor records.</p></div>
    <div class="hub-card"><span class="hub-icon">📋</span><h3>Duty-impact matrix</h3><p>Map brain fog, fatigue, and sedation to the duties your role actually requires.</p></div>
    <div class="hub-card"><span class="hub-icon">📨</span><h3>Record requests</h3><p>Draft PAIA/POPIA access letters for claim-file notes insurers rarely volunteer.</p></div>
  </div>
</section>

<section class="ac-block" id="pricing-teaser">
  <h2>Simple pricing</h2>
  <p class="ac-hero-lead">Start free. Upgrade when you need structured exports.</p>
  <div class="hub-grid">
    <div class="card price-card">
      <h3>Free triage</h3>
      <div class="price-amount">R0 <span>forever</span></div>
      <ul class="price-features"><li>Claim stage triage</li><li>Evidence checklist</li><li>Educational resources</li></ul>
      <a href="{{ url_for('intake') }}" class="btn btn-secondary">Start triage</a>
    </div>
    <div class="card price-card hub-card-primary">
      <span class="ac-pill">Popular</span>
      <h3>Claimant pack</h3>
      <div class="price-amount">R290 <span>per claim</span></div>
      <ul class="price-features"><li>Full 8-step intake</li><li>Policy &amp; gap reports</li><li>Pack exports &amp; PAIA templates</li></ul>
      <a href="#waitlist" class="btn btn-primary">Join waitlist</a>
    </div>
    <div class="card price-card">
      <h3>Pro review</h3>
      <div class="price-amount">R890 <span>per review</span></div>
      <ul class="price-features"><li>Everything in claimant pack</li><li>Human quality review</li><li>Escalation routing notes</li></ul>
      <a href="mailto:hello@claimbuddy.co.za" class="btn btn-secondary">Enquire</a>
    </div>
  </div>
</section>

<section class="ac-panel ac-block" id="waitlist" style="max-width:640px;">
  <h2>Private beta</h2>
  <p class="ac-hero-lead">Claimant pack launch — early access and pricing.</p>
  <form class="tool-form">
    <div class="field">
      <label for="wl-email">Email</label>
      <input type="email" id="wl-email" name="email" placeholder="you@example.com" required disabled>
    </div>
    <button type="submit" class="btn btn-primary" disabled>Join waitlist (coming soon)</button>
  </form>
  <p class="field-hint">Launch updates only — no spam.</p>
</section>
{% endblock %}
```

### 5.2 `templates/claimbuddy/about.html` (from `045b5952-about.html`)

```jinja
{% extends "risk_atlas_base.html" %}
{% block title %}Our story — ClaimBuddy{% endblock %}
{% block meta_description %}Why ClaimBuddy exists — product insight from a real income protection claim journey.{% endblock %}
{% block content %}
<nav class="ac-breadcrumb">
  <a href="{{ url_for('claimbuddy_home') }}">ClaimBuddy</a>
  <span>›</span>
  <span>Our story</span>
</nav>
{% include "claimbuddy/_subnav.html" with context %}

<section class="hero">
  <h1>Built from a real claim journey</h1>
  <p>Not a dispute page — a workspace so the next person navigates faster, with clearer evidence, and fewer procedural surprises.</p>
</section>

<div class="ra-grid-2">
  <div>
    <h2>The pattern</h2>
    <p>People are genuinely unwell, but claims stumble on <strong>dates</strong>, <strong>wording</strong>, <strong>missing records</strong>, and the gap between medical language and policy tests.</p>
    <p>Generic folders, chatbots, and one-off lawyer letters do not solve this. You need a workspace that understands DoA, waiting periods, material duties, functional capacity, and insurer timelines.</p>
    <p>ClaimBuddy is that workspace — claim-readiness and evidence organisation, with clear boundaries about what it is not.</p>
  </div>
  <div class="card">
    <h3>What we believe</h3>
    <ul>
      <li>Fair treatment means clear information at every stage</li>
      <li>Claimants should not face unreasonable barriers to submit or complain</li>
      <li>Advice must suit circumstances — duty impact, not diagnosis alone</li>
      <li>Technology should organise and explain, not replace professional judgment</li>
    </ul>
    <p class="field-hint"><em>TCF alignment — formal mapping on backburner.</em></p>
  </div>
</div>
{% endblock %}
```

`.ra-grid-2` is from `riskatlas.css` (always loaded, §2) — a plain
2-column responsive grid, no theme dependency beyond the tokens it
already has. Safe to reuse here even though this page isn't an
AtlasCore page; it's a generic layout utility.

### 5.3 `templates/claimbuddy/how_it_works.html` (from `d2576e43-howitworks.html`)

```jinja
{% extends "risk_atlas_base.html" %}
{% block title %}How it works — ClaimBuddy{% endblock %}
{% block meta_description %}How ClaimBuddy works — from upload to review-ready claim pack.{% endblock %}
{% block content %}
<nav class="ac-breadcrumb">
  <a href="{{ url_for('claimbuddy_home') }}">ClaimBuddy</a>
  <span>›</span>
  <span>How it works</span>
</nav>
{% include "claimbuddy/_subnav.html" with context %}

<section class="hero">
  <h1>From upload to review-ready pack</h1>
  <p>A structured path through the ClaimBuddy intake — you edit and approve every draft before anything is sent.</p>
</section>

<ol class="stage-step-list">
  <li class="stage-step"><span class="step-num">1</span><div><h3>Upload &amp; profile</h3><p class="step-focus">Policy wording, payslips, medical records.</p><p class="step-detail">ClaimBuddy scans key clauses — waiting period, DoA, own-occupation, notice.</p></div></li>
  <li class="stage-step"><span class="step-num">2</span><div><h3>Build your timeline</h3><p class="step-focus">Symptom onset, when duties stopped, first certificate, first notice.</p><p class="step-detail">Precision date pickers — insurers argue about the gaps.</p></div></li>
  <li class="stage-step"><span class="step-num">3</span><div><h3>Policy checklist</h3><p class="step-focus">Which requirements you have evidence for.</p><p class="step-detail">Waiting period continuity, material duties, proof-of-claim items, complaint deadlines.</p></div></li>
  <li class="stage-step"><span class="step-num">4</span><div><h3>Health story &amp; functional capacity</h3><p class="step-focus">Story shape, symptoms, diagnoses.</p><p class="step-detail">Then bridge each symptom to a material duty via the duty-impact matrix.</p></div></li>
  <li class="stage-step"><span class="step-num">5</span><div><h3>Evidence gap report</h3><p class="step-focus">What is missing, who holds it.</p><p class="step-detail">Employer HR, insurer, hospital, specialist — plus suggested request wording.</p></div></li>
  <li class="stage-step"><span class="step-num">6</span><div><h3>Draft letters &amp; pack</h3><p class="step-focus">Employer and insurer record requests.</p><p class="step-detail">Internal review letters, seven-section Markdown claim pack.</p></div></li>
  <li class="stage-step"><span class="step-num">7</span><div><h3>Human review</h3><p class="step-focus">You edit and approve every draft.</p><p class="step-detail">Optional pro review tier for lawyer, OT, or tax support.</p></div></li>
</ol>

<div class="disclaimer"><strong>Remember:</strong> ClaimBuddy organises and drafts — it does not submit claims or guarantee outcomes.</div>

<section class="ac-panel ac-block">
  <h2>See it in the browser</h2>
  <p class="ac-hero-lead">Interactive demo with triage, vault, timeline, gaps, and action pack.</p>
  <div class="hero-actions">
    <a href="{{ url_for('claimbuddy_demo') }}" class="btn btn-primary">Full demo</a>
    <a href="{{ url_for('claimbuddy_claim_stages') }}" class="btn btn-secondary">Claim stages</a>
  </div>
</section>
{% endblock %}
```

### 5.4 `templates/claimbuddy/claim_stages.html` (from `a66833d2-claimstages.html`)

```jinja
{% extends "risk_atlas_base.html" %}
{% block title %}Claim stages — ClaimBuddy{% endblock %}
{% block meta_description %}ClaimBuddy guidance for every stage of a South African income protection claim.{% endblock %}
{% block content %}
<nav class="ac-breadcrumb">
  <a href="{{ url_for('claimbuddy_home') }}">ClaimBuddy</a>
  <span>›</span>
  <span>Claim stages</span>
</nav>
{% include "claimbuddy/_subnav.html" with context %}

<section class="hero">
  <h1>Where your claim actually stands</h1>
  <p>Insurers process claims in eight distinct stages. Evidence priorities, trap alerts, and checklist items shift at each one — most people only discover this after a rejection letter.</p>
</section>

<nav class="phase-nav-wrap" aria-label="Claim stage phases">
  <div class="phase-nav" id="phase-nav">
    <a href="#phase-early" data-phase="phase-early">Before decision</a>
    <span class="phase-divider" aria-hidden="true"></span>
    <a href="#step-01" data-phase="step-01">01 Preparing</a>
    <a href="#step-02" data-phase="step-02">02 Waiting</a>
    <a href="#step-03" data-phase="step-03">03 Assessment</a>
    <span class="phase-divider" aria-hidden="true"></span>
    <a href="#phase-escalation" data-phase="phase-escalation">Escalation</a>
    <a href="#step-04" data-phase="step-04">04 Rejected</a>
    <a href="#step-05" data-phase="step-05">05 Review</a>
    <a href="#step-06" data-phase="step-06">06 Ombud</a>
    <span class="phase-divider" aria-hidden="true"></span>
    <a href="#phase-access" data-phase="phase-access">Access</a>
    <a href="#step-07" data-phase="step-07">07 Records</a>
    <a href="#step-08" data-phase="step-08">08 Adviser</a>
  </div>
</nav>

<section class="ac-block" id="phase-early">
  <h2>Before the insurer decides</h2>
  <p class="ac-hero-lead">Most claims fail here — on dates, continuity, or functional evidence — not on whether you were genuinely unwell.</p>
  <ol class="stage-step-list">
    <li class="stage-step" id="step-01"><span class="step-num">01</span><div><h3>Preparing claim</h3><p class="step-focus">Gathering policy, medical, and employment records before first submission</p><p class="step-detail">Policy wording, payslips, job description, and a working chronology — before you lodge. Symptom onset, Date of Absence, and first notice are rarely the same day.</p><p class="step-tools"><strong>Workspace:</strong> Guided intake · document vault · policy reader · evidence gaps</p></div></li>
    <li class="stage-step" id="step-02"><span class="step-num">02</span><div><h3>Waiting-period evidence</h3><p class="step-focus">Proving continuous incapacity through your policy waiting period</p><p class="step-detail">The deferred period is where light-duty returns and partial attendance often reset the clock. Document absence continuity week by week.</p><p class="step-tools"><strong>Workspace:</strong> Timeline · functional-capacity builder · absence continuity</p></div></li>
    <li class="stage-step" id="step-03"><span class="step-num">03</span><div><h3>Insurer assessment</h3><p class="step-focus">Claim lodged — awaiting decision or further evidence requests</p><p class="step-detail">Respond to information requests promptly. Functional-capacity evidence must map to material duties, not diagnosis alone.</p><p class="step-tools"><strong>Workspace:</strong> Access requests · further-medical-evidence tracking</p></div></li>
  </ol>
</section>

<section class="ac-block" id="phase-escalation">
  <h2>After rejection — structured escalation</h2>
  <p class="ac-hero-lead">Capture reasons and deadlines immediately. Each step needs a chronology, not a folder of PDFs.</p>
  <ol class="stage-step-list">
    <li class="stage-step" id="step-04"><span class="step-num">04</span><div><h3>Rejected claim</h3><p class="step-focus">Rejection received — preparing internal review or escalation</p><p class="step-detail">Record every stated reason, the insurer's Date-of-Absence calculation, and appeal deadlines before you respond.</p><p class="step-tools"><strong>Workspace:</strong> Rejection explainer · review-ground matrix · record access</p></div></li>
    <li class="stage-step" id="step-05"><span class="step-num">05</span><div><h3>Internal review</h3><p class="step-focus">Challenging the decision through the insurer's internal review process</p><p class="step-detail">A structured review request: chronology, gap-closure plan, and duty-impact evidence tied to policy wording.</p><p class="step-tools"><strong>Workspace:</strong> Review pack · issue matrix · cure evidence plan</p></div></li>
    <li class="stage-step" id="step-06"><span class="step-num">06</span><div><h3>Ombud complaint</h3><p class="step-focus">Escalating to NFOSA, FSCA, or industry ombud after insurer review</p><p class="step-detail">Track complaint deadlines. Document insurer conduct, prejudice, and any record-access failures alongside your chronology.</p><p class="step-tools"><strong>Workspace:</strong> Escalation pack · prejudice summary · deadline tracker</p></div></li>
  </ol>
</section>

<section class="ac-block" id="phase-access">
  <h2>Records and professional handover</h2>
  <p class="ac-hero-lead">Employers and insurers hold memos you cannot see. Advisers need an organised pack — not scattered attachments.</p>
  <ol class="stage-step-list">
    <li class="stage-step" id="step-07"><span class="step-num">07</span><div><h3>Record-access dispute</h3><p class="step-focus">POPIA/PAIA non-response or inadequate disclosure from insurer or employer</p><p class="step-detail">Request claim-file notes, DOA calculation memos, and assessment records. Follow up non-response formally.</p><p class="step-tools"><strong>Workspace:</strong> Access-request follow-ups · non-response notices</p></div></li>
    <li class="stage-step" id="step-08"><span class="step-num">08</span><div><h3>Professional review</h3><p class="step-focus">Attorney, OT, doctor, or adviser actively assisting your claim</p><p class="step-detail">Hand over a seven-section claim pack with source-linked chronology — so professionals spend time on strategy, not sorting files.</p><p class="step-tools"><strong>Workspace:</strong> Shared workspace · reviewer routing · export pack</p></div></li>
  </ol>
</section>

<section class="ac-panel ac-block">
  <h2>Select your stage in the workspace</h2>
  <p class="ac-hero-lead">ClaimBuddy shifts trap alerts, evidence gaps, and checklist items to match where you are — not a generic template.</p>
  <a href="{{ url_for('intake') }}" class="btn btn-primary">Open claim triage</a>
</section>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/claimbuddy-marketing.js') }}" defer></script>
{% endblock %}
```

Note: `<dl class="step-tools">` in the original prototype became a `<p>`
here for simplicity — keep it a `<p>` unless the CSS in §6 specifically
needs the `<dt>/<dd>` pair (it doesn't; single-line "Workspace: ..." is
fine as one paragraph).

### 5.5 `templates/claimbuddy/demo.html` (from `2ffc8f97-demo.html`)

This one keeps closest to the original since it's a self-contained
product-mockup widget. Port the full markup from `2ffc8f97-demo.html`
lines 14–304 (the `#demo-landing` and `#demo-workspace` divs and the
`#demo-modal`) essentially verbatim, with these changes only:

- Delete `<div id="site-header-mount">` and the `css/site.css`,
  `css/demo.css` `<link>` tags (replaced by `head_extra` block, §6).
- Delete `js/config.js`, `js/site-header.js`, `js/site-links.js`,
  `js/site.js` `<script>` tags.
- `href="http://127.0.0.1:8004/"` → `{{ url_for('claimbuddy_landing') }}`.
- Wrap the whole thing in the standard template scaffold:

```jinja
{% extends "risk_atlas_base.html" %}
{% block title %}Interactive demo — ClaimBuddy{% endblock %}
{% block meta_description %}ClaimBuddy interactive demo — map function, not just diagnosis.{% endblock %}
{% block head_extra %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/claimbuddy-marketing.css') }}">
{% endblock %}
{% block content %}
<nav class="ac-breadcrumb">
  <a href="{{ url_for('claimbuddy_home') }}">ClaimBuddy</a>
  <span>›</span>
  <span>Interactive demo</span>
</nav>
{% include "claimbuddy/_subnav.html" with context %}

<!-- paste lines 14-304 of 2ffc8f97-demo.html here, with the link-target
     substitutions above applied -->

{% endblock %}
{% block scripts %}
<script src="{{ url_for('static', filename='js/claimbuddy-marketing.js') }}" defer></script>
{% endblock %}
```

Apply the same `head_extra`/`scripts` blocks (loading
`claimbuddy-marketing.css`/`.js`) to `home.html` and
`claim_stages.html` too (tool-tabs and phase-nav both need the JS;
home's `.tools-widget`/`.price-*` need the CSS). `about.html` and
`how_it_works.html` need the CSS (for `.stage-step`) but not the JS.

## 6. New CSS — `static/css/claimbuddy-marketing.css`

Scoped to these pages only (never added to `platform_base.html`
globally). Literal values throughout — deliberately not pulling
`--ink`/`--teal`/`--primary` tokens, so this sheet reads the same in
both Classic and Editorial mode (a conscious exception to "reuse the
token system," justified because this is a single self-contained
add-on, not a competing base layer):

```css
/* ClaimBuddy marketing pages — tool tabs, stage steps, demo workspace.
   Loaded only on templates/claimbuddy/*.html via head_extra. */

.stage-step-list { list-style: none; margin: 0; padding: 0; }
.stage-step {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}
.stage-step:last-child { border-bottom: none; }
.stage-step .step-num {
  flex: none;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 999px;
  background: #2f6fed;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}
.stage-step h3 { margin: 0 0 0.25rem; }
.stage-step .step-focus { margin: 0 0 0.35rem; font-weight: 600; color: #1e293b; }
.stage-step .step-detail { margin: 0 0 0.35rem; color: #64748b; }
.stage-step .step-tools { margin: 0; font-size: 0.85rem; color: #475569; }

.phase-nav-wrap {
  position: sticky;
  top: var(--header-h, 3.25rem);
  z-index: 50;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
}
.phase-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  padding: 0.65rem 0;
  align-items: center;
}
.phase-nav a {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  text-decoration: none;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
}
.phase-nav a:hover, .phase-nav a.is-active { color: #1e56d4; background: #e8f1ff; }
.phase-divider { width: 1px; height: 1rem; background: #e2e8f0; margin: 0 0.25rem; }

.price-amount { font-size: 1.75rem; font-weight: 800; margin: 0.5rem 0; }
.price-amount span { font-size: 0.85rem; font-weight: 500; color: #64748b; }
.price-features { list-style: none; margin: 0 0 1rem; padding: 0; font-size: 0.88rem; color: #475569; }
.price-features li { padding: 0.3rem 0; border-bottom: 1px solid #f1f5f9; }
.price-features li:last-child { border-bottom: none; }

.tools-widget { border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-top: 1rem; }
.tool-tabs { display: flex; flex-wrap: wrap; background: #f6f8fc; border-bottom: 1px solid #e2e8f0; }
.tool-tab {
  font: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.7rem 1rem;
  border: none;
  background: none;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}
.tool-tab:hover { color: #1e293b; }
.tool-tab.active { color: #1e56d4; border-bottom-color: #1e56d4; background: #fff; }
.tools-panel { display: none; padding: 1.25rem; }
.tools-panel.active { display: block; }
.tool-app-bar { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.tool-app-title { font-weight: 700; }
.tool-app-sub { font-size: 0.82rem; color: #64748b; }
.tool-form .field { margin-bottom: 0.85rem; }
.tool-form label { display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 0.3rem; }
.tool-form input, .tool-form textarea {
  width: 100%;
  padding: 0.55rem 0.7rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font: inherit;
}
.tool-output { margin-top: 1rem; font-size: 0.85rem; color: #475569; }

/* Demo workspace mockup -- deliberately its own visual language, like a
   product screenshot embedded in a marketing page. */
.demo-landing { padding: 1rem 0; }
.demo-workspace { display: none; grid-template-columns: 220px 1fr; min-height: 32rem; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; margin-top: 1rem; }
.demo-workspace.active { display: grid; }
.demo-sidebar { background: #0f172a; color: #e2e8f0; padding: 1rem 0.75rem; display: flex; flex-direction: column; }
.demo-sidebar-brand { display: flex; align-items: center; gap: 0.5rem; font-weight: 700; padding: 0 0.5rem 1rem; }
.demo-sidebar-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; padding: 0 0.5rem 0.5rem; }
.demo-nav { display: flex; flex-direction: column; gap: 0.15rem; flex: 1; }
.demo-nav-btn {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font: inherit;
  font-size: 0.85rem;
  text-align: left;
  padding: 0.55rem 0.6rem;
  border: none;
  border-radius: 8px;
  background: none;
  color: #cbd5e1;
  cursor: pointer;
}
.demo-nav-btn svg { width: 18px; height: 18px; flex: none; }
.demo-nav-btn:hover { background: #1e293b; color: #fff; }
.demo-nav-btn.active { background: #2f6fed; color: #fff; }
.demo-sidebar-footer { padding-top: 1rem; border-top: 1px solid #1e293b; }
.demo-sidebar-footer a { color: #94a3b8; font-size: 0.82rem; text-decoration: none; }
.demo-main { display: flex; flex-direction: column; min-width: 0; }
.demo-topbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #e2e8f0; }
.demo-topbar h2 { margin: 0; font-size: 1.05rem; }
.demo-topbar-badge { font-size: 0.75rem; font-weight: 600; color: #b91c1c; background: #fee2e2; padding: 0.2rem 0.5rem; border-radius: 999px; }
.demo-panel { flex: 1; overflow-y: auto; padding: 1.25rem; }
.demo-panel[hidden] { display: none; }
.demo-panel-inner { max-width: 46rem; }
.demo-vault { display: grid; grid-template-columns: 1fr 1.4fr; gap: 1rem; max-width: none; }
.demo-alert { display: flex; gap: 0.65rem; padding: 0.85rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.88rem; }
.demo-alert svg { flex: none; width: 20px; height: 20px; }
.demo-alert-info { background: #eff6ff; color: #1e3a8a; }
.demo-alert-target { background: #f5f3ff; color: #4c1d95; }
.demo-alert-warn { background: #fff7ed; color: #9a3412; }
.demo-card { border: 1px solid #e2e8f0; border-radius: 10px; margin-bottom: 1rem; overflow: hidden; }
.demo-card-head { display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 600; font-size: 0.88rem; }
.demo-card-head svg { width: 18px; height: 18px; }
.demo-card-body { padding: 1rem; }
.demo-field { margin-bottom: 0.85rem; }
.demo-field label { display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.3rem; color: #475569; }
.demo-field input, .demo-field select, .demo-field textarea { width: 100%; padding: 0.5rem 0.65rem; border: 1px solid #e2e8f0; border-radius: 6px; font: inherit; }
.demo-actions { margin-top: 0.85rem; display: flex; justify-content: flex-end; }
.demo-doc-list { padding: 0.5rem; }
.demo-doc-item { padding: 0.65rem 0.5rem; border-radius: 8px; cursor: pointer; }
.demo-doc-item:hover, .demo-doc-item.active { background: #f1f5f9; }
.demo-doc-meta { display: flex; gap: 0.5rem; font-size: 0.75rem; color: #64748b; margin-top: 0.2rem; }
.demo-badge { font-size: 0.68rem; font-weight: 700; padding: 0.1rem 0.4rem; border-radius: 999px; }
.demo-badge-flag { background: #fee2e2; color: #b91c1c; }
.demo-badge-ok { background: #dcfce7; color: #15803d; }
.demo-badge-urgent { background: #fef3c7; color: #92400e; }
.demo-timeline { display: flex; flex-direction: column; gap: 1rem; }
.demo-tl-item { display: flex; gap: 0.75rem; }
.demo-tl-dot { width: 10px; height: 10px; border-radius: 999px; background: #94a3b8; margin-top: 0.35rem; flex: none; }
.demo-tl-item.employer .demo-tl-dot { background: #2f6fed; }
.demo-tl-item.warn .demo-tl-dot { background: #ea580c; }
.demo-tl-card { flex: 1; }
.demo-tl-head { display: flex; justify-content: space-between; gap: 0.5rem; font-size: 0.92rem; }
.demo-tl-head .date { color: #64748b; font-size: 0.82rem; }
.demo-tl-warn { margin-top: 0.5rem; padding: 0.6rem 0.75rem; background: #fff7ed; border: 1px solid #fed7aa; border-radius: 6px; font-size: 0.82rem; color: #9a3412; }
.demo-func-card { display: flex; gap: 0.75rem; padding: 0.85rem; border-radius: 8px; margin-bottom: 0.75rem; }
.demo-func-card:last-child { margin-bottom: 0; }
.demo-func-card.purple { background: #f5f3ff; }
.demo-func-card.rose { background: #fff1f2; }
.demo-func-card.amber { background: #fffbeb; }
.demo-func-icon { font-size: 1.35rem; }
.demo-func-card h4 { margin: 0 0 0.35rem; font-size: 0.92rem; }
.demo-func-card textarea { width: 100%; border: none; background: none; font: inherit; resize: none; color: #334155; }
.demo-synthesis { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 10px; flex-wrap: wrap; }
.demo-synthesis h3 { margin: 0 0 0.25rem; font-size: 0.95rem; color: #065f46; }
.demo-synthesis p { margin: 0; font-size: 0.85rem; color: #047857; }
.demo-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.demo-table th, .demo-table td { text-align: left; padding: 0.6rem 0.5rem; border-bottom: 1px solid #e2e8f0; }
.demo-mini-btn { font: inherit; font-size: 0.8rem; font-weight: 600; padding: 0.35rem 0.65rem; border: 1px solid #2f6fed; color: #2f6fed; background: none; border-radius: 6px; cursor: pointer; }
.demo-pack-hero { text-align: center; padding: 1rem 0 1.5rem; }
.demo-pack-icon { width: 3rem; height: 3rem; margin: 0 auto 0.75rem; border-radius: 999px; background: #eff6ff; display: flex; align-items: center; justify-content: center; }
.demo-pack-icon svg { width: 24px; height: 24px; color: #2f6fed; }
.demo-pack-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
.demo-pack-card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; display: flex; flex-direction: column; justify-content: space-between; }
.demo-modal-backdrop { display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.5); z-index: 200; align-items: center; justify-content: center; padding: 1rem; }
.demo-modal-backdrop.open { display: flex; }
.demo-modal { background: #fff; border-radius: 12px; max-width: 32rem; width: 100%; max-height: 80vh; display: flex; flex-direction: column; }
.demo-modal-head { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #e2e8f0; }
.demo-modal-close { border: none; background: none; font-size: 1.25rem; cursor: pointer; color: #64748b; }
.demo-modal-body { padding: 1.25rem; overflow-y: auto; font-size: 0.88rem; line-height: 1.6; white-space: pre-line; }
.demo-modal-foot { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem 1.25rem; border-top: 1px solid #e2e8f0; font-size: 0.78rem; color: #64748b; }

@media (max-width: 720px) {
  .demo-workspace.active { grid-template-columns: 1fr; }
  .demo-sidebar { flex-direction: row; overflow-x: auto; }
  .demo-nav { flex-direction: row; }
}
```

## 7. New JS — `static/js/claimbuddy-marketing.js`

Replaces the prototype's `site.js` + `demo.js` + `claim-stages.js`.
Vanilla, no framework, matching the style of the existing
`static/js/theme.js` / `ui-style.js`:

```js
(function () {
  // --- Home page: tool tabs -------------------------------------------
  document.querySelectorAll(".tool-tabs").forEach(function (tabs) {
    const widget = tabs.closest(".tools-widget");
    tabs.querySelectorAll(".tool-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.querySelectorAll(".tool-tab").forEach(function (t) { t.classList.remove("active"); });
        widget.querySelectorAll(".tools-panel").forEach(function (p) { p.classList.remove("active"); });
        tab.classList.add("active");
        widget.querySelector('[data-tool-panel="' + tab.dataset.tool + '"]').classList.add("active");
      });
    });
  });

  // --- Home page: sample timeline data ---------------------------------
  const fillSample = document.getElementById("fill-sample");
  const output = document.getElementById("timeline-output");
  if (fillSample && output) {
    fillSample.addEventListener("click", function () {
      document.getElementById("tf-employer").value = "Deloitte — Group Risk";
      document.getElementById("tf-insurer").value = "Old Mutual — Pol 44821";
      document.getElementById("tf-doa").value = "2025-05-20";
      document.getElementById("tf-impact").value =
        "Cognitive fatigue after 90 minutes of screen time; unable to sustain an 8-hour workday.";
    });
  }
  const timelineForm = document.getElementById("timeline-form");
  if (timelineForm && output) {
    timelineForm.addEventListener("submit", function (e) {
      e.preventDefault();
      output.innerHTML =
        "<strong>Sample output</strong> — this is a demo; the live workspace generates a full chronology from your intake. " +
        '<a href="' + (window.CLAIMBUDDY_INTAKE_URL || "/intake") + '">Start real intake →</a>';
    });
  }

  // --- Demo page: landing <-> workspace switch -------------------------
  const enterDemo = document.getElementById("enter-demo");
  const exitDemo = document.getElementById("exit-demo");
  const landing = document.getElementById("demo-landing");
  const workspace = document.getElementById("demo-workspace");
  if (enterDemo && workspace) {
    enterDemo.addEventListener("click", function () {
      landing.style.display = "none";
      workspace.classList.add("active");
    });
  }
  if (exitDemo && workspace) {
    exitDemo.addEventListener("click", function (e) {
      e.preventDefault();
      workspace.classList.remove("active");
      landing.style.display = "";
    });
  }

  // --- Demo page: sidebar tab switching ---------------------------------
  function showDemoPanel(name) {
    document.querySelectorAll(".demo-nav-btn").forEach(function (b) {
      b.classList.toggle("active", b.dataset.tab === name);
    });
    document.querySelectorAll(".demo-panel").forEach(function (p) {
      p.hidden = p.dataset.panel !== name;
    });
    const titles = {
      intake: "Triage & context",
      vault: "Document extraction",
      timeline: "The Date of Absence conflict",
      functional: "Functional capacity mapping",
      gaps: "Record gaps",
      pack: "Claim review action pack",
    };
    const title = document.getElementById("demo-topbar-title");
    if (title && titles[name]) title.textContent = titles[name];
  }
  document.querySelectorAll(".demo-nav-btn").forEach(function (btn) {
    btn.addEventListener("click", function () { showDemoPanel(btn.dataset.tab); });
  });
  document.querySelectorAll("[data-goto]").forEach(function (btn) {
    btn.addEventListener("click", function () { showDemoPanel(btn.dataset.goto); });
  });

  // --- Demo page: modal drafts -------------------------------------------
  const DRAFTS = {
    paia: {
      title: "POPIA / PAIA request (draft)",
      body:
        "To: [Insurer claims department]\n\n" +
        "Re: Request for access to records — Policy [reference]\n\n" +
        "In terms of the Promotion of Access to Information Act and POPIA, I request copies of:\n" +
        "  - The internal Date-of-Absence calculation memo for this claim\n" +
        "  - All claim-file notes considered in the assessment decision\n\n" +
        "Please respond within the statutory timeframe. [Your details]",
    },
    doctor: {
      title: "Functional questionnaire (draft)",
      body:
        "Specialist questionnaire — functional capacity\n\n" +
        "1. Please describe the patient's cognitive endurance across a typical working day.\n" +
        "2. Please describe any physical stamina limitations relevant to sustained desk-based work.\n" +
        "3. Please comment on medication side-effects (timing, severity, duration) relevant to " +
        "safety-critical or high-accuracy tasks.\n\n" +
        "[Generated from the claimant's functional map — for specialist completion.]",
    },
  };
  const modal = document.getElementById("demo-modal");
  const modalTitle = document.getElementById("demo-modal-title");
  const modalBody = document.getElementById("demo-modal-body");
  const modalClose = document.getElementById("demo-modal-close");
  document.querySelectorAll("[data-modal]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const draft = DRAFTS[btn.dataset.modal];
      if (!draft || !modal) return;
      modalTitle.textContent = draft.title;
      modalBody.textContent = draft.body;
      modal.classList.add("open");
    });
  });
  if (modalClose) modalClose.addEventListener("click", function () { modal.classList.remove("open"); });
  if (modal) modal.addEventListener("click", function (e) { if (e.target === modal) modal.classList.remove("open"); });

  // --- Claim-stages page: scroll-spy on the phase-nav ---------------------
  const phaseNav = document.getElementById("phase-nav");
  if (phaseNav && "IntersectionObserver" in window) {
    const links = phaseNav.querySelectorAll("a[data-phase]");
    const targets = Array.from(links)
      .map(function (a) { return document.getElementById(a.dataset.phase); })
      .filter(Boolean);
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (a) { a.classList.remove("is-active"); });
          const active = phaseNav.querySelector('a[data-phase="' + entry.target.id + '"]');
          if (active) active.classList.add("is-active");
        });
      },
      { rootMargin: "-40% 0px -55% 0px" }
    );
    targets.forEach(function (t) { observer.observe(t); });
  }
})();
```

## 8. Explicit non-goals

- Not touching `/claimbuddy` (`claimbuddy_landing`), `templates/landing.html`
  (beyond the one added link), or any workspace route (`intake`,
  `dashboard`, `vault`, `policy`, `functional`, `gaps`, `letters`,
  `pack`, etc.).
- Not building a working waitlist backend, PAIA-request e-mail sending,
  or PDF export for the demo's "Export PDF" button — those stay
  presentational/demo-only, same as in the supplied prototype (waitlist
  form input/button rendered `disabled` with "coming soon" copy, §5.1).
- Not creating `pricing.html`, `privacy.html`, or `tools.html` as
  separate pages — content wasn't supplied for them; links repoint to
  the nearest real section (§3/§5) instead.
- Not adding a fourth CSS token system — `claimbuddy-marketing.css` uses
  literal values by design (§6), and the shared `.hero`/`.hub-card`/
  `.btn`/`.card` classes are reused unchanged everywhere else.

## 9. Build order / checklist

1. Add `templates/claimbuddy/_subnav.html` (§4).
2. Add the 5 templates (§5) — content + shared classes only, tabs/demo
   left inert (no JS yet) so pages render correctly before scripting.
3. Add the 5 routes to `app.py`, each passing `active=...` (§3).
4. Add `static/css/claimbuddy-marketing.css` (§6), wire `head_extra` on
   `home.html`, `claim_stages.html`, `demo.html` (`about.html`/
   `how_it_works.html` also need it for `.stage-step`).
5. Add `static/js/claimbuddy-marketing.js` (§7), wire `scripts` block on
   `home.html`, `claim_stages.html`, `demo.html`.
6. Add the one cross-link in `templates/landing.html` (§3).
7. Smoke-test every new route with the Flask test client (expect 200 on
   all five, plus the existing full route list unaffected — see
   `VERCEL=1 python -c` pattern already used in this repo's session
   history), then verify visually in both Classic and Editorial UI
   styles before pushing.
8. Push to `main` and the feature branch; confirm the Vercel deployment
   is READY with zero runtime errors (`get_deployment` +
   `get_runtime_errors`, as done for every previous change this
   session).

## 10. Design inspiration for the demo workspace — indigo SaaS language

The user supplied three Tailwind/FontAwesome mockups (full ecosystem
nav, detailed co-pilot, unified co-pilot) as layout inspiration. They're
built on a CDN stack this app doesn't use, so nothing gets copied
verbatim — but they share one clean, consistent component language that
is a better fit for `demo.html`'s workspace mockup (§5.5/§6/§7) than the
plainer version originally specified there. Where this section and §6
disagree on the demo workspace's look, this section wins; §5's page
*structure* (panels, tabs, sidebar) stays as specified, only the visual
treatment changes.

**Palette**: primary indigo `#4f46e5` (hover `#4338ca`), neutrals
`#0f172a`/`#1e293b`/`#64748b`/`#94a3b8` on `#f8fafc`/white, semantic
`#16a34a`/`#22c55e` (green, verified/ok), `#f59e0b`/`#fbbf24` (amber,
pending), `#ef4444`/`#f87171` (red, missing/urgent).

**Card**: white, `border-radius: 1rem` (`rounded-2xl`), `1px solid
#f1f5f9` border, `box-shadow: 0 1px 2px rgba(0,0,0,0.04)` at rest. On
hover (`.card-hover`): `translateY(-3px)` + `box-shadow: 0 16px 40px
rgba(0,0,0,0.06)`, transition `transform 0.15s ease, box-shadow 0.15s
ease`.

**Tag pill** (`.tag-pill`): `background:#eef2ff; color:#4338ca; padding:
0.2rem 0.8rem; border-radius:9999px; font-size:0.8rem; font-weight:500;
display:inline-flex; align-items:center; gap:0.4rem`. Clickable variant
hovers to `#dbeafe`.

**Status badge** (`.status-badge`, replaces the plainer `.demo-badge` in
§6): `font-size:0.65rem; font-weight:700; padding:0.15rem 0.6rem;
border-radius:9999px; text-transform:uppercase; letter-spacing:0.03em`.
Verified = `background:#dcfce7;color:#15803d`. Pending =
`background:#fef3c7;color:#92400e`. Missing/urgent =
`background:#fee2e2;color:#b91c1c`.

**Role tabs** (`.role-tab`, new — the demo workspace's sidebar becomes a
top-of-panel role switcher instead, reusing this component):
inactive `background:transparent;color:#374151`, hover
`background:#f3f4f6`; active `background:#4f46e5;color:#fff;box-shadow:0
4px 12px rgba(79,70,229,0.3)`. Sits in a pill-shaped container:
`background:#f3f4f6;padding:0.25rem;border-radius:0.75rem;display:inline-flex;gap:0.25rem`.

**Readiness ring** (replaces the plain progress bar for the demo's
"score" concept): SVG circle pair, `viewBox="0 0 100 100"`, radius 40,
`stroke-width:8`. Background ring `stroke:#e5e7eb;fill:none`. Progress
ring `stroke:#4f46e5;fill:none;stroke-linecap:round;
stroke-dasharray:251.2;transition:stroke-dashoffset 0.8s
ease-in-out;transform:rotate(-90deg);transform-origin:50% 50%`. Center
percentage label absolutely centered over the SVG. Color shifts by
value: `<50%` → `#ef4444`, `<75%` → `#f59e0b`, else `#4f46e5` (see the
`updateScore()` JS pattern below).

**Toast notifications** (new — use for the demo's simulated actions:
"request sent", "document uploaded", "pack exported", instead of
silently updating the DOM): fixed `bottom:2rem;right:2rem`, dark
`background:#0f172a;color:#fff;padding:0.9rem 1.5rem;border-radius:1rem;
box-shadow:0 24px 64px rgba(0,0,0,0.25)`, slides in via
`transform:translateY(140%)` → `translateY(0)` on `.show`, transition
`0.35s cubic-bezier(0.34,1.56,0.64,1)`, auto-dismiss after ~3s.

**Smart-ingest input pattern** (adopt for the demo's "sample data"
concept in `home.html`'s timeline tab, §5.1): a single text input +
primary button ("Analyze"/"Map"), with matched results rendered as tag
pills next to it and a small reasoning line below
(`.ingest-reason`-style, `font-size:0.7rem;color:#9ca3af`, hidden until
first analyzed). Keep the *canned-response* matching approach from the
mockups' `runSmartIngest()` (keyword regex → fixed condition/med/
occupation triples) — it's presentational, not a real NLP call, and
must stay labeled as sample/demo data per §8's non-goals.

**Modal** (replaces §6's `.demo-modal-*` styling, structure unchanged):
`background:rgba(15,23,42,0.5)` backdrop with `backdrop-filter:
blur(4px)`; card `transform:scale(0.96) translateY(12px)` →
`scale(1) translateY(0)` on open, `transition:transform 0.25s
cubic-bezier(0.34,1.56,0.64,1)`; sticky header with blurred white
background (`background:rgba(255,255,255,0.9);backdrop-filter:
blur(4px)`).

**Practical effect on §6/§7**: when implementing `demo.html`, swap the
flat `.demo-*` palette for these values (same class names, updated
declarations), add `.tag-pill`, `.status-badge`, `.role-tab`, a
`.toast` element + `triggerToast()` helper, and an SVG readiness ring
in place of the plain `.price-amount`-style number — everything else in
§5.5/§7 (panel structure, `showDemoPanel()`, modal open/close, scroll-spy)
stays as specified. Do not adopt Tailwind or FontAwesome as dependencies
— translate the utility classes shown here into the same
literal-value, framework-free CSS style already used throughout
`claimbuddy-marketing.css`, and swap FontAwesome icons for the inline
SVGs or emoji already used elsewhere in this app (`hub-icon` spans,
`demo-nav-btn` inline `<svg>`).
