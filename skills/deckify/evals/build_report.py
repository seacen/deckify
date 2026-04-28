#!/usr/bin/env python3
"""
build_report.py — aggregate per-sample hard_checks + judge results into reports.

Inputs (from run.sh):
    argv[1]   = OUT_DIR (tests/reports/runs/<ts>/)
    argv[2]   = pass_threshold (numeric, e.g. "4")
    argv[3..] = sample tuples "brand|url|deck|ds"

Reads:
    OUT_DIR/per-sample/<brand>/hard_checks.json
    OUT_DIR/per-sample/<brand>/judge.json

Writes:
    OUT_DIR/summary.md             — overall scoreboard, all samples
    OUT_DIR/per-sample/<brand>.md  — per-brand detailed findings
    OUT_DIR/raw.jsonl              — one JSON object per sample (judge + hard)
    OUT_DIR/repair_actions.json    — concrete fix recommendations the runner can act on

Exits 0 on success regardless of pass/fail (the report itself is the output).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Disqualifier wiring — mirrors rubric.json
DISQUALIFIERS = [
    ("D1_logo_missing_or_placeholder",
     lambda hc, jd: (not _hc_passed(hc, "logo_renders"))
                    or (_judge_score(jd, "logo_present_and_branded") is not None
                        and _judge_score(jd, "logo_present_and_branded") <= 2)),
    ("D2_slide_dimensions_wrong",
     lambda hc, jd: not _hc_passed(hc, "slide_dimensions")),
    ("D3_console_errors",
     lambda hc, jd: bool(_hc_detail(hc, "slide_dimensions").get("console_errors"))),
    ("D4_mobile_horizontal_scroll",
     lambda hc, jd: not _hc_passed(hc, "mobile_collapse")),
    ("D5_ds_template_violated",
     lambda hc, jd: not _hc_passed(hc, "ds_has_engineering_dna")),
]


def _hc_iter(hc: dict):
    """Yield (check_id, passed, detail) for either schema:
       - flat: {check_id: {passed, evidence}}
       - list: {checks: [{id, passed, detail|evidence}]}"""
    if isinstance(hc, dict) and "checks" in hc:
        for c in hc.get("checks", []):
            yield c.get("id"), bool(c.get("passed")), (c.get("detail") or c.get("evidence") or {})
        return
    for cid, payload in (hc or {}).items():
        if isinstance(payload, dict):
            yield cid, bool(payload.get("passed")), (payload.get("evidence") or payload.get("detail") or {})


def _hc_passed(hc: dict, check_id: str) -> bool:
    for cid, passed, _ in _hc_iter(hc):
        if cid == check_id:
            return passed
    return False


def _hc_detail(hc: dict, check_id: str) -> dict:
    for cid, _, detail in _hc_iter(hc):
        if cid == check_id:
            return detail or {}
    return {}


def _judge_score(judge: dict, dim: str):
    if not judge or judge.get("skipped") or judge.get("error"):
        return None
    scores = (judge.get("scores") or {}).get("scores") or judge.get("scores") or {}
    val = scores.get(dim)
    if isinstance(val, (int, float)):
        return float(val)
    return None


def _judge_avg(judge: dict) -> float | None:
    if not judge or judge.get("skipped") or judge.get("error"):
        return None
    scores = (judge.get("scores") or {}).get("scores") or judge.get("scores") or {}
    nums = [v for v in scores.values() if isinstance(v, (int, float))]
    return round(sum(nums) / len(nums), 2) if nums else None


def status(passed: int, total: int, judge_avg: float | None, threshold: float, dq_hit: list[str]) -> str:
    if dq_hit:
        return "FAIL"
    if passed < total:
        return "WARN"
    if judge_avg is None:
        return "PASS (hard-only — judge skipped)"
    if judge_avg < threshold:
        return "WARN"
    return "PASS"


def repair_actions_for(brand: str, hc: dict, judge: dict) -> list[dict]:
    """Concrete, actionable fix recommendations the skill author can resolve."""
    actions: list[dict] = []
    if not _hc_passed(hc, "logo_renders"):
        d = _hc_detail(hc, "logo_renders")
        actions.append({
            "brand": brand,
            "kind": "logo_loader",
            "severity": "blocker",
            "evidence": d,
            "fix": "Re-run logo discovery: try Wikipedia logo URL, then /favicon.ico (PNG ok), then brand press kit. "
                   "If only PNG available, base64-embed via <image href> inside <symbol id='brand-wm'>. "
                   "If only typographic placeholder is possible, the deck FAILS — do not ship.",
        })
    if not _hc_passed(hc, "slide_dimensions"):
        d = _hc_detail(hc, "slide_dimensions")
        actions.append({
            "brand": brand,
            "kind": "slide_size",
            "severity": "blocker",
            "evidence": d,
            "fix": "Every .slide must measure 1280×720 ±2px (offsetWidth/offsetHeight). "
                   "Check that .deck transform-origin is top-left and that no slide overrides width/height. "
                   "Fixed canvas pattern: .slide { width:1280px; height:720px; padding:48px; box-sizing:border-box; }",
        })
    if not _hc_passed(hc, "fit_contract_intact"):
        actions.append({
            "brand": brand,
            "kind": "fit_contract",
            "severity": "blocker",
            "evidence": _hc_detail(hc, "fit_contract_intact"),
            "fix": "Each stacked .sc must declare exactly one flex:1 child as the absorber, with min-height:0 and overflow:hidden. "
                   "Re-emit DS §5 verbatim and check generator pipeline.",
        })
    if not _hc_passed(hc, "token_only_colors"):
        actions.append({
            "brand": brand,
            "kind": "ad_hoc_color",
            "severity": "warn",
            "evidence": _hc_detail(hc, "token_only_colors"),
            "fix": "Replace any ad-hoc hex literals with a CSS variable from :root. Allowed raw: #fff/#000 only.",
        })
    if not _hc_passed(hc, "no_emoji"):
        actions.append({
            "brand": brand,
            "kind": "emoji_leak",
            "severity": "warn",
            "evidence": _hc_detail(hc, "no_emoji"),
            "fix": "Strip pictographic emoji (U+1F300–U+1FAFF, U+1F600–U+1F6FF). Typographic marks (✓ ✗ → ★) are allowed.",
        })
    if not _hc_passed(hc, "mobile_collapse"):
        actions.append({
            "brand": brand,
            "kind": "mobile_overflow",
            "severity": "blocker",
            "evidence": _hc_detail(hc, "mobile_collapse"),
            "fix": "DS §10 mobile media query must catch ALL .g2/.g3/.flip-row/.tabs and force flex-direction:column. "
                   "Beware the inline-flex trap (display:inline-flex bypasses flex-direction:column).",
        })
    if not _hc_passed(hc, "ds_has_engineering_dna"):
        actions.append({
            "brand": brand,
            "kind": "ds_template_drift",
            "severity": "blocker",
            "evidence": _hc_detail(hc, "ds_has_engineering_dna"),
            "fix": "DS markdown is missing one of: 'Single-Slide Fit Contract', 'three-layer overflow safety net', "
                   "'inline-flex trap', 'this.classList.toggle', '12 px floor'. Re-emit using ds-template.md verbatim.",
        })
    # Judge-driven actions
    logo_score = _judge_score(judge, "logo_present_and_branded")
    if logo_score is not None and logo_score <= 2:
        actions.append({
            "brand": brand,
            "kind": "judge_logo_placeholder",
            "severity": "blocker",
            "evidence": {"logo_score": logo_score, "reasoning": (judge.get("scores") or {}).get("reasoning")},
            "fix": "Vision judge sees a placeholder, not a real logo. Re-run logo loader as above, then regenerate.",
        })
    visual = _judge_score(judge, "slide_visual_quality")
    if visual is not None and visual <= 3:
        actions.append({
            "brand": brand,
            "kind": "visual_quality",
            "severity": "warn",
            "evidence": {"visual_score": visual, "reasoning": (judge.get("scores") or {}).get("reasoning")},
            "fix": "Several slides feel awkward per the vision judge. Re-check breathing room, type hierarchy, and bottom-edge whitespace.",
        })
    return actions


def render_summary(out_dir: Path, threshold: float, samples: list[dict]) -> str:
    lines = []
    lines.append("# deckify — auto-eval summary")
    lines.append("")
    lines.append(f"- Run dir: `{out_dir.name}`")
    lines.append(f"- Pass threshold (judge avg): **{threshold}**")
    lines.append(f"- Samples: **{len(samples)}**")
    lines.append("")

    # Scoreboard
    lines.append("## Scoreboard")
    lines.append("")
    lines.append("| Brand | Hard checks | Judge avg | Disqualifiers | Status |")
    lines.append("|-------|------------:|----------:|---------------|--------|")
    for s in samples:
        hard_str = f"{s['hard_passed']}/{s['hard_total']}"
        judge_str = "—" if s['judge_avg'] is None else f"{s['judge_avg']}"
        dq_str = ", ".join(s['dq_hit']) if s['dq_hit'] else "—"
        lines.append(f"| {s['brand']} | {hard_str} | {judge_str} | {dq_str} | **{s['status']}** |")
    lines.append("")

    # Aggregate failure modes
    failure_kinds: dict[str, list[str]] = {}
    for s in samples:
        for a in s['actions']:
            failure_kinds.setdefault(a['kind'], []).append(s['brand'])
    if failure_kinds:
        lines.append("## Failure modes (cross-sample)")
        lines.append("")
        for kind, brands in sorted(failure_kinds.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"- **{kind}** — affects: {', '.join(sorted(set(brands)))}")
        lines.append("")

    # Per-sample drilldown
    lines.append("## Per-sample drilldown")
    lines.append("")
    for s in samples:
        lines.append(f"### {s['brand']} — {s['status']}")
        lines.append("")
        lines.append(f"- Detailed report: `per-sample/{s['brand']}.md`")
        if s['actions']:
            lines.append("- Top fixes:")
            for a in s['actions'][:3]:
                lines.append(f"  - **[{a['severity']}] {a['kind']}** — {a['fix'][:160]}")
        lines.append("")

    # Self-closure note
    lines.append("---")
    lines.append("")
    lines.append("## Self-closure")
    lines.append("")
    lines.append("`repair_actions.json` lists every actionable fix. The skill author (or a follow-up agent) "
                 "should resolve every blocker action before regenerating decks. Re-run `eval/run.sh` to confirm green.")
    return "\n".join(lines) + "\n"


def render_per_sample(s: dict, hc: dict, judge: dict) -> str:
    lines = []
    lines.append(f"# {s['brand']} — auto-eval detail")
    lines.append("")
    lines.append(f"- Status: **{s['status']}**")
    lines.append(f"- Hard checks: {s['hard_passed']}/{s['hard_total']}")
    lines.append(f"- Judge avg: {s['judge_avg']}")
    lines.append(f"- Disqualifiers hit: {', '.join(s['dq_hit']) if s['dq_hit'] else 'none'}")
    lines.append("")
    lines.append("## Hard checks")
    lines.append("")
    lines.append("| ID | Passed | Notes |")
    lines.append("|----|:------:|-------|")
    for cid, passed, detail in _hc_iter(hc):
        mark = "✓" if passed else "✗"
        notes = json.dumps(detail, ensure_ascii=False)
        notes = notes if len(notes) < 240 else notes[:237] + "..."
        lines.append(f"| {cid} | {mark} | `{notes}` |")
    lines.append("")

    lines.append("## Vision judge")
    lines.append("")
    if not judge or judge.get("skipped"):
        lines.append(f"_skipped: {judge.get('reason') if judge else 'no result'}_")
    elif judge.get("error"):
        lines.append(f"_error: {judge.get('error')}_")
        if judge.get("raw"):
            lines.append("```")
            lines.append(judge["raw"][:600])
            lines.append("```")
    else:
        scores = (judge.get("scores") or {}).get("scores") or judge.get("scores") or {}
        lines.append("| Dimension | Score |")
        lines.append("|-----------|------:|")
        for k, v in scores.items():
            lines.append(f"| {k} | {v} |")
        reasoning = (judge.get("scores") or {}).get("reasoning")
        if reasoning:
            lines.append("")
            lines.append(f"**Reasoning:** {reasoning}")
        flags = (judge.get("scores") or {}).get("regression_flags")
        if flags:
            lines.append("")
            lines.append("**Regression flags:**")
            for f in flags:
                lines.append(f"- {f}")
    lines.append("")

    lines.append("## Repair actions")
    lines.append("")
    if not s['actions']:
        lines.append("_None — clean run._")
    else:
        for a in s['actions']:
            lines.append(f"### [{a['severity']}] {a['kind']}")
            lines.append("")
            lines.append(f"**Fix:** {a['fix']}")
            lines.append("")
            ev = json.dumps(a['evidence'], ensure_ascii=False, indent=2)
            if len(ev) > 1200:
                ev = ev[:1200] + "..."
            lines.append("**Evidence:**")
            lines.append("```json")
            lines.append(ev)
            lines.append("```")
            lines.append("")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 4:
        print("usage: build_report.py <out_dir> <pass_threshold> <brand|url|deck|ds>...", file=sys.stderr)
        sys.exit(2)

    out_dir = Path(sys.argv[1])
    threshold = float(sys.argv[2])
    sample_specs = sys.argv[3:]

    samples = []
    raw_lines = []
    repair_payload = []

    for spec in sample_specs:
        brand, url, deck, ds = spec.split("|", 3)
        sample_dir = out_dir / "per-sample" / brand
        hc_path = sample_dir / "hard_checks.json"
        judge_path = sample_dir / "judge.json"

        hc = json.loads(hc_path.read_text()) if hc_path.exists() else {}
        judge = json.loads(judge_path.read_text()) if judge_path.exists() else {"skipped": True, "reason": "no judge.json"}

        check_rows = list(_hc_iter(hc))
        hard_total = len(check_rows)
        hard_passed = sum(1 for _, passed, _ in check_rows if passed)

        dq_hit = [name for name, predicate in DISQUALIFIERS if predicate(hc, judge)]
        actions = repair_actions_for(brand, hc, judge)
        judge_avg = _judge_avg(judge)

        s = {
            "brand": brand,
            "url": url,
            "hard_passed": hard_passed,
            "hard_total": hard_total,
            "judge_avg": judge_avg,
            "dq_hit": dq_hit,
            "actions": actions,
            "status": status(hard_passed, hard_total, judge_avg, threshold, dq_hit),
        }
        samples.append(s)

        # per-sample markdown
        (out_dir / "per-sample" / f"{brand}.md").write_text(render_per_sample(s, hc, judge), encoding="utf-8")

        # raw jsonl
        raw_lines.append(json.dumps({
            "brand": brand,
            "url": url,
            "deck": deck,
            "ds": ds,
            "hard_checks": hc,
            "judge": judge,
            "status": s["status"],
            "dq_hit": dq_hit,
        }, ensure_ascii=False))

        # repair actions
        repair_payload.extend(actions)

    (out_dir / "summary.md").write_text(render_summary(out_dir, threshold, samples), encoding="utf-8")
    (out_dir / "raw.jsonl").write_text("\n".join(raw_lines) + "\n", encoding="utf-8")
    (out_dir / "repair_actions.json").write_text(json.dumps(repair_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print scoreboard for the runner
    print()
    print("=" * 60)
    print(" AUTO-EVAL SCOREBOARD")
    print("=" * 60)
    for s in samples:
        ja = "—" if s['judge_avg'] is None else f"{s['judge_avg']:.2f}"
        dq = f"  DQ: {','.join(s['dq_hit'])}" if s['dq_hit'] else ""
        print(f"  {s['brand']:<10} hard={s['hard_passed']}/{s['hard_total']}  judge={ja:>5}  status={s['status']}{dq}")
    print("=" * 60)
    print(f"  Repair actions: {len(repair_payload)} (see repair_actions.json)")
    print("=" * 60)


if __name__ == "__main__":
    main()
