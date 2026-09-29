# STRING

**STRING** is an experimental universal language designed to be simple to learn, fast to use, predictable to pronounce, and easy for both humans and machines to process.

The project starts from an older language design and rebuilds it around two strict principles:

1. **what you write is what you say**;
2. **new vocabulary should remain as close as practical to recognizable English pronunciation**.

English is the primary lexical donor language. STRING does **not** copy irregular English spelling: the pronunciation of an English word is taken as the source, represented technically with IPA, and then normalized into STRING's regular sound and word system.

## Core principles

- **One written form, one spoken form.** No silent letters and no hidden pronunciation rules.
- **One symbol, one sound.** Once the final alphabet is fixed, every STRING letter will keep the same pronunciation in every word.
- **English-derived vocabulary.** New lexical roots should resemble the English pronunciation whenever the STRING sound system allows it.
- **IPA as a reference layer.** IPA is stored in the dictionary to document source pronunciation; normal STRING text uses the STRING alphabet, not IPA.
- **Simple word shapes.** Words are built from consonant-vowel units, with an optional single final consonant: `(CV)+C?`.
- **No diphthongs in STRING surface forms.** English diphthongs are normalized to legal STRING sounds.
- **No internal consonant clusters.**
- **Short, regular words.** Forms such as `DARU`, `MALU`, `CAMU`, and `MAR` represent the intended rhythm.
- **Minimal grammar.** Prefer explicit particles and regular constructions over exceptions and inflection tables.
- **No unnecessary grammatical information.** A distinction is encoded only when it adds useful meaning.
- **International use.** The language should be practical for conversation, writing, teaching, translation, and machine use.

## Repository structure

- `grammar/` — the normative grammar, written in English.
- `dictionary/` — dictionary model, lexical rules, source data, and generated entries.
- `prompts/` — prompts for LLMs that need to understand or produce STRING.
- `site/` — source area for the future static documentation and searchable dictionary.
- `book/` — publishing plan and sources for future PDF and EPUB editions.

## Project goals

The project will ultimately publish:

1. a complete but intentionally small grammar;
2. a practical dictionary, initially based on the 50,000 most-used English words;
3. a grammar book in PDF and EPUB;
4. a dictionary in PDF and EPUB;
5. a static GitHub Pages website containing the complete grammar and a searchable dictionary;
6. machine-readable lexical data and an LLM reference prompt.

## Current word-shape rule

A STRING word follows:

```text
(CV)+C?
```

That means one or more consonant-vowel units, optionally followed by one final consonant.

Examples:

- `DARU` → DA-RU
- `MALU` → MA-LU
- `CAMU` → CA-MU
- `MAR` → MA-R

The final consonant is part of the word: it is written if it is pronounced and pronounced if it is written.

## Lexical derivation

The intended dictionary workflow is:

```text
English lemma + sense
        ↓
reference English pronunciation (IPA)
        ↓
STRING phonological normalization
        ↓
legal STRING word shape
        ↓
final STRING spelling
```

Recognition matters, but regularity has priority. A spelling inherited from English is never kept merely because it is familiar if it breaks STRING pronunciation rules.

## Design status

STRING is under active design. Grammar documents distinguish **confirmed rules**, **provisional rules**, and **legacy material**.

The historical spreadsheet is a design source, not an automatic standard. Older forms that conflict with the current phonetic or grammatical principles are redesigned rather than copied unchanged.
