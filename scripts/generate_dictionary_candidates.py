#!/usr/bin/env python3
"""Generate sense-aware English -> STRING candidate forms.

Open English WordNet provides lemma/POS/sense inventory, wordfreq provides
review priority, and CMUdict provides reference pronunciation.

This script never modifies dictionary/entries.jsonl and never accepts words.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

from normalize_ipa import normalize

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "dictionary-candidates.jsonl"
DEFAULT_META = ROOT / "build" / "dictionary-candidates.meta.json"

WORDFREQ_VERSION = "3.1.1"
WN_VERSION = "1.1.1"
OEWN_LEXICON = "oewn:2025"

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


def lexical_inventory() -> list[dict]:
    # Imported lazily so the core language test suite does not need lexical
    # generator dependencies.
    import wn
    from wordfreq import zipf_frequency

    wordnet = wn.Wordnet(OEWN_LEXICON)
    inventory: dict[tuple[str, str], dict] = {}

    for word in wordnet.words():
        lemma = word.lemma().lower()
        pos = word.pos

        # The first 50k target is single-word core vocabulary. Multiword
        # expressions are handled compositionally first.
        if not ASCII_WORD.fullmatch(lemma):
            continue

        key = (lemma, pos)
        record = inventory.setdefault(
            key,
            {
                "english": lemma,
                "part_of_speech": pos,
                "zipf_frequency": zipf_frequency(lemma, "en"),
                "wordnet_word_ids": [],
                "senses": [],
            },
        )
        record["wordnet_word_ids"].append(word.id)

        known_sense_ids = {sense["sense_id"] for sense in record["senses"]}
        for sense in word.senses():
            if sense.id in known_sense_ids:
                continue
            synset = sense.synset()
            definition = synset.definition() or ""
            record["senses"].append(
                {
                    "sense_id": sense.id,
                    "synset_id": synset.id,
                    "definition_en": definition,
                }
            )

    records = list(inventory.values())
    records.sort(
        key=lambda item: (
            -float(item["zipf_frequency"]),
            item["english"],
            item["part_of_speech"],
        )
    )
    return records


def build_candidates(limit: int, cmudict_path: Path) -> tuple[list[dict], dict]:
    pronunciations = load_cmudict(cmudict_path)
    accepted = accepted_headwords()
    generated_by_form: dict[str, list[dict]] = defaultdict(list)

    inventory = lexical_inventory()
    selected = inventory[:limit]

    output: list[dict] = []
    with_pronunciation = 0
    unsupported = 0
    accepted_collisions = 0
    candidate_collisions = 0

    for rank, lexical in enumerate(selected, start=1):
        english = lexical["english"]
        pos = lexical["part_of_speech"]
        variants = pronunciations.get(english, [])
        senses = lexical["senses"]

        row = {
            "frequency_rank": rank,
            "english": english,
            "part_of_speech": pos,
            "zipf_frequency": lexical["zipf_frequency"],
            "wordnet_word_ids": lexical["wordnet_word_ids"],
            "senses": senses,
            "sense_id": senses[0]["sense_id"] if senses else None,
            "definition_en": senses[0]["definition_en"] if senses else "",
            "source_status": "oewn-lemma-pos",
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
                    collisions.append(
                        {
                            "type": "accepted",
                            "english": existing,
                            "string": candidate,
                        }
                    )
                    accepted_collisions += 1

                for previous in generated_by_form.get(candidate, []):
                    collisions.append(
                        {
                            "type": "candidate",
                            "english": previous["english"],
                            "part_of_speech": previous["part_of_speech"],
                            "same_english_lemma": previous["english"] == english,
                            "string": candidate,
                        }
                    )
                    candidate_collisions += 1

                row.update(
                    {
                        "ipa_variants": ipa_variants,
                        "ipa_reference": "/" + ipa_reference + "/",
                        "mechanical_string": candidate,
                        "string_segments": segments,
                        "collisions": collisions,
                        "review_status": "candidate",
                    }
                )
                generated_by_form[candidate].append(
                    {"english": english, "part_of_speech": pos}
                )
                with_pronunciation += 1
            except ValueError as exc:
                row["review_status"] = "unsupported-pronunciation"
                row["error"] = str(exc)
                unsupported += 1

        output.append(row)

    meta = {
        "project": "STRING",
        "purpose": "sense-aware review candidates; never normative automatically",
        "requested_limit": limit,
        "available_single_word_lemma_pos_records": len(inventory),
        "generated_rows": len(output),
        "rows_with_string_candidate": with_pronunciation,
        "unsupported_pronunciation_rows": unsupported,
        "accepted_collision_events": accepted_collisions,
        "candidate_collision_events": candidate_collisions,
        "wordfreq_version": WORDFREQ_VERSION,
        "wn_version": WN_VERSION,
        "wordnet_lexicon": OEWN_LEXICON,
        "cmudict_repository": "cmusphinx/cmudict",
        "cmudict_commit": CMUDICT_COMMIT,
        "cmudict_url": CMUDICT_URL,
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
