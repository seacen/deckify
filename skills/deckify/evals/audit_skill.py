#!/usr/bin/env python3
"""audit_skill.py — DRY + reachability audit for the deckify skill.

Walks the chain, surfaces dark/orphaned scripts, catches broken references,
ensures every script and reference is reachable from SKILL.md, and confirms
the engineering-DNA invariants are baked into ds-template.md verbatim.

Cross-platform Python (no shell). Exit code 0 if all checks pass, 1 otherwise.

This is Layer 1 step 0 — `run_phase_a.py` invokes it before kicking off the
brand-panel hard checks. Failures here mean a structural / referential bug
in the skill source that you should fix before bothering to run brands.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"

# What we expect to find in skills/deckify/scripts/
RUNTIME_SCRIPTS = [
    "setup.py",
    "init_workspace.py",
    "fetch_sitemap.py",
    "fetch_pages.py",
    "enumerate_assets.py",
    "embed_logo.py",
    "persist_brand_source.py",
]

# What we expect to find in skills/deckify/references/
REFERENCES = [
    "ds-template.md",
    "ds-template.zh.md",
    "decision-questions.md",
    "verification-deck-spec.md",
]

# Layer 1 / Layer 2 eval files (must always be present)
EVAL_FILES = [
    "evals/evals.json",
    "evals/trigger_evals.json",
    "evals/README.md",
    "evals/run_phase_a.py",
    "evals/hard_checks.py",
    "evals/build_report.py",
    "evals/rubric.json",
    "evals/audit_skill.py",
]

# Engineering-DNA invariants that MUST be in references/ds-template.md verbatim.
# Each entry is (label, [substring(s) — ALL must be present]).
ENGINEERING_DNA = [
    ("Single-Slide Fit Contract",         ["Single-Slide Fit Contract"]),
    ("three-layer overflow safety net",   ["three-layer overflow safety net"]),
    ("single absorber rule",              ["single flex:1 absorber"]),
    ("602 px content budget",             ["602"]),
    ("inline-flex trap section",          ["inline-flex trap"]),
    ("flip-card mobile fix",              ["this.classList.toggle"]),
    ("logo as SVG symbol with currentColor", ["<symbol", "fill: currentColor"]),
    ("12 px readability floor",           ["12 px"]),
    ("§13 Checklist",                     ["## 13. Checklist"]),
    ("375px mobile verification",         ["375"]),
]


class Result:
    def __init__(self) -> None:
        self.fails = 0
        self.passes = 0

    def check(self, label: str, ok: bool, detail: str = "") -> None:
        if ok:
            print(f"  ✓ {label}")
            self.passes += 1
        else:
            suffix = f" — {detail}" if detail else ""
            print(f"  ✗ {label}{suffix}")
            self.fails += 1


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(n in text for n in needles)


def file_contains_any(path: Path, needles: list[str]) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return any(n in text for n in needles)


def audit_skill_md_basics(r: Result) -> None:
    print("── SKILL.md basics ──")
    skill_text = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.is_file() else ""
    r.check("SKILL.md exists", SKILL_MD.is_file())
    r.check(
        "SKILL.md has YAML frontmatter (name + description)",
        bool(re.search(r"^name:\s*deckify", skill_text, re.MULTILINE))
        and bool(re.search(r"^description:", skill_text, re.MULTILINE)),
    )
    r.check("SKILL.md declares agent-browser dependency", "agent-browser" in skill_text.lower())
    r.check(
        "SKILL.md describes Phase 1–6 pipeline",
        all(f"Phase {i}" in skill_text for i in range(1, 7)),
    )


def audit_scripts_reachability(r: Result) -> None:
    print()
    print("── scripts reachability ──")
    skill_text = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.is_file() else ""
    for s in RUNTIME_SCRIPTS:
        path = SKILL_DIR / "scripts" / s
        r.check(f"scripts/{s} exists", path.is_file())
        r.check(f"scripts/{s} referenced from SKILL.md", s in skill_text)


def audit_references_reachability(r: Result) -> None:
    print()
    print("── references reachability ──")
    skill_text = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.is_file() else ""
    for ref in REFERENCES:
        path = SKILL_DIR / "references" / ref
        r.check(f"references/{ref} exists", path.is_file())
        r.check(f"references/{ref} referenced from SKILL.md", ref in skill_text)


def audit_eval_files_present(r: Result) -> None:
    print()
    print("── evals presence ──")
    for rel in EVAL_FILES:
        path = SKILL_DIR / rel
        r.check(f"{rel} exists", path.is_file())


def audit_engineering_dna(r: Result) -> None:
    print()
    print("── ENGINEERING-DNA bake-in (template invariants) ──")
    tpl = SKILL_DIR / "references" / "ds-template.md"
    for label, needles in ENGINEERING_DNA:
        r.check(f"template has {label}", file_contains(tpl, needles))


def audit_no_path_leakage(r: Result) -> None:
    """Scan shipped files for hardcoded user-specific or platform-specific paths.

    Excluded: tests/reports/* (regenerable run output), __pycache__/, this
    audit script itself, and the legacy /Users/<name>/ patterns from prior
    failure-mapping examples in evals.json (those are intentionally negative-
    asserted).
    """
    print()
    print("── no local-path leakage ──")
    leak_patterns = [
        re.compile(r"/Users/[A-Za-z0-9_-]+/"),     # macOS home
        re.compile(r"C:\\\\Users\\\\"),             # Windows home
        re.compile(r"/opt/local/"),                 # MacPorts
        re.compile(r"/Library/Mobile/"),            # iCloud
        re.compile(r"\biCloud\b"),
    ]
    skip_dirs = {"reports", "__pycache__", ".git"}
    skip_files = {"audit_skill.py"}
    leaks: list[str] = []
    for path in SKILL_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".sh", ".py", ".json"}:
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.name in skip_files:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pat in leak_patterns:
                if pat.search(line):
                    leaks.append(f"{path.relative_to(SKILL_DIR)}:{line_no}: {line.strip()[:120]}")
                    break
    r.check("no hardcoded user-specific paths in shipped files", not leaks)
    if leaks:
        for leak in leaks[:10]:
            print(f"      {leak}")
        if len(leaks) > 10:
            print(f"      ... and {len(leaks) - 10} more")


def main() -> int:
    print(f"auditing: {SKILL_DIR}")
    print()
    r = Result()

    audit_skill_md_basics(r)
    audit_scripts_reachability(r)
    audit_references_reachability(r)
    audit_eval_files_present(r)
    audit_engineering_dna(r)
    audit_no_path_leakage(r)

    print()
    if r.fails == 0:
        print(f"audit passed ({r.passes} checks).")
        return 0
    else:
        print(f"audit FAILED — {r.fails} check(s) failed (passed: {r.passes}).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
