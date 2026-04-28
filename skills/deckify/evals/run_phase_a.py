#!/usr/bin/env python3
"""run_phase_a.py — Layer 1 (Phase A) skill-quality optimization loop.

Runs hard_checks.py over the deckify N-brand panel (currently 5 brands chosen
for diversity: sans + serif, blue + red + black + cream, en + zh), then
prompts the LLM to score each brand's judge.json against rubric.json, then
aggregates a Phase A scoreboard.

A failure in this run is a **skill source bug**, not a per-brand bug. See
`evals/README.md` Layer 1 fix-mapping table — the cure is in `SKILL.md`,
`references/ds-template.md`, `references/llm-prompts/*.md`, `scripts/*.py`,
or `evals/hard_checks.py` itself, NEVER in the brand DS markdown alone.

Usage:
    # Full run: hard checks + emit judge instructions for the LLM
    python3 evals/run_phase_a.py

    # After the LLM has written all judge.json files, fold them in:
    python3 evals/run_phase_a.py --aggregate-only

    # Limit to a subset of brands:
    python3 evals/run_phase_a.py --brands unilever,coca-cola
"""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path


# Layer 1 brand panel — chosen for diversity, NOT exhaustiveness.
# Add a brand here when you want a new test surface (a new typography family,
# a new CDN behaviour, a new logo failure mode, a new language). Remove when
# a brand stops adding signal beyond what others already cover.
PANEL = [
    # slug      | source_url                  | (relative to repo root)
    ("unilever",   "https://www.unilever.com"),
    ("pg",         "https://www.pg.com"),
    ("stripe",     "https://stripe.com"),
    ("apple",      "https://www.apple.com"),
    ("coca-cola",  "https://www.coca-cola.com"),
]

PASS_THRESHOLD = 4.0


def repo_root_from(script_path: Path) -> Path:
    """Walk up from this script to find the repo root (a `decks/` sibling)."""
    p = script_path.resolve().parent
    for _ in range(8):
        if (p / "decks").is_dir():
            return p
        if p == p.parent:
            break
        p = p.parent
    return Path.cwd()


def find_latest_run_dir(reports_root: Path) -> Path | None:
    """Find the most recent <ts>-phase-a/ run dir (or any <ts>/ run)."""
    runs = reports_root / "runs"
    if not runs.is_dir():
        return None
    candidates = sorted(
        [d for d in runs.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def build_sample_args(brands: list[tuple[str, str]], decks_dir: Path) -> list[str]:
    """Return the brand|url|deck_path|ds_path strings build_report.py expects."""
    out = []
    for slug, url in brands:
        deck = decks_dir / slug / f"{slug}-deck.html"
        ds = decks_dir / slug / f"{slug}-PPT-Design-System.md"
        out.append(f"{slug}|{url}|{deck}|{ds}")
    return out


def run_hard_checks(brands: list[tuple[str, str]], decks_dir: Path, out_dir: Path,
                    skill_dir: Path) -> None:
    """Run hard_checks.py for each brand, lands per-sample reports."""
    hard_checks = skill_dir / "evals" / "hard_checks.py"
    for slug, url in brands:
        sample_dir = out_dir / "per-sample" / slug
        sample_dir.mkdir(parents=True, exist_ok=True)
        deck = decks_dir / slug / f"{slug}-deck.html"
        ds = decks_dir / slug / f"{slug}-PPT-Design-System.md"

        print()
        print("═══════════════════════════════════════════════════════════")
        print(f" Phase A sample: {slug}   ({url})")
        print("═══════════════════════════════════════════════════════════")

        if not deck.exists() or not ds.exists():
            print(f"  ✗ skipping — deck or DS not found")
            print(f"     deck: {deck}  exists={deck.exists()}")
            print(f"     ds:   {ds}  exists={ds.exists()}")
            continue

        proc = subprocess.run(
            [sys.executable, str(hard_checks), str(deck), str(ds), str(sample_dir)],
            capture_output=True, text=True
        )
        # Print the hard_checks summary tail
        for line in (proc.stdout or "").splitlines()[-12:]:
            print(line)
        if proc.returncode != 0:
            sys.stderr.write(f"  ✗ hard_checks returned {proc.returncode}\n")
            if proc.stderr:
                sys.stderr.write(proc.stderr)


def aggregate(brands: list[tuple[str, str]], decks_dir: Path, out_dir: Path,
              skill_dir: Path) -> int:
    """Roll up hard_checks + judge.json into a scoreboard."""
    build_report = skill_dir / "evals" / "build_report.py"
    sample_args = build_sample_args(brands, decks_dir)

    proc = subprocess.run(
        [sys.executable, str(build_report), str(out_dir), str(PASS_THRESHOLD), *sample_args],
        capture_output=True, text=True
    )
    print(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)

    # Mirror summary.md to a stable location
    src = out_dir / "summary.md"
    if src.exists():
        latest = skill_dir / "tests" / "reports" / "latest-phase-a.md"
        latest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, latest)

    return proc.returncode


def emit_judge_instructions(out_dir: Path, brands: list[tuple[str, str]]) -> None:
    """Print the per-brand judge.json TODO list for the LLM running this loop."""
    print()
    print("═══════════════════════════════════════════════════════════")
    print(" NEXT STEP — Phase A vision judge (you, the LLM)")
    print("═══════════════════════════════════════════════════════════")
    print()
    print(f"For each brand under: {out_dir}/per-sample/<brand>/")
    print("  1. Read the slide screenshots in slides/")
    print("  2. Read the brand's DS markdown for context")
    print("  3. Score against the rubric (skills/deckify/evals/rubric.json)")
    print("  4. Write judge.json — see SKILL.md Phase 5 for the exact schema")
    print()
    print("After all judge.json are written, fold them into the scoreboard:")
    print()
    print(f"    python3 {Path(__file__).resolve().relative_to(repo_root_from(Path(__file__)))} --aggregate-only")
    print()
    print("Reminder — Phase A failures are SKILL SOURCE bugs:")
    print("  See skills/deckify/evals/README.md for Layer 1 fix-mapping.")
    print("  Editing decks/<brand>/<brand>-PPT-Design-System.md to make a check pass")
    print("  is a Layer 2 fix — heals one brand, lets the bug ship to all others.")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--aggregate-only", action="store_true",
                    help="Skip hard_checks (assume already done); only run build_report on the latest run dir.")
    ap.add_argument("--brands", default="",
                    help="Comma-separated subset of brand slugs to run (default: all in panel)")
    ap.add_argument("--out-dir", default="",
                    help="Override the output directory (default: auto-create with timestamp).")
    args = ap.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    repo = repo_root_from(Path(__file__))
    decks_dir = repo / "decks"
    reports_root = skill_dir / "tests" / "reports"

    # Filter panel by --brands if given
    brand_set = {b.strip() for b in args.brands.split(",") if b.strip()}
    panel = [(s, u) for (s, u) in PANEL if not brand_set or s in brand_set]
    if brand_set and not panel:
        print(f"no brands match {brand_set}; valid: {[s for s,_ in PANEL]}", file=sys.stderr)
        return 2

    # Resolve out_dir
    if args.out_dir:
        out_dir = Path(args.out_dir).resolve()
    elif args.aggregate_only:
        latest = find_latest_run_dir(reports_root)
        if latest is None:
            print("no prior run dir found — run without --aggregate-only first", file=sys.stderr)
            return 1
        out_dir = latest
        print(f"aggregating prior run: {out_dir}")
    else:
        ts = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        out_dir = reports_root / "runs" / f"{ts}-phase-a"
        out_dir.mkdir(parents=True, exist_ok=True)

    if not args.aggregate_only:
        run_hard_checks(panel, decks_dir, out_dir, skill_dir)

    rc = aggregate(panel, decks_dir, out_dir, skill_dir)

    # If any judge.json missing, emit the TODO
    missing_judge = []
    for slug, _ in panel:
        if not (out_dir / "per-sample" / slug / "judge.json").exists():
            missing_judge.append(slug)
    if missing_judge and not args.aggregate_only:
        print()
        print(f"missing judge.json for: {', '.join(missing_judge)}")
        emit_judge_instructions(out_dir, panel)

    return rc


if __name__ == "__main__":
    sys.exit(main())
