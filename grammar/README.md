# STRING Grammar

This directory contains the normative grammar of STRING.

The grammar is written in English so that the project has one common documentation language. STRING examples appear inside the chapters.

## Editorial rules

Every grammatical feature should be:

- explicit;
- regular;
- short to explain;
- free of unnecessary exceptions;
- usable without memorizing large paradigms;
- compatible with the rule that written STRING is pronounced exactly as written.

Nothing is inherited automatically merely because it exists in English or another natural language.

## Status labels

Grammar decisions use four statuses:

- **CONFIRMED** — accepted as part of the current STRING specification.
- **WORKING STANDARD** — implemented and used by the current tools, but deliberately easier to revise before 1.0.
- **PROVISIONAL** — an explored rule that is not yet relied upon by the standard.
- **LEGACY** — extracted from the historical spreadsheet and retained only as design input.

Normative current files take precedence over legacy notes.

Machine-readable working standards live in `spec/`, including phonology and canonical number reading.

## Current chapters

- `01-orthography-and-pronunciation.md`
- `02-core-grammar.md`
- `03-pronouns-and-nouns.md`
- `04-verbs-tense-and-questions.md`
- `05-modifiers-quantity-and-comparison.md`
- `06-prepositions-and-conjunctions.md`
- `07-numbers.md`
- `08-writing-proper-names-and-compounds.md`
- `09-commands-and-complex-sentences.md`
- `10-word-classes-and-word-formation.md`
- `11-reference-reflexives-and-existence.md`
- `12-dates-time-and-structured-notation.md`
- `13-core-sentence-patterns.md`
- `14-modality-necessity-advice-and-intention.md`
- `15-indefinite-reference-and-selection.md`
- `16-verb-complements-and-semantic-roles.md`
- `17-canonical-noun-phrase-order.md`
- `18-canonical-clause-and-predicate-order.md`

The book pipeline discovers numbered grammar chapters automatically, so adding a new chapter to this directory adds it to the next generated grammar publication.
