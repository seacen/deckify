# skills/deckify/evals — runtime quality gate (Phase B)

This directory holds the runtime evaluation that ships with the deckify skill. It runs as a mandatory gate inside `SKILL.md` Phase 4–5 every time a user produces a brand DS + verification deck.

> **Phase A vs Phase B** — this directory is **Phase B only**: the per-user runtime gate. The Phase A development loop (5-brand panel, skill-source tuning, structural audit) lives at `tools/phase-a/` in the maintainer's repo and is not part of the shipped skill. See [TESTING.md](../../../TESTING.md) for the full picture.

## Files

| File | Role |
|---|---|
| `hard_checks.py` | 11 deterministic DOM / regex / governance checks. Cross-platform Python (no shell). |
| `rubric.json` | 6 visual-judge dimensions + 5 disqualifier definitions. The LLM scores against this. |
| `build_report.py` | Rolls hard checks + judge.json into a per-brand scoreboard. |
| `trigger_evals.json` | Marketplace-grader routing samples (Anthropic skill-eval format). |
| `README.md` | This file. |

## Where artefacts live

End-user runs land everything under `~/deckify/`:

```
~/deckify/decks/<brand>/<brand>-deck.html
~/deckify/decks/<brand>/<brand>-PPT-Design-System.md
~/deckify/decks/<brand>/source/{brand.json, decisions.json, pages.txt, assets/}
~/deckify/reports/runs/<ts>/per-sample/<brand>/{slides/, hard_checks.json, judge.json, .provenance.json}
```

This is independent of the cwd you run from. `scripts/persist_brand_source.py` always resolves to `~/deckify/`. Do not write user artefacts into the deckify source repo or anywhere else.

## How Phase B uses these

```
   User runs deckify on their URL
         │
         ▼
   Phase 4 produces ~/deckify/decks/<brand>/<brand>-deck.html
                   ~/deckify/decks/<brand>/<brand>-PPT-Design-System.md
         │
         ▼
   hard_checks.py <deck.html> <ds.md> <out_dir>     ← 11 deterministic checks
         │
         ▼
   LLM reads out_dir/slides/*.png + DS markdown,
   scores judge.json against rubric.json            ← 6 visual dimensions
         │
         ▼
   build_report.py <out_dir> 4.0 "<brand>|<url>|<deck>|<ds>"   ← aggregate
         │
         ▼
   PASS = hard 11/11 (or 10/11 with cjk_font_quality soft)
          AND judge avg ≥ 4.0
          AND no disqualifier
```

## Running it manually

```bash
TS=$(date +%Y-%m-%dT%H-%M-%S)
OUT="$HOME/deckify/reports/runs/$TS/per-sample/<brand>"
mkdir -p "$OUT"

# Step 1: deterministic hard checks
python3 <skill-path>/evals/hard_checks.py \
  "$HOME/deckify/decks/<brand>/<brand>-deck.html" \
  "$HOME/deckify/decks/<brand>/<brand>-PPT-Design-System.md" \
  "$OUT"

# Step 2: write judge.json (LLM, see SKILL.md Phase 5 for schema)

# Step 3: aggregate
python3 <skill-path>/evals/build_report.py \
  "$HOME/deckify/reports/runs/$TS/" 4.0 \
  "<brand>|<url>|$HOME/deckify/decks/<brand>/<brand>-deck.html|$HOME/deckify/decks/<brand>/<brand>-PPT-Design-System.md"
```

`<skill-path>` is wherever the deckify skill is installed — typically resolved by the host (Claude Code, Codex, etc) and not something the user types directly.

## When a check fails

Fix the **brand DS** at `~/deckify/decks/<brand>/<brand>-PPT-Design-System.md`, regenerate the deck from the updated DS, re-run. The fail-mapping table in [`references/verification-deck-spec.md`](../references/verification-deck-spec.md) §8 tells you which DS section owns each check.

**Do not edit the deck alone to make a check pass** — and starting now this is structurally enforced. The 11th hard check (`phase_b_workflow`) hashes deck + DS each run; on a re-run in the same `out_dir`, if the deck changed but the DS didn't, it FAILS as `deck_modified_without_ds_update`. The legitimate cycle (edit DS → regenerate deck → re-run) updates both SHAs and clears the gate.

See [TESTING.md](../../../TESTING.md) for the full Phase A vs Phase B fix-routing model.
