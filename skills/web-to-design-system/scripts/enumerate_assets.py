#!/usr/bin/env python3
"""
enumerate_assets.py — Phase 1c: aggregate every brand-asset candidate from all
fetched pages into a single raw-assets.json. Pure deterministic enumeration —
no judgment about which logo / palette / font is "the right one". That's the
LLM's job in step 1d.

Reads:  $WS/recon/pages/<slug>/probe.json   (one per fetched URL)
        $WS/recon/jsonld.json               (homepage's JSON-LD blocks)
        $WS/recon/nav-links.json
Writes: $WS/raw-assets.json

raw-assets.json schema (high-level):
{
  "host": "...",
  "title": "...",
  "logo_candidates": [
    {"id": "<sha8>", "kind": "inline-svg", "page": "home", "region": "header",
     "viewBox": "...", "width": 220, "height": 32, "pathCount": 12,
     "maxPathDLen": 824, "hasText": false, "hasImage": false,
     "ariaLabel": "...", "outerHTML": "<svg>...</svg>", "outerHTML_truncated": false},
    {"id": "<sha8>", "kind": "img", "page": "home", "region": "header",
     "src": "https://...", "alt": "...", "width": 120, "height": 30},
    {"id": "<sha8>", "kind": "icon-link", "rel": "icon", "href": "..."},
    {"id": "<sha8>", "kind": "jsonld-logo", "src": "...", "context": "Organization"},
    {"id": "<sha8>", "kind": "bg-image", "url": "...", "el": "header > div"}
  ],
  "color_frequency": [{"hex": "#FF5733", "count": 142, "sources": ["home", "about"]}],
  "root_vars": {"--brand-blue": "#1F36C7", ...},   # union across pages
  "computed_palette": {                            # what each surface actually paints
    "home/header.bg": "rgb(15, 35, 72)",
    "home/.cta.bg":  "rgb(0, 80, 160)", ...
  },
  "fonts": {
    "frequencies": [{"family": "Source Sans 3", "count": 23}],
    "computed_primary": ["Source Sans 3", "system-ui", "sans-serif"],
    "computed_heading": ["Inter", "sans-serif"],
    "font_face_srcs": [{"family": "...", "src": "url(...) format(woff2)"}],
    "preload_urls": ["https://...woff2"]
  },
  "screenshots": ["recon/pages/index/shot.png", "recon/pages/about/shot.png"],
  "pages_indexed": ["index", "about", "products", ...]
}

Usage: enumerate_assets.py <workspace_dir>
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HEX_RE = re.compile(r"#([0-9a-fA-F]{6})\b|#([0-9a-fA-F]{3})\b")
RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*[\d.]+\s*)?\)")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}\"]+)", re.IGNORECASE)


def short_id(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]


def expand_short_hex(s: str) -> str:
    return "".join(c * 2 for c in s.lower())


def normalize_hex(s: str) -> str | None:
    s = s.strip()
    m = HEX_RE.match(s)
    if m:
        return (m.group(1) or expand_short_hex(m.group(2))).lower()
    m = RGB_RE.match(s)
    if m:
        r, g, b = (max(0, min(255, int(m.group(i)))) for i in (1, 2, 3))
        return f"{r:02x}{g:02x}{b:02x}"
    return None


def extract_colors_from_text(text: str) -> Counter:
    c: Counter = Counter()
    for m in HEX_RE.finditer(text):
        c[(m.group(1) or expand_short_hex(m.group(2))).lower()] += 1
    for m in RGB_RE.finditer(text):
        r, g, b = (max(0, min(255, int(m.group(i)))) for i in (1, 2, 3))
        c[f"{r:02x}{g:02x}{b:02x}"] += 1
    return c


def clean_family(raw: str) -> list[str]:
    parts = []
    for p in raw.split(","):
        n = p.strip().strip("'\"").strip()
        if n.lower() in {"sans-serif", "serif", "monospace", "system-ui", "cursive",
                         "fantasy", "inherit", "initial", "ui-sans-serif", "ui-serif",
                         "ui-monospace", "ui-rounded", "-apple-system",
                         "blinkmacsystemfont", "segoe ui", "helvetica", "arial",
                         "apple color emoji", "segoe ui emoji"}:
            continue
        if n:
            parts.append(n)
    return parts


def crawl_jsonld_logos(blocks, out: list[dict]):
    """Walk JSON-LD payloads recursively, looking for logo / image fields tied to Organization-ish nodes."""
    def visit(obj, ctx_type: str = ""):
        if isinstance(obj, dict):
            t = obj.get("@type") or obj.get("type") or ctx_type
            t_str = t if isinstance(t, str) else (",".join(t) if isinstance(t, list) else "")
            for key in ("logo", "image"):
                v = obj.get(key)
                if isinstance(v, str):
                    out.append({"src": v, "context": t_str, "field": key})
                elif isinstance(v, dict):
                    src = v.get("url") or v.get("contentUrl") or v.get("@id")
                    if isinstance(src, str):
                        out.append({"src": src, "context": t_str, "field": key})
                elif isinstance(v, list):
                    for x in v:
                        if isinstance(x, str):
                            out.append({"src": x, "context": t_str, "field": key})
                        elif isinstance(x, dict) and (x.get("url") or x.get("contentUrl")):
                            out.append({"src": x.get("url") or x.get("contentUrl"),
                                        "context": t_str, "field": key})
            for v in obj.values():
                visit(v, t_str)
        elif isinstance(obj, list):
            for v in obj:
                visit(v, ctx_type)
    visit(blocks)


def main(workspace: str) -> int:
    ws = Path(workspace)
    pages_dir = ws / "recon" / "pages"
    if not pages_dir.exists():
        print(f"ERROR: {pages_dir} not found — run fetch_pages.sh first", file=sys.stderr)
        return 2

    raw = {
        "host": "", "title": "", "pages_indexed": [],
        "logo_candidates": [],
        "color_frequency": [],
        "root_vars": {},
        "computed_palette": {},
        "fonts": {"frequencies": [], "computed_primary": [], "computed_heading": [],
                  "font_face_srcs": [], "preload_urls": []},
        "screenshots": [],
        "icon_links": [],
        "bg_images": [],
        "jsonld_logos": [],
    }

    color_counter: Counter = Counter()
    color_sources: dict = defaultdict(set)
    font_counter: Counter = Counter()
    seen_logo_ids: set[str] = set()

    # 1. Walk every fetched page directory
    for page_dir in sorted(pages_dir.iterdir()):
        if not page_dir.is_dir():
            continue
        slug = page_dir.name
        raw["pages_indexed"].append(slug)
        shot = page_dir / "shot.png"
        if shot.exists():
            raw["screenshots"].append(str(shot.relative_to(ws)))

        probe_path = page_dir / "probe.json"
        if not probe_path.exists():
            continue
        try:
            probe = json.loads(probe_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"warn: {probe_path}: {e}", file=sys.stderr)
            continue

        if not raw["host"]:
            raw["host"] = probe.get("host", "")
        if not raw["title"] and probe.get("title"):
            raw["title"] = probe.get("title", "")

        # 1a. inline SVGs → logo candidates
        for svg in probe.get("allInlineSvg", []) or []:
            payload = svg.get("outerHTML", "")
            if not payload:
                continue
            cid = short_id(payload)
            if cid in seen_logo_ids:
                continue
            seen_logo_ids.add(cid)
            raw["logo_candidates"].append({
                "id": cid, "kind": "inline-svg", "page": slug, "region": svg.get("region"),
                "viewBox": svg.get("viewBox", ""), "width": svg.get("width"),
                "height": svg.get("height"), "pathCount": svg.get("pathCount", 0),
                "maxPathDLen": svg.get("maxPathDLen", 0),
                "hasText": svg.get("hasText", False), "hasImage": svg.get("hasImage", False),
                "ariaLabel": svg.get("ariaLabel", ""), "classNames": svg.get("classNames", ""),
                "outerHTML": payload,
                "outerHTML_truncated": "<!-- truncated -->" in payload,
            })

        # 1b. <img> → logo candidates (filter to plausible logo size)
        for img in probe.get("allImg", []) or []:
            src = img.get("src")
            if not src or src.startswith("data:"):
                continue
            cid = short_id(f"img:{src}")
            if cid in seen_logo_ids:
                continue
            seen_logo_ids.add(cid)
            raw["logo_candidates"].append({
                "id": cid, "kind": "img", "page": slug, "region": img.get("region"),
                "src": src, "alt": img.get("alt", ""),
                "width": img.get("width"), "height": img.get("height"),
                "classNames": img.get("classNames", ""),
            })

        # 1c. icon links
        for il in probe.get("iconLinks", []) or []:
            href = il.get("href")
            if not href:
                continue
            cid = short_id(f"iconlink:{href}:{il.get('rel','')}")
            if cid not in seen_logo_ids:
                seen_logo_ids.add(cid)
                raw["logo_candidates"].append({
                    "id": cid, "kind": "icon-link", "page": slug,
                    "rel": il.get("rel", ""), "href": href,
                    "sizes": il.get("sizes", ""), "type": il.get("type", ""),
                })
            raw["icon_links"].append({"page": slug, **il})

        # 1d. background-image URLs
        for bg in probe.get("bgImageUrls", []) or []:
            url = bg.get("url")
            if not url or url.startswith("data:"):
                continue
            cid = short_id(f"bg:{url}")
            if cid not in seen_logo_ids:
                seen_logo_ids.add(cid)
                raw["logo_candidates"].append({
                    "id": cid, "kind": "bg-image", "page": slug,
                    "region": bg.get("region"), "url": url, "el": bg.get("el", ""),
                })
            raw["bg_images"].append({"page": slug, **bg})

        # 1e. :root vars (union, last write wins)
        for k, v in (probe.get("rootVars") or {}).items():
            raw["root_vars"][k] = v

        # 1f. computed palette per surface (key = page/selector)
        for sel, props in (probe.get("computed") or {}).items():
            if not isinstance(props, dict):
                continue
            raw["computed_palette"][f"{slug}/{sel}"] = props
            # bleed colors into color counter, weighted lower than literal scans
            for v in props.values():
                if isinstance(v, str):
                    h = normalize_hex(v)
                    if h:
                        color_counter[h] += 1
                        color_sources[h].add(slug)

        # 1g. font-face srcs / preload fonts
        for ff in probe.get("fontFaceSrcs", []) or []:
            raw["fonts"]["font_face_srcs"].append({"page": slug, **ff})
        for pf in probe.get("preloadFontUrls", []) or []:
            raw["fonts"]["preload_urls"].append(pf.get("href", ""))

        # 1h. fonts from probe.computed surfaces
        for sel, props in (probe.get("computed") or {}).items():
            font_str = props.get("font") if isinstance(props, dict) else None
            if isinstance(font_str, str):
                for fam in clean_family(font_str):
                    font_counter[fam] += 1
            if sel == "body" and isinstance(props, dict):
                if isinstance(props.get("font"), str) and not raw["fonts"]["computed_primary"]:
                    raw["fonts"]["computed_primary"] = clean_family(props["font"])
            if sel in ("h1", "h2") and isinstance(props, dict):
                if isinstance(props.get("font"), str) and not raw["fonts"]["computed_heading"]:
                    raw["fonts"]["computed_heading"] = clean_family(props["font"])

        # 1i. on-page font-family literal scan (catches CSS in <style> blocks)
        dom_path = page_dir / "dom.html"
        if dom_path.exists():
            text = dom_path.read_text(encoding="utf-8", errors="replace")
            for m in FONT_FAMILY_RE.finditer(text):
                for fam in clean_family(m.group(1)):
                    font_counter[fam] += 1
            ccnt = extract_colors_from_text(text)
            for h, n in ccnt.items():
                color_counter[h] += n
                color_sources[h].add(slug)

        # 1j. JSON-LD on this page
        jl_blocks = probe.get("jsonLd") or []
        page_logos: list[dict] = []
        crawl_jsonld_logos(jl_blocks, page_logos)
        for entry in page_logos:
            cid = short_id(f"jsonld:{entry['src']}:{entry['context']}")
            if cid not in seen_logo_ids:
                seen_logo_ids.add(cid)
                raw["logo_candidates"].append({
                    "id": cid, "kind": "jsonld-logo", "page": slug, **entry,
                })
            raw["jsonld_logos"].append({"page": slug, **entry})

    # 2. Homepage-level JSON-LD (from fetch_sitemap.sh)
    home_jl = ws / "recon" / "jsonld.json"
    if home_jl.exists():
        try:
            blocks = json.loads(home_jl.read_text(encoding="utf-8"))
            extra: list[dict] = []
            crawl_jsonld_logos(blocks, extra)
            for entry in extra:
                cid = short_id(f"jsonld-home:{entry['src']}:{entry['context']}")
                if cid not in seen_logo_ids:
                    seen_logo_ids.add(cid)
                    raw["logo_candidates"].append({
                        "id": cid, "kind": "jsonld-logo", "page": "home", **entry,
                    })
        except Exception as e:
            print(f"warn: home jsonld: {e}", file=sys.stderr)

    # 3. Finalize aggregates
    raw["color_frequency"] = [
        {"hex": f"#{h.upper()}", "count": n, "sources": sorted(color_sources[h])}
        for h, n in color_counter.most_common(60)
    ]
    raw["fonts"]["frequencies"] = [
        {"family": f, "count": n} for f, n in font_counter.most_common(20)
    ]

    # 4. Sort logo candidates: highest "interestingness" first
    # (this is *ranking*, not *selection*; LLM still picks. Just helps it scan.)
    def interest(c: dict) -> int:
        score = 0
        if c.get("kind") == "inline-svg":
            # path-rich SVGs in header/footer rank highest
            score += min(c.get("maxPathDLen", 0), 5000)
            score += c.get("pathCount", 0) * 5
            if c.get("region") in ("header", "footer", "logo-class"):
                score += 200
            if c.get("hasText"):
                score -= 50  # text-only SVG is suspicious
        elif c.get("kind") == "jsonld-logo":
            score += 1500  # explicit declared logo, very high signal
        elif c.get("kind") == "icon-link":
            sz = (c.get("sizes") or "")
            score += 300
            if "180" in sz or "192" in sz or "512" in sz:
                score += 200
        elif c.get("kind") == "img":
            if c.get("region") in ("header", "footer"):
                score += 100
            if "logo" in (c.get("alt") or "").lower() or "logo" in (c.get("classNames") or "").lower():
                score += 250
        elif c.get("kind") == "bg-image":
            if c.get("region") in ("header", "footer"):
                score += 80
        return score

    raw["logo_candidates"].sort(key=interest, reverse=True)

    out_path = ws / "raw-assets.json"
    out_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    # Stats
    print(f"wrote {out_path}")
    print(f"  pages indexed:      {len(raw['pages_indexed'])}")
    print(f"  logo candidates:    {len(raw['logo_candidates'])}")
    by_kind: Counter = Counter(c["kind"] for c in raw["logo_candidates"])
    for k, n in by_kind.most_common():
        print(f"    - {k}: {n}")
    print(f"  color frequency:    {len(raw['color_frequency'])} unique values")
    print(f"  :root vars:         {len(raw['root_vars'])}")
    print(f"  font families:      {len(raw['fonts']['frequencies'])}")
    print(f"  computed surfaces:  {len(raw['computed_palette'])}")
    print(f"  font-face srcs:     {len(raw['fonts']['font_face_srcs'])}")
    print(f"  jsonld logo refs:   {len(raw['jsonld_logos'])}")
    print(f"  bg-image refs:      {len(raw['bg_images'])}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: enumerate_assets.py <workspace_dir>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
