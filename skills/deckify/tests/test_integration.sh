#!/usr/bin/env bash
# test_integration.sh — Phase 1 pipeline against 3 live brand sites.
#
# Hits real endpoints, catches "real data has malformed event lines" bugs that
# fixtures miss. Run after touching fetch_sitemap.py / fetch_pages.py /
# enumerate_assets.py / embed_logo.py.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

BRANDS=(
  "stripe https://stripe.com"
  "apple  https://www.apple.com"
  "github https://github.com"
)

pass=0
fail=0

for entry in "${BRANDS[@]}"; do
  read -r name url <<< "$entry"
  WS=$(python3 "$SKILL_DIR/scripts/init_workspace.py" "integ-$name")

  echo
  echo "──────────────────────────────────────────"
  echo " integration: $name → $url"
  echo " ws: $WS"
  echo "──────────────────────────────────────────"

  if ! python3 "$SKILL_DIR/scripts/fetch_sitemap.py" "$url" "$WS" 2>&1 | tail -3; then
    echo "  FAIL: fetch_sitemap.py exited non-zero"
    fail=$((fail+1))
    continue
  fi

  echo "$url" > "$WS/pages.txt"
  if ! python3 "$SKILL_DIR/scripts/fetch_pages.py" "$WS/pages.txt" "$WS" 2>&1 | tail -3; then
    echo "  FAIL: fetch_pages.py exited non-zero"
    fail=$((fail+1))
    continue
  fi

  if ! python3 "$SKILL_DIR/scripts/enumerate_assets.py" "$WS" 2>&1 | tail -5; then
    echo "  FAIL: enumerate_assets.py exited non-zero"
    fail=$((fail+1))
    continue
  fi

  RAW="$WS/raw-assets.json"
  if [[ ! -f "$RAW" ]]; then
    echo "  FAIL: raw-assets.json missing"
    fail=$((fail+1))
    continue
  fi

  LC=$(python3 -c "import json; print(len(json.load(open('$RAW')).get('logo_candidates', [])))")
  CC=$(python3 -c "import json; print(len(json.load(open('$RAW')).get('color_frequency', [])))")
  FC=$(python3 -c "import json; print(len(json.load(open('$RAW')).get('fonts', {}).get('frequencies', [])))")
  echo "  logo candidates:  $LC"
  echo "  unique colours:   $CC"
  echo "  font families:    $FC"

  # Pass: ≥1 logo candidate, ≥5 colours, ≥1 font
  if [[ "$LC" -ge 1 && "$CC" -ge 5 && "$FC" -ge 1 ]]; then
    echo "  PASS ✓"
    pass=$((pass+1))
  else
    echo "  FAIL: thresholds not met (need logo≥1, colours≥5, fonts≥1)"
    fail=$((fail+1))
  fi
done

echo
echo "═══════════════════════════════════════════"
echo " integration result: $pass passed, $fail failed (of ${#BRANDS[@]})"
echo "═══════════════════════════════════════════"
[[ "$fail" == "0" ]] && exit 0 || exit 1
