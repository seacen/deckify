#!/usr/bin/env bash
# smoke_unilever.sh — full Phase-1 smoke test against unilever.com.
#
# Per Skillify step 9: the full pipeline, end-to-end. Catches the case where
# every individual layer is correct but the pieces don't connect.
#
# Usage: smoke_unilever.sh [workspace_dir]
# Default workspace: /tmp/web-to-ds-smoke/<unix-ts>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

WS_BASE="${1:-/tmp/web-to-ds-smoke}"
WS="$WS_BASE/$(date +%s)"
mkdir -p "$WS"

URL="https://www.unilever.com"

echo "=========================================================="
echo " smoke test: $URL"
echo " workspace:  $WS"
echo "=========================================================="

echo
echo "[1/4] setup check"
bash "$SKILL_DIR/scripts/setup.sh" >/dev/null

echo
echo "[2/4] fetch_site (agent-browser)"
bash "$SKILL_DIR/scripts/fetch_site.sh" "$URL" "$WS"

echo
echo "[3/4] extract_brand (Python deterministic parse)"
python3 "$SKILL_DIR/scripts/extract_brand.py" "$WS"

echo
echo "[4/4] download_logo"
bash "$SKILL_DIR/scripts/download_logo.sh" "$WS" || {
  echo "WARNING: logo download failed — would prompt user in real run"
}

echo
echo "─── assertions ──────────────────────────────────────────"

RECON_JSON="$WS/brand-recon.json"
if [[ ! -f "$RECON_JSON" ]]; then
  echo "FAIL: $RECON_JSON not produced"
  exit 1
fi

# At least 3 brand candidates
BRAND_COUNT=$(python3 -c "import json; d=json.load(open('$RECON_JSON')); print(len(d['colors']['brand_candidates']))")
echo "  brand candidates: $BRAND_COUNT"
if [[ "$BRAND_COUNT" -lt 3 ]]; then
  echo "FAIL: expected ≥3 brand color candidates, got $BRAND_COUNT"
  exit 1
fi

# At least 1 font detected — count BOTH the HTML-parsed list AND the computed_signal.primary_fonts
# (latter comes from agent-browser's eval probe and is more reliable on JS-heavy sites)
FONT_COUNT=$(python3 -c "
import json
d = json.load(open('$RECON_JSON'))
html_fonts = len(d.get('fonts') or [])
cs = d.get('computed_signal') or {}
computed_fonts = len(cs.get('primary_fonts') or [])
print(max(html_fonts, computed_fonts))
")
echo "  font families:    $FONT_COUNT (HTML+computed combined)"
if [[ "$FONT_COUNT" -lt 1 ]]; then
  echo "FAIL: expected ≥1 font family, got $FONT_COUNT"
  exit 1
fi

# Logo path was set (logo file exists or warning was surfaced)
LOGO_PATH=$(python3 -c "import json; d=json.load(open('$RECON_JSON')); print(d.get('logo_local_path') or '')")
if [[ -n "$LOGO_PATH" && -f "$LOGO_PATH" ]]; then
  echo "  logo:             $LOGO_PATH ($(wc -c < "$LOGO_PATH") bytes)"
else
  echo "  logo:             (none — would prompt user)"
fi

# Computed signal exists
HAS_COMPUTED=$(python3 -c "import json; d=json.load(open('$RECON_JSON')); print('yes' if d.get('computed_signal') else 'no')")
echo "  computed signal:  $HAS_COMPUTED"

echo
echo "OK — Phase 1 smoke passed."
echo "Artifacts in: $WS"
