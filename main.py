#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The Agent's Uh-Oh — writes one word an agent says when it is lost.

The word: Buffering…buffering…
A stall that loops: the agent is not thinking, not fixing, just spinning
forever — the honest one-word confession of a machine with no idea.
"""
import os

WORD = "Buffering…buffering…"


def main() -> None:
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
    except OSError:
        path = "entry.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(WORD)


if __name__ == "__main__":
    main()
