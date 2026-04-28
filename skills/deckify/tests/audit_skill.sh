#!/usr/bin/env bash
# audit_skill.sh — DRY + reachability audit for this skill.
#
# Per Skillify step 8: walk the chain, surface dark/orphaned scripts, catch
# broken references, ensure every script and reference is reachable from
# SKILL.md.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_MD="$SKILL_DIR/SKILL.md"

fails=0

check() {
  local label="$1"; local condition="$2"
  if eval "$condition"; then
    echo "  ✓ $label"
  else
    echo "  ✗ $label"
    fails=$((fails + 1))
  fi
}

echo "auditing: $SKILL_DIR"
echo

echo "── SKILL.md basics ──"
check "SKILL.md exists" "[[ -f '$SKILL_MD' ]]"
check "SKILL.md has YAML frontmatter (name + description)" \
      "grep -q '^name: deckify' '$SKILL_MD' && grep -q '^description:' '$SKILL_MD'"
check "SKILL.md declares agent-browser dependency" \
      "grep -qi 'agent-browser' '$SKILL_MD'"
check "SKILL.md describes 4-phase pipeline" \
      "grep -q 'Phase 1' '$SKILL_MD' && grep -q 'Phase 2' '$SKILL_MD' && grep -q 'Phase 3' '$SKILL_MD' && grep -q 'Phase 4' '$SKILL_MD'"

echo
echo "── scripts reachability ──"
for s in setup.py init_workspace.py fetch_sitemap.py fetch_pages.py enumerate_assets.py embed_logo.py persist_brand_source.py; do
  check "scripts/$s exists" "[[ -f '$SKILL_DIR/scripts/$s' ]]"
  check "scripts/$s referenced from SKILL.md" "grep -q '$s' '$SKILL_MD'"
done

echo
echo "── references reachability ──"
for r in ds-template.md ds-template.zh.md decision-questions.md verification-deck-spec.md; do
  check "references/$r exists" "[[ -f '$SKILL_DIR/references/$r' ]]"
  check "references/$r referenced from SKILL.md" "grep -q '$r' '$SKILL_MD'"
done

echo
echo "── tests/evals presence ──"
check "tests/smoke_unilever.sh exists"      "[[ -f '$SKILL_DIR/tests/smoke_unilever.sh' ]]"
check "tests/test_integration.sh exists"    "[[ -f '$SKILL_DIR/tests/test_integration.sh' ]]"
check "evals/evals.json exists"             "[[ -f '$SKILL_DIR/evals/evals.json' ]]"
check "evals/trigger_evals.json exists"     "[[ -f '$SKILL_DIR/evals/trigger_evals.json' ]]"
check "evals/README.md exists"              "[[ -f '$SKILL_DIR/evals/README.md' ]]"
check "evals/run_phase_a.py exists"         "[[ -f '$SKILL_DIR/evals/run_phase_a.py' ]]"

echo
echo "── ENGINEERING-DNA bake-in (template invariants) ──"
TPL="$SKILL_DIR/references/ds-template.md"
check "template has Single-Slide Fit Contract"        "grep -q 'Single-Slide Fit Contract' '$TPL'"
check "template has three-layer overflow safety net"  "grep -q 'three-layer overflow safety net' '$TPL'"
check "template has single absorber rule"             "grep -q 'single flex:1 absorber' '$TPL'"
check "template has 602 px content budget"            "grep -q '602' '$TPL'"
check "template has inline-flex trap section"         "grep -q 'inline-flex trap' '$TPL'"
check "template has flip-card mobile fix"             "grep -q \"this.classList.toggle\" '$TPL'"
check "template has logo as SVG symbol with currentColor" \
      "grep -q '<symbol' '$TPL' && grep -q 'fill: currentColor' '$TPL'"
check "template has 12 px readability floor"          "grep -q '12 px' '$TPL'"
check "template has §13 Checklist"                    "grep -q '## 13. Checklist' '$TPL'"
check "template includes 375px mobile verification"   "grep -q '375' '$TPL'"

echo
echo "── no local-path leakage ──"
# Exclude binary caches, the audit script itself (self-references), and
# evals.json's negative-assertion strings ("not_contains: /Users/" is intentional).
LEAKS=$(grep -rn "Users/\|/opt/local\|/Library/Mobile\|iCloud" "$SKILL_DIR" 2>/dev/null \
        --include="*.md" --include="*.sh" --include="*.py" \
        --exclude-dir="__pycache__" \
        --exclude-dir="reports" \
        --exclude="audit_skill.sh" \
        | wc -l | tr -d ' ')
check "no hardcoded user-specific paths in shipped files" "[[ '$LEAKS' == '0' ]]"
if [[ "$LEAKS" != "0" ]]; then
  grep -rn "Users/\|/opt/local\|/Library/Mobile\|iCloud" "$SKILL_DIR" 2>/dev/null \
    --include="*.md" --include="*.sh" --include="*.py" \
    --exclude-dir="__pycache__" \
    --exclude-dir="reports" \
    --exclude="audit_skill.sh"
fi

echo
if [[ "$fails" == "0" ]]; then
  echo "audit passed."
  exit 0
else
  echo "audit FAILED — $fails check(s) failed."
  exit 1
fi
