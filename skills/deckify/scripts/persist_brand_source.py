#!/usr/bin/env python3
"""persist_brand_source.py — copy durable Phase 1/2 artifacts out of the
transient workspace into the user's home deckify directory.

Phase 1 produces a temp workspace under the OS tempdir (/var/folders/.../T/
deckify-<slug>-<rand>/ on macOS, %TEMP%\\deckify-... on Windows). When the
OS sweeps that dir, we don't want to lose:
  - brand.json       (LLM-synthesised brand profile + chosen logo id)
  - decisions.json   (Phase 2 user choices: language, palette, fonts, etc.)
  - pages.txt        (LLM-picked subpage list — the recon scope)
  - assets/          (quality-gated logo files: .svg / .png / .embed.html / .dataurl)

These are durable artifacts: they encode judgment + user input that's
expensive to recreate. They go into ~/deckify/decks/<brand>/source/
alongside the DS markdown and the verification deck — that's the
"everything you'd need to regenerate the deck" bundle.

The big regenerable junk (recon/ DOM dumps, raw-assets.json, screenshots)
stays in the tempdir and is swept by the OS.

Usage:
    python3 persist_brand_source.py <workspace_dir> <brand-slug>

Outputs to: ~/deckify/decks/<brand-slug>/source/

Idempotent: re-running overwrites the source/ tree, so this is safe to call
at the end of any successful run.
"""
import shutil
import sys
from pathlib import Path


def user_deckify_root() -> Path:
    """Resolve the user-level home deckify directory: ~/deckify/.

    Why home-fixed instead of cwd-derived: every previous resolution
    strategy had a failure mode in practice.

      - script-location: walked up from this file's location and landed in
        the deckify skill source repo (because the skill is symlinked into
        Claude's plugin cache). Mars session reproduced this bug —
        artefacts wrote into the skill's own decks/ tree.
      - cwd-first: a user running deckify *from* the deckify source repo
        would still drop artefacts there. P&G and L'Oréal sessions
        reproduced this — even after the cwd-first fix, repo-internal
        cwds remained ambiguous.

    A fixed home-directory convention removes all ambiguity. Every
    deckify run for every brand from every cwd writes to the same
    predictable place: ~/deckify/decks/<brand>/. The skill source repo
    keeps its own decks/<brand>/ as a maintainer-only reference panel
    (Tiffany / Unilever / Stripe / Apple / Coca-Cola); user runs never
    touch it.

    The directory is created on first use. No environment variable
    override is supported (cf. previous failure modes — every escape
    hatch we've added has been the bug we're fixing later).
    """
    return Path.home() / "deckify"


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: persist_brand_source.py <workspace_dir> <brand-slug>", file=sys.stderr)
        return 2

    ws = Path(sys.argv[1]).resolve()
    slug = sys.argv[2].strip().lower()
    safe_slug = "".join(c if c.isalnum() or c in "-_" else "-" for c in slug)[:60] or "brand"

    if not ws.is_dir():
        print(f"workspace not found: {ws}", file=sys.stderr)
        return 1

    home_root = user_deckify_root()
    target = home_root / "decks" / safe_slug / "source"
    target.mkdir(parents=True, exist_ok=True)

    copied = []
    skipped = []

    # Single-file artifacts
    for name in ("brand.json", "decisions.json", "pages.txt"):
        src = ws / name
        if src.exists():
            shutil.copy2(src, target / name)
            copied.append(name)
        else:
            skipped.append(name)

    # assets/ tree
    assets_src = ws / "assets"
    assets_dst = target / "assets"
    if assets_src.is_dir():
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
        copied.append(f"assets/ ({sum(1 for _ in assets_dst.iterdir())} files)")
    else:
        skipped.append("assets/")

    print(f"persisted to: {target}")
    for c in copied:
        print(f"  + {c}")
    for s in skipped:
        print(f"  · {s} (not present in workspace)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
