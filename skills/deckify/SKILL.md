---
name: deckify
description: Generate a complete HTML-slide Design System markdown file from a reference URL. Studies the page's color palette, typography, logo, and aesthetic mood, then writes a Design System that bakes in proven engineering rules (1280×720 fit contract, three-layer overflow safety net, single-absorber rule, mobile inline-flex trap catch-all, flip-card mobile fix, logo-as-SVG-symbol-with-currentColor pattern, 12px readability floor) while letting the brand identity drive the visuals. Use this whenever the user gives you a URL and asks to "build a design system from this site," "extract a design system from", "make slides like this brand," "skin slides to match this site's visual language," or wants to author HTML slides in the visual language of any specific website. Also use when the user names a brand site as a slide-deck reference, even if they don't say "design system" explicitly.
dependencies:
  - agent-browser  # Standalone CLI from Vercel Labs (https://github.com/vercel-labs/agent-browser). Install via npm/brew/cargo — see scripts/setup.py. Used for URL fetch, computed-style introspection, screenshots in Phase 1. NOT the same as any plugin called "agent-browser" — this is the standalone binary at github.com/vercel-labs/agent-browser. Verify with `which agent-browser` and `agent-browser --version`.
  - python3        # Stdlib only (urllib, subprocess, pathlib, tempfile). All Phase 1 scripts (fetch_sitemap.py, fetch_pages.py, enumerate_assets.py, embed_logo.py, init_workspace.py) and Phase 0 (setup.py) are Python — no shell needed, runs natively on macOS / Linux / Windows.
---

# deckify

Turn a reference URL into a production-ready Design System markdown plus a verified 9-slide HTML sample deck. Another agent (or you) can use the DS to build precise, mobile-friendly HTML slides in the brand's visual language. The sample deck is the proof that the DS spec works.

## Opening — print this banner once when the skill activates

Right before Phase 0, print exactly one of these two banners depending on the user's language preference (defaults to English on a fresh run; switches to 中文 once Phase 2 Round 0 confirms `decisions.json.language === "中文"`). Print it cleanly with surrounding blank lines, then continue straight into Phase 0 — do **not** add a "Hi! I'm deckify, what's your brand?" intro on top of this. The user already gave you the URL; the slogan is the entire hello.

**English** (default):
```
═══════════════════════════════════════════════════════════════════════
        PPT just turned the page.
        AI takes the canvas from here —
        in HTML, where stories run further.

                                                              — deckify
═══════════════════════════════════════════════════════════════════════
```

**中文** (after Round 0 confirms zh):
```
═══════════════════════════════════════════════════════════════════════
        PPT 翻篇了，
        AI 用 HTML 接管讲故事的边界。

                                                              — deckify
═══════════════════════════════════════════════════════════════════════
```

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
python3 scripts/setup.py
```

This script:
- Confirms `python3` is on PATH
- Confirms `agent-browser` is on PATH and can open a page
- If either is missing, prints the recommended install command for the platform (npm / brew / cargo) and the project URL: https://github.com/vercel-labs/agent-browser
- Reminds the user to run `agent-browser install` after first install (downloads Chrome from Chrome for Testing)

If the user is on Linux and Chrome won't download, suggest `agent-browser install --with-deps` (pulls in `libnss3`, etc.).

Do NOT silently fall back to `curl` if `agent-browser` is missing — modern brand sites hydrate client-side and curl returns a near-empty shell, breaking the whole pipeline. Surface the install command and stop.

> **All user artefacts land in `~/deckify/`** — independent of the cwd you run from. The brand's DS markdown, verification deck, persisted recon source, and per-run reports all go to `~/deckify/decks/<brand>/` and `~/deckify/reports/`. Do not write user artefacts into the deckify source repo, into the cwd, into a temp dir, or anywhere else. `~/deckify/` is created on first use; subsequent runs reuse it. This is enforced by `scripts/persist_brand_source.py` at Phase 6 — it always resolves to `~/deckify/`, ignoring cwd. (If you're a skill maintainer running the Phase A panel, see `tools/phase-a/README.md` — that path is separate and writes to the deckify repo's `tests/`, not to `~/deckify/`.)

### Phase 1 — Reconnaissance (5 steps: thin deterministic harness + LLM exploration)

Architecture: Python scripts only do what's deterministic (fetch, enumerate, quality-gate, embed). Every act of *judgment* — which subpages to crawl, which candidate is the real wordmark, what the brand palette actually is — is done by **you**, the LLM running this skill, using the guideline files in `references/llm-prompts/`.

```
1a. fetch_sitemap.py   →   1b. (LLM picks pages)   →   1c. fetch_pages.py
                                                                ↓
1f. embed_logo.py      ←   1e. (LLM synthesizes)   ←   1d. enumerate_assets.py
```

Each step's output is the next step's input. Don't skip.

Phase 1 happens in a transient workspace inside the OS temp dir — these are large, regenerable recon files (DOM dumps, screenshots, raw asset pools), not durable artifacts. The OS sweeps them on its own schedule (macOS ~3 days idle, Linux on reboot, Windows by user / Disk Cleanup). Durable artifacts (brand.json / decisions.json / assets / DS markdown / deck HTML) get copied out at Phase 6.

```bash
# Cross-platform: creates /var/folders/.../T/deckify-<slug>-<rand>/ on macOS,
# %TEMP%\deckify-<slug>-<rand>\ on Windows, /tmp/deckify-<slug>-<rand>/ on Linux.
WS=$(python3 scripts/init_workspace.py <brand-slug>)
echo "Workspace: $WS"
```

**1a — Fetch sitemap + home (deterministic)**

```bash
python3 scripts/fetch_sitemap.py <URL> "$WS"
```

Pulls `recon/home.html` + `recon/home.png` + `recon/sitemap.xml` + `recon/sitemap-urls.txt` + `recon/nav-links.json` + `recon/jsonld.json`.

**1b — Pick subpages to fetch (LLM, you)**

Read `references/llm-prompts/discover-pages.md`. Then read the discovery files from 1a, decide which 5–8 subpages are most likely to expose the brand's real wordmark / palette / typography / aesthetic, and write them to `$WS/pages.txt` (one URL per line, `#` comments allowed).

**1c — Batch-fetch the chosen pages (deterministic)**

```bash
python3 scripts/fetch_pages.py "$WS/pages.txt" "$WS"
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
2. Look at `$WS/recon/pages/<slug>/shot.png` for each indexed page using your host's image-viewing capability (the `Read` tool in Claude Code, the equivalent in Codex / OpenClaw, or your own image loader if scripted)
3. Pick the chosen logo (by candidate `id`), brand_primary / secondary / ink / paper / accents (with hex + evidence), display + body fonts, spacing/radius/shadow style, aesthetic mood + precedents
4. Write `$WS/brand.json` per the schema in synthesize-brand.md, including `chosen_logo.id` plus 2–3 `alt_logo_ids`

**1f — Materialize the chosen logo (deterministic)**

```bash
python3 scripts/embed_logo.py "$WS"
```

Looks up `chosen_logo.id` in raw-assets, downloads if remote, runs the quality gate (SVG must have `<path d>` ≥ 40 chars or `<image>` child; raster ≥ 64×64), and writes `$WS/assets/logo.{svg|png|…}` + `$WS/assets/logo.embed.html` (a `<symbol id="brand-wm">` snippet ready to paste into Phase 3) + `$WS/assets/logo.dataurl`.

If quality-gate fails (exit 1), swap `chosen_logo.id` to the next item in `alt_logo_ids` in `brand.json` and rerun. If all alternatives fail, **stop** and ask the user for a logo URL or file path. Never invent a typographic placeholder.

### Phase 2 — Confirm with the user (latent — interactive Q&A)

Goal: take the brand.json you produced in 1e and resolve the decisions YOU couldn't make alone — language, ambiguous logo picks, contested colour direction, proprietary typography fallbacks. Don't ask the user to confirm things YOU already have strong evidence for — that's noise.

**Host-conditional interaction rule** (this is a hard rule on Claude Code, a recommendation elsewhere — read carefully):

| Host environment | Required mechanism | If unavailable |
|---|---|---|
| **Claude Code / Claude Desktop** | **MUST use the `AskUserQuestion` tool** for every Round below. If the tool is *deferred* (schema not loaded at session start), invoke `ToolSearch` with `query: "select:AskUserQuestion"` first to load its schema, then call it. **Do not substitute plain text questions** — that bypasses the structured-choice UI, loses analytics, and produces ambiguous free-text answers the rest of this phase depends on. |  No graceful fallback — refuse to proceed and tell the user the tool is missing. |
| **Codex CLI / OpenClaw / similar AI hosts** | Use the host's nearest equivalent structured-question mechanism if it exists (each host names it differently). | If no structured mechanism exists, fall back to a single block of clearly-numbered text questions with explicit option labels. |
| **Headless / scripted runs** (no human in the loop) | Skip Phase 2 entirely; commit `brand.json` as-is and write `decisions.json` with `interaction_mode: "headless-defaults"` and the synthesizer's best evidence-based picks for every required field. |  N/A — by definition there's no user to ask. |

After Phase 2 finishes, **always record which mode was actually used** in `decisions.json`:

```jsonc
{
  "interaction_mode": "ask-user-question" | "host-equivalent" | "text-fallback" | "headless-defaults",
  "host": "claude-code" | "codex" | "openclaw" | "other-name" | "headless",
  // ... rest of decisions.json (language, slide_emphasis, etc.) ...
}
```

This field is what `audit_skill.py` and `build_report.py` use to detect "this run silently downgraded interaction quality" — a recurring failure mode where an agent skips structured Q&A and the resulting brand DS reflects guesswork instead of user choice.

**Question philosophy: ask only where you are genuinely uncertain.** A confident, evidence-backed brand.json shouldn't need 4 confirmation rounds — it needs maybe 1 or 2 for the genuinely ambiguous decisions, plus the always-required language round. If a decision is unambiguous (single canonical SVG logo, dominant chord with 100× CSS frequency, body font is the only computed font), commit and don't waste the user's attention.

**Round 0 (ALWAYS first): language.** Ask the user with exactly two options: 中文 (Simplified Chinese) and English. These are the only two languages with maintained sister templates (`ds-template.zh.md` and `ds-template.md`). Do NOT offer Japanese / Spanish / Other free-text — there is no `ds-template.<other>.md` to route to, so any non-zh/en answer would silently fall back to the English template + a per-run translation pass, which produces drift and undercuts the language_consistency hard check. If the user genuinely needs another language, they can author it in 中文 or English and re-translate downstream. After this answer, conduct every subsequent round AND Phase 3 generation in that language. Token names (`--primary`, `--accent`, etc.), code snippets, CSS, hex values, viewBox numbers, and HTML comment anchors (`<!-- ENGINEERING-DNA: ... -->`) stay in English regardless — only the prose changes.

**Round 1 (CONDITIONAL — only if logo is ambiguous): logo selection.** Trigger when you have ≥ 2 candidates that all pass the quality gate AND no clear winner from the synthesize-brand priority order. Surface 2–3 specific candidates with their evidence:
- Each option labeled with where it came from (e.g. "Nav inline-SVG, viewBox 0 0 67 44, single path" / "JSON-LD knowledge_graph_logo.png, RGB-only" / "apple-touch-icon, 180×180 RGBA").
- Description explains the trade-off (e.g. "RGB PNG flips badly on dark covers; SVG is cleaner but might be a wordmark not the silhouette").
- If candidates differ only trivially, pick yourself — don't ask.

**Round 2 (CONDITIONAL — only if dominant chord is contested): palette anchor.** Trigger when colour-frequency analysis has 2+ candidates with similar counts (within 1.5×) AND the screenshots don't clearly resolve which is the brand's actual primary chord (vs a campaign accent). Surface the top 2–3 colours with their hex + role evidence; ask which is the brand's actual `--primary`.

**Round 3 (CONDITIONAL — only if typography needs licensing decision): font fallback.** Trigger when `font.frequencies` show a proprietary face (UnileverDesire, SF Pro, Söhne, Stripe Sans) that won't be licensable for a typical standalone slide deck. Surface 2–3 fallback options:
- "Helvetica Neue → system-ui" (Apple's actual fallback chain)
- "Inter / Source Sans" (modern open source)
- "system-ui only" (zero webfont load, generic)

**Round 4 (ALWAYS, but short): slide-type emphasis for the verification deck.** Multi-select from the 8 required slide types per `references/verification-deck-spec.md` — which 2–3 should the deck particularly lean into for this brand's voice? (e.g. Apple → Type J pullquote + Type F image + Type H chart.)

**Round 5+ (CONDITIONAL — only when needed): scope-of-deck decisions.** Quarterly review vs annual letter vs internal deck — only ask if the user's original prompt didn't clarify. If they said "build me a DS for SaaS pitch decks", that's enough; don't re-ask.

Take the user's responses. Save the final decisions to `$WS/decisions.json`. If the user redirects on a token (e.g., "actually use the secondary as primary"), update brand.json's `palette` accordingly so Phase 3 generation reflects it.

**Anti-pattern**: asking 4 ceremonial confirmation questions when the recon was unambiguous. Each interactive question costs the user attention — earn it with genuine choices, not with reciting back what you already know.

If the user gives no clear direction on something, default to brand.json's pick (LLM's best evidence-based guess) and note it in the output.

### Phase 3 — Generation (latent, template-driven)

**Step 0 — Pick the template by language.** Read `decisions.json` for `language`:
- `English` → use `references/ds-template.md` (the English source-of-truth)
- `中文` / `Chinese` / `zh` → use `references/ds-template.zh.md` (the Chinese sister template; same engineering-DNA anchors, prose pre-translated)

These are the two and only two supported languages — Phase 2 Round 0 only offers them, so `decisions.json.language` will always be one of these. There is no general translation-pass fallback; if you ever see another value here, treat it as a bug in Round 0 and re-ask the language question instead of silently translating.

Both templates contain identical:
- **Brand-variable placeholders**: `{{BRAND_NAME}}`, `{{BRAND_SLUG}}`, `{{PHILOSOPHY_PARAGRAPH}}`, `{{PRIMARY_HEX}}`, `{{ACCENT_HEX}}`, `{{BRAND_PALETTE_TOKENS}}`, etc.
- **Engineering DNA baked in verbatim**: the entire fit contract section, the single-absorber rule, the mobile section including the inline-flex trap, the flip-card mobile fix, the pre-ship checklist. Never edited, never "simplified."
- **HTML comment ID anchors**: `<!-- ENGINEERING-DNA: fit-contract -->`, `<!-- ENGINEERING-DNA: scale-to-fit -->`, etc. These are language-agnostic stable identifiers used by `evals/hard_checks.py:check_ds_engineering_dna`.

Steps:

1. Fill brand-variable placeholders from `$WS/decisions.json` + `$WS/brand.json` (palette hex, font families, brand name, etc.).
2. **Logo embed**: paste the contents of `$WS/assets/logo.embed.html` directly into the §4 Logo section's "Definition (once per HTML file)" block. `embed_logo.py` already produced the correct `<symbol id="brand-wm">` snippet — vector or base64-raster form, with hardcoded fills stripped so `currentColor` works. Do not regenerate this; do not re-extract paths.
3. Set `{{LOGO_VIEWBOX}}` placeholder in §4's `.logo` usage examples to match the viewBox in the embed snippet.
4. **Language pass** (only when Round 0 picked 中文): if Step 0 already routed you to `ds-template.zh.md`, the prose is already pre-translated — your work in this step is limited to (a) translating the brand-variable text you injected via placeholders (`{{PHILOSOPHY_PARAGRAPH}}`, `{{TYPE_PHILOSOPHY_NOTE}}`, etc.) and (b) checking that no English sentences leaked through. The output must be **single-language throughout** — no leftover English sentences mixed into a Chinese DS.

   **Translate everything that is prose**, including:
   - Chapter titles (`## 1. Design Philosophy` → `## 1. 设计理念`)
   - Section narration paragraphs
   - The Constraints / Freedom / Bespoke bullet contents
   - The Design Taste anti-AI-slop rules
   - Slide-type descriptions in §6
   - The pre-ship Checklist labels (§13)
   - Anti-pattern explanations
   - All the words around the code blocks

   **Never translate**:
   - Token names: `--primary`, `--accent`, `--surface`, `--ink`, `--mid`, `--rule`, `--tint`, `--green`, `--red`, `--warn`, `--teal`, plus brand-palette tokens
   - All CSS / JS / HTML code blocks (every fenced ```css ``` ```js ``` ```html ``` block stays as-is)
   - Hex values, viewBox numbers, file names, URLs
   - **HTML comment anchors**: `<!-- ENGINEERING-DNA: fit-contract -->`, `<!-- ENGINEERING-DNA: typography-safety -->`, etc. These are stable identifiers — the prose around them adapts; the IDs stay.

   **How the engineering-DNA hard check works under translation**: `evals/hard_checks.py:check_ds_engineering_dna` reads the markdown looking for `<!-- ENGINEERING-DNA: <id> -->` HTML comments — NOT for the English chapter titles. As long as you preserve the comment anchors verbatim, the chapter heading and surrounding prose can be in any language. So `### 5.1 单页适配契约 <!-- ENGINEERING-DNA: fit-contract -->` passes the check the same as the English original.
5. Write the final markdown to the user's chosen path. Default: `./{{BRAND_SLUG}}-PPT-Design-System.md`. Confirm path before writing if it would overwrite an existing file.

### Phase 4 — Verification deck + runtime hard checks (MANDATORY, not optional)

The DS markdown is the deliverable. The verification deck is the **proof that the DS produces correct slides**. Skipping this means shipping an unverified spec — don't.

<EXTREMELY-IMPORTANT>

**The Phase B fix-routing rule, enforced structurally.** When a hard check
fails, the fix lives in the brand DS — never in the deck alone. This is
not advice; this is the workflow contract that makes Phase B work at all,
because if you patch the deck to make the check pass, you've healed one
slide and left the spec wrong. The next deck built from this DS will have
the same bug; every other brand sharing the affected DS pattern will too.

**Starting now this is checked**: `hard_checks.py` includes a
`phase_b_workflow` check that hashes the deck and the DS each run. On a
re-run, if the deck changed but the DS didn't, the check FAILS with
`deck_modified_without_ds_update`. There is no way around this short of
also editing the DS — which is the point.

The correct loop is:
1. Run hard_checks → see which check fails.
2. Look up that check in `references/verification-deck-spec.md` §8 — it
   names the brand DS section that owns the rule.
3. Edit that DS section.
4. Regenerate the deck from the updated DS (literally re-do Phase 4a
   using the new DS as source).
5. Re-run hard_checks.

If after step 5 the same check still fails, the fix you applied to the
DS didn't actually capture the rule — go back to step 2 and read the
fix-mapping more carefully, or pick a different DS section.

</EXTREMELY-IMPORTANT>

**Step 4a — Write the verification deck.**
Read `references/verification-deck-spec.md`. It defines the 8 required slide types (cover, narrative+pullquote, two-column, data table, chart, flip cards, timeline, big pull-quote) and 6 coverage rules (multi-column collapse, click interaction, semantic colour, real numbers, bespoke composition, absorber variety). Write the deck to `~/deckify/decks/<brand>/<brand>-deck.html` using copy drawn from the recon corpus — **never invented stats**.

> **Where artefacts live**: every brand the user generates lands under `~/deckify/decks/<brand>/` (a fixed home-directory convention — independent of the cwd you happen to be in, the deckify source repo, or any project structure). The brand DS markdown, the verification deck, the persisted recon source, and per-run hard-check reports all live under that single tree. `~/deckify/` is created on first use; it is the only path you should write user artefacts to. Do not write into the deckify source repo (the maintainer's `decks/` there is a reference panel — not your output target).

**Step 4b — Run the runtime hard checks (deterministic).**

For Layer 2 (single brand the user just generated), run `hard_checks.py` directly. Cross-platform — only Python, no shell required:

```bash
# Pick a per-run output dir under ~/deckify/. Re-use the same out_dir across
# re-runs of the same brand — that's how phase_b_workflow can compare SHAs
# (it persists a .provenance.json there). A fresh timestamped dir per
# attempt also works; the gate will treat it as a first run each time.
REPORTS="$HOME/deckify/reports/runs/$(date +%Y-%m-%dT%H-%M-%S)"
mkdir -p "$REPORTS/per-sample/<brand>"

# 11 deterministic checks: slide dimensions (1280×720), fit contract intact,
# token-only colors, no emoji, mobile collapse at 375 px, logo renders,
# language consistency, text layout safe (no truncation, no glued-to-bottom),
# DS engineering DNA preserved, CJK font quality (zh decks only),
# AND phase_b_workflow (no deck-only fixes — see EXTREMELY-IMPORTANT above).
python3 <skill-path>/evals/hard_checks.py \
  "$HOME/deckify/decks/<brand>/<brand>-deck.html" \
  "$HOME/deckify/decks/<brand>/<brand>-PPT-Design-System.md" \
  "$REPORTS/per-sample/<brand>"
```

Phase A skill-author note: the multi-brand panel runner is `python3 tools/phase-a/run_phase_a.py` — see `tools/phase-a/README.md`. That tool is for skill maintainers tuning the deckify skill against the reference brand panel; it writes to the deckify repo's `tests/reports/`, not to `~/deckify/`. End-user runs always use `~/deckify/`.

**Step 4c — On any hard-check failure, FIX THE BRAND DS — never the deck alone.**
See the `<EXTREMELY-IMPORTANT>` block above. The brand DS markdown is your tunable; the deck is the verification artifact. When a check fails, trace it to the relevant section of *your brand's DS* (use the fail → DS-section mapping table in `references/verification-deck-spec.md` §8), update the DS, regenerate the deck from the updated DS, re-run hard checks.

Iterate until hard checks are 10/11+ PASS (cjk_font_quality is soft for en decks; the rest including phase_b_workflow must all pass).

### Phase 5 — Visual judge (LLM, you) — MANDATORY

Hard checks measure DOM shapes; they don't measure whether the deck *looks* on-brand. That's your job.

Phase 5 is **single-brand** — it scores the one deck the user just generated. Do not iterate over a panel here; that's Layer 1 (skill-author territory, see `evals/run_phase_a.py`).

**Step 5a — Read the per-slide screenshots.**
For the user's brand at `~/deckify/reports/runs/<latest>/per-sample/<brand>/slides/`, view the PNGs using your host's image-viewing capability (`Read` tool in Claude Code, equivalents elsewhere). Re-read the brand's DS markdown for context.

**Step 5b — Score against the rubric.**
Read `evals/rubric.json` — 6 dimensions (logo present and branded, slide visual quality, brand fidelity, content substantive, engineering DNA visible in DS, CJK typography quality for zh decks), each 0–5. Plus 5 disqualifiers (D1 logo missing, D2 dimensions wrong, D3 console errors, D4 mobile horizontal scroll, D5 DS template violated).

For `cjk_typography_quality`: this is a vision-judged quality score, not a hard constraint. The hard check `cjk_font_quality` only catches the absolute bug (zero CJK fonts in chain). The judge dimension catches "the CJK is technically rendering, but looks thin / cheap / mismatched with Latin / wrong weight / wrong serif-vs-sans pairing." If you score this ≤ 3, the fix routes to DS §3 CJK 字体回退链 — typically swap CJK family to front of font-family chain AND bump body font-weight to 500/600. en decks return 5 for this dimension (not applicable).

**Step 5c — Write `judge.json`.**
Land at `~/deckify/reports/runs/<latest>/per-sample/<brand>/judge.json` with this schema:

```json
{
  "ok": true,
  "judged_by": "<your model id>",
  "scores": {
    "scores": {
      "logo_present_and_branded":      0,
      "slide_visual_quality":          0,
      "brand_fidelity":                0,
      "content_substantive":           0,
      "engineering_dna_visible_in_ds": 0,
      "cjk_typography_quality":        0
    },
    "reasoning": "<2-3 sentences explaining the lowest scores>",
    "regression_flags": []
  }
}
```

**Step 5d — Aggregate (single brand).**

```bash
python3 <skill-path>/evals/build_report.py <run-dir> 4 \
  "<brand>|<source-url>|$HOME/deckify/decks/<brand>/<brand>-deck.html|$HOME/deckify/decks/<brand>/<brand>-PPT-Design-System.md"
```

PASS criteria (per `rubric.json`): hard 9/10+ AND judge avg ≥ 4 AND no disqualifier triggered.

**Step 5e — Failure handling.** All routes go to **the user's brand DS** (this is Layer 2; never edit skill source from a Phase 5 failure):
- Judge score < 4 on `brand_fidelity` → revisit `~/deckify/decks/<brand>/source/brand.json` (was the mood paragraph too generic? did the palette flatten to white+grey+single-accent?). Update with sharper evidence, regenerate the brand DS §1 + §2, regenerate the deck, re-judge.
- Judge score < 4 on `slide_visual_quality` → tighten the user's brand DS §6 (per-slide-type spec) or §7 (component density), regenerate the deck, re-judge.
- Judge score < 4 on `content_substantive` → the Phase 1 recon corpus was thin; widen `pages.txt` to broader subpages OR pull more verbatim phrases from existing recon screenshots into the deck.
- Judge score < 4 on `engineering_dna_visible_in_ds` → the user's brand DS is missing a required chapter or it got diluted during the language pass. Restore the chapter verbatim from `references/ds-template.md` (or `.zh.md` for zh decks).
- Judge score < 4 on `cjk_typography_quality` → fix `~/deckify/decks/<brand>/<brand>-PPT-Design-System.md` §3 CJK 字体回退链, then propagate the new font-family chain into the deck.
- Disqualifier triggered → see the fail-mapping table in `references/verification-deck-spec.md` §8.

Iterate until PASS. The skill is not done until both hard 9/10+ AND judge ≥ 4.

### Phase 6 — Persist + hand back

**Step 6a — Persist durable artifacts out of the temp workspace.** Before the OS sweeps `$WS`, copy the parts that encode user judgment + LLM synthesis into the user's home deckify directory:

```bash
python3 <skill-path>/scripts/persist_brand_source.py "$WS" <brand-slug>
```

This copies `brand.json`, `decisions.json`, `pages.txt`, and `assets/` (logo files) from `$WS` into `~/deckify/decks/<brand-slug>/source/` — sitting next to the DS markdown and the deck HTML. The `recon/` DOM dumps + `raw-assets.json` are intentionally **not** copied — those are large + regenerable from the URL, and the OS will sweep them on its own.

After this step, the brand has a complete persisted bundle in the user's home tree:

```
~/deckify/
└── decks/
    └── <brand>/
        ├── <brand>-PPT-Design-System.md   ← the deliverable
        ├── <brand>-deck.html              ← verification deck
        └── source/
            ├── brand.json                 ← LLM synthesis
            ├── decisions.json             ← user choices (Phase 2)
            ├── pages.txt                  ← LLM-picked subpages
            └── assets/                    ← embedded logo files
                ├── logo.svg
                ├── logo.embed.html
                ├── logo.dataurl
                └── logo.report.json
```

Per-run hard-check + judge reports live alongside, under `~/deckify/reports/runs/<ts>/per-sample/<brand>/`.

**Step 6b — Hand back to the user.**

Give the user:
1. The DS markdown path + the deck HTML path (both under `~/deckify/decks/<brand>/`)
2. A 5-line summary: palette, font, logo source, aesthetic mood, slide-type emphasis
3. The eval scoreboard: hard 10/11+, judge avg, status PASS/WARN/FAIL
4. Path to `~/deckify/reports/runs/<latest>/summary.md` for the full per-brand breakdown

**Step 6c — Print the closing message.** After the summary above, print exactly one of these two closing blocks depending on `decisions.json.language`. The closing is a real piece of writing, not flavour text — preserve every word, including the line breaks. Print it AFTER the deliverable summary so the user has already seen what they got, then read this as the parting thought.

**English** (default):
```
═══════════════════════════════════════════════════════════════════════

Done.

You're holding two things: a Design System markdown that you — or any
AI agent — can use forever to build precise, brand-faithful slides;
and a sample deck that proves the spec works.

Notice what just happened. You didn't open PowerPoint. You didn't
move a single text box. You didn't fight a template. PPT was built
for **humans to draw with their hands** — every box, every gradient,
every line spacing, hand-placed. That made sense for fifty years.

The job has changed. Slides are no longer drawn; they're **imagined
and described**. The author has shifted from human to AI, and AI's
native medium isn't `.pptx` binary — it's HTML. Living markup,
animatable, queryable, transformable, copy-paste-able into any
conversation. Where PPT slows AI down, HTML lets it run.

Welcome to the deck for the AI era.

                                                          — deckify
═══════════════════════════════════════════════════════════════════════
```

**中文** (when `decisions.json.language === "中文"`):
```
═══════════════════════════════════════════════════════════════════════

完成了。

你现在拥有两份东西：一份 Design System markdown —— 你或任何 AI agent 都能
拿它无限次地生成贴合这个品牌的精准 slides；一份示范 deck，证明这套规范确实
可以工作。

留意一下刚才发生了什么。你没有打开 PowerPoint。你没有挪动一个文本框。你没
有跟模板较劲。PPT 是 **为「人手绘」而设计的** —— 每个方块、每段渐变、每行
间距，都靠手摆。这在过去五十年里讲得通。

但 slide 的制作方式变了。slide 不再被「画」出来，它们被 **想象出来、描述
出来**。创作者已经从人变成了 AI，而 AI 的母语不是 `.pptx` 二进制 —— 是
HTML。活的标签、可动画、可被查询、可被改写、可粘贴进任何对话。PPT 拖慢
AI 的地方，HTML 让 AI 跑起来。

欢迎来到 AI 时代的 deck。

                                                          — deckify
═══════════════════════════════════════════════════════════════════════
```

## Hard rules — engineering DNA (NEVER violate, NEVER simplify)

These parts of the generated DS must be copied verbatim from `references/ds-template.md`. They came from real, painful bugs. If you find yourself thinking "this section is overkill, let me trim it," stop — you are about to reintroduce a bug someone else already fixed.

1. **Single-Slide Fit Contract**: 1280×720 fixed canvas; three-layer `overflow:hidden` safety net (`.slide`, `.sw .sc`, and any `flex:1` absorber); single-absorber rule; 602px content-height budget math; pre-build height checklist; verify at native 1280×720 (the `transform:scale()` masks overflow at scaled sizes).
2. **Logo as SVG `<symbol>` + `currentColor`**: `<symbol>` defined once in a hidden `<svg>` block at the top of `<body>`; referenced via `<use href="#…">`; `fill: currentColor` set on the outer `<svg>` (NOT on the `<path>` — selectors don't pierce shadow DOM). Variants: `.W` (white-on-dark), `.L` (brand-dark-on-light).
3. **Token-only color**: every color in slides comes from `:root` CSS variables. No ad-hoc hex values. Token *names* stay stable across brands (`--primary`, `--accent`, `--surface`, `--ink`, `--mid`, `--rule`, `--tint`, `--green`, `--red`, `--warn`, `--teal`) even when the actual hex differs — so downstream slide code doesn't need to know which DS it's using.
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
- `scripts/fetch_sitemap.py` — step 1a: home + sitemap + nav-links + JSON-LD.
- `scripts/fetch_pages.py` — step 1c: batch-fetch a URL list with full per-page probes.
- `scripts/enumerate_assets.py` — step 1d: aggregate all probes into raw-assets.json with stable candidate ids.
- `scripts/embed_logo.py` — step 1f: navigate-to-asset-then-same-origin-fetch + quality-gate + base64-embed the chosen logo. Handles cross-origin CDN (Contentful, Cloudinary).
- `scripts/setup.py` — Phase 0 dependency check.
- `evals/` — quality contract directory (see `evals/README.md`). Two layers in one folder:
  - `evals/evals.json` + `evals/trigger_evals.json` — marketplace harness contract (Anthropic skill-eval format).
  - `evals/hard_checks.py` + `evals/rubric.json` + `evals/build_report.py` — Layer 2 runtime auto-eval invoked by Phase 4-5 (cross-platform Python; no shell wrapper).
  - `evals/run_phase_a.py` — Layer 1 multi-brand panel orchestrator (skill author use only, not part of the runtime path).
- `tests/` — unit + integration + smoke tests.
