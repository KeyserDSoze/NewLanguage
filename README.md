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

- `grammar/` — normative grammar sources, written in English.
- `dictionary/` — canonical lexical data, lexical rules, and dictionary metadata.
- `prompts/` — prompts for LLMs that need to understand or produce STRING.
- `site/` — sources for the static documentation and searchable dictionary.
- `book/` — publishing policy only; generated books are never edited here.
- `scripts/` — deterministic generators used by CI.
- `.github/workflows/` — build and release automation.

## Single-source publishing model

The repository is the source; the books are build products.

**PDF and EPUB files are never edited or committed manually.** Contributions are made to grammar Markdown, dictionary data, prompts, and other canonical sources. GitHub Actions rebuilds the publications from those sources.

The build pipeline produces:

- `STRING-Grammar-vX.Y.Z.pdf`
- `STRING-Grammar-vX.Y.Z.epub`
- `STRING-Dictionary-vX.Y.Z.pdf`
- `STRING-Dictionary-vX.Y.Z.epub`
- versioned machine-readable dictionary data;
- a build manifest containing the exact source commit;
- SHA-256 checksums.

Every push to `main` builds and validates the current publications as a GitHub Actions artifact.

## Versioning and releases

The canonical project version is stored in `VERSION` and follows semantic versioning.

A release version is immutable:

1. update the canonical source files;
2. update `VERSION` when the contribution set is ready to become a release;
3. push to `main`;
4. GitHub Actions rebuilds everything;
5. the workflow creates tag `vX.Y.Z`;
6. the generated PDF, EPUB, dictionary data, build manifest, and checksums are attached to the GitHub Release.

The workflow can also be started manually from GitHub Actions with **Publish the current VERSION** enabled. This is useful for publishing a version whose `VERSION` file already existed before the release pipeline.

Generated output is intentionally ignored by Git. A release can always be reproduced from its tag and source commit.

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
