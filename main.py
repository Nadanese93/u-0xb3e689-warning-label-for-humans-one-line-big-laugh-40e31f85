#!/usr/bin/env python3
"""Write the warning-label entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3 stdlib only, no network, deterministic: the entry text is a
constant, so every run writes byte-identical output.
"""

import os
import sys

ENTRY = "WARNING: This human's 'I'll start Monday' has been running since 2019."

MAX_CHARS = 160
OUTPUT_FILENAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_MODE = 0o644


def validate(text):
    """Return an error string for an invalid entry, else None."""
    if not text or not text.strip():
        return "entry is empty or whitespace-only"
    if len(text) > MAX_CHARS:
        return "entry exceeds %d characters (%d)" % (MAX_CHARS, len(text))
    for ch in text:
        code = ord(ch)
        if ch in "\n\r\t" or code < 0x20 or code == 0x7F:
            return "entry contains a newline, tab or control character"
    return None


def main():
    error = validate(ENTRY)
    if error is not None:
        sys.exit("invalid entry: " + error)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    os.chmod(path, OUTPUT_MODE)


if __name__ == "__main__":
    main()
