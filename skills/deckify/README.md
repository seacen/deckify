# deckify

Turns a brand URL into a production-ready Design System markdown for HTML-slide authoring, plus a verified 9-slide sample deck. Brand identity adapts to the source; engineering DNA (1280×720 fit contract, single-absorber rule, three-layer overflow safety net, mobile inline-flex catch-all, flip-card mobile fix, logo-as-SVG-symbol pattern, CJK font fallback chain, scale-to-fit runtime) stays invariant — those rules came from real production-deck bugs, and the skill prevents you from re-learning any of them.

## Portability

deckify runs unchanged on **macOS, Linux, and Windows**, and is host-neutral: it works under Claude Code, Codex CLI, OpenClaw, or any agent / human runner. The runtime path is pure Python (stdlib + the `agent-browser` CLI) — no bash, no shell-only tools, no hardcoded paths. See `CLAUDE.md` §0 for the full portability invariant.

Dev-time tooling under `tests/*.sh` and the bash smoke scripts are bash-only by design (skill-author convenience); end users never invoke them.

## What it does

Give it a URL. The skill drives a 6-phase pipeline (see `SKILL.md`):

1. **Phase 0** — verify dependencies (`agent-browser` CLI installed, Chrome for Testing set up).
2. **Phase 1** — recon: fetch the site, screenshot subpages, probe `:root` CSS variables, enumerate every logo / colour / font candidate, embed the chosen logo as a clean SVG `<symbol>` with `currentColor`.
3. **Phase 2** — confirm with the user (interactive Q&A, host-portable): language (zh / en), ambiguous logo picks, contested palette, font fallback for proprietary faces.
4. **Phase 3** — generate the DS markdown by filling brand-variable placeholders in `references/ds-template.md` (or the Chinese sister `ds-template.zh.md`) while preserving engineering-DNA chapters verbatim.
5. **Phase 4** — write a 9-slide verification deck per `references/verification-deck-spec.md`, then run `evals/hard_checks.py` (10 deterministic DOM / regex checks).
6. **Phase 5** — visual judge: the LLM scores the rendered slides against `evals/rubric.json` (6 dimensions). Aggregate via `evals/build_report.py`. Pass = hard 9/10+ AND judge avg ≥ 4 AND no disqualifier.
7. **Phase 6** — persist durable artifacts (brand.json, decisions.json, pages.txt, assets/) from the OS tempdir into `decks/<brand>/source/` and hand back paths + scoreboard.

## Install

```bash
# 1. The skill itself belongs in your host's skill directory.
#    Claude Code default: ~/.claude/skills/deckify/
#    Other hosts: see your host's skill-loading docs.

# 2. Verify dependencies (cross-platform — same command on macOS / Linux / Windows)
python3 scripts/setup.py
```

`setup.py` checks Python 3.8+ and `agent-browser`, and prints the platform-appropriate install command (brew / npm / cargo / scoop / winget) if anything's missing.

## Use

In any agent that loads the skill, say something like:

```
build me a design system from https://www.unilever.com so I can author slides in their visual language
```

The skill triggers on any request naming a URL plus slides / decks / design-system / visual-language vocabulary.

## Test architecture

Three orthogonal test surfaces (`evals/README.md` is the authoritative description):

### Layer 1 — skill-quality optimization loop (Phase A)

Used by **us, the skill authors**, to make deckify better. Same `hard_checks.py` + `rubric.json` tooling as Layer 2, but scoped to a multi-brand panel and aimed at fixing **skill source code**.

```bash
# Run hard checks across the 5-brand panel (Unilever / P&G / Stripe / Apple / Coca-Cola)
python3 evals/run_phase_a.py

# After writing per-brand judge.json files (LLM step), aggregate the scoreboard
python3 evals/run_phase_a.py --aggregate-only
```

A failure in Layer 1 means the **skill source has a gap** (template / prompt / hard_check / script). The fix never goes into a single brand's DS — that heals one brand and lets the bug ship to all others. Trace upstream.

### Layer 2 — runtime per-user gate (Phase B)

Invoked automatically by `SKILL.md` Phase 4 every time the skill executes on a user's brand. Same tooling as Layer 1 but scoped to one brand. Failures point to the user's brand DS via `references/verification-deck-spec.md` §8 fail-mapping.

### Marketplace grader

`evals.json` + `trigger_evals.json` are read by Anthropic's skill-eval grader at marketplace submission. They verify a thin slice of Layer 1 (file_contains / regex_in_file / transcript_contains). Not the optimization loop — a downstream contract.

### Dev-time tooling

```bash
bash tests/audit_skill.sh         # DRY + reachability audit (no network)
bash tests/smoke_unilever.sh      # Phase 1 end-to-end smoke (live)
bash tests/test_integration.sh    # 3-brand Phase 1 integration (live)
bash tests/run_trigger_evals.sh   # static keyword scan of trigger_evals.json
```

## File layout

```
deckify/
├── SKILL.md                              # The contract (Phase 0–6 + hard rules)
├── README.md                             # This file
├── scripts/                              # All cross-platform Python (no bash on runtime path)
│   ├── setup.py                          # Phase 0: dependency check + install guide
│   ├── init_workspace.py                 # Phase 1 entry: per-run OS-tempdir workspace
│   ├── fetch_sitemap.py                  # 1a: home page + sitemap + nav-links + JSON-LD
│   ├── fetch_pages.py                    # 1c: batch-fetch chosen URLs (DOM + screenshot + probe)
│   ├── enumerate_assets.py               # 1d: aggregate probes → raw-assets.json
│   ├── embed_logo.py                     # 1f: download + quality-gate + base64-embed logo
│   └── persist_brand_source.py           # 6a: copy durable artifacts → decks/<brand>/source/
├── references/
│   ├── ds-template.md                    # English DS template (brand placeholders + engineering DNA)
│   ├── ds-template.zh.md                 # Chinese sister template (CJK fallback chain, etc.)
│   ├── decision-questions.md             # Phase 2 interactive Q&A checklist (host-neutral)
│   ├── verification-deck-spec.md         # Phase 4 contract + §8 fail-mapping table
│   └── llm-prompts/
│       ├── discover-pages.md             # 1b: how to pick subpages
│       └── synthesize-brand.md           # 1e: how to pick logo / palette / mood from raw assets
├── evals/                                # See evals/README.md for full architecture
│   ├── README.md                         # Layer 1 / Layer 2 / marketplace grader explained
│   ├── hard_checks.py                    # 10 deterministic checks (Layer 1 + Layer 2)
│   ├── rubric.json                       # 6 visual judge dimensions + 5 disqualifiers
│   ├── build_report.py                   # Per-brand scoreboard aggregation
│   ├── run_phase_a.py                    # Layer 1 multi-brand panel orchestrator
│   ├── evals.json                        # Marketplace grader: 4 declarative cases
│   └── trigger_evals.json                # Marketplace grader: 22 routing samples
└── tests/                                # Dev-time only — bash OK here, never on runtime path
    ├── audit_skill.sh                    # DRY + reachability audit
    ├── smoke_unilever.sh                 # Phase 1 end-to-end smoke
    ├── test_integration.sh               # 3-brand Phase 1 integration
    └── run_trigger_evals.sh              # Static keyword scan
```

## Philosophy

The skill separates **brand-variable** (per-brand recon: philosophy, colours, type, logo, aesthetic mood) from **engineering DNA** (per-deck invariants: fit contract, single-absorber rule, three-layer overflow safety net, logo-as-symbol pattern, mobile catch-alls, 12 px floor, the 40-item pre-ship checklist). One adapts; the other never does.

Layer 1 + Layer 2 use the same hard checks + visual rubric, but optimize different things. Layer 1 makes the skill better across brands; Layer 2 makes one user's deck pass once. Same tools, opposite debugging direction. See `evals/README.md` for the full picture.

## Contributing

If a new brand surfaces a class of bug the skill doesn't catch:
1. Add a hard check to `evals/hard_checks.py` that detects the bad output deterministically.
2. Trace the bug upstream to the rule that should have prevented it — usually `references/ds-template.md` (or `.zh.md`), occasionally `references/llm-prompts/synthesize-brand.md`. Fix THERE.
3. Regenerate the offending brand's DS + deck from the updated template, re-run `python3 evals/run_phase_a.py` across the full panel, confirm the fix doesn't regress other brands.
4. Sanity-check `bash tests/audit_skill.sh` before pushing.

This is the Layer 1 loop. The skill is supposed to get better with every brand we add, not patched ad-hoc.
