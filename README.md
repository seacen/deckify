# Deckify

> Turn any reference URL into a production-ready Design System markdown that other agents can use to build precise, mobile-friendly HTML slides in the brand's visual language.

## What's in this repo

```
deckify/
├── skills/
│   └── deckify/      ← the Claude skill (install via symlink to ~/.claude/skills/)
│       ├── SKILL.md               ← entry point, defines the 4-phase pipeline
│       ├── scripts/               ← deterministic Python/bash (fetch, enumerate, embed)
│       ├── references/            ← DS template + LLM guideline prompts
│       └── eval/                  ← hard checks + agent-as-judge framework
├── samples/
│   └── <brand>/                   ← Phase 1 pipeline output per brand
│       ├── brand.json             ← LLM-synthesized brand profile (palette / type / logo)
│       ├── pages.txt              ← LLM-chosen subpages
│       └── assets/logo.embed.html ← validated <symbol> snippet ready to paste
└── decks/
    └── <brand>/
        ├── <brand>-PPT-Design-System.md   ← the actual skill output
        └── <brand>-deck.html              ← verification sample deck
```

## Architecture

**Thin deterministic harness + fat LLM exploration.** Python scripts only do what's deterministic (fetch pages, enumerate candidates, quality-gate logos, embed assets). Anything that requires judgment — *which subpages are worth fetching*, *which SVG is the real wordmark*, *what the brand palette actually is* — is done by the LLM running the skill, guided by `references/llm-prompts/`.

There are no `_request.json` / `_response.json` middle layers. The agent running the skill is itself an LLM; when it hits a step that needs judgment, it does that step directly — no "external API to call" abstraction.

## Phase 1 (recon) — five steps

```
1a. fetch_sitemap.sh   → home + sitemap + nav-links + JSON-LD
1b. (LLM picks pages)  → writes pages.txt per discover-pages.md guideline
1c. fetch_pages.sh     → batch DOM/CSS/screenshot for each chosen URL
1d. enumerate_assets   → aggregate all candidates → raw-assets.json
1e. (LLM synthesizes)  → brand.json per synthesize-brand.md guideline
1f. embed_logo.py      → quality-gate + base64 embed → assets/logo.embed.html
```

`embed_logo.py` defaults to **agent-browser** as its HTTP client (real Chrome, passes anti-bot/TLS quirks on enterprise CDNs).

## Setup

```bash
# Install the skill into Claude
ln -s "$(pwd)/skills/deckify" ~/.claude/skills/deckify

# Verify dependencies (agent-browser, python3, curl)
bash skills/deckify/scripts/setup.sh
```

## Run a sample

In Claude, point the skill at a brand URL:

> "Use the deckify skill to extract a Design System from https://www.unilever.com"

The skill will run Phase 1 → ask you to confirm the synthesized palette/typography → generate `decks/unilever/unilever-PPT-Design-System.md`.

## Eval

```bash
bash skills/deckify/eval/run.sh
```

Two layers:
- **Hard checks** (deterministic): slide dimensions, fit contract, token-only colors, no emoji, mobile collapse, real logo, text layout safe, DS engineering DNA. See `eval/rubric.json`.
- **Vision judge** (the agent that ran the skill — no external API needed): scores logo fidelity, slide visual quality, brand fidelity, content substantiveness, engineering DNA presence. The agent reads the cover + 2 content screenshots from each sample, scores against the rubric, writes `judge.json`.

## Status

- ✅ Architecture: thin deterministic + LLM exploration with guideline-based judgment
- ✅ Phase 1 pipeline (5 steps + helper) end-to-end on Unilever
- ✅ DS markdown generated for Unilever (with real `--color-brand-*` tokens + real wordmark embed)
- ⏳ Verification: regenerate `unilever-deck.html` from the new DS, run eval to PASS
- ⏳ P&G + Stripe: re-run full pipeline + DS regeneration

## License

Private repo for now.
