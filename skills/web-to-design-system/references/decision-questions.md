# Phase 2 — decision questions

The questions to walk through with the user via `AskUserQuestion` before you generate the DS. Goal: turn raw recon into committed decisions, prevent overfit, surface taste choices the data can't decide on its own.

**Bundle into 4–5 batched calls** to `AskUserQuestion` (max 4 questions per call, max 4 options per question). Don't ask one at a time — that's annoying.

## Round 0 — Language (ask FIRST)

This question runs before anything else, because it determines the language for the rest of the conversation AND the language the generated Design System is written in. Once selected, all subsequent rounds — and the output DS file — use that language.

**Question:** "What language should I use for the rest of this conversation, and the generated Design System?"

**Options (Chinese and English first; offer 4 total + the auto-Other):**

| Label | Value |
|---|---|
| 中文 (Simplified Chinese) | `zh-CN` |
| English | `en` |
| 日本語 (Japanese) | `ja` |
| Español (Spanish) | `es` |

If the user picks Other, take their free-text answer (any ISO language tag or natural-language name). The skill itself contains no other language-specific copy — Phase 3 generation produces the DS in the chosen language by translating the template's prose sections (philosophy paragraph, rules narration, anti-pattern callouts) at write time. The CSS, token names (`--navy`, `--blue`, etc.), code snippets, and structural section numbers stay invariant across languages.

**Important:** if the user has been writing to you in a particular language up to this point, default the recommended option to that language — but still ask explicitly so they can choose differently for the DS output (e.g., user types in Chinese but wants the DS in English for an international team).

## Round 1 — Mood & Aesthetic (the most-decisive call)

This drives the Design Philosophy paragraph in §1 of the generated DS. If you get this wrong, the whole DS reads wrong.

**Question:** "I read [Brand] as [hypothesis]. Confirm or redirect?"

**Options to offer (pick the 3–4 closest to your hypothesis):**

| Option | When to offer | Drives |
|---|---|---|
| Premium / editorial / typographically-led | Luxury, fashion, professional services, high-end consumer goods | Generous whitespace, type does the work, restrained color |
| Engineering-clean / grid-driven | SaaS, dev tools, B2B, fintech | Tighter grids, mono accents, copy-pastable code blocks, muted gray scales |
| Bold-colorful / consumer | Energy drinks, gaming, youth fashion, creator economy | High saturation, hero typography, illustrative shapes, whitespace as accent |
| Minimal-monochrome | Architecture, design studios, art galleries, certain luxury | Reductive palette, one accent, type-led, near-empty layouts |
| Playful-illustrated | Education, kids, creative tools | Hand-drawn elements, friendly type, off-grid composition |
| Technical-dense | Scientific publishing, engineering reference, dashboards | Information-rich, Tufte-influenced, charts foregrounded |

**Hint to the user:** include in the question the *evidence* you saw — "I saw a [color family] palette, [font kind] at large weights, generous whitespace on the homepage, [type of imagery]" — so they can correct your read with specifics, not vibes.

## Round 2 — Color anchors

**Question:** "Primary palette I extracted: [hex list, with role labels]. Which is the dominant accent vs the dark anchor? Anything to swap or add?"

Show the user **side-by-side**:
- Top 4 brand color candidates from `brand-recon.json` (with hex + frequency + source)
- Top 4 neutrals
- Any `:root` custom property the site exposes (often the brand's actual token system — strongest signal)

**Common decisions:**
- Which color → `--navy` (the primary brand dark, used as background on dark slides and ink on light slides). NOT necessarily literal navy — it's whatever the brand uses as anchor.
- Which color → `--blue` (the accent / CTA — the color used for links, buttons, focus states).
- Whether the homepage hero gradient is brand-permanent or campaign-only (often: campaign — don't bake it in).
- Semantic palette overrides? Some brands have a brand-specific "positive" green different from the system default.

**Pitfall:** brand sites often display TWO competing colors: the marketing accent (loud, used for hero CTAs) and the brand anchor (quiet, used in nav/footer/long-form). The anchor is usually right for slides. Confirm.

## Round 3 — Typography

**Question:** "Typography: I see [Family] as the primary on-page font. Use it as-is, substitute, or pair with a presentation-friendly fallback?"

**Options:**
- **Use brand font verbatim** — only if you've checked the font is licensable (Google Fonts URL, OFL/SIL hosted, or user owns a license). Many brand fonts are bespoke and slide audiences can't render them.
- **Use a close systems-friendly substitute** — e.g., brand uses a proprietary display font → DS uses an open equivalent like `Inter`, `Manrope`, `Barlow`, or `IBM Plex Sans`. Closest weight-spread match.
- **Use an OFL workhorse** — pick a high-quality open-license font that covers 100–900 weights + italic and has a strong CJK fallback. Reasonable defaults if the brand font is unavailable.
- **Pair brand display + system body** — if the brand font is great for headlines but poor for body (common with display fonts).

Always confirm CJK fallback if the user works in a CJK language — `PingFang SC`, `Noto Sans SC`, `Source Han Sans SC`, etc.

## Round 4 — Slide-type emphasis & special asks

**Question:** "Which slide types should this DS foreground for [Brand] decks?"

**Multi-select** — let the user pick 2–4. The DS still includes all 11 types; this just sets which appear first in §6 with worked examples.

| Brand archetype | Default emphasis |
|---|---|
| Premium / editorial | Type J (quote), Type C (narrative), Type F (image), Type A (cover) |
| Engineering / SaaS | Type E (data table), Type H (chart), Type G (interactive demo), Type B (two-col) |
| Consumer / bold | Type F (image), Type D (flip), Type J (quote), Type A (cover) |
| Pitch / fundraising | Type A (cover), Type J (quote), Type H (chart), Type K (timeline) |
| Internal report | Type E (table), Type H (chart), Type C (narrative), Type K (timeline) |

**Optional fourth question** if needed:
- Logo restrictions? ("Only use on white background" / "Min size 24px" / "Always pair with TM" — bake into §4)
- Border-radius preference? Most DS default to 3–4px; some brands want 0 (sharp) or 12+ (rounded).
- Any sections from §6 the brand explicitly does NOT want? (Some brands forbid charts, interactive demos, etc.)

## Anti-patterns when asking

- **Don't ask before doing recon.** The user shouldn't have to invent answers — show them what you found and let them validate.
- **Don't ask "what should the philosophy be?"** Open-ended questions get vague answers. Always offer 3–4 concrete options + Other.
- **Don't accept silence as approval.** If the user gave no notes on a question, treat it as "the recommended option is fine" — but say so explicitly in your Phase 4 summary, so they can flag if they meant something different.

## Save decisions

After all rounds, write a JSON snapshot to `$WS/decisions.json` capturing every committed answer. Phase 3 reads this file to fill template placeholders. The shape (keys only — values come from the recon + the user's answers, never from a hardcoded fixture):

```json
{
  "language":             "<ISO tag the user picked, e.g. zh-CN | en | ja | es | ...>",
  "brand_name":           "<as user named the brand>",
  "brand_slug":           "<lowercased kebab-case>",
  "mood":                 "<one of the archetypes from Round 1, or user's Other>",
  "philosophy_paragraph": "<the §1 mood paragraph in the chosen language>",
  "colors": {
    "navy":     "<hex from extraction + Round 2 confirmation>",
    "blue":     "<hex>",
    "surface":  "<hex>",
    "ink":      "<hex>",
    "mid":      "<hex>",
    "rule":     "<hex>",
    "tint":     "<hex>",
    "green":    "<hex>", "green_bg": "<hex>",
    "red":      "<hex>", "red_bg":   "<hex>",
    "warn":     "<hex>", "warn_bg":  "<hex>",
    "teal":     "<hex>", "teal_bg":  "<hex>"
  },
  "typography": {
    "primary_font":      "<family as agreed in Round 3>",
    "weight_range":      "<e.g. 300–900>",
    "italic_note":       "<e.g. ' + italic 300', or empty>",
    "fallback":          "<CJK or system-ui fallback family>",
    "fallback_use_case": "<e.g. 'Chinese', 'system fallback', or empty>"
  },
  "logo": {
    "local_path":   "<$WS/assets/logo.svg or .png — written by download_logo.sh>",
    "viewBox":      "<extracted from the saved SVG>",
    "height":       "<e.g. 19px>",
    "source_url":   "<where the file came from>",
    "restrictions": "<any brand-rule notes the user gave>"
  },
  "emphasis":          ["<two-to-four Type X identifiers from Round 4>"],
  "border_radius":     "<as decided>",
  "cover_background":  "<solid color OR a linear-gradient using only token-derived colors>",
  "flip_back_color":   "<one shade softer than --blue, for Type D back face>",
  "bespoke_examples":  "<one short paragraph with 2–3 hypothetical bespoke compositions for §1, all built from token colors only — no brand-specific hard-coded names from prior decks>"
}
```

**Critical:** the values in this file come from THIS session's recon + THIS session's user answers. Do NOT carry over hex values, font choices, or example phrasings from another brand's prior session. Every brand's `decisions.json` is its own snapshot.
