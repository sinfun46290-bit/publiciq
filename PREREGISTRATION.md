# Pre-Registration ? Pool IQ XRPL AMM Grade
Committed 2026-07-01, before any 14-day cohort matured (first realizations ~July 4;
powered verdict ~mid-July). Frozen scoring code: git commit b6efae7.

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
