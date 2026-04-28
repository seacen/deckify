# deckify

A Claude Code skill that turns a reference URL into a production-ready Design System markdown for HTML-slide authoring. Brand identity adapts to the source; engineering DNA (1280×720 fit contract, single-absorber rule, mobile inline-flex catch-all, flip-card mobile fix, logo-as-SVG-symbol pattern) stays invariant — those rules came from real, painful slide-deck bugs and the skill prevents you from re-learning any of them.

## What it does

Give it a URL. It will:

1. Use the [`agent-browser`](https://github.com/vercel-labs/agent-browser) CLI to render the live page, dump the DOM, take desktop + mobile screenshots, and probe `:root` CSS variables.
2. Run a deterministic Python parser to extract candidate brand colors, fonts, and logo sources.
3. Best-effort download the brand logo as SVG (or PNG fallback).
4. Read the screenshots with vision and form a hypothesis about the brand's mood.
5. **Ask you to confirm 3–4 key decisions** (palette anchor, primary font, aesthetic mood, slide-type emphasis) — never overfits a one-shot output.
6. Generate the Design System by filling brand-variable placeholders in `references/ds-template.md` while preserving the engineering DNA verbatim.
7. Optionally build a 3-slide sample deck to verify the DS actually produces what you expect.

## Install

```bash
# 1. The skill itself: this directory belongs in your Claude skills location.
#    For Claude Code default, put the folder at: ~/.claude/skills/deckify/

# 2. Run the dependency setup once per machine — it walks you through installing
#    agent-browser via your preferred package manager.
python3 scripts/setup.py
```

`setup.py` will:
- Check `python3` is available
- Check `agent-browser` is installed (and Chrome is set up via `agent-browser install`)
- If anything is missing, print the recommended install command for your platform (npm / brew / cargo) and link to https://github.com/vercel-labs/agent-browser

## Use

In Claude Code (or any agent that loads this skill), say something like:

```
build me a design system from https://www.unilever.com so I can author slides in their visual language
```

The skill triggers on any request that names a URL + slides/decks/design-system/visual-language. If it doesn't fire when you expect, say `/deckify <URL>` explicitly.

## Tests

```bash
# Reachability + DRY audit (no network)
bash tests/audit_skill.sh

# Full Phase 1 smoke against unilever.com (live web)
bash tests/smoke_unilever.sh

# 3-brand integration test (live web — stripe / apple / github)
bash tests/test_integration.sh

# LLM evals (run via skill-creator's run_loop.py — see TESTING.md)
```

See [`TESTING.md`](TESTING.md) for the full Skillify 10-step mapping — each layer has explicit artifacts and a verification cadence.

## File layout

```
deckify/
├── SKILL.md                          # The contract (what + when + how)
├── README.md                         # This file
├── TESTING.md                        # Skillify 10-step mapping for this skill
├── references/
│   ├── ds-template.md                # English DS template — brand placeholders + engineering DNA
│   ├── ds-template.zh.md             # Chinese sister template (CJK fallback chain, etc.)
│   ├── decision-questions.md         # Phase 2 user-confirmation checklist
│   ├── verification-deck-spec.md     # Phase 4 contract: 8 required slide types + fail-mapping table
│   └── llm-prompts/                  # Per-step prompts for the LLM half (discover-pages, synthesize-brand)
├── scripts/                          # All cross-platform Python (no bash dependency)
│   ├── setup.py                      # Dependency check + install guide
│   ├── init_workspace.py             # Create per-run workspace in OS tempdir
│   ├── fetch_sitemap.py              # 1a: home page + sitemap + nav-links + JSON-LD
│   ├── fetch_pages.py                # 1c: batch-fetch chosen URLs (DOM + screenshot + probe)
│   ├── enumerate_assets.py           # 1d: aggregate probes → raw-assets.json
│   ├── embed_logo.py                 # 1f: download + quality-gate + base64-embed logo
│   └── persist_brand_source.py       # 6a: copy durable artifacts out of tempdir into decks/<brand>/source/
├── tests/
│   ├── audit_skill.sh                # DRY + reachability audit
│   ├── smoke_unilever.sh             # End-to-end Phase 1 smoke (live)
│   └── test_integration.sh           # 3-brand integration test (live)
├── evals/
│   ├── evals.json                    # 4 LLM eval cases (varied brand archetypes + a deliverable end-to-end test)
│   └── trigger_evals.json            # 20 trigger queries for description optimization
└── assets/                           # Per-session logo storage (gitignored)
```

## Philosophy

This skill follows the **"thin harness, fat skill"** pattern from Garry Tan's [skillify](https://x.com/garrytan/article/2046876981711769720) and the **"separate brand-variable from engineering-DNA"** rule that a hard-won real-world DS distilled. The model's judgment lives in latent space (Phase 2 — mood synthesis); the deterministic work (color extraction, logo download, template fill) lives in scripts that always produce the same output. The two layers constrain each other.

The point is: this skill could not have been written without first making a real production deck and finding every layout bug it took to harden the engineering DNA. Skillification turns those discoveries into a permanent shared asset.

## Contributing / extending

If a new brand site breaks something:
1. Add a failing case to `evals/` (assertions on the trigger description and / or the output DS).
2. If the bug is in deterministic logic (Phase 1 scripts, hard-checks), add a hard-check rule in `evals/hard_checks.py` and reproduce locally.
3. If the bug is in latent judgment (LLM picks wrong logo / palette / mood), tighten the corresponding prompt in `references/llm-prompts/`.
4. Re-run `bash tests/audit_skill.sh` + `bash tests/smoke_unilever.sh` before sharing.

That's the loop. Same one Garry's article describes.
