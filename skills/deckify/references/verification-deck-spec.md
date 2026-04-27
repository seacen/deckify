# Verification Deck Spec

> What every Phase 4 verification deck (`decks/<brand>/<brand>-deck.html`) must contain so it actually proves the Design System works in real-world PPT scenarios — not just survives the auto-eval.

---

## Why this exists

A 4-slide deck (cover + narrative + 2-col + flip) passes hard checks but says little about **whether the DS is good for actual presentations**. Real decks need charts, tables, timelines, quotes, comparisons, image slides — the full vocabulary that consumer-grade slide tools cover.

This spec defines the minimum coverage so each brand's verification deck stress-tests the DS across the typical scenarios a real presentation would hit. If a brand's DS produces a beautiful cover but breaks on a bar chart, the eval as-currently-shaped wouldn't catch it. This spec closes that gap.

It applies to **every** brand. The "what" stays constant (this slide-type list), the "what content" varies by brand (pull from each brand's own recon corpus).

---

## 1. Required slide types

A verification deck **must** contain a slide for each of these. They map 1:1 to Section 6 of the DS template, so any DS that follows the template can produce them.

| # | Slide Type | DS §6 ref | Purpose in the eval |
|---|-----------|-----------|---------------------|
| 1 | Cover | Type A | Primary brand statement; white-on-dark logo top-right; tests cover hierarchy, no-decorative-line rule. |
| 2 | Full-width narrative + pullquote | Type C | Long-form prose flow; tests body line-height, pull-quote treatment, single-absorber math when content is text-only. |
| 3 | Two-column comparison | Type B | Side-by-side panels via `.g2`; **the** mobile-collapse target; tests `--blue` vs `--navy` accent contrast. |
| 4 | Data table | Type E + §7.7 | Real tabular data with semantic colour cells (`.pos` / `.neg` / `.neu`); tests row rhythm, ALL-CAPS labels at 13–14 px, no badge crutch. |
| 5 | Chart / quantitative insight | Type H + §7.8 | One primary visualization (bar / line / sparkline); tests animated entrance, "title states the insight" rule, callout placement. |
| 6 | Flip cards | Type D + §10 mobile flip | Two `.fc` cards with `onclick="this.classList.toggle('on')"`; tests perspective + backface visibility on desktop AND the mobile show/hide override. |
| 7 | Timeline / roadmap | Type K + §7.12 | Horizontal or vertical milestones; tests temporal sequence layout, label-number rhythm. |
| 8 | Pull-quote / takeaway | Type J | Single striking statement; tests display-size type at 28–36 px, attribution treatment, restraint (no decorative noise). |

Eight slides is the floor. A brand may add more.

## 2. Encouraged when the brand supports it

Add these when the recon corpus gives you the raw material. Skip silently if it doesn't — half-baked is worse than missing.

| Slide Type | DS §6 ref | When to include |
|-----------|-----------|-----------------|
| Image slide | Type F | Brand has its own imagery in recon (product UI, factory shot, hero photography). Never substitute stock. |
| Tabs | Type I + §7.9 | Content has 2–4 natural categories that share a frame (e.g. regional breakdowns, before/after, capability matrix). |
| Stat-card row | §7.4 | Brand publishes meaningful KPIs in its recon. 3–4 large numbers in a row, each with caption. Pairs well as the second slide. |
| Interactive demo | Type G | Only when the narrative *needs* live demonstration. Most brand decks don't. |

## 3. Coverage rules (independent of slide type)

Across the whole deck, these must all be hit:

- **Multi-column collapse**: ≥1 slide with `.g2` or `.g3`. Mobile catch-all must verify.
- **Click interaction**: ≥1 slide with `onclick` (the flip cards count).
- **Semantic colour signal**: ≥1 slide where `--green` / `--red` / `--warn` / `--teal` carries actual meaning (pass/fail, ahead/behind, on/off track) — not decoration.
- **Quantitative element**: ≥1 slide with real numbers (chart, table, or stat row). Numbers come from recon, not invention.
- **Bespoke composition**: ≥1 slide that does NOT lean on a named §7 component — proves the DS is a toolkit, not a menu.
- **Variety in the absorber**: at least three different patterns of "what fills the flex:1 absorber" (e.g. text column, grid, table, chart).

## 4. Content rules (the hard line)

- **Real copy from recon only.** No invented stats. If the brand's recon doesn't yield enough numbers for a chart, build the chart from real recon numbers and label the rest as "qualitative" — don't fabricate "27%" because it looks better.
- **No emoji** anywhere. Typographic symbols (`✓ — ! × → ←`) are fine.
- **Single language** within a deck. If the user picked 中文 in Phase 2, *every* user-facing string is Chinese; if English, every string is English. No mixed-language drift.
- **Cite where helpful.** A small `.cap` or footnote citing the recon page (e.g. `SOURCE: /sustainability/`) earns trust and helps the judge verify content provenance.

## 5. Eval target

- All 8 hard checks pass for the brand.
- Judge avg ≥ 4 across the 5 dimensions (logo / visual / brand fidelity / content / engineering DNA).
- No disqualifier triggered (D1 logo, D2 dimensions, D3 console errors, D4 mobile scroll, D5 DS template violation).

If any required slide above causes a hard check to fail, **fix the slide**, don't drop the type. Dropping a type to game the eval defeats the purpose.

## 6. Per-brand emphasis

Same eight required types, but brands have natural strengths:

| Brand | Lean into | De-emphasize |
|-------|-----------|---------------|
| Unilever | Sustainability narrative (Type C), pull-quotes from leadership (Type J), brand-portfolio image slide (Type F if recon has good photography) | Heavy interactive demos (Type G) |
| P&G | Brand portfolio (Type F), category data (Type E table), consumer trend chart (Type H) | Long pull-quote slides — P&G voice is operational, not editorial |
| Stripe | Data density (Type E table, Type H chart, stat-card row), product-flow timeline (Type K), code-adjacent typography | Decorative imagery |

Use this only as a tilt. Every brand still ships all eight required slide types.

## 7. Pre-flight checklist (before running eval)

- [ ] All 8 required slide types present
- [ ] All 6 coverage rules satisfied (multi-col, onclick, semantic colour, numbers, bespoke, absorber variety)
- [ ] Every stat / quote / claim traceable to a recon page
- [ ] One language throughout (no mixed-language drift)
- [ ] No emoji (grep `[\U0001F300-\U0001FAFF]`)
- [ ] Logo on every slide; `<symbol id="brand-wm">` has `path d > 40` chars or `<image href>`
- [ ] DS file passes `ds_has_engineering_dna` (Single-Slide Fit Contract / three-layer overflow safety net / inline-flex trap / `this.classList.toggle` / 12 px / Typography Safety)
- [ ] Verified at native 1280×720 (not the scaled view)
- [ ] Verified at 375 px width — every multi-col stacks; flip card click reveals back face
