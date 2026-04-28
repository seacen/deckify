# TESTING.md — Skillify 10-step mapping for `deckify`

This file maps Garry Tan's [10-item skillify checklist](https://x.com/garrytan/article/2046876981711769720) to the concrete artifacts in this skill, so future-you can verify nothing has rotted and future-contributors know where each layer lives.

> **The 10-step checklist (verbatim):**
> 1. SKILL.md — the contract (name, triggers, rules)
> 2. Deterministic code — scripts/*.mjs (no LLM for what code can do)
> 3. Unit tests — vitest
> 4. Integration tests — live endpoints
> 5. LLM evals — quality + correctness
> 6. Resolver trigger — entry in AGENTS.md
> 7. Resolver eval — verify the trigger actually routes
> 8. Check-resolvable + DRY audit
> 9. E2E smoke test
> 10. Brain filing rules

Below: how each one is realized for *this* skill.

---

## 1. SKILL.md — the contract

**File:** [`SKILL.md`](SKILL.md)

The contract names the skill (`deckify`), declares its `dependencies` (agent-browser, python3, curl), describes WHEN to trigger (push-y description with multiple trigger phrases), and specifies the four-phase pipeline + invariant engineering DNA.

**Health check (manual):**
- Does the description trigger on real-world phrasings? (See step 7 below for the eval set.)
- Does the SKILL.md stay under 500 lines? Currently ~250.
- Do all `<= ENGINEERING-DNA -->` rules exist verbatim in `references/ds-template.md`?

---

## 2. Deterministic code — scripts/

**Files:**
- [`scripts/setup.sh`](scripts/setup.sh) — dependency check + guided install for agent-browser
- [`scripts/fetch_site.sh`](scripts/fetch_site.sh) — drives agent-browser CLI to capture DOM, screenshots, and computed-style probe
- [`scripts/extract_brand.py`](scripts/extract_brand.py) — pure-stdlib parser that turns recon files into `brand-recon.json`
- [`scripts/download_logo.sh`](scripts/download_logo.sh) — best-effort logo file extraction with curl fallback chain

**Why these are deterministic** (per the article: "deterministic work happens in deterministic space"):
- Same URL → same `index.html` (modulo the live page changing)
- Same `index.html` + `computed.json` → same `brand-recon.json`. Always.
- No LLM in the loop for color extraction, font detection, or logo discovery.

The latent layer (Phase 2 mood synthesis, Phase 3 prose for the philosophy paragraph) is *constrained* by the deterministic JSON, not the other way around. This is the "latent space builds the deterministic tool, then the deterministic tool constrains the latent space" pattern from the article.

---

## 3. Unit tests — Python (stdlib `unittest`)

**File:** [`tests/test_extract_brand.py`](tests/test_extract_brand.py)

Vitest is JS-only; this skill's deterministic code is Python and Bash, so unit tests are stdlib `unittest`. Run:

```bash
python3 -m unittest tests.test_extract_brand -v
```

What's covered:
- `_normalize_hex` round-trips 3-char and 6-char hex
- `_rgb_to_hex` clamps and converts
- `_is_neutral` flags whites, blacks, and pure grays correctly
- `_clean_family` strips quotes and skips generic CSS keywords
- `extract_colors` produces frequency-correct counts on fixture HTML
- `parse_meta` extracts title, og:image, favicon, header inline SVG
- `rank_logo_candidates` orders inline-svg before favicon before path-guess
- `merge_computed_signal` promotes `:root` color vars to `root_color_vars`
- `_color_str_to_hex` handles `rgb()`, `#abc`, `#aabbcc`

Fixture data lives in `tests/fixtures/` — synthetic HTML files representing common brand-site shapes (CSS-variable site, monolithic-CSS site, image-heavy site).

The kinds of bugs these catch (per the article): "parseEventLine silently drops events with Unicode characters in the location field" — equivalent here would be `extract_colors` silently dropping rgba() values, `parse_meta` failing on broken HTML, `_is_neutral` mis-classifying a brand color as gray.

---

## 4. Integration tests — live endpoints

**File:** [`tests/test_integration.sh`](tests/test_integration.sh)

These do hit the live web. Run only when you've actually changed `fetch_site.sh` or `extract_brand.py`'s real-world contract.

```bash
bash tests/test_integration.sh
```

Tests:
- Run the full Phase 1 pipeline on `https://stripe.com` → assert `brand-recon.json` has at least 3 brand candidates and a logo file
- Run on `https://apple.com` → assert at least 1 logo candidate succeeded
- Run on `https://www.unilever.com` → assert the `:root` custom-property surface is non-empty (a real corporate site exposes a token system)

Integration tests catch the "real data has malformed event lines" bugs — e.g., a brand site that returns 403 to non-real-browser User-Agents (caught by agent-browser, missed by curl).

---

## 5. LLM evals — quality + correctness

**File:** [`evals/evals.json`](evals/evals.json)

These are the test cases the `skill-creator` flow runs. Each has a prompt + assertions. Assertions for THIS skill check both the *process* (did the agent run setup → fetch → extract → confirm → generate?) and the *output* (does the generated DS contain the engineering DNA invariants?).

Sample assertions (shape — full list in `evals/evals.json`):

- `output_has_fit_contract`: generated DS contains "Single-Slide Fit Contract" + "single absorber" verbatim
- `output_has_inline_flex_catchall`: contains the `@media (max-width: 768px) .sc div[style*="display:flex"]` rule
- `output_has_flip_card_mobile_fix`: contains `onclick="this.classList.toggle('on')"` AND `transform: none !important`
- `output_has_logo_symbol`: contains `<symbol id=` AND `fill: currentColor` on `.logo` (NOT on the `path`)
- `output_has_12px_floor`: contains "12 px" or "12px" floor in the typography section
- `output_no_ad_hoc_hex`: § 7 / § 12 contain `var(--` references and not raw `#` hex literals
- `output_has_mobile_375_check`: pre-ship checklist contains "375px" (mobile verification)
- `process_called_extract_brand`: agent transcript shows it ran `python3 scripts/extract_brand.py`
- `process_called_ask_user_question`: agent invoked `AskUserQuestion` at least once before generation
- `output_unilever_palette_match` (a real corporate site-only): generated `--primary` is within ΔE < 10 of `#07005A`

Run via `skill-creator`'s normal evaluation flow:

```bash
# from inside the skill-creator workspace
python -m scripts.run_loop --eval-set deckify/evals/evals.json --skill-path deckify
```

The "fucking shit" eval heuristic from the article applies: if a brand site breaks the skill in production, add it as a new eval case with the failing assertion captured.

---

## 6. Resolver trigger

The "resolver" in Claude Code is the `description` field of `SKILL.md`'s YAML frontmatter — Claude reads available skills' descriptions and decides which to invoke. (No separate `AGENTS.md` table to maintain.)

The current description is intentionally **push-y** (per skill-creator guidance: "currently Claude has a tendency to undertrigger skills"). It mentions:
- Multiple trigger phrases ("build a design system from this site", "extract a design system", "make slides like this brand", "skin slides like X")
- Specific brand examples (a real corporate site, Stripe, Apple)
- The implicit case ("when the user names a brand site as a slide-deck reference, even if they don't say 'design system' explicitly")

If you tune the description, update the trigger eval (step 7) in lockstep.

---

## 7. Resolver eval — verify the trigger actually routes

**File:** [`evals/trigger_evals.json`](evals/trigger_evals.json)

20 queries (10 should-trigger, 10 should-not) run against the current description. Run via `skill-creator`'s `run_loop.py`:

```bash
python -m scripts.run_loop \
  --eval-set deckify/evals/trigger_evals.json \
  --skill-path deckify \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose
```

Sample trigger phrasings tested:

- ✓ "build me a design system from unilever.com so i can make decks in their style"
- ✓ "我想做一份像 stripe 那样风格的 html slide，能不能先帮我从他们官网抽出设计系统"
- ✓ "got a deck to write that needs to look like apple.com — start with the design system"
- ✗ "design a new product page for our internal tool" (frontend design, not extracting from a URL)
- ✗ "extract the colors from this image" (color extraction without URL → wrong skill)
- ✗ "build slides for this conference talk about React 19" (slide content, not visual system)

False-negative bugs (skill should fire but doesn't) → strengthen description.
False-positive bugs (skill fires when it shouldn't) → tighten description scope.

---

## 8. Check-resolvable + DRY audit

**File:** [`tests/audit_skill.sh`](tests/audit_skill.sh)

Smaller-scale than Garry's `gbrain doctor` — just for this single skill — but the same idea. Run:

```bash
bash tests/audit_skill.sh
```

Checks:
1. Every script in `scripts/` is referenced from SKILL.md (no orphans)
2. Every `references/*.md` file is referenced from SKILL.md
3. Every `{{PLACEHOLDER}}` token in `ds-template.md` is documented in `decision-questions.md`'s `decisions.json` shape
4. No duplicate skill name in the user's installed skill list (no overlap with another `*-design-system` skill)
5. SKILL.md description is not identical to any other skill's description (DRY)

---

## 9. E2E smoke test

This step has two flavors:

### 9a. Phase-1 deterministic smoke

**File:** [`tests/smoke_unilever.sh`](tests/smoke_unilever.sh)

The full pipeline, end-to-end, against unilever.com (the canonical reference brand for this skill). Run:

```bash
bash tests/smoke_unilever.sh /tmp/web-to-ds-smoke
```

Steps:
1. Run `setup.sh` (verifies deps)
2. Run `fetch_site.sh https://www.unilever.com /tmp/web-to-ds-smoke/<ts>`
3. Run `extract_brand.py /tmp/web-to-ds-smoke/<ts>`
4. Run `download_logo.sh /tmp/web-to-ds-smoke/<ts>`
5. Assert: `brand-recon.json` exists, has ≥ 3 brand candidates, has at least 1 successful logo
6. Print a summary of what would feed into Phase 2 (the latent half — not part of this smoke; that's covered by the LLM evals in step 5)

If the smoke breaks, the LLM evals will all fail too, and the cause is in the deterministic layer.

### 9b. End-to-end deliverable test (Procter & Gamble)

The deterministic smoke (9a) only covers Phase 1 — the parts a script can verify. To catch regressions in the *latent* layers (mood synthesis, decisions, template fill, sample-deck generation), there's a higher-fidelity human-in-the-loop test using P&G as the second canonical brand.

**Test contract** (also encoded as eval id 4 `pg-end-to-end-with-deck` in `evals/evals.json`):

1. The agent runs the full pipeline against `https://www.pg.com`.
2. The agent generates `./pg-PPT-Design-System.md` using the template + decisions.
3. **The agent then writes 5–6 slides of original copy itself** — a fictional "P&G China Q2 brand performance" update — and produces `./pg-deck.html`: a complete single-file deck at native 1280×720 that exercises the DS (cover + dark-bg slide with white logo + light-bg slide with brand-dark logo + two-column comparison + chart slide + closing pull-quote).
4. The user opens `./pg-deck.html` and reviews against the manual checklist (logo flip, mobile collapse at 375px, visible bottom breathing room, on-brand feel for P&G).

**What this test catches that 9a doesn't:**
- Whether the model actually *uses* the engineering DNA from the generated DS when authoring slides (vs. ignoring it and freestyling)
- Whether the logo-as-symbol pattern actually works end-to-end (most-bespoke part of any DS — easy to break)
- Whether the brand mood reads as P&G to a human (the qualitative half)
- Whether the model writes coherent slide copy without lapsing into generic AI slop

The eval includes both programmatic assertions (`file_contains`, `regex_in_file`) and a `manual_review` array — the human reviewer goes through that checklist after the run.

**Run cadence:** before sharing the skill with new users; after material edits to `references/ds-template.md`; whenever the eval suite for the a real corporate site case starts to look "too easy" to detect a regression.

---

## 10. Filing rules — where the generated DS goes

The output Design System file goes to a deterministic, predictable location:

- **Default:** `./{{BRAND_SLUG}}-PPT-Design-System.md` in the current working directory
- **Logo:** `./{{BRAND_SLUG}}-PPT-Design-System-assets/logo.svg` (sibling directory)
- **Session workspace** (recon files, intermediate JSONs, screenshots): `./.web-to-ds-workspace/<timestamp>/` (gitignored by default)

Why this matters: a future invocation of the skill against the same brand should *not* silently overwrite the prior DS file. Phase 3 must check for an existing `{{BRAND_SLUG}}-PPT-Design-System.md` and ask the user before overwriting.

If the user has a project-level convention (e.g., "all design systems live in `docs/design-systems/`"), they can override by passing an explicit output path during Phase 4 confirmation.

---

## Verification cadence

- **Unit tests** (step 3): run before every commit to scripts. Sub-2-second.
- **Integration tests** (step 4): run after editing `fetch_site.sh` or when bumping the agent-browser dependency version. Sub-30-second.
- **LLM evals** (step 5): run before considering the skill "shipped" or after major SKILL.md edits. Several minutes.
- **Trigger evals** (step 7): run after editing the SKILL.md description. Several minutes.
- **Audit** (step 8): run before sharing the skill with anyone new. Sub-second.
- **Smoke** (step 9): run after any change to scripts/ or references/. Sub-minute.

If you skip a layer, you accept the corresponding class of bug coming back.
