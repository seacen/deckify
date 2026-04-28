# skills/deckify/evals — runtime quality gate (Phase B)

This directory holds the runtime evaluation that ships with the deckify skill. It runs as a mandatory gate inside `SKILL.md` Phase 4–5 every time a user produces a brand DS + verification deck.

> **Phase A vs Phase B** — this directory is **Phase B only**: the per-user runtime gate. The Phase A development loop (5-brand panel, skill-source tuning, structural audit) lives at `tools/phase-a/` at the repo root and is not part of the shipped skill. See [TESTING.md](../../../TESTING.md) for the full picture.

## Files

| File | Role |
|---|---|
| `hard_checks.py` | 10 deterministic DOM / regex checks. Cross-platform Python (no shell). |
| `rubric.json` | 6 visual-judge dimensions + 5 disqualifier definitions. The LLM scores against this. |
| `build_report.py` | Rolls hard checks + judge.json into a per-brand scoreboard. |
| `trigger_evals.json` | Marketplace-grader routing samples (Anthropic skill-eval format). |
| `README.md` | This file. |

## How Phase B uses these

```
   User runs deckify on their URL
         │
         ▼
   Phase 4 produces decks/<brand>/<brand>-deck.html + <brand>-PPT-Design-System.md
         │
         ▼
   hard_checks.py <deck.html> <ds.md> <out_dir>     ← 10 deterministic checks
         │
         ▼
   LLM reads out_dir/slides/*.png + DS markdown,
   scores judge.json against rubric.json            ← 6 visual dimensions
         │
         ▼
   build_report.py <out_dir> 4.0 "<brand>|<url>|<deck>|<ds>"   ← aggregate
         │
         ▼
   PASS = hard 10/10 (or 9/10 with cjk_font_quality soft) AND judge avg ≥ 4.0 AND no disqualifier
```

## Running it manually

```bash
# Step 1: deterministic hard checks
python3 skills/deckify/evals/hard_checks.py \
  decks/<brand>/<brand>-deck.html \
  decks/<brand>/<brand>-PPT-Design-System.md \
  tests/reports/runs/<ts>/per-sample/<brand>/

# Step 2: write judge.json (LLM, see SKILL.md Phase 5 for schema)

# Step 3: aggregate
python3 skills/deckify/evals/build_report.py \
  tests/reports/runs/<ts>/ 4.0 \
  "<brand>|<url>|decks/<brand>/<brand>-deck.html|decks/<brand>/<brand>-PPT-Design-System.md"
```

## When a check fails

Fix the **brand DS** (`decks/<brand>/<brand>-PPT-Design-System.md`), regenerate the deck from the updated DS, re-run. The fail-mapping table in [`references/verification-deck-spec.md`](../references/verification-deck-spec.md) §8 tells you which DS section owns each check.

**Do not edit the deck alone to make a check pass** — the deck is the test, the DS is the spec; only the spec deserves the fix. See [TESTING.md](../../../TESTING.md) for the full Phase A vs Phase B fix-routing model.
