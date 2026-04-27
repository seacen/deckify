# Stripe-PPT-Design-System

> The visual language for all decks produced for Stripe. Follow it precisely so every new deck is immediately recognisable as part of the same family.

---

## 1. Design Philosophy

**Stripe reads as engineering-clean and developer-first: tight grids, monospace accents, restrained palette, generous use of muted gray scales with a single signature blurple accent. The deck identity is monochrome navy + one purple thing — the campaign-chrome hero gradients you see on stripe.com are explicitly out of scope here. Every element earns its place; if it's not load-bearing, it's not on the slide.**

> Stripe's deck mood: structured as a developer documentation site — tight grid, monospace accents, copy-pastable code blocks, generous use of muted gray scales with one strong accent. The accent (`--blue` blurple) appears once or twice per slide as emphasis, never as decoration.

**Two modes:**
- **Desktop (≥ 769 px)**: 1280 × 720 px canvas, scale-to-fit, keyboard / click navigation.
- **Mobile (≤ 768 px)**: all slides stack vertically as a scrollable page; single-column layouts.

### Constraints vs Freedom

This Design System defines **hard constraints** (what you must never break) and **reusable components** (what you can reach for). It does NOT define recipes — every slide should be composed for its specific content, not assembled from a template.

**Hard constraints (locked):**
- Colour palette (§2 tokens only — no ad-hoc colours)
- Inter typeface (substituting for licensed Söhne Var), no serif/display fonts; monospace permitted only for code/tabular numerals
- 12px readability floor
- Logo on every slide
- No emoji (the entire visual system rejects them) — typographic symbols (✓ − ! ×) and geometric indicators are permitted
- No decorative stock imagery; no campaign-chrome hero gradients (those belong on marketing pages, not internal decks)
- `.shd` header strip on content slides
- `.sw` border-left accent

**Reusable components (reach for, don't force):**
- §7 Component Library provides cards, tables, charts, tabs, marks — use them when they fit. Skip them when a bespoke layout serves the content better.

**Bespoke elements (encouraged):**
- **Invent freely** within the colour palette. A CSS-drawn funnel diagram, a custom step diagram with monospace labels, a diff-style before/after block — all welcome, as long as they use only the tokens below and respect the type floor.
- The test is: does the element use only the defined colour tokens, the brand typeface, and respect the readability floor? If yes, it's in-system even if it doesn't match any named component.
- **Do not self-restrict to the named components.** If a slide needs something that doesn't exist in §7, design it from the tokens. The best slides are bespoke compositions built from system tokens.

---

## 2. Colour Tokens

```css
:root {
  /* ── Brand ── */
  --navy:     #0A2540;   /* Stripe ink */
  --blue:     #635BFF;   /* Stripe blurple — the iconic accent */
  /* ── Neutrals ── */
  --surface:  #F6F9FC;   /* cool off-white */
  --white:    #FFFFFF;
  --ink:      #0A2540;   /* same as navy — type-led */
  --mid:      #425466;   /* secondary text */
  --rule:     #E3E8EE;   /* dividers */
  --tint:     #ECF1F6;   /* row tint */
  /* ── Semantic ── */
  --green:    #14B872;   /* Stripe success green */
  --green-bg: #E5F8EE;
  --red:      #DF1B41;   /* Stripe error red */
  --red-bg:   #FCE8EC;
  --warn:     #F8A302;   /* Stripe warning amber */
  --warn-bg:  #FFF6E0;
  --teal:     #11B5D9;   /* Informational / neutral highlight */
  --teal-bg:  #E1F4F9;
}
```

**Rules:**
- `--navy` and `--blue` are the only dark fills. Never pure black. (Token names are abstractions — `--navy` is whatever this brand's dominant dark is; for Stripe that's `#0A2540`.)
- One *dominant* accent colour per slide. Semantic colours (green/red for pass/fail, amber for caution, teal for info) may coexist when they carry distinct, opposing meaning — e.g., a comparison slide with ✓/✗ marks.
- `--tint` is for rows, not card fills.

---

## 3. Typography

**Inter** — sole typeface. Weights 300–900, italic 300. `system-ui, sans-serif` fallback for environments without Inter loaded.

> Stripe's production face is **Söhne Var** (Klim Type Foundry) — licensed for stripe.com use only. Inter is the closest open-license substitute and is what every internal deck should use; the type personality (high contrast between weights, slightly humanist forms, strong italic) carries across. If the deck will only ever live inside Stripe and Söhne Var is licensed for the surface, swap Inter for `sohne-var` in the font stack — no other change required.

### Type scale

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

### Readability

1. **Maximise**: Default to the largest size that fits. Half-empty slide with 14px body = design failure.
2. **Floor**: Nothing below 12px. If content doesn't fit at min sizes, change layout — never shrink font.

| Role | Minimum | **Enforced default** |
|---|---|---|
| Slide title | 38 px | **50 px** — only shrink for multi-line on dense slides |
| Card headline | 22 px | **28 px** |
| Primary body / list | 14 px | **16 px** — slide-level paragraphs, main content |
| Component secondary | 13 px | **13–14 px** — descriptions inside cards, list item details, supporting text under a title within a component |
| Subtitle | 16 px | **20 px** |
| Badges / labels | 12 px | **13 px** |

**Enforcement**: Title below 50px or primary body below 16px on a slide's main content area is a bug. Component-internal secondary text (card descriptions, list details) may use 13–14px to maintain visual hierarchy between title and description within the component.

---

## 4. Stripe Logo

### Definition (once per HTML file)

Define the wordmark as an SVG `<symbol>` in a hidden `<svg>` block at the top of `<body>`. The path below was extracted from stripe.com's rendered logo SVG and saved at `$WS/assets/logo.svg`. Any hardcoded `fill` attributes have been removed from the `<path>` so CSS `currentColor` controls the colour.

```html
<svg style="display:none" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 60 25">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M59.6444 14.2813h-8.062c.1843 1.9296 1.5983 2.5476 3.2032 2.5476 1.6352 0 2.9534-.3656 4.0453-.9506v3.3179c-1.1186.7115-2.5964 1.1068-4.5645 1.1068-4.011 0-6.8218-2.5122-6.8218-7.4783 0-4.19441 2.3837-7.52509 6.3017-7.52509 3.912 0 5.9537 3.28038 5.9537 7.49819 0 .3982-.0372 1.261-.0556 1.4835Zm-5.9241-5.62407c-1.0294 0-2.1739.72812-2.1739 2.58387h4.2573c0-1.85362-1.0721-2.58387-2.0834-2.58387ZM40.9547 20.303c-1.4411 0-2.322-.6087-2.9133-1.0417l-.0088 4.6271-4.1181.8755-.0014-19.19053h3.7543l.0864 1.01784c.6035-.52914 1.6114-1.29157 3.2256-1.29162 2.8925 0 5.6162 2.6052 5.6162 7.39971 0 5.2327-2.6948 7.6037-5.6409 7.6037Zm-.959-11.35573c-.9453 0-1.5376.34559-1.9669.81586l.0245 6.11967c.3997.433.9763.7813 1.9424.7813 1.5231 0 2.5437-1.6575 2.5437-3.8745 0-2.1544-1.037-3.84233-2.5437-3.84233Zm-11.7602-3.3739h4.1341V20.0088h-4.1341V5.57337Zm0-4.694699L32.3696 0v3.35821l-4.1341.87868V.878671ZM23.9198 10.2223v9.7861h-4.1156V5.57296h3.6867l.1317 1.21751c1.0035-1.7722 3.0722-1.41321 3.6209-1.21594v3.78524c-.5242-.16908-2.2894-.42779-3.3237.86253Zm-8.5525 4.7221c0 2.4275 2.5988 1.6719 3.1263 1.4609v3.3522c-.5492.3013-1.5437.5458-2.8901.5458-2.4441 0-4.2773-1.7999-4.2773-4.2379l.0173-13.17658 4.0206-.85464.0032 3.5395h3.1278V9.0857h-3.1278v5.8588-.0001Zm-4.9069.7026c0 2.9645-2.31051 4.6562-5.73464 4.6562-1.41958 0-2.92289-.2761-4.453935-.9347v-3.9319c1.382085.7516 3.093705 1.315 4.457755 1.315.91864 0 1.53106-.2459 1.53106-1.0069C6.26064 13.7786 0 14.5192 0 9.95995 0 7.04457 2.27622 5.2998 5.61655 5.2998c1.36404 0 2.72806.20934 4.09208.75351V9.9317c-1.25265-.67618-2.84332-1.05979-4.09588-1.05979-.86296 0-1.44753.24965-1.44753.8924.0001 1.85329 6.29518.97249 6.29518 5.88279v-.0001Z"/>
  </symbol>
</svg>
```

### Usage

```html
<!-- White (on dark slides) -->
<svg class="logo W" viewBox="0 0 60 25" aria-label="Stripe">
  <use href="#brand-wm"/>
</svg>

<!-- Brand-dark (on light slides) -->
<svg class="logo L" viewBox="0 0 60 25" aria-label="Stripe">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor must be on .logo — NOT on .logo path.
   CSS selectors do not pierce SVG <use> shadow DOM.
   Inherited fill on the outer <svg> cascades in correctly. */
.logo   { height: 19px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--navy); }
```

### Placement rules
- **Every slide** must carry the logo — cover and all content slides.
- **Cover**: top-right corner of the `.cov-top` flex row.
- **Content slides**: right end of the `.shd` header strip (left = title eyebrow / slide number, right = logo).
- Minimum clear space around the logo = logo height (19 px) on all sides.
- Never stretch, recolour outside `W`/`L`, or overlay the logo on a patterned area.

The Stripe wordmark must never be re-coloured to anything other than `--navy` (light surface) or `#fff` (dark surface). Do NOT place it on the campaign blurple gradient — it belongs on the deck's restrained navy/white system.

---

## 5. Slide Architecture

### Scaffold
```
#wrap — fixed fullscreen, flex-centre
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

### Visibility
```css
.slide          { opacity: 0; pointer-events: none; transition: opacity .38s ease; overflow: hidden; }
.slide.active   { opacity: 1; pointer-events: auto; }
.slide.active .sc { animation: enter .42s cubic-bezier(.4,0,.2,1) both; }
```

### Content slide (`.sw`)
```css
.sw { background: var(--surface); border-left: 3px solid var(--blue); display: flex; flex-direction: column; height: 100%; }
/* Default: symmetric padding. Override with asymmetric bottom pad for visible breathing room. */
.sw .sc { flex: 1; padding: 32px 80px 32px 96px; display: flex; flex-direction: column; overflow: hidden; }
```

### Header strip (`.shd`) — every content slide
```css
.shd { display: flex; align-items: center; justify-content: space-between; padding: 0 80px 0 96px; flex: 0 0 54px; border-bottom: 1px solid var(--rule); }
.shd-num { font-size: 11px; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; color: var(--blue); }
```

---

### 5.1 Single-Slide Fit Contract (hard-won, non-negotiable)

**The one rule that prevents every "content overflowing the deck" bug:** a content slide is a *fixed-size box*, not a scrolling document. Every slide must fit inside 720 px with visible bottom breathing room. If it doesn't, you reduce content — never ship a slide that clips or leaks.

#### The three-layer overflow safety net

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
2. **Estimate natural heights** using the type scale.
3. **Sum fixed sections + gaps**. Confirm total ≤ (602 − absorber minimum).
4. **Write the copy short enough that single-line bullets don't wrap**.
5. **Render at 1280×720 and eye the bottom edge.** Native canvas is the source of truth.

#### Anti-patterns that cause overflow

- **N natural-height sections with no absorber**: total exceeds 602 px, content leaks past the deck.
- **Absorber without `min-height: 0`**: flex refuses to shrink it below content's natural size.
- **Absorber without `overflow: hidden`**: oversized children push through and break the parent.
- **Omitting `overflow: hidden` on `.slide`/`.sc`**: content bleeds outside the deck.
- **Packing 2 section labels + 5+ bullets into one card that gets ~240 px of flex:1 space**: clipping guaranteed.
- **Trusting the 1920×1080 render**: `transform: scale()` masks overflow. Always verify at native 1280×720.

---

## 6. Slide Types

> **Emphasis for Stripe**: Stripe decks are narrative-led and data-led, not image-led. Foreground these types when designing decks: **Type A (cover), Type C (full-width narrative), Type E (data table), Type H (chart), Type J (pull-quote), Type K (timeline)**.
> Use sparingly: **Type F (image-dominant)** — Stripe avoids stock photography and most decorative imagery, so image-anchored slides only earn their place when there's a real product UI shot or a CSS-drawn diagram. **Type G (interactive demo)** — Stripe's docs already do interactive demos better than a slide can; a slide demo competes and loses.

### Type A — Cover
- Background: `linear-gradient(135deg, var(--navy) 0%, #1A2A4F 50%, #0A1F3D 100%)` — subtle, almost-monochrome navy gradient. The bridge stops `#1A2A4F` and `#0A1F3D` are derived directly from `--navy` (one shade lighter, one shade deeper) — the cover reads as monochrome navy with a hint of depth, not a campaign gradient.
- Structure: Logo top-right → Eyebrow → Giant headline → Italic subtitle → Meta row
- **No decorative lines of any kind** — no hairlines, no accent lines, no gradient borders. The background is the surface.

### Type B — Two-column content
Comparisons, feature lists, metrics. `grid-template-columns: 1fr 1fr; gap: 20px`. Collapses on mobile.

### Type C — Full-width narrative
Single column, large type, pull-quotes. For context, summary, recommendation slides. **The Stripe workhorse** — most argument-led slides land here.

### Type D — Flip cards
Two cards side-by-side. Front = `--navy`, back = `#4A45D1` (one shade softer than `--blue`). **Hover + click flip** — JS `onclick` toggles `.on` class (required for mobile). Ghost Roman numerals on front. Spacious back (32px padding, ≤ 4 content elements).

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
Slide dominated by a table or structured data grid. **One of Stripe's foreground types** — funnel tables, MRR breakdowns, cohort matrices land here. The table component spec (§7.7) defines the element-level design; this type defines when to use it and how to lay out the slide around it.

**Principles:** The table is the star — title + table + optional one-line callout below. No side panels competing for attention. If the table has 6+ columns, let it span full width.

### Type F — Image slide (use sparingly for Stripe)
One or more images dominate the slide, with text anchored to a calm area. For Stripe, this means real product UI screenshots or CSS-drawn diagrams ONLY — never stock photography, never campaign chrome.

**Principles:**
- Image treatment: `border-radius: 4px`, optional `1px solid var(--rule)` border. On dark backgrounds, no border needed.
- Layout: image fills 50–70% of slide area. Text sits beside or overlaid on a tinted region.
- Caption below image: `.cap` style (13px, 800 weight, ALL CAPS, `--mid`).
- Prefer CSS-drawn diagrams over fetched images whenever the data is simple — they're crisper, smaller, and stay in-system.

### Type G — Interactive demo (use sparingly for Stripe)
A self-contained, click-to-advance micro-experience embedded in a slide. Stripe's actual product is the world's best interactive demo; a slide rarely competes. Reserve for genuinely novel scenarios that the live product doesn't cover.

### Type H — Chart / data insight slide
Slide led by one or more data visualizations. **Foreground type for Stripe.**

**Principles:**
- One primary chart per slide.
- Title states the insight, not the chart type. Good: "Cross-border SaaS exporters convert 4× better than B2C marketplaces". Bad: "Bar Chart Comparison".
- Chart fills 50–70% of slide area. Remaining space: title + one paragraph of interpretation or a callout.
- Animate on entrance for narrative impact.

### Type I — Tabs slide
Multiple content views switchable via tabs. Max 4 tabs.

### Type J — Quote / pullquote
A single striking statement that anchors a narrative moment. **Foreground type for Stripe** — used heavily for strategy doc excerpts, customer voice, founding-principle reframes.

**Structure:** Large quote text (28–36px, weight 700, `--ink`) centered or left-aligned. Optional attribution below (14px, `--mid`). Left border accent (`3px solid var(--blue)`) preferred.

### Type K — Timeline / roadmap
Horizontal or vertical sequence of milestones. **Foreground type for Stripe** — phase plans, rollout sequences, market-launch chronologies.

---

## 7. Component Library

Reusable elements available on **any** slide type. A slide may combine multiple components, or use none — building bespoke layouts from colour tokens and type scale instead.

### 7.1 Panel Card (Tier 1 — "big card")

```css
.panel {
  flex: 1; padding: 22px;
  display: flex; flex-direction: column; gap: 8px;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--rule);
}
.panel.blue { border-top-color: var(--blue); }
.panel.dark { background: var(--navy); color: #fff; border: none; border-top: 3px solid rgba(255,255,255,.2); }
```

### 7.2 Showcase Card (Tier 2 — "block card")

```css
.show-card {
  flex: 1; display: flex; flex-direction: column;
  background: var(--white); border: 1px solid var(--rule);
  border-top: 3px solid var(--blue);
  padding: 20px 22px;
  gap: 10px;
  transition: transform .22s ease, box-shadow .22s ease;
}
.show-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.08); }
.show-card .show-title { font-size: 20px; font-weight: 900; color: var(--ink); line-height: 1.15; }
.show-card .show-desc { font-size: 15px; font-weight: 600; color: var(--mid); line-height: 1.5; }
.show-card.accent-navy { border-top-color: var(--navy); }
.show-card.accent-green { border-top-color: var(--green); }
.show-card.compact { padding: 16px 18px; gap: 8px; }
.show-card.compact .show-title { font-size: 18px; }
```

### 7.3 Item Card (Tier 3 — "list card")

```css
.bitem {
  display: flex; align-items: flex-start; gap: 14px;
  padding: 12px 16px;
  background: var(--white);
  border-left: 3px solid var(--blue);
}
```

### 7.4 Stat Card (Tier 4 — "number card")
Compact metric display. `stat-num` (36px 900 `--navy`) + `stat-label` (12px 800 ALL CAPS `--mid`).

### 7.5 Callout / Note

**Light** (inline note):
```css
.snote { border-left: 3px solid var(--navy); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 700; }
```

**Dark** (conclusion / recommendation bar): Full-width navy block for slide-ending takeaways.

### 7.6 Marks, Badges & Chips

```css
.mark::before { display: inline-block; width: 18px; height: 18px; border-radius: 50%; text-align: center; line-height: 18px; font-size: 11px; font-weight: 900; margin-right: 8px; }
.mark.yes::before { content: '✓'; background: var(--green); color: #fff; }
.mark.no::before  { content: '−'; background: var(--red); color: #fff; }
```

### 7.7 Table (`.dt`)

```css
.dt { width: 100%; border-collapse: collapse; font-size: 14px; font-weight: 600; }
.dt th { background: var(--navy); color: #fff; font-size: 13px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
.dt td { padding: 10px 14px; color: var(--ink); border-bottom: 1px solid var(--rule); }
.dt tr.hi td { background: var(--tint); }
.dt .pos { color: var(--green); font-weight: 800; }
.dt .neg { color: var(--red); font-weight: 800; }
.dt .neu { color: var(--mid); font-weight: 600; }
```

### 7.8 Charts

| Type | Primary | Secondary | Neutral |
|---|---|---|---|
| Bar | `--blue` | `--navy` | `--rule` |
| Progress | `--blue` fill | — | `--rule` track |
| Pie / donut | `--navy` | `--blue` | `--rule` |
| Timeline | `--navy` dots | — | `--rule` dots |

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'Inter'; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
.tb:hover { border-color: var(--blue); color: var(--blue); }
.tb.on { background: var(--navy); border-color: var(--navy); color: #fff; }
.tc { display: none; } .tc.on { display: block; }
```

### 7.10 Sequential steps / barriers
Numeric labels `01` `02` `03` in `--blue`, weight 800 — preferred over bullet points.

### 7.11 Decision questions
Prefix with `Q.1` / `Q.2` spans in `--blue`, weight 800, letter-spacing 0.12 em.

### 7.12 Timeline

```css
.tl-wrap { position: relative; padding: 0 10px; }
.tl-line { position: absolute; top: 73px; left: 30px; right: 30px; height: 3px; background: var(--rule); }
.tl-row { display: flex; position: relative; z-index: 1; }
.tl-node { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 4px; }
.tl-date-top { font-size: 22px; font-weight: 900; color: var(--blue); min-height: 48px; margin-bottom: 16px; display: flex; align-items: flex-end; justify-content: center; }
.tl-dot2 { width: 18px; height: 18px; border-radius: 50%; background: var(--rule); margin-bottom: 12px; flex-shrink: 0; }
.tl-name { font-size: 18px; font-weight: 900; color: var(--ink); line-height: 1.2; margin-bottom: 4px; }
.tl-detail { font-size: 14px; font-weight: 600; color: var(--mid); line-height: 1.3; }
```

---

## 8. Imagery & Visual Evidence

### Principle
Stripe avoids decorative imagery. Every visual element is either typographic, a CSS-drawn diagram, a real product UI screenshot, or a data viz. Stock photography, AI placeholder art, and abstract gradients are not in the system.

### When to include images
- Product UI screenshots (real Stripe Dashboard, Stripe Atlas onboarding, etc.)
- Data visualizations — build with CSS / SVG, not as static image exports
- Diagrams — CSS/SVG over external images

### Image treatment
- `border-radius: 4px`. Optional `1px solid var(--rule)` border on light backgrounds.
- Caption: `.cap` style below.
- Never place text over a busy image without a scrim.

---

## 9. Navigation

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

## 10. Mobile

```css
@media (max-width: 768px) {
  body { overflow-y: auto; }
  #wrap { position: static; display: block; }
  #deck { width: 100%; position: static; transform: none !important; }
  .slide { position: relative !important; opacity: 1 !important; pointer-events: auto !important; min-height: 100dvh; }
  .cov-title { font-size: 48px; } .stitle { font-size: 32px; }
  .shd { padding: 0 20px; } .sw .sc { padding: 24px 20px; }
  .g2,.g3,.flip-row,.tabs { grid-template-columns: 1fr; flex-direction: column; }
  #nav, #ctr { display: none; }
}
```

All interactive elements ≥ 44×44px tap area. Never use `vh` for font/padding on mobile.

### The inline-flex trap (critical)

**Root cause of most mobile layout failures**: Multi-column layouts written with inline `style="display:flex"` instead of CSS classes. The mobile media query collapses `.g2`/`.g3` to single-column, but inline `style="display:flex"` is immune to class-based media queries — it keeps the horizontal layout on mobile.

```css
@media (max-width: 768px) {
  .sc div[style*="display:flex"] { flex-direction: column !important; }
  .sc div[style*="grid-template-columns"] { grid-template-columns: 1fr !important; }
  .pnl { flex: none !important; width: 100% !important; }
}
```

**Preferred approach**: Use `.g2` / `.g3` classes. Inline flex should be the exception, the catch-all is the safety net. Verify at 375px width before declaring done.

### Mobile flip card fix

CSS `:hover` does not work on touch devices. Flip cards **must** have a JS `onclick` handler that toggles a `.on` class.

```html
<div class="fc" onclick="this.classList.toggle('on')">
```

```css
.fc:hover .fc-inner, .fc.on .fc-inner { transform: rotateY(180deg); }

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

## 11. Animation

| Element | Animation | Duration | Easing |
|---|---|---|---|
| Slide transition | opacity | 380 ms | ease |
| Content entrance | translateY(14px) → 0 + fade | 420 ms | cubic-bezier(.4,0,.2,1) |
| Flip card | rotateY 180° | 650 ms | cubic-bezier(.4,0,.2,1) |
| Dot nav | width expand | 220 ms | ease |
| Bar chart grow | width 0 → target | 600 ms + 100 ms stagger | ease-out |

Every animation serves comprehension. Play once on entrance. Total entrance ≤ 2 seconds per slide.

---

## 12. Layout Rules

### Overflow prevention
Every slide fits 720px. If too dense: reduce gaps → reduce body to 14px → split slide. Never clip or scroll.

### Spacing

| Token | Value |
|---|---|
| H-padding left | 96 px |
| H-padding right | 80 px |
| V-padding | 32 px |
| Header height | 54 px |
| Card gap | 20 px |
| Card inner padding | 32 px |
| Border radius | 4px |
| Rule thickness | 1 px |
| Accent border | 3 px |

---

## 13. Checklist

Before sharing a deck, verify every item.

### Brand & tokens
- [ ] Logo on every slide (cover top-right, content `.shd` right end)
- [ ] Colours: only system tokens — no ad-hoc hex values
- [ ] All bespoke elements built from system tokens only
- [ ] No emoji — typographic symbols (✓ − ! ×) are fine
- [ ] Inter 300–900 (italic 300) loaded; no serif or display fonts
- [ ] Cover subtitle: Inter 300 italic
- [ ] No campaign-chrome hero gradients leaked from stripe.com — the deck cover is monochrome navy, not blurple

### Typography & readability
- [ ] No text below 12px
- [ ] Slide titles ≥ 50px (38px only on dense multi-line exceptions)
- [ ] Body text ≥ 16px on non-table slides
- [ ] Subtitles ≥ 20px

### Slide structure
- [ ] Every content slide has `.shd` header strip with slide number + logo
- [ ] Cover has no decorative lines
- [ ] Every slide fits within 720px

### Fit contract (§5.1)
- [ ] `.slide` AND `.sw .sc` both carry `overflow: hidden`
- [ ] Every flex:1 absorber ALSO carries `overflow: hidden` AND `min-height: 0`
- [ ] Vertical stack inside `.sc` has exactly **one** `flex: 1 1 0` absorber
- [ ] Sum of natural-section heights + gaps ≤ 602 px
- [ ] Visible bottom gap from last content to deck edge ≥ 20 px
- [ ] Verified at native **1280 × 720** render

### Components & interaction
- [ ] Flip cards click-to-toggle on mobile (JS `onclick` toggles `.on`)
- [ ] Tables: no coloured badges in cells — text colour only
- [ ] Card tier matches content density

### Visual & imagery
- [ ] Images serve comprehension — no decorative stock photos
- [ ] Image captions use `.cap` style

### Animation
- [ ] Entrance animation plays on slide activation
- [ ] Entrance animation total time per slide ≤ 2s
- [ ] No entrance animation loops

### Responsive (mobile parity)
- [ ] All multi-col layouts collapse to 1-col at ≤ 768px
- [ ] No inline `display:flex` without a matching catch-all in mobile CSS
- [ ] Touch swipe works (48px threshold)
- [ ] Tap targets ≥ 44×44px on mobile
- [ ] Flip cards work via tap on mobile
- [ ] Browser tested at **375px width** before declaring done
