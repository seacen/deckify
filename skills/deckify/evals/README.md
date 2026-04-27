# skills/deckify/evals — quality contract

This directory holds **two layers of quality gates** that work together. They live in the same folder so there's one source of truth, but they have different audiences, different runtimes, and they correspond to **two phases of the skill's lifecycle**.

## Two phases, two audiences

| | Phase A — skill is being tuned (project devs) | Phase B — skill has shipped (end users) |
|---|---|---|
| **Who's running** | Project authors (us) + Anthropic marketplace harness | End user with the skill installed |
| **What's the test verifying** | The skill's *source* produces good artifacts across multiple brands | The brand DS produced for a specific user produces a good deck |
| **What gets fixed on failure** | Skill source files (`SKILL.md`, `ds-template.md`, prompts, scripts) | The user's `<brand>-PPT-Design-System.md` |
| **Which files in this directory** | `evals.json`, `trigger_evals.json` | `hard_checks.py`, `rubric.json`, `build_report.py`, `run.sh` |

In neither phase is the deck the fix target. The deck is the *test of the spec*; the spec is what tunes.

## Layer 1 — Skill-quality eval (Phase A)

**Files**: `evals.json`, `trigger_evals.json`

**Audience**: Anthropic's skill-eval grader / marketplace harness, plus us during local skill development.

**What it tests**: Given a user prompt, does the skill produce the right artifacts? Does the skill fire on the right queries (and stay silent on the wrong ones)?

- `evals.json` — 4 cases, each with a prompt and a list of declarative assertions (`file_exists`, `file_contains`, `regex_in_file`, `transcript_contains`). Verifies DS markdown structure + verification-deck HTML structure + transcript signals (the skill called the right scripts, asked the right questions).
- `trigger_evals.json` — 22 routing samples (12 should-trigger / 10 should-not). Tests whether the skill description fires on real-shaped queries.

**When it runs**: At marketplace submission, on every version bump, and locally when we want to verify the skill itself didn't regress. **Failures here drive fixes to skill source files** — not to any brand DS.

## Layer 2 — Runtime auto-eval (Phase B)

**Files**: `hard_checks.py`, `rubric.json`, `build_report.py`, `run.sh`

**Audience**: The skill running on a user's machine, on the user's brand. Phase 4-5 of `SKILL.md` invokes this as a mandatory gate.

**What it tests**: Given a generated `<brand>-deck.html` + `<brand>-PPT-Design-System.md`, does the deck actually render correctly in a real browser at 1280×720 and at 375 px? Does it pass the 8 hard DOM checks and clear the 5-dimension visual judge with avg ≥ 4?

- `hard_checks.py` — 8 deterministic checks via `agent-browser`: slide dimensions, fit contract, token-only colors, no emoji, mobile collapse, logo renders, text-layout safety, DS engineering DNA preserved.
- `rubric.json` — 5 visual-judge dimensions (logo branding, slide quality, brand fidelity, content substance, DS engineering DNA presence) + 5 disqualifiers.
- `build_report.py` — aggregates hard-check + LLM-judge scores into a per-brand pass/fail.
- `run.sh` — orchestrator. Iterates over the registered brand samples, lands per-sample reports under `skills/deckify/tests/reports/runs/<ts>/`, prints next-step instructions for the LLM-judge phase.

**When it runs**: On every Phase 4 of the skill, on every brand. **Failures here drive fixes to *the user's* brand DS markdown** — see the fail-mapping table in `references/verification-deck-spec.md` §8.

## How the two layers relate

```
        ┌──────────────────────────────────────────────────────┐
        │ Phase A — marketplace grader runs evals.json +       │
        │ trigger_evals.json                                   │
        │ (declarative file/regex assertions)                  │
        │ Failures → fix the SKILL source                      │
        └──────────────────────────────────────────────────────┘
                              ↓ verifies
        ┌──────────────────────────────────────────────────────┐
        │ Skill produces deck.html + DS.md correctly           │
        │ (because Phase 4 mandates run.sh + hard_checks.py)   │
        └──────────────────────────────────────────────────────┘
                              ↑ powered by
        ┌──────────────────────────────────────────────────────┐
        │ Phase B — runtime auto-eval (hard_checks + rubric +  │
        │ judge) runs every time the skill executes            │
        │ Failures → fix the user's BRAND DS                   │
        └──────────────────────────────────────────────────────┘
```

## Running locally

```bash
# Runtime auto-eval — what the skill calls during Phase 4
bash skills/deckify/evals/run.sh

# Then read screenshots + write per-sample/<brand>/judge.json (LLM step),
# then re-run build_report.py to fold judge scores into the scoreboard.
```

The Phase A evals (`evals.json`, `trigger_evals.json`) are not invoked locally — they run in Anthropic's harness or in CI.
