# STRING Dictionary

The first large lexical target is a dictionary based on approximately the **50,000 most-used English words**.

English supplies the lexical anchor and recognizable pronunciation. STRING supplies a small, regular sound system and deterministic spelling.

## Canonical files

- `entries.jsonl` — accepted and proposed lexical data.
- `schema.md` — dictionary record format.
- `collision-policy.md` — rules for avoiding accidental homophones.
- `../spec/phonology.json` — machine-readable sound system and IPA mapping.

## Generation pipeline

```text
English lemma + sense + frequency
            ↓
licensed/reference pronunciation data
            ↓
broad English IPA
            ↓
scripts/normalize_ipa.py
            ↓
mechanical STRING candidate
            ↓
collision check
            ↓
human review / optional shortening
            ↓
scripts/validate_sources.py
            ↓
accepted STRING entry
```

The mechanical candidate is reproducible but is never automatically normative.

## Core lexical rule

STRING follows **English sound, not English spelling**.

Silent letters, English vowel ambiguity, and inconsistent English spelling conventions are discarded.

## Current core vocabulary

The repository already contains the accepted grammatical vocabulary needed by the current grammar, including:

- personal pronouns;
- negation;
- tense markers;
- core auxiliaries;
- demonstratives;
- question words;
- a small set of example lexical words.

This core vocabulary is reserved before mass generation begins.

## Frequency list

The 50,000-word source must record:

- corpus/source name;
- source version or date;
- license;
- frequency methodology;
- lemma/sense policy.

Raw imported source data must remain reproducible and should not be silently edited.

## Sense separation

Generation operates on **lemma + intended sense**, not spelling alone.

Related meanings may intentionally share one STRING entry. Unrelated meanings should not accidentally become homophones.

## Validation

Run:

```bash
python3 scripts/validate_sources.py
```

A failed validation blocks the publication pipeline.

## Single source

PDF, EPUB, website, search indexes, and machine-readable exports are generated from the canonical dictionary data. None of those outputs is maintained separately.
