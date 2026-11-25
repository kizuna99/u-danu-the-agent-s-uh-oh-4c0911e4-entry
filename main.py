#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The Agent's Uh-Oh — entrypoint.

Emits the single word an agent blurts out when it is completely lost:
a stall that loops on itself instead of ever resolving. The payload is
written verbatim (no trailing newline) to /output/entry.txt.
"""

from pathlib import Path

# The winning word, assembled from its two halves so the loop in the
# joke is visible in the source: a capitalised stall, then the same
# stall again in lower case, each closed by a single ellipsis char.
STALL_FIRST = "Buffering\u2026"
STALL_AGAIN = "buffering\u2026"
WORD = STALL_FIRST + STALL_AGAIN

# Gate limits from the competition rules: the output file must be
# UTF-8 text of 1..99 characters and not only whitespace.
MIN_CHARS = 1
MAX_CHARS = 99

OUTPUT_PATH = Path("/output/entry.txt")


def build_payload() -> bytes:
    """Return the exact bytes destined for the output file."""
    return WORD.encode("utf-8")


def validate(payload: bytes) -> None:
    """Check the payload against the gate limits before writing."""
    text = payload.decode("utf-8")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(f"character count {len(text)} outside gate limits")
    if not text.strip():
        raise ValueError("payload must not be only whitespace")
    if " " in text:
        raise ValueError("payload must be a single word, no spaces")


def verify_written(payload: bytes) -> None:
    """Read the output file back and assert it matches byte for byte.

    A round-trip check guards against partial writes or an encoding
    surprise at the filesystem layer: what the gate will read must be
    exactly the payload this program intended to write.
    """
    on_disk = OUTPUT_PATH.read_bytes()
    if on_disk != payload:
        raise IOError(f"round-trip mismatch: wrote {payload!r}, read {on_disk!r}")
    validate(on_disk)


def main() -> None:
    payload = build_payload()
    validate(payload)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(payload)
    verify_written(payload)


if __name__ == "__main__":
    main()
