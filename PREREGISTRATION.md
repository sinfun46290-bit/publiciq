# Pre-Registration ? Pool IQ XRPL AMM Grade
Committed 2026-07-01, before any 14-day cohort matured (first realizations ~July 4;
powered verdict ~mid-July). Frozen scoring code: git commit b6efae7.

## Publication provenance (2026-07-17)
This repository was created 2026-07-06 (commit `8243833`) and was **not pushed to any
remote until 2026-07-17**. The 2026-07-13 and 2026-07-14 amendments below were authored on
their stated dates in the private canonical repository (verifiable in that repo's history)
and are **first published here on 2026-07-17**, together with the 2026-07-17 EXCLUDE
addendum. Every amendment predates any powered verdict (earliest mid-August 2026 — the gate
decides, not the calendar). This public copy is a sanitized rendering of the private
canonical under a documented redaction discipline: internal module names and absolute local
file paths are removed and footnoted; the meaning and all hashes are preserved.

## Hypothesis
The tiered GBM/IL-penalized pool scores carry cross-sectional predictive power for
realized 14-day net LP return on the high-volume speculative XRPL AMM tail.

## Primary metric
cross_sectional_IC (Spearman rank IC of predicted vs realized net, per date).

## Pre-registered pass contract (A-AND-B dual gate)
- PROMOTION_Z        = 2.0    (one-sided; leg passes iff HAC t >= 2.0)
- Leg A: overlapping cross-sectional IC, Newey-West HAC, lag L = 14
- Leg B: non-overlapping phase sweep, MIN_RESOLVED_PHASES = 10 of 14
- Quorum: MIN_POOLS_PER_DATE = 12 ; MIN_PHASE_FRAC = 1.00
- Verdict = leg A AND leg B. Anything short of both -> HOLD (underpowered) or FAIL.
- Universe scope: high-volume speculative XRPL AMM tail (top-vol fetch, vol >= 100 XRP);
  deep stable pools (RLUSD, USDC, CRYPTO) intentionally excluded as non-trap liquidity.

## Commitment
I will read the verdict strictly per the above. I will not tune thresholds, the
universe, or the scoring after observing realized outcomes. Deviations, if any, will
be logged as post-hoc and reported as such.

## Clarification 2026-07-13 — Evidence-integrity anchor (does NOT alter the frozen gate)
This documents the meaning of an existing manifest field. It is not a change to the
hypothesis, primary metric, pass contract, thresholds, or universe above — commit
b6efae7 stays frozen. Since the first grade manifest (2026-07-06), every run has
recorded two hashes of the graded inputs: `source_sha256` (SHA-256 of the raw
`pool_iq_snapshots.db` input bytes) and `sha256` (SHA-256 of the backup-API snapshot
copy). The pre-registered audit anchor — the hash a verdict cites to fix which inputs
it graded — is and always was `source_sha256`, because it is a pure function of the
input bytes and is identical on any machine. The snapshot-file `sha256` is a
within-platform convenience checksum only (the backup API re-serializes pages, so it
is platform-local) and is not a cross-environment identifier. See the transition note
in VERDICT_PROTOCOL.md for the 2026-07-14 laptop→box collection-host move.

## Addendum 2026-07-17 (pre-verdict) — EXCLUDE cohorts are included in the frozen v5 cross-sectional IC
Recorded before any powered verdict exists (earliest mid-August 2026). It changes nothing
frozen: hypothesis, primary metric, pass contract, thresholds, universe, and commit
`b6efae7` are all untouched. It documents a property of the frozen contract, found while
building the public `/xrpl` board, and fixes its handling in advance of a verdict.

### The finding
As of `source_sha256` `7b95e0f7…` (2026-07-17), 13 of 376 graded cohorts (7 resolved,
6 pending) carry `exp_net_*` predictions in `pool_grades` while their entry-snapshot tier
was `EXCLUDE` — i.e. the screener issued no verdict for them. `EXCLUDE` fires when
`exch_xrp < MIN_TRUST_EXCH` (1e-6): near-zero-price / near-zero-volume pools the screener
declines to grade. The frozen grader (`pooliq_grade.py`) reads `pool_grades` verbatim, so
these 13 cohorts are included in the pre-registered cross-sectional IC the gate reads.

### Ruling (no change to the frozen contract)
- v5 is NOT modified. The gate fires on the verbatim grader output; the board publishes
  that as the contract number. Dropping EXCLUDE after seeing outcomes would itself be a
  post-hoc deviation, so we do not do it.
- A verdict-only IC (the 13 EXCLUDE cohorts dropped → 363 rows / 142 resolved) is
  published alongside, labeled diagnostic / non-contract, for transparency only.

### Measured magnitude and direction (as of `source_sha256` `7b95e0f7…`; n = 8 qualifying dates, MIN_POOLS_PER_DATE = 12)
| Quantity | Verbatim (contract, 149 resolved) | Verdict-only (diagnostic, 142) | Δ |
|---|---|---|---|
| ΔIC[t1−t0] (gate leg) | −0.1355  [−0.258, −0.039] | −0.1590  [−0.294, −0.054] | −0.0235 |
| ΔIC[t1−heur] | −0.0879  [−0.193, −0.011] | −0.0935  [−0.183, −0.028] | −0.0057 |
| IC[t1] level | 0.7389 | 0.7373 | −0.0016 |
| IC[t0] level | 0.8744 | 0.8963 | +0.0219 |
| IC[heur] level | 0.8268 | 0.8308 | +0.0041 |

(BCa 95% CI, 20 000 resamples — descriptive; the gate itself promotes on Newey–West HAC
t ≥ 2.0 AND a non-overlapping phase sweep ≥ 10/14, not on this interval.)

Direction is mixed — stated as measured, not assumed:
- On the null's level IC (t0), including EXCLUDE biases IC toward zero (−0.022), as the
  "these are noise" reasoning predicts.
- On the contract number ΔIC[t1−t0], the effect runs the other way: verbatim −0.1355 vs
  clean −0.1590 — including EXCLUDE makes the model look less bad relative to the null,
  because it depresses t0 more than t1. Stated plainly: the number we are obligated to
  publish is marginally kinder to the model than the clean number.

All deltas sit inside the BCa intervals at n = 8. The contamination changes no sign and no
conclusion: ΔIC is negative on both legs both ways — t1 beats neither the null nor the
heuristic — and the read is underpowered.

### How publication is kept honest
The board exporter re-derives every cohort's entry tier from the frozen scorer and
hard-stops if it disagrees with the persisted verdict; it recomputes the IC from the frozen
grader on the same DB whose `source_sha256` the board cites, and hard-stops if that IC
disagrees with the grade run's recorded output for that `source_sha256`. The published
contract number cannot silently drift from the frozen pipeline the gate reads.
