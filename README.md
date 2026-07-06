# Pool IQ (XRPL) — Public Pre-Registration & Grade Ledger

**Published 2026-07-06.** This repository is the public, tamper-evident record of a
pre-registered forward test: does a frozen XRPL AMM risk scorer predict realized
14-day net LP return (fees − impermanent loss) out-of-sample?

The **frozen scoring contract** was committed **2026-07-01 as git commit `b6efae7`**
in a **separate private repository**. Only the pre-registration, the verdict-response
protocol, the methodology, and the dated data-audit exhibits are public here; the
scoring implementation is deliberately withheld. **The `b6efae7` hash is verifiable
on request** — it lets anyone confirm the scoring code existed and was frozen before
any outcome resolved, without the code itself being disclosed.

This public repository was created 2026-07-06 to publish the pre-registration; the
frozen scorer it references was committed earlier (2026-07-01) in the private working
repository, which is not public.

## Why this repo exists
To make the prediction impossible to back-fit. Everything here was committed while
the outcome was unknown: the first 14-day cohort closes ~mid-July 2026; the earliest
*powered* verdict is ~mid-August (pre-registered maturity deadline 2026-08-15). The
companion exhibit `exhibits/preflight_2026-07-02.txt` is a read-only data audit run
on 2026-07-02 showing **zero resolved rows** at that date — independent evidence the
predictions predated any resolution.

## The verdict — a frozen A-AND-B gate
The scorer "works" only if **both** legs of a pre-registered dual gate clear, on
cross-sectional IC (Spearman rank IC of predicted vs realized net, per date):

- **Leg A** — overlapping IC, Newey-West HAC (calendar-aware, lag L = 14), one-sided **t ≥ 2.0**.
- **Leg B** — non-overlapping phase sweep: promote in **all** of **≥ 10 of 14** resolvable phases.
- **Quorum** — **≥ 12 pools per date**; underpowered ⇒ **HOLD**, never pass or fail.
- **Verdict = Leg A AND Leg B.** Anything short ⇒ HOLD (underpowered) or FAIL.

(Constant values above are as fixed in `PREREGISTRATION.md`.)

## The freeze model
The scoring pipeline is frozen at `b6efae7`. It is never edited to make a result
pass: any change is a **new model version on a fresh forward clock**, never a
retro-fit. Verdict-day responses (pass / hold / fail) were fixed in advance in
`VERDICT_PROTOCOL.md`. Deviations, if any, are logged as post-hoc and dated.

## Contents
| File | What it is |
|---|---|
| `PREREGISTRATION.md` | The frozen hypothesis, primary metric, pass contract, quorum, universe (committed 2026-07-01). |
| `VERDICT_PROTOCOL.md` | Outcome A/B/C responses, decided before maturity. |
| `METHODOLOGY.md` | Plain-language methodology: tiers, grading, dead-pool imputation, the gate. |
| `exhibits/preflight_2026-07-02.txt` | Read-only data audit, 2026-07-02 — zero resolved rows (prediction-predates-resolution evidence). |
| `exhibits/verdict-inputs-*.json` | Input manifest: SHA-256 + per-table row counts of the graded database snapshot (no database contents published). |

*This is analytics, not financial advice. No capital executor is wired to any tier.*
