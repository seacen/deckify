#!/usr/bin/env python3
"""init_workspace.py — create a per-run scratch directory in the OS temp area.

Phase 1 of the deckify pipeline lives in a workspace dir that holds:
  - recon/                 (DOM dumps, screenshots, sitemap, jsonld)
  - raw-assets.json        (aggregated candidate pool)
  - brand.json             (LLM synthesised brand profile)
  - decisions.json         (user choices from Phase 2)
  - pages.txt              (LLM-picked subpage list)
  - assets/                (quality-gated logo files)

These files are LARGE (recon DOM dumps run hundreds of KB each, screenshots
even more) and REGENERABLE — re-running on the same URL rebuilds them. So
the workspace lives in the OS temp dir, not in the user's project, where:
  - macOS: $TMPDIR (/var/folders/.../T/)
  - Linux: /tmp
  - Windows: %TEMP% / %LOCALAPPDATA%/Temp

The OS will sweep these on its own schedule (macOS: 3 days idle; Linux:
typically reboot or systemd-tmpfiles; Windows: user-initiated). The skill
only persists the *durable* artifacts — the brand DS markdown, the
verification deck, and the canonical brand.json/decisions.json/assets —
into the user's repo via persist_brand_source.py at Phase 6.

Usage:
    python3 init_workspace.py [<brand-slug>]
prints (to stdout) the absolute path to the freshly-created workspace.
The caller (SKILL.md Phase 1 entrypoint) captures stdout into $WS.
"""
import sys
import tempfile
from pathlib import Path


def main() -> int:
    slug = sys.argv[1] if len(sys.argv) > 1 else "run"
    # Sanitise slug for filesystem
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in slug.lower())[:40] or "run"
    ws = Path(tempfile.mkdtemp(prefix=f"deckify-{safe}-"))
    (ws / "recon").mkdir()
    print(ws, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
