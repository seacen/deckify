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
| 3 | Two-column comparison | Type B | Side-by-side panels via `.g2`; **the** mobile-collapse target; tests `--accent` vs `--primary` accent contrast. |
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

## 6. Per-brand emphasis (illustrative — not a closed list)

Same eight required types, but brands have natural strengths. The table below illustrates the kind of tilt to look for, using brands from our Layer 1 panel as examples — it is NOT a whitelist. For any new brand, infer the analogous tilt from Phase 1 recon (the brand's own page rhythm, voice register, and content density).

| Example brand | Lean into | De-emphasize |
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

---

## 8. When a check fails: which section of your brand DS owns the rule?

**The brand DS is your tunable. The deck is just the verification of it.** When a runtime check fails, the fix lives in a specific section of *your brand's* `<brand>-PPT-Design-System.md`. Update the DS, regenerate the deck from the updated DS, re-run the check.

| Failing check / observation | Section of *your* DS to fix | What to verify is present |
|---|---|---|
| `slide_dimensions` (offset ≠ 1280×720) | DS §5 Scaffold + the scale-to-fit `<script>` block | The deck must keep the canvas at fixed `width: 1280px; height: 720px;` and use a CSS-transform `scaleDeck()` runtime to fill the viewport. Never resize the canvas to viewport units. |
| `fit_contract_intact` (≠ exactly one `flex:1 1 0` absorber per `.sc`, or absorber missing `min-height: 0` / `overflow: hidden`) | DS §5.1 Single-Slide Fit Contract | Each content slide's `.sc` has exactly one absorber; absorber carries `min-height: 0` AND `overflow: hidden`; non-absorber children are `flex: 0 0 auto`. |
| `token_only_colors` (ad-hoc hex outside `:root`) | DS §2 Colour Tokens — extend the token list rather than inlining hex | Every CSS color in the deck reads through `var(--token)`. If you need a new accent, add it to §2 (with a name + evidence + hex) and use `var(--new-token)`. |
| `no_emoji` (👍🎉 etc. found) | DS §1 Hard constraints | Replace any emoji with a typographic symbol (✓ — ! × → ←). The no-emoji rule is invariant. |
| `mobile_collapse` (body.scrollWidth > 375 OR multi-col still flex-row at 375 px) | DS §10 Mobile | The `@media (max-width: 768px)` block must include: (a) `.g2, .g3, .flip-row, .tabs { grid-template-columns: 1fr; flex-direction: column }`, (b) inline-flex catch-all `.sc div[style*="display:flex"] { flex-direction: column !important }`, (c) `.cov, .sw { min-height: 100dvh }`. If you added a new multi-col class, extend the §10 selector list to cover it. |
| `logo_renders` (typographic placeholder, path `d` < 40 chars, no `<image href>`, or `<symbol>` inner element has hardcoded `fill` overriding `currentColor`) | DS §4 Logo | The `<symbol id="brand-wm">` must contain either a real `<path>` with `d` ≥ 40 chars OR an `<image href="data:...">`. Outer SVG carries `fill: currentColor`; inner paths carry no hardcoded fill. If the gate rejected your candidate, get a better logo file and re-embed (re-run `embed_logo.py` with a different `chosen_logo.id`). |
| `text_layout_safe` overflow (text container with `overflow:hidden` but `scrollHeight > clientHeight`) | DS §3.1 Typography Safety + the specific slide-type density rule in §6 (e.g. Type E Row-count rule for tables) | First try cutting copy or splitting the slide. Don't shrink fonts below the §3 readability floor. If a per-slide-type density rule fits the symptom, follow it (Type E: 5 rows max at standard padding; 6+ rows requires tightened padding or splitting). |
| `text_layout_safe` bottom-glue (text within 18 px of slide bottom) | DS §5.1 (asymmetric padding) + per-type §6 spec | Switch `.sw .sc` to asymmetric `padding: 24px 80px 40px 96px` on slides that consistently glue. The 40 px bottom pad guarantees breathing room. |
| `text_layout_safe` heading > 3 lines | DS §3.1 max-line cap + per-type title-length budget in §6 | Cut the title — typically dropping subordinate clauses or splitting "X — Y" structures. Don't reduce H1/H2/H3 font sizes below the §3 floor. |
| `cjk_font_quality` FAIL (zh deck — no CJK font anywhere in body font-family) | DS §3 CJK 字体回退链 | Add at least one CJK family (PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans SC) to the chain in DS §3, then regenerate the deck. Without any CJK font, every CJK char falls through to OS default and renders thinly. |
| `cjk_font_quality` warning (zh deck — CJK font present but Latin family is first) | DS §3 (optional) | This is intentional design space, not always a bug. If your deck is English-heavy with occasional CJK, leaving Latin first is fine. If CJK glyphs look thin / cheap to vision judge, swap order to put CJK first AND consider bumping body `font-weight` from 400 → 500 (PingFang SC Medium reads heavier and matches Latin sans weight better). |
| `ds_has_engineering_dna` (required phrase missing from your DS) | The DS chapter that owns the phrase | Restore the phrase verbatim. Required: "Single-Slide Fit Contract", "three-layer overflow safety net", "inline-flex trap", "this.classList.toggle", "12 px floor"/"Nothing below 12 px", "Typography Safety". A language pass is the most common cause of dilution — translate prose only, never the engineering-DNA phrases. |
| Judge `logo_present_and_branded` < 4 | DS §4 (logo embed) + your brand.json `chosen_logo.id` | The logo embedded is too generic or wrong (utility icon, single-letter disc). Pick a different `chosen_logo.id` from `brand.json.alt_logo_ids` (or get a better source file from the user) and re-run `scripts/embed_logo.py`. |
| Judge `slide_visual_quality` < 4 | DS §6 (per-slide-type spec) + §7 (component density) + §3 type scale | Tighten the relevant section — sizes, spacing, gap minimums. A slide reading "cramped" usually means component spacing in §7 needs more gap; "weak hierarchy" usually means type-scale ratios in §3 need bumping. |
| Judge `brand_fidelity` < 4 (generic, not on-brand) | DS §1 Design Philosophy + §1 Design Taste | The mood paragraph and the anti-slop rules drove this. Sharpen the mood (specific words: "editorial sustainability gravitas", not "modern clean bold"). Re-check the §2 palette against the actual brand recon — flatten to white+grey+single-accent is the AI-slop signature. |
| Judge `content_substantive` < 4 (vague filler) | Your deck content + the `brand.json` evidence_screenshots | The deck copy isn't drawing from the recon corpus. Re-read the recon screenshots and pull verbatim phrases / numbers; never invent stats. |
| Judge `engineering_dna_visible_in_ds` < 4 | DS chapters listed in §13 Pre-ship checklist | A chapter is missing or got diluted. Run through the pre-ship checklist; restore each missing piece from the source template. |
| Disqualifier D1 logo missing/placeholder | DS §4 + brand.json | Same as `logo_renders`. **Never** ship a typographic placeholder. If `embed_logo.py` rejects every candidate, ask the user for a logo file. |
| Disqualifier D3 console error in deck | The deck CSS/JS (one-off bug) — but if the error class repeats across brands, the pattern in DS §11 Animation or §10 Mobile needs fixing | Most console errors are typos in the deck (missing CSS escape, malformed JS). Fix the deck. If the same class of error keeps appearing across brands, escalate to fixing the DS §11 / §10 pattern. |

**The general principle**: the brand DS is *your* spec for *your* brand's slides. The deck is just the test of that spec. Fix the spec, regenerate the test, run again.

> ### Note for skill developers (Phase A — tuning the skill itself)
>
> If you're working in the deckify skill repo (not just using the skill on your brand), failures often point at *both* the brand DS AND a gap in the upstream skill source — `skills/deckify/references/ds-template.md`, an LLM prompt, or a script. The rule "fix the brand DS first, then regenerate the deck" still applies; but ALSO push the rule into `ds-template.md` so the next brand picks it up automatically. See `CLAUDE.md` §2 in the project root for the upstream-fix workflow.
