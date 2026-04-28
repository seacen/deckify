#!/usr/bin/env python3
"""
embed_logo.py — Phase 1e: take the LLM's chosen logo (by id), validate it,
download if remote, base64-embed if raster, generate a <symbol> snippet.

Reads:
    $WS/raw-assets.json     (the pool of logo candidates with stable ids)
    $WS/brand.json          (LLM output; must contain chosen_logo_id)

Writes:
    $WS/assets/logo.<ext>           original payload (svg/png/jpg/webp)
    $WS/assets/logo.embed.html      <symbol id="brand-wm">…</symbol> ready to paste
    $WS/assets/logo.dataurl         data: URL (utility for DS markdown)
    $WS/assets/logo.report.json     what passed / failed quality gate

Quality gates (hard, deterministic):
    SVG:    must have at least one <path d="..."> with len(d) >= 40
            OR an <image> child (raster fallback inside SVG)
    Raster: min(width, height) >= 64
    Both:   non-empty payload

If chosen logo fails the gate, exits non-zero with an explicit error so the
agent knows to pick another candidate from raw-assets.json.

Usage: embed_logo.py <workspace_dir>
"""
from __future__ import annotations

import base64
import json
import re
import struct
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ab_common import agent_browser_cmd  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
}
TIMEOUT = 20
MIN_RASTER_SIDE = 64
MIN_PATH_D_LEN = 40

PATH_D_RE = re.compile(r'<path[^>]*\sd="([^"]+)"', re.IGNORECASE)
VIEWBOX_RE = re.compile(r'\sviewBox="([^"]+)"', re.IGNORECASE)
WIDTH_RE = re.compile(r'\swidth="([^"]+)"', re.IGNORECASE)
HEIGHT_RE = re.compile(r'\sheight="([^"]+)"', re.IGNORECASE)
TEXT_RE = re.compile(r'<text\b', re.IGNORECASE)
IMAGE_RE = re.compile(r'<image\b', re.IGNORECASE)

CT_TO_EXT = {
    "image/svg+xml": "svg", "image/svg": "svg",
    "image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg",
    "image/webp": "webp", "image/gif": "gif",
    "image/x-icon": "ico", "image/vnd.microsoft.icon": "ico",
}


def http_get(url: str, referer: str | None = None) -> tuple[bytes, str]:
    """Fetch URL via agent-browser by default.

    The skill's whole pipeline already drives a real Chrome via agent-browser to
    pass anti-bot and TLS quirks on production brand sites. Using urllib here
    would defeat that — many CDNs (Akamai, Cloudflare-bot-management, Imperva)
    reject anything that doesn't look like a fully-fingerprinted browser.

    Strategy:
      1. agent-browser open <url>  (navigate the browser AT the asset itself —
         this handles both same-origin assets and third-party CMS CDNs like
         Contentful / Cloudinary that block cross-origin in-page fetch via CORS)
      2. agent-browser eval `fetch(location.href) → arrayBuffer → base64`
         (now a same-origin fetch — no CORS issue because the page IS the asset)
      3. Decode base64 + content-type → return

    Why not "navigate to referer, then cross-origin fetch the asset"?
    Many production CMS CDNs (Contentful, Cloudinary, Akamai-fronted) set CORS
    headers that BLOCK cross-origin in-page fetch even when the asset is
    publicly readable. Direct navigation to the asset URL succeeds where
    cross-origin fetch fails. Surfaced concretely on P&G's JSON-LD logo at
    images.ctfassets.net (2026-04-27).
    """
    import subprocess, json as _json
    # Navigate the browser AT the asset URL itself — this is the most reliable
    # path for both same-origin assets and third-party CMS CDNs.
    try:
        subprocess.run(agent_browser_cmd("open", url),
                       capture_output=True, timeout=30, check=False)
    except Exception:
        pass
    # `location.href` instead of the literal URL — once we've navigated to the
    # asset, fetch(location.href) is by definition same-origin and bypasses CORS.
    js = (
        "(async () => {"
        "  const r = await fetch(location.href, {credentials:'include'});"
        "  if (!r.ok) throw new Error('HTTP ' + r.status);"
        "  const b = await r.arrayBuffer();"
        "  const a = new Uint8Array(b);"
        "  let s = ''; for (let i=0;i<a.length;i++) s += String.fromCharCode(a[i]);"
        "  return JSON.stringify({ct: r.headers.get('content-type') || '', b64: btoa(s), bytes: a.length});"
        "})()"
    )
    try:
        result = subprocess.run(agent_browser_cmd("eval", js),
                                capture_output=True, timeout=90, check=False)
    except FileNotFoundError:
        # Last-resort fallback if agent-browser is somehow missing — try urllib
        req = urllib.request.Request(url, headers={"User-Agent": UA, **BROWSER_HEADERS})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read(), r.headers.get("Content-Type", "").lower().split(";")[0].strip()

    if result.returncode != 0:
        raise RuntimeError(f"agent-browser fetch failed: {result.stderr.decode('utf-8', 'replace')[:300]}")

    out = result.stdout.decode("utf-8", "replace").strip()
    # agent-browser eval may double-wrap JSON-string output. Unwrap once.
    if out.startswith('"') and out.endswith('"'):
        out = out[1:-1].encode().decode("unicode_escape")
    i = out.find("{")
    if i > 0:
        out = out[i:]
    payload = _json.loads(out)
    return (base64.b64decode(payload["b64"]),
            (payload.get("ct") or "").lower().split(";")[0].strip())


def raster_size(buf: bytes) -> tuple[int, int] | None:
    if len(buf) < 24:
        return None
    if buf.startswith(b"\x89PNG\r\n\x1a\n") and buf[12:16] == b"IHDR":
        return struct.unpack(">II", buf[16:24])
    if buf[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", buf[6:10])
    if buf[:4] == b"RIFF" and buf[8:12] == b"WEBP":
        if buf[12:16] == b"VP8X":
            w = (buf[24] | (buf[25] << 8) | (buf[26] << 16)) + 1
            h = (buf[27] | (buf[28] << 8) | (buf[29] << 16)) + 1
            return w, h
    if buf[:2] == b"\xff\xd8":
        i = 2
        while i < len(buf) - 9:
            if buf[i] != 0xFF:
                i += 1; continue
            m = buf[i + 1]; i += 2
            if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                continue
            seg = struct.unpack(">H", buf[i:i + 2])[0]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB):
                h, w = struct.unpack(">HH", buf[i + 3:i + 7])
                return w, h
            i += seg
    return None


def svg_dims(svg: str) -> tuple[float, float] | None:
    m = VIEWBOX_RE.search(svg)
    if m:
        parts = re.split(r'[\s,]+', m.group(1).strip())
        if len(parts) == 4:
            try:
                return float(parts[2]), float(parts[3])
            except ValueError:
                pass
    wm, hm = WIDTH_RE.search(svg), HEIGHT_RE.search(svg)
    if wm and hm:
        try:
            return float(re.sub(r'[^\d.]', '', wm.group(1))), float(re.sub(r'[^\d.]', '', hm.group(1)))
        except ValueError:
            pass
    return None


def svg_passes(svg: str) -> tuple[bool, dict]:
    paths = PATH_D_RE.findall(svg)
    max_d = max((len(d) for d in paths), default=0)
    has_image = bool(IMAGE_RE.search(svg))
    ev = {"paths": len(paths), "max_d_len": max_d, "has_inner_image": has_image,
          "has_text": bool(TEXT_RE.search(svg)), "dims": svg_dims(svg)}
    if max_d >= MIN_PATH_D_LEN or has_image:
        return True, ev
    return False, {**ev, "reason": "no path with d ≥ 40 and no <image>"}


def png_color_type(buf: bytes) -> int | None:
    """Return PNG IHDR colour-type byte, or None if not a PNG.
    0 = grayscale  2 = RGB  3 = palette  4 = grayscale+alpha  6 = RGBA"""
    if not buf.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    if buf[12:16] != b"IHDR":
        return None
    return buf[25]


def png_has_alpha(buf: bytes) -> bool:
    """True if the PNG has an alpha channel (color type 4 or 6 OR has tRNS chunk for type 3 palette)."""
    ct = png_color_type(buf)
    if ct is None:
        return False
    if ct in (4, 6):
        return True
    if ct == 3:
        # palette PNG — check for tRNS chunk (transparency table)
        return b"tRNS" in buf[:512]
    return False


def raster_passes(buf: bytes) -> tuple[bool, dict]:
    sz = raster_size(buf)
    if not sz:
        return False, {"reason": "unknown raster format"}
    w, h = sz
    if min(w, h) < MIN_RASTER_SIDE:
        return False, {"size": [w, h], "reason": f"min side < {MIN_RASTER_SIDE}"}
    # PNG-specific: warn (don't fail) if no alpha channel — surface the trade-off.
    # An RGB-only PNG cannot composite cleanly on coloured backgrounds; filter:invert
    # flips both the silhouette AND its surrounding rectangle, producing a visible
    # bright square on dark covers. The skill caller can choose to swap to a different
    # candidate or accept the trade-off (and document it in chosen_logo.why).
    info = {"size": [w, h]}
    if buf.startswith(b"\x89PNG\r\n\x1a\n"):
        if png_has_alpha(buf):
            info["alpha"] = "rgba"
        else:
            info["alpha"] = "rgb-only"
            info["warning"] = (
                "PNG has no alpha channel (RGB-only). filter:invert / brightness(0) "
                "on this logo flips BOTH the silhouette AND its background rectangle, "
                "producing a visible bright square on dark covers. Prefer an SVG or "
                "RGBA-PNG candidate when available."
            )
    return True, info


def find_candidate(raw_assets: dict, logo_id: str) -> dict | None:
    for c in raw_assets.get("logo_candidates", []):
        if c.get("id") == logo_id:
            return c
    return None


def materialize_inline_svg(cand: dict, assets_dir: Path) -> dict:
    svg = cand.get("outerHTML", "")
    if cand.get("outerHTML_truncated"):
        return {"ok": False, "reason": "inline SVG was truncated in raw-assets — cannot use"}
    ok, ev = svg_passes(svg)
    out = assets_dir / "logo.svg"
    out.write_text(svg, encoding="utf-8")
    return {"ok": ok, "format": "svg", "path": str(out), "evidence": ev}


def materialize_url(url: str, base_url: str | None, assets_dir: Path) -> dict:
    if not url:
        return {"ok": False, "reason": "candidate has no src/url"}
    if url.startswith("data:"):
        return {"ok": False, "reason": "data: URLs not yet supported (could be added)"}
    if url.startswith("/") and base_url:
        url = urllib.parse.urljoin(base_url, url)
    elif not url.startswith(("http://", "https://")) and base_url:
        url = urllib.parse.urljoin(base_url, url)
    try:
        body, ct = http_get(url, referer=base_url)
    except Exception as e:
        return {"ok": False, "reason": f"download failed: {e}", "url": url}
    ext = CT_TO_EXT.get(ct, "")
    if not ext:
        for guess in ("svg", "png", "jpg", "webp", "gif", "ico"):
            if url.lower().split("?")[0].endswith("." + guess):
                ext = guess; break
    if not ext:
        return {"ok": False, "reason": f"unknown content-type: {ct}", "url": url}
    out = assets_dir / f"logo.{ext}"
    out.write_bytes(body)
    if ext == "svg":
        ok, ev = svg_passes(body.decode("utf-8", errors="replace"))
    else:
        ok, ev = raster_passes(body)
    return {"ok": ok, "format": ext, "path": str(out), "evidence": ev, "url": url}


def build_embed(result: dict) -> tuple[str, str]:
    p = Path(result["path"])
    fmt = result["format"]
    if fmt == "svg":
        svg = p.read_text(encoding="utf-8")
        m = VIEWBOX_RE.search(svg)
        if m:
            viewbox = m.group(1)
        else:
            d = svg_dims(svg)
            viewbox = f"0 0 {d[0]:g} {d[1]:g}" if d else "0 0 100 100"
        # strip outer <svg ...>...</svg>
        inner = re.sub(r'^\s*<svg[^>]*>', '', svg, count=1, flags=re.IGNORECASE | re.DOTALL)
        inner = re.sub(r'</svg>\s*$', '', inner, count=1, flags=re.IGNORECASE)
        # strip <style>...</style> blocks (they pin fill colors and defeat currentColor)
        inner = re.sub(r'<style[^>]*>.*?</style>', '', inner, flags=re.IGNORECASE | re.DOTALL)
        # strip <metadata>, <defs> with linearGradient/radialGradient that pin colors
        inner = re.sub(r'<metadata[^>]*>.*?</metadata>', '', inner, flags=re.IGNORECASE | re.DOTALL)
        # remove hardcoded fills so currentColor works (keep fill="none" — that means stroke-only)
        inner = re.sub(r'\sfill="(?!none\b|currentColor\b)[^"]+"', '', inner, flags=re.IGNORECASE)
        # also strip inline style="fill:..."
        inner = re.sub(r'\sstyle="[^"]*fill:[^;"]*[;"]?[^"]*"', '', inner, flags=re.IGNORECASE)
        embed = (
            '<svg style="display:none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n'
            f'  <symbol id="brand-wm" viewBox="{viewbox}" fill="currentColor">\n'
            f'{inner}\n'
            '  </symbol>\n'
            '</svg>'
        )
        b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return embed, f"data:image/svg+xml;base64,{b64}"
    body = p.read_bytes()
    mime = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp",
            "gif": "image/gif", "ico": "image/x-icon"}.get(fmt, "image/png")
    b64 = base64.b64encode(body).decode("ascii")
    dataurl = f"data:{mime};base64,{b64}"
    sz = raster_size(body) or (256, 256)
    embed = (
        '<svg style="display:none" xmlns="http://www.w3.org/2000/svg"\n'
        '     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">\n'
        f'  <symbol id="brand-wm" viewBox="0 0 {sz[0]} {sz[1]}">\n'
        f'    <image href="{dataurl}" width="{sz[0]}" height="{sz[1]}"/>\n'
        '  </symbol>\n'
        '</svg>'
    )
    return embed, dataurl


def main(workspace: str) -> int:
    ws = Path(workspace)
    raw_path = ws / "raw-assets.json"
    brand_path = ws / "brand.json"
    if not raw_path.exists():
        print(f"ERROR: {raw_path} not found — run enumerate_assets.py first", file=sys.stderr)
        return 2
    if not brand_path.exists():
        print(f"ERROR: {brand_path} not found — agent must write it (LLM step 1d)", file=sys.stderr)
        return 2
    raw_assets = json.loads(raw_path.read_text(encoding="utf-8"))
    brand = json.loads(brand_path.read_text(encoding="utf-8"))
    chosen = brand.get("chosen_logo") or {}
    logo_id = chosen.get("id") or brand.get("chosen_logo_id")
    explicit_url = chosen.get("url")
    explicit_kind = chosen.get("kind") or "jsonld-logo"
    if not logo_id and not explicit_url:
        print("ERROR: brand.json must include chosen_logo.id, chosen_logo_id, or chosen_logo.url",
              file=sys.stderr)
        return 2

    assets_dir = ws / "assets"
    assets_dir.mkdir(exist_ok=True)

    base_url = brand.get("base_url") or f"https://{raw_assets.get('host', '')}"

    # Two ways to point at a logo:
    # 1. Standard path — chosen_logo.id refers to a stable candidate id in
    #    raw-assets.json (the schema synthesize-brand.md describes).
    # 2. Direct URL — chosen_logo.url + (optional) chosen_logo.kind. Used when
    #    the LLM identified an authoritative source (e.g. JSON-LD
    #    Organization.logo or a press-kit URL) that wasn't enumerated as a
    #    discrete candidate by enumerate_assets.py. The candidate enumerator
    #    can't always know which JSON-LD logos are organisational vs product
    #    listings, so this escape hatch lets the LLM pick what evidence shows.
    cand: dict
    if logo_id:
        found = find_candidate(raw_assets, logo_id)
        if not found:
            if not explicit_url:
                print(f"ERROR: no candidate with id={logo_id} in raw-assets.json", file=sys.stderr)
                return 2
            print(f"note: id={logo_id} not in raw-assets.json — falling back to chosen_logo.url")
            cand = {"id": logo_id, "kind": explicit_kind, "url": explicit_url, "page": "(explicit)"}
        else:
            cand = found
    else:
        cand = {"id": "(explicit-url)", "kind": explicit_kind, "url": explicit_url, "page": "(explicit)"}

    print(f"chosen logo:  id={cand.get('id')}  kind={cand['kind']}  page={cand.get('page', '?')}")

    if cand["kind"] == "inline-svg":
        result = materialize_inline_svg(cand, assets_dir)
    elif cand["kind"] in ("img", "icon-link", "jsonld-logo", "bg-image"):
        url = cand.get("src") or cand.get("href") or cand.get("url")
        result = materialize_url(url, base_url, assets_dir)
    else:
        print(f"ERROR: unknown candidate kind: {cand['kind']}", file=sys.stderr)
        return 2

    (assets_dir / "logo.report.json").write_text(
        json.dumps({"chosen": cand, "result": result}, indent=2, ensure_ascii=False)
    )

    if not result.get("ok"):
        print(f"FAIL quality gate: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        print("→ agent should pick another candidate id and rerun.", file=sys.stderr)
        return 1

    embed, dataurl = build_embed(result)
    (assets_dir / "logo.embed.html").write_text(embed, encoding="utf-8")
    (assets_dir / "logo.dataurl").write_text(dataurl, encoding="utf-8")

    print(f"  format: {result['format']}  path: {result['path']}")
    print(f"  embed:  {assets_dir / 'logo.embed.html'}")
    print(f"  dataurl bytes: {len(dataurl)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: embed_logo.py <workspace_dir>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
