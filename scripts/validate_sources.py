#!/usr/bin/env python3
"""Validate canonical STRING sources used by builds and releases."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "phonology.json"
NUMBER_SPEC_PATH = ROOT / "spec" / "numbers.json"
DICTIONARY_PATH = ROOT / "dictionary" / "entries.jsonl"

VALID_STATUSES = {"proposed", "reviewed", "accepted", "deprecated"}
REQUIRED_ACCEPTED = {
    "id",
    "english",
    "sense_id",
    "part_of_speech",
    "definition_en",
    "ipa_reference",
    "string",
    "string_segments",
    "status",
    "source",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def segment(word: str, vowels: set[str], consonants: set[str]) -> str:
    parts: list[str] = []
    i = 0
    while i < len(word):
        if word[i] not in consonants:
            raise ValueError(f"expected consonant at position {i + 1}")
        if i + 1 == len(word):
            parts.append(word[i])
            i += 1
            break
        if word[i + 1] not in vowels:
            raise ValueError(f"expected vowel at position {i + 2}")
        parts.append(word[i : i + 2])
        i += 2
    return "-".join(parts)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"Cannot load {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(errors, f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return value


def load_entries(errors: list[str]) -> list[dict]:
    if not DICTIONARY_PATH.exists():
        fail(errors, f"Missing {DICTIONARY_PATH.relative_to(ROOT)}")
        return []

    entries: list[dict] = []
    for line_no, raw in enumerate(DICTIONARY_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, f"{DICTIONARY_PATH.relative_to(ROOT)}:{line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(item, dict):
            fail(errors, f"{DICTIONARY_PATH.relative_to(ROOT)}:{line_no}: row must be an object")
            continue
        item["_line"] = line_no
        entries.append(item)
    return entries


def validate_number_spec(
    errors: list[str],
    number_spec: dict,
    accepted_words: set[str],
    pattern: re.Pattern[str],
) -> None:
    digits = number_spec.get("digits")
    if not isinstance(digits, dict):
        fail(errors, "spec/numbers.json: digits must be an object")
        return

    expected_keys = {str(i) for i in range(10)}
    actual_keys = set(digits)
    if actual_keys != expected_keys:
        fail(
            errors,
            "spec/numbers.json: digits must contain exactly 0 through 9",
        )

    values = [str(value) for value in digits.values()]
    if len(values) != len(set(values)):
        fail(errors, "spec/numbers.json: spoken digit names must be unique")

    special = [
        number_spec.get("decimal_separator", {}).get("spoken"),
        number_spec.get("negative", {}).get("spoken"),
    ]

    for word in values + [str(v) for v in special if v]:
        if not pattern.fullmatch(word):
            fail(errors, f"spec/numbers.json: illegal spoken numeric form {word!r}")
        if word not in accepted_words:
            fail(
                errors,
                f"spec/numbers.json: spoken numeric form {word!r} is not an accepted dictionary headword",
            )


def main() -> int:
    errors: list[str] = []

    spec = load_json(SPEC_PATH, errors)
    number_spec = load_json(NUMBER_SPEC_PATH, errors)

    if not spec:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    orth = spec["orthography"]
    vowels = set(orth["vowels"])
    consonants = set(orth["consonants"])
    pattern = re.compile(orth["word_pattern"])

    entries = load_entries(errors)
    ids: list[str] = []
    accepted_words: list[str] = []

    for item in entries:
        line = item.pop("_line")
        label = f"{DICTIONARY_PATH.relative_to(ROOT)}:{line}"

        status = str(item.get("status", "")).lower()
        if status not in VALID_STATUSES:
            fail(errors, f"{label}: invalid status {status!r}")

        entry_id = item.get("id")
        if entry_id:
            ids.append(str(entry_id))
        else:
            fail(errors, f"{label}: missing id")

        word = item.get("string")
        if word is not None and word != "":
            if not isinstance(word, str):
                fail(errors, f"{label}: string must be text")
            else:
                if word != word.lower():
                    fail(errors, f"{label}: canonical STRING headwords must be lowercase: {word!r}")
                if not pattern.fullmatch(word):
                    fail(errors, f"{label}: illegal STRING form {word!r}; expected {orth['word_shape']}")
                else:
                    try:
                        expected_segments = segment(word, vowels, consonants)
                        if item.get("string_segments") != expected_segments:
                            fail(
                                errors,
                                f"{label}: string_segments must be {expected_segments!r} for {word!r}",
                            )
                    except ValueError as exc:
                        fail(errors, f"{label}: {word!r}: {exc}")

        if status == "accepted":
            missing = sorted(
                key for key in REQUIRED_ACCEPTED
                if key not in item or item[key] in (None, "", [])
            )
            if missing:
                fail(errors, f"{label}: accepted entry missing required fields: {', '.join(missing)}")
            if isinstance(word, str) and word:
                accepted_words.append(word)

    duplicate_ids = [value for value, count in Counter(ids).items() if count > 1]
    for value in duplicate_ids:
        fail(errors, f"Duplicate dictionary id: {value}")

    duplicate_accepted = [value for value, count in Counter(accepted_words).items() if count > 1]
    for value in duplicate_accepted:
        fail(
            errors,
            f"Duplicate accepted STRING form: {value}. Resolve the collision or model related senses in one entry.",
        )

    if number_spec:
        validate_number_spec(errors, number_spec, set(accepted_words), pattern)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    counts = Counter(str(e.get("status", "")).lower() for e in entries)
    print(
        "STRING source validation passed: "
        f"{len(entries)} dictionary entries; "
        f"{counts.get('accepted', 0)} accepted; "
        f"{counts.get('reviewed', 0)} reviewed; "
        f"{counts.get('proposed', 0)} proposed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
