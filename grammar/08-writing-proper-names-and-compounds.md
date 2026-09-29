# 08 — Writing, Proper Names, and Compounds

## 1. Canonical case — CONFIRMED

Canonical STRING dictionary words are lowercase.

Uppercase letters may be used typographically for:

- the beginning of a sentence;
- headings;
- display text;
- names;
- emphasis where the writing system permits it.

Case never changes pronunciation or lexical meaning.

`mi`, `Mi`, and `MI` contain the same STRING sounds.

## 2. Punctuation — CONFIRMED

STRING uses common international punctuation:

```text
. , ? ! : ; ( ) " "
```

Punctuation organizes text and indicates boundaries or discourse intent. It is not part of a word and does not change the pronunciation of its letters.

A question mark is recommended for written questions even though question syntax is already grammatical.

## 3. No grammatical apostrophe — CONFIRMED

STRING does not use apostrophes for:

- possession;
- contractions;
- omitted letters;
- plural formation.

There are no grammatical contractions with hidden or deleted sounds.

An apostrophe may appear only when reproducing external text.

## 4. Hyphen — WORKING STANDARD

A hyphen may be used editorially to show pronunciation segmentation or to clarify an unfamiliar compound.

It is not normally part of the canonical dictionary spelling.

For example:

```text
ha-va
```

is a teaching representation of canonical `hava`.

## 5. Proper names — WORKING STANDARD

A proper name used inside fully pronounceable STRING should be adapted from its **spoken source pronunciation**, not copied from an irregular source spelling.

The same phonological rules used for English-derived vocabulary apply:

1. obtain a reliable pronunciation;
2. map the sounds to the STRING inventory;
3. repair the result to legal STRING phonotactics;
4. write exactly the resulting STRING pronunciation.

The adapted name does not need to become a dictionary entry.

## 6. Preserving an external spelling — CONFIRMED

When exact identity matters, an external spelling may be shown as metadata or quoted text next to the STRING-adapted name.

External spelling is not automatically valid STRING pronunciation.

This distinction is especially important for:

- legal names;
- usernames;
- URLs;
- product names;
- source-language quotations;
- scientific identifiers.

## 7. URLs, email addresses, code, and identifiers — CONFIRMED

Machine identifiers may appear unchanged inside STRING text.

They are treated as external technical tokens, not as ordinary STRING words.

The rule "write as pronounced" applies to STRING lexical text, not to opaque identifiers that must preserve exact bytes.

## 8. Compounds prefer separate words — CONFIRMED

New concepts should first be expressed compositionally with existing words.

A transparent phrase is preferred over creating a new lexical item when both are equally clear.

This keeps the dictionary smaller and meaning easier to infer.

## 9. Modifier–head order — WORKING STANDARD

For noun compounds, the more specific modifier normally comes before the semantic head, following the same pattern as ordinary modifiers.

```text
MODIFIER + HEAD
```

This preserves a familiar English-like order while keeping both component words unchanged.

## 10. Lexicalized compounds — WORKING STANDARD

A frequent compound may eventually become one dictionary entry when:

- its meaning is stable;
- it is common enough to justify memorization;
- the combined word remains legal STRING;
- lexicalization does not create an avoidable collision.

Until accepted as a dictionary entry, write the components as separate words.

## 11. Abbreviations and acronyms — PROVISIONAL

STRING avoids making abbreviations a core grammatical requirement.

A future chapter may define spoken letter names for acronyms. Until then, an external acronym can remain an external technical token or be replaced by its full STRING expression.
