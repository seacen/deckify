# Phase 1d guideline — synthesize brand from raw assets

You are running the `deckify` skill. Phase 1c (`enumerate_assets.py`) has produced `$WS/raw-assets.json`, an exhaustive enumeration of every brand-asset candidate scraped from all fetched pages. Each candidate has a stable `id`. Phase 1b also saved screenshots at `$WS/recon/pages/<slug>/shot.png`.

Your job: read `raw-assets.json`, **look at the screenshots with your host's image-viewing capability** (the `Read` tool in Claude Code, equivalents in Codex / OpenClaw, or your own image loader if scripted), and produce `$WS/brand.json` — a synthesized, opinionated brand profile that the deck generator can use directly.

You are choosing real things from real evidence. You are not allowed to invent.

---

## Design taste — read this before anything else

**Commit to a bold aesthetic direction, not a safe average.** The brand recon gives you everything you need to recognise the brand's actual visual register; your job is to capture that register with conviction, not to soften it into a generic "clean modern corporate" mush.

Useful aesthetic directions to pick from (and remix): brutally minimal, maximalist, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, geometric/art-deco, soft/pastel, industrial/utilitarian, archival/serious, optimistic/scientific, monochrome/typographic. Pick the one (or two) that the screenshots actually support, and execute precisely. Both bold maximalism and refined minimalism work — the failure mode is timidity.

### Anti-AI-slop guardrails

When the recon gives you a real choice, **never** default to:

- **Generic fonts** as the "design choice": Inter, Roboto, Arial, "system-ui", Helvetica Neue, Source Sans, Open Sans. If the brand's `font-face` declares a real custom face (e.g. UnileverDesire, Stripe Sans, Inter for Stripe IS a deliberate brand choice — but Inter on a luxury skincare brand is slop), use it. If only system fonts are present, pick the *most* characterful fallback in the chain (Georgia / Charter / Iowan over generic; Avenir / Inter / Söhne over Arial), name the trade-off in `evidence`.
- **Cliché palettes**: pure-white background + a single purple/blue accent + slate-grey type is the AI-slop signature. If the brand's actual palette has warm earth tones, brand-saturated accents, or unexpected neutrals (warm stone, cool fog, off-white papers), capture them — do not flatten to white + grey + one accent.
- **Even-weighted multi-accent palettes**: 6 equal-weight accent colours look like a Storybook colour grid, not a brand. **One dominant chord (the brand's signature)**, plus 2-3 supporting accents that carry distinct meaning (semantic / categorical), is almost always the right shape.
- **Default radii / shadow / spacing**: 8 px radius + soft shadow + comfortable spacing on every brand makes them all look like SaaS dashboards. Match the recon: if the brand's CTAs are sharp 0-radius rectangles, capture that. If the body text breathes at 1.7 line-height, capture that.
- **Three SaaS adjectives in `mood`**: "modern, clean, bold" describes everything and therefore nothing. Use specific, vivid 2-3 word combinations: `editorial sustainability gravitas`, `clinical scientific optimism`, `industrial workhorse confidence`, `studio luxury restraint`.

### What "bold commitment" actually means in `brand.json`

- **Mood line is the thesis**: every other field should be downstream of it. If your `mood` is "editorial sustainability gravitas", your palette better not be a SaaS purple gradient. If your `mood` is "playful warmth", your spacing better not be tight clinical 4 px gaps.
- **Style keywords are sharp, not generic**: `humanist`, `archival`, `loud`, `quiet`, `saturated`, `washed-out`, `editorial`, `engineered`, `botanical`, `tactile`, `hairline`, `weighty`. Avoid `clean`, `modern`, `professional`, `bold`, `minimalist` — they're so overused they communicate no constraint.
- **Precedents help downstream**: name 2-3 real reference points the deck generator can mentally calibrate against ("Patagonia annual reports", "old IBM brochures", "Bauhaus posters", "modernist Swiss editorial"). Skip if you can't name one with conviction.

The deck generator downstream uses `brand.json` as its design brief. A timid brief produces a timid deck. A vivid brief produces a memorable one.

---

## What to write into brand.json

```jsonc
{
  "host": "<copy from raw-assets.host>",
  "brand_name": "<the actual brand name as people say it>",
  "base_url": "https://<host>/",

  // chosen_logo has two legal forms — pick whichever fits your evidence:
  //
  // Form A (default) — point at a candidate id from raw-assets.json:
  //   "chosen_logo": { "id": "<8-char id>", "why": "..." }
  //
  // Form B (escape hatch) — point at an authoritative URL directly. Use this
  // when the LLM identified a canonical asset (typically the JSON-LD
  // Organization.logo) that enumerate_assets.py didn't surface as a discrete
  // candidate id (e.g. it got bucketed into jsonld_logos as ListItem.image
  // along with product photos). See "Direct-URL escape hatch" section below
  // for full criteria.
  //   "chosen_logo": {
  //     "id": "<stable-name-you-chose>",     // any stable string; not looked up in raw-assets
  //     "kind": "jsonld-logo" | "img" | "icon-link",
  //     "url": "https://...",
  //     "why": "..."
  //   }
  "chosen_logo": {
    "id": "<id of the candidate from raw-assets.logo_candidates, OR a stable name when using direct-URL form>",
    "why": "<1-2 sentences of evidence: where you saw it, why it's the real wordmark>"
  },

  "alt_logo_ids": ["<2-3 backup ids in case the chosen one fails the quality gate>"],

  "palette": {
    "brand_primary":   { "hex": "#RRGGBB", "name": "<token name>", "evidence": "<source>" },
    "brand_secondary": { "hex": "#RRGGBB", "name": "<token name>", "evidence": "<source>" },
    "ink":             { "hex": "#RRGGBB", "name": "<token name>", "evidence": "<source>" },
    "paper":           { "hex": "#RRGGBB", "name": "<token name>", "evidence": "<source>" },
    "accents":         [{ "hex": "#RRGGBB", "name": "<token>", "evidence": "..." }, …]
  },

  "typography": {
    "display_font": { "family": "<font>", "evidence": "<source>" },
    "body_font":    { "family": "<font>", "evidence": "<source>" },
    "mono_font":    { "family": "<font>", "evidence": "<source>" }   // optional
  },

  "spacing_radius_shadow": {
    "radius_style":  "<sharp | softly-rounded (4-8px) | pill (≥16px)>",
    "shadow_style":  "<flat | subtle | dramatic>",
    "spacing_density": "<tight | comfortable | airy>",
    "evidence": "<which surfaces in raw-assets.computed_palette informed this>"
  },

  "aesthetic": {
    "mood": "<2-3 words, e.g. 'corporate gravitas', 'playful clarity', 'editorial restraint'>",
    "style_keywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
    "precedents": ["<brands or design references this reminds you of>"],
    "voice_register": "<formal | conversational | technical | aspirational | etc.>"
  },

  "evidence_screenshots": ["recon/pages/index/shot.png", "recon/pages/about/shot.png"]
}
```

## How to actually pick

### Choosing the real wordmark (most important decision)

Look at the screenshots. Find where you actually see the brand identity element on the rendered page. Then trace that back to a candidate id.

Heuristics to apply, **in combination, not strictly**:

- A **real wordmark** usually appears in the `<header>` and/or `<footer>` of every page on the site
- It's visually distinct enough that someone could identify the company from it alone (a generic disc with a letter is *not* — that's a placeholder)
- For SVG candidates: real wordmarks tend to have **several `<path>` elements with substantial `d` strings** (the wordmark's letterforms). A `pathCount: 0` SVG containing only `<text>` is a rendered fallback, not the wordmark.
- **Utility icons** (search, menu, arrow, close, share, social) typically have:
  - Small `viewBox` (≤ 32px in either dimension)
  - 1-3 simple paths
  - aria-label like "search", "menu", "close"
  - A single decorative purpose
  Skip these.
- **JSON-LD `logo` fields** are often the official URL the brand wants you to use — strong signal. Check `kind: "jsonld-logo"` candidates.
- **`<link rel="apple-touch-icon">`** at 180×180 is usually a clean PNG of the brand mark — a fine fallback if SVGs are all utility icons.
- **`<img>` with `alt` containing "logo"** or class names containing `logo` are explicit candidates.
- **Screenshots are the truth check.** If the candidate you're considering doesn't visually match what you see in `shot.png`'s header, it's wrong.

If multiple candidates pass these tests, prefer (in order):
1. **Nav-region single-path SVG with square-ish viewBox (aspect ratio between 0.8 and 1.3) that visually matches the silhouette in the screenshot.** Most iconic brand marks (Apple silhouette, Twitter X, Nike swoosh, Mercedes star) are 1-path roughly-square SVG icons sitting in the global nav. This is the gold-standard match.
2. **`<link rel="apple-touch-icon">` PNG (180×180)** — usually RGBA with the brand mark on transparent background. Currentcolor-style flipping doesn't work on rasters, but the alpha channel makes it composite cleanly on dark and light backgrounds without visible squares.
3. **Single-path or few-path SVG anywhere on the page** — even if not in nav. Vector + currentColor-flippable = clean white-on-dark / brand-on-light.
4. **SVG over raster** (resolution-independent).
5. **`<img>` with `class*="logo"` or `alt*="logo"` in nav or footer** — explicit semantic signal.
6. **JSON-LD `logo` URL** — strong semantic signal but BEWARE: many JSON-LD logos are RGB-only PNGs without alpha channel (see RGB-only PNG warning below). Use only as a fallback when no SVG / apple-touch-icon candidate works.
7. **Footer logo, higher `maxPathDLen`** — last resort tiebreaker.

If nothing passes — if every SVG is a utility icon and every img is decorative — populate `chosen_logo.id` with the best of a bad lot, **set `alt_logo_ids` to `[]`, and add a `note` field explaining the situation**. The skill's caller can then ask the user for a logo file.

### Direct-URL escape hatch <!-- surfaced from Tiffany end-to-end test -->

`enumerate_assets.py` aggregates JSON-LD `logo` fields into the `jsonld_logos` list, but it doesn't distinguish an `Organization.logo` from product images embedded in `ItemList`/`ListItem` blocks (which also use the `logo`/`image` schema field on big e-commerce sites). The result: on a luxury / e-commerce site (Tiffany, P&G, fashion houses) the canonical logo URL declared in JSON-LD `Organization.logo` may have *no* discrete candidate id in `raw-assets.json` — its bytes were scooped into `jsonld_logos` alongside dozens of product photos.

When this happens AND the JSON-LD URL is clearly authoritative (the brand declares it in `@type: "Corporation"` or `@type: "Organization"` blocks on every page, and visually matches the rendered wordmark in `shot.png`), use the **direct-URL escape hatch** in `chosen_logo`:

```jsonc
{
  "chosen_logo": {
    "id": "jsonld-tiffany-logo-svg",   // any stable name — for documentation/audit only
    "kind": "jsonld-logo",             // tells embed_logo.py which materialization path to use
    "url": "https://www.tiffany.com/.../logo.svg",
    "why": "Official Schema.org Organization.logo from JSON-LD on every page; vector wordmark, currentColor-flippable, matches the visible 'TIFFANY & CO.' in every shot.png header."
  },
  "alt_logo_ids": ["press-newsroom-logo-png", "..."]   // alt_logo_sources is encouraged here too
}
```

**When to use the escape hatch:**
- ✓ The site declares an `Organization.logo` URL in JSON-LD on every page, AND
- ✓ The URL passes the visual sanity check (you can fetch it in a browser tab and see it matches the rendered wordmark), AND
- ✓ `raw-assets.json` does NOT contain that URL as a `logo_candidates[].src` (otherwise just use the candidate id).

**When NOT to use it:**
- ✗ JSON-LD `logo` is missing, contradictory, or RGB-only PNG that won't currentColor-flip cleanly (use `alt_logo_ids` candidates instead).
- ✗ You're tempted to invent a URL ("tiffany.com/logo.svg") not actually declared anywhere — never invent.

`embed_logo.py` will quality-gate the URL the same as a candidate (SVG `<path d>` ≥ 40 chars OR `<image>` child OR raster ≥ 64×64). If it fails, swap to `alt_logo_ids` and try again — same fallback chain as Form A.

### Disambiguating wordmark glyphs vs icon silhouettes vs Lottie animations <!-- surfaced from Apple end-to-end test -->

Big brands sometimes have 100+ SVG candidates in the recon. Three failure patterns that all pass the basic d-string-length quality gate but produce a wrong "logo" downstream:

- **Wordmark glyphs**: A `<svg>` in nav with viewBox like `60×25` or `67×44` containing one path whose `d` traces letterforms ("Stripe" / "Apple" wordmark / etc.). Width-to-height ratio is wide (≥ 1.4:1), and the path data, when scanned, contains many cubic-bezier curves arranged in the patterns of typeset characters. **Distinguish**: if the brand's actual visible mark on the screenshot is an icon (Apple silhouette, P&G monogram), and the SVG candidate has wide-aspect viewBox, it's likely a wordmark glyph — not the icon. Cross-check by reading the screenshot of the page where the SVG appears.
- **Lottie animation composites**: A `<svg>` with viewBox like `670×670`, `<defs>`, `<clipPath>`, `transform: translate3d`, multiple paths. These are scrubbed Lottie illustrations, not static logos. **Distinguish**: the presence of `<defs>` / `<clipPath>` / inline `style=` with transform-3d patterns indicates animation. Skip.
- **Decorative section headings**: A `<svg>` with `class*="logo"` may not actually be the brand mark — sometimes it's a decorative section heading rendered as SVG. Cross-check against the screenshot of the page header.

When in doubt, prefer a small simple nav SVG (1 path, square-ish or near-square viewBox) over a fancy logo-class SVG. The iconic mark is usually the simplest one.

### RGB-only PNG warning <!-- ENGINEERING-DNA — surfaced from Apple end-to-end test -->

Some brands' JSON-LD `logo` URLs return PNG without an alpha channel (RGB only). The PNG renders as a coloured silhouette on a coloured background — and `filter: invert()` or `filter: brightness(0)` on the outer SVG will flip BOTH the silhouette AND its background, producing a visible bright square on the cover. This breaks the `currentColor` flip pattern.

**If the JSON-LD logo is your only candidate**: check `embed_logo.py`'s output for the PNG colour mode (RGBA = ✓, RGB = ⚠). For an RGB-only PNG candidate, prefer ANY single-path SVG (even a wordmark glyph) over the PNG — the SVG will at least flip cleanly. Document this trade-off in `chosen_logo.why`.

In Apple's case specifically, the JSON-LD `knowledge_graph_logo.png` is RGB-only — produces a visible white square on the dark cover. A `<link rel="apple-touch-icon">` PNG (when present) is usually RGBA and works cleanly.

### Picking the palette

Three sources to triangulate:

1. **`root_vars`** in raw-assets — if the site has CSS custom properties named `--brand-blue`, `--primary`, etc., that IS their token system. Use those names if reasonable.
2. **`computed_palette`** — actual painted colors of body/header/buttons/CTAs. The CTA color is almost always brand-primary. Header backgrounds reveal the dominant chrome.
3. **`color_frequency`** — purely literal counting from CSS text. Lower trust than the above (it picks up disabled-state grays, hover colors, etc.) but useful as a tiebreaker.

Skim screenshots: does the dominant brand color match what you're picking? If not, pick what you see.

A good palette is **3-6 colors**: primary, optional secondary, ink (near-black for text), paper (near-white for surfaces), 1-3 accents. Don't dump 20 colors into accents.

### Picking typography

`fonts.computed_primary` (body's actual font) and `fonts.computed_heading` (h1's actual font) are usually the answer. If those are generic system fonts but `fonts.frequencies` shows a clear high-count custom font (often a Google Font or self-hosted woff2), that custom font is probably the display face.

`fonts.font_face_srcs` reveals self-hosted webfonts — they're declared because they're used.

### Recording aesthetic

Look at the screenshots. Two or three words. Examples of useful mood vocab: `corporate gravitas`, `clinical precision`, `playful warmth`, `editorial restraint`, `industrial confidence`, `optimistic energy`, `studio minimalism`, `enterprise neutrality`. Avoid SaaS clichés like "modern, clean, bold" — they describe everything and therefore nothing.

Precedents help downstream: "evokes Stripe + Apple", "feels like an old IBM brochure", "Bauhaus-leaning"…

### Provenance

Every choice should cite evidence. The `evidence` fields aren't ceremony — they're so the deck generator can show the user *why* this color or font was picked, and so a future audit can validate.

## After writing brand.json

Run `python3 scripts/embed_logo.py $WS` to materialize the chosen logo (download/quality-gate/base64-embed). If that exits non-zero, swap `chosen_logo.id` to the next best from `alt_logo_ids` and rerun. Repeat until it passes (or all alts exhausted, in which case ask the user for a logo file).
