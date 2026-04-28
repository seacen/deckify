#!/usr/bin/env python3
"""fetch_pages.py — Phase 1c: batch-fetch the agent's chosen URL list.

Cross-platform replacement for fetch_pages.sh. Reads pages.txt
(one URL per line, # comments allowed). For each URL:
  - desktop screenshot
  - full DOM dump
  - per-page computed CSS probe (root vars, computed styles, inline SVG,
    <img>, background-image url(), @font-face + preload font URLs, JSON-LD,
    icon links)

Outputs to <ws>/recon/pages/<slug>/{dom.html, shot.png, probe.json}
(slug = sanitised path, e.g. /about/leadership → about-leadership;
index = home).

Self-healing: if 2+ consecutive navigations fail, kills any Chrome for
Testing process so agent-browser respawns on the next call. Cross-platform
implementation uses psutil if available, otherwise falls back to platform
commands (taskkill on Windows, pkill on Unix).

Usage: python3 fetch_pages.py <pages.txt> <workspace_dir>
"""
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ab_common import agent_browser_cmd  # noqa: E402


PROBE_JS = r"""(() => {
  const out = {
    url: location.href, host: location.hostname, title: document.title || '',
    rootVars: {}, computed: {}, allInlineSvg: [], allImg: [],
    bgImageUrls: [], fontFaceSrcs: [], preloadFontUrls: [], jsonLd: [],
    iconLinks: [], headerSvg: [], footerSvg: []
  };

  for (const sheet of Array.from(document.styleSheets)) {
    let rules; try { rules = sheet.cssRules; } catch { continue; }
    for (const r of Array.from(rules || [])) {
      if (!r.style || !r.selectorText) continue;
      if (/(^|,\s*)(:root|html)(\s*,|\s*$)/.test(r.selectorText)) {
        for (const p of Array.from(r.style)) {
          if (p.startsWith('--')) out.rootVars[p] = r.style.getPropertyValue(p).trim();
        }
      }
      try {
        if (r.style && r.cssText && r.cssText.toLowerCase().startsWith('@font-face')) {
          const src = r.style.getPropertyValue('src');
          if (src) out.fontFaceSrcs.push({ family: r.style.getPropertyValue('font-family'), src });
        }
      } catch {}
    }
  }

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

  document.querySelectorAll('link[rel="preload"][as="font"], link[rel*="font"]').forEach(l => {
    const href = l.getAttribute('href');
    if (href) out.preloadFontUrls.push({ href, type: l.getAttribute('type') || '' });
  });

  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try { out.jsonLd.push(JSON.parse(s.textContent || 'null')); }
    catch { out.jsonLd.push({ __raw: (s.textContent || '').slice(0, 1500) }); }
  });

  document.querySelectorAll('link[rel*="icon" i], link[rel="apple-touch-icon"], link[rel="image_src"]').forEach(l => {
    out.iconLinks.push({
      rel: l.getAttribute('rel') || '', href: l.getAttribute('href') || '',
      sizes: l.getAttribute('sizes') || '', type: l.getAttribute('type') || ''
    });
  });

  return JSON.stringify(out);
})()"""


def slugify(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    slug = re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-") or "index"
    return slug[:60]


def run_ab(args: list[str], capture: bool = True, check: bool = False, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(agent_browser_cmd(*args), capture_output=capture, text=True, check=check, timeout=timeout)


def navigate_or_settle(url: str) -> tuple[bool, str]:
    """Navigate to URL. agent-browser's 'open' waits for networkidle, which
    on heavy brand sites (videos, ad SDKs, 3p analytics) routinely doesn't
    fire within the 60s subprocess timeout — even though the DOM is fully
    hydrated and ready to query. Treat TimeoutExpired as recoverable: if
    document.readyState is 'interactive' or 'complete' afterwards, we have
    enough to extract the DOM + run probes. Returns (ok, reason).
    """
    try:
        nav = run_ab(["open", url], timeout=90)
        if nav.returncode == 0:
            return True, "navigate ok"
    except subprocess.TimeoutExpired:
        pass  # fall through to readiness check
    # Either non-zero or hard timeout — see if the page is actually loaded.
    try:
        chk = run_ab(["eval", "document.readyState"], timeout=20)
    except subprocess.TimeoutExpired:
        return False, "readyState probe timed out"
    state = parse_ab_eval(chk.stdout).strip().strip('"')
    if state in ("interactive", "complete"):
        return True, f"settled (readyState={state})"
    return False, f"not ready (readyState={state!r})"


def parse_ab_eval(stdout: str) -> str:
    s = stdout.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1].encode("utf-8").decode("unicode_escape")
    return s


def warmup_daemon(sample_url: str) -> None:
    """Pre-flight a fresh agent-browser daemon so the first real page load
    doesn't bear the cost of (cold Chromium boot + first TLS handshake +
    Akamai bot challenge + cookie issuance) all at once.

    Without warmup, the first navigate on heavy CDN-fronted brands routinely
    blows past the 60s subprocess timeout AND blocks the recovery readyState
    probe on the same daemon socket — even though pages 2..N then load in
    a few seconds each (daemon warm, cookies cached).

    Sequence:
      1. set viewport — forces daemon to spawn Chrome for Testing
      2. open about:blank — first navigate is local, completes instantly
      3. open <site root> — gives Akamai/Cloudflare a chance to issue
         session cookies that all subsequent same-origin pages reuse.
         networkidle still won't fire (heavy hero video + ad SDKs), so we
         catch TimeoutExpired and continue regardless.
      4. small sleep — let cookies settle before the real loop starts.
    """
    from urllib.parse import urlparse
    parsed = urlparse(sample_url)
    if not parsed.scheme or not parsed.netloc:
        return
    root = f"{parsed.scheme}://{parsed.netloc}/"
    print(f"[warmup] {root}")
    run_ab(["set", "viewport", "1440", "900"])
    try:
        run_ab(["open", "about:blank"], timeout=30)
    except subprocess.TimeoutExpired:
        pass
    try:
        run_ab(["open", root], timeout=90)
        print("    warmup navigate ok")
    except subprocess.TimeoutExpired:
        # Expected on heavy brand sites — DOM is hydrated, networkidle isn't.
        print("    warmup navigate hit networkidle timeout (DOM still hydrated — fine)")
    time.sleep(2)


def kill_chrome_for_testing() -> None:
    """Cross-platform: kill any 'Chrome for Testing' processes so agent-browser
    respawns a fresh daemon. Used as self-healing when 2+ navigations fail."""
    system = platform.system()
    try:
        if system == "Windows":
            # Best-effort match — Chrome for Testing exe name varies; matches both
            # 'chrome.exe' from CfT and any embedded copies.
            subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe"],
                capture_output=True, timeout=10
            )
        else:
            # macOS / Linux
            subprocess.run(
                ["pkill", "-f", "Chrome for Testing"],
                capture_output=True, timeout=10
            )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: fetch_pages.py <pages.txt> <workspace_dir>", file=sys.stderr)
        return 2

    pages_file = Path(sys.argv[1])
    ws = Path(sys.argv[2]).resolve()
    pages_dir = ws / "recon" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    if shutil.which("agent-browser") is None:
        print("agent-browser not on PATH", file=sys.stderr)
        return 127

    consecutive_failures = 0
    i = 0

    # Pre-flight: warm the daemon + same-origin Akamai/Cloudflare cookies on
    # the first URL's host before starting the real fetch loop. Without this,
    # the very first navigate of the loop frequently absorbs (cold Chromium
    # boot + first TLS handshake + bot challenge) all at once, blowing past
    # the navigate timeout AND blocking the recovery readyState probe on the
    # same daemon socket.
    raw_urls = [
        line.split("#", 1)[0].strip()
        for line in pages_file.read_text(encoding="utf-8").splitlines()
    ]
    real_urls = [u for u in raw_urls if u]
    if real_urls:
        warmup_daemon(real_urls[0])

    for url in real_urls:
        i += 1
        slug = slugify(url)
        page_dir = pages_dir / slug
        page_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{i}] {url}")
        print(f"    slug: {slug} → {page_dir}")

        run_ab(["set", "viewport", "1440", "900"])
        ok, reason = navigate_or_settle(url)
        if not ok:
            print(f"    ✗ navigate failed: {reason}; checking if daemon is exhausted...")
            consecutive_failures += 1
            if consecutive_failures >= 2:
                print(f"    ⚠ {consecutive_failures} consecutive failures — restarting Chrome for Testing")
                kill_chrome_for_testing()
                time.sleep(4)
                run_ab(["set", "viewport", "1440", "900"])
                ok2, reason2 = navigate_or_settle(url)
                if ok2:
                    print(f"    ✓ retry succeeded after daemon restart ({reason2})")
                    consecutive_failures = 0
                    time.sleep(1.5)
                else:
                    (page_dir / "probe.json").write_text(
                        json.dumps({"error": f"navigate failed after restart: {reason2}"}, indent=2)
                    )
                    print(f"    ✗ retry also failed: {reason2}; skipping")
                    continue
            else:
                (page_dir / "probe.json").write_text(json.dumps({"error": f"navigate failed: {reason}"}, indent=2))
                continue
        else:
            consecutive_failures = 0
            print(f"    {reason}")
            time.sleep(1.5)

        # DOM
        dom_res = run_ab(["eval", "document.documentElement.outerHTML"])
        (page_dir / "dom.html").write_text(parse_ab_eval(dom_res.stdout), encoding="utf-8")

        # Screenshot (best-effort)
        try:
            run_ab(["screenshot", str(page_dir / "shot.png")])
        except Exception:
            pass

        # Probe
        try:
            probe_res = run_ab(["eval", PROBE_JS])
            raw = parse_ab_eval(probe_res.stdout)
            j = raw.find("{")
            if j > 0:
                raw = raw[j:]
            try:
                data = json.loads(raw)
                (page_dir / "probe.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
                n_svg = len(data.get("allInlineSvg", []))
                n_img = len(data.get("allImg", []))
                n_jsonld = len(data.get("jsonLd", []))
                print(f"    {n_svg} inline SVGs, {n_img} <img>, {n_jsonld} JSON-LD blocks")
            except json.JSONDecodeError as e:
                (page_dir / "probe.json").write_text(
                    json.dumps({"error": str(e), "raw_preview": raw[:500]}, indent=2)
                )
        except subprocess.TimeoutExpired:
            (page_dir / "probe.json").write_text(json.dumps({"error": "probe timeout"}, indent=2))

    print(f"\nfetch_pages.py: done — {i} pages saved to {pages_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
