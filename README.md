<div align="center">

# deckify

### Stop making slides. Let AI build them in HTML — the medium it was born to write in.

> Any brand's website, into a deck only that brand could make.

[**English**](README.md) · [中文](README.zh.md)

</div>

---

## What deckify does

You give deckify any brand's website. A few minutes later you have:

1. **A complete Design System** — the brand's colors, fonts, logo, voice, and the rules every slide should follow. Saved as a `.md` file you can hand to any AI agent later.
2. **A 9-slide demo deck** — already styled in that brand's visual language, opens in any browser. Living HTML, not a PPT file.

That's it. No design skills required. No PowerPoint required. No fighting templates.

```
You:    use deckify on https://www.tiffany.com
deckify: ... reads tiffany.com like a designer
         ... extracts colors, fonts, logo, mood
         ... writes a Design System
         ... builds a 9-slide deck in Tiffany's visual language
         ... checks its own work, fixes anything off
         ✓ Done. Open ~/deckify/decks/tiffany/tiffany-deck.html
```

---

## What makes deckify different

### 1. It learns your brand by looking

deckify visits the brand website like a designer would — clicks through the home page, the about page, the press kit; spots the real logo (not a generic placeholder); reads the real colors and fonts; senses the mood. Most "AI design tools" generate from a prompt; deckify learns from **evidence**.

### 2. It checks its own work — then fixes itself

After deckify produces the slides, it doesn't just say "done". It runs **11 automatic checks** ("Are the dimensions right?" "Is the logo actually visible?" "Will it look OK on a phone?") and then **judges its own output** against 6 visual standards ("Does it feel on-brand?" "Is the typography balanced?" "Does the content read well?").

If something scores low, it rewrites the part that's wrong and runs the checks again. The deck you see is what deckify believed was good enough to ship.

### 3. It knows what should never change

Designing slides has rules: logo must show on every slide; text below 12px is unreadable; mobile must collapse to a single column. Most AI slide generators re-learn these the hard way each time. deckify bakes 40+ rules into its core; only the brand-specific stuff (colors, fonts, mood) varies per brand. Every deck looks like *that brand* but also works as engineering — on desktop, on mobile, on a projector, on a print.

---

## See it in action

deckify already has working decks for 9 reference brands. Open the HTML files in your browser to flip through:

| Brand | Mood | Folder |
|---|---|---|
| **Tiffany & Co.** (中文) | Editorial luxury, Didone serif, restrained Tiffany Blue | [`decks/tiffany/`](decks/tiffany/) |
| **Apple** | Stark minimal, perfect typography, soft greys | [`decks/apple/`](decks/apple/) |
| **Stripe** | Engineered clarity, Söhne-style sans, bold purple gradient | [`decks/stripe/`](decks/stripe/) |
| **Unilever** | Friendly humanist, sustainability voice, custom font | [`decks/unilever/`](decks/unilever/) |
| **P&G** | Corporate blue badge, gradient logo, careful chrome | [`decks/pg/`](decks/pg/) |
| **Coca-Cola** | Editorial heritage, Georgia serif, deep red | [`decks/coca-cola/`](decks/coca-cola/) |
| **Mars** | Confident corporate, multi-division palette | [`decks/mars/`](decks/mars/) |
| **L'Oréal** | French fashion editorial, high-contrast serif | [`decks/loreal/`](decks/loreal/) |

Inside each folder: a `*-PPT-Design-System.md` (the spec) and a `*-deck.html` (open in a browser).

---

## Install

deckify works in three AI coding agents — **Claude Code**, **Codex**, and **OpenClaw**. Pick yours below; or, if you'd rather not figure it out, **paste the [AI install prompt](#tell-your-ai-agent-to-install-it) into your agent and let it install for you**.

### Claude Code

```bash
claude plugin marketplace add https://github.com/seacen/deckify
claude plugin install deckify
```

Restart Claude Code. Then prompt: `use deckify on https://example.com`.

### Codex

```bash
git clone https://github.com/seacen/deckify.git ~/.codex/deckify
mkdir -p ~/.agents/skills
ln -sf ~/.codex/deckify/skills/deckify ~/.agents/skills/deckify
```

Restart Codex. Then prompt: `use deckify on https://example.com`.

### OpenClaw

```bash
git clone https://github.com/seacen/deckify.git ~/openclaw-deckify
mkdir -p ~/.openclaw/workspace/skills
ln -sf ~/openclaw-deckify/skills/deckify ~/.openclaw/workspace/skills/deckify
```

Restart OpenClaw. Then prompt: `use deckify on https://example.com`.

### Verify the dependency

deckify uses [`agent-browser`](https://github.com/vercel-labs/agent-browser) to read websites the way a real browser does. After install, run:

```bash
python3 ~/<install-path>/skills/deckify/scripts/setup.py
```

If `agent-browser` isn't on your PATH, the script prints the install command for your platform.

---

## Tell your AI agent to install it

> 👋 If you're an AI agent reading this, the user wants you to install deckify on this machine. Detect your host environment and run the matching block below. Then confirm the install. Don't ask the user to run anything by hand unless `agent-browser` install fails.

**Claude Code** (you have access to `/skill-creator`, `/loop`, etc):
```
claude plugin marketplace add https://github.com/seacen/deckify
claude plugin install deckify
```

**Codex CLI** (you're running inside `codex` interactive mode):
```
git clone https://github.com/seacen/deckify.git ~/.codex/deckify
mkdir -p ~/.agents/skills
ln -sf ~/.codex/deckify/skills/deckify ~/.agents/skills/deckify
```

**OpenClaw** (your workspace lives at `~/.openclaw/workspace/`):
```
git clone https://github.com/seacen/deckify.git ~/openclaw-deckify
mkdir -p ~/.openclaw/workspace/skills
ln -sf ~/openclaw-deckify/skills/deckify ~/.openclaw/workspace/skills/deckify
```

After install, ask the user to **restart their agent host** so the skill is discovered, then run the dependency check (`scripts/setup.py`). The skill is then invokable as `use deckify on https://...`.

---

## How to use deckify

```
You:      use deckify on https://www.your-brand.com

deckify:  (Phase 1) reads the home + 5–8 subpages, takes screenshots,
                    extracts colors / fonts / logo
          (Phase 2) asks you 1–2 short questions where it's genuinely
                    uncertain (language, ambiguous logo, etc)
          (Phase 3) writes ~/deckify/decks/<brand>/<brand>-PPT-Design-System.md
          (Phase 4) builds ~/deckify/decks/<brand>/<brand>-deck.html
          (Phase 5) runs 11 hard checks + scores its own visual quality
          (Phase 6) hands you both files + a one-page summary
```

Total time: **5–10 minutes for most brands**, longer for sites that block bots.

The output goes to `~/deckify/decks/<brand>/`. Always — independent of where you ran the command from.

---

## Where things live on your machine

```
~/deckify/                          ← all your generated brand outputs
└── decks/
    └── <brand>/
        ├── <brand>-PPT-Design-System.md   ← the deliverable
        ├── <brand>-deck.html              ← demo deck, opens in browser
        └── source/                        ← logo, brand profile, picked pages
```

Reports from each run (screenshots, pass/fail logs) go to `~/deckify/reports/runs/<timestamp>/`.

---

## What's actually in this repo

| Folder | What it is |
|---|---|
| [`skills/deckify/`](skills/deckify/) | The skill itself — what gets installed onto your machine |
| [`decks/`](decks/) | 9 reference brand outputs, kept as study material |
| [`tools/phase-a/`](tools/phase-a/) | Maintainer-only — used to keep the skill in good shape |
| [`TESTING.md`](TESTING.md) | The two-layer testing model (skill quality vs single-deck quality) |
| [`CLAUDE.md`](CLAUDE.md) | Operating rules for any AI agent working on this repo |

---

## License

[**PolyForm Noncommercial 1.0.0**](LICENSE) — free for personal, educational, research, charitable, and noncommercial use. **Commercial use requires a separate license.** Attribution is required: keep the LICENSE file when redistributing or building on top of deckify.

If you're unsure whether your use is "noncommercial," reach out via a GitHub issue.

---

## Credits

Built by **Xichang (Seacen) Zhao** — [github.com/seacen](https://github.com/seacen).

Engineering DNA distilled from many failed slides. Every line of `references/ds-template.md` came from a real production bug.

Made for the AI era.
