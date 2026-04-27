#!/usr/bin/env bash
# run.sh — auto-eval orchestrator.
#
# Two layers:
#   1. Hard checks (deterministic, hard_checks.py): DOM measurements + regex/file checks
#   2. Aggregate (build_report.py): scoreboard + per-sample reports + repair_actions
#
# Vision-judge is NOT a Python step — it's done by the agent that runs this skill.
# After this script finishes, the agent reads each per-sample/<brand>/slides/*.png
# according to eval/rubric.json and writes per-sample/<brand>/judge.json directly.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TS="$(date +%Y-%m-%dT%H-%M-%S)"
OUT_DIR="$SKILL_DIR/tests/reports/runs/$TS"
mkdir -p "$OUT_DIR/per-sample"

# Sample registry — format: brand|source_url|deck_html|ds_md
# Resolve repo root (deckify/) so paths work regardless of cwd
DECKIFY_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
SAMPLES=(
  "unilever|https://www.unilever.com|$DECKIFY_ROOT/decks/unilever/unilever-deck.html|$DECKIFY_ROOT/decks/unilever/unilever-PPT-Design-System.md"
  "pg|https://www.pg.com|$DECKIFY_ROOT/decks/pg/pg-deck.html|$DECKIFY_ROOT/decks/pg/pg-PPT-Design-System.md"
  "stripe|https://stripe.com|$DECKIFY_ROOT/decks/stripe/stripe-deck.html|$DECKIFY_ROOT/decks/stripe/stripe-PPT-Design-System.md"
)

PASS_THRESHOLD=4

for entry in "${SAMPLES[@]}"; do
  IFS='|' read -r brand url deck ds <<< "$entry"
  echo
  echo "═══════════════════════════════════════════════════════════"
  echo " sample: $brand   ($url)"
  echo "═══════════════════════════════════════════════════════════"

  sample_dir="$OUT_DIR/per-sample/$brand"
  mkdir -p "$sample_dir"

  python3 "$SCRIPT_DIR/hard_checks.py" "$deck" "$ds" "$sample_dir" 2>&1 | tail -10
done

# Aggregate (judge.json may still be missing — build_report tolerates that)
python3 "$SCRIPT_DIR/build_report.py" "$OUT_DIR" "$PASS_THRESHOLD" "${SAMPLES[@]}"
cp "$OUT_DIR/summary.md" "$SKILL_DIR/tests/reports/latest.md"

# Emit instructions for the agent (this skill's caller) to do the vision judge step.
cat <<EOF

═══════════════════════════════════════════════════════════
 NEXT STEP — vision judge (you, the agent)
═══════════════════════════════════════════════════════════

Hard checks are done. Vision judge is your job — no Python wrapper.

For each sample under: $OUT_DIR/per-sample/<brand>/
  1. Read the 3 screenshots in slides/  (cover + 2 representative content slides)
  2. Read the deck's DS markdown for context
  3. Score against the rubric in: $SKILL_DIR/eval/rubric.json (5 dimensions, 0-5 each)
  4. Write judge.json with this exact shape:

     {
       "ok": true,
       "judged_by": "<your model id>",
       "scores": {
         "scores": {
           "logo_present_and_branded":      <0-5>,
           "slide_visual_quality":          <0-5>,
           "brand_fidelity":                <0-5>,
           "content_substantive":           <0-5>,
           "engineering_dna_visible_in_ds": <0-5>
         },
         "reasoning": "<2-3 sentences explaining the lowest scores>",
         "regression_flags": ["<short flag>", ...]
       }
     }

  5. After all judge.json files are written, re-run build_report.py to
     fold judge scores into the scoreboard:

       python3 $SCRIPT_DIR/build_report.py $OUT_DIR $PASS_THRESHOLD \\
         "unilever|https://www.unilever.com|$DECKIFY_ROOT/decks/unilever/unilever-deck.html|$DECKIFY_ROOT/decks/unilever/unilever-PPT-Design-System.md" \\
         "pg|https://www.pg.com|$DECKIFY_ROOT/decks/pg/pg-deck.html|$DECKIFY_ROOT/decks/pg/pg-PPT-Design-System.md" \\
         "stripe|https://stripe.com|$DECKIFY_ROOT/decks/stripe/stripe-deck.html|$DECKIFY_ROOT/decks/stripe/stripe-PPT-Design-System.md"

Reports:
  $OUT_DIR/summary.md
  $SKILL_DIR/tests/reports/latest.md
═══════════════════════════════════════════════════════════
EOF
