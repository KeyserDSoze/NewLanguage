#!/usr/bin/env python3
"""Generate frequency-prioritized English -> STRING candidate forms.

This script does not modify dictionary/entries.jsonl and never accepts words.
It produces a review artifact.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

from wordfreq import top_n_list, zipf_frequency

from normalize_ipa import normalize

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "dictionary-candidates.jsonl"
DEFAULT_META = ROOT / "build" / "dictionary-candidates.meta.json"

CMUDICT_COMMIT = "0f8072f814306c5ee4fbf992ed853601b12c01f9"
CMUDICT_URL = (
    "https://raw.githubusercontent.com/cmusphinx/cmudict/"
    + CMUDICT_COMMIT
    + "/cmudict.dict"
)

ASCII_WORD = re.compile(r"^[a-z]+$")

ARPABET_CONSONANTS = {
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "F": "f",
    "G": "g",
    "HH": "h",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "P": "p",
    "R": "ɹ",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ",
}

ARPABET_VOWELS = {
    "AA": "ɑ",
    "AE": "æ",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "aɪ",
    "EH": "ɛ",
    "EY": "eɪ",
    "IH": "ɪ",
    "IY": "i",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "UH": "ʊ",
    "UW": "u",
}


def arpabet_phone_to_ipa(phone: str) -> str:
    stress = phone[-1] if phone and phone[-1].isdigit() else None
    base = phone[:-1] if stress is not None else phone

    if base == "AH":
        return "ə" if stress == "0" else "ʌ"
    if base == "ER":
        return "ɚ" if stress == "0" else "ɝ"
    if base in ARPABET_VOWELS:
        return ARPABET_VOWELS[base]
    if base in ARPABET_CONSONANTS:
        return ARPABET_CONSONANTS[base]
    raise ValueError(f"Unsupported ARPABET phone: {phone}")


def arpabet_to_ipa(phones: list[str]) -> str:
    return "".join(arpabet_phone_to_ipa(phone) for phone in phones)


def load_cmudict(path: Path) -> dict[str, list[list[str]]]:
    result: dict[str, list[list[str]]] = defaultdict(list)

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith(";;;"):
            continue

        parts = raw.split()
        if len(parts) < 2:
            continue

        word = re.sub(r"\(\d+\)$", "", parts[0].lower())
        if not ASCII_WORD.fullmatch(word):
            continue

        result[word].append(parts[1:])

    return dict(result)


def ensure_cmudict(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(CMUDICT_URL, timeout=60) as response:
        path.write_bytes(response.read())


def accepted_headwords() -> dict[str, list[str]]:
    path = ROOT / "dictionary" / "entries.jsonl"
    result: dict[str, list[str]] = defaultdict(list)

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        item = json.loads(raw)
        if item.get("status") == "accepted" and item.get("string"):
            result[item["string"]].append(item.get("english", item["id"]))

    return dict(result)


def frequency_words(limit: int) -> list[str]:
    # Ask for a larger surface-token pool because punctuation, contractions,
    # duplicates, and non-simple forms are filtered here.
    pool_size = max(limit * 3, limit + 25000)
    raw = top_n_list("en", pool_size, ascii_only=True)

    result: list[str] = []
    seen: set[str] = set()
    for value in raw:
        word = value.lower()
        if not ASCII_WORD.fullmatch(word):
            continue
        if word in seen:
            continue
        seen.add(word)
        result.append(word)
        if len(result) >= limit:
            break

    return result


def build_candidates(limit: int, cmudict_path: Path) -> tuple[list[dict], dict]:
    pronunciations = load_cmudict(cmudict_path)
    accepted = accepted_headwords()
    generated_by_form: dict[str, list[str]] = defaultdict(list)

    output: list[dict] = []
    with_pronunciation = 0
    unsupported = 0

    for rank, english in enumerate(frequency_words(limit), start=1):
        variants = pronunciations.get(english, [])
        row = {
            "frequency_rank": rank,
            "english_surface": english,
            "zipf_frequency": zipf_frequency(english, "en"),
            "source_status": "frequency-surface-form",
            "cmudict_pronunciations": variants,
            "ipa_variants": [],
            "ipa_reference": None,
            "mechanical_string": None,
            "string_segments": None,
            "collisions": [],
            "review_status": "needs-pronunciation",
        }

        if variants:
            try:
                ipa_variants = [arpabet_to_ipa(v) for v in variants]
                ipa_reference = ipa_variants[0]
                candidate, segments = normalize("/" + ipa_reference + "/")

                collisions = []
                for existing in accepted.get(candidate, []):
                    collisions.append({
                        "type": "accepted",
                        "english": existing,
                        "string": candidate,
                    })
                for previous in generated_by_form.get(candidate, []):
                    collisions.append({
                        "type": "candidate",
                        "english": previous,
                        "string": candidate,
                    })

                row.update({
                    "ipa_variants": ipa_variants,
                    "ipa_reference": "/" + ipa_reference + "/",
                    "mechanical_string": candidate,
                    "string_segments": segments,
                    "collisions": collisions,
                    "review_status": "candidate",
                })
                generated_by_form[candidate].append(english)
                with_pronunciation += 1
            except ValueError as exc:
                row["review_status"] = "unsupported-pronunciation"
                row["error"] = str(exc)
                unsupported += 1

        output.append(row)

    meta = {
        "project": "STRING",
        "purpose": "review candidates; never normative automatically",
        "requested_limit": limit,
        "generated_rows": len(output),
        "rows_with_string_candidate": with_pronunciation,
        "unsupported_pronunciation_rows": unsupported,
        "wordfreq_version": "3.2.0",
        "cmudict_repository": "cmusphinx/cmudict",
        "cmudict_commit": CMUDICT_COMMIT,
        "cmudict_url": CMUDICT_URL,
        "lexical_sense_source_planned": "Open English WordNet 2025",
    }
    return output, meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--meta", type=Path, default=DEFAULT_META)
    parser.add_argument(
        "--cmudict",
        type=Path,
        default=ROOT / "build" / "sources" / "cmudict.dict",
    )
    args = parser.parse_args()

    if args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    ensure_cmudict(args.cmudict)
    candidates, meta = build_candidates(args.limit, args.cmudict)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in candidates),
        encoding="utf-8",
    )
    args.meta.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
