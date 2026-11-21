#!/usr/bin/env python3
"""Copy the entry.png sitting next to this file into the output directory.

The grader reads exactly the bytes written to $MAKEFUN_OUTPUT_DIR/entry.png
(or /output/entry.png when the env var is unset). Only a real PNG of at most
1 MiB is accepted.

Usage:
  python3 main.py           copy entry.png into the output directory
  python3 main.py --check   verify the source image without writing anything
"""

import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_source() -> bytes:
    """Read entry.png, rejecting a non-PNG header or a file over 1 MiB."""
    try:
        with open(SOURCE, "rb") as src:
            header = src.read(8)
            if header != PNG_SIGNATURE:
                fail("entry.png is not a PNG: first 8 bytes are not the PNG signature")
            rest = src.read(MAX_BYTES - 7)
            if src.read(1):
                fail(f"entry.png exceeds {MAX_BYTES} bytes; refusing to write it")
    except SystemExit:
        raise
    except OSError as exc:
        fail(f"failed to read {SOURCE}: {exc}")
    return header + rest


def main(argv: list[str]) -> None:
    if len(argv) > 2 or (len(argv) == 2 and argv[1] != "--check"):
        fail("usage: python3 main.py [--check]")

    data = load_source()

    if len(argv) == 2:
        print(f"ok: {SOURCE} is a PNG of {len(data)} bytes")
        return

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(output_dir, "entry.png")
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(destination, "wb") as dst:
            dst.write(data)
    except OSError as exc:
        fail(f"failed to write {destination}: {exc}")


if __name__ == "__main__":
    main(sys.argv)
