# 01 — Orthography and Pronunciation

## 1. Fundamental rule — CONFIRMED

STRING is phonemic:

> Write what is pronounced. Pronounce what is written.

There are no silent letters, contextual spelling rules, or alternate standard spellings for the same word.

Case is typographic only. The canonical dictionary stores headwords in lowercase.

## 2. Lexical relationship with English — CONFIRMED

English is the primary source of lexical roots.

STRING follows the **pronunciation** of an English source word rather than copying its historical spelling.

The technical pipeline is:

```text
English lemma + sense
        ↓
broad reference IPA
        ↓
STRING phoneme mapping
        ↓
phonotactic repair
        ↓
reviewed STRING word
```

IPA is metadata and a design tool. Normal STRING text is written with the STRING alphabet.

The default technical reference is broad General American IPA. Common variants may be stored and may be used during human review when they produce a better legal STRING form.

## 3. Five vowels — WORKING STANDARD

STRING uses five vowel phonemes.

| Letter | Target IPA | Rule |
|---|---:|---|
| `A` | /a/ | one open vowel |
| `E` | /e/ | one mid-front vowel |
| `I` | /i/ | one high-front vowel |
| `O` | /o/ | one mid/back rounded vowel |
| `U` | /u/ | one high-back rounded vowel |

English vowel distinctions are intentionally compressed into these five vowels.

Examples of the normalization groups:

- English /i, ɪ/ → `I`
- English /e, ɛ, eɪ/ → `E`
- English /æ, ʌ, ə/ → `A`
- English /ɑ, ɒ, ɔ, oʊ/ → `O`
- English /u, ʊ/ → `U`

English diphthongs do not remain diphthongs in STRING. They collapse to one STRING vowel.

## 4. Consonants — WORKING STANDARD

Each consonant letter has one phonemic value.

| Letter | IPA |
|---|---:|
| `B` | /b/ |
| `C` | /tʃ/ |
| `D` | /d/ |
| `F` | /f/ |
| `G` | /g/ |
| `H` | /h/ |
| `J` | /dʒ/ |
| `K` | /k/ |
| `L` | /l/ |
| `M` | /m/ |
| `N` | /n/ |
| `P` | /p/ |
| `R` | /ɹ/ |
| `S` | /s/ |
| `T` | /t/ |
| `V` | /v/ |
| `W` | /w/ |
| `X` | /ʃ/ |
| `Y` | /j/ |
| `Z` | /z/ |

`Q` is not currently part of the STRING alphabet.

The English sounds /θ/ and /ð/ normalize to `T` and `D`. English /ŋ/ normalizes to `N`. English /ʒ/ normalizes to `J`.

Accent variation is acceptable in ordinary speech as long as speakers preserve the phonemic distinctions of STRING. Accent never changes spelling.

## 5. Word shape — CONFIRMED

The canonical STRING word shape is:

```text
(CV)+C?
```

Where:

- `C` = one STRING consonant;
- `V` = one STRING vowel;
- `+` = one or more CV units;
- `C?` = zero or one final consonant.

Examples of legal shapes:

- `daru` = DA-RU
- `malu` = MA-LU
- `camu` = CA-MU
- `mar` = MA-R
- `not` = NO-T
- `hav` = HA-V

A final consonant is part of the word. It is never an optional pronunciation.

## 6. Forbidden structures — CONFIRMED

A standard STRING word does not contain:

- adjacent vowels;
- an internal consonant cluster;
- a silent letter;
- a contextual letter pronunciation;
- stress-based lexical distinctions;
- pronunciation differences encoded only by capitalization.

## 7. Vowel-initial English words — WORKING STANDARD

Because STRING syllables require a consonant onset, a mechanical candidate derived from an English vowel-initial word receives audible `H`.

For example, a source beginning with /æ/ begins mechanically as `HA...`.

This is a repair sound, not a silent carrier.

## 8. Consonant-cluster repair — WORKING STANDARD

English consonant clusters are repaired mechanically before review.

When a cluster is followed by a vowel, the generator copies that next STRING vowel as needed to create CV units.

Example mechanical candidate:

```text
English "string" /strɪŋ/
S T R I N
→ SI-TI-RI-N
→ sitirin
```

When a cluster has no following vowel, `A` is the default repair vowel while preserving at most one final consonant.

Example:

```text
English "work" /wɝk/
W E R K
→ WE-RA-K
→ werak
```

Mechanical candidates are reproducible but are **not automatically dictionary words**.

## 9. Human lexical review — CONFIRMED

A reviewer may shorten a mechanical candidate when the shorter form:

1. still resembles a recognizable English pronunciation;
2. obeys the current STRING alphabet;
3. obeys `(CV)+C?`;
4. creates no silent spelling;
5. does not create an accidental collision with an accepted word.

A reviewer may also select a documented English pronunciation variant.

The accepted STRING spelling remains fully phonemic even when it differs from the mechanical candidate.

## 10. Machine-readable authority

The current alphabet and normalization tables are mirrored in:

```text
spec/phonology.json
```

Dictionary validation and future lexical generation use that file directly.
