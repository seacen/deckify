"""
Unit tests for scripts/extract_brand.py — pure-stdlib, no network.

Run: python3 -m unittest tests.test_extract_brand -v
   (from the skill root, with PYTHONPATH=. or with the script alongside)

These tests are the "structurally impossible to recur" layer for the
deterministic extractor. Per the skillify article (step 3): unit tests catch
the small/boring/critical bugs in pure functions before they propagate into
the LLM layer where they're 100x harder to diagnose.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Make scripts/ importable regardless of where the test is invoked from.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

import extract_brand as eb  # noqa: E402


class TestColorPrimitives(unittest.TestCase):
    def test_normalize_hex_long(self):
        m = eb.HEX_RE.match("#aAbBcC")
        self.assertEqual(eb._normalize_hex(m), "aabbcc")

    def test_normalize_hex_short(self):
        m = eb.HEX_RE.match("#aBc")
        self.assertEqual(eb._normalize_hex(m), "aabbcc")

    def test_rgb_to_hex_clamped(self):
        # CSS doesn't allow negatives in rgb(), so test the clamping with an
        # over-255 value (which spec-non-compliant CSS does occasionally produce)
        m = eb.RGB_RE.match("rgb(300, 0, 128)")
        self.assertEqual(eb._rgb_to_hex(m), "ff0080")

    def test_rgba_ignores_alpha(self):
        m = eb.RGB_RE.match("rgba(7, 0, 90, 0.8)")
        self.assertEqual(eb._rgb_to_hex(m), "07005a")

    def test_is_neutral_white(self):
        self.assertTrue(eb._is_neutral("ffffff"))
        self.assertTrue(eb._is_neutral("fafaf8"))

    def test_is_neutral_black(self):
        self.assertTrue(eb._is_neutral("000000"))
        self.assertTrue(eb._is_neutral("0c0c1e"))

    def test_is_neutral_pure_gray(self):
        self.assertTrue(eb._is_neutral("808080"))
        self.assertTrue(eb._is_neutral("606078"))   # a desaturated gray-purple — should be neutral

    def test_is_neutral_brand_navy(self):
        self.assertFalse(eb._is_neutral("07005a"))   # a saturated dark blue-purple — should NOT be neutral
        self.assertFalse(eb._is_neutral("1a1ae6"))   # a saturated electric blue — should NOT be neutral

    def test_is_neutral_red_green(self):
        self.assertFalse(eb._is_neutral("8b1a1a"))   # red brand
        self.assertFalse(eb._is_neutral("005c45"))   # green brand


class TestColorStringHelper(unittest.TestCase):
    def test_color_str_to_hex_rgb(self):
        self.assertEqual(eb._color_str_to_hex("rgb(7, 0, 90)"), "07005a")

    def test_color_str_to_hex_rgba(self):
        self.assertEqual(eb._color_str_to_hex("rgba(7, 0, 90, 0.5)"), "07005a")

    def test_color_str_to_hex_hex_long(self):
        self.assertEqual(eb._color_str_to_hex("#07005A"), "07005a")

    def test_color_str_to_hex_hex_short(self):
        self.assertEqual(eb._color_str_to_hex("#abc"), "aabbcc")

    def test_color_str_to_hex_invalid(self):
        self.assertIsNone(eb._color_str_to_hex("not-a-color"))
        self.assertIsNone(eb._color_str_to_hex(""))
        self.assertIsNone(eb._color_str_to_hex(None))   # type: ignore


class TestFontExtraction(unittest.TestCase):
    def test_clean_family_strips_quotes(self):
        self.assertEqual(eb._clean_family("'Barlow', 'PingFang SC', sans-serif"),
                         ["Barlow", "PingFang SC"])

    def test_clean_family_skips_generics(self):
        self.assertEqual(eb._clean_family("system-ui, -apple-system, sans-serif"), [])

    def test_clean_family_handles_double_quotes(self):
        self.assertEqual(eb._clean_family('"Inter", Arial'), ["Inter", "Arial"])

    def test_extract_fonts_from_css(self):
        css = '''
            body { font-family: 'Inter', sans-serif; }
            h1 { font-family: 'Inter', system-ui; }
            .meta { font-family: 'Barlow', monospace; }
        '''
        results = dict(eb.extract_fonts(css))
        self.assertIn("Inter", results)
        self.assertEqual(results["Inter"], 2)
        self.assertIn("Barlow", results)

    def test_extract_fonts_google_fonts_link_is_weighted(self):
        html = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700&display=swap">'
        results = dict(eb.extract_fonts(html))
        self.assertIn("Manrope", results)
        # Google Fonts hits weight 5 in extract_fonts → strongly preferred
        self.assertGreaterEqual(results["Manrope"], 5)


class TestColorExtraction(unittest.TestCase):
    def test_extract_colors_counts_occurrences(self):
        css = """
            :root { --navy: #07005A; --blue: #1A1AE6; }
            .btn { background: #1A1AE6; color: #FFFFFF; }
            .nav { background-color: rgb(7, 0, 90); }
        """
        c = eb.extract_colors(css)
        self.assertEqual(c["07005a"], 2)   # one #07005A + one rgb(7,0,90)
        self.assertEqual(c["1a1ae6"], 2)
        self.assertEqual(c["ffffff"], 1)

    def test_extract_colors_handles_short_hex(self):
        c = eb.extract_colors("color: #abc; background: #ABC;")
        self.assertEqual(c["aabbcc"], 2)


class TestMetaParsing(unittest.TestCase):
    def test_parses_title_and_og_image(self):
        html = """
        <html>
          <head>
            <title>Acme — premium widgets</title>
            <meta property="og:image" content="https://acme.example/og.png">
            <link rel="icon" href="/favicon.svg">
          </head>
          <body><header><svg viewBox="0 0 100 20"><path d="M10 10"/></svg></header></body>
        </html>
        """
        meta = eb.parse_meta(html)
        self.assertEqual(meta.title.strip(), "Acme — premium widgets")
        self.assertEqual(meta.og_image, "https://acme.example/og.png")
        self.assertEqual(meta.favicon, "/favicon.svg")
        self.assertEqual(len(meta.header_svg_inline), 1)

    def test_handles_apple_touch_icon(self):
        html = '<link rel="apple-touch-icon" href="/apple.png">'
        meta = eb.parse_meta(html)
        self.assertEqual(meta.apple_touch, "/apple.png")


class TestLogoCandidateRanking(unittest.TestCase):
    def test_inline_svg_ranks_first(self):
        html = """
        <head>
          <link rel="icon" href="/favicon.svg">
          <meta property="og:image" content="/og.png">
        </head>
        <body><header><svg viewBox="0 0 1 1"><path/></svg></header></body>
        """
        meta = eb.parse_meta(html)
        candidates = eb.rank_logo_candidates(meta, "https://acme.example")
        kinds = [c["kind"] for c in candidates]
        self.assertEqual(kinds[0], "inline-svg")
        self.assertIn("link-icon", kinds)
        self.assertIn("og-image", kinds)
        self.assertTrue(any(k == "path-guess" for k in kinds))

    def test_absolutize_handles_relative(self):
        self.assertEqual(eb._absolutize("/logo.svg", "https://acme.example/about"),
                         "https://acme.example/logo.svg")

    def test_absolutize_passes_through_absolute(self):
        self.assertEqual(eb._absolutize("https://cdn.acme.example/logo.svg", "https://acme.example"),
                         "https://cdn.acme.example/logo.svg")

    def test_absolutize_passes_through_data_uri(self):
        data = "data:image/svg+xml;base64,PHN2Zz4="
        self.assertEqual(eb._absolutize(data, "https://acme.example"), data)


class TestComputedSignalMerge(unittest.TestCase):
    def test_promotes_root_color_vars(self):
        out = {"logo_candidates": []}
        computed = {
            "rootVars": {
                "--brand-primary": "#07005A",
                "--brand-accent":  "rgb(26, 26, 230)",
                "--spacing-md":    "16px",   # not a color, skipped from color_vars
            },
            "computed": {"body": {"font-family": "'Barlow', sans-serif"}},
            "meta": {},
        }
        eb.merge_computed_signal(out, computed)
        cs = out["computed_signal"]
        self.assertIn("--brand-primary", cs["root_color_vars"])
        self.assertEqual(cs["root_color_vars"]["--brand-primary"], "#07005A")
        self.assertEqual(cs["root_color_vars"]["--brand-accent"], "#1A1AE6")
        self.assertNotIn("--spacing-md", cs["root_color_vars"])
        self.assertEqual(cs["primary_fonts"], ["Barlow"])

    def test_promotes_header_inline_svgs_first(self):
        out = {"logo_candidates": [{"kind": "favicon", "rank": 1}]}
        computed = {
            "meta": {
                "headerSvgInline": [
                    "<svg viewBox='0 0 1 1'><path/></svg>",
                ]
            }
        }
        eb.merge_computed_signal(out, computed)
        # Header inline-svg-computed should now be candidate[0]
        self.assertEqual(out["logo_candidates"][0]["kind"], "inline-svg-computed")
        self.assertEqual(out["logo_candidates"][0]["rank"], -1)

    def test_handles_missing_computed(self):
        out = {"logo_candidates": []}
        eb.merge_computed_signal(out, {})
        self.assertIsNone(out["computed_signal"])


class TestFullPipeline(unittest.TestCase):
    """Integration-flavored: feeds a synthetic recon dir to main()."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        recon = Path(self.tmp) / "recon"
        recon.mkdir()
        (recon / "index.html").write_text("""
            <html>
              <head>
                <title>Acme</title>
                <link rel="icon" href="/favicon.svg">
                <meta property="og:image" content="/og.png">
                <style>
                  :root { --brand: #07005A; --accent: #1A1AE6; }
                  body { font-family: 'Inter', sans-serif; background: #FAFAF8; }
                  .btn { background: #1A1AE6; color: #fff; }
                </style>
              </head>
              <body>
                <header><svg viewBox="0 0 100 20"><path d="M10 10 L20 20"/></svg></header>
              </body>
            </html>
        """, encoding="utf-8")
        (recon / "computed.json").write_text(json.dumps({
            "rootVars": {"--brand-primary": "#07005A", "--brand-accent": "#1A1AE6"},
            "computed": {"body": {"font-family": "'Inter', sans-serif", "background-color": "rgb(250, 250, 248)"}},
            "meta": {"title": "Acme", "host": "acme.example"},
        }), encoding="utf-8")

    def test_main_writes_brand_recon(self):
        rc = eb.main(self.tmp)
        self.assertEqual(rc, 0)
        out_path = Path(self.tmp) / "brand-recon.json"
        self.assertTrue(out_path.exists())
        out = json.loads(out_path.read_text())
        self.assertEqual(out["title"], "Acme")
        # Brand candidates should include the navy and the blue, NOT the off-white
        brand_hexes = {c["hex"] for c in out["colors"]["brand_candidates"]}
        self.assertIn("#07005A", brand_hexes)
        self.assertIn("#1A1AE6", brand_hexes)
        # Off-white is neutral
        neutral_hexes = {c["hex"] for c in out["colors"]["neutral_candidates"]}
        self.assertIn("#FAFAF8", neutral_hexes)
        # Computed signal merged in
        self.assertIsNotNone(out["computed_signal"])
        self.assertIn("--brand-primary", out["computed_signal"]["root_color_vars"])
        # Logo candidates: the computed inline-svg-computed (if any was set) +
        # the HTML-parsed inline-svg + favicon + og-image + path-guesses
        kinds = [c["kind"] for c in out["logo_candidates"]]
        self.assertIn("inline-svg", kinds)
        self.assertIn("link-icon", kinds)


if __name__ == "__main__":
    unittest.main()
