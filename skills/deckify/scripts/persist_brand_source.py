#!/usr/bin/env python3
"""persist_brand_source.py — copy durable Phase 1/2 artifacts out of the
transient workspace into the user's repo.

Phase 1 produces a temp workspace under the OS tempdir (/var/folders/.../T/
deckify-<slug>-<rand>/ on macOS, %TEMP%\\deckify-... on Windows). When the
OS sweeps that dir, we don't want to lose:
  - brand.json       (LLM-synthesised brand profile + chosen logo id)
  - decisions.json   (Phase 2 user choices: language, palette, fonts, etc.)
  - pages.txt        (LLM-picked subpage list — the recon scope)
  - assets/          (quality-gated logo files: .svg / .png / .embed.html / .dataurl)

These are durable artifacts: they encode judgment + user input that's
expensive to recreate. They go into <repo>/decks/<brand>/source/ alongside
the DS markdown and the verification deck — that's the "everything you'd
need to regenerate the deck" bundle.

The big regenerable junk (recon/ DOM dumps, raw-assets.json, screenshots)
stays in the tempdir and is swept by the OS.

Usage:
    python3 persist_brand_source.py <workspace_dir> <brand-slug>

Outputs to: <repo-root>/decks/<brand-slug>/source/

Idempotent: re-running overwrites the source/ tree, so this is safe to call
at the end of any successful run.
"""
import shutil
import sys
from pathlib import Path


def find_repo_root() -> Path:
    """Find the user's project root, where decks/<brand-slug>/source/ should land.

    Search order matters here. The script is shipped inside the deckify skill,
    which gets symlinked / installed into Claude's plugin cache (e.g.
    ~/.claude/plugins/.../skills/deckify/scripts/) — so the script's *own
    location* points at the deckify repo, NOT at wherever the user is actually
    working. A user running deckify on their own brand from a totally
    different project would otherwise have their durable artefacts written
    into the deckify source repo. That's the Mars-session bug we are fixing.

    Resolution order:
      1. cwd, then walking up — this is the user's project. Highest priority.
      2. cwd unconditionally — even if no `decks/` exists yet, persist into
         a fresh `<cwd>/decks/<brand>/source/`. The user is here for a reason;
         create the directory rather than escaping to the skill's repo.
      3. (No script-location fallback. If cwd genuinely isn't a project, the
         user will see the artefacts in cwd and can move them manually — far
         better than silently dumping into Claude's plugin cache.)
    """
    cwd = Path.cwd().resolve()
    # Walk up from cwd looking for an existing decks/ — the strongest signal
    # that this is a deckify project.
    p = cwd
    for _ in range(8):
        if (p / "decks").is_dir():
            return p
        if p == p.parent:
            break
        p = p.parent
    # No decks/ ancestor found — persist into cwd anyway. This is the
    # "first run on a new project" case; mkdir will create decks/<brand>/.
    return cwd


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

    repo_root = find_repo_root()
    target = repo_root / "decks" / safe_slug / "source"
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
