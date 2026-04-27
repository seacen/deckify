#!/usr/bin/env bash
# test_integration.sh — Phase 1 pipeline against 3 live brand sites.
#
# Per Skillify step 4: hits real endpoints, catches "real data has malformed
# event lines" bugs that fixtures miss. Skip this if you're just changing
# script comments — only run after touching fetch_site.sh / extract_brand.py
# / download_logo.sh.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

BRANDS=(
  "stripe https://stripe.com"
  "apple  https://www.apple.com"
  "github https://github.com"
)

TMP_BASE="${TMPDIR:-/tmp}/web-to-ds-integ-$(date +%s)"
mkdir -p "$TMP_BASE"

pass=0
fail=0

for entry in "${BRANDS[@]}"; do
  read -r name url <<< "$entry"
  WS="$TMP_BASE/$name"
  echo
  echo "──────────────────────────────────────────"
  echo " integration: $name → $url"
  echo " ws: $WS"
  echo "──────────────────────────────────────────"

  if ! bash "$SKILL_DIR/scripts/fetch_site.sh" "$url" "$WS" 2>&1 | tail -5; then
    echo "  FAIL: fetch_site.sh exited non-zero"
    fail=$((fail+1))
    continue
  fi
  if ! python3 "$SKILL_DIR/scripts/extract_brand.py" "$WS" 2>&1 | tail -10; then
    echo "  FAIL: extract_brand.py exited non-zero"
    fail=$((fail+1))
    continue
  fi
  bash "$SKILL_DIR/scripts/download_logo.sh" "$WS" 2>&1 | tail -3 || true

  # Assertions
  RECON="$WS/brand-recon.json"
  if [[ ! -f "$RECON" ]]; then
    echo "  FAIL: brand-recon.json missing"
    fail=$((fail+1))
    continue
  fi
  BC=$(python3 -c "import json; print(len(json.load(open('$RECON'))['colors']['brand_candidates']))")
  NC=$(python3 -c "import json; print(len(json.load(open('$RECON'))['colors']['neutral_candidates']))")
  FC=$(python3 -c "import json; d=json.load(open('$RECON')); cs=d.get('computed_signal') or {}; print(max(len(d.get('fonts') or []), len(cs.get('primary_fonts') or [])))")
  LP=$(python3 -c "import json; d=json.load(open('$RECON')); print(d.get('logo_local_path') or '')")
  echo "  brand candidates: $BC"
  echo "  neutral candidates: $NC"
  echo "  fonts (combined): $FC"
  echo "  logo local path:  ${LP:-(none)}"

  # Pass: ≥2 brand candidates (monochrome brands like Apple/GitHub legitimately have few)
  #   AND total color signal ≥6 (brand + neutral)
  #   AND ≥1 font detected
  TC=$(( BC + NC ))
  if [[ "$BC" -ge 2 && "$TC" -ge 6 && "$FC" -ge 1 ]]; then
    echo "  PASS ✓"
    pass=$((pass+1))
  else
    echo "  FAIL: thresholds not met (need brand≥3, fonts≥1)"
    fail=$((fail+1))
  fi
done

echo
echo "═══════════════════════════════════════════"
echo " integration result: $pass passed, $fail failed (of ${#BRANDS[@]})"
echo " artifacts: $TMP_BASE"
echo "═══════════════════════════════════════════"
[[ "$fail" == "0" ]] && exit 0 || exit 1
