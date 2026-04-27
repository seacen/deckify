#!/usr/bin/env bash
# fetch_pages.sh — Phase 1b: batch-fetch the agent's chosen URL list.
#
# Reads pages.txt (one URL per line, # comments allowed). For each URL:
#   - desktop screenshot
#   - full DOM dump
#   - per-page computed CSS probe (root vars, computed styles, all inline SVG,
#     all <img> + background-image url(), @font-face + preload font URLs)
#
# Outputs to $WS/recon/pages/<slug>/
#   - dom.html
#   - shot.png
#   - probe.json
#
# Per-page slug = sanitized path; e.g. /about/leadership → about-leadership.
# index = home.
#
# Usage: fetch_pages.sh <pages.txt> <workspace_dir>

set -uo pipefail

PAGES_FILE="${1:?usage: fetch_pages.sh <pages.txt> <workspace_dir>}"
WS_INPUT="${2:?usage: fetch_pages.sh <pages.txt> <workspace_dir>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$WS_INPUT/recon/pages"
WS="$(cd "$WS_INPUT" && pwd)"
PAGES_DIR="$WS/recon/pages"

if ! command -v agent-browser >/dev/null 2>&1; then
  echo "agent-browser not on PATH" >&2
  exit 127
fi

# Per-page JS probe — exhaustive enumeration, no judgment
read -r -d '' PROBE_JS <<'JSEOF' || true
(() => {
  const out = {
    url: location.href, host: location.hostname, title: document.title || '',
    rootVars: {}, computed: {}, allInlineSvg: [], allImg: [],
    bgImageUrls: [], fontFaceSrcs: [], preloadFontUrls: [], jsonLd: [],
    iconLinks: [], headerSvg: [], footerSvg: []
  };

  // 1. :root vars across stylesheets
  for (const sheet of Array.from(document.styleSheets)) {
    let rules; try { rules = sheet.cssRules; } catch { continue; }
    for (const r of Array.from(rules || [])) {
      if (!r.style || !r.selectorText) continue;
      if (/(^|,\s*)(:root|html)(\s*,|\s*$)/.test(r.selectorText)) {
        for (const p of Array.from(r.style)) {
          if (p.startsWith('--')) out.rootVars[p] = r.style.getPropertyValue(p).trim();
        }
      }
      // Capture @font-face src URLs
      try {
        if (r.style && r.cssText && r.cssText.toLowerCase().startsWith('@font-face')) {
          const src = r.style.getPropertyValue('src');
          if (src) out.fontFaceSrcs.push({ family: r.style.getPropertyValue('font-family'), src });
        }
      } catch {}
    }
  }

  // 2. Computed of a wider set of selectors than before — let LLM see real palette
  const SURFACES = ['body', 'header', 'nav', 'footer', 'main', 'h1', 'h2', 'h3',
    '.hero', '.cta', '.btn-primary', '.button-primary', 'button',
    '.bg-primary', '.section-dark', '[class*="hero" i]', '[class*="cta" i]',
    'a', 'a.btn'];
  for (const sel of SURFACES) {
    try {
      const el = document.querySelector(sel);
      if (!el) continue;
      const cs = getComputedStyle(el);
      out.computed[sel] = {
        bg: cs.backgroundColor, color: cs.color, font: cs.fontFamily,
        size: cs.fontSize, weight: cs.fontWeight,
        radius: cs.borderRadius, shadow: cs.boxShadow,
        padX: cs.paddingLeft, padY: cs.paddingTop
      };
    } catch {}
  }

  // 3. ALL inline SVGs anywhere (header/footer/etc) — note location, dimensions, content size
  const allSvg = Array.from(document.querySelectorAll('svg'));
  for (let i = 0; i < allSvg.length && i < 80; i++) {
    const svg = allSvg[i];
    const r = svg.getBoundingClientRect();
    let region = 'body';
    if (svg.closest('header')) region = 'header';
    else if (svg.closest('footer')) region = 'footer';
    else if (svg.closest('nav')) region = 'nav';
    else if (svg.closest('[class*="logo" i]')) region = 'logo-class';
    out.allInlineSvg.push({
      idx: i, region,
      width: Math.round(r.width), height: Math.round(r.height),
      viewBox: svg.getAttribute('viewBox') || '',
      pathCount: svg.querySelectorAll('path').length,
      maxPathDLen: Math.max(0, ...Array.from(svg.querySelectorAll('path')).map(p => (p.getAttribute('d') || '').length)),
      hasText: !!svg.querySelector('text'),
      hasImage: !!svg.querySelector('image'),
      ariaLabel: svg.getAttribute('aria-label') || '',
      classNames: svg.className.baseVal || svg.getAttribute('class') || '',
      outerHTML: svg.outerHTML.length < 8000 ? svg.outerHTML : svg.outerHTML.slice(0, 8000) + '<!-- truncated -->'
    });
  }
  out.headerSvg = out.allInlineSvg.filter(s => s.region === 'header').map(s => s.idx);
  out.footerSvg = out.allInlineSvg.filter(s => s.region === 'footer').map(s => s.idx);

  // 4. ALL <img> with src + region
  const imgs = Array.from(document.querySelectorAll('img'));
  for (let i = 0; i < imgs.length && i < 100; i++) {
    const img = imgs[i];
    const r = img.getBoundingClientRect();
    let region = 'body';
    if (img.closest('header')) region = 'header';
    else if (img.closest('footer')) region = 'footer';
    else if (img.closest('nav')) region = 'nav';
    out.allImg.push({
      idx: i, region,
      src: img.currentSrc || img.src || '',
      alt: img.alt || '', width: Math.round(r.width), height: Math.round(r.height),
      classNames: img.className || ''
    });
  }

  // 5. background-image: url(...) sniffing on key elements
  const visited = new Set();
  document.querySelectorAll('header *, footer *, [class*="logo" i], [class*="hero" i], .bg, .background').forEach(el => {
    if (visited.has(el) || visited.size > 200) return;
    visited.add(el);
    const bg = getComputedStyle(el).backgroundImage;
    const m = bg && bg.match(/url\((['"]?)([^)'"]+)\1\)/);
    if (m) {
      out.bgImageUrls.push({
        url: m[2], el: el.tagName + (el.className ? '.' + String(el.className).slice(0, 60) : ''),
        region: el.closest('header') ? 'header' : el.closest('footer') ? 'footer' : 'body'
      });
    }
  });

  // 6. preload font URLs
  document.querySelectorAll('link[rel="preload"][as="font"], link[rel*="font"]').forEach(l => {
    const href = l.getAttribute('href');
    if (href) out.preloadFontUrls.push({ href, type: l.getAttribute('type') || '' });
  });

  // 7. JSON-LD on this page
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try { out.jsonLd.push(JSON.parse(s.textContent || 'null')); }
    catch { out.jsonLd.push({ __raw: (s.textContent || '').slice(0, 1500) }); }
  });

  // 8. icon links
  document.querySelectorAll('link[rel*="icon" i], link[rel="apple-touch-icon"], link[rel="image_src"]').forEach(l => {
    out.iconLinks.push({
      rel: l.getAttribute('rel') || '', href: l.getAttribute('href') || '',
      sizes: l.getAttribute('sizes') || '', type: l.getAttribute('type') || ''
    });
  });

  return JSON.stringify(out);
})()
JSEOF

slugify() {
  local url="$1"
  python3 -c "
import sys, re, urllib.parse as u
parsed = u.urlparse(sys.argv[1])
path = parsed.path.strip('/')
slug = re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-') or 'index'
print(slug[:60])
" "$url"
}

i=0
while IFS= read -r raw_url || [[ -n "$raw_url" ]]; do
  url=$(echo "$raw_url" | sed 's/#.*$//' | xargs)
  [[ -z "$url" ]] && continue
  i=$((i+1))
  slug=$(slugify "$url")
  page_dir="$PAGES_DIR/$slug"
  mkdir -p "$page_dir"

  echo
  echo "[$i] $url"
  echo "    slug: $slug → $page_dir"

  agent-browser set viewport 1440 900 >/dev/null
  if ! agent-browser open "$url" >/dev/null 2>&1; then
    echo "    ✗ navigate failed; skipping"
    echo '{"error":"navigate failed"}' > "$page_dir/probe.json"
    continue
  fi
  sleep 1.5

  # DOM
  agent-browser eval 'document.documentElement.outerHTML' > "$page_dir/dom.raw"
  python3 - "$page_dir/dom.raw" "$page_dir/dom.html" <<'PYEOF'
import sys, pathlib
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").strip()
if raw.startswith('"') and raw.endswith('"'):
    raw = raw[1:-1].encode('utf-8').decode('unicode_escape')
pathlib.Path(sys.argv[2]).write_text(raw, encoding="utf-8")
PYEOF
  rm -f "$page_dir/dom.raw"

  # Screenshot
  agent-browser screenshot "$page_dir/shot.png" >/dev/null 2>&1 || true

  # Probe
  agent-browser eval "$PROBE_JS" > "$page_dir/probe.raw" 2>/dev/null || true
  python3 - "$page_dir/probe.raw" "$page_dir/probe.json" <<'PYEOF'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1])
raw = p.read_text(encoding="utf-8", errors="replace").strip() if p.exists() else ""
if raw.startswith('"') and raw.endswith('"'):
    raw = raw[1:-1].encode('utf-8').decode('unicode_escape')
i = raw.find('{')
if i > 0: raw = raw[i:]
try:
    pathlib.Path(sys.argv[2]).write_text(json.dumps(json.loads(raw), indent=2, ensure_ascii=False))
except Exception as e:
    pathlib.Path(sys.argv[2]).write_text(json.dumps({"error": str(e), "raw_preview": raw[:500]}, indent=2))
PYEOF
  rm -f "$page_dir/probe.raw"

  # Quick stats
  python3 -c "
import json, pathlib
p = json.loads(pathlib.Path('$page_dir/probe.json').read_text())
n_svg = len(p.get('allInlineSvg', []))
n_img = len(p.get('allImg', []))
n_jsonld = len(p.get('jsonLd', []))
print(f'    {n_svg} inline SVGs, {n_img} <img>, {n_jsonld} JSON-LD blocks')
" 2>/dev/null || true
done < "$PAGES_FILE"

echo
echo "fetch_pages.sh: done — $i pages saved to $PAGES_DIR"
