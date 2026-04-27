# TEST_PLAN.md — actionable E2E plan for `web-to-design-system`

This is the runnable test plan. Each step has a command, an exit criterion, and an artifact to inspect. The full sweep maps 1:1 to the Skillify 10-step layers in `TESTING.md`.

## Order of execution

| # | Layer | Command | Pass criterion | Artifact |
|---|---|---|---|---|
| 1 | Reachability + DRY audit | `bash tests/audit_skill.sh` | `audit passed.` exit 0 | stdout |
| 2 | Unit tests (Python stdlib) | `python3 -m unittest tests.test_extract_brand` | `OK`, all tests pass | stdout |
| 3 | Integration (live) | `bash tests/test_integration.sh` | All 3 brands produce ≥3 brand candidates and a logo path | `tmp/integ-<brand>/brand-recon.json` |
| 4 | Phase-1 smoke (deterministic) | `bash tests/smoke_unilever.sh` | `OK — Phase 1 smoke passed.` | `/tmp/web-to-ds-smoke/<ts>/brand-recon.json` |
| 5 | Trigger evals (description matches intent) | `bash tests/run_trigger_evals.sh` | ≥ 80% of pos triggers + ≥ 80% of neg refusals as a static keyword scan | stdout summary |
| 6 | E2E deliverable (the user-facing acceptance) | latent execution against `https://www.pg.com` | Two files exist: `./pg-PPT-Design-System.md` + `./pg-deck.html`, and the deck renders content-richly at native 1280×720 | the two files |
| 7 | One-shot orchestrator | `bash tests/run_all.sh` | Steps 1–5 sequentially pass | aggregated stdout |

## Layer 6 — deliverable acceptance criteria (what the user reviews)

- [ ] `./pg-PPT-Design-System.md` exists, mirrors the §1–§13 template structure, with engineering DNA verbatim and brand-variable parts filled from P&G recon
- [ ] `./pg-deck.html` is one self-contained file, 1280×720 fixed canvas
- [ ] The deck is **content-rich**: at minimum a cover + 7 content slides exercising **Type A (cover) + Type B (two-col) + Type C (full-width narrative) + Type D (flip cards) + Type E (data table) + Type F (image / image-suggested) + Type H (chart) + Type J (pull-quote) + Type K (timeline)**
- [ ] Every slide carries the logo: white-on-dark on cover, brand-dark on light content slides
- [ ] Token-only colors (no ad-hoc hex literals in the slide CSS — all `var(--…)`)
- [ ] §10 mobile rules in effect: at 375px width, every multi-col layout collapses to single column, no horizontal scroll
- [ ] No emoji anywhere
- [ ] Pre-ship checklist (§13) items all pass

## What's NOT in this plan (and why)

- **Trigger eval optimization loop** (skill-creator's `run_loop.py`): out of scope for this run — that's a multi-iteration loop that runs the live model 60+ times and tunes the description string. We use the static keyword-scan approximation in step 5 to confirm the current description doesn't have obvious holes.
- **Blind A/B comparison**: only useful when iterating against a prior version of the skill. This is the first version.
