# Testing architecture

> How quality is verified in this repo. Two phases, same checks, different fix targets.

## TL;DR

| | Phase A | Phase B |
|---|---|---|
| **Audience** | Skill authors (us) | Skill users (anyone who installs deckify) |
| **When** | After any change to the skill source | Every time a user runs the skill on their brand |
| **Scope** | 5-brand panel (Unilever / P&G / Stripe / Apple / Coca-Cola) | Single brand (the one the user is working on) |
| **Failure means** | Bug in **skill source** | Bug in **user's brand DS** |
| **Fix lives in** | `skills/deckify/{SKILL.md, references/, scripts/, evals/hard_checks.py}` | `decks/<brand>/<brand>-PPT-Design-System.md` |
| **Tooling** | `tools/phase-a/` | `skills/deckify/evals/` |
| **Run by** | `python3 tools/phase-a/run_phase_a.py` | `SKILL.md` Phase 4 (automatic) or `python3 skills/deckify/evals/hard_checks.py` (manual) |

**Same 10 hard checks + same 6 judge dimensions are used by both phases.** The only thing that changes is *what gets fixed when something fails*. That's the whole architectural insight.

---

## Why this split exists

The skill solves a hard problem: turn any brand URL into a verified, mobile-friendly Design System markdown. To stay reliable, two questions have to be answered separately:

1. **"Is the skill itself good enough?"** → Phase A. Run the skill across a diverse brand panel, fix the source whenever any brand fails. Subsequent brands inherit the fix automatically.
2. **"Does this specific brand DS produce decks that pass the bar?"** → Phase B. Run the same checks against the one brand the user is working on, point them at *their own DS file* to fix.

If you only have Phase B, every user has to re-discover bugs we've already found. If you only have Phase A, no end user gets feedback when their custom brand misbehaves. Both phases are mandatory.

The implementation reuses code aggressively — `hard_checks.py`, `rubric.json`, `build_report.py` are bit-for-bit identical between phases. Only the orchestrator (`run_phase_a.py`) and the structural pre-check (`audit_skill.py`) are Phase A-specific.

---

## Repository layout

```
deckify/
├── skills/deckify/                  ← what gets shipped to marketplace users
│   ├── SKILL.md                       ← entry point
│   ├── scripts/                       ← deterministic Phase 1 pipeline
│   ├── references/                    ← DS template + LLM guideline prompts
│   └── evals/                         ← runtime quality gate (PHASE B)
│       ├── hard_checks.py
│       ├── rubric.json
│       ├── build_report.py
│       ├── trigger_evals.json
│       └── README.md                  ← Phase B docs only
│
├── tools/phase-a/                   ← dev tooling (PHASE A) — not shipped
│   ├── run_phase_a.py                 ← orchestrator
│   ├── audit_skill.py                 ← structural pre-check (DRY / refs / DNA / anchor sync)
│   ├── evals.json                     ← 5-brand panel + marketplace grader cases
│   └── README.md                      ← Phase A docs only
│
├── decks/<brand>/                   ← per-brand outputs (one passing example each)
│   ├── <brand>-PPT-Design-System.md
│   ├── <brand>-deck.html
│   └── source/                        ← brand.json + decisions.json + assets/ + pages.txt
│
├── tests/reports/runs/              ← per-run output (gitignored)
│   └── <ts>(-phase-a)/per-sample/<brand>/{slides/, hard_checks.json, judge.json, ...}
│
├── README.md                          ← user-facing project intro
├── CLAUDE.md                          ← agent operating rules in this repo
├── HANDOFF.md                         ← rolling session-to-session state log
└── TESTING.md                         ← this file
```

**The boundary that matters**: `skills/deckify/` is what gets zipped up and submitted to the marketplace. Anything outside `skills/deckify/` is repo-internal. If you ever need to ask "should this go in `skills/deckify/` or somewhere else?", the test is: *does an end user pulling deckify from the marketplace need this file to run their brand?* If no, it doesn't belong inside `skills/deckify/`.

---

## The 10 hard checks

Defined in [`skills/deckify/evals/hard_checks.py`](skills/deckify/evals/hard_checks.py). All deterministic — no LLM. Cross-platform Python (no shell).

| # | Check | What it catches |
|---|---|---|
| 1 | `slide_dimensions` | Every `.slide` rect = 1280×720 ±2px |
| 2 | `fit_contract_intact` | Each `.sw .sc` has exactly one `flex:1 1 0` absorber with `min-height: 0` and `overflow: hidden` |
| 3 | `token_only_colors` | Slide CSS contains no ad-hoc hex literals outside `:root` |
| 4 | `no_emoji` | Body contains no emoji-range characters |
| 5 | `mobile_collapse` | At 375×812: `body.scrollWidth ≤ 375`, every `.g2/.g3/.flip-row/.tabs` collapses to single column |
| 6 | `logo_renders` | Every `.logo` SVG renders with non-zero bounding box; `<symbol id="brand-wm">` has real `<path d>` ≥ 40 chars OR `<image href>` |
| 7 | `text_layout_safe` | No truncated text, no glued-to-bottom, H1/H2/H3 ≤ 3 lines |
| 8 | `language_consistency` | DS markdown is single-language throughout (no leaked English in zh DS or vice versa) |
| 9 | `ds_has_engineering_dna` | DS markdown carries the ENGINEERING-DNA HTML comment anchors that hard_checks expects |
| 10 | `cjk_font_quality` | (zh decks only) at least one CJK font in body font-family chain — hard FAIL if zero, soft warning if Latin-first |

A brand passes hard checks when **all 10 pass** (or when only `cjk_font_quality` is in soft-warning state for an en deck).

## The 6 judge dimensions

Defined in [`skills/deckify/evals/rubric.json`](skills/deckify/evals/rubric.json). Scored 0–5 by the LLM running the skill, after reading the per-slide screenshots that hard_checks emits.

1. `logo_present_and_branded` — real wordmark on every slide, not a typographic placeholder
2. `slide_visual_quality` — composition, hierarchy, breathing room
3. `brand_fidelity` — does it look unmistakably *this brand*, not generic SaaS
4. `content_substantive` — copy is real, on-domain, recon-anchored — no AI filler
5. `engineering_dna_visible_in_ds` — DS markdown explicitly carries the engineering invariants
6. `cjk_typography_quality` — (zh decks only) CJK glyphs render with characterful family, weights match Latin

Plus 5 disqualifiers: D1 logo missing, D2 dimensions wrong, D3 console errors, D4 mobile horizontal scroll, D5 DS template violated.

## Pass criteria

```
PASS = (hard_checks == 10/10  OR  9/10 with only cjk_font_quality soft)
       AND (judge_avg ≥ 4.0)
       AND (no disqualifier triggered)
```

In Phase A, **every brand in the panel** must individually PASS. In Phase B, **the one brand the user is working on** must PASS.

---

## Adding a new brand to the Phase A panel

The panel currently has 5 brands chosen for visual / typographic / language diversity. Adding a brand means:

1. Run the skill end-to-end on the new brand → produces `decks/<new-brand>/`.
2. Verify it PASSes (hard 10/10 + judge ≥ 4) on its own first — if it doesn't, that's a skill bug to fix before adding to panel.
3. Add a row to `PANEL` in [`tools/phase-a/run_phase_a.py`](tools/phase-a/run_phase_a.py).
4. Re-run `tools/phase-a/run_phase_a.py` to make sure all `len(PANEL)` brands still PASS.

Drop a brand only when it stops adding signal beyond what others already cover. The panel is a *test surface*, not a museum.

---

## Anti-patterns

- **Editing only the deck** to make a check pass. The deck is the test, the DS is the spec; only the spec deserves the fix. (Per-brand DS in Phase B; ds-template.md in Phase A.)
- **Fixing `decks/<brand>/<brand>-PPT-Design-System.md` during a Phase A failure.** That heals one brand and lets the bug ship to every other brand. Trace upstream into `references/ds-template.md` or the relevant prompt / script.
- **Skipping the audit step** when iterating on `hard_checks.py`. Fine sometimes (use `--skip-audit`), but a habit of skipping it lets structural drift accumulate.
- **Adding files to `skills/deckify/` that aren't needed for an end-user run.** That's how the shipped skill bloats. Dev tooling lives at `tools/`.
- **Not updating `LANGUAGE_SPECIFIC_ANCHORS` in `audit_skill.py`** when introducing a new zh-only or en-only ENGINEERING-DNA chapter. The audit will catch you, but it's nicer to update the allowlist in the same change.

---

## Pointers

- Phase A operations: [`tools/phase-a/README.md`](tools/phase-a/README.md)
- Phase B operations: [`skills/deckify/evals/README.md`](skills/deckify/evals/README.md)
- Per-failure fix routing: [`skills/deckify/references/verification-deck-spec.md`](skills/deckify/references/verification-deck-spec.md) §8
- Phase A vs Phase B fix-target rule: [`CLAUDE.md`](CLAUDE.md) §2
