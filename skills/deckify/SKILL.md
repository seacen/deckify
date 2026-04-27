---
name: deckify
description: Generate a complete HTML-slide Design System markdown file from a reference URL. Studies the page's color palette, typography, logo, and aesthetic mood, then writes a Design System that bakes in proven engineering rules (1280×720 fit contract, three-layer overflow safety net, single-absorber rule, mobile inline-flex trap catch-all, flip-card mobile fix, logo-as-SVG-symbol-with-currentColor pattern, 12px readability floor) while letting the brand identity drive the visuals. Use this whenever the user gives you a URL and asks to "build a design system from this site," "extract a design system from", "make slides like this brand," "skin slides to match this site's visual language," or wants to author HTML slides in the visual language of any specific website. Also use when the user names a brand site as a slide-deck reference, even if they don't say "design system" explicitly.
dependencies:
  - agent-browser  # Standalone CLI from Vercel Labs (https://github.com/vercel-labs/agent-browser). Install via npm/brew/cargo — see scripts/setup.sh. Used for URL fetch, computed-style introspection, screenshots in Phase 1. NOT the same as any plugin called "agent-browser" — this is the standalone binary at github.com/vercel-labs/agent-browser. Verify with `which agent-browser` and `agent-browser --version`.
  - python3        # Stdlib only. enumerate_assets.py and embed_logo.py post-process agent-browser output. No external deps.
  - curl           # Used by fetch_sitemap.sh to fetch /sitemap.xml.
---

# deckify

Turn a reference URL into a production-ready Design System markdown plus a verified 9-slide HTML sample deck. Another agent (or you) can use the DS to build precise, mobile-friendly HTML slides in the brand's visual language. The sample deck is the proof that the DS spec works.

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

### Phase 4 — Verification deck + runtime hard checks (MANDATORY, not optional)

The DS markdown is the deliverable. The verification deck is the **proof that the DS produces correct slides**. Skipping this means shipping an unverified spec — don't.

**Step 4a — Write the verification deck.**
Read `references/verification-deck-spec.md`. It defines the 8 required slide types (cover, narrative+pullquote, two-column, data table, chart, flip cards, timeline, big pull-quote) and 6 coverage rules (multi-column collapse, click interaction, semantic colour, real numbers, bespoke composition, absorber variety). Write the deck to `decks/<brand>/<brand>-deck.html` using copy drawn from the recon corpus — **never invented stats**.

**Step 4b — Run the runtime hard checks (deterministic).**

```bash
bash evals/run.sh
```

This invokes `evals/hard_checks.py` over each registered brand sample, lands measurements under `tests/reports/runs/<ts>/per-sample/<brand>/`. The 8 checks are: slide dimensions (1280×720), fit contract intact, token-only colors, no emoji, mobile collapse at 375 px, logo renders, text layout safe (no truncation, no glued-to-bottom), DS engineering DNA preserved.

**Step 4c — On any hard-check failure, FIX THE BRAND DS — never the deck alone.**
The brand DS markdown is your tunable; the deck is the verification artifact. When a check fails, trace it to the relevant section of *your brand's DS* (use the fail → DS-section mapping table in `references/verification-deck-spec.md`), update the DS, regenerate the deck from the updated DS, re-run hard checks. **If you find yourself editing only the deck to make a check pass, you are doing it wrong** — the DS is the spec, the deck just exercises it.

Iterate until hard checks are 8/8 PASS.

### Phase 5 — Visual judge (LLM, you) — MANDATORY

Hard checks measure DOM shapes; they don't measure whether the deck *looks* on-brand. That's your job.

**Step 5a — Read the per-slide screenshots.**
For each brand under `tests/reports/runs/<latest>/per-sample/<brand>/slides/`, read the PNGs (Read tool, vision). Re-read the brand's DS markdown for context.

**Step 5b — Score against the rubric.**
Read `evals/rubric.json` — 5 dimensions (logo present and branded, slide visual quality, brand fidelity, content substantive, engineering DNA visible in DS), each 0–5. Plus 5 disqualifiers (D1 logo missing, D2 dimensions wrong, D3 console errors, D4 mobile horizontal scroll, D5 DS template violated).

**Step 5c — Write `judge.json`.**
Land at `tests/reports/runs/<latest>/per-sample/<brand>/judge.json` with the schema printed by `run.sh` — scores, reasoning (especially for low scores), regression_flags.

**Step 5d — Aggregate.**

```bash
python3 evals/build_report.py <run-dir> 4 \
  "<brand>|<url>|<deck-path>|<ds-path>" ...
```

PASS criteria (per `rubric.json`): hard 8/8 AND judge avg ≥ 4 AND no disqualifier triggered.

**Step 5e — Failure handling.**
- Judge score < 4 on `brand_fidelity` → revisit the brand.json (was the mood paragraph too generic? did the palette flatten to white+grey+single-accent?). Update brand.json with sharper evidence, regenerate the brand DS §1 + §2, regenerate the deck, re-judge.
- Judge score < 4 on `slide_visual_quality` → tighten the brand DS §6 (per-slide-type spec) or §7 (component density). Update the relevant section in *your brand's* DS, regenerate the deck, re-judge.
- Judge score < 4 on `content_substantive` → the recon copy was thin; revisit Phase 1b page picks (broader subpages) or pull more from the existing recon corpus into the deck content.
- Judge score < 4 on `engineering_dna_visible_in_ds` → your brand DS is missing a required chapter or it got diluted during the language/translation pass. Restore the chapter verbatim from `references/ds-template.md`.
- Disqualifier triggered → see the fail → DS-section mapping table in `references/verification-deck-spec.md`.

Iterate until PASS. The skill is not done until both hard 8/8 AND judge ≥ 4.

### Phase 6 — Hand back to the user (latent)

Give the user:
1. The DS markdown path + the deck HTML path
2. A 5-line summary: palette, font, logo source, aesthetic mood, slide-type emphasis
3. The eval scoreboard: hard 8/8, judge avg, status PASS/WARN/FAIL
4. Path to `tests/reports/runs/<latest>/summary.md` for the full per-brand breakdown

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

- `references/ds-template.md` — full DS template with placeholders + engineering DNA (incl. §3.1 Typography Safety, §4 multi-format logo embed, §5 scale-to-fit runtime, §6 Type E row-count rule, §10 mobile cov/sw fill rule). Read in Phase 3.
- `references/verification-deck-spec.md` — Phase 4 contract: the 8 required slide types every verification deck must include, plus the 6 coverage rules. Read in Phase 4a.
- `references/decision-questions.md` — Phase 2 structured decision checklist + Round 0 language framing.
- `references/llm-prompts/discover-pages.md` — guideline you (LLM) read at step 1b to decide which subpages to fetch.
- `references/llm-prompts/synthesize-brand.md` — guideline you (LLM) read at step 1e. Includes Design Taste anti-AI-slop guardrails (no Inter as the design choice, no even-weighted accent grids, no SaaS-default chrome).
- `scripts/fetch_sitemap.sh` — step 1a: home + sitemap + nav-links + JSON-LD.
- `scripts/fetch_pages.sh` — step 1c: batch-fetch a URL list with full per-page probes.
- `scripts/enumerate_assets.py` — step 1d: aggregate all probes into raw-assets.json with stable candidate ids.
- `scripts/embed_logo.py` — step 1f: navigate-to-asset-then-same-origin-fetch + quality-gate + base64-embed the chosen logo. Handles cross-origin CDN (Contentful, Cloudinary).
- `scripts/setup.sh` — Phase 0 dependency check.
- `evals/` — quality contract directory (see `evals/README.md`). Two layers in one folder:
  - `evals/evals.json` + `evals/trigger_evals.json` — marketplace harness contract (Anthropic skill-eval format).
  - `evals/hard_checks.py` + `evals/rubric.json` + `evals/build_report.py` + `evals/run.sh` — runtime auto-eval invoked by Phase 4-5.
- `tests/` — unit + integration + smoke tests.
