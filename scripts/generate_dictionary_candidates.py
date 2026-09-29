#!/usr/bin/env python3
"""Generate sense-aware English -> STRING candidate forms.

Open English WordNet provides lemma/sense inventory, wordfreq provides review
priority, and CMUdict provides reference pronunciation.

One candidate row represents one English lemma and can contain multiple parts
of speech and senses. Review may later split unrelated senses into distinct
STRING entries.

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
DEFAULT_COLLISIONS = ROOT / "build" / "dictionary-collisions.jsonl"
DEFAULT_PRONUNCIATION_REVIEW = ROOT / "build" / "dictionary-pronunciation-review.jsonl"

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


def accepted_index() -> tuple[dict[str, list[dict]], dict[str, list[dict]]]:
    path = ROOT / "dictionary" / "entries.jsonl"
    by_string: dict[str, list[dict]] = defaultdict(list)
    by_english: dict[str, list[dict]] = defaultdict(list)

    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        item = json.loads(raw)
        if item.get("status") != "accepted" or not item.get("string"):
            continue

        record = {
            "id": item.get("id"),
            "english": str(item.get("english", "")).lower(),
            "string": item["string"],
            "sense_id": item.get("sense_id"),
            "part_of_speech": item.get("part_of_speech"),
        }
        by_string[item["string"]].append(record)
        by_english[record["english"]].append(record)

    return dict(by_string), dict(by_english)


def lexical_inventory() -> list[dict]:
    # Imported lazily so the core language test suite does not need lexical
    # generator dependencies.
    import wn
    from wordfreq import zipf_frequency

    wordnet = wn.Wordnet(OEWN_LEXICON)
    inventory: dict[str, dict] = {}
    inflected_form_of: dict[str, set[str]] = defaultdict(set)

    words = wordnet.words()

    # Identify strings whose wordfreq score may be inflated because the same
    # spelling is an inflected form of another lemma (e.g. "are" <- "be").
    for word in words:
        lemma = word.lemma().lower()
        if not ASCII_WORD.fullmatch(lemma):
            continue
        for form in word.forms():
            surface = form.lower()
            if (
                surface != lemma
                and ASCII_WORD.fullmatch(surface)
                and len(surface) >= 2
            ):
                inflected_form_of[surface].add(lemma)

    for word in words:
        lemma = word.lemma().lower()
        if not ASCII_WORD.fullmatch(lemma) or len(lemma) < 2:
            continue

        record = inventory.setdefault(
            lemma,
            {
                "english": lemma,
                "parts_of_speech": set(),
                "zipf_frequency": zipf_frequency(lemma, "en"),
                "wordnet_word_ids": [],
                "senses": [],
            },
        )
        record["parts_of_speech"].add(word.pos)
        record["wordnet_word_ids"].append(word.id)

        known_sense_ids = {sense["sense_id"] for sense in record["senses"]}
        for sense in word.senses():
            if sense.id in known_sense_ids:
                continue

            synset = sense.synset()
            try:
                sense_count = sum(sense.counts())
            except Exception:
                sense_count = 0

            record["senses"].append(
                {
                    "sense_id": sense.id,
                    "synset_id": synset.id,
                    "part_of_speech": word.pos,
                    "definition_en": synset.definition() or "",
                    "corpus_count": sense_count,
                }
            )

    records: list[dict] = []
    for lemma, record in inventory.items():
        contaminators = sorted(inflected_form_of.get(lemma, set()))
        raw_zipf = float(record["zipf_frequency"])

        # This penalty affects review order only. It does not delete the
        # legitimate homographic lemma or change its recorded wordfreq value.
        effective_zipf = raw_zipf - (1.5 if contaminators else 0.0)

        record["parts_of_speech"] = sorted(record["parts_of_speech"])
        record["also_inflected_form_of"] = contaminators
        record["ranking_zipf_frequency"] = effective_zipf
        record["sense_corpus_count"] = sum(
            int(sense.get("corpus_count", 0)) for sense in record["senses"]
        )
        records.append(record)

    records.sort(
        key=lambda item: (
            -float(item["ranking_zipf_frequency"]),
            -int(item["sense_corpus_count"]),
            item["english"],
        )
    )
    return records


def build_candidates(limit: int, cmudict_path: Path) -> tuple[list[dict], dict]:
    pronunciations = load_cmudict(cmudict_path)
    accepted_by_string, accepted_by_english = accepted_index()
    generated_by_form: dict[str, list[str]] = defaultdict(list)

    inventory = lexical_inventory()
    selected = inventory[:limit]

    output: list[dict] = []
    with_pronunciation = 0
    unsupported = 0
    already_accepted = 0
    true_accepted_collisions = 0
    candidate_collisions = 0

    for rank, lexical in enumerate(selected, start=1):
        english = lexical["english"]
        variants = pronunciations.get(english, [])
        senses = lexical["senses"]

        accepted_matches = accepted_by_english.get(english, [])

        row = {
            "frequency_rank": rank,
            "english": english,
            "parts_of_speech": lexical["parts_of_speech"],
            "zipf_frequency": lexical["zipf_frequency"],
            "ranking_zipf_frequency": lexical["ranking_zipf_frequency"],
            "also_inflected_form_of": lexical["also_inflected_form_of"],
            "sense_corpus_count": lexical["sense_corpus_count"],
            "wordnet_word_ids": lexical["wordnet_word_ids"],
            "senses": senses,
            "accepted_matches": accepted_matches,
            "source_status": "oewn-lemma",
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
                review_status = "candidate"

                if accepted_matches:
                    # This English lemma is already standardized. Keep the
                    # mechanical form for audit/debugging, but do not let it
                    # create collision events: its lexical decision is already
                    # represented by the accepted dictionary entry.
                    review_status = "already-accepted"
                    already_accepted += 1
                else:
                    for existing in accepted_by_string.get(candidate, []):
                        if existing["english"] == english:
                            continue
                        collisions.append(
                            {
                                "type": "accepted-different-lemma",
                                "id": existing["id"],
                                "english": existing["english"],
                                "string": candidate,
                            }
                        )
                        true_accepted_collisions += 1

                    for previous in generated_by_form.get(candidate, []):
                        if previous == english:
                            continue
                        collisions.append(
                            {
                                "type": "candidate-different-lemma",
                                "english": previous,
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
                        "review_status": review_status,
                    }
                )

                if review_status == "candidate":
                    generated_by_form[candidate].append(english)

                with_pronunciation += 1
            except ValueError as exc:
                row["review_status"] = "unsupported-pronunciation"
                row["error"] = str(exc)
                unsupported += 1

        output.append(row)

    meta = {
        "project": "STRING",
        "purpose": "sense-aware lemma review candidates; never normative automatically",
        "requested_limit": limit,
        "available_single_word_lemmas": len(inventory),
        "generated_rows": len(output),
        "rows_with_string_candidate": with_pronunciation,
        "already_accepted_lemmas": already_accepted,
        "unsupported_pronunciation_rows": unsupported,
        "true_accepted_collision_events": true_accepted_collisions,
        "candidate_collision_events": candidate_collisions,
        "wordfreq_version": WORDFREQ_VERSION,
        "wn_version": WN_VERSION,
        "wordnet_lexicon": OEWN_LEXICON,
        "cmudict_repository": "cmusphinx/cmudict",
        "cmudict_commit": CMUDICT_COMMIT,
        "cmudict_url": CMUDICT_URL,
        "ranking_note": (
            "wordfreq ranks lemmas; forms also detected as inflections of another "
            "lemma receive a transparent 1.5 Zipf review-order penalty"
        ),
    }
    return output, meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--meta", type=Path, default=DEFAULT_META)
    parser.add_argument("--collisions", type=Path, default=DEFAULT_COLLISIONS)
    parser.add_argument(
        "--pronunciation-review",
        type=Path,
        default=DEFAULT_PRONUNCIATION_REVIEW,
    )
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

    collision_rows = [row for row in candidates if row.get("collisions")]
    pronunciation_rows = [
        row for row in candidates
        if row.get("review_status") in {
            "needs-pronunciation",
            "unsupported-pronunciation",
        }
    ]

    args.collisions.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in collision_rows),
        encoding="utf-8",
    )
    args.pronunciation_review.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in pronunciation_rows),
        encoding="utf-8",
    )

    meta["collision_review_rows"] = len(collision_rows)
    meta["pronunciation_review_rows"] = len(pronunciation_rows)

    args.meta.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
