# {{BRAND_NAME}}-PPT-Design-System

> The visual language for all decks produced for {{BRAND_NAME}}. Follow it precisely so every new deck is immediately recognisable as part of the same family.

---

<!--
  TEMPLATE NOTES (delete this comment block in the generated output):

  Sections marked <!-- BRAND-VARIABLE --> must be filled with brand-specific content.
  Sections marked <!-- ENGINEERING-DNA --> must be copied verbatim. They came from
  real, painful bugs in production decks. Do NOT "simplify" or "trim" them — every
  line earns its place.

  Placeholder syntax: {{TOKEN}}. Replace each from $WS/decisions.json.
-->

## 1. Design Philosophy

<!-- BRAND-VARIABLE: 1-2 paragraphs capturing the brand's mood + a "Constraints vs Freedom" block -->

**{{PHILOSOPHY_PARAGRAPH}}**

> Example mood paragraphs to draw from (pick or remix the closest match, then customize):
> - **Premium / editorial / typographically-led**: "draws from luxury brand communications: generous whitespace, high-contrast type, restrained colour. Every element earns its place. No decorative gradients, no stock icons, no emoji."
> - **Engineering-clean / grid-driven**: "structured as a developer documentation site: tight grid, monospace accents, copy-pastable code blocks, generous use of muted gray scales with one strong accent."
> - **Bold-colorful / consumer**: "high-energy, high-saturation, hero typography, big illustrative shapes. Whitespace exists to make the colour pop, not to reduce noise."
> - **Minimal-monochrome**: "reductive, near-monochrome palette, one accent colour reserved for emphasis only, type does the heavy lifting."

**Two modes:**
- **Desktop (≥ 769 px)**: 1280 × 720 px canvas, scale-to-fit (§5 runtime), keyboard / click navigation.
- **Mobile (≤ 768 px)**: all slides stack vertically as a scrollable page; single-column layouts.

### Design taste <!-- ENGINEERING-DNA: design-taste -->

**Commit to a clear aesthetic point of view.** This DS is a brand instrument, not a generic SaaS template. Every deck made from it should be unmistakably *this* brand on first glance — not "another tasteful business presentation." Bold maximalism and refined minimalism both succeed; the failure mode is timidity.

**Anti-AI-slop rules** (apply on every slide, every component, every variant):

- **No generic font defaults.** The brand typeface is named in §3 and must be used. If a fallback is needed it should be the most characterful option available, not Arial/system-ui as the "design choice".
- **No cliché palettes.** Pure-white background + one purple/blue accent + slate-grey type = AI-slop signature. The §2 palette has a dominant chord and supporting accents — use them with that hierarchy. Do not flatten everything to "white + grey + one accent".
- **No even-weighted accent grids.** A 6-colour decorative rainbow looks like a Storybook page, not a brand. One dominant chord + 2–3 semantic accents (with distinct meaning) is the right shape.
- **No off-the-shelf SaaS dashboard chrome.** 8 px radius + soft drop-shadow + tidy spacing on every component homogenises every brand. Match the brand's actual radius / shadow / density per §2.
- **No vague mood language in copy.** "Modern, clean, bold" describes everything and therefore nothing. Slide titles and section copy should be specific and concrete.
- **One orchestrated entrance, not scattered micro-interactions.** A staggered slide-content reveal on activation is the only motion most slides need; do not bolt hover wiggles onto every card.

### Constraints vs Freedom <!-- ENGINEERING-DNA framing; bullet contents are BRAND-VARIABLE -->

This Design System defines **hard constraints** (what you must never break) and **reusable components** (what you can reach for). It does NOT define recipes — every slide should be composed for its specific content, not assembled from a template.

**Hard constraints (locked):**
- Colour palette (§2 tokens only — no ad-hoc colours)
- {{PRIMARY_FONT}} typeface, no serif/display fonts {{FONT_RESTRICTION_NOTES}}
- 12px readability floor
- Logo on every slide
- **Every slide content lives inside a `.sc` container** (even bespoke full-bleed Type J / Type A compositions). The `.sc` is what `fit_contract_intact` measures — bespoke layouts that draw straight into a custom shell silently bypass absorber detection, mobile catch-all, and the 602 px content budget. No `.sc`, no contract.
- **Logo `<symbol>` must contain no inner `fill` attributes** (including `fill="none"` on wrapper `<g>` elements). Any inner fill overrides the `currentColor` cascade and renders the wordmark fully invisible — while every byte-level check still says PASS. `embed_logo.py` strips these on materialization; the `logo_renders` hard check rejects any that survive.
- No emoji (👍🎉 etc.) — typographic symbols (✓ − ! ×) and geometric indicators are permitted
- No decorative stock imagery
- `.shd` header strip on content slides
- `.sw` border-left accent

**Reusable components (reach for, don't force):**
- §7 Component Library provides cards, tables, charts, tabs, marks — use them when they fit. Skip them when a bespoke layout serves the content better.

**Bespoke elements (encouraged):**
- **Invent freely** within the colour palette. {{BESPOKE_EXAMPLES_PARAGRAPH}}
- The test is: does the element use only the defined colour tokens, the brand typeface, and respect the readability floor? If yes, it's in-system even if it doesn't match any named component.
- **Do not self-restrict to the named components.** If a slide needs something that doesn't exist in §7, design it from the tokens. The best slides are bespoke compositions built from system tokens.

---

## 2. Colour Tokens <!-- BRAND-VARIABLE: hex values + brand-palette names; core role token names are invariant -->

The token system has three layers:

1. **Core role tokens** — invariant names across every brand. They identify *what role* the colour plays, not *what colour it is*. A red brand's `--primary` is red; a blue brand's `--primary` is blue.
2. **Semantic tokens** — invariant names; encode meaning (positive / negative / warning / informational) rather than colour identity.
3. **Brand palette tokens** — brand-specific names AND hex values. These are the additional accents the brand actually uses (e.g. Unilever's `--lilac` and `--water`, P&G's `--spark`, Stripe's `--lavender`). Naming is whatever the brand uses for them — captured during Phase 1 from `brand.json`.

```css
:root {
  /* ── Core role tokens (invariant names) ── */
  --primary:  {{NAVY_HEX}};   /* Dominant brand chord — cover bg, primary mark colour */
  --accent:   {{BLUE_HEX}};   /* CTA / link / single saturated highlight */
  /* ── Neutrals ── */
  --surface:  {{SURFACE_HEX}};   /* Paper / slide bg */
  --white:    #FFFFFF;
  --ink:      {{INK_HEX}};   /* Body text on light surfaces */
  --mid:      {{MID_HEX}};   /* Secondary text / muted labels */
  --rule:     {{RULE_HEX}};   /* Dividers / hairlines */
  --tint:     {{TINT_HEX}};   /* Subtle row / section bg */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    {{GREEN_HEX}};   /* Positive */
  --green-bg: {{GREEN_BG_HEX}};
  --red:      {{RED_HEX}};   /* Negative */
  --red-bg:   {{RED_BG_HEX}};
  --warn:     {{WARN_HEX}};   /* Warning / caution */
  --warn-bg:  {{WARN_BG_HEX}};
  --teal:     {{TEAL_HEX}};   /* Informational / neutral highlight */
  --teal-bg:  {{TEAL_BG_HEX}};
  /* ── Brand palette (brand-specific names; expanded from brand.json accents+neutrals) ── */
{{BRAND_PALETTE_TOKENS}}
}
```

**Rules:** <!-- ENGINEERING-DNA -->
- **Token names are role abstractions, not colour names.** `--primary` is the brand's dominant chord regardless of whether that chord is navy / red / yellow / black. Slide CSS reads `var(--primary)` and gets the right colour for whichever brand DS it's loaded against.
- **One *dominant* accent colour per slide.** Use `--accent` for the slide's signature highlight (CTA, callout border, chart fill). Brand-palette tokens (e.g. `var(--lilac)`) are reach-for-when-needed decoration, not parallel accents — at most one decorative brand-palette colour per slide.
- **Semantic colours coexist when they carry distinct, opposing meaning** — e.g., a comparison slide with ✓ (`--green`) / ✗ (`--red`) marks. Otherwise pick one.
- **`--tint` is for rows, not card fills.**
- **Never pure black.** `--primary` is the brand's actual dark; if the brand has nothing dark, use `--ink` for what would otherwise have been black.
- **Never ad-hoc hex literals in slide CSS.** Every colour must come from a token (core / semantic / brand palette). The `token_only_colors` hard check enforces this.

---

## 3. Typography <!-- BRAND-VARIABLE: font family + fallback; the scale below is mostly invariant -->

**{{PRIMARY_FONT}}** — sole typeface. Weights {{WEIGHT_RANGE}}{{ITALIC_NOTE}}. `{{FALLBACK_FONT}}` fallback for {{FALLBACK_USE_CASE}}.

> {{TYPE_PHILOSOPHY_NOTE}}

### Type scale <!-- ENGINEERING-DNA — sizes are invariant; the scale is what makes decks readable -->

| Role | Size | Weight | Letter-spacing | Notes |
|---|---|---|---|---|
| Cover headline | 82 px | 900 | −0.03 em | Line-height 0.98 |
| Cover subtitle | 22 px | 300 italic | +0.01 em | |
| Slide title | 50 px | 900 | −0.025 em | Line-height 1.06 |
| Slide subtitle | 20 px | 600 | +0.01 em | `--mid` |
| Eyebrow / badge | 11–12 px | 800 | +0.18–0.24 em | ALL CAPS |
| Card headline | 28 px | 900 | −0.01 em | |
| Body / list | 16 px | 600 | default | Line-height 1.5–1.6 |
| Table / data | 13–14 px | 700–800 | +0.1 em | ALL CAPS |
| Caption / meta | 12–13 px | 700–800 | +0.14 em | Never below 12 px |

### Readability <!-- ENGINEERING-DNA -->

1. **Maximise**: Default to the largest size that fits. Half-empty slide with 14px body = design failure.
2. **Floor**: Nothing below 12px <!-- ENGINEERING-DNA: typography-floor -->. If content doesn't fit at min sizes, change layout — never shrink font.

| Role | Minimum | **Enforced default** |
|---|---|---|
| Slide title | 38 px | **50 px** — only shrink for multi-line on dense slides |
| Card headline | 22 px | **28 px** |
| Primary body / list | 14 px | **16 px** — slide-level paragraphs, main content |
| Component secondary | 13 px | **13–14 px** — descriptions inside cards, list item details, supporting text under a title within a component |
| Subtitle | 16 px | **20 px** |
| Badges / labels | 12 px | **13 px** |

**Enforcement**: Title below 50px or primary body below 16px on a slide's main content area is a bug. Component-internal secondary text (card descriptions, list details) may use 13–14px to maintain visual hierarchy between title and description within the component.

### 3.1 Typography Safety <!-- ENGINEERING-DNA: typography-safety -->

Slide "looks good" is engineering-quantifiable. The rules below are hard rules; the `text_layout_safe` auto-check enforces most of them.

1. **Never glued to the bottom edge**: the lowest visible text element on a content slide must be ≥ 18px from the slide's bottom (target 24–48px). Keep `padding-bottom` on `.sw` / `.sc` as a guardrail; do not push content to the edge.
2. **Never truncated**: any text container with `overflow:hidden` must have `scrollHeight ≤ clientHeight`. If content might overflow, use `text-overflow: ellipsis` or `-webkit-line-clamp` and explicitly declare the allowed max line count — never "bet" that it just fits.
3. **Never broken across lines arbitrarily**: H1/H2/H3 single titles ≤ 3 lines; body paragraphs ≤ 5 lines. For CJK titles, avoid mid-phrase wraps — use `word-break: keep-all; line-break: strict;` paired with shorter copy, do not let auto-wrap take over.
4. **Global layout law** (the basics):
   - Disable `hyphens: auto` globally (it produces broken hyphens in mixed-CJK environments).
   - `line-height` ≥ 1.4 for body, ≥ 1.15 for headings — never tighter.
   - Minimum 12px spacing between cards / paragraphs (matches the §5 12px floor); two text blocks must never touch.
   - At most 3 levels of hierarchy inside one `.sc` (title → subtitle/figure → list/cards). If you need more, split the slide.
5. **Build-time self-check** (run after writing HTML):
   ```js
   document.querySelectorAll('.slide').forEach((s, i) => {
     const slideBottom = s.getBoundingClientRect().bottom;
     let maxBottom = -Infinity;
     s.querySelectorAll('h1,h2,h3,h4,p,li').forEach(el => {
       if ((el.textContent||'').trim().length < 3) return;
       const r = el.getBoundingClientRect();
       if (r.height > 0) maxBottom = Math.max(maxBottom, r.bottom);
       if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden')
         console.warn(`slide ${i+1}: ${el.tagName} text truncated →`, (el.textContent||'').slice(0,40));
     });
     const gap = slideBottom - maxBottom;
     if (gap < 18) console.warn(`slide ${i+1}: text only ${gap.toFixed(1)}px from bottom (need ≥ 18)`);
   });
   ```
6. **Repair priority when a check fails**:
   - First, **edit the copy** (cut words, shorten sentences, use noun phrases).
   - Then, **change the layout** (drop an item, split the slide, turn a list into a 2-column grid).
   - **Never** "fit it in" by shrinking type below 12px or allowing truncation.

---

## 4. {{BRAND_NAME}} Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### Definition (once per HTML file)

The logo must be a real brand identity asset, **fully inlined** into the HTML (no external network dependency). `embed_logo.py` automatically chooses one of three colour-handling tiers based on what the source SVG actually contains. The tier you got is recorded in `<brand>/source/assets/logo.report.json` as `colour_handling`.

#### Tier A — `mono` (single-colour wordmark or silhouette)

Used when the source SVG is a single-colour wordmark (Tiffany "TIFFANY&CO.", Unilever wordmark, Apple silhouette, Stripe wordmark, etc). Inner fills are stripped so the `<symbol fill="currentColor">` cascade colours the whole shape; `.logo.W` / `.logo.L` flip white-on-dark / brand-dark-on-light by setting CSS `color:`.

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="{{LOGO_VIEWBOX}}" fill="currentColor">
    {{LOGO_PATH_ELEMENTS}}  <!-- inner <path>/<g> carry NO fill attribute at all -->
  </symbol>
</svg>
```

> ⚠️ **fill-cascade pitfall** <!-- ENGINEERING-DNA: logo-inner-fill -->
> Many SVG exporters wrap real glyph paths inside a defaulting group:
> `<g fill="none" fill-rule="evenodd"><g><path d="..."/></g></g>`. Pasted into our
> `<symbol fill="currentColor">`, the inner `fill="none"` **wins** over the parent
> currentColor cascade — the wordmark renders 100% invisible while every byte-level
> check (path-d length, viewBox, even `visible_on_cover` via getBoundingClientRect)
> still says PASS. **In tier A every inner `fill` (including `fill="none"`) MUST
> be stripped.** `embed_logo.py` does this automatically; the `logo_renders` hard
> check enforces it (mono-mode only) by rejecting any inner `fill` that isn't
> `fill="currentColor"`. If you hand-paste a logo, strip manually.

#### Tier B — `multi` (multi-colour or gradient SVG)

Used when the source SVG contains `<linearGradient>`, `<radialGradient>`, `fill="url(#…)"`, or two-or-more distinct fill colours — typically circular badges (P&G), figurative marks (Starbucks green-on-white, Netflix N), tri-colour glyphs, or tint-on-tint logos.

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="{{LOGO_VIEWBOX}}">  <!-- NO fill="currentColor" on the symbol -->
    {{LOGO_PATH_ELEMENTS}}  <!-- inner <path>/<g>/<defs>/<gradient> kept verbatim with their native fills -->
  </symbol>
</svg>
```

The logo always renders in its native colours. **`.logo.W` / `.logo.L` flipping is a no-op** in this tier — gradient stops do not accept the `currentColor` cascade. Cover slides for tier-B brands need a layout that ensures contrast natively (see "Multi-colour cover handling" below).

> The `logo_renders` hard check inspects `<symbol>` for `fill="currentColor"`; if it's absent and `<image>` is also absent, the check infers tier B and **skips** the `hasInnerFill` rule. Inner fills are expected and required.

#### Tier C — `raster` (PNG/JPG/WebP fallback)

Used only when no SVG source is available and a raster logo passes the quality gate (minimum 64×64). The bytes are base64-embedded inside an `<image href>`:

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 {{LOGO_W}} {{LOGO_H}}">
    <image href="data:image/png;base64,{{LOGO_BASE64}}" width="{{LOGO_W}}" height="{{LOGO_H}}"/>
  </symbol>
</svg>
```

Like tier B, `.logo.W` / `.logo.L` flipping is a no-op (raster pixels don't respond to CSS `color:`). Same cover-handling caveat applies. Resolution-bound — prefer tiers A/B whenever an SVG source can be found, even if the raster gate also passes.

> ⚠️ **Typographic placeholders are forbidden**: faking a logo with `<text>` of the brand name (e.g. `<text>P&G</text>`, a generic disc-with-letter) is a build failure. The `logo_renders` hard check rejects `<symbol>` blocks that contain only `<text>`. If no source produces a real logo, **stop and ask the user** for an original file — never invent a placeholder.

#### Multi-colour cover handling (tiers B and C only) <!-- ENGINEERING-DNA: logo-multicolor-cover -->

Tier-A logos flip cleanly on any background via `.logo.W` / `.logo.L`. Tiers B and C don't — the logo renders in its native colours regardless. Two design responses, in order of preference:

1. **Choose a cover background where the native logo reads cleanly.** A P&G blue-and-white badge sits on its own white circular plate or on a light cover; a Starbucks green-and-white siren sits on cream. The cover doesn't need to be `var(--surface)` — it just needs enough contrast around the logo's bounding box. **Don't try to flip via CSS** — the symbol won't respond.
2. **Use a backplate** when a dark cover is non-negotiable (brand mood requires it). Wrap the `.logo` in a `.logo-chip` with `background: #fff; border-radius: 50%; padding: 8px;` (size to taste). The badge then floats on white inside a small chip, the chip floats on the dark cover. This pattern was used in early P&G / Starbucks deckify runs and is acceptable when option 1 won't fit the brand voice.

The pre-ship checklist (§13) enforces "logo visibly renders on cover" regardless of tier — but does NOT enforce `.W` / `.L` flip on tiers B/C.

Source resolution order (the actual order `embed_logo.py` tries):
1. Inline SVG inside the page's `<header>` (filtered to drop utility icons with viewBox < 60px)
2. Wikipedia infobox logo file for the brand
3. apple-touch-icon (typically ≥ 180px PNG)
4. favicon (SVG or PNG)
5. og:image / twitter:image
6. Common path guesses (/logo.svg, /assets/logo.svg, …)

### Usage

```html
<!-- White (on dark slides) -->
<svg class="logo W" viewBox="{{LOGO_VIEWBOX}}" aria-label="{{BRAND_NAME}}">
  <use href="#brand-wm"/>
</svg>

<!-- Brand-dark (on light slides) -->
<svg class="logo L" viewBox="{{LOGO_VIEWBOX}}" aria-label="{{BRAND_NAME}}">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor must be on .logo — NOT on .logo path.
   CSS selectors do not pierce SVG <use> shadow DOM.
   Inherited fill on the outer <svg> cascades in correctly. */
.logo   { height: {{LOGO_HEIGHT}}; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### Placement rules <!-- ENGINEERING-DNA -->
- **Every slide** must carry the logo — cover and all content slides.
- **Cover**: top-right corner of the `.cov-top` flex row.
- **Content slides**: right end of the `.shd` header strip (left = title eyebrow / slide number, right = logo).
- Minimum clear space around the logo = logo height ({{LOGO_HEIGHT}}) on all sides.
- Never stretch, recolour outside `W`/`L`, or overlay the logo on a patterned area.

{{LOGO_BRAND_RESTRICTIONS_NOTE}}

---

## 5. Slide Architecture <!-- ENGINEERING-DNA — the entire section, invariant -->

### Scaffold
```
#wrap — fixed fullscreen, flex-centre, background: var(--ink)
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

`#wrap` and `body` background **must use `var(--ink)`**, not hardcoded `#000` / `#1A1A1A` / `#1F1F22` — those get caught by `token_only_colors`. Each brand's `--ink` already encodes its real dark register (Coca-Cola pure black, Unilever warm graphite, Apple near-black), so the letterbox follows it correctly.

### Fullscreen fit — scale-to-fit at runtime <!-- ENGINEERING-DNA: scale-to-fit -->

The deck is a **fixed-size 1280×720 canvas** at the DOM level. To fill any viewport without black borders, scale at runtime via CSS transform — never resize the canvas itself. This keeps every measurement, every fit-contract calculation, every `offsetWidth` value invariant; the auto-eval and the visual reality both stay coherent.

```css
/* Required CSS hooks */
#deck { transform-origin: center center; will-change: transform; }
```

```html
<!-- Required JS at the end of <body>; runs on load + resize -->
<script>
(function () {
  var deck = document.getElementById('deck');
  function scaleDeck() {
    if (!deck) return;
    if (window.matchMedia('(max-width: 768px)').matches) {
      deck.style.transform = 'none';
      return;
    }
    var s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    deck.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', scaleDeck);
  window.addEventListener('load', scaleDeck);
  scaleDeck();
})();
</script>
```

**Why a CSS transform and not a viewport unit on the canvas itself:**
- `transform: scale()` does not change `offsetWidth` / `offsetHeight`, so every layout calculation, fit-contract budget (602 px content area), and auto-eval measurement remains exact.
- A viewport-relative `width: 100vw` on the canvas would warp the type scale; a slide tuned for 50 px headlines becomes 38 px on a small laptop.
- Mobile is exempt: the mobile media query already turns the deck into a flow document, so `transform: none` is required there or the stacked slides scale with the canvas and break.

**Anti-pattern**: shipping a deck without `scaleDeck()` lets `#wrap`'s flex-centre place a 1280×720 deck inside a 1920×1080 viewport with 320 px / 180 px of dark border — the deck looks unfinished even when content is correct. Every brand DS must wire scale-to-fit into the verification deck.

### Visibility
```css
.slide          { opacity: 0; pointer-events: none; transition: opacity .38s ease; overflow: hidden; }
.slide.active   { opacity: 1; pointer-events: auto; }
.slide.active .sc { animation: enter .42s cubic-bezier(.4,0,.2,1) both; }
```

### Content slide (`.sw`)
```css
.sw { background: var(--surface); border-left: 3px solid var(--accent); display: flex; flex-direction: column; height: 100%; }
/* Default: symmetric padding. Override with asymmetric bottom pad for visible breathing room. */
.sw .sc { flex: 1; padding: 32px 80px 32px 96px; display: flex; flex-direction: column; overflow: hidden; }
```

### Header strip (`.shd`) — every content slide
```css
.shd { display: flex; align-items: center; justify-content: space-between; padding: 0 80px 0 96px; flex: 0 0 54px; border-bottom: 1px solid var(--rule); }
.shd-num { font-size: 11px; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; color: var(--accent); }
```

---

### 5.1 Single-Slide Fit Contract (hard-won, non-negotiable) <!-- ENGINEERING-DNA: fit-contract -->

**The one rule that prevents every "content overflowing the deck" bug:** a content slide is a *fixed-size box*, not a scrolling document. Every slide must fit inside 720 px with visible bottom breathing room. If it doesn't, you reduce content — never ship a slide that clips or leaks.

#### The three-layer overflow safety net <!-- ENGINEERING-DNA: three-layer-overflow -->

Every stacked content slide MUST carry `overflow: hidden` at THREE levels. This is belt-and-braces: one layer catches whatever the others miss.

```css
.slide   { overflow: hidden; }   /* Layer 1 — absolute stop at deck edge */
.sw .sc  { overflow: hidden; }   /* Layer 2 — content area stop */
.row-x   { overflow: hidden; }   /* Layer 3 — any flex:1 absorber inside .sc */
.card    { overflow: hidden; }   /* Layer 4 — any card with bounded height */
```

Without these, a single oversized bullet cascades outward and pushes the deck past 720 px. With them, the worst case is clipping — ugly, but never a layout break.

#### Content-height budget (memorise this math)

For a standard content slide with default 54 px header strip and symmetric 32 px V-padding:

```
Deck height         720 px
− header strip      54 px
− top padding       32 px
− bottom padding    32 px
─────────────────────────
= content area     602 px   ← all section heights + gaps must fit in here
```

If you use asymmetric padding (24 top / 40 bottom) to create visible bottom breathing room:

```
Deck 720 − 54 − 24 − 40 = 602 px content area
Visible bottom margin from deck edge = 40 px (from padding) + any flex spacer
```

**Before writing HTML, sum your planned section heights + gaps.** If the total exceeds 602 px, cut content. Do not shrink fonts below the 12 px floor. Do not bet on the browser "figuring it out." The numbers don't lie.

#### The "single flex:1 absorber" rule

A vertical stack of N sections inside `.sc` must have **exactly one** section that absorbs leftover space. All others are natural-sized.

```html
<div class="sc">
  <div class="hero">     <!-- flex: 0 0 auto — natural height -->
  <div class="tl-wrap">  <!-- flex: 0 0 auto — natural height -->
  <div class="row-top">  <!-- flex: 1 1 0; min-height: 0; overflow: hidden — absorbs remaining -->
  <div class="row-risk"> <!-- flex: 0 0 auto — natural height -->
</div>
```

**Why:** With one absorber, total height = always exactly 602 px. Zero is wrong (content collapses). Two+ absorbers race for space and one gets squashed. Exactly one is the only stable configuration.

The absorber MUST carry `min-height: 0` (so it can shrink below its content's natural size) AND `overflow: hidden` (so its children clip instead of pushing it taller). Both are required — missing either breaks the contract.

#### Asymmetric bottom padding — visible breathing room

Default `.sc` padding is symmetric `32 80 32 96`. For weekly-status / progress-report slides where the audience reads top-down and the bottom edge carries visual weight, prefer:

```css
.sw .sc { padding: 24px 80px 40px 96px; }   /* 24 top / 40 bottom */
```

The extra bottom padding creates deliberate visible breathing — roughly half a section-gap worth — between the last content block and the deck edge. This reads as "composed" rather than "crammed."

#### Pre-build checklist (do this BEFORE writing HTML)

1. **List your sections** and assign each a role: `absorber` (exactly one) or `natural`.
2. **Estimate natural heights** using the type scale. A card with head (30) + label (14) + 5 single-line 13 px bullets (~125) + V-padding (34) = ~203 px.
3. **Sum fixed sections + gaps**. Confirm total ≤ (602 − absorber minimum) — the absorber needs at least ~160 px to hold meaningful content.
4. **Write the copy short enough that single-line bullets don't wrap**. In a half-width column at 13 px CJK, budget ~28 characters per bullet before wrapping.
5. **Render at 1280×720 and eye the bottom edge.** Not at 1920×1080 (the `transform: scale()` masks overflow by rescaling). The native canvas is the source of truth.

#### Anti-patterns that cause overflow

- **N natural-height sections with no absorber**: total exceeds 602 px, content leaks past the deck. Missing the "one absorber" rule.
- **Absorber without `min-height: 0`**: flex refuses to shrink it below content's natural size, defeats the whole point.
- **Absorber without `overflow: hidden`**: oversized children push through the flex:1 and break the parent.
- **Omitting `overflow: hidden` on `.slide`/`.sc`**: if any math is slightly off, content bleeds outside the deck onto the body. Safety net missing.
- **Packing 2 section labels + 5+ bullets into one card that gets ~240 px of flex:1 space**: natural content ~260 px, clipping guaranteed. Merge into one section, or cut bullets.
- **Trusting the 1920×1080 render**: the `transform: scale()` shrinks everything uniformly — a 730 px deck still *looks* fine at scale, but it *is* broken. Always verify at native 1280×720.

---

## 6. Slide Types <!-- BRAND-VARIABLE: emphasis order varies; the type definitions are mostly invariant -->

> **Emphasis for {{BRAND_NAME}}**: {{SLIDE_TYPE_EMPHASIS_NOTE}}
> Foreground these types when designing decks: {{EMPHASIZED_TYPES_LIST}}.
> Use sparingly: {{DEEMPHASIZED_TYPES_LIST}}.

### Type A — Cover
- Background: `{{COVER_BACKGROUND}}`
- Structure: Logo top-right → Eyebrow → Giant headline → Italic subtitle → Meta row
- **No decorative lines of any kind** — no hairlines, no accent lines, no gradient borders. The background is the surface.

### Type B — Two-column content
Comparisons, feature lists, metrics. `grid-template-columns: 1fr 1fr; gap: 20px`. Collapses on mobile.

### Type C — Full-width narrative
Single column, large type, pull-quotes. For context, summary, recommendation slides.

### Type D — Flip cards
Two cards side-by-side. Front = `--primary`, back = `{{FLIP_BACK_COLOR}}` (softer than `--accent`). **Hover + click flip** — JS `onclick` toggles `.on` class (required for mobile). Ghost Roman numerals on front. Spacious back (32px padding, ≤ 4 content elements).

**Typography — must be large and commanding:**

| Element | Class | Size | Weight |
|---|---|---|---|
| Front title | `.cnm` | **28px** | 900 |
| Front body | `.cbd` | **17px** | 600 |
| Front hint | `.ht` | 13px | 800 |
| Back label | `.bkl` | 13px | 800 |
| Back title | `.bkt` | **22px** | 900 |
| Compare tag | `.vs .vt` | 13px | 900 |
| Compare body | `.vs .vb` | **16px** | 700 |
| Conclusion | `.ccl` | **15px** | 600 |

**Do not use inline style overrides** to shrink flip card text below these sizes. If content doesn't fit, reduce the number of items — never the font size.

### Type E — Data / comparison slide
Slide dominated by a table or structured data grid. Used for feature comparisons, TCO analysis, specification matrices. The table component spec (§7.7) defines the element-level design; this type defines when to use it and how to lay out the slide around it.

**Principles:** The table is the star — title + table + optional one-line callout below. No side panels competing for attention. If the table has 6+ columns, let it span full width.

**Row-count rule** <!-- ENGINEERING-DNA: type-e-row-count -->
- 5 rows is the comfortable count at standard 14 px row-padding (cell `padding: 14px 18px`).
- 6+ rows require either (a) tightening cell padding to `padding: 10px 16px` or (b) splitting the data across two slides. Do not let the absorber clip — the `text_layout_safe` hard check catches it.
- If the table needs 6+ rows AND a side callout in the absorber, split. Don't pack.

### Type F — Image slide
One or more images dominate the slide, with text anchored to a calm area. Used to show real product UI, real screenshots, or contextual photography that makes an abstract concept concrete.

**Principles:**
- Images must serve comprehension — no decorative stock. Prefer: product UI screenshots, real data visualizations, contextual photos that illustrate a specific point.
- When building a deck, **actively web search for relevant images** (product logos, UI screenshots, real-world examples) that support the narrative.
- Image treatment: `border-radius: 4px`, optional `1px solid var(--rule)` border. On dark backgrounds, no border needed.
- Layout: image fills 50–70% of slide area. Text sits beside or overlaid on a tinted region. Never place text over a busy image without a scrim.
- Caption below image: `.cap` style (13px, 800 weight, ALL CAPS, `--mid`).

### Type G — Interactive demo
A self-contained, click-to-advance micro-experience embedded in a slide. Purpose: help the audience *see* a concept working, not just read about it.

**When to use:** Scenario walkthroughs, before/after comparisons, multi-step process visualizations.

**Structure:** A "screen" area (dark bg `--primary` or `#1a1a2e`, 4px radius) with step-by-step content that advances on click. Controls: forward/back buttons or numbered steps. Content appears via CSS transitions.

**Design rules:**
- Must feel like a polished product demo, not a prototype. Clean typography, restrained animation.
- CSS `@keyframes` only — no JS animation libraries. Keep under 50 lines of CSS per demo.
- Each step should be one clear idea. Max 5 steps per demo.
- Mobile: auto-advance on scroll or tap targets ≥ 44px.

### Type H — Chart / data insight slide
Slide led by one or more data visualizations. Used for quantitative arguments, trend analysis, performance comparisons. The chart component spec (§7.8) defines element-level design; this type defines slide-level principles.

**Principles:**
- One primary chart per slide. A secondary small chart is acceptable if it directly supports the primary.
- Title states the insight, not the chart type. Good: "{{BRAND_NAME}} leads on all three dimensions". Bad: "Bar Chart Comparison".
- Chart fills 50–70% of slide area. Remaining space: title + one paragraph of interpretation or a callout.
- Animate on entrance for narrative impact.

### Type I — Tabs slide
Multiple content views switchable via tabs. Fits more information in one slide when content has natural categories. Tab component spec in §7.9.

**Principles:** Max 4 tabs. Each tab panel is a self-contained slide-within-a-slide — it can use any component from §7. Avoid tabs as a crutch for overstuffed slides; if 2 tabs would each be sparse, merge into one view instead.

### Type J — Quote / pullquote
A single striking statement that anchors a narrative moment. Used for key takeaways, audience reframes, or memorable one-liners.

**Structure (standard):** Large quote text (28–36px, weight 700, `--ink`) centered or left-aligned. Optional attribution below (14px, `--mid`). Left border accent (`3px solid --accent`) or none.

**Structure (full-bleed bespoke variant):** Some brands lean into full-bleed `--primary` slides with multi-line poster type (e.g. Mars's Five Principles page — six lines of Inter Black 900 stacked vertically with selected words tinted in `--accent` or a brand-palette colour). When you do this:

1. **The composition still goes inside `.sw + .sc`.** Use `.sw` (with `background: var(--primary)` overriding the default) and a single `.sc` containing your bespoke layout. Do **not** invent a sibling shell class (`.fpwrap`, `.poster-wrap`, etc.) — bespoke shells silently bypass `fit_contract_intact` (no `.sc` = no absorber count = `bad_slides: [{absorbers: 0}]`).
2. **Exactly one absorber** inside the `.sc` carries `flex: 1 1 0; min-height: 0; overflow: hidden` — usually the middle band that holds the big type. The header band and footer attribution are `flex: 0 0 auto`.
3. **Cap line size by row count.** `clientH` of the absorber is `(720 − 54 header − 32 top − 32 bottom) − header_band − footer_band`. For a 5-line stack with header band ~120 px and footer band ~30 px, the absorber is ~420 px — cap each line at ≈ `floor((420 − 4×gap) / 5) ≈ 78 px`. **At 84 px × 5 lines you overflow by ~40 px.** Pick the line size from the budget; never the other way around.
4. **No header strip (`.shd`) on full-bleed Type J.** Put logo + slide-eyebrow inline at the top of `.sc` instead.

### Type K — Timeline / roadmap
Horizontal or vertical sequence of milestones. Used for project plans, evolution narratives, phase descriptions. Component spec in §7.12.

---

## 7. Component Library <!-- ENGINEERING-DNA — every component preserved verbatim -->

Reusable elements available on **any** slide type. A slide may combine multiple components, or use none — building bespoke layouts from colour tokens and type scale instead. The library is a toolkit, not a constraint. If a slide's content calls for something not listed here, invent it from the system tokens (§2 colours, §3 type, §12 spacing).

### 7.1 Panel Card (Tier 1 — "big card")

Full-height comparison panels. Used when 2–3 options need deep, structured comparison.

```css
.panel {
  flex: 1; padding: 22px;
  display: flex; flex-direction: column; gap: 8px;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--rule);
}
.panel.blue { border-top-color: var(--accent); }
.panel.dark { background: var(--primary); color: #fff; border: none; border-top: 3px solid rgba(255,255,255,.2); }
```

Internal: `.cap` eyebrow → title (18–22px 900) → rows (`.panel-row`: surface bg, 8px 12px padding) → optional callout.

### 7.2 Showcase Card (Tier 2 — "block card")

Clean, elegant blocks for grouping content. White background, thin coloured top accent, content-first. **No heavy coloured header strips** — the card should feel like premium stationery, not a dashboard widget.

**Design treatment:**
- Background: `var(--white)` with `1px solid var(--rule)` border
- **Top accent line**: `3px solid var(--accent)` (default). Can be `--primary`, `--green`, or `--red` per context. This is a thin, elegant line — not a filled header block.
- **No mandatory label strip.** The title lives inside the card body as part of the content.
- Title: 20px weight 900 `--ink`
- Content: 15–16px weight 600 `--mid`, generous 12px+ gaps
- Optional SVG icon: 32–36px, inline next to the title or above it.
- **Hover**: subtle lift (`translateY(-2px)`) + shadow

```css
.show-card {
  flex: 1; display: flex; flex-direction: column;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--accent);
  padding: 20px 22px;
  gap: 10px;
  transition: transform .22s ease, box-shadow .22s ease;
}
.show-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.08); }
.show-card .show-title { font-size: 20px; font-weight: 900; color: var(--ink); line-height: 1.15; }
.show-card .show-desc { font-size: 15px; font-weight: 600; color: var(--mid); line-height: 1.5; }
.show-card.accent-navy { border-top-color: var(--primary); }
.show-card.accent-green { border-top-color: var(--green); }
.show-card.compact { padding: 16px 18px; gap: 8px; }
.show-card.compact .show-title { font-size: 18px; }
```

**Anti-pattern**: Heavy filled colour strips across every card when shown 6+ in a grid — visual monotony. Use the thin top accent line instead.

### 7.3 Item Card (Tier 3 — "list card")

Small horizontal cards for structured lists. Left accent border + leading indicator + content.

```css
.bitem {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 12px 16px;
  background: var(--white);
  border-left: 3px solid var(--accent);
}
```

**Leading indicator** — flexible:
- **Ghost number** (default): `20px 900, --accent, opacity .4` — for sequential lists (`01`, `02`, `03`)
- **Icon circle**: small circle (24px) with symbol (`!`, `✓`, `→`) — for findings, alerts. Use semantic bg.
- **Letter / label**: single letter or short label in same ghost style — for categorized items.

### 7.4 Stat Card (Tier 4 — "number card")

Compact metric display. `stat-num` (36px 900 `--primary`) + `stat-label` (12px 800 ALL CAPS `--mid`).

### 7.5 Callout / Note

**Light** (inline note):
```css
.snote { border-left: 3px solid var(--primary); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 700; }
```

**Dark** (conclusion / recommendation bar):
Full-width navy block for slide-ending takeaways. Text: 13–16px 700–800, `rgba(255,255,255,.85)`. Bold key phrases with `color: #fff`. No border-left — the solid navy fill IS the emphasis.

### 7.6 Marks, Badges & Chips

**Status marks**:
```css
.mark::before { display: inline-block; width: 18px; height: 18px; border-radius: 50%; text-align: center; line-height: 18px; font-size: 11px; font-weight: 900; margin-right: 8px; }
.mark.yes::before { content: '✓'; background: var(--green); color: #fff; }
.mark.no::before  { content: '−'; background: var(--red); color: #fff; }
```

**Badges** — small label pills (`.bg-g`, `.bg-r`, `.bg-b`) for inline status. 12–13px, 900 weight, ALL CAPS.

**Tech chips** — compact inline labels for technology/feature names. 13px 700, `min-height: 26px`.

### 7.7 Table (`.dt`)

```css
.dt { width: 100%; border-collapse: collapse; font-size: 14px; font-weight: 600; }
.dt th { background: var(--primary); color: #fff; font-size: 13px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
.dt td { padding: 10px 14px; color: var(--ink); border-bottom: 1px solid var(--rule); }
.dt tr.hi td { background: var(--tint); }
.dt .pos { color: var(--green); font-weight: 800; }
.dt .neg { color: var(--red); font-weight: 800; }
.dt .neu { color: var(--mid); font-weight: 600; }
```

**Rules:**
- Navy header row is the only colour block. All data cells: white bg, `--ink` text.
- **No coloured badges in `<table>` cells** — use text weight/colour for emphasis instead.
- One optional `--tint` highlight row for the single most important row.
- The "clean grid" test: squint at the table. If you see a patchwork of coloured boxes, the design has failed.

### 7.8 Charts

| Type | Primary colour | Secondary | Neutral | Notes |
|---|---|---|---|---|
| Bar (H / V) | `--accent` | `--primary` | `--rule` | Animated grow on entrance |
| Progress / gauge | `--accent` fill | — | `--rule` track | 8px height, 4px radius |
| Pie / donut | `--primary` | `--accent` | `--rule` | Max 3 segments |
| Timeline | `--primary` dots | — | `--rule` dots | Key nodes: `--tint` ring |

Max 2 colours per chart (+ `--rule` neutral). Animate on entrance: bars grow, counters count up.

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 '{{PRIMARY_FONT}}'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
.tb:hover { border-color: var(--accent); color: var(--accent); }
.tb.on { background: var(--primary); border-color: var(--primary); color: #fff; }
.tc { display: none; } .tc.on { display: block; }
```

Max 4 tabs.

### 7.10 Sequential steps / barriers
Use numeric labels `01` `02` `03` in monospace-weight span, `--accent` colour, rather than bullet points or decorative emoji.

### 7.11 Decision questions
Prefix with `Q.1` / `Q.2` spans in `--accent`, weight 800, letter-spacing 0.12 em.

### 7.12 Timeline

Horizontal sequence of milestones with connecting line.

**Critical layout rule — dot always sits on the line, line passes through dot center:**
The `.tl-line` uses a fixed `top` value calculated from total space above the dot's center. Date block uses `min-height` for text + `margin-bottom` for breathing room.

**Important: use `margin-bottom`, NOT `padding-bottom` for date-to-dot spacing.** With `box-sizing: border-box`, padding is INSIDE `min-height` — it shrinks the content area instead of adding space. `margin` is OUTSIDE the box.

```
Date height:    min-height = 48px
Date-to-dot gap: margin-bottom = 16px
Total above dot: 64px → dot center: 73px → line top: 73px
```

```css
.tl-wrap { position: relative; padding: 0 10px; }
.tl-line { position: absolute; top: 73px; left: 30px; right: 30px; height: 3px; background: var(--rule); }
.tl-row { display: flex; position: relative; z-index: 1; }
.tl-node { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 4px; }
.tl-date-top {
  font-size: 22px; font-weight: 900; letter-spacing: -.01em; color: var(--accent);
  min-height: 48px; margin-bottom: 16px;
  display: flex; align-items: flex-end; justify-content: center;
}
.tl-dot2 { width: 18px; height: 18px; border-radius: 50%; background: var(--rule); margin-bottom: 12px; flex-shrink: 0; transition: transform .3s ease; }
.tl-name { font-size: 18px; font-weight: 900; color: var(--ink); line-height: 1.2; margin-bottom: 4px; }
.tl-detail { font-size: 14px; font-weight: 600; color: var(--mid); line-height: 1.3; }
```

### Component selection guide

| Content | Component | Layout |
|---|---|---|
| 2–3 deep comparisons | Panel | side-by-side flex |
| 2–3 labeled concept blocks (premium) | Showcase Card | side-by-side flex or 3-col grid |
| 3–4 labeled concept blocks (compact) | Showcase Card `.compact` | 3-col or 2×2 grid |
| Sequential steps, feature lists | Item Card | stacked column |
| Findings with status icons | Item Card (icon variant) | stacked column |
| Key metrics | Stat Card | row of 3–4 |
| Interactive comparison | Flip Card (Type D) | 2 side-by-side |
| Single takeaway | Callout / Note (light) | full width |
| Slide conclusion / recommendation | Callout / Note (dark) | full width |
| Project milestones | Timeline | horizontal flex |

---

## 8. Imagery & Visual Evidence <!-- BRAND-VARIABLE intro; rules are ENGINEERING-DNA -->

### Principle

{{IMAGERY_PHILOSOPHY_NOTE}}

### When to include images

- **Product UI screenshots**: When discussing a specific tool, show its real interface.
- **Data visualizations**: When a number or trend is central, build a chart (Type H).
- **Contextual photography**: When a scenario benefits from visual grounding, search for and include a relevant image.
- **Diagrams**: When a concept has structure (layers, flows, comparisons), draw it with CSS/SVG rather than describing it in words.

### How to source images

1. **Search actively**: Use web search to find relevant product screenshots, diagrams, contextual photos. Prefer official assets.
2. **CSS-drawn alternatives**: Bar charts, progress bars, timeline diagrams — preferable to external images when data is simple.
3. **Never use**: Decorative stock photos, abstract gradients, AI-generated placeholder art, images that don't directly support the slide's point.

### Image treatment

- `border-radius: 4px`. Optional `1px solid var(--rule)` border on light backgrounds.
- Images on dark backgrounds: no border.
- Caption: `.cap` style below the image.
- Never place text over a busy image without a scrim (`rgba(0,0,0,.5)` minimum).

---

## 9. Navigation <!-- ENGINEERING-DNA -->

### Dot nav — bottom-centre, horizontal

```css
#nav { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 7px; z-index: 99; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.25); cursor: pointer; transition: all .22s ease; }
.dot.on { width: 20px; border-radius: 3px; background: rgba(255,255,255,.85); }
```

### Slide counter — bottom-right
`SLIDE N / TOTAL` — 12px, weight 700, 35% white.

### Controls
Keyboard: `← → Space Home End`. Touch: 48px swipe threshold.

---

## 10. Mobile <!-- ENGINEERING-DNA — every line invariant; this section saved real decks -->

```css
@media (max-width: 768px) {
  body { overflow-y: auto; }
  #wrap { position: static; display: block; }
  #deck { width: 100%; position: static; transform: none !important; }
  .slide { position: relative !important; opacity: 1 !important; pointer-events: auto !important; min-height: 100dvh; }
  /* Cover and content shells must fill the slide on mobile — `.slide` only sets min-height,
     which a child's `height: 100%` does not inherit, so each shell needs its own min-height. */
  .cov, .sw { min-height: 100dvh; height: auto; }
  .cov-title { font-size: 48px; } .stitle { font-size: 32px; }
  .shd { padding: 0 20px; } .sw .sc { padding: 24px 20px; }
  /* All multi-col → single-col */ .g2,.g3,.flip-row,.tabs { grid-template-columns: 1fr; flex-direction: column; }
  #nav, #ctr { display: none; }
}
```

All interactive elements ≥ 44×44px tap area. Never use `vh` for font/padding on mobile.

### The inline-flex trap (critical) <!-- ENGINEERING-DNA: inline-flex-trap -->

**Root cause of most mobile layout failures**: Multi-column layouts written with inline `style="display:flex"` instead of CSS classes (`.g2`, `.g3`). The mobile media query collapses `.g2,.g3` to single-column, but inline `style="display:flex"` is immune to class-based media queries — it keeps the horizontal layout on mobile, making cards tiny and unreadable.

**Prevention rule**: Every multi-column layout inside `.sc` must use a CSS class (`.g2`, `.g3`, `.fr`) for its flex/grid direction. If inline `style="display:flex"` is unavoidable (e.g., bespoke one-off layouts), the mobile CSS must include a **catch-all override**:

```css
@media (max-width: 768px) {
  /* Catch-all: force ALL flex layouts inside content areas to stack */
  .sc div[style*="display:flex"] { flex-direction: column !important; }
  .sc div[style*="grid-template-columns"] { grid-template-columns: 1fr !important; }
  /* Panel cards should not have fixed flex ratios on mobile */
  .pnl { flex: none !important; width: 100% !important; }
}
```

**Preferred approach**: Use `.g2` / `.g3` classes instead of inline flex. Inline flex should be the exception, and the catch-all CSS above is the safety net.

**Checklist addition**: Before shipping, resize the browser to 375px width and verify every slide stacks vertically. Any slide that still shows side-by-side content on mobile is a bug.

### Mobile flip card fix <!-- ENGINEERING-DNA: flip-card-mobile -->

CSS `:hover` does not work on touch devices. Flip cards **must** have a JS `onclick` handler that toggles a `.on` class. This is the **only** reliable cross-platform flip mechanism.

**Required JS on every flip card:**
```html
<div class="fc" onclick="this.classList.toggle('on')">
```

**Required CSS — both desktop and mobile:**
```css
/* Desktop: hover + .on both trigger flip */
.fc:hover .fc-inner, .fc.on .fc-inner { transform: rotateY(180deg); }

/* Mobile: kill ALL 3D transforms, use show/hide instead */
@media (max-width: 768px) {
  .fc { perspective: none !important; min-height: auto !important; }
  .fc .fc-inner { transform-style: flat !important; transition: none !important; height: auto !important; transform: none !important; }
  .fc:hover .fc-inner, .fc.on .fc-inner { transform: none !important; }
  .fc .ff { position: relative !important; backface-visibility: visible !important; transform: none !important; }
  .fc .ff-back { display: none; transform: none !important; }
  .fc.on .ff-front { display: none; }
  .fc.on .ff-back { display: flex; transform: none !important; }
}
```

---

## 11. Animation <!-- ENGINEERING-DNA -->

### Core transitions

| Element | Animation | Duration | Easing |
|---|---|---|---|
| Slide transition | opacity | 380 ms | ease |
| Content entrance | translateY(14px) → 0 + fade | 420 ms | cubic-bezier(.4,0,.2,1) |
| Flip card | rotateY 180° | 650 ms | cubic-bezier(.4,0,.2,1) |
| Dot nav | width expand | 220 ms | ease |

### Storytelling animations

| Element | Spec | When to use |
|---|---|---|
| Staggered entrance | 80ms delay between items, 350ms each | Lists, grids |
| Counter roll-up | 0 → target, 1200ms | Statistics |
| Bar chart grow | width 0 → target, 600ms + 100ms stagger | Comparisons |
| Scale-in | scale(.85) → 1, 400ms | Callout cards |

### Principles

- Every animation serves comprehension. Remove if purely ornamental.
- Play once on entrance. No loops (except flip cards on hover).
- Total **entrance animation** time per slide ≤ 2 seconds. Does not apply to interactive demos or flip cards.

### Storytelling-first design

1. **Flip cards for reveals**: problem/solution, before/after, myth/reality.
2. **Concrete over abstract**: specific scenarios beat generic descriptions.
3. **Visual evidence**: Charts > text. Screenshots > descriptions. Diagrams > bullet lists.
4. **The screenshot test**: If no one would photograph this slide, it needs a visual hook.

---

## 12. Layout Rules <!-- ENGINEERING-DNA -->

### Overflow prevention

Every slide fits 720px. If too dense: reduce gaps → reduce body to 14px → split slide. Never clip or scroll.

**The "blue block" trap**: Dark callout at bottom-right = visual imbalance. Move to full-width bottom, use `.snote` instead, or place dark cards at top.

**The "blue-on-navy" trap**: On dark slides (`--primary` bg), never use `--accent` for text or accent — it creates jarring, cheap-looking contrast. Use white (`#fff`) or semi-transparent white (`rgba(255,255,255,.85)`) for emphasis. For subtle CTAs on dark backgrounds, use `rgba(255,255,255,.08)` bg fill + white text.

**The "dark stack" trap**: When a dark element sits directly below another dark element, they visually merge. Always separate dark elements with at least 12px of `--surface` or `--tint` gap.

**Header-content dedup**: The `.shd-n` bar already carries the slide's section label. Do not repeat the same text as a separate eyebrow/title inside the content area.

### Spacing

| Token | Value |
|---|---|
| H-padding left | 96 px |
| H-padding right | 80 px |
| V-padding | 32 px |
| Header height | 54 px |
| Card gap | 20 px |
| Card inner padding | 32 px |
| Border radius | {{BORDER_RADIUS}} |
| Rule thickness | 1 px |
| Accent border | 3 px |

---

## 13. Checklist <!-- ENGINEERING-DNA: pre-ship-checklist -->

Before sharing a deck, verify every item.

### Brand & tokens
- [ ] Logo on every slide (cover top-right, content `.shd` right end)
- [ ] **Logo visibly renders on cover** — open the deck, eyeball the top-right of slide 1. A wordmark that is "embedded" but invisible is the most common failure mode (see §4 fill-cascade pitfall). `has_real_vector_path: true` alone does NOT guarantee visibility.
- [ ] Logo `<symbol>` block contains no inner `fill` attribute (including `fill="none"` on wrapper `<g>`) — only `fill="currentColor"` is allowed
- [ ] **Every slide content lives inside a `.sc` container** — including bespoke full-bleed Type J / Type A. No sibling shells like `.fpwrap` / `.poster-wrap` (they bypass `fit_contract_intact` silently)
- [ ] Colours: only system tokens — no ad-hoc hex values
- [ ] All bespoke elements built from system tokens only (§1 Constraints vs Freedom)
- [ ] No emoji (👍🎉 etc.) — typographic symbols (✓ − ! ×) are fine
- [ ] {{PRIMARY_FONT}} {{WEIGHT_RANGE}}{{ITALIC_NOTE_SHORT}} loaded; no serif or display fonts
- [ ] Cover subtitle: {{PRIMARY_FONT}} 300 italic only (or brand-equivalent if 300 italic unavailable)

### Typography & readability
- [ ] No text below 12px — check badge/label columns especially
- [ ] Slide titles ≥ 50px (38px only on dense multi-line exceptions)
- [ ] Body text ≥ 16px on non-table slides (14px only on data-dense tables)
- [ ] Subtitles ≥ 20px
- [ ] Chinese text same size/weight as English equivalents (if mixed)

### Slide structure
- [ ] Every content slide has `.shd` header strip with slide number + logo
- [ ] Cover has no decorative lines — no hairlines, no accent lines, no gradient borders
- [ ] Every slide fits within 720px — no content clipped or overflowing
- [ ] No "blue block" trap — dark callouts not isolated at bottom-right of 2-col layouts
- [ ] Scanning headlines only gives a coherent story

### Fit contract (§5.1) — the layout-safety gate
- [ ] `.slide` AND `.sw .sc` both carry `overflow: hidden` (three-layer safety net)
- [ ] Every flex:1 absorber ALSO carries `overflow: hidden` AND `min-height: 0`
- [ ] Vertical stack inside `.sc` has exactly **one** `flex: 1 1 0` absorber; all other rows are `flex: 0 0 auto`
- [ ] Sum of natural-section heights + gaps ≤ 602 px (standard content area)
- [ ] Visible bottom gap from last content to deck edge ≥ 20 px
- [ ] Verified at native **1280 × 720** render, not scaled — overflow is invisible at scaled sizes
- [ ] No single card packs 2 section labels + 5+ bullets into a half-column absorber slot — merge or cut

### Components & interaction
- [ ] Flip cards are hover-only on desktop, click-to-toggle on mobile (JS `onclick` toggles `.on`)
- [ ] Tables: no coloured badges in cells — text colour only (`.pos` / `.neg` / `.neu`)
- [ ] Card tier matches content density (no bitem-only sparse slides)
- [ ] Interactive elements have visible hover/focus states

### Visual & imagery
- [ ] Images serve comprehension — no decorative stock photos
- [ ] Text over images has a scrim (≥ 50% opacity dark overlay)
- [ ] Image captions use `.cap` style

### Animation
- [ ] Entrance animation plays on slide activation
- [ ] Entrance animation total time per slide ≤ 2s (does not apply to interactive demos or flip cards)
- [ ] No entrance animation loops

### Responsive (mobile parity — non-negotiable)
- [ ] All multi-col layouts collapse to 1-col at ≤ 768px — **including inline `style="display:flex"` layouts** (verify at 375px width)
- [ ] No inline `display:flex` without a matching catch-all in mobile CSS (see §10 "inline-flex trap")
- [ ] Touch swipe works (48px threshold)
- [ ] Dot nav hidden in mobile scroll mode
- [ ] Tap targets ≥ 44×44px on mobile
- [ ] Flip cards work via tap (not just hover) on mobile — every `.fc` has `onclick="this.classList.toggle('on')"`
- [ ] Browser tested at **375px width** before declaring done
