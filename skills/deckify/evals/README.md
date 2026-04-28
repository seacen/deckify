# skills/deckify/evals — quality contract

This directory holds the quality gates for deckify. **Two layers, one set of tools, two different fix targets.**

The single most important thing to understand before reading code in here: **the same 10 hard checks + 6-dimension visual judge are used by both layers**. What changes is _what gets fixed when something fails_:

- **Layer 1 — skill-quality optimization loop**: failures fix the **skill source** (`SKILL.md`, `ds-template.md`, prompts, scripts, the eval framework itself). Run during skill development.
- **Layer 2 — runtime per-user gate**: failures fix the **user's own brand DS** (`decks/<brand>/<brand>-PPT-Design-System.md`). Run automatically every time the skill executes Phase 4.

Same tools, different debugging direction. That's the whole architecture.

---

## Layer 1 — skill-quality optimization loop (Phase A)

**Audience**: us, the skill authors, while we're tuning deckify.

**The loop**:
```
   ┌────────────────────────────────────────────────────────────┐
   │ 1. Pick N representative brands (currently 5: Unilever /   │
   │    P&G / Stripe / Apple / Coca-Cola — sans-serif + serif,  │
   │    blue + red + black + cream, en + zh)                    │
   ├────────────────────────────────────────────────────────────┤
   │ 2. Run the skill end-to-end on each brand → produce        │
   │    decks/<brand>/<brand>-PPT-Design-System.md +            │
   │    decks/<brand>/<brand>-deck.html                         │
   ├────────────────────────────────────────────────────────────┤
   │ 3. Run hard_checks.py on each brand's deck + DS            │
   │    (10 deterministic DOM / regex checks)                   │
   ├────────────────────────────────────────────────────────────┤
   │ 4. LLM (you) reads the slide screenshots + DS markdown,    │
   │    scores judge.json against the 6-dim rubric              │
   ├────────────────────────────────────────────────────────────┤
   │ 5. Aggregate scoreboard via build_report.py:               │
   │    PASS = hard 10/10 AND judge avg ≥ 4 AND no DQ           │
   ├────────────────────────────────────────────────────────────┤
   │ 6. **A failure here means a skill source bug**, not a      │
   │    brand bug. Trace upstream: which template clause /      │
   │    prompt / script let this through? Fix THAT. Then        │
   │    regenerate the brand DS from the updated template,      │
   │    regenerate the deck from the updated DS, re-run.        │
   ├────────────────────────────────────────────────────────────┤
   │ 7. Goto 2. Loop until all N brands PASS.                   │
   └────────────────────────────────────────────────────────────┘
```

**Why this is "Layer 1" not just "regression testing"**: every loop iteration improves the skill. A bug found on Coca-Cola becomes a new rule in `ds-template.md`, a new anchor in `hard_checks.py`, or a sharpened heuristic in `references/llm-prompts/synthesize-brand.md`. Subsequent brands inherit the fix automatically — you don't have to re-discover it.

This is the optimization mechanism for the skill itself. Marketplace evals (below) are a downstream gate, not the loop.

### Files used by Layer 1

The Layer 1 toolset is a strict superset of Layer 2's:

| File | Role | Shared with Layer 2? |
|---|---|---|
| `audit_skill.py` | **Structural pre-check** — DRY + reachability + ENGINEERING-DNA + path-leakage. Runs first; fails fast on skill-source bugs before any brand panel work. | **Layer 1 only** |
| `hard_checks.py` | 10 deterministic checks per brand | yes |
| `rubric.json` | 6 visual judge dimensions | yes |
| `build_report.py` | Per-brand scoreboard aggregation | yes |
| `run_phase_a.py` | **Layer 1 entry point** — orchestrates `audit_skill.py` → `hard_checks.py` over the registered brand panel → emit judge instructions → `build_report.py`. Cross-platform Python (no shell). | **Layer 1 only** |
| `evals.json` | 4 declarative cases for Anthropic's marketplace grader | Layer 1 only (marketplace) |
| `trigger_evals.json` | 22 routing samples for the marketplace grader | Layer 1 only (marketplace) |

`evals.json` and `trigger_evals.json` are the marketplace grader's input — they're a *thin slice* of Layer 1, not the whole thing. The whole thing is the loop above.

### Running Layer 1 locally

```bash
# 1. Full Layer 1 run (audit → hard checks across brand panel → emit judge instructions)
python3 skills/deckify/evals/run_phase_a.py

# 2. The script prints which brands need a judge.json. For each:
#    - View the slide screenshots in tests/reports/runs/<latest>-phase-a/per-sample/<brand>/slides/
#    - Read the brand DS markdown
#    - Score against rubric.json
#    - Write tests/reports/runs/<latest>-phase-a/per-sample/<brand>/judge.json

# 3. Re-run aggregation to fold the judge scores in
python3 skills/deckify/evals/run_phase_a.py --aggregate-only

# Useful options:
# --brands unilever,coca-cola   limit panel to a subset
# --skip-audit                  skip step 1 (when iterating on hard_checks)
```

If `audit_skill.py` (step 1) reports failures, `run_phase_a.py` halts before touching the brand panel — fix the structural issue first. To run the audit standalone (no network, no brand panel):

```bash
python3 skills/deckify/evals/audit_skill.py
```

### When a Layer 1 brand fails

The fix-mapping is **inverted** vs Layer 2:

| Layer 2 (user's deck fails) | Layer 1 (our brand panel fails) |
|---|---|
| Fix `decks/<brand>/<brand>-PPT-Design-System.md` | Fix `skills/deckify/references/ds-template.md` (or .zh.md) — so EVERY future brand picks it up |
| Fix one brand DS section | Fix the engineering-DNA template chapter that should have constrained this |
| Update one row in `decks/<brand>/source/decisions.json` | Sharpen `references/llm-prompts/synthesize-brand.md` so the LLM picks better next time |
| Change the deck's HTML | Add a new rule to `evals/hard_checks.py` AND fix the upstream template clause that violated it |

If you ever find yourself fixing `decks/<brand>/<brand>-PPT-Design-System.md` in Layer 1 mode, **stop**. That's a Layer 2 fix — it heals one brand and lets the bug ship to every other brand. Trace upstream first.

---

## Layer 2 — runtime per-user gate (Phase B)

**Audience**: the skill running on a user's machine, on the user's brand. Phase 4-5 of `SKILL.md` invokes this as a mandatory gate.

**The flow**:
```
   ┌────────────────────────────────────────────────────────────┐
   │ User runs deckify on their URL → Phase 4 produces a        │
   │ deck.html + DS.md                                          │
   ├────────────────────────────────────────────────────────────┤
   │ Phase 4 invokes (cross-platform, no shell):                │
   │   - hard_checks.py on the single brand                     │
   │   - then asks the LLM to write judge.json                  │
   ├────────────────────────────────────────────────────────────┤
   │ LLM (you, mid-skill-execution) writes judge.json           │
   ├────────────────────────────────────────────────────────────┤
   │ build_report.py rolls up the score                         │
   ├────────────────────────────────────────────────────────────┤
   │ **A failure here means a brand-DS bug.** The user doesn't  │
   │ have the skill source; they have their own DS markdown.    │
   │ Look up the failing check in references/                   │
   │ verification-deck-spec.md §8 fail-mapping table → fix the  │
   │ corresponding section of decks/<brand>/<brand>-PPT-Design- │
   │ System.md → regenerate the deck → re-run.                  │
   └────────────────────────────────────────────────────────────┘
```

**Layer 2 is Layer 1 baked into runtime** — it inherits the same checks and rubric, but the optimization target is the user's brand DS rather than the skill source. By the time we ship, the skill source is supposed to already be optimized (Layer 1 saw to that), so a Layer 2 failure points at *this brand's* idiosyncrasy.

### Files used by Layer 2

`hard_checks.py`, `rubric.json`, `build_report.py` — same files as Layer 1 minus `run_phase_a.py` and the marketplace JSONs. There is no shell wrapper; SKILL.md Phase 4 invokes the Python entrypoints directly so the runtime path stays cross-platform.

### Running Layer 2 locally (during skill development)

You generally don't run Layer 2 directly — it's invoked by `SKILL.md` Phase 4. But to manually re-evaluate a single brand:

```bash
python3 skills/deckify/evals/hard_checks.py \
  decks/<brand>/<brand>-deck.html \
  decks/<brand>/<brand>-PPT-Design-System.md \
  skills/deckify/tests/reports/runs/<ts>/per-sample/<brand>/
```

Then write `judge.json` per `rubric.json`, then run `build_report.py` to roll up the score.

---

## Pass criteria (both layers)

A brand PASSes when:
- Hard checks: 9/10 or 10/10 (cjk_font_quality is soft for en decks)
- Judge avg: ≥ 4.0 across the 6 dimensions
- No disqualifier triggered (D1 logo missing, D2 dimensions wrong, D3 console errors, D4 mobile horizontal scroll, D5 DS template violated)

In Layer 1 we want **all N brands** to PASS. If 4 PASS and 1 FAILs, we still have a skill bug — fix it.

In Layer 2 we want **the one brand** to PASS. The user iterates on their DS until it does.

---

## How the marketplace grader fits

`evals.json` + `trigger_evals.json` are read by **Anthropic's skill-eval grader at marketplace submission time**. They're declarative (file_contains, regex_in_file, transcript_contains) and they verify a thin slice of Layer 1 — basically "did the skill emit the expected DS structure and call the right scripts?"

They are NOT the Layer 1 optimization loop. They're a downstream contract that the loop's outputs need to satisfy. If `run_phase_a.py` is green across our brand panel, `evals.json` should also be green at marketplace submission — and if it's not, that's a gap in our brand panel coverage, not a separate testing system.

**Host portability of evals.json**: one assertion (`process_called_ask_user_question`) checks the transcript for the literal string `AskUserQuestion`, which is Claude-Code-specific. When other grader hosts (Codex / OpenClaw) ship their own marketplace grader, this assertion should be replaced with a host-neutral signal (e.g. file_contains on `decisions.json` proving Phase 2 happened). The runtime path itself (the skill scripts + SKILL.md prose) is already host-neutral; only this one grader assertion isn't.

---

## Quick reference: what runs when

| Trigger | What runs | Fix target on failure |
|---|---|---|
| Skill author tunes skill | `python3 evals/run_phase_a.py` (audit → panel → aggregate) | **Skill source** (template, prompts, scripts, hard_checks) |
| Author wants the structural audit only (no brand network calls) | `python3 evals/audit_skill.py` | **SKILL.md / docs / references / template that drifted** |
| Marketplace submission | `evals.json` + `trigger_evals.json` (Anthropic harness) | **Skill source** (same — these are Layer 1) |
| End user runs the skill | `python3 evals/hard_checks.py` + `build_report.py` (auto, in Phase 4) | **User's brand DS markdown** |
