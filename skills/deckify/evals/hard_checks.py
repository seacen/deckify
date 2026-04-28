#!/usr/bin/env python3
"""
hard_checks.py — deterministic verification layer of the auto-eval.

Drives agent-browser to render the deck, measure DOM, and run regex
checks over the source HTML / DS markdown. No LLM calls.

Output: dict[check_id -> {"passed": bool, "evidence": ...}].

Usage:
    python3 hard_checks.py <deck.html> <ds.md> <out_dir>
        out_dir receives: measurements.json, slides/<n>.png, mobile.png
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

AB = "agent-browser"
JS_DESKTOP_MEASURE = r"""(()=>{
  const slides = Array.from(document.querySelectorAll('.slide'));
  const out = {slideCount: slides.length, slides: [], deck: null, body: null, consoleErrors: window.__captured_errors || []};
  const deck = document.querySelector('#deck');
  if (deck) {
    const r = deck.getBoundingClientRect();
    out.deck = {w: r.width, h: r.height, scW: deck.scrollWidth, scH: deck.scrollHeight};
  }
  out.body = {scrollWidth: document.body.scrollWidth, overflowX: getComputedStyle(document.body).overflowX,
              fontFamily: getComputedStyle(document.body).fontFamily};
  // Sample the first visible CJK text element's computed font-family to verify CJK fallback actually engages
  const CJK_RE = /[一-鿿぀-ヿ가-힯]/;
  let cjkSample = null;
  const candidates = document.querySelectorAll('h1,h2,h3,p,li,div,span');
  for (const el of candidates) {
    const txt = (el.textContent || '').trim();
    if (txt.length < 2 || !CJK_RE.test(txt)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 10 || r.height < 10) continue;
    cjkSample = {tag: el.tagName, text: txt.slice(0, 40), fontFamily: getComputedStyle(el).fontFamily,
                 fontWeight: getComputedStyle(el).fontWeight, fontSize: getComputedStyle(el).fontSize};
    break;
  }
  out.cjkSample = cjkSample;
  // Activate each slide in turn and measure
  for (let i = 0; i < slides.length; i++) {
    slides.forEach((s,k)=>s.classList.toggle('active', k===i));
    const a = slides[i];
    const r = a.getBoundingClientRect();
    const sc = a.querySelector('.sw .sc') || a.querySelector('.sc');
    const scR = sc ? sc.getBoundingClientRect() : null;
    // Count flex:1 absorbers (children of .sc)
    let absorbers = 0;
    if (sc) {
      Array.from(sc.children).forEach(ch => {
        const cs = getComputedStyle(ch);
        const fg = cs.flexGrow;
        const fs = cs.flexShrink;
        if (parseFloat(fg) >= 1 && parseFloat(fs) >= 1) absorbers++;
      });
    }
    // Logo presence on this slide
    const logos = a.querySelectorAll('.logo');
    const logoBboxes = Array.from(logos).map(l => {
      const lr = l.getBoundingClientRect();
      return {w: lr.width, h: lr.height, visible: lr.width>0 && lr.height>0};
    });
    // Text layout probes — overflow, bottom-guard, headline line count
    const slideRect = a.getBoundingClientRect();
    const slideBottom = slideRect.bottom;
    const overflowingText = [];
    const allText = a.querySelectorAll('h1,h2,h3,h4,p,li,figcaption,blockquote,div,span');
    let maxBottom = -Infinity;
    let maxBottomTag = '';
    let maxBottomText = '';
    const lineCounts = [];
    allText.forEach(el => {
      const cs = getComputedStyle(el);
      // 文本截断/溢出检测：仅看显式块级文本容器，避免误报 flex 容器
      if (el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0
          && (cs.overflow === 'hidden' || cs.overflowY === 'hidden')
          && cs.textOverflow !== 'ellipsis') {
        const r2 = el.getBoundingClientRect();
        if (r2.width > 30 && r2.height > 10) {
          overflowingText.push({tag: el.tagName, text: (el.textContent||'').trim().slice(0,80),
                                clientH: el.clientHeight, scrollH: el.scrollHeight});
        }
      }
      // 跟踪页面里"最低的可见文本元素"位置
      const txt = (el.textContent || '').trim();
      if (txt.length > 2 && el.children.length === 0) {
        const r3 = el.getBoundingClientRect();
        if (r3.width > 0 && r3.height > 0 && r3.bottom > maxBottom && r3.bottom <= slideBottom + 1) {
          maxBottom = r3.bottom;
          maxBottomTag = el.tagName;
          maxBottomText = txt.slice(0, 60);
        }
      }
      // 标题类元素的行数（heading 不应被胡乱拆成 4+ 行）
      if (['H1','H2','H3'].includes(el.tagName)) {
        const lh = parseFloat(cs.lineHeight);
        const h = el.getBoundingClientRect().height;
        if (lh > 0 && h > 0) {
          const lines = Math.round(h / lh);
          if (lines > 0) lineCounts.push({tag: el.tagName, lines, text: (el.textContent||'').trim().slice(0,60)});
        }
      }
    });
    const bottomGap = (maxBottom > -Infinity) ? (slideBottom - maxBottom) : null;

    out.slides.push({
      idx: i,
      width: a.offsetWidth, height: a.offsetHeight,
      bbWidth: r.width, bbHeight: r.height,
      scrollWidth: a.scrollWidth, scrollHeight: a.scrollHeight,
      scH: scR ? scR.height : null, scScrollH: sc ? sc.scrollHeight : null,
      scOverflows: sc ? sc.scrollHeight > sc.clientHeight + 1 : null,
      absorbers,
      logoCount: logos.length,
      logoBboxes,
      textLayout: {
        overflowingText: overflowingText.slice(0, 5),
        bottomGap, bottomTag: maxBottomTag, bottomText: maxBottomText,
        headingLines: lineCounts,
      },
    });
  }
  // Reset to slide 0
  slides.forEach((s,k)=>s.classList.toggle('active', k===0));
  // Also probe the brand-wm symbol contents
  const sym = document.querySelector('symbol#brand-wm');
  if (sym) {
    out.brandSymbol = {
      pathCount: sym.querySelectorAll('path').length,
      pathDLen: Array.from(sym.querySelectorAll('path')).map(p => (p.getAttribute('d')||'').length),
      textCount: sym.querySelectorAll('text').length,
      imageCount: sym.querySelectorAll('image').length,
      circleCount: sym.querySelectorAll('circle').length,
      hasInnerFill: !!sym.querySelector('[fill]:not([fill="none"]):not([fill="currentColor"])'),
    };
  } else {
    out.brandSymbol = null;
  }
  return JSON.stringify(out);
})()"""

JS_MOBILE_MEASURE = r"""(()=>{
  const out = {body: {scrollWidth: document.body.scrollWidth}, multiCol: []};
  ['.g2','.g3','.flip-row','.tabs','.f-row','.fr'].forEach(sel => {
    document.querySelectorAll(sel).forEach(el => {
      const cs = getComputedStyle(el);
      out.multiCol.push({selector: sel, flexDir: cs.flexDirection, gridCols: cs.gridTemplateColumns, displayMode: cs.display});
    });
  });
  return JSON.stringify(out);
})()"""


def run_ab(args: list[str], capture=True, check=False):
    return subprocess.run([AB, *args], capture_output=capture, text=True, check=check, timeout=60)


def parse_ab_eval(out: str):
    """agent-browser eval prints JSON wrapped in quotes; unwrap."""
    s = out.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1].encode().decode("unicode_escape")
    # find first { or [
    for i, c in enumerate(s):
        if c in "{[":
            s = s[i:]
            break
    return json.loads(s)


def measure_desktop(deck_path: Path, out_dir: Path) -> dict:
    run_ab(["set", "viewport", "1440", "900"])
    run_ab(["open", f"file://{deck_path.resolve()}"])
    import time; time.sleep(1.2)
    res = run_ab(["eval", JS_DESKTOP_MEASURE])
    try:
        measurements = parse_ab_eval(res.stdout)
    except Exception as e:
        return {"error": f"desktop measure failed: {e}", "raw": res.stdout[:500]}
    # screenshot first slide as the cover
    shots_dir = out_dir / "slides"
    shots_dir.mkdir(parents=True, exist_ok=True)
    for i in range(measurements.get("slideCount", 0)):
        run_ab(["eval", f"document.querySelectorAll('.slide').forEach((s,k)=>s.classList.toggle('active',k==={i}))"])
        time.sleep(0.25)
        run_ab(["screenshot", str(shots_dir / f"slide-{i+1:02d}.png")])
    return measurements


def measure_mobile(deck_path: Path, out_dir: Path) -> dict:
    import time
    run_ab(["set", "viewport", "375", "812"])
    run_ab(["open", f"file://{deck_path.resolve()}"])
    time.sleep(1.0)
    res = run_ab(["eval", JS_MOBILE_MEASURE])
    try:
        m = parse_ab_eval(res.stdout)
    except Exception as e:
        m = {"error": str(e), "raw": res.stdout[:500]}
    run_ab(["screenshot", str(out_dir / "mobile.png")])
    # restore desktop viewport
    run_ab(["set", "viewport", "1440", "900"])
    return m


# ── checks ────────────────────────────────────────────────────────────────

def check_slide_dimensions(measurements: dict) -> dict:
    bad = []
    for s in measurements.get("slides", []):
        if abs(s["width"] - 1280) > 2 or abs(s["height"] - 720) > 2:
            bad.append({"idx": s["idx"], "w": s["width"], "h": s["height"]})
    return {"passed": len(bad) == 0, "evidence": {"bad_slides": bad, "n_slides": len(measurements.get("slides", []))}}


def check_fit_contract(measurements: dict) -> dict:
    # Skip cover (slide 0) — covers don't always have an absorber.
    bad = []
    for s in measurements.get("slides", []):
        if s["idx"] == 0:
            continue
        if s["absorbers"] != 1:
            bad.append({"idx": s["idx"], "absorbers": s["absorbers"]})
    return {"passed": len(bad) == 0, "evidence": {"bad_slides": bad}}


HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
ROOT_BLOCK_RE = re.compile(r":root\s*\{[^}]*\}", re.DOTALL)


# Universal-backdrop colors that are reasonable to use without a token.
# (e.g. the page-outside-the-deck background, scrim overlays, pure-white text on dark cover.)
TOKEN_HEX_ALLOWLIST = {"#fff", "#FFF", "#ffffff", "#FFFFFF", "#000", "#000000"}


def check_token_only_colors(html: str) -> dict:
    """Find <style> blocks. Strip :root{...}. Then any remaining hex literal not in the allowlist is a violation."""
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    violations = []
    for blk in style_blocks:
        # remove :root blocks (where token defs legitimately have hex)
        cleaned = ROOT_BLOCK_RE.sub("", blk)
        for m in HEX_RE.finditer(cleaned):
            hex_str = m.group(0)
            if hex_str in TOKEN_HEX_ALLOWLIST:
                continue
            i = m.start()
            ctx = cleaned[max(0, i-30):i+10]
            violations.append({"hex": hex_str, "context": ctx.strip()})
    return {"passed": len(violations) == 0, "evidence": {"count": len(violations), "samples": violations[:10]}}


# Pictographic emoji ranges. Explicitly EXCLUDES typographic symbols:
#   - U+2600–U+26FF (misc symbols, includes ✓ ✗ → ←)
#   - U+2700–U+27BF (dingbats, includes ✂ ✔ ✖)
# These are documented as permitted in the DS template ("typographic symbols only").
EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FAFF]"
)


def check_no_emoji(html: str) -> dict:
    matches = EMOJI_RE.findall(html)
    return {"passed": len(matches) == 0, "evidence": {"count": len(matches), "samples": list(set(matches))[:10]}}


def check_mobile_collapse(mobile: dict) -> dict:
    if "error" in mobile:
        return {"passed": False, "evidence": mobile}
    body_w = mobile.get("body", {}).get("scrollWidth", 9999)
    multi_col = mobile.get("multiCol", [])
    # no horizontal scroll
    horiz_ok = body_w <= 375 + 2  # 2px tolerance
    # every multi-col element should be flex-direction: column OR grid-template-columns: ~"none/1fr"
    bad = []
    for el in multi_col:
        is_column = el.get("flexDir") == "column"
        is_single_grid = "1fr" in (el.get("gridCols") or "") or el.get("gridCols") in (None, "none", "")
        # tabs (a row of tab buttons) is allowed to stay row — accept either
        if el.get("selector") == ".tabs":
            continue
        if not (is_column or is_single_grid or el.get("displayMode") == "block"):
            bad.append(el)
    return {
        "passed": horiz_ok and len(bad) == 0,
        "evidence": {"body_scrollWidth": body_w, "horiz_ok": horiz_ok, "bad_multi_col": bad[:10]},
    }


def check_logo_renders(measurements: dict) -> dict:
    sym = measurements.get("brandSymbol")
    if not sym:
        return {"passed": False, "evidence": "no <symbol id='brand-wm'> defined"}
    # must contain either a path with d>40 chars, OR an <image href> (raster fallback embedded)
    has_real_vector = any(d > 40 for d in sym.get("pathDLen", []))
    has_image = sym.get("imageCount", 0) > 0
    has_inner_fill_violation = sym.get("hasInnerFill", False)
    # Also confirm logos rendered visibly on at least the cover
    visible_on_cover = False
    if measurements.get("slides"):
        cover = measurements["slides"][0]
        visible_on_cover = any(b.get("visible") for b in cover.get("logoBboxes", []))
    passed = (has_real_vector or has_image) and visible_on_cover and not has_inner_fill_violation
    return {
        "passed": passed,
        "evidence": {
            "has_real_vector_path": has_real_vector,
            "has_embedded_image": has_image,
            "visible_on_cover": visible_on_cover,
            "has_inner_fill_violation": has_inner_fill_violation,
            "symbol_summary": sym,
        },
    }


def check_text_layout_safe(measurements: dict) -> dict:
    """
    通用排版安全检查：
      - 不允许任何块级文本元素被截断（overflow:hidden 且 scrollHeight > clientHeight）
      - 不允许 slide 最低文本元素贴底（bottomGap < 18px → 视为贴底）
      - 不允许 H1/H2 被拆成 ≥ 4 行（视为胡乱换行）
    跳过封面（slide 0）以放宽 hero 排版。
    """
    overflow_hits = []
    bottom_glued = []
    too_many_lines = []
    BOTTOM_GAP_FLOOR = 18  # px：到 slide 底部的最小空白
    HEADING_MAX_LINES = 3  # H1/H2/H3 最多 3 行
    for s in measurements.get("slides", []):
        if s.get("idx") == 0:
            continue
        tl = s.get("textLayout") or {}
        for ot in tl.get("overflowingText") or []:
            overflow_hits.append({"slide": s["idx"], **ot})
        bg = tl.get("bottomGap")
        if isinstance(bg, (int, float)) and bg < BOTTOM_GAP_FLOOR:
            bottom_glued.append({
                "slide": s["idx"],
                "bottomGap": round(bg, 2),
                "tag": tl.get("bottomTag"),
                "text": tl.get("bottomText"),
            })
        for hc in tl.get("headingLines") or []:
            if hc.get("lines", 0) > HEADING_MAX_LINES:
                too_many_lines.append({"slide": s["idx"], **hc})
    bad = bool(overflow_hits or bottom_glued or too_many_lines)
    return {
        "passed": not bad,
        "evidence": {
            "overflow_hits": overflow_hits[:8],
            "bottom_glued": bottom_glued[:8],
            "too_many_lines": too_many_lines[:8],
            "thresholds": {"bottom_gap_floor_px": BOTTOM_GAP_FLOOR, "heading_max_lines": HEADING_MAX_LINES},
        },
    }


def check_language_consistency(ds_md: str, ds_path: Path) -> dict:
    """
    Verify the DS prose is in the language declared by decisions.json.

    Looks for `decisions.json` in the brand workspace (sibling to the brand DS in
    `samples/<brand>/decisions.json`, or at the same dir as the DS markdown).
    If the declared language is non-English ("zh", "ja", "es", etc.), measure
    what fraction of the DS body is actually in that language using a simple
    character-class heuristic. If the body is dominantly English when a non-
    English language was chosen, fail — the LLM forgot the Phase 3 step 4
    translation pass.

    This is the structural safeguard that prevents the "asked for Chinese DS,
    got English DS with translated headings only" failure mode surfaced on
    Coca-Cola.
    """
    # Find decisions.json — try common locations
    candidates = [
        ds_path.parent / "decisions.json",
        ds_path.parent.parent / "samples" / ds_path.parent.name / "decisions.json",
    ]
    # Walk up to find samples/<brand>/decisions.json
    p = ds_path
    for _ in range(5):
        p = p.parent
        candidate = p / "samples" / ds_path.stem.replace("-PPT-Design-System", "") / "decisions.json"
        if candidate.exists():
            candidates.append(candidate)
            break

    decisions = None
    decisions_path = None
    for c in candidates:
        if c.exists():
            try:
                decisions = json.loads(c.read_text(encoding="utf-8"))
                decisions_path = str(c)
                break
            except Exception:
                pass

    if decisions is None:
        # No decisions.json — skip (default English DS is fine)
        return {"passed": True, "evidence": {"skipped": "no decisions.json found", "checked_paths": [str(c) for c in candidates]}}

    lang = (decisions.get("language") or "en").lower()
    if lang in ("en", "english"):
        return {"passed": True, "evidence": {"language": "en", "skipped": "English DS — no translation check needed"}}

    # Measure body language. Strip everything that legitimately stays English
    # regardless of declared language: code, comments, tokens, hex, URLs,
    # explicit kept-English markers (e.g. file names, token names in prose).
    # Also strip lines that are mostly punctuation / markdown structure
    # (table separators, ===, ---, |---|---).
    body = ds_md
    body = re.sub(r'```[a-z]*\n.*?\n```', '', body, flags=re.DOTALL)            # fenced code blocks
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)                      # HTML comments
    body = re.sub(r'`[^`\n]+`', '', body)                                        # inline code
    body = re.sub(r'--[a-z][a-z0-9-]*', '', body)                                # CSS tokens
    body = re.sub(r'#[0-9A-Fa-f]{3,8}\b', '', body)                              # hex
    body = re.sub(r'https?://\S+', '', body)                                     # URLs
    body = re.sub(r'\b\w+\.(md|html|js|css|py|sh|json)\b', '', body)              # filenames
    body = re.sub(r'\b[a-z]+(?:-[a-z]+)+\b', '', body)                            # CSS class names like type-e-row-count
    body = re.sub(r'\bType [A-K]\b', '', body)                                    # Type A/B/C/... slide-type identifiers (kept English)
    body = re.sub(r'\b\d+\s*(px|em|rem|dvh|vh|vw)\b', '', body)                   # CSS length units
    body = re.sub(r'^\s*\|.*\|\s*$', '', body, flags=re.MULTILINE)                # markdown table rows
    body = re.sub(r'^\s*[-=]{3,}\s*$', '', body, flags=re.MULTILINE)              # horizontal rules
    body = re.sub(r'^\s*\d+\.\s*$', '', body, flags=re.MULTILINE)                 # bare list numbers

    cjk_count = sum(1 for ch in body if '一' <= ch <= '鿿' or '぀' <= ch <= 'ゟ' or '゠' <= ch <= 'ヿ')
    latin_count = sum(1 for ch in body if 'a' <= ch.lower() <= 'z')

    # Threshold rationale: a Chinese-language DS still contains substantial English
    # (CSS code blocks, token names, hex values, HTML comments, file paths). The
    # check distinguishes "fully Chinese prose with English code" (~ ratio 0.2-0.5)
    # from "all-English with translated chapter titles only" (~ ratio < 0.05).
    # Threshold rationale: detect "translation pass actually happened" not
    # "perfect translation density". A DS template has ~30% prose, ~70% code/CSS;
    # even fully translated, ratios stay around 0.1-0.3 because the canonical
    # English body around code blocks is structurally unavoidable. The "all-
    # English with translated chapter titles only" failure mode shows ratio
    # < 0.02. Threshold 1000 CJK chars + ratio 0.04 cleanly catches that.
    expectations = {
        "zh": ("CJK prose translation done (chapter titles + body paragraphs)",
               cjk_count, latin_count,
               lambda c, l: c >= 1000 and c >= l * 0.04),
        "ja": ("CJK + kana translation done",
               cjk_count, latin_count,
               lambda c, l: c >= 1000 and c >= l * 0.04),
        "es": ("Spanish prose has many ñ/á/é/í/ó/ú", None, None, None),  # fallback
    }
    if lang not in expectations:
        return {"passed": True, "evidence": {"language": lang, "skipped": "language not yet checkable"}}

    desc, c, l, ok_fn = expectations[lang]
    if ok_fn is None:
        return {"passed": True, "evidence": {"language": lang, "skipped": "no rule defined"}}

    passed = ok_fn(c, l)
    return {
        "passed": passed,
        "evidence": {
            "language": lang,
            "decisions_path": decisions_path,
            "rule": f"{desc}; need cjk_count > latin_count * 0.5",
            "cjk_chars": c,
            "latin_chars": l,
            "ratio": round(c / max(l, 1), 2),
            "verdict": "PASS — body prose is in declared language" if passed else "FAIL — DS body is mostly English but decisions.json declares non-English language. The Phase 3 step 4 translation pass was incomplete.",
        },
    }


def check_ds_engineering_dna(ds_md: str) -> dict:
    """
    Check that the DS markdown carries every required engineering-DNA chapter
    by stable ID anchor — not by English prose phrase. This makes the check
    language-agnostic: a Chinese DS can fully translate chapter titles and
    narration as long as the `<!-- ENGINEERING-DNA: <id> -->` HTML comments
    stay as-is. The IDs are the universal identifiers; the prose around them
    adapts to the user's chosen language.
    """
    required_ids = [
        "design-taste",
        "typography-safety",
        "typography-floor",
        "scale-to-fit",
        "fit-contract",
        "three-layer-overflow",
        "inline-flex-trap",
        "flip-card-mobile",
        "pre-ship-checklist",
    ]
    missing = [i for i in required_ids if f"<!-- ENGINEERING-DNA: {i} -->" not in ds_md]
    return {"passed": len(missing) == 0, "evidence": {"missing_ids": missing, "checked": required_ids}}


# Family names that count as "real CJK fonts" — i.e. characterful, not the system default fallback.
# When a zh deck's body font-family resolves to one of these on the first CJK glyph, the CJK rendering
# is high-quality. If it falls through to system-ui / Helvetica / generic sans, the CJK glyphs render
# with the OS thin-default (STHeiti on macOS, Microsoft YaHei UI Light on Windows, Noto Sans Thin on
# Linux) — visually cheap and what the cjk-fallback engineering-DNA chapter exists to prevent.
_CJK_FONT_NAMES = [
    "PingFang SC", "PingFang TC", "苹方-简", "苹方",
    "Hiragino Sans GB", "冬青黑体简体中文", "Hiragino Kaku Gothic", "ヒラギノ角ゴ",
    "Microsoft YaHei", "微软雅黑", "Microsoft JhengHei",
    "Source Han Sans", "Source Han Sans SC", "Source Han Sans CN", "Source Han Serif",
    "Noto Sans SC", "Noto Sans CJK", "Noto Sans CJK SC", "Noto Serif SC", "Noto Serif CJK",
    "Songti SC", "宋体-简", "STSong", "Heiti SC", "黑体-简",
]


def _font_family_first_real(fam_str: str) -> str:
    """Strip quotes/spaces, return the first non-generic family name."""
    GENERIC = {"sans-serif", "serif", "monospace", "system-ui", "-apple-system", "blinkmacsystemfont"}
    for raw in (fam_str or "").split(","):
        name = raw.strip().strip("'\"").lower()
        if not name or name in GENERIC:
            continue
        return name
    return ""


def check_cjk_font_quality(ds_path: Path, desktop: dict, deck_path: Path = None) -> dict:
    """
    Verify a zh deck has *some* CJK font in its body font-family chain, so CJK glyphs
    don't fall through to the OS thin-default (STHeiti on macOS, YaHei UI Light on Windows).

    Active only when the run's decisions.json declares language=zh. en decks pass trivially.

    SOFT rule on purpose:
    - PASS: body font-family contains at least one real CJK font name from _CJK_FONT_NAMES.
    - FAIL: zero CJK fonts anywhere in the chain — that's an absolute bug, CJK chars will
            render with the OS default and look cheap.
    - When CJK fonts ARE present but a Latin brand font sits first, this is a stylistic
      choice (an English-heavy deck may legitimately put SF Pro / Helvetica first to keep
      Latin glyphs in the brand voice). We surface it as a `warning` field but still PASS.
      Vision judge can then decide whether the rendering looks good.

    Failure routes the agent to DS §3 'CJK 字体回退链' chapter. The fix is in the DS
    (and propagated into the deck's body font-family rule), not in the deck alone.
    """
    # Locate decisions.json near the DS file (sibling samples/<brand>/decisions.json or workspace)
    decisions = None
    for cand in [
        ds_path.parent / "decisions.json",
        ds_path.parent.parent / "samples" / ds_path.stem.replace("-PPT-Design-System", "") / "decisions.json",
        Path("/Users/seacen/Development/Projects/deckify/samples") / ds_path.stem.replace("-PPT-Design-System", "") / "decisions.json",
    ]:
        if cand.exists():
            try:
                decisions = json.loads(cand.read_text())
                break
            except Exception:
                pass
    lang = (decisions or {}).get("language", "").lower() if decisions else ""
    # Fallback 1: deck html `<html lang>` attr
    if not lang and deck_path and deck_path.exists():
        m = re.search(r'<html[^>]+lang=["\']([^"\']+)["\']', deck_path.read_text(encoding="utf-8")[:1000])
        if m:
            lang = m.group(1).lower()
    # Fallback 2: DS markdown CJK density (already computed in language_consistency, but recompute cheaply)
    if not lang and ds_path.exists():
        ds = ds_path.read_text(encoding="utf-8")
        cjk = len(re.findall(r"[一-鿿]", ds))
        if cjk >= 1000:
            lang = "zh"

    if lang not in ("zh", "zh-cn", "zh-hans", "中文", "chinese", "simplified chinese"):
        return {"passed": True, "evidence": {"skipped": True, "reason": f"language is not zh (detected: {lang!r}) — CJK font check N/A"}}

    body_fam = (desktop.get("body") or {}).get("fontFamily", "") or ""
    cjk_sample = desktop.get("cjkSample")
    cjk_fam = (cjk_sample or {}).get("fontFamily", "") or ""

    cjk_lower = [n.lower() for n in _CJK_FONT_NAMES]

    def first_real_is_cjk(fam_str):
        first = _font_family_first_real(fam_str)
        return first in cjk_lower, first

    body_ok, body_first = first_real_is_cjk(body_fam)
    cjk_ok, cjk_first = (True, "") if not cjk_sample else first_real_is_cjk(cjk_fam)

    body_has_cjk_anywhere = any(n in body_fam.lower() for n in cjk_lower)

    # Hard pass: at least one CJK family must be in the chain. Order is a soft warning.
    passed = body_has_cjk_anywhere
    warning = None
    if passed and not (body_ok and cjk_ok):
        warning = ("CJK font is present but a Latin family is listed first. "
                   f"body first real: {body_first!r}; CJK sample first real: {cjk_first!r}. "
                   "If your zh deck looks visually thin or cheap on CJK glyphs, move the CJK "
                   "family to the front of the chain (DS §3 CJK 字体回退链). If the deck is "
                   "mostly English with occasional CJK, the current order may be intentional.")
    return {
        "passed": passed,
        "evidence": {
            "language": lang,
            "body_font_family": body_fam,
            "body_first_real": body_first,
            "body_has_cjk_anywhere": body_has_cjk_anywhere,
            "cjk_sample": cjk_sample,
            "cjk_first_real": cjk_first,
            "warning": warning,
            "rule": "zh deck must have at least one CJK font (PingFang SC / Hiragino Sans GB / Microsoft YaHei / Source Han Sans / etc.) somewhere in body font-family. CJK-first ordering is recommended but not required.",
            "fix_location": "DS §3 CJK 字体回退链 — add a CJK family to the font-family chain",
        },
    }


# ── orchestration ──────────────────────────────────────────────────────────

def run_all(deck_path: Path, ds_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    html = deck_path.read_text(encoding="utf-8")
    ds_md = ds_path.read_text(encoding="utf-8") if ds_path.exists() else ""

    print(f"[1/2] desktop measure {deck_path.name}")
    desktop = measure_desktop(deck_path, out_dir)
    print(f"[2/2] mobile measure {deck_path.name}")
    mobile = measure_mobile(deck_path, out_dir)

    (out_dir / "measurements.json").write_text(
        json.dumps({"desktop": desktop, "mobile": mobile}, indent=2, ensure_ascii=False)
    )

    checks = {
        "slide_dimensions":         check_slide_dimensions(desktop),
        "fit_contract_intact":      check_fit_contract(desktop),
        "token_only_colors":        check_token_only_colors(html),
        "no_emoji":                 check_no_emoji(html),
        "mobile_collapse":          check_mobile_collapse(mobile),
        "logo_renders":             check_logo_renders(desktop),
        "language_consistency":     check_language_consistency(ds_md, ds_path),
        "text_layout_safe":         check_text_layout_safe(desktop),
        "ds_has_engineering_dna":   check_ds_engineering_dna(ds_md),
        "cjk_font_quality":         check_cjk_font_quality(ds_path, desktop, deck_path),
    }
    (out_dir / "hard_checks.json").write_text(json.dumps(checks, indent=2, ensure_ascii=False))
    return checks


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: hard_checks.py <deck.html> <ds.md> <out_dir>", file=sys.stderr)
        sys.exit(2)
    deck, ds, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    res = run_all(deck, ds, out)
    n_pass = sum(1 for v in res.values() if v["passed"])
    print(f"\n{n_pass}/{len(res)} hard checks passed")
    for k, v in res.items():
        print(f"  {'✓' if v['passed'] else '✗'} {k}")
