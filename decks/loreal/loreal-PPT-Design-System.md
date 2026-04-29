# L'Oréal-PPT-Design-System

> The visual language for all decks produced for L'Oréal. Follow it precisely so every new deck is immediately recognisable as part of the same family.

---

## 1. Design Philosophy

**L'Oréal's visual language is *Parisian editorial gravitas*. Every deck reads like a page torn from a serious beauty annual: generous white surfaces, large light-weight serif italics for the moments that matter, restrained black sans for everything else, and a single warm stone-beige chord that lifts the whole composition out of corporate monochrome into luxury. There are no decorative gradients, no rounded SaaS chrome, no bright accent splashes — the brand expresses confidence by leaving things out, not by adding them.**

**Two modes:**
- **Desktop (≥ 769 px)**: 1280 × 720 px canvas, scale-to-fit (§5 runtime), keyboard / click navigation.
- **Mobile (≤ 768 px)**: all slides stack vertically as a scrollable page; single-column layouts.

### Design taste <!-- ENGINEERING-DNA: design-taste -->

**Commit to a clear aesthetic point of view.** This DS is a brand instrument, not a generic SaaS template. Every deck made from it should be unmistakably *L'Oréal* on first glance — not "another tasteful business presentation." Bold maximalism and refined minimalism both succeed; the failure mode is timidity.

**Anti-AI-slop rules** (apply on every slide, every component, every variant):

- **No generic font defaults.** Cormorant Garamond (display) and Inter (body) are the named typefaces in §3 and must be used. Fallbacks are spelled out — never let the cascade decay into Arial / system-ui as the "design choice".
- **No cliché palettes.** Pure-white + slate-grey + a single purple/blue accent is the AI-slop signature. The L'Oréal chord is **black + warm stone-beige (#CDC4BA) on paper white**. The stone is non-negotiable — without it the deck looks like a generic black-and-white annual report.
- **No even-weighted accent grids.** Six equal-weight rainbow accents look like a Storybook colour grid, not a luxury brand. The hierarchy is one dominant chord (black) + one signature warm (stone) + 2-3 semantic accents that carry distinct meaning. Use them with that hierarchy.
- **No off-the-shelf SaaS dashboard chrome.** L'Oréal CTAs are sharp 0-radius rectangles, no drop-shadow, no rounded corners. Any soft-radius button or boxy-shadow card breaks the editorial register. Match `--radius: 0` and `--shadow: flat`.
- **No vague mood language in copy.** "Modern, clean, bold" describes everything and therefore nothing. Slide titles speak in the L'Oréal corporate register: declarative, scientific, slightly aspirational. ("A Deep Dive Into Beauty", "The Adventure of Beauty", "Our Global Brands Portfolio".)
- **One orchestrated entrance, not scattered micro-interactions.** A staggered slide-content reveal on activation is the only motion most slides need; do not bolt hover wiggles onto every card. Editorial decks earn their gravitas by being still.

### Constraints vs Freedom <!-- ENGINEERING-DNA framing; bullet contents are BRAND-VARIABLE -->

This Design System defines **hard constraints** (what you must never break) and **reusable components** (what you can reach for). It does NOT define recipes — every slide should be composed for its specific content, not assembled from a template.

**Hard constraints (locked):**
- Colour palette (§2 tokens only — no ad-hoc colours)
- Inter typeface for chrome / body / data; Cormorant Garamond reserved for display headlines, hero pullquotes, italic editorial moments. No third typeface.
- 12px readability floor
- Logo on every slide
- **Every slide content lives inside a `.sc` container** (even bespoke full-bleed Type J / Type A compositions). The `.sc` is what `fit_contract_intact` measures — bespoke layouts that draw straight into a custom shell silently bypass absorber detection, mobile catch-all, and the 602 px content budget. No `.sc`, no contract.
- **Logo `<symbol>` must contain no inner `fill` attributes** (including `fill="none"` on wrapper `<g>` elements). Any inner fill overrides the `currentColor` cascade and renders the wordmark fully invisible — while every byte-level check still says PASS. `embed_logo.py` strips these on materialization; the `logo_renders` hard check rejects any that survive.
- No emoji (👍🎉 etc.) — typographic symbols (✓ − ! ×) and geometric indicators are permitted
- No decorative stock imagery — L'Oréal photography is editorial portrait or product macro only
- `.shd` header strip on content slides
- `.sw` border-left accent (3px solid `--accent` stone — sets the warm tone)
- Border-radius is **0 everywhere**. Sharp edges, never rounded.
- Shadows are **forbidden on cards**. Editorial typesetting has no shadow; only the flip-card hover state may carry a 6px shadow as a tactile reveal cue.

**Reusable components (reach for, don't force):**
- §7 Component Library provides cards, tables, charts, tabs, marks — use them when they fit. Skip them when a bespoke layout serves the content better.

**Bespoke elements (encouraged):**
- **Invent freely** within the colour palette. A full-bleed black cover with a single Cormorant italic cover line floating in the upper third; a stone-banded section divider with the chapter eyebrow set in tracked sans; a pullquote slide with one 64px italic line and nothing else — all of these are in-system if they only use the §2 tokens, the §3 type, and respect the §3 readability floor.
- The test is: does the element use only the defined colour tokens, the brand typeface, and respect the readability floor? If yes, it's in-system even if it doesn't match any named component.
- **Do not self-restrict to the named components.** If a slide needs something that doesn't exist in §7, design it from the tokens. The best L'Oréal slides are bespoke compositions built from system tokens.

---

## 2. Colour Tokens <!-- BRAND-VARIABLE: hex values + brand-palette names; core role token names are invariant -->

The token system has three layers:

1. **Core role tokens** — invariant names across every brand. They identify *what role* the colour plays, not *what colour it is*. A red brand's `--primary` is red; a blue brand's `--primary` is blue. L'Oréal's `--primary` is black.
2. **Semantic tokens** — invariant names; encode meaning (positive / negative / warning / informational) rather than colour identity.
3. **Brand palette tokens** — brand-specific names AND hex values. For L'Oréal these capture the warm-monochrome accents the corporate site actually uses.

```css
:root {
  /* ── Core role tokens (invariant names) ── */
  --primary:  #000000;   /* Dominant brand chord — cover bg, primary mark colour, big headline ink */
  --accent:   #CDC4BA;   /* L'Oréal signature warm stone — section bands, hairlines, eyebrow accents, callout borders */
  /* ── Neutrals ── */
  --surface:  #FFFFFF;   /* Paper / slide bg — uncompromisingly white */
  --white:    #FFFFFF;
  --ink:      #1A1A1A;   /* Body text on light surfaces — slightly off-pure-black for editorial warmth */
  --mid:      #6D6D6D;   /* Secondary text / muted labels / captions */
  --rule:     #D8D8D8;   /* Dividers / hairlines — thin and quiet */
  --tint:     #F4F4F4;   /* Subtle row / section bg / fog grey */
  /* ── Semantic (invariant names; values may map to brand-palette colours) ── */
  --green:    #468254;   /* Positive / sustainability — matches loreal.com For-The-Planet pages */
  --green-bg: #E5EFE7;
  --red:      #B23A48;   /* Negative — restrained editorial red, never neon */
  --red-bg:   #F4E4E5;
  --warn:     #B57E2F;   /* Warning / caution — bronze, befits beauty palette */
  --warn-bg:  #F5EBD9;
  --teal:     #2E3644;   /* Informational dark-navy from recon — alternative to pure black for image overlays */
  --teal-bg:  #E5E8EE;
  /* ── Brand palette (L'Oréal-specific names) ── */
  --stone:      #CDC4BA;   /* Same value as --accent; named for explicit semantic use */
  --stone-soft: #E8E2DA;   /* Lighter stone for tinted bands and back-of-card surfaces */
  --link-blue:  #3860BE;   /* Inline links and the rare saturated CTA */
  --deep-navy:  #2E3644;   /* Editorial image-overlay dark, alternative to pure black */
  --fog:        #F4F4F4;   /* Banded section background, same as --tint */
  --radius:     0;          /* Sharp — every corner */
}
```

**Rules:** <!-- ENGINEERING-DNA -->
- **Token names are role abstractions, not colour names.** `--primary` is the brand's dominant chord regardless of whether that chord is navy / red / yellow / black. Slide CSS reads `var(--primary)` and gets the right colour for whichever brand DS it's loaded against.
- **One *dominant* accent colour per slide.** Use `--accent` (stone) for the slide's signature highlight (callout border, eyebrow tint, section band). Brand-palette tokens (e.g. `var(--link-blue)`) are reach-for-when-needed decoration, not parallel accents — at most one decorative brand-palette colour per slide.
- **Semantic colours coexist when they carry distinct, opposing meaning** — e.g., a comparison slide with ✓ (`--green`) / ✗ (`--red`) marks. Otherwise pick one.
- **`--tint` is for rows, not card fills.**
- **Never pure black for backgrounds without intent.** `--primary` (#000) IS pure black for L'Oréal — but use it deliberately on covers and pullquote slides, not as a default body background.
- **Never ad-hoc hex literals in slide CSS.** Every colour must come from a token (core / semantic / brand palette). The `token_only_colors` hard check enforces this.

---

## 3. Typography <!-- BRAND-VARIABLE: font family + fallback; the scale below is mostly invariant -->

**Inter** — sole sans typeface for body, chrome, data, lists, captions, badges. Weights 300–900. Open-source proxy for L'Oréal's proprietary HelveticaNowDisplay; the visual register is near-identical at body sizes.

**Cormorant Garamond** — display serif, reserved for cover headlines, slide-title hero moments, full-bleed pullquotes, and italic editorial flourishes. Weights 300–700, italic available. Open-source proxy for L'Oréal's proprietary Halesworth; both are fashion-magazine-style high-contrast serifs and pair the same way against Inter.

> Type philosophy: L'Oréal slides earn their gravitas through restraint. Use Cormorant Garamond *only* where editorial impact is intended — covers, pullquotes, slide-title moments where the headline is the whole composition. Everywhere else, Inter handles the work invisibly. Mixing the two is allowed (and encouraged) on cover slides, where a Cormorant italic headline sits above an Inter eyebrow / subtitle. Never use Cormorant for body lists, table data, or chrome — it loses crispness below ~22 px.

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600&display=swap');

:root {
  --font-body:    'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-display: 'Cormorant Garamond', 'Times New Roman', Times, serif;
}
body, .slide, .sw, .sc { font-family: var(--font-body); }
.cov-title, .pq-line, .stitle.serif { font-family: var(--font-display); font-weight: 400; font-style: italic; letter-spacing: -.005em; }
```

### Type scale <!-- ENGINEERING-DNA — sizes are invariant; the scale is what makes decks readable -->

| Role | Size | Weight | Letter-spacing | Notes |
|---|---|---|---|---|
| Cover headline | 82 px | 900 | −0.03 em | Line-height 0.98 — Cormorant 400 italic for editorial covers |
| Cover subtitle | 22 px | 300 italic | +0.01 em | Inter 300 italic |
| Slide title | 50 px | 900 | −0.025 em | Line-height 1.06 — Inter 900 default, Cormorant italic 400 for hero/pullquote moments |
| Slide subtitle | 20 px | 600 | +0.01 em | `--mid` |
| Eyebrow / badge | 11–12 px | 800 | +0.18–0.24 em | ALL CAPS — sets the editorial chapter feel |
| Card headline | 28 px | 900 | −0.01 em | |
| Body / list | 16 px | 600 | default | Line-height 1.5–1.6 |
| Table / data | 13–14 px | 700–800 | +0.1 em | ALL CAPS for headers |
| Caption / meta | 12–13 px | 700–800 | +0.14 em | Never below 12 px |

### Readability <!-- ENGINEERING-DNA -->

1. **Maximise**: Default to the largest size that fits. Half-empty slide with 14px body = design failure.
2. **Floor**: Nothing below 12px <!-- ENGINEERING-DNA: typography-floor -->. If content doesn't fit at min sizes, change layout — never shrink font.

| Role | Minimum | **Enforced default** |
|---|---|---|
| Slide title | 38 px | **50 px** — only shrink for multi-line on dense slides |
| Card headline | 22 px | **28 px** |
| Primary body / list | 14 px | **16 px** — slide-level paragraphs, main content |
| Component secondary | 13 px | **13–14 px** — descriptions inside cards, list item details |
| Subtitle | 16 px | **20 px** |
| Badges / labels | 12 px | **13 px** |

**Enforcement**: Title below 50px or primary body below 16px on a slide's main content area is a bug. Component-internal secondary text may use 13–14px to maintain visual hierarchy.

### 3.1 Typography Safety <!-- ENGINEERING-DNA: typography-safety -->

Slide "looks good" is engineering-quantifiable. The rules below are hard rules; the `text_layout_safe` auto-check enforces most of them.

1. **Never glued to the bottom edge**: the lowest visible text element on a content slide must be ≥ 18px from the slide's bottom (target 24–48px). Keep `padding-bottom` on `.sw` / `.sc` as a guardrail; do not push content to the edge.
2. **Never truncated**: any text container with `overflow:hidden` must have `scrollHeight ≤ clientHeight`. If content might overflow, use `text-overflow: ellipsis` or `-webkit-line-clamp` and explicitly declare the allowed max line count — never "bet" that it just fits.
3. **Never broken across lines arbitrarily**: H1/H2/H3 single titles ≤ 3 lines; body paragraphs ≤ 5 lines. For CJK titles, avoid mid-phrase wraps — use `word-break: keep-all; line-break: strict;` paired with shorter copy.
4. **Global layout law** (the basics):
   - Disable `hyphens: auto` globally (it produces broken hyphens in mixed-CJK environments).
   - `line-height` ≥ 1.4 for body, ≥ 1.15 for headings — never tighter.
   - Minimum 12px spacing between cards / paragraphs; two text blocks must never touch.
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

## 4. L'Oréal Logo <!-- BRAND-VARIABLE: SVG payload is brand-specific; surrounding pattern + multi-format support is ENGINEERING-DNA -->

### Definition (once per HTML file)

The logo must be a real brand identity asset, **fully inlined** into the HTML (no external network dependency). Two embed paths are allowed; `embed_logo.py` picks one automatically:

**A. SVG vector path** (the form L'Oréal uses) — the canonical wordmark inline-SVG was extracted from the loreal.com `<header>` and quality-gated; viewBox is `0 0 137 36`, 9 paths, no inner `fill` attributes (so `currentColor` cascades correctly on both light and dark covers):

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 137 36" fill="currentColor">
    <title>L'Oréal Groupe</title>
    <g clip-path="url(#clip0)">
      <path d="M100.545 34.7024V32.7235H103.601V31.5326H100.545V29.6927H104.321V28.5014H99.2406V35.8927H104.321V34.7018L100.545 34.7024ZM89.7172 29.7161C89.8919 29.7058 90.0669 29.732 90.2313 29.7931C90.3957 29.8542 90.5462 29.9489 90.6734 30.0714C90.8007 30.1938 90.902 30.3415 90.9713 30.5054C91.0406 30.6692 91.0764 30.8457 91.0764 31.0241C91.0764 31.2026 91.0406 31.3791 90.9713 31.5429C90.902 31.7068 90.8007 31.8545 90.6734 31.9769C90.5462 32.0994 90.3957 32.1941 90.2313 32.2552C90.0669 32.3163 89.8919 32.3425 89.7172 32.3322H87.7664V29.7161H89.7172ZM86.4626 35.8947H87.7664V33.5339H89.7067C91.3341 33.5339 92.3875 32.5448 92.3875 31.0026C92.3875 29.4925 91.3236 28.5034 89.7067 28.5034H86.4619L86.4626 35.8947ZM73.0376 28.5034V33.034C73.0376 34.8525 74.3312 36.0013 76.167 36.0013C78.0028 36.0013 79.2965 34.8525 79.2965 33.0447V28.5034H78.0031V33.0447C78.0031 34.0445 77.3148 34.7676 76.1677 34.7676C75.0412 34.7676 74.3424 34.0445 74.3424 33.034V28.5021L73.0376 28.5034ZM62.5024 34.7676C61.8515 34.7414 61.2359 34.4593 60.7844 33.9805C60.333 33.5017 60.0809 32.8634 60.0809 32.1992C60.0809 31.5351 60.333 30.8967 60.7844 30.4179C61.2359 29.9391 61.8515 29.6571 62.5024 29.6309C63.8689 29.6309 64.9118 30.6838 64.9118 32.2039C64.9283 32.5359 64.8781 32.8679 64.7642 33.1795C64.6504 33.491 64.4752 33.7755 64.2496 34.0155C64.024 34.2556 63.7526 34.446 63.4522 34.5752C63.1517 34.7044 62.8285 34.7697 62.5024 34.7669V34.7676ZM62.5024 28.3965C61.7657 28.3996 61.0465 28.6251 60.4353 29.0445C59.8242 29.4639 59.3486 30.0585 59.0686 30.7532C58.7885 31.4479 58.7165 32.2116 58.8618 32.9479C59.007 33.6843 59.3628 34.3603 59.8844 34.8907C60.4061 35.421 61.0701 35.782 61.7927 35.9281C62.5154 36.0741 63.2642 35.9987 63.9449 35.7113C64.6255 35.4238 65.2074 34.9373 65.6171 34.3131C66.0268 33.6889 66.246 32.955 66.2471 32.2039C66.2581 31.6999 66.1688 31.1989 65.9844 30.7312C65.8 30.2635 65.5244 29.8388 65.1743 29.4828C64.8242 29.1268 64.4069 28.847 63.9476 28.6603C63.4884 28.4736 62.9967 28.3838 62.5024 28.3965ZM49.432 29.7161C50.3081 29.7161 50.788 30.2477 50.788 30.9191C50.788 31.6208 50.3186 32.1528 49.432 32.1528H47.69V29.7161H49.432ZM46.3862 35.8947H47.69V33.3638H49.1816L51.0279 35.8947H52.5717L50.474 33.0764C50.9519 32.9521 51.3739 32.665 51.6698 32.2628C51.9658 31.8605 52.118 31.3672 52.1013 30.8646C52.1013 29.4277 51.0479 28.5034 49.4206 28.5034H46.3852L46.3862 35.8947ZM39.3869 31.8848H36.2679V32.9802H38.1657V34.4478C37.673 34.681 37.1337 34.7939 36.5908 34.7776C35.0992 34.7776 33.9933 33.8203 33.9933 32.1932C33.9832 31.8557 34.0406 31.5195 34.1621 31.2053C34.2835 30.8911 34.4664 30.6054 34.6996 30.3656C34.9329 30.1258 35.2116 29.937 35.5187 29.8105C35.8259 29.6841 36.1551 29.6227 36.4862 29.6302C36.8612 29.6186 37.2345 29.6842 37.584 29.8231C37.9335 29.962 38.252 30.1713 38.5203 30.4385L39.2925 29.4494C38.5256 28.7419 37.52 28.3646 36.4862 28.3965C34.3168 28.3965 32.6685 30.0024 32.6685 32.1932C32.6685 34.5009 34.2958 36.0007 36.5908 36.0007C37.5824 36.0109 38.555 35.7223 39.3862 35.1709L39.3869 31.8848Z"></path>
      <path d="M74.5328 23.5709H92.2115V21.3704H77.5623V14.3242H88.5655V12.0971H77.5623V5.60695H92.2102V3.41217H74.5328V23.5709Z"></path>
      <path d="M83.7195 0.153748L81.3269 2.89388L88.8408 0.153748H83.7195Z"></path>
      <path d="M119.128 3.41278V23.5701H137V21.3697H121.89V3.41278H119.128Z"></path>
      <path d="M103.667 3.41278L93.6141 23.5711H97.012L99.5839 18.3535H111.642L114.236 23.5711H117.6L107.537 3.41278H103.667ZM100.856 15.8272L105.593 6.19869L110.387 15.8272H100.856Z"></path>
      <path d="M64.939 15.1426C69.4689 13.9105 69.9085 10.4727 69.8862 9.24462C69.6161 5.64402 67.2359 3.41315 62.96 3.41315H50.4976V23.5705H53.3386V15.1132H61.4513L67.4191 23.5675H71.0009C71.0009 23.5675 66.7072 17.877 64.939 15.1396V15.1426ZM62.5716 12.7296H53.3386V5.79907H62.8941C65.092 5.79907 66.3306 6.84567 66.7761 8.17564C66.9088 8.66415 66.9434 9.17496 66.8779 9.67744C66.8123 10.1799 66.6479 10.6637 66.3946 11.0999C65.5958 12.4472 64.0793 12.7326 62.5716 12.7326"></path>
      <path d="M33.3292 22.7688C27.7809 22.7688 23.2103 18.2242 23.2103 12.7483C23.2103 7.27906 27.5649 2.51658 33.5442 2.51658C34.869 2.50541 36.1829 2.76184 37.41 3.27105C38.6371 3.78026 39.7531 4.53217 40.6937 5.48341C41.6343 6.43464 42.3808 7.56636 42.8902 8.81326C43.3996 10.0602 43.6617 11.3976 43.6615 12.7483C43.6615 18.2236 38.8762 22.7688 33.3292 22.7688ZM33.4253 0C25.4066 0 19.9403 5.76464 19.9403 12.7413C19.9403 20.0865 25.9789 25.2724 33.4253 25.2724C40.8716 25.2724 46.9034 20.1614 46.9034 12.7413C46.9034 5.76464 41.3705 0 33.4253 0Z"></path>
      <path d="M12.7863 10.5438H14.8355L18.5565 3.41315H15.5625L12.7863 10.5438Z"></path>
      <path d="M0 3.41278V23.5701H17.8704V21.3697H2.76465V3.41278H0Z"></path>
    </g>
    <defs><clipPath id="clip0"><rect width="137" height="36"></rect></clipPath></defs>
  </symbol>
</svg>
```

> ⚠️ **fill-cascade pitfall** <!-- ENGINEERING-DNA: logo-inner-fill -->
> Many brand-site SVG exporters wrap real glyph paths inside a defaulting group:
> `<g fill="none" fill-rule="evenodd"><g><path d="..."/></g></g>`. Pasted as-is into our
> `<symbol fill="currentColor">`, the inner `fill="none"` **wins** over the parent
> currentColor cascade — the wordmark renders 100% invisible while every byte-level
> check (path-d length, viewBox, even `visible_on_cover` via getBoundingClientRect)
> still says PASS. **Strip every inner `fill` attribute (including `fill="none"`)
> before embedding.** `embed_logo.py` does this automatically; if you ever hand-paste
> a logo, do it manually. The `logo_renders` hard check rejects any inner `fill` other
> than `fill="currentColor"`.

**B. PNG/JPG/WebP base64 embed** (raster fallback) — when only a raster logo is available (minimum 64×64), base64-encode it and wrap it in the same `<symbol>` via `<image href>`:

```html
<svg style="display:none" xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true">
  <symbol id="brand-wm" viewBox="0 0 LOGO_W LOGO_H">
    <image href="data:image/png;base64,LOGO_BASE64" width="LOGO_W" height="LOGO_H"/>
  </symbol>
</svg>
```

> ⚠️ **Typographic placeholders are forbidden**: faking a logo with `<text>` of the brand name (e.g. `<text>L'ORÉAL</text>`, a generic disc-with-letter) is a build failure. The `logo_renders` hard check rejects `<symbol>` blocks that contain only `<text>`. If no source produces a real logo, **stop and ask the user** for an original file — never invent a placeholder.

Source resolution order (the actual order `embed_logo.py` tries):
1. Inline SVG inside the page's `<header>` (filtered to drop utility icons with viewBox < 60px)
2. Wikipedia infobox logo file for the brand
3. apple-touch-icon (typically ≥ 180px PNG)
4. favicon (SVG or PNG)
5. og:image / twitter:image
6. Common path guesses (/logo.svg, /assets/logo.svg, …)

### Usage

```html
<!-- White (on dark / black slides) -->
<svg class="logo W" viewBox="0 0 137 36" aria-label="L'Oréal">
  <use href="#brand-wm"/>
</svg>

<!-- Brand-dark (on light slides) -->
<svg class="logo L" viewBox="0 0 137 36" aria-label="L'Oréal">
  <use href="#brand-wm"/>
</svg>
```

```css
/* fill: currentColor must be on .logo — NOT on .logo path.
   CSS selectors do not pierce SVG <use> shadow DOM.
   Inherited fill on the outer <svg> cascades in correctly. */
.logo   { height: 18px; width: auto; flex-shrink: 0; fill: currentColor; }
.logo.W { color: #fff; }
.logo.L { color: var(--primary); }
```

### Placement rules <!-- ENGINEERING-DNA -->
- **Every slide** must carry the logo — cover and all content slides.
- **Cover**: top-right corner of the `.cov-top` flex row.
- **Content slides**: right end of the `.shd` header strip (left = title eyebrow / slide number, right = logo).
- Minimum clear space around the logo = logo height (18 px) on all sides.
- Never stretch, recolour outside `W`/`L`, or overlay the logo on a patterned area.

> **L'Oréal brand-restriction note**: The L'Oréal Groupe wordmark is a trademark of L'Oréal SA. Use this DS to build internal communications, partner decks, and editorial pieces. Do **not** reproduce the wordmark on consumer-facing product packaging, retail signage, or paid advertising without legal sign-off from the L'Oréal brand team. The DS captures the *visual register* of the corporate site so partner content feels coherent — it is not a substitute for the official L'Oréal Brand Guidelines.

---

## 5. Slide Architecture <!-- ENGINEERING-DNA — the entire section, invariant -->

### Scaffold
```
#wrap — fixed fullscreen, flex-centre, background: var(--ink)
  #deck — 1280 × 720, position:relative, overflow:hidden (hard contract)
    .slide × N — absolute inset, opacity show/hide, overflow:hidden (hard contract)
```

`#wrap` and `body` background **must use `var(--ink)`**, not hardcoded `#000` / `#1A1A1A` / `#1F1F22` — those get caught by `token_only_colors`. L'Oréal's `--ink` (#1A1A1A) is intentionally a hair softer than pure `--primary` black, so the letterbox feels editorial rather than industrial.

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
.shd-num { font-size: 11px; font-weight: 800; letter-spacing: .2em; text-transform: uppercase; color: var(--ink); }
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
2. **Estimate natural heights** using the type scale.
3. **Sum fixed sections + gaps**. Confirm total ≤ (602 − absorber minimum).
4. **Write the copy short enough that single-line bullets don't wrap**.
5. **Render at 1280×720 and eye the bottom edge.** Not at 1920×1080 (the `transform: scale()` masks overflow by rescaling). The native canvas is the source of truth.

#### Anti-patterns that cause overflow

- **N natural-height sections with no absorber**: total exceeds 602 px, content leaks past the deck.
- **Absorber without `min-height: 0`**: flex refuses to shrink it below content's natural size.
- **Absorber without `overflow: hidden`**: oversized children push through the flex:1 and break the parent.
- **Omitting `overflow: hidden` on `.slide`/`.sc`**: if any math is slightly off, content bleeds outside the deck onto the body.
- **Trusting the 1920×1080 render**: the `transform: scale()` shrinks everything uniformly — always verify at native 1280×720.

---

## 6. Slide Types <!-- BRAND-VARIABLE: emphasis order varies; the type definitions are mostly invariant -->

> **Emphasis for L'Oréal**: lean into editorial register, not data-dashboard register. The corporate site speaks through portrait photography, italic display serif, and quiet typesetting; decks should mirror that.
> Foreground these types when designing decks: **Type J pullquote** (full-bleed Cormorant italic anchor moments), **Type F image hero** (editorial portrait or product macro at full bleed), **Type B two-column** (parallel narrative for mission / heritage / brand-portfolio chapters).
> Use sparingly: **Type D flip cards** — interactive flips fight the editorial calm. Reserve for genuinely binary myth/reality moments. **Type G interactive demo** — almost never appropriate for L'Oréal.

### Type A — Cover
- Background: `var(--surface)` paper white (default editorial cover) OR `var(--primary)` black for a "campaign launch" / "annual letter" register.
- Structure: Logo top-right → small ALL-CAPS Inter eyebrow ("THE GROUPE", "ANNUAL REPORT 2025") → Cormorant italic giant headline ("A Deep Dive Into Beauty") → Inter 300 italic subtitle → meta row (date, author, location).
- **No decorative lines of any kind** — no hairlines, no accent lines, no gradient borders. The background is the surface; the type carries the slide.

### Type B — Two-column content
Comparisons, parallel narratives, mission-and-vision pairings. `grid-template-columns: 1fr 1fr; gap: 32px` (wider than default 20 px — editorial breathing). Collapses on mobile. Optional thin `var(--rule)` vertical hairline between columns for editorial typeset feel.

### Type C — Full-width narrative
Single column, large type, pull-quotes. For context, summary, recommendation slides.

### Type D — Flip cards *(de-emphasised on L'Oréal — use with restraint)*
Two cards side-by-side. Front = `--primary` (black), back = `var(--deep-navy)` (#2E3644 — softer than pure black, still dark enough to feel editorial). **Hover + click flip** — JS `onclick` toggles `.on` class (required for mobile). Ghost Roman numerals on front. Spacious back (32px padding, ≤ 4 content elements).

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
Slide dominated by a table or structured data grid. The table component spec (§7.7) defines the element-level design; this type defines when to use it and how to lay out the slide around it.

**Principles:** The table is the star — title + table + optional one-line callout below. No side panels competing for attention. If the table has 6+ columns, let it span full width.

**Row-count rule** <!-- ENGINEERING-DNA: type-e-row-count -->
- 5 rows is the comfortable count at standard 14 px row-padding (cell `padding: 14px 18px`).
- 6+ rows require either (a) tightening cell padding to `padding: 10px 16px` or (b) splitting the data across two slides.
- If the table needs 6+ rows AND a side callout in the absorber, split. Don't pack.

### Type F — Image slide *(emphasised on L'Oréal)*
One or more images dominate the slide, with text anchored to a calm area. L'Oréal's editorial photography (portrait, product macro, ingredient still life) is the brand's strongest visual asset — deck designers should lean on it.

**Principles:**
- Images must serve comprehension — no decorative stock. Prefer: real product UI, real data visualisations, contextual photos that illustrate a specific point. For L'Oréal, lean toward editorial portrait + product macro.
- When building a deck, **actively web search for relevant images** (product logos, UI screenshots, real-world examples) that support the narrative.
- Image treatment: `border-radius: 0` (sharp — matches the rest of the L'Oréal system), no border on dark backgrounds, optional `1px solid var(--rule)` hairline on light backgrounds.
- Layout: image fills 50–70% of slide area. Text sits beside or overlaid on a tinted region. Never place text over a busy image without a `rgba(0,0,0,.55)` scrim.
- Caption below image: `.cap` style (12px, 800 weight, ALL CAPS, `--mid`, +0.18em letterspacing).

### Type G — Interactive demo
A self-contained, click-to-advance micro-experience embedded in a slide. Almost never appropriate for L'Oréal corporate decks; reserve for product-team internal pieces.

**Structure:** A "screen" area (dark bg `--primary` or `--deep-navy`, 0px radius) with step-by-step content. Controls: forward/back buttons or numbered steps. CSS transitions only.

**Design rules:**
- Must feel like a polished product demo, not a prototype.
- CSS `@keyframes` only — no JS animation libraries. Keep under 50 lines of CSS per demo.
- Each step should be one clear idea. Max 5 steps per demo.
- Mobile: auto-advance on scroll or tap targets ≥ 44px.

### Type H — Chart / data insight slide
Slide led by one or more data visualisations. L'Oréal is a public company with rich annual-report data — sales by division, geography, sustainability metrics. Charts should feel typographic, not dashboard-y.

**Principles:**
- One primary chart per slide. A secondary small chart is acceptable if it directly supports the primary.
- Title states the insight, not the chart type. Good: "Asia drove 38% of 2024 growth". Bad: "Bar Chart Comparison".
- Chart fills 50–70% of slide area. Remaining space: title + one paragraph of interpretation or a callout.
- Use `--accent` (stone) as the dominant chart fill; `--primary` (black) as the comparison/highlight. Avoid the saturated brand-palette colours in charts — they break the editorial calm.
- Animate on entrance for narrative impact.

### Type I — Tabs slide
Multiple content views switchable via tabs. Tab component spec in §7.9. Max 4 tabs.

### Type J — Quote / pullquote *(emphasised on L'Oréal)*
A single striking statement that anchors a narrative moment. THE signature L'Oréal slide type — "Because You're Worth It" energy. Used for key takeaways, brand-philosophy moments, mission-statement reframes.

**Structure (standard):** Large Cormorant italic quote text (44–56px, weight 400, italic, `--ink`), centred or left-aligned with generous side margins. Optional attribution below in Inter 13 px ALL CAPS tracked. Left border accent (`3px solid var(--accent)`) — subtle stone bar, not a heavy block.

**Structure (full-bleed bespoke variant):** L'Oréal's most powerful slide is a full-bleed `--primary` (black) cover with a single Cormorant italic line floating slightly above visual centre. When you do this:

1. **The composition still goes inside `.sw + .sc`.** Use `.sw` (with `background: var(--primary)` overriding the default) and a single `.sc` containing your bespoke layout. Do **not** invent a sibling shell class (`.fpwrap`, `.poster-wrap`, etc.) — bespoke shells silently bypass `fit_contract_intact` (no `.sc` = no absorber count = `bad_slides: [{absorbers: 0}]`).
2. **Exactly one absorber** inside the `.sc` carries `flex: 1 1 0; min-height: 0; overflow: hidden` — usually the middle band that holds the big italic line. Header (eyebrow + logo) and footer (attribution) are `flex: 0 0 auto`.
3. **Cap line size by row count.** For a single-line Cormorant italic centred at 64px on a 720-deck, `clientH` of the absorber is `(720 − 54 header band − 32 top − 40 bottom) − 0 (no footer) = 594`. A 64 px line at 1.1 line-height = ~70 px visual height — sits comfortably with ~262 px breathing room above and below. **Never let the headline exceed 80 px on a single line, or 56 px on a 2-line stack.**
4. **No header strip (`.shd`) on full-bleed Type J.** Put logo + slide-eyebrow inline at the top of `.sc` instead.

### Type K — Timeline / roadmap
Horizontal or vertical sequence of milestones. Used for L'Oréal's 100+-year heritage narrative, sustainability commitments roadmap, brand-acquisition history. Component spec in §7.12.

---

## 7. Component Library <!-- ENGINEERING-DNA — every component preserved verbatim -->

Reusable elements available on **any** slide type. A slide may combine multiple components, or use none — building bespoke layouts from colour tokens and type scale instead. The library is a toolkit, not a constraint.

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
.show-card.accent-primary { border-top-color: var(--primary); }
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
- **Icon circle**: small circle (24px) with symbol (`!`, `✓`, `→`).
- **Letter / label**: single letter or short label in same ghost style.

### 7.4 Stat Card (Tier 4 — "number card")

Compact metric display. `stat-num` (36px 900 `--primary`) + `stat-label` (12px 800 ALL CAPS `--mid`).

### 7.5 Callout / Note

**Light** (inline note):
```css
.snote { border-left: 3px solid var(--primary); padding: 10px 18px; background: var(--tint); font-size: 14px; font-weight: 700; color: var(--ink); }
```

**Dark** (conclusion / recommendation bar):
Full-width black block for slide-ending takeaways. Text: 13–16px 700–800, `rgba(255,255,255,.85)`. Bold key phrases with `color: #fff`. No border-left — the solid black fill IS the emphasis.

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
- Black header row is the only colour block. All data cells: white bg, `--ink` text.
- **No coloured badges in `<table>` cells** — use text weight/colour for emphasis instead.
- One optional `--tint` highlight row for the single most important row.
- The "clean grid" test: squint at the table. If you see a patchwork of coloured boxes, the design has failed.

### 7.8 Charts

| Type | Primary colour | Secondary | Neutral | Notes |
|---|---|---|---|---|
| Bar (H / V) | `--accent` (stone) | `--primary` (black) | `--rule` | Animated grow on entrance |
| Progress / gauge | `--accent` fill | — | `--rule` track | 8px height, **0px radius** (sharp) |
| Pie / donut | `--primary` | `--accent` | `--rule` | Max 3 segments |
| Timeline | `--primary` dots | — | `--rule` line | Key nodes: `--accent` ring |

Max 2 colours per chart (+ `--rule` neutral). Animate on entrance: bars grow, counters count up.

### 7.9 Tabs

```css
.tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.tb { padding: 7px 16px; border: 1px solid var(--rule); background: transparent; font: 800 12px/1 'Inter', sans-serif; letter-spacing: .06em; color: var(--mid); cursor: pointer; }
.tb:hover { border-color: var(--accent); color: var(--ink); }
.tb.on { background: var(--primary); border-color: var(--primary); color: #fff; }
.tc { display: none; } .tc.on { display: block; }
```

Max 4 tabs.

### 7.10 Sequential steps / barriers
Use numeric labels `01` `02` `03` in Inter 800, `--accent` colour, rather than bullet points or decorative emoji.

### 7.11 Decision questions
Prefix with `Q.1` / `Q.2` spans in `--ink`, weight 800, letter-spacing 0.12 em.

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
.tl-line { position: absolute; top: 73px; left: 30px; right: 30px; height: 1px; background: var(--rule); }
.tl-row { display: flex; position: relative; z-index: 1; }
.tl-node { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 4px; }
.tl-date-top {
  font-size: 22px; font-weight: 900; letter-spacing: -.01em; color: var(--ink);
  min-height: 48px; margin-bottom: 16px;
  display: flex; align-items: flex-end; justify-content: center;
}
.tl-dot2 { width: 14px; height: 14px; border-radius: 50%; background: var(--primary); margin-bottom: 12px; flex-shrink: 0; transition: transform .3s ease; border: 3px solid var(--surface); box-shadow: 0 0 0 1px var(--rule); }
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
| Brand heritage milestones | Timeline | horizontal flex |

---

## 8. Imagery & Visual Evidence <!-- BRAND-VARIABLE intro; rules are ENGINEERING-DNA -->

### Principle

L'Oréal is a beauty company; its visual evidence is photographic — editorial portraits of women across diverse backgrounds, product macro of formulations and packaging, archive imagery from the 100+-year heritage. Slides should treat photography as a peer to typography, never as decoration. When data drives the argument, render it as a typographic chart (Type H) using only `--accent` and `--primary`.

### When to include images

- **Editorial portraits**: Show the human face of beauty — diverse models, makeup artists, scientists. Use full-bleed Type F when the portrait IS the slide.
- **Product macro**: Specific formulation shots, lab-bench imagery, ingredient close-ups. Better than illustrations for "we make real products".
- **Archive heritage**: For history/timeline slides, source from the L'Oréal corporate archive (Eugène Schueller in his lab, vintage advertising plates).
- **Data visualisations**: When a number or trend is central, build a chart (Type H).
- **Diagrams**: When a concept has structure (layers, flows, comparisons), draw it with CSS/SVG rather than describing it in words.

### How to source images

1. **Search actively**: Use web search to find official L'Oréal corporate photography, archived ads, lab/production imagery. Prefer official assets over generic stock.
2. **CSS-drawn alternatives**: Bar charts, progress bars, timeline diagrams — preferable to external images when data is simple.
3. **Never use**: Decorative stock beauty photos (the genre is saturated with AI-slop), abstract gradients, AI-generated placeholder art, images that don't directly support the slide's point.

### Image treatment

- `border-radius: 0`. Sharp — every corner. Optional `1px solid var(--rule)` hairline on light backgrounds.
- Images on dark backgrounds: no border.
- Caption: `.cap` style below the image (12 px ALL CAPS Inter 800, +0.18em).
- Never place text over a busy image without a `rgba(0,0,0,.55)` minimum scrim.

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

1. **Pullquote moments for reframes**: a single Cormorant italic line beats three bullet points every time.
2. **Concrete over abstract**: specific scenarios beat generic descriptions.
3. **Visual evidence**: Charts > text. Photographs > descriptions. Diagrams > bullet lists.
4. **The screenshot test**: If no one would photograph this slide and put it in their feed, it needs a visual hook.

---

## 12. Layout Rules <!-- ENGINEERING-DNA -->

### Overflow prevention

Every slide fits 720px. If too dense: reduce gaps → reduce body to 14px → split slide. Never clip or scroll.

**The "blue block" trap**: Dark callout at bottom-right = visual imbalance. Move to full-width bottom, use `.snote` instead, or place dark cards at top.

**The "blue-on-navy" trap**: On dark slides (`--primary` bg), never use saturated brand-palette colours for text — it creates jarring, cheap-looking contrast. Use white (`#fff`) or semi-transparent white (`rgba(255,255,255,.85)`) for emphasis. For subtle CTAs on dark backgrounds, use `rgba(255,255,255,.08)` bg fill + white text. The L'Oréal exception: `--accent` (stone-beige #CDC4BA) DOES work on `--primary` (black) — it is the brand's signature warm-on-dark register, used sparingly for editorial eyebrows and hairlines on black covers.

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
| Border radius | 0 (sharp — every corner) |
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
- [ ] Inter 300–900 loaded; Cormorant Garamond loaded for display moments only
- [ ] Cover subtitle: Inter 300 italic only
- [ ] Border-radius is 0 on all components. Any rounded card is a bug.

### Typography & readability
- [ ] No text below 12px — check badge/label columns especially
- [ ] Slide titles ≥ 50px (38px only on dense multi-line exceptions)
- [ ] Body text ≥ 16px on non-table slides (14px only on data-dense tables)
- [ ] Subtitles ≥ 20px
- [ ] Cormorant Garamond never used below 22px (loses crispness)

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
