# Publishing

STRING is published as generated artifacts, not as hand-maintained book files.

The two primary books are:

1. **STRING Grammar**
2. **STRING Dictionary**

Both are generated from the same canonical repository sources used by the website and machine-readable exports.

## Non-negotiable publishing rule

**Never edit a generated PDF, EPUB, or assembled book Markdown file.**

The editable sources are:

- `grammar/*.md` for normative grammar chapters;
- `dictionary/intro.md` for the dictionary introduction;
- `dictionary/entries.jsonl` for lexical entries;
- repository metadata such as `VERSION`.

The build script discovers normative grammar chapters automatically. Files named `README.md` and `legacy*.md` are not included in the normative grammar book.

The dictionary book includes only entries with:

```json
"status": "accepted"
```

Proposed dictionary entries therefore remain reviewable in source control without accidentally becoming part of a released standard.

## Generated formats

Every build produces:

- grammar PDF;
- grammar EPUB;
- dictionary PDF;
- dictionary EPUB;
- machine-readable dictionary JSONL;
- build manifest;
- SHA-256 checksum file.

Generated filenames contain the project version.

## Reproducibility

`scripts/build_books.py` assembles the canonical Markdown inputs.

GitHub Actions then uses Pandoc to generate EPUB and PDF. The build manifest records the version, source commit, included grammar files, and accepted dictionary entry count.

The generated `build/` and `dist/` directories are ignored by Git.

## Release lifecycle

The canonical version is stored in the root `VERSION` file.

On every push to `main`, GitHub Actions builds the books and stores them as a workflow artifact.

When `VERSION` changes on `main`, the workflow additionally:

1. creates immutable tag `vX.Y.Z`;
2. creates the corresponding GitHub Release;
3. uploads all generated publications and checksums.

A manual workflow dispatch can also publish the current `VERSION` when needed.

A released version tag is never moved to another commit.

## Grammar book

The grammar book should be intentionally explicit. A rule may be repeated where repetition improves learning or removes ambiguity.

Planned chapters include:

- design principles;
- alphabet and pronunciation;
- word formation;
- pronouns;
- noun phrases;
- verbs;
- negation;
- questions;
- tense/aspect/mood;
- prepositions;
- conjunctions;
- quantities and numbers;
- sentence patterns;
- examples and exercises.

## Dictionary book

Each accepted entry should include, where applicable:

- STRING headword;
- English source lemma;
- part of speech;
- English definition/sense;
- source IPA;
- pronunciation segmentation;
- usage notes;
- related forms.

The digital dictionary may expose additional metadata that is omitted from print for readability.
