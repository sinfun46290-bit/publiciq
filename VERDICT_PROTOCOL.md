# Verdict-Day Protocol — Pool IQ XRPL
Written 2026-07-01, before cohort maturity. Decides my response to each outcome
in advance, so a marginal result can't be rationalized post-hoc.

## AMENDMENT 2026-07-06 (pre-verdict) — Publication decoupled from verdict
Logged BEFORE any powered verdict exists (at most a July 3 HOLD observed, which
carries zero verdict information). This is a deliberate, timestamped change to
the operational DISPLAY policy — NOT a change to PREREGISTRATION.md, which stays
frozen (hypothesis, gate, thresholds, universe, commit b6efae7 all unchanged).

Decision: the XRPL dashboard goes PUBLIC NOW, with grades shown as pending,
exactly as Poolwatch launched. Rationale: gating public display on a PASS is a
selection-bias mechanism — the public would only ever see the model if it won,
the same survivorship bug already fixed in an earlier cohort grader.[^1] A visible public FAIL
is not a failure of the product; the public, frozen, falsifiable track record —
misses included — IS the product.

This decision is made while the outcome is unknown, on purpose. If a future
version of me wants to re-enable auth after seeing a bad number, that is a
VIOLATION of this amendment, not a new decision. The line was drawn here, blind.

## Global Definitions
- Quorum / Powered: >=12 pools AND >=10 phases.
- Maturity Deadline: 2026-08-15 (cohort has full natural maturation + buffer;
  after this, persistent underpowered = Outcome C, insufficient-data failure).

## Outcome A — PASS (leg A AND leg B clear, Z>=2.0, quorum met)
- Record the verdict + git commit b6efae7 + the exact numbers.
- This unlocks downstream: begin the Sui gate. (Public display is NO LONGER
  gated here — see 2026-07-06 amendment; the dashboard is already public with
  pending grades.) NOT a signal to add capital or build the trading executor.
- Write the book's Verdict chapter with the real numbers.

## Outcome B — HOLD / UNDERPOWERED (quorum not yet met, or one leg only) [LIKELY FIRST]
- This is NOT failure and NOT a reason to touch the model.
- Let the cohort keep maturing; the daily grade re-evaluates automatically.
- Re-read only when quorum is genuinely met OR the Maturity Deadline is reached.
- Dashboard is already public with pending grades (see 2026-07-06 amendment); a
  HOLD changes nothing about display. Nothing else downstream (the Sui gate)
  unlocks yet.

## Outcome C — FAIL (quorum met but does not clear the gate, OR Maturity Deadline reached without quorum)
- Log it honestly as a negative result. This is data, not an error.
- Do NOT edit the frozen pipeline to make it pass. Ever.
- Any improvement = a NEW model (v2) on its own fresh forward clock.
- The failure is legitimate content for the book; report it plainly.
- The dashboard stays public through the failure. That is the entire point of
  the 2026-07-06 amendment: a public FAIL is the credential, not a thing to hide.

## Standing rule
I will not tune thresholds, universe, or scoring after seeing outcomes.
The frozen v1 result stands as what it was, whatever it is.

[^1]: One internal module name was redacted here ("an earlier cohort grader") for
privacy. This public copy is otherwise identical to the pre-registered original
committed in the private repository; the frozen scoring contract it references is
git commit `b6efae7` (hash verifiable on request).
