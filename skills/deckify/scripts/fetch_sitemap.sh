#!/usr/bin/env bash
# fetch_sitemap.sh — Phase 1a: pull just enough to let the agent decide which
# subpages to fetch next.
#
# Outputs to $WS/recon/:
#   - home.html            full DOM of the home page (post-hydration)
#   - home.png             desktop screenshot
#   - sitemap.xml          robots-discovered sitemap (best-effort)
#   - sitemap-urls.txt     flat URL list extracted from sitemap (best-effort)
#   - nav-links.json       all <a> in <header>/<nav>/<footer> with text + href
#                          (the agent uses this to pick high-value subpages)
#
# This script is deterministic. The agent's job (next step) is to read
# home.html / sitemap-urls.txt / nav-links.json and decide which 5-8 URLs
# to actually fetch in step 1b.
#
# Usage: fetch_sitemap.sh <url> <workspace_dir>

set -euo pipefail

URL="${1:?usage: fetch_sitemap.sh <url> <workspace_dir>}"
WS_INPUT="${2:?usage: fetch_sitemap.sh <url> <workspace_dir>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$WS_INPUT/recon"
WS="$(cd "$WS_INPUT" && pwd)"
RECON="$WS/recon"

if ! command -v agent-browser >/dev/null 2>&1; then
  echo "agent-browser not on PATH — running setup helper..." >&2
  bash "$SCRIPT_DIR/setup.sh" || true
  exit 127
fi

echo "URL:     $URL"
echo "WS:      $WS"
echo

# ── 1. Home page DOM + screenshot ─────────────────────────────────────────
echo "[1/4] navigate + dump home"
agent-browser set viewport 1440 900 >/dev/null
agent-browser open "$URL" >/dev/null
sleep 1.5
agent-browser eval 'document.documentElement.outerHTML' > "$RECON/home.html.raw"
python3 - "$RECON/home.html.raw" "$RECON/home.html" <<'PYEOF'
import sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").strip()
if raw.startswith('"') and raw.endswith('"'):
    raw = raw[1:-1].encode('utf-8').decode('unicode_escape')
pathlib.Path(sys.argv[2]).write_text(raw, encoding="utf-8")
PYEOF
rm -f "$RECON/home.html.raw"

agent-browser screenshot "$RECON/home.png" >/dev/null
echo "    → $RECON/home.html  $RECON/home.png"

# ── 2. Nav / header / footer link extraction ──────────────────────────────
echo "[2/4] extract nav-links.json"
agent-browser eval "$(cat <<'JSEOF'
(() => {
  const out = { home: location.href, host: location.hostname, links: [] };
  const seen = new Set();
  const collect = (root, region) => {
    if (!root) return;
    for (const a of root.querySelectorAll('a[href]')) {
      const href = a.href;
      if (!href || seen.has(href)) continue;
      // only same-host links, skip anchors & mailto
      try {
        const u = new URL(href);
        if (u.host !== location.hostname) continue;
        if (u.pathname === location.pathname && u.hash) continue;
      } catch { continue; }
      seen.add(href);
      out.links.push({
        region,
        href,
        text: (a.textContent || '').trim().slice(0, 120),
        aria: a.getAttribute('aria-label') || ''
      });
    }
  };
  collect(document.querySelector('header'), 'header');
  collect(document.querySelector('nav'),    'nav');
  collect(document.querySelector('footer'), 'footer');
  // Some sites put the menu in a custom element / role=navigation
  document.querySelectorAll('[role=navigation]').forEach(el => collect(el, 'role-nav'));
  return JSON.stringify(out);
})()
JSEOF
)" > "$RECON/nav-links.raw"
python3 - "$RECON/nav-links.raw" "$RECON/nav-links.json" <<'PYEOF'
import json, sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").strip()
if raw.startswith('"') and raw.endswith('"'):
    raw = raw[1:-1].encode('utf-8').decode('unicode_escape')
i = raw.find('{')
if i > 0: raw = raw[i:]
try:
    data = json.loads(raw)
    pathlib.Path(sys.argv[2]).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"    → {len(data.get('links', []))} nav links")
except Exception as e:
    sys.stderr.write(f"warn: nav-links parse failed: {e}\n")
    pathlib.Path(sys.argv[2]).write_text("{}")
PYEOF
rm -f "$RECON/nav-links.raw"

# ── 3. Sitemap (best-effort) ──────────────────────────────────────────────
echo "[3/4] sitemap"
SITEMAP_URLS=()
# Try common sitemap locations
ROOT=$(python3 -c "from urllib.parse import urlparse; u=urlparse('$URL'); print(f'{u.scheme}://{u.netloc}')")
for path in /sitemap.xml /sitemap_index.xml /sitemap-index.xml; do
  if curl -sfL --max-time 8 -A "Mozilla/5.0" "${ROOT}${path}" -o "$RECON/sitemap.xml.try"; then
    if [[ -s "$RECON/sitemap.xml.try" ]] && head -c 200 "$RECON/sitemap.xml.try" | grep -qi "<urlset\|<sitemapindex"; then
      mv "$RECON/sitemap.xml.try" "$RECON/sitemap.xml"
      echo "    found ${ROOT}${path}"
      break
    fi
    rm -f "$RECON/sitemap.xml.try"
  fi
done

if [[ -f "$RECON/sitemap.xml" ]]; then
  python3 - "$RECON/sitemap.xml" "$RECON/sitemap-urls.txt" <<'PYEOF'
import re, sys, pathlib
xml = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
urls = re.findall(r'<loc>\s*([^<]+?)\s*</loc>', xml)
# Dedup, keep order, cap to a reasonable size for LLM consumption
seen = set(); out = []
for u in urls:
    if u not in seen:
        seen.add(u); out.append(u)
        if len(out) >= 500: break
pathlib.Path(sys.argv[2]).write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"    → {len(out)} URLs in sitemap-urls.txt")
PYEOF
else
  echo "    no sitemap found (not fatal — agent can rely on nav-links.json)"
  : > "$RECON/sitemap-urls.txt"
fi

# ── 4. JSON-LD payloads (often contain official logo URL + brand metadata) ──
echo "[4/4] extract JSON-LD"
agent-browser eval "$(cat <<'JSEOF'
(() => {
  const blocks = [];
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try { blocks.push(JSON.parse(s.textContent || 'null')); }
    catch { blocks.push({ __raw: (s.textContent || '').slice(0, 2000) }); }
  });
  return JSON.stringify(blocks);
})()
JSEOF
)" > "$RECON/jsonld.raw"
python3 - "$RECON/jsonld.raw" "$RECON/jsonld.json" <<'PYEOF'
import json, sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").strip()
if raw.startswith('"') and raw.endswith('"'):
    raw = raw[1:-1].encode('utf-8').decode('unicode_escape')
i = raw.find('[')
if i > 0: raw = raw[i:]
try:
    data = json.loads(raw)
    pathlib.Path(sys.argv[2]).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"    → {len(data)} JSON-LD blocks")
except Exception as e:
    pathlib.Path(sys.argv[2]).write_text("[]")
    print(f"    warn: JSON-LD parse failed ({e})")
PYEOF
rm -f "$RECON/jsonld.raw"

echo
echo "fetch_sitemap.sh: done. Files in $RECON:"
ls -la "$RECON" | grep -v '^total'
echo
echo "Next step: the agent reads home.html / nav-links.json / sitemap-urls.txt /"
echo "jsonld.json and writes pages.txt — the URL list to fetch in step 1b."
