# Verifying the OP-MC economic contract anchor

`genesis_manifest.json` in this directory pins:

    "economic_contract_sha256": "fd83492aeba03aacb821e852249d0d2a42dd27970d9b4689c700bdeccb43e15a"

That hash is **not** the hash of a JSON contract file. It is the SHA-256 of the
**OP-MC-ECON v1.1 amendment text** — the amendment that closed the B2 fee-split
verification against the base economic contract (OP-MC-PREMATURITY.3C). Those exact
bytes are published here as `econ_amendment_v1_1.txt`.

## Verify

    sha256sum econ_amendment_v1_1.txt

Expected:

    fd83492aeba03aacb821e852249d0d2a42dd27970d9b4689c700bdeccb43e15a  econ_amendment_v1_1.txt

That value must equal `/economic_contract_sha256` in `genesis_manifest.json`.

## Convention

The hash is over the **raw file bytes**. There is no canonicalization step — no JCS,
no key sorting, no whitespace normalization. Two properties of the file are
load-bearing and easy to destroy by accident:

- **No trailing newline.** The file ends at the final `.` of the last line. Adding a
  trailing newline yields `edbb0ac5…` and will not match. Many editors append one on
  save; do not re-save this file before hashing it.
- **Trailing whitespace is significant.** Eight of the twenty lines end in a space.
  Any "strip trailing whitespace" pass changes the hash.

The file is UTF-8 and contains two non-ASCII characters (`§`, U+00A7, on lines 2 and
19). Transcoding to another encoding changes the bytes and therefore the hash.

For reference, the file is 1267 bytes and contains 19 newline characters (20 lines,
the last unterminated).

## Provenance

The amendment text originates as a fenced block in
`OP-MC-PREMATURITY_3E_FEE_SPLIT_VERIFICATION.md` §7, whose own SHA-256
(`9056ED34C3E2EBEB5356B43AFBE8520F066DA70A39527C224B6C0FEEF10E9639`) is certified in
the dependency table of `OP-MC-PREMATURITY_3H_FINAL_GENESIS_REHEARSAL.md`. The same
`fd83492a…` value is bound independently by three frozen artifacts: this genesis
manifest, the cohort contract v1.1
(`/dependencies/economic_contract/amendment_sha256`), and the acceptance standard v1
(`/provenance/economic_contract_v1_1/sha256`).
