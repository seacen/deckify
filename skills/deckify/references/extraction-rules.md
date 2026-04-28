# Extraction rules — fallbacks when the deterministic pass comes up short

Read this when `extract_brand.py` couldn't surface enough signal — e.g., the brand site is mostly images, uses inline obfuscated CSS, sits behind a heavy framework wrapper that hides custom properties, or is a SPA whose initial HTML is mostly a `<noscript>` and a `<div id="root">`.

## When to consult this file

- `brand-recon.json` shows < 3 brand color candidates
- `computed_signal.root_color_vars` is empty
- `fonts` array is empty or only contains `Helvetica Neue` / `Arial` (sniffed from minified CSS)
- `logo_candidates` only has `path-guess` entries (everything else missed)

## Fallback heuristics

### Color, when CSS variables aren't exposed

1. **Re-screenshot at 1px stripe granularity.** Use `agent-browser eval` to find the dominant header background by sampling pixels:
   ```bash
   agent-browser eval '(()=>{const r=document.querySelector("header,nav").getBoundingClientRect();return JSON.stringify({bg:getComputedStyle(document.querySelector("header,nav")).backgroundColor,top:r.top,h:r.height})})()'
   ```
2. **Sample the hero `<section>`** for accent colors (often campaign-specific — note this in your hypothesis):
   ```bash
   agent-browser eval '(()=>{const h=document.querySelector("main section, [class*=hero i]");return h?getComputedStyle(h).backgroundImage||getComputedStyle(h).backgroundColor:null})()'
   ```
3. **Pull the favicon and read its dominant color visually** — for monogram brands the favicon is often the cleanest single source of brand color.

### Typography, when font-family declarations are missing

1. **Check `<link>` tags pointing at `fonts.googleapis.com`** — these are explicit, scriptable.
2. **Check `<link rel="preload" as="font">`** — same deal, names are usually in the URL.
3. **Look for `@font-face { font-family: "X" }` in CSS files** — `extract_brand.py` already covers this if CSS was fetched, but double-check by globbing all `.css` files in `$WS/recon/`.
4. **As a last resort, ask the user.** Don't guess — substituting the wrong font on slides looks worse than asking a quick question.

### Logo, when `download_logo.sh` returns nothing

The most likely failures and their workarounds:

| Failure | Why | Workaround |
|---|---|---|
| Inline header SVG present but extraction is empty | The SVG is wrapped in a `<picture>` or `<button>` and the regex didn't reach it | Use `agent-browser eval` with `document.querySelector('header svg, [class*=logo i] svg').outerHTML` |
| Favicon is a `.ico` with multiple sizes | `.ico` doesn't render well as logo on slides | Look for `apple-touch-icon` or `manifest.json icons[]` (often higher-res PNG) |
| Logo is loaded as a CSS background-image | Common on consumer brands | `agent-browser eval` to read `background-image` of the header element, then curl the URL |
| Logo is behind Cloudflare and bot-blocked | Common on enterprise sites | Tell the user; ask for a press-kit URL instead. Most brand sites have `/press`, `/brand`, `/media-kit` |

### Aesthetic mood — when the screenshots are confusing

If you're not sure how to describe the brand's mood after looking at the screenshots, batch-evaluate against the canonical archetypes from `decision-questions.md` (premium-editorial / engineering-clean / bold-colorful / minimal-monochrome / playful-illustrated / luxury-restrained / technical-dense). Pick the closest TWO and surface both as options to the user — they'll often pick one or the other immediately.

If you're VERY unsure, take an extra screenshot of an inner page like `/about` or `/values` — those are usually the most "brand-true" surfaces (the homepage chases conversion; the about page is what the brand wants to be remembered as).

## What NOT to do

- Don't fabricate color hex values. If `brand-recon.json` doesn't surface a needed token, leave it null in your hypothesis and surface it as a question to the user — don't invent #1A1A1A or any default.
- Don't substitute a "similar font" without flagging it. If the brand uses a font you don't recognize, ASK rather than picking a "vibe match" — the wrong font is the most-noticed substitution.
- Don't pick the homepage hero color as `--accent` (the accent) without checking the nav and footer first. Hero colors are often campaign-specific; the nav/footer/buttons usually carry the actual brand accent.
- Don't extract decorative gradient backgrounds as brand tokens. A 5-stop pink/orange gradient on a fashion brand homepage is a marketing campaign, not a token.
