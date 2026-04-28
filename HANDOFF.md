# Handoff for the next session

> Last updated: mid-session 2026-04-27 (skill upgrade pass — see §A below).
> Read this file in full before doing anything. CLAUDE.md at the project root is the canonical project rules; this HANDOFF.md is the rolling state log.

## TL;DR

You're picking up the **deckify** project. The skill architecture is done; **Unilever** is fully validated (9-slide verification deck, hard 8/8 PASS, visually verified at 1920×1080 / 1440×900 / 1280×720 / 375×812 mobile). The repo now carries a **CLAUDE.md** anchoring the core rule that all eval failures must be fixed in the skill, never in a single deck.

**Your job**: run Phase 1 → 4 for **P&G** and **Stripe** using the upgraded skill (scale-to-fit + design-taste + verification-deck-spec), then run final eval and confirm all three brands PASS.

The user prefers **中文 replies**, no external API keys (you're the LLM), and absolutely no typographic-placeholder logos or mixed-language DS.

---

## A. What changed this session (skill-level upgrades)

Read these BEFORE touching any new brand:

1. **CLAUDE.md** at the project root (new). The core rule: when eval reveals a deck-level issue, fix the SKILL artifact (DS template / prompt / script), not the deck. Decks are downstream artifacts. Patching a deck while the skill stays broken means the next brand will hit the same bug.

2. **skills/deckify/references/verification-deck-spec.md** (new). 8 required slide types every Phase 4 verification deck must contain — cover, narrative+pullquote, two-col, table, chart, flip cards, timeline, pull-quote — plus 6 coverage rules (mobile collapse, click interaction, semantic colour, real numbers, bespoke composition, absorber variety). Read this before writing any new brand's deck.

3. **skills/deckify/references/ds-template.md** §5 (engineering-DNA). New "Fullscreen fit — scale-to-fit at runtime" subsection mandates a CSS-transform scale on `#deck` so the 1280×720 canvas fills any viewport without warping the type scale. Without this, a deck has visible 320×180 px black borders on a 1920×1080 viewport. Every brand DS must wire the scale-to-fit JS into its verification deck. §10 mobile gains `.cov, .sw { min-height: 100dvh }` so cover backgrounds fill the full mobile viewport.

4. **ds-template.md §1 + llm-prompts/synthesize-brand.md** carry a Design Taste subsection inspired by compound-engineering's frontend-design skill. Forbids generic font defaults (Inter, Arial, system-ui as the "design choice"), cliché white+grey+single-accent palettes, even-weighted accent grids, off-the-shelf SaaS chrome, and vague mood language. Pushes the synthesizer toward bold, specific aesthetic commitments.

The Unilever DS markdown + verification deck have been regenerated to carry all four upgrades. P&G and Stripe **must** use the upgraded skill — re-read ds-template.md / synthesize-brand.md before starting.

---

## 0. Quick orientation

```bash
cd ~/Development/Projects/deckify
git log --oneline                          # see what's done
ls samples/unilever/                       # Phase 1 output for Unilever
cat decks/unilever/unilever-PPT-Design-System.md | head -100   # the DS that came out
```

The skill is installed via symlink:
```
~/.claude/skills/deckify → ~/Development/Projects/deckify/skills/deckify
```

GitHub: https://github.com/seacen/deckify (private, account: seacen)

---

## 1. What this skill is

**deckify** turns a brand URL into a production-ready Design System markdown that other agents (or future you) can use as a spec to build precise, mobile-friendly HTML slides in the brand's visual language.

The actual deliverable is `decks/<brand>/<brand>-PPT-Design-System.md`. HTML decks (`<brand>-deck.html`) are **verification samples** — proof that the DS spec produces good slides.

## 2. Architecture (read SKILL.md for full)

**Thin deterministic harness + fat LLM exploration.** Python/bash scripts only do what's deterministic (fetch pages, enumerate candidates, quality-gate logos, base64-embed). All judgment — *which subpages to fetch*, *which SVG is the real wordmark*, *what the brand palette actually is* — is done by **you, the agent running the skill**, guided by `references/llm-prompts/`.

There is **no external LLM API call**. No `_request.json` / `_response.json` middle layer. When the pipeline hits a step that needs judgment, you do that step directly, in this conversation.

### Phase 1 — five-step pipeline (per brand)

```
1a. fetch_sitemap.sh <url> $WS
    → recon/{home.html, home.png, sitemap-urls.txt, nav-links.json, jsonld.json}

1b. (you, the LLM)
    Read references/llm-prompts/discover-pages.md
    Read recon/{nav-links.json, sitemap-urls.txt, jsonld.json}
    Pick 5–8 high-value subpages (about/brand/press/leadership/etc.)
    Write $WS/pages.txt (one URL per line, # comments OK)

1c. fetch_pages.sh $WS/pages.txt $WS
    → recon/pages/<slug>/{dom.html, shot.png, probe.json}
    Per-page probe captures: every inline SVG, every <img>, every bg-image url(),
    every JSON-LD logo, every :root var, every @font-face src, computed styles.

1d. enumerate_assets.py $WS
    → raw-assets.json (all logo candidates with stable id, color frequencies,
                       fonts, computed palette, etc.)
    Python doesn't pick anything — just enumerates with a stable id per candidate.

1e. (you, the LLM)
    Read references/llm-prompts/synthesize-brand.md
    Read raw-assets.json
    Use Read tool on screenshots (recon/pages/<slug>/shot.png)
    Pick chosen_logo (by id), build palette/typography/aesthetic
    Write $WS/brand.json (with chosen_logo.id + 2-3 alt_logo_ids)

1f. embed_logo.py $WS
    Looks up chosen_logo.id, fetches via agent-browser (passes anti-bot CDNs),
    quality-gates (SVG path d ≥ 40 chars OR <image> child; raster ≥ 64×64),
    strips hardcoded fills + <style> blocks (so currentColor cascades),
    writes $WS/assets/{logo.svg|png, logo.embed.html, logo.dataurl}.
    If quality gate fails, swap chosen_logo.id to next alt and rerun.
    If all alts fail, STOP and ask the user for a logo file. Never invent one.
```

### Phase 3 — generation

Read `references/ds-template.md` (864 lines, **all English** as of last commit). Fill these placeholders from `brand.json`:

```
{{BRAND_NAME}}, {{BRAND_SLUG}}, {{PHILOSOPHY_PARAGRAPH}},
{{NAVY_HEX}}, {{BLUE_HEX}}, {{SURFACE_HEX}}, {{INK_HEX}}, {{MID_HEX}}, {{RULE_HEX}}, {{TINT_HEX}},
{{GREEN_HEX}}, {{GREEN_BG_HEX}}, {{RED_HEX}}, {{RED_BG_HEX}}, {{WARN_HEX}}, {{WARN_BG_HEX}}, {{TEAL_HEX}}, {{TEAL_BG_HEX}},
{{PRIMARY_FONT}}, {{FONT_RESTRICTION_NOTES}}, {{FALLBACK_FONT}}, {{FALLBACK_USE_CASE}}, {{WEIGHT_RANGE}}, {{ITALIC_NOTE}}, {{ITALIC_NOTE_SHORT}}, {{TYPE_PHILOSOPHY_NOTE}},
{{LOGO_VIEWBOX}}, {{LOGO_PATH_ELEMENTS}}, {{LOGO_HEIGHT}}, {{LOGO_W}}, {{LOGO_H}}, {{LOGO_BRAND_RESTRICTIONS_NOTE}}, {{LOGO_BASE64}},
{{COVER_BACKGROUND}}, {{BORDER_RADIUS}}, {{FLIP_BACK_COLOR}},
{{IMAGERY_PHILOSOPHY_NOTE}}, {{EMPHASIZED_TYPES_LIST}}, {{DEEMPHASIZED_TYPES_LIST}}, {{SLIDE_TYPE_EMPHASIS_NOTE}},
{{BESPOKE_EXAMPLES_PARAGRAPH}}
```

A working reference for how to do this is the python script in this commit's history at `decks/unilever/unilever-PPT-Design-System.md` — read it as an example.

For `{{LOGO_PATH_ELEMENTS}}`: extract the inner content of `<symbol>...</symbol>` from `samples/<brand>/assets/logo.embed.html`.

**Language rule (Phase 3 step 4)**: if the user picked non-English in Phase 2 Round 0, do a translation pass over **prose only** (philosophy, aesthetic notes, anti-patterns, checklist labels). **Never translate**: token names (`--primary`), CSS/JS/HTML code, viewBox numbers, hex values, comment markers like `<!-- ENGINEERING-DNA -->`. Output must be **single-language throughout** — no leftover English in a Chinese DS.

### Phase 4 — verification

Use the DS as a spec to write a sample HTML deck (cover + 2-3 content slides) at `decks/<brand>/<brand>-deck.html`. Then run the eval and confirm PASS.

---

## 3. What's already done

```
✅ Architecture (5-step Phase 1 + agent-browser default fetch + eval framework)
✅ All Phase 1 scripts written and tested
✅ Two LLM-guideline files (discover-pages.md, synthesize-brand.md)
✅ ds-template.md is 100% English (28 lines of mixed Chinese were cleaned up)
✅ SKILL.md updated for the new architecture + Phase 3 translation rule
✅ Repo set up + pushed to GitHub (https://github.com/seacen/deckify)
✅ Symlink ~/.claude/skills/deckify → repo (Claude can load the skill)

✅ UNILEVER Phase 1 end-to-end validated:
   samples/unilever/brand.json            (5-color palette from real --color-brand-* tokens)
   samples/unilever/pages.txt             (6 high-value subpages)
   samples/unilever/raw-assets.json       (136 candidates, gitignored — regenerable)
   samples/unilever/recon/                (DOM dumps + screenshots, gitignored)
   samples/unilever/assets/logo.embed.html (favicon.svg, 23 path elements, real wordmark)

✅ UNILEVER Phase 3 done:
   decks/unilever/unilever-PPT-Design-System.md  (871 lines, all English, all placeholders filled)
```

---

## 4. ✨ What YOU need to do

### Step 1 — Unilever DONE ✓

`decks/unilever/unilever-deck.html` is the 9-slide verification deck per `skills/deckify/references/verification-deck-spec.md`. Hard 8/8 PASS. Visually verified at 1920×1080 (perfect fill), 1440×900 (fills horizontally; 45 px letterbox top/bottom is unavoidable on 16:10 viewports), 1280×720 (perfect), 375×812 mobile (cover + content fill the full viewport with `min-height: 100dvh`).

Judge step still pending — when you next run a full eval, write `judge.json` per the instructions printed by `bash skills/deckify/evals/run.sh`.

### Step 2 — P&G Phase 1 + Phase 3 + Phase 4 (apply upgraded skill)

```bash
WS=/tmp/web-to-ds/pg
rm -rf "$WS" && mkdir -p "$WS"
bash skills/deckify/scripts/fetch_sitemap.sh https://www.pg.com "$WS"
# Then YOU pick subpages (read discover-pages.md guideline):
#   /who-we-are, /brands, /sustainability, /news, /investors, /careers
# Write $WS/pages.txt
bash skills/deckify/scripts/fetch_pages.sh "$WS/pages.txt" "$WS"
python3 skills/deckify/scripts/enumerate_assets.py "$WS"
# Then YOU read raw-assets.json + screenshots and write $WS/brand.json
# (per synthesize-brand.md guideline)
python3 skills/deckify/scripts/embed_logo.py "$WS"

# Copy small artifacts into repo
mkdir -p samples/pg
cp $WS/brand.json $WS/pages.txt samples/pg/
cp -r $WS/assets samples/pg/

# Generate the DS markdown (use the same fill-template python pattern
# as the one used for Unilever — see git log for the snippet)
# Output: decks/pg/pg-PPT-Design-System.md

# Then write decks/pg/pg-deck.html (verification sample) using the new DS.
```

### Step 3 — Stripe (same as P&G)

URL: https://stripe.com  
Sitemap is rich; pick from /about, /customers, /newsroom, /atlas, /payments, /press.

### Step 4 — Run eval and confirm all three PASS

```bash
bash skills/deckify/evals/run.sh
# Then write judge.json for each brand (read screenshots, score per rubric).
# Re-run build_report.py to aggregate.
# Target: 3/3 PASS.
```

### Step 5 — Commit + push when green

```bash
git add -A
git commit -m "Phase 4 verification: unilever / pg / stripe all PASS"
git push
```

---

## 5. ⚠️ Hard rules (these have already burned us — don't repeat)

1. **Typographic placeholder is a build failure.** A `<symbol>` whose only content is `<text>` of the brand name (e.g. `<text>P&G</text>`, single-letter disc) **will fail `logo_renders` hard check**. If quality gate rejects all candidates, **stop and ask the user**. Never invent.

2. **Embed_logo.py defaults to agent-browser** for HTTP — Unilever, Stripe, P&G all have anti-bot CDNs that 403 stdlib urllib + curl. Don't add a "fallback to urllib" thinking it's safer. The browser path is *the* path.

3. **DS must be single-language**. The template is English. If user picks 中文 in Round 0, translate prose only — never tokens/CSS/code/hex/viewBox. No half-translation. (Last session burned us: §3.1 was Chinese while §3 was English. Took a fix-up commit.)

4. **Token names are stable across brands**: `--primary`, `--accent`, `--surface`, `--ink`, `--mid`, `--rule`, `--tint`, `--green`, `--red`, `--warn`, `--teal`. Hex values change, names don't. This is so downstream slide code is brand-agnostic.

5. **Engineering DNA chapters are verbatim** — never trim, simplify, or "improve". They came from real production bugs:
   - §3.1 Typography Safety
   - §5 Slide Architecture (fit contract, three-layer overflow safety net, single-absorber rule, 602px content budget)
   - §10 Mobile (inline-flex trap catch-all, flip-card mobile fix)
   - §13 Pre-ship checklist (verify at 375px width)

6. **fill="#FFFFFF" on inner SVG paths breaks `currentColor`**. embed_logo.py already strips these — don't add hardcoded fills back during Phase 3.

7. **No emoji in the DS or in sample decks**. Typographic symbols (`✓ − ! × → ←`) are OK. `👍🎉🔥` etc. are forbidden.

8. **The user wants 中文 replies** (set in `~/.claude/CLAUDE.md`). Code/file names/CSS/error messages stay English; conversational prose is Chinese.

---

## 6. File map

```
~/Development/Projects/deckify/
├── HANDOFF.md                                     ← you are here
├── README.md                                      ← project overview
├── .gitignore                                     ← excludes recon/ + raw-assets.json
├── skills/deckify/                                ← the skill (symlinked into ~/.claude/skills/)
│   ├── SKILL.md                                   ← READ FIRST. 4-phase pipeline.
│   ├── README.md
│   ├── scripts/
│   │   ├── fetch_sitemap.sh                       (Phase 1a)
│   │   ├── fetch_pages.sh                         (Phase 1c)
│   │   ├── enumerate_assets.py                    (Phase 1d)
│   │   ├── embed_logo.py                          (Phase 1f, defaults to agent-browser)
│   │   └── setup.sh                               (Phase 0 dep check)
│   ├── references/
│   │   ├── ds-template.md                         (DS template, ALL ENGLISH)
│   │   ├── decision-questions.md                  (Phase 2 question bank)
│   │   └── llm-prompts/
│   │       ├── discover-pages.md                  (read at step 1b)
│   │       └── synthesize-brand.md                (read at step 1e)
│   └── eval/
│       ├── run.sh                                 (entry point)
│       ├── rubric.json                            (8 hard checks + 5 judge dims)
│       ├── hard_checks.py                         (DOM measurement via agent-browser)
│       └── build_report.py                        (aggregator)
├── samples/
│   └── unilever/                                  ← reference example, complete
│       ├── brand.json                             (LLM synthesis output)
│       ├── pages.txt                              (LLM-picked subpages)
│       └── assets/logo.embed.html                 (real wordmark, ready to paste)
└── decks/
    ├── unilever/
    │   ├── unilever-PPT-Design-System.md          ← the actual skill output (DONE, English)
    │   └── unilever-deck.html                     ← STALE — your job to regenerate
    ├── pg/
    │   ├── pg-PPT-Design-System.md                ← stale (old version)
    │   └── pg-deck.html                           ← stale
    └── stripe/                                    ← stale
```

---

## 7. Useful commands

```bash
# Verify symlink
ls -la ~/.claude/skills/deckify

# Run a fresh Phase 1 on a new URL
WS=/tmp/web-to-ds/<brand>
mkdir -p "$WS"
bash skills/deckify/scripts/fetch_sitemap.sh <url> "$WS"
# you write $WS/pages.txt
bash skills/deckify/scripts/fetch_pages.sh "$WS/pages.txt" "$WS"
python3 skills/deckify/scripts/enumerate_assets.py "$WS"
# you write $WS/brand.json
python3 skills/deckify/scripts/embed_logo.py "$WS"

# Inspect what enumerate_assets caught
python3 -c "
import json
r = json.load(open('$WS/raw-assets.json'))
print('logo candidates:', len(r['logo_candidates']))
for c in r['logo_candidates'][:8]:
    print(' ', c['id'], c['kind'], c.get('region',''), c.get('width',''),'x',c.get('height',''),
          'src=', (c.get('src') or c.get('href') or '')[:60])
print('top colors:')
for c in r['color_frequency'][:6]:
    print(' ', c['hex'], c['count'])
print('fonts:', [f['family'] for f in r['fonts']['frequencies'][:4]])
print('root vars containing brand:', [k for k in r['root_vars'] if 'brand' in k.lower()][:8])
"

# Run eval (after decks are regenerated)
bash skills/deckify/evals/run.sh

# Latest report
cat skills/deckify/tests/reports/latest.md
```

---

## 8. User context (from prior conversations)

- **Communication**: 中文 (set in `~/.claude/CLAUDE.md` as a global preference). Code stays English.
- **No API keys**: agent (you) is the LLM. No Anthropic key, no OpenAI key. Don't suggest setting one up.
- **Anti-bot is real**: Unilever / P&G CDNs reject stdlib HTTP. agent-browser is *the* HTTP client.
- **Quality bar**: user has explicitly said "我们不能妥协或者牺牲测试的标准" — don't lower thresholds to make things pass. Fix the deck.
- **Project trajectory**: this is the user's evening project. They have other repos at `~/Development/Projects/` (OfficeMemoryST, etc.) that they reference. Treat deckify as polished, public-shareable code (private repo for now).

---

## 9. Open questions / known issues

- `samples/unilever/raw-assets.json` is gitignored (132KB; regenerable from recon/ which is also gitignored). If you need to inspect it on a fresh clone, re-run Phase 1 1c+1d.
- `embed_logo.py` does an `agent-browser open <referer>` before each fetch — if you make many calls, this opens the same page multiple times. Acceptable for now; could batch later.
- **embed_logo.py cross-origin CDN fetches fail** (surfaced on P&G 2026-04-27). When the JSON-LD canonical logo lives on a third-party CMS CDN (e.g. Contentful's `images.ctfassets.net`), CORS headers block the script's in-page `fetch()` from the referer page. `agent-browser open <url>` works (full navigation, no CORS) but the script does an eval-fetch that fails. The script silently falls back to alt logo IDs (e.g. `apple-touch-icon.png` from the brand's own host), which is usable but skips the canonical brand asset. Fix: when the asset host differs from the referer host, navigate directly to the asset URL and extract bytes from there. Tracked as Task #17.
- Some Unilever utility-icon SVGs got embedded into raw-assets.json (~40KB). Not a problem because LLM correctly ignores them, but the file is bigger than necessary. Future optimization: filter by viewBox at enumerate time.

---

## 10. If you get stuck

- Re-read SKILL.md from the top.
- Re-read this HANDOFF.md.
- Look at `samples/unilever/` as a known-good reference.
- The git log has every architectural decision documented in commit messages.
- Ask the user — they have full context and prefer being asked over silent assumptions.

Good luck. Ship green.
