# Pool IQ (XRPL) — Grade-Ledger Methodology

*Public methodology for the XRPL AMM board. Companion to the Poolwatch (EVM)
methodology; the two boards score different chains with different pipelines, so
the vocabularies below are XRPL-specific and do not carry over 1:1.*

Frozen scoring: git commit `b6efae7`. Pre-registered 2026-07-01
(`PREREGISTRATION.md`), before any 14-day cohort matured. Verdict-response rules
fixed in advance (`VERDICT_PROTOCOL.md`).

---

## What this board is

An XRPL AMM pool screener whose forward predictions are **graded against realized
outcomes on a public, frozen track record**. The board does not sort pools by
yield; it scores IL-trap / thin-exit / rug risk in the churny speculative tail,
then waits 14 days and records whether each call was right. Misses stay visible.

The claim under test (`PREREGISTRATION.md`): the tiered GBM/IL-penalized scores
carry cross-sectional predictive power for realized 14-day net LP return. That
claim is being decided **live, in public, before the outcome is known** — not
published after the fact conditional on winning. A public failure is a recorded
result, not a hidden one.

---

## Launch state (read this first)

The XRPL board goes public **before its verdict exists.** At launch:

- **Every grade is `pending`.** The first 14-day cohort closes ~mid-July 2026;
  the earliest *powered* verdict is ~mid-August (the pre-registered maturity
  deadline is 2026-08-15).
- A `pending` grade is a standing prediction with the forward clock still
  running. It is not a result and makes no claim of being correct.
- Nothing here is retro-fitted. The verdict-response protocol was committed
  2026-07-01; the decision to publish pending grades was committed 2026-07-06,
  both while the outcome was unknown.

---

## Scorer tiers (the risk call, per snapshot)

Each pool gets one tier per snapshot from a composite risk score, using frozen
tiered thresholds:

| Tier | Band | Meaning |
|---|---|---|
| `WATCH` | lowest risk band | Lowest risk. The only tier a (hypothetical, unbuilt) deployment gate would ever consider. |
| `CAUTION` | middle risk band | Elevated risk; not a clean pool. |
| `AVOID` | highest risk band | High trap / rug / thin-exit risk. |
| `EXCLUDE` | low confidence | **The scorer abstained** — see below. |

> Note for cross-board readers: the Poolwatch (EVM) board uses `OK` as its clean
> tier; this board uses `WATCH`. Same role, different label — the pipelines are
> independent by design.

### `EXCLUDE` = abstention, and abstention is never graded

`EXCLUDE` is emitted when the pool's price is too small to mark reliably — below a
pre-registered trust floor, near the ledger's smallest atomic price unit. This is
the scorer declining to issue a rankable verdict, not a risk verdict of its own.

**A verdict that was never issued cannot enter the grade ledger.** An `EXCLUDE`
row is not scored `correct`/`miss` and is not in the hit-rate denominator.
"Unknown" is never coerced to a real tier. This mirrors the Poolwatch void
principle; the *trigger* differs (there it is a missing price series, here it is
an untrustworthy price), the *rule* is the same: where the scorer abstained,
there is nothing to grade.

Any future change to the `EXCLUDE` criterion is a **methodology version bump** —
announced and versioned, never a silent edit — because it changes what is graded.

---

## Grade states (the forward outcome, per cohort)

Grading is realized-return forward validation, on the direction-neutral metric
**net LP return = fees − impermanent loss** over a 14-day window. Not total
return: a price-direction bet is not LP skill.

| State | What it means |
|---|---|
| `pending` | The 14-day window has not matured yet (the realized net return is undefined by *time*, not by death). A live prediction, not a result. |
| `correct` / `miss` | The window closed and realized net resolved; the tier's directional call is scored against it. |

### Dead pools are imputed and surfaced, not dropped

A pool alive at snapshot *t* but gone by *t+14* is **not** silently removed — that
is survivorship bias, and it flatters a screener by deleting its worst outcomes.
Instead the realized return is imputed from the pool's **last observed price**
(IL at last-seen + accrued fees). A pool that vanishes with no post-*t* data at
all is assigned an explicit, pre-registered dead-pool imputation and flagged. Both
are counted in the hit-rate denominator, and both are surfaced.

---

## The verdict (frozen A-AND-B gate)

The board-level "does the scorer work" question is decided by a pre-registered
dual gate on cross-sectional IC (Spearman rank IC of predicted vs realized net,
per date). Both legs must clear:

- **Leg A** — overlapping IC, Newey-West HAC (calendar-aware, lag L = 14),
  one-sided `t ≥ 2.0`.
- **Leg B** — non-overlapping phase sweep, promote in **all** of ≥ 10 of 14
  resolvable phases.
- **Quorum** — ≥ 12 pools per date; underpowered results read as `HOLD`, never
  as pass or fail.
- **Verdict = Leg A AND Leg B.** Anything short → `HOLD` (underpowered) or `FAIL`.

The headline test is not "the model beats naive APY." It is the model vs the
**cheap heuristic** (magnitude-matched): does the expected-IL integral beat a
hand-tuned squash a screener could compute for free? If it does not, that is
reported plainly.

**Universe scope (frozen):** high-volume speculative XRPL AMM tail (top-volume
fetch, vol ≥ 100 XRP). Deep stable pools (RLUSD, USDC, CRYPTO) are excluded on
purpose as non-trap liquidity — so this board's TVL is a deliberate slice and
does **not** reconcile to whole-DEX figures (that is a separate measurement
layer's job).

---

## What is and isn't claimed

- **Claimed:** for the pools shown, these were the frozen tiers, and these were
  the realized outcomes, graded by a rule fixed before the outcomes were known.
- **Not claimed:** that any pool is safe, that `WATCH` is an endorsement to
  supply liquidity, or that the verdict is in. Until ~mid-August the honest state
  is `HOLD`. This is analytics, not advice, and there is no executor wired to any
  tier.

*Frozen contract: `PREREGISTRATION.md`. Verdict-response rules:
`VERDICT_PROTOCOL.md`. Both committed before cohort maturity; deviations, if any,
are logged as post-hoc and dated.*
