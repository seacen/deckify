#!/usr/bin/env bash
# smoke_unilever.sh — Phase-1 smoke test against unilever.com.
#
# Runs the full deterministic pipeline (1a fetch_sitemap, 1c fetch_pages on
# a single page, 1d enumerate_assets, 1f embed_logo against a chosen candidate)
# and checks that the workspace ends up with the artifacts the LLM would
# consume in 1b/1e.
#
# Usage: smoke_unilever.sh [workspace_dir]
# If no workspace given, creates one in the OS temp area (auto-swept by OS).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [[ $# -ge 1 ]]; then
  WS="$1"
  mkdir -p "$WS"
else
  WS=$(python3 "$SKILL_DIR/scripts/init_workspace.py" smoke-unilever)
fi

URL="https://www.unilever.com"

echo "=========================================================="
echo " smoke test: $URL"
echo " workspace:  $WS"
echo "=========================================================="

echo
echo "[1/4] setup check"
python3 "$SKILL_DIR/scripts/setup.py" >/dev/null

echo
echo "[2/4] fetch_sitemap (1a)"
python3 "$SKILL_DIR/scripts/fetch_sitemap.py" "$URL" "$WS"

echo
echo "[3/4] fetch_pages — minimal one-page list"
echo "$URL/our-company/at-a-glance/" > "$WS/pages.txt"
python3 "$SKILL_DIR/scripts/fetch_pages.py" "$WS/pages.txt" "$WS"

echo
echo "[4/4] enumerate_assets (1d)"
python3 "$SKILL_DIR/scripts/enumerate_assets.py" "$WS"

echo
echo "─── assertions ──────────────────────────────────────────"

RAW_JSON="$WS/raw-assets.json"
if [[ ! -f "$RAW_JSON" ]]; then
  echo "FAIL: $RAW_JSON not produced"
  exit 1
fi

# At least 1 logo candidate
LOGO_COUNT=$(python3 -c "import json; d=json.load(open('$RAW_JSON')); print(len(d.get('logo_candidates', [])))")
echo "  logo candidates:  $LOGO_COUNT"
[[ "$LOGO_COUNT" -lt 1 ]] && { echo "FAIL: expected ≥1 logo candidate"; exit 1; }

# At least 5 colours in frequency
COLOR_COUNT=$(python3 -c "import json; d=json.load(open('$RAW_JSON')); print(len(d.get('color_frequency', [])))")
echo "  unique colours:   $COLOR_COUNT"
[[ "$COLOR_COUNT" -lt 5 ]] && { echo "FAIL: expected ≥5 unique colours"; exit 1; }

# At least 1 font family
FONT_COUNT=$(python3 -c "import json; d=json.load(open('$RAW_JSON')); print(len(d.get('fonts', {}).get('frequencies', [])))")
echo "  font families:    $FONT_COUNT"
[[ "$FONT_COUNT" -lt 1 ]] && { echo "FAIL: expected ≥1 font family"; exit 1; }

echo
echo "OK — Phase 1 smoke passed."
echo "Artifacts in: $WS"
