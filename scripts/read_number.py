#!/usr/bin/env python3
"""Render canonical decimal notation into spoken STRING digit words."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "numbers.json"

NUMBER_RE = re.compile(r"^-?[0-9]+(?:\.[0-9]+)?$")


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def read_number(value: str) -> str:
    spec = load_spec()
    normalized = value.replace(",", "")

    if not NUMBER_RE.fullmatch(normalized):
        raise ValueError(
            "Expected canonical decimal notation: optional '-', digits, and optional '.' plus digits."
        )

    words: list[str] = []
    if normalized.startswith("-"):
        words.append(spec["negative"]["spoken"])
        normalized = normalized[1:]

    integer, dot, fraction = normalized.partition(".")
    words.extend(spec["digits"][digit] for digit in integer)

    if dot:
        words.append(spec["decimal_separator"]["spoken"])
        words.extend(spec["digits"][digit] for digit in fraction)

    return " ".join(words)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="Decimal number such as 2026, 007, or -3.14")
    args = parser.parse_args()

    try:
        print(read_number(args.number))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
