#!/usr/bin/env bash
# run_trigger_evals.sh — static keyword scan of trigger queries vs SKILL.md description.
#
# This is a fast, network-free approximation of skill-creator's run_loop.py
# (which runs the live model). It scores each query by whether the
# description's trigger phrases would obviously route to this skill.
# Not a substitute for the full LLM eval, but catches obvious gaps.

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

python3 - "$SKILL_DIR/SKILL.md" "$SKILL_DIR/evals/trigger_evals.json" <<'PYEOF'
import json, sys, re, pathlib

skill_md, evals_path = sys.argv[1], sys.argv[2]
desc = pathlib.Path(skill_md).read_text(encoding="utf-8").lower()
evals = json.loads(pathlib.Path(evals_path).read_text(encoding="utf-8"))

# Cues the skill description establishes as triggers
positive_cues = [
    "design system", "url", "from this site", "from this brand",
    "extract a design system", "make slides like", "skin slides",
    "visual language", "html slide", "html slides", "slide deck",
    "brand site", "design-system",
]
# Cues for things the skill should NOT trigger on
negative_cues = [
    "fix the css", "convert this powerpoint", "extract colors from",
    "audit ... accessibility", "react 19", "fibonacci", "hex code for",
    "brand guideline document", "no website yet", "tailwind config",
]

def query_looks_in_scope(q):
    q = q.lower()
    has_url_or_brand = bool(re.search(r"(https?://|\.com|\.io|\.app|\.design)", q)) \
                       or any(c in q for c in ["unilever","stripe","apple","figma","notion","airbnb","linear","vercel","everlane","pg.com"])
    has_slide_intent = any(c in q for c in ["slide", "deck", "ppt", "design system", "html5"]) \
                       or any(c in q for c in ["设计系统", "幻灯片", "ppt"])
    return has_url_or_brand and has_slide_intent

pos_total = 0; pos_pass = 0
neg_total = 0; neg_pass = 0
misses = []

for e in evals:
    in_scope = query_looks_in_scope(e["query"])
    expected = e["should_trigger"]
    if expected:
        pos_total += 1
        if in_scope:
            pos_pass += 1
        else:
            misses.append(("FN", e["query"][:90]))
    else:
        neg_total += 1
        if not in_scope:
            neg_pass += 1
        else:
            misses.append(("FP", e["query"][:90]))

print(f"trigger eval (static keyword approximation):")
print(f"  positives:  {pos_pass}/{pos_total}  ({pos_pass*100//max(1,pos_total)}%)")
print(f"  negatives:  {neg_pass}/{neg_total}  ({neg_pass*100//max(1,neg_total)}%)")
if misses:
    print("  misses:")
    for kind, q in misses:
        print(f"    [{kind}] {q}")
ok = (pos_pass / max(1, pos_total) >= 0.8) and (neg_pass / max(1, neg_total) >= 0.8)
print("  result:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
PYEOF
