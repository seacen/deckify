#!/usr/bin/env python3
"""fetch_sitemap.py — Phase 1a: pull just enough to let the agent decide which
subpages to fetch next. Cross-platform replacement for fetch_sitemap.sh.

Outputs to <ws>/recon/:
  - home.html           full DOM of the home page (post-hydration)
  - home.png            desktop screenshot
  - sitemap.xml         robots-discovered sitemap (best-effort)
  - sitemap-urls.txt    flat URL list extracted from sitemap (best-effort)
  - nav-links.json      every <a> in <header>/<nav>/<footer>/[role=navigation]
  - jsonld.json         JSON-LD blocks (often carries official logo URL + org meta)

Usage: python3 fetch_sitemap.py <url> <workspace_dir>

Cross-platform notes:
  - Uses subprocess.run with explicit list args (no shell), so works on Windows
  - Uses urllib.request for sitemap (no curl dependency) — Windows ships urllib
  - All file paths via pathlib (handles \\ vs / automatically)
"""
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse

# Local import — sibling helper that wraps agent-browser invocations with the
# stealth flags every brand-CDN-blocked site needs. See _ab_common.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ab_common import agent_browser_cmd  # noqa: E402


JS_NAV_LINKS = r"""(() => {
  const out = { home: location.href, host: location.hostname, links: [] };
  const seen = new Set();
  const collect = (root, region) => {
    if (!root) return;
    for (const a of root.querySelectorAll('a[href]')) {
      const href = a.href;
      if (!href || seen.has(href)) continue;
      try {
        const u = new URL(href);
        if (u.host !== location.hostname) continue;
        if (u.pathname === location.pathname && u.hash) continue;
      } catch { continue; }
      seen.add(href);
      out.links.push({
        region, href,
        text: (a.textContent || '').trim().slice(0, 120),
        aria: a.getAttribute('aria-label') || ''
      });
    }
  };
  collect(document.querySelector('header'), 'header');
  collect(document.querySelector('nav'),    'nav');
  collect(document.querySelector('footer'), 'footer');
  document.querySelectorAll('[role=navigation]').forEach(el => collect(el, 'role-nav'));
  return JSON.stringify(out);
})()"""

JS_JSONLD = r"""(() => {
  const blocks = [];
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try { blocks.push(JSON.parse(s.textContent || 'null')); }
    catch { blocks.push({ __raw: (s.textContent || '').slice(0, 2000) }); }
  });
  return JSON.stringify(blocks);
})()"""


def run_ab(args: list[str], capture: bool = True, check: bool = False) -> subprocess.CompletedProcess:
    """Invoke agent-browser with explicit args (no shell)."""
    return subprocess.run(agent_browser_cmd(*args), capture_output=capture, text=True, check=check, timeout=180)


def parse_ab_eval(stdout: str) -> str:
    """agent-browser eval prints JSON wrapped in quotes; unwrap."""
    s = stdout.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1].encode("utf-8").decode("unicode_escape")
    return s


def fetch_url(url: str, *, timeout: int = 8) -> bytes | None:
    """Best-effort GET. Returns bytes on success, None on any error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; deckify)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError, OSError):
        return None


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: fetch_sitemap.py <url> <workspace_dir>", file=sys.stderr)
        return 2

    url, ws_input = sys.argv[1], sys.argv[2]
    ws = Path(ws_input).resolve()
    recon = ws / "recon"
    recon.mkdir(parents=True, exist_ok=True)

    if shutil.which("agent-browser") is None:
        print("agent-browser not on PATH — install via npm/brew/cargo (see scripts/setup.py)", file=sys.stderr)
        return 127

    print(f"URL:     {url}")
    print(f"WS:      {ws}\n")

    # ── 1. Home page DOM + screenshot ─────────────────────────────────────
    print("[1/4] navigate + dump home")
    run_ab(["set", "viewport", "1440", "900"])
    run_ab(["open", url])
    time.sleep(1.5)

    res = run_ab(["eval", "document.documentElement.outerHTML"])
    (recon / "home.html").write_text(parse_ab_eval(res.stdout), encoding="utf-8")

    run_ab(["screenshot", str(recon / "home.png")])
    print(f"    → {recon / 'home.html'}  {recon / 'home.png'}")

    # ── 2. Nav / header / footer link extraction ──────────────────────────
    print("[2/4] extract nav-links.json")
    res = run_ab(["eval", JS_NAV_LINKS])
    raw = parse_ab_eval(res.stdout)
    i = raw.find("{")
    if i > 0:
        raw = raw[i:]
    try:
        data = json.loads(raw)
        (recon / "nav-links.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"    → {len(data.get('links', []))} nav links")
    except json.JSONDecodeError as e:
        sys.stderr.write(f"warn: nav-links parse failed: {e}\n")
        (recon / "nav-links.json").write_text("{}")

    # ── 3. Sitemap (best-effort) ──────────────────────────────────────────
    print("[3/4] sitemap")
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    sitemap_xml: bytes | None = None
    for path in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"):
        body = fetch_url(root + path)
        if body and (b"<urlset" in body[:200] or b"<sitemapindex" in body[:200]):
            sitemap_xml = body
            print(f"    found {root}{path}")
            break

    if sitemap_xml:
        (recon / "sitemap.xml").write_bytes(sitemap_xml)
        text = sitemap_xml.decode("utf-8", errors="replace")
        urls = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text)
        seen = set()
        out = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                out.append(u)
                if len(out) >= 500:
                    break
        (recon / "sitemap-urls.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"    → {len(out)} URLs in sitemap-urls.txt")
    else:
        print("    no sitemap found (not fatal — agent can rely on nav-links.json)")
        (recon / "sitemap-urls.txt").write_text("", encoding="utf-8")

    # ── 4. JSON-LD payloads ───────────────────────────────────────────────
    print("[4/4] extract JSON-LD")
    res = run_ab(["eval", JS_JSONLD])
    raw = parse_ab_eval(res.stdout)
    i = raw.find("[")
    if i > 0:
        raw = raw[i:]
    try:
        data = json.loads(raw)
        (recon / "jsonld.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"    → {len(data)} JSON-LD blocks")
    except json.JSONDecodeError as e:
        (recon / "jsonld.json").write_text("[]")
        print(f"    warn: JSON-LD parse failed ({e})")

    print(f"\nfetch_sitemap.py: done. Files in {recon}:")
    for p in sorted(recon.iterdir()):
        print(f"  {p.name}")
    print("\nNext step: the agent reads home.html / nav-links.json / sitemap-urls.txt /"
          "\njsonld.json and writes pages.txt — the URL list to fetch in step 1b.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
