# deckify — auto-eval summary

- Run dir: `2026-04-28T17-19-09-phase-a`
- Pass threshold (judge avg): **4.0**
- Samples: **5**

## Scoreboard

| Brand | Hard checks | Judge avg | Disqualifiers | Status |
|-------|------------:|----------:|---------------|--------|
| unilever | 10/10 | — | — | **PASS (hard-only — judge skipped)** |
| pg | 10/10 | — | — | **PASS (hard-only — judge skipped)** |
| stripe | 10/10 | — | — | **PASS (hard-only — judge skipped)** |
| apple | 9/10 | — | — | **WARN** |
| coca-cola | 9/10 | — | — | **WARN** |

## Per-sample drilldown

### unilever — PASS (hard-only — judge skipped)

- Detailed report: `per-sample/unilever.md`

### pg — PASS (hard-only — judge skipped)

- Detailed report: `per-sample/pg.md`

### stripe — PASS (hard-only — judge skipped)

- Detailed report: `per-sample/stripe.md`

### apple — WARN

- Detailed report: `per-sample/apple.md`

### coca-cola — WARN

- Detailed report: `per-sample/coca-cola.md`

---

## Self-closure

`repair_actions.json` lists every actionable fix. The skill author (or a follow-up agent) should resolve every blocker action before regenerating decks. Re-run `python3 evals/run_phase_a.py` (Layer 1) or `python3 evals/hard_checks.py` (Layer 2) to confirm green.
