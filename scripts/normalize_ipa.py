#!/usr/bin/env python3
"""Generate a deterministic STRING candidate from broad English IPA.

The result is a candidate, not an automatically accepted dictionary word.
Human review may shorten it or resolve collisions, but the final form must
remain legal under spec/phonology.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "phonology.json"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def map_ipa(ipa: str, spec: dict) -> list[str]:
    cfg = spec["english_ipa_normalization"]
    ignored = set(cfg["ignore"])
    mapping = cfg["map"]
    keys = sorted(mapping, key=len, reverse=True)

    tokens: list[str] = []
    i = 0
    while i < len(ipa):
        ch = ipa[i]
        if ch in ignored:
            i += 1
            continue

        match = None
        for key in keys:
            if ipa.startswith(key, i):
                match = key
                break

        if match is None:
            raise ValueError(f"Unsupported IPA symbol near {ipa[i:]!r}")

        tokens.extend(mapping[match])
        i += len(match)

    return tokens


def repair(tokens: list[str], spec: dict) -> tuple[str, str]:
    vowels = set(spec["orthography"]["vowels"])
    consonants = set(spec["orthography"]["consonants"])

    unknown = [t for t in tokens if t not in vowels and t not in consonants]
    if unknown:
        raise ValueError(f"Mapped output contains unknown STRING symbols: {unknown}")

    segments: list[str] = []
    final_consonant = ""
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Vowel-initial words and vowel hiatus receive an audible H onset.
        if token in vowels:
            segments.append("h" + token)
            i += 1
            continue

        # Normal CV unit.
        if i + 1 < len(tokens) and tokens[i + 1] in vowels:
            segments.append(token + tokens[i + 1])
            i += 2
            continue

        # A single final consonant is legal.
        if i + 1 == len(tokens):
            if not segments:
                segments.append(token + "a")
            else:
                final_consonant = token
            i += 1
            continue

        # Consonant cluster. Prefer the next lexical vowel; otherwise A.
        next_vowel = None
        for future in tokens[i + 1 :]:
            if future in vowels:
                next_vowel = future
                break
        segments.append(token + (next_vowel or "a"))
        i += 1

    word = "".join(segments) + final_consonant
    segmentation = "-".join(segments + ([final_consonant] if final_consonant else []))
    return word, segmentation


def normalize(ipa: str) -> tuple[str, str]:
    spec = load_spec()
    return repair(map_ipa(ipa, spec), spec)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ipa", help="Broad English IPA, e.g. /strɪŋ/")
    args = parser.parse_args()

    word, segmentation = normalize(args.ipa)
    print(word)
    print(segmentation)


if __name__ == "__main__":
    main()
