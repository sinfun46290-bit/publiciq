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

## CLARIFICATION 2026-07-13 (pre-verdict) — Audit anchor is source_sha256, and always was
This clarifies the meaning of evidence fields that have been recorded since the FIRST
grade manifest (`verdict-inputs-20260706_100154.json`). It changes no rule and no
frozen scoring content — PREREGISTRATION.md and commit b6efae7 (hypothesis, gate,
thresholds, universe) are untouched. This is not a mid-stream switch of anchor: both
hashes below have been present in every manifest from the first one; we are only
stating which of the two is environment-invariant.

Every grade manifest records TWO hashes of the graded inputs:
- `source_sha256` — SHA-256 of the raw source-DB bytes (`pool_iq_snapshots.db`). This
  is, and has always been, the portable audit anchor: a pure function of the input
  bytes, therefore identical on any machine. This is the value a verdict cites to fix
  exactly which inputs it graded.
- `sha256` — SHA-256 of the read-only *snapshot copy* the archiver writes via the
  SQLite backup API. This is a within-platform convenience checksum only. The backup
  API re-serializes pages, so the same input DB yields a different snapshot-file hash
  under Windows SQLite vs Linux SQLite. It is platform-local and was never the
  cross-environment anchor.

### Transition note — collection-host move (laptop → box)
- Through 2026-07-13, manifests were produced on the operator's laptop (Windows SQLite).[^1]
- From the 2026-07-14 cutover, manifests are produced on the box (Linux SQLite).
- The cutover re-seed copies the laptop's canonical DB to the box verbatim.
  `source_sha256` portability across the move was verified on identical input bytes:
  the same DB produced an identical `source_sha256` (a33568a2…) on both hosts, while
  the platform-local snapshot `sha256` differed exactly as described above (210cee35…
  on the box vs 7b85cff7… on the laptop for that same input) — confirming the anchor
  is invariant and the file-sha is not.
- The 7 historical laptop snapshot `.db` files (2026-07-06 … 2026-07-12) are retained
  unchanged. Their platform-local `sha256` remains reproducible only on the laptop;
  this is expected and non-blocking, because the anchor is `source_sha256`.

## NOTE 2026-07-14 (pre-verdict) — Autonomous daily grading on the box
As of 2026-07-14, XRPL grading runs automatically daily on the box; cohorts resolve
on 14-day maturity without operator intervention. This removes operator discretion
over resolution timing: through 2026-07-14 grading ran on the operator's laptop
(scheduled daily, but under direct operator control — manually re-runnable and
toggleable); the box runs it as autonomous infrastructure via the hardened
`pooliq_grade_run.sh` wrapper (preflight + read-only input archive + sha256 manifest
+ quiet nothing-to-grade branch), chained by `OnSuccess=` after the daily
snapshot+panel collection. No change to the frozen scorer (b6efae7), rule,
thresholds, or universe.

## CLARIFICATION 2026-07-17 (pre-verdict) — EXCLUDE cohorts sit inside the frozen v5 IC
Logged before any powered verdict exists (Outcome B / underpowered is the only observation
to date, which carries zero verdict information). This changes no rule and no frozen scoring
content — PREREGISTRATION.md and commit `b6efae7` (hypothesis, gate, thresholds, universe)
are untouched. It is the same kind of pre-verdict, timestamped disclosure as the 2026-07-06
publication amendment and the 2026-07-13 audit-anchor clarification above.

Building the public `/xrpl` board surfaced that 13 of 376 graded cohorts carry
`exp_net_*` predictions while their entry-snapshot tier was `EXCLUDE` — pools for which
the screener issued no verdict (`exch_xrp < 1e-6`). The frozen grader reads `pool_grades`
verbatim, so these cohorts are included in the pre-registered cross-sectional IC.

Ruling, fixed here while the outcome is unknown, on purpose:
- v5 is not modified. The gate fires on the verbatim grader output; that is the contract
  number the board publishes. A verdict-only IC (EXCLUDE dropped) is published beside it as
  diagnostic, non-contract. Re-defining the panel after seeing outcomes would be a
  violation of this clarification, not a new decision — the same discipline as the
  2026-07-06 amendment.
- The full analysis, measured magnitudes, and the (mixed, honestly stated) direction —
  including that the contract number is marginally kinder to the model than the clean
  number — are recorded in PREREGISTRATION.md → "Addendum 2026-07-17 (pre-verdict) —
  EXCLUDE cohorts are included in the frozen v5 cross-sectional IC."

Every delta is inside the intervals at the current n = 8 qualifying dates; the contamination
changes no sign and no conclusion. Disclosed now so that when a powered read becomes
possible (~mid-August), the record already shows it was known and the panel definition was
fixed in advance.

## CLARIFICATION 2026-07-18 (pre-verdict) — Deployment + first live-data observations
Logged the day after the public `/xrpl` board went live, before any powered verdict. Changes
no rule and no frozen content (commit `b6efae7` untouched); does NOT edit the 2026-07-17
disclosure. Records three things deployment surfaced: (1) the 2026-07-17 addendum is a dated
`source_sha256` snapshot (376 / 149 verbatim / ΔIC[t1−t0] −0.1355) while the live board
recomputes from current bytes (first live export: 391 / 162 verbatim / ΔIC[t1−t0] −0.1113) —
expected forward growth, not a revision; (2) all 13 EXCLUDE cohorts are one pool (Xoge) on 13
distinct dates, a live-computed count that cannot overstate; (3) the board's integrity
guarantees — export-time IC recompute with a hard-stop against the grade run's recorded ΔIC,
the entry-tier oracle, refresh only inside the grade chain, and staleness self-report. Full
detail in PREREGISTRATION.md -> "Addendum 2026-07-18 (pre-verdict) — Deployment + first
live-data observations."

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

[^1]: Internal module names and absolute local file paths were redacted here for privacy
(the module name "an earlier cohort grader"; and the laptop/box `source_db` paths in the
2026-07-13 transition note). This public copy is otherwise identical to the pre-registered
original committed in the private repository; the frozen scoring contract it references is
git commit `b6efae7` (hash verifiable on request).
