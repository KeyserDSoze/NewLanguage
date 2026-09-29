# 01 — Orthography and Pronunciation

## 1. Fundamental rule — CONFIRMED

STRING is phonemic:

> Write what is pronounced. Pronounce what is written.

There are no silent letters, contextual spelling rules, or alternate spellings for the same standard word.

The final alphabet must obey **one symbol = one sound**.

## 2. Lexical relationship with English — CONFIRMED

English is the primary source of lexical roots.

STRING words should remain as close as practical to the **pronunciation** of the corresponding English word, not to its traditional English spelling.

Examples such as English words with silent letters, irregular vowel spelling, or ambiguous consonants must be respelled according to STRING pronunciation rules.

IPA is used as a technical bridge:

```text
English word → reference IPA → STRING sounds → STRING spelling
```

IPA is metadata and a design tool. Ordinary STRING is written with the STRING alphabet.

## 3. Word shape — CONFIRMED

The canonical STRING word shape is:

```text
(CV)+C?
```

Where:

- `C` = one consonant;
- `V` = one vowel;
- `+` = one or more CV units;
- `C?` = zero or one final consonant.

Examples:

- `DARU` = DA-RU
- `MALU` = MA-LU
- `CAMU` = CA-MU
- `MAR` = MA-R

A final consonant is allowed when it produces a shorter or more natural-sounding word.

The final consonant is not optional in pronunciation. `MAR` and `MARU` would be different written forms and therefore different pronunciations.

## 4. Forbidden structures — CONFIRMED

Standard STRING words do not contain:

- adjacent vowels;
- diphthongs as two-vowel sequences;
- internal consonant clusters;
- silent letters;
- letters whose pronunciation changes from word to word.

The normalization process must repair an English source pronunciation when it would create one of these structures.

## 5. English recognition versus regularity — CONFIRMED

The lexical design priority is:

1. deterministic STRING pronunciation;
2. legal STRING word shape;
3. closeness to recognizable English pronunciation;
4. short and pleasant sound;
5. closeness to English spelling.

This means a STRING form may differ substantially from English spelling while remaining recognizably related to its sound.

## 6. Reference accent and phoneme mapping — PROVISIONAL

The dictionary will store a normalized reference IPA pronunciation for each English source sense. Common pronunciation variants may also be stored.

Before mass-generating the 50,000-word dictionary, the project must freeze:

- the STRING vowel inventory;
- the STRING consonant inventory;
- the exact letter-to-sound table;
- rules for English sounds absent from STRING;
- rules for English vowel-initial words;
- rules for English diphthongs;
- rules for consonant clusters;
- collision rules when two English words normalize to the same STRING form.

No automatically generated lexical form becomes normative until it passes these rules.
