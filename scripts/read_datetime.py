#!/usr/bin/env python3
"""Read canonical STRING date/time notation using the digit vocabulary."""

from __future__ import annotations

import argparse
import datetime as dt
import re

from read_number import read_number

DATE_RE = re.compile(r"^([0-9]{4})-([0-9]{2})-([0-9]{2})$")
TIME_RE = re.compile(r"^([0-9]{2}):([0-9]{2})(?::([0-9]{2}))?$")


def read_date(value: str) -> str:
    match = DATE_RE.fullmatch(value)
    if not match:
        raise ValueError("Expected YYYY-MM-DD")

    year, month, day = match.groups()
    dt.date(int(year), int(month), int(day))
    return "det " + ", ".join(read_number(group) for group in (year, month, day))


def read_time(value: str) -> str:
    match = TIME_RE.fullmatch(value)
    if not match:
        raise ValueError("Expected HH:MM or HH:MM:SS")

    hour, minute, second = match.groups()
    dt.time(int(hour), int(minute), int(second or "0"))

    groups = [hour, minute]
    if second is not None:
        groups.append(second)

    return "tam " + ", ".join(read_number(group) for group in groups)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="kind", required=True)

    date_parser = sub.add_parser("date")
    date_parser.add_argument("value")

    time_parser = sub.add_parser("time")
    time_parser.add_argument("value")

    args = parser.parse_args()
    try:
        if args.kind == "date":
            print(read_date(args.value))
        else:
            print(read_time(args.value))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
