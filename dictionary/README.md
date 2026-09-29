# STRING Dictionary

The first major lexical target is a dictionary based on approximately the **50,000 most-used English words**.

English supplies the source concepts and recognizable pronunciations. STRING supplies a regular pronunciation and spelling system.

## Generation pipeline

Each candidate entry follows this pipeline:

```text
English lemma
  + part of speech
  + intended sense
  + frequency rank
        ↓
reference English IPA
        ↓
phoneme normalization
        ↓
STRING phonotactic repair
        ↓
collision check
        ↓
human review
        ↓
accepted STRING form
```

## Core lexical rule

STRING follows **English sound, not English spelling**.

For example, an English spelling containing silent letters or inconsistent vowel letters must never be copied blindly. The IPA pronunciation is the lexical source used by the normalizer.

## Frequency list

The 50,000-word list must record its source, license, frequency methodology, and corpus date.

Raw source lists belong in a source-data area and should not be silently edited. Generated STRING entries should be reproducible from source data plus normalization rules.

## Sense separation

One English spelling can represent multiple unrelated meanings. Dictionary generation must therefore operate on **lemma + sense**, not only on text strings.

Where a single STRING word can safely cover related senses, that relationship should be documented explicitly.

## Collisions

Because STRING deliberately has a small and regular sound system, unrelated English words may normalize to the same candidate form.

Collisions must be resolved systematically, for example by:

- choosing a secondary recognizable English pronunciation feature;
- using a legal extra CV unit;
- reserving extremely short forms for high-frequency grammar words;
- rejecting a candidate that is too easily confused in speech.

Collision handling must never introduce irregular pronunciation.

## Data format

The canonical machine-readable dictionary will use structured data. See `schema.md`.

Human-facing PDF, EPUB, and website versions are generated from the same canonical data rather than maintained separately.
