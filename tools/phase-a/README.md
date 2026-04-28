# tools/phase-a — skill-quality optimization loop (Phase A)

Dev tooling for tuning the deckify skill itself. **Not part of the shipped skill** — these scripts are for skill authors, not skill users.

> See [TESTING.md](../../TESTING.md) for the architectural picture: Phase A (here) vs Phase B (`skills/deckify/evals/`).

## When to run Phase A

After making any change to the skill source — `SKILL.md`, `references/ds-template.md` (or `.zh.md`), `references/llm-prompts/*.md`, `scripts/*.py`, or `evals/hard_checks.py`. Phase A re-runs the hardened brand panel and tells you whether the change is a net improvement, a regression, or neutral.

## Files

| File | Role |
|---|---|
| `audit_skill.py` | Structural pre-check — DRY + reachability + ENGINEERING-DNA + cross-template anchor sync + path-leakage. Fast (no network). Runs before any brand work. |
| `run_phase_a.py` | Orchestrator — runs `audit_skill.py` → invokes `skills/deckify/evals/hard_checks.py` over the brand panel → emits judge.json TODO list → calls `skills/deckify/evals/build_report.py` to aggregate. |
| `evals.json` | The 5-brand panel definition (Unilever / P&G / Stripe / Apple / Coca-Cola — sans+serif, blue+red+black+cream, en+zh) plus declarative cases for Anthropic's marketplace grader. |
| `README.md` | This file. |

## The Phase A loop

```
   ┌────────────────────────────────────────────────────────────┐
   │ 1. audit_skill.py — fail-fast on skill-source structural   │
   │    bugs (broken refs, drifted DNA, anchor desync)          │
   ├────────────────────────────────────────────────────────────┤
   │ 2. For each of the N brands in the panel, run the same     │
   │    hard_checks.py + judge.json + build_report.py that      │
   │    ships with the skill (Phase B). Same checks, panel      │
   │    width.                                                  │
   ├────────────────────────────────────────────────────────────┤
   │ 3. Any failure means a SKILL SOURCE bug — not a brand bug. │
   │    Trace upstream: which template clause / prompt /        │
   │    script let this through? Fix THAT. Then regenerate the  │
   │    brand DS from the updated template, regenerate the      │
   │    deck from the updated DS, re-run.                       │
   ├────────────────────────────────────────────────────────────┤
   │ 4. Goto 2. Loop until all N brands PASS.                   │
   └────────────────────────────────────────────────────────────┘
```

## Running

```bash
# Full loop: audit + panel + aggregate
python3 tools/phase-a/run_phase_a.py

# After judge.json files have been written, fold them in:
python3 tools/phase-a/run_phase_a.py --aggregate-only

# Subset of brands:
python3 tools/phase-a/run_phase_a.py --brands unilever,coca-cola

# Skip step 1 (when iterating on hard_checks):
python3 tools/phase-a/run_phase_a.py --skip-audit

# Run the audit standalone (no network, no brand panel):
python3 tools/phase-a/audit_skill.py
```

Run output lands at `tests/reports/runs/<ts>-phase-a/` at the repo root (gitignored).

## Fix routing (Phase A failures)

If a Phase A brand fails, the cure is in the skill source — never in `decks/<brand>/<brand>-PPT-Design-System.md` directly:

| Symptom | Where to fix |
|---|---|
| Hard check fails on multiple brands | `skills/deckify/evals/hard_checks.py` (rule too strict?) OR `skills/deckify/references/ds-template.md` (rule should have been baked in) |
| Hard check fails on one brand only | Inspect — is it the brand's recon being weird, or did the synthesizer make a wrong call? Fix in `references/llm-prompts/synthesize-brand.md` if the LLM should have seen this. |
| Judge `brand_fidelity` low | `references/llm-prompts/synthesize-brand.md` (mood paragraph generator weak) OR `references/ds-template.md` Type spec |
| Judge `engineering_dna_visible_in_ds` low | `references/ds-template.md` chapter got diluted / a new DNA chapter wasn't backfilled into both en + zh |
| Anchor sync drift detected by audit | One template added a chapter the other didn't get — copy across, or update `LANGUAGE_SPECIFIC_ANCHORS` in `audit_skill.py` if it's intentionally one-language-only |

**If you ever find yourself fixing `decks/<brand>/<brand>-PPT-Design-System.md` in Phase A mode, stop.** That's a Phase B fix — heals one brand, lets the bug ship to all others. Trace upstream first.

## Pass criteria

For Phase A to PASS overall, **every** brand in the panel must individually PASS by the same criteria as Phase B:
- Hard checks: 9/10 or 10/10 (`cjk_font_quality` is soft for en decks)
- Judge avg: ≥ 4.0 across the 6 dimensions
- No disqualifier (D1 logo / D2 dimensions / D3 console errors / D4 mobile scroll / D5 DS template violated)

If 4 brands PASS and 1 fails, the skill still has a bug. Fix it.

## Marketplace grader (`evals.json` + `trigger_evals.json`)

`evals.json` here, `trigger_evals.json` in `skills/deckify/evals/` (it ships with the skill — the marketplace platform reads it from there at submission time).

`evals.json` is *also* used by Anthropic's marketplace grader at submission time, but it lives in `tools/phase-a/` because the cases inside it (`file_contains` / `regex_in_file` / `transcript_contains` over the 5-brand panel) are written from a Phase A perspective — they encode "the optimization loop converged on these states", which is dev-internal knowledge. If a future grader version becomes user-facing, a Phase B-style `evals.json` may need to ship under `skills/deckify/evals/` too.

**Host portability note**: one assertion in `evals.json` (`process_called_ask_user_question`) checks the transcript for the literal string `AskUserQuestion`, which is Claude Code specific. When other grader hosts (Codex / OpenClaw) ship their own grader, this assertion should be replaced with a host-neutral signal (e.g. `file_contains` on `decisions.json` proving Phase 2 happened with a structured mechanism). The runtime path itself (the skill scripts + SKILL.md prose + Phase B evals) is already host-neutral; only this one Phase A grader assertion isn't.
