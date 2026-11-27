#!/usr/bin/env python3
"""Write the competition entry to the output directory.

The text lives in entry.txt beside this file; this program copies it to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt), byte for byte
identical on every run.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.txt"
MAX_CHARS = 1000


def load_text() -> str:
    """Return the entry text, normalised so every run emits the same bytes.

    Line endings are folded to \\n and trailing space is dropped, so a
    checkout that rewrote the source file cannot change the output.
    """
    raw = SOURCE.read_text(encoding="utf-8")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines).strip()


def main() -> int:
    text = load_text()

    # The gate: 1 to 1000 Unicode code points, not only whitespace. The
    # normalising strip above already rules out a whitespace-only text.
    if not 1 <= len(text) <= MAX_CHARS:
        print(f"entry text is {len(text)} code points", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    print(f"wrote {len(text)} code points to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
