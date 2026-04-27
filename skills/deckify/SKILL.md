---
name: deckify
description: Generate a complete HTML-slide Design System markdown file from a reference URL. Studies the page's color palette, typography, logo, and aesthetic mood, then writes a Design System that bakes in proven engineering rules (1280×720 fit contract, three-layer overflow safety net, single-absorber rule, mobile inline-flex trap catch-all, flip-card mobile fix, logo-as-SVG-symbol-with-currentColor pattern, 12px readability floor) while letting the brand identity drive the visuals. Use this whenever the user gives you a URL and asks to "build a design system from this site," "extract a design system from", "make slides like this brand," "skin slides to match this site's visual language," or wants to author HTML slides in the visual language of any specific website. Also use when the user names a brand site as a slide-deck reference, even if they don't say "design system" explicitly.
dependencies:
  - agent-browser  # Standalone CLI from Vercel Labs (https://github.com/vercel-labs/agent-browser). Install via npm/brew/cargo — see scripts/setup.sh. Used for URL fetch, computed-style introspection, screenshots in Phase 1. NOT the same as any plugin called "agent-browser" — this is the standalone binary at github.com/vercel-labs/agent-browser. Verify with `which agent-browser` and `agent-browser --version`.
  - python3        # Stdlib only. enumerate_assets.py and embed_logo.py post-process agent-browser output. No external deps.
  - curl           # Used by fetch_sitemap.sh to fetch /sitemap.xml.
---

# Web → Design System

Turn a reference URL into a production-ready Design System markdown that another agent (or you) can use to build precise, mobile-friendly HTML slides in the brand's visual language.

## Why this skill exists (read first)

"Make slides in the visual language of brand X" is deceptively hard. The naive approach — show Claude the URL and say "make slides like this" — produces drift: colors shift, fonts get substituted, the logo renders as an emoji or a placeholder, and slides clip the deck at 720px because nobody told the model that a slide is a *fixed-size box*, not a scrolling document.

This skill solves the problem by separating **what changes per brand** from **what never should**:

- **Brand-variable** (you do recon and let the user confirm): philosophy, colors, type, logo, aesthetic emphasis
- **Engineering DNA** (baked in unchanged, every time): fit contract, single-absorber rule, three-layer overflow safety net, logo-as-symbol pattern, mobile inline-flex catch-all, flip-card mobile fix, 12px readability floor, the 40-item pre-ship checklist

That split is the whole game. Without it, every new brand = relearning the same hard-won bugs.

## The pipeline (4 phases — do not skip any)

### Phase 0 — Verify dependencies (one-time)

Before the first run on any new machine, verify the standalone `agent-browser` CLI is installed:

```bash
bash scripts/setup.sh
```

This script:
- Confirms `python3` is on PATH
- Confirms `agent-browser` is on PATH and can open a page
- If either is missing, prints the recommended install command for the platform (npm / brew / cargo) and the project URL: https://github.com/vercel-labs/agent-browser
- Reminds the user to run `agent-browser install` after first install (downloads Chrome from Chrome for Testing)

If the user is on Linux and Chrome won't download, suggest `agent-browser install --with-deps` (pulls in `libnss3`, etc.).

Do NOT silently fall back to `curl` if `agent-browser` is missing — modern brand sites hydrate client-side and curl returns a near-empty shell, breaking the whole pipeline. Surface the install command and stop.

### Phase 1 — Reconnaissance (5 steps: thin deterministic harness + LLM exploration)

Architecture: Python scripts only do what's deterministic (fetch, enumerate, quality-gate, embed). Every act of *judgment* — which subpages to crawl, which candidate is the real wordmark, what the brand palette actually is — is done by **you**, the LLM running this skill, using the guideline files in `references/llm-prompts/`.

```
1a. fetch_sitemap.sh   →   1b. (LLM picks pages)   →   1c. fetch_pages.sh
                                                                ↓
1f. embed_logo.py      ←   1e. (LLM synthesizes)   ←   1d. enumerate_assets.py
```

Each step's output is the next step's input. Don't skip.

```bash
WS=./.web-to-ds-workspace/$(date +%s)
mkdir -p "$WS"
```

**1a — Fetch sitemap + home (deterministic)**

```bash
bash scripts/fetch_sitemap.sh <URL> "$WS"
```

Pulls `recon/home.html` + `recon/home.png` + `recon/sitemap.xml` + `recon/sitemap-urls.txt` + `recon/nav-links.json` + `recon/jsonld.json`.

**1b — Pick subpages to fetch (LLM, you)**

Read `references/llm-prompts/discover-pages.md`. Then read the discovery files from 1a, decide which 5–8 subpages are most likely to expose the brand's real wordmark / palette / typography / aesthetic, and write them to `$WS/pages.txt` (one URL per line, `#` comments allowed).

**1c — Batch-fetch the chosen pages (deterministic)**

```bash
bash scripts/fetch_pages.sh "$WS/pages.txt" "$WS"
```

For each URL: desktop screenshot + DOM dump + per-page probe (every inline SVG anywhere with metadata, every `<img>` with size+region, every `background-image: url()`, every JSON-LD logo field, all `<link rel*=icon>`, all `:root` vars, computed bg/color/font on a wide selector set, `@font-face` srcs, preload font URLs). Lands at `$WS/recon/pages/<slug>/{dom.html,shot.png,probe.json}`.

**1d — Aggregate into a candidate pool (deterministic)**

```bash
python3 scripts/enumerate_assets.py "$WS"
```

Merges every page's `probe.json` into one `$WS/raw-assets.json`. Each logo candidate gets a stable 8-char `id`. Color frequency, computed palette per surface, font frequencies, font-face URLs are all aggregated. Candidates are ranked by interestingness as a hint, but nothing is filtered out — that's your job.

**1e — Synthesize brand from raw assets (LLM, you)**

Read `references/llm-prompts/synthesize-brand.md`. Then:

1. Read `$WS/raw-assets.json`
2. Use the Read tool to look at `$WS/recon/pages/<slug>/shot.png` for each indexed page (vision)
3. Pick the chosen logo (by candidate `id`), brand_primary / secondary / ink / paper / accents (with hex + evidence), display + body fonts, spacing/radius/shadow style, aesthetic mood + precedents
4. Write `$WS/brand.json` per the schema in synthesize-brand.md, including `chosen_logo.id` plus 2–3 `alt_logo_ids`

**1f — Materialize the chosen logo (deterministic)**

```bash
python3 scripts/embed_logo.py "$WS"
```

Looks up `chosen_logo.id` in raw-assets, downloads if remote, runs the quality gate (SVG must have `<path d>` ≥ 40 chars or `<image>` child; raster ≥ 64×64), and writes `$WS/assets/logo.{svg|png|…}` + `$WS/assets/logo.embed.html` (a `<symbol id="brand-wm">` snippet ready to paste into Phase 3) + `$WS/assets/logo.dataurl`.

If quality-gate fails (exit 1), swap `chosen_logo.id` to the next item in `alt_logo_ids` in `brand.json` and rerun. If all alternatives fail, **stop** and ask the user for a logo URL or file path. Never invent a typographic placeholder.

### Phase 2 — Confirm with the user (latent + AskUserQuestion)

Goal: take the brand.json you produced in 1e and confirm with the user before generating. Most synthesis already happened in 1e — this phase is a sanity-check + scope decision, not redoing the work.

**Round 0 (always first): language.** Before any other question, call `AskUserQuestion` to ask which language the rest of the conversation AND the generated DS should be in. The four primary options are 中文 (Simplified Chinese), English, 日本語 (Japanese), Español (Spanish), plus an Other free-text choice. After this answer, conduct every subsequent round AND the Phase 3 generation in that language. Token names (`--navy`, `--blue`, etc.), code snippets, and CSS stay in English regardless — only the prose changes (philosophy paragraph, rules narration, anti-patterns, checklist labels). See `references/decision-questions.md` Round 0 for full guidance.

Then read `$WS/brand.json`. Surface the LLM-derived choices to the user via `AskUserQuestion` (3-4 rounds). Examples:

- "I read [Brand] as **[aesthetic.mood]** (precedents: [precedents]). Confirm or redirect?"
- "Palette I picked from the site: brand_primary [hex], secondary [hex], ink [hex], paper [hex], + accents. The chosen logo came from [chosen_logo.why]. Anything to swap?"
- "Typography: display = [display_font.family], body = [body_font.family]. Substitute? (web fonts often aren't licensable for slides — fallback to Inter/Source Sans is fine if needed.)"
- "Slide types to emphasize for this deck family: [shortlist]?" (use `references/decision-questions.md` for the 11-type catalog)

Take the user's responses. Save the final decisions to `$WS/decisions.json`. If the user redirects on a token (e.g., "actually use the secondary as primary"), update brand.json's `palette` accordingly so Phase 3 generation reflects it.

If the user gives no clear direction on something, default to brand.json's pick (LLM's best evidence-based guess) and note it in the output.

### Phase 3 — Generation (latent, template-driven)

Open `references/ds-template.md`. It is a complete Design System with:
- **Brand-variable placeholders** clearly marked: `{{BRAND_NAME}}`, `{{BRAND_SLUG}}`, `{{PHILOSOPHY_PARAGRAPH}}`, `{{NAVY_HEX}}`, `{{BLUE_HEX}}`, etc.
- **Engineering DNA baked in verbatim**: the entire fit contract section, the single-absorber rule, the mobile section including the inline-flex trap, the flip-card mobile fix, the pre-ship checklist. None of these may be edited or "simplified."

Steps:

1. Fill brand-variable placeholders from `$WS/decisions.json` + `$WS/brand.json` (palette hex, font families, brand name, etc.).
2. **Logo embed**: paste the contents of `$WS/assets/logo.embed.html` directly into the §4 Logo section's "Definition (once per HTML file)" block. `embed_logo.py` already produced the correct `<symbol id="brand-wm">` snippet — vector or base64-raster form, with hardcoded fills stripped so `currentColor` works. Do not regenerate this; do not re-extract paths.
3. Set `{{LOGO_VIEWBOX}}` placeholder in §4's `.logo` usage examples to match the viewBox in the embed snippet.
4. **Language pass** (only if Round 0 picked a non-English language): the template is English. Translate **prose only** — section narration, philosophy paragraph, anti-patterns, checklist labels, mood/aesthetic notes, repair-priority bullets. **Never translate**: token names (`--navy`, `--blue`), CSS / JS / HTML code, viewBox numbers, hex values, comment markers like `<!-- ENGINEERING-DNA -->`, file names. The output must be **single-language throughout** — no half-translated paragraphs and no leftover English sentences mixed into a Chinese DS.
5. Write the final markdown to the user's chosen path. Default: `./{{BRAND_SLUG}}-PPT-Design-System.md`. Confirm path before writing if it would overwrite an existing file.

### Phase 4 — Verification (latent)

After writing, give the user:
1. Output file path
2. A 5-line summary: palette, font, logo source, aesthetic mood, slide-type emphasis
3. A one-line offer: "Want me to build a sample 3-slide deck using this DS to verify it actually produces what you expect?"

If the user accepts the verification offer, generate one cover + two content slides exercising:
- The logo on a dark slide AND a light slide (confirms the `currentColor` flip works)
- A single-column dense slide (confirms fit contract math)
- A two-column slide (confirms `.g2` collapses on mobile)

Open the resulting HTML file at native 1280×720 and at 375px width to visually confirm.

## Hard rules — engineering DNA (NEVER violate, NEVER simplify)

These parts of the generated DS must be copied verbatim from `references/ds-template.md`. They came from real, painful bugs. If you find yourself thinking "this section is overkill, let me trim it," stop — you are about to reintroduce a bug someone else already fixed.

1. **Single-Slide Fit Contract**: 1280×720 fixed canvas; three-layer `overflow:hidden` safety net (`.slide`, `.sw .sc`, and any `flex:1` absorber); single-absorber rule; 602px content-height budget math; pre-build height checklist; verify at native 1280×720 (the `transform:scale()` masks overflow at scaled sizes).
2. **Logo as SVG `<symbol>` + `currentColor`**: `<symbol>` defined once in a hidden `<svg>` block at the top of `<body>`; referenced via `<use href="#…">`; `fill: currentColor` set on the outer `<svg>` (NOT on the `<path>` — selectors don't pierce shadow DOM). Variants: `.W` (white-on-dark), `.L` (brand-dark-on-light).
3. **Token-only color**: every color in slides comes from `:root` CSS variables. No ad-hoc hex values. Token *names* stay stable across brands (`--navy`, `--blue`, `--surface`, `--ink`, `--mid`, `--rule`, `--tint`, `--green`, `--red`, `--warn`, `--teal`) even when the actual hex differs — so downstream slide code doesn't need to know which DS it's using.
4. **Type scale + 12px readability floor**: nothing below 12px ever; enforced default sizes for title (50px), card headline (28px), body (16px), subtitle (20px); changing layout when content doesn't fit, never shrinking font.
5. **Mobile media query (≤768px) collapses everything to single column** AND **inline-flex trap catch-all CSS** (`@media` rules that override `style="display:flex"` and `style*="grid-template-columns"` in case bespoke slides used inline styles). This is how mobile parity survives bespoke slide compositions.
6. **Flip card mobile fix**: every flip card carries `onclick="this.classList.toggle('on')"`; mobile CSS kills 3D transforms and uses `display:none/flex` to swap front/back. CSS `:hover` doesn't work on touch.
7. **Constraints vs Freedom philosophy** (§1): explicit list of hard constraints + explicit list of reusable components + explicit "bespoke compositions encouraged within tokens" paragraph. This is what stops the next agent from either (a) reinventing the system or (b) restricting itself to a rigid catalog.
8. **No emoji, typographic symbols only**: `✓ − ! × → ←` permitted; `👍🎉🔥` etc. forbidden. (Brand may override toward more or fewer symbols, but the no-emoji rule is invariant.)
9. **Pre-ship checklist (§13)**: the ~40-item checklist that catches every common bug. Keep all groups: brand & tokens, typography & readability, slide structure, fit contract, components & interaction, visual & imagery, animation, **responsive (verify at 375px width)**.

If any of these is missing from the generated DS, the DS will produce broken decks. The whole point of skillifying this is so future you doesn't have to remember any of it.

## What legitimately changes per brand

- §1 Design Philosophy (the mood paragraph + the Constraints/Freedom *list contents*, not the framing itself)
- §2 Colour Tokens (hex values; token *names* stay stable)
- §3 Typography (family, weights, fallback chain, line-height tweaks)
- §4 Logo (SVG path)
- §6 Slide Types (emphasis order, illustrative example contents)
- Cosmetic component params: border-radius, accent thickness, hover lift distance

## Anti-patterns

- **Skipping Phase 2 confirmation**. Without user confirmation, you ship overfit garbage — possibly the wrong mood, possibly the wrong dominant color (sites often have hero accents that aren't the actual brand color).
- **Renaming color tokens** to brand-specific names (`--unilever-navy`, `--stripe-purple`). Tokens are abstractions — keep names stable.
- **"Improving" the engineering DNA** by simplifying the fit contract, dropping the absorber rule, removing the inline-flex catch-all, etc. Those rules are non-negotiable.
- **Generating without a logo**. If `download_logo.sh` failed, ASK the user for a logo URL or local file before generating §4.
- **Using emoji in the generated DS or its sample slides**. Typographic symbols only.
- **Trusting the homepage hero color as the brand primary**. Hero gradients are often campaign-specific; the actual brand primary is usually in the nav, footer, or buttons. `extract_brand.py` reports candidates with frequency — prefer the higher-frequency one and confirm.
- **Skipping mobile verification**. Every line of the §10 Mobile section in the template is there because a real production deck broke in that exact way. Always render at 375px once before declaring done.

## Companion files

- `references/ds-template.md` — full DS template with placeholders + engineering DNA (incl. §3.1 Typography Safety, §4 multi-format logo embed). Read in Phase 3.
- `references/decision-questions.md` — Phase 2 structured decision checklist + Round 0 language framing.
- `references/llm-prompts/discover-pages.md` — guideline you (LLM) read at step 1b to decide which subpages to fetch.
- `references/llm-prompts/synthesize-brand.md` — guideline you (LLM) read at step 1e to pick logo + palette + type + aesthetic from raw assets.
- `scripts/fetch_sitemap.sh` — step 1a: home + sitemap + nav-links + JSON-LD.
- `scripts/fetch_pages.sh` — step 1c: batch-fetch a URL list with full per-page probes.
- `scripts/enumerate_assets.py` — step 1d: aggregate all probes into raw-assets.json with stable candidate ids.
- `scripts/embed_logo.py` — step 1f: quality-gate + base64-embed the chosen logo.
- `scripts/setup.sh` — Phase 0 dependency check.
- `eval/` — auto-eval framework (hard checks + LLM-judged rubric, run via `eval/run.sh`).
- `tests/` — unit + integration + smoke tests.
