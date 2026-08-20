#!/usr/bin/env python3
"""
verify_addendum_hash.py — standalone public verifier for pre-registration artifacts.

Self-contained. Depends ONLY on:
    jcs          (RFC-8785 JSON Canonicalization Scheme)
    hashlib       (Python standard library)
    json          (Python standard library)
    sys / argparse / os.path (Python standard library)

NO gradedlp imports. NO prereg_hash.py dependency.

Reproduces the canonical_row_hash semantics:
    1. Load the artifact JSON as native Python types.
    2. Remove the 'addendum_hash' top-level key from the payload.
    3. Canonicalize the remaining object with RFC-8785 JCS.
    4. Compute SHA-256 of the canonical bytes.
    5. Compare the digest against the declared addendum_hash.

The to_native() coercion in the original canonical_row_hash handles numpy scalars
(NaN/Inf rejection). For artifacts loaded from JSON, all values are already JSON-native
Python types (bool/int/float/str/None/list/dict), so to_native() is a no-op.
JCS canonicalize itself rejects NaN/Inf and non-finite floats, which matches the
original's fail-closed behavior on malformed data.
"""
import argparse
import json
import os
import sys

import hashlib
import jcs


EXCLUDED_KEY = "addendum_hash"


class VerificationError(Exception):
    """Raised when verification cannot proceed (fail-closed)."""


def load_artifact(path):
    """Load and parse a JSON artifact. Fails closed on malformed JSON."""
    if not os.path.isfile(path):
        raise VerificationError(f"Artifact not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        raise VerificationError(f"Cannot read file {path}: {e}") from e
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise VerificationError(f"Malformed JSON in {path}: {e}") from e


def verify_artifact(path):
    """
    Verify a single artifact's addendum_hash.

    Returns a dict:
        artifact:  the path given
        declared:  the declared addendum_hash (string)
        calculated:  the recomputed SHA-256 hex digest (string)
        status:  'MATCH' or 'MISMATCH'

    Fails closed (raises VerificationError) on:
        - malformed JSON
        - missing addendum_hash field
        - unsupported structure (not a JSON object)
    """
    artifact = load_artifact(path)

    if not isinstance(artifact, dict):
        raise VerificationError(
            f"Unsupported structure: root is {type(artifact).__name__}, expected JSON object"
        )

    if "addendum_hash" not in artifact:
        raise VerificationError(
            f"Missing 'addendum_hash' field in {path}"
        )

    declared = artifact["addendum_hash"]
    if not isinstance(declared, str):
        raise VerificationError(
            f"addendum_hash is not a string in {path} (got {type(declared).__name__})"
        )

    # Normalize the prefix: accept "sha256:<hex>" or bare "<hex>"
    declared_prefix_stripped = declared
    if declared.startswith("sha256:"):
        declared_prefix_stripped = declared[len("sha256:"):]

    # Build payload excluding addendum_hash (the excluded field)
    payload = {k: v for k, v in artifact.items() if k != EXCLUDED_KEY}

    # JCS canonicalization — RFC-8785.
    # jcs.canonicalize rejects NaN/Inf and other non-JSON types, matching
    # the original canonical_row_hash's fail-closed behavior.
    try:
        canonical_out = jcs.canonicalize(payload)
    except Exception as e:
        raise VerificationError(
            f"JCS canonicalization failed for {path}: {e}"
        ) from e

    # jcs.canonicalize returns bytes in practice; normalize defensively
    if isinstance(canonical_out, str):
        canonical_bytes = canonical_out.encode("utf-8")
    else:
        canonical_bytes = canonical_out

    calculated = hashlib.sha256(canonical_bytes).hexdigest()

    status = "MATCH" if calculated == declared_prefix_stripped else "MISMATCH"

    return {
        "artifact": path,
        "declared": declared,
        "calculated": calculated,
        "status": status,
    }


def format_result(result, verbose=False):
    """Format a verification result for human-readable output."""
    lines = []
    lines.append(f"artifact: {result['artifact']}")
    lines.append(f"declared hash:  {result['declared']}")
    lines.append(f"calculated hash: sha256:{result['calculated']}")
    if result["status"] == "MATCH":
        lines.append("status: MATCH")
    else:
        lines.append("status: MISMATCH")
    if verbose and result["status"] == "MISMATCH":
        declared_hex = result["declared"].split(":", 1)[-1]
        lines.append("")
        lines.append("  MISMATCH details:")
        lines.append(f"    declared:    {declared_hex}")
        lines.append(f"    calculated:  {result['calculated']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Standalone public verifier for pre-registration artifacts. "
            "Verifies the addendum_hash field of a published artifact using "
            "only jcs + hashlib + stdlib. No gradedlp dependency."
        )
    )
    parser.add_argument(
        "artifact",
        help="Path to a published pre-registration artifact JSON file",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show mismatch details",
    )
    args = parser.parse_args()

    try:
        result = verify_artifact(args.artifact)
    except VerificationError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    print(format_result(result, verbose=args.verbose))
    if result["status"] != "MATCH":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
