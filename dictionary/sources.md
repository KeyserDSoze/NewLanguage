# Dictionary Source Policy

The released STRING dictionary must be reproducible, attributable, and legally redistributable.

The lexical pipeline separates four jobs that natural-language dictionaries often mix together:

1. lexical inventory and senses;
2. frequency prioritization;
3. pronunciation;
4. STRING normalization and human acceptance.

No single external dictionary is treated as the authority for all four.

## Open English WordNet — lexical inventory and senses

STRING uses **Open English WordNet 2025** as the preferred open lexical/sense source for the large dictionary build.

Role:

- identify English lemmas;
- separate parts of speech and senses;
- provide short English glosses/definitions;
- expose lexical relationships useful during review.

License:

- Open English WordNet is released under **CC BY 4.0**;
- it incorporates material derived from Princeton WordNet and retains the required WordNet notices.

The project must preserve the upstream attribution and license notices in dictionary distributions that incorporate this data.

The base 2025 edition is preferred for ordinary vocabulary. Proper names are handled separately by STRING's proper-name rules rather than being allowed to dominate the core 50,000-word target.

## wordfreq 3.1.1 — frequency prioritization

STRING uses **wordfreq 3.1.1** as a reproducible frequency signal.

Role:

- estimate which English lemma spellings are common;
- prioritize review order;
- help rank candidate lemmas.

The generator ranks **unique lemmas**, not separate lemma+POS rows. All Open English WordNet parts of speech and senses for the same spelling travel together into review. This prevents a single English word from consuming several positions in the 50,000-word target.

Important licensing rule:

wordfreq code is Apache-2.0, while included frequency data has separate attribution/share-alike requirements documented by the project.

STRING therefore:

- records the exact wordfreq version;
- preserves the required attribution;
- does not publish an unattributed stripped copy of wordfreq data;
- treats frequency values/ranks as source metadata, not as original STRING authorship.

Frequency rank is a prioritization tool. It is not a definition of meaning and it does not automatically make a word part of STRING.

## CMU Pronouncing Dictionary — pronunciation

STRING uses the upstream **CMU Pronouncing Dictionary** as the primary machine-readable US-English pronunciation source.

Pinned dictionary source for candidate generation:

```text
repository: cmusphinx/cmudict
commit: 0f8072f814306c5ee4fbf992ed853601b12c01f9
file: cmudict.dict
```

Role:

- provide one or more US-English pronunciations;
- convert ARPABET to broad IPA;
- feed the deterministic IPA → STRING normalizer.

CMU states that use of the dictionary for research or commercial purposes is unrestricted and requests acknowledgment of its origin.

## Source precedence

For a large-scale candidate:

```text
Open English WordNet lemma + sense
        ↓
wordfreq priority
        ↓
CMUdict pronunciation where available
        ↓
broad IPA
        ↓
STRING mechanical normalization
        ↓
collision analysis
        ↓
human review
        ↓
accepted dictionary entry
```

When CMUdict lacks a pronunciation, the candidate is flagged for pronunciation review rather than guessed silently.

When a frequent surface form is merely an English inflection that STRING grammar does not need as a separate word, it should resolve to the relevant base lexical concept instead of becoming a redundant STRING entry.

## Definitions

Definitions imported from Open English WordNet retain source attribution.

Human-edited STRING definitions should remain short and should describe the intended sense, not copy text from incompatible proprietary dictionaries.

## Reproducibility

Generator dependencies are pinned.

Generated candidate files are build artifacts. They are not automatically canonical dictionary content.

Only explicitly reviewed records added to `dictionary/entries.jsonl` can become `accepted`.


## Frequency contamination by English inflection

A spelling can be both a rare dictionary lemma and a very common inflected form of another word. For example, a lexical entry spelled like an English auxiliary form can inherit that auxiliary's very high surface frequency.

The generator detects when a candidate lemma also appears as a non-lemma form of another Open English WordNet word. It records those source lemmas in `also_inflected_form_of` and applies a transparent ranking penalty.

This affects review order only. It never deletes the legitimate homographic sense.

Accepted STRING core lemmas are classified as `already-accepted` instead of being counted as collisions with themselves.
