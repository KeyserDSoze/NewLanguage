# STRING

**STRING** is an experimental universal language designed to be simple to learn, fast to use, predictable to pronounce, and easy for both humans and machines to process.

The project starts from an older language design and rebuilds it around a stricter principle: **what you write is what you say**.

## Core principles

- **One written form, one spoken form.** No silent letters and no hidden pronunciation rules.
- **Simple word shapes.** Words are built from consonant-vowel units, with an optional single final consonant: `(CV)+C?`.
- **No diphthongs.** Adjacent vowel sounds are avoided.
- **No internal consonant clusters.** Consonants do not pile up inside a word.
- **Short, regular words.** Forms such as `DARU`, `MALU`, `CAMU`, and `MAR` represent the intended rhythm.
- **Minimal grammar.** Prefer explicit particles and regular constructions over exceptions and inflection tables.
- **No unnecessary grammatical information.** A distinction is encoded only when it adds useful meaning.
- **International use.** The language should be practical for conversation, writing, teaching, translation, and machine use.

## Repository structure

- `grammar/` — the normative grammar, written in English.
- `dictionary/` — dictionary data and generation rules.
- `prompts/` — prompts for LLMs that need to understand or produce STRING.
- `site/` — sources for the future static documentation and searchable dictionary.
- `book/` — sources/configuration for future PDF and EPUB publications.

## Project goals

The project will ultimately publish:

1. a complete but intentionally small grammar;
2. a practical dictionary, initially derived from the 50,000 most-used English words;
3. a grammar book in PDF and EPUB;
4. a dictionary in PDF and EPUB;
5. a static GitHub Pages website containing the complete grammar and a searchable dictionary;
6. machine-readable lexical data and an LLM reference prompt.

## Design status

STRING is under active design. The grammar files distinguish stable rules from provisional decisions. The historical spreadsheet is treated as a design source, not as an automatic standard: older forms that conflict with the current phonotactic rules will be redesigned.

## Current phonotactic rule

A STRING word follows:

```text
(CV)+C?
```

That means one or more consonant-vowel units, optionally followed by one final consonant.

Valid shape examples:

- `DARU` → DA-RU
- `MALU` → MA-LU
- `CAMU` → CA-MU
- `MAR` → MA-R

The final consonant is written if it is pronounced and pronounced if it is written.

## License and contributions

Licensing and contribution rules will be defined as the language specification stabilizes.
