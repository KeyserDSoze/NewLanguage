# 18 — Canonical Clause and Predicate Order

STRING uses a stable clause skeleton and a stable order for predicate operators.

This chapter does not add new conjugations. It makes the existing invariant-word system explicit.

## 1. Canonical clause skeleton — CONFIRMED

The preferred declarative order is:

```text
SUBJECT + PREDICATE CHAIN + [DIRECT OBJECT] + [RELATIONAL PHRASE...]
```

Examples:

```text
mi si buk.
I see a book.

mi giv buk tu yu.
I give a book to you.
```

## 2. Predicate chain — WORKING STANDARD

When all relevant layers are present, the preferred order is:

```text
[TENSE] [MODAL / DEPENDENCY] [HAV] [BI] LEXICAL VERB
```

The bracketed elements are optional.

Typical predicate words include:

- tense: `did`, `wil`, `wud`;
- modal/dependency: `kan`, `me`, `nid`, `mas`, `xud`, `won`;
- perfect: `hav`;
- progressive: `bi`.

## 3. Tense comes first — CONFIRMED

When explicit tense is present, it precedes the rest of the predicate chain.

```text
mi did go.
mi wil go.
mi did nid go.
mi wil kan go.
```

There is no tense agreement on later words.

## 4. Modal or dependency before aspect — WORKING STANDARD

A modal or dependency word normally precedes perfect or progressive aspect.

```text
mi xud hav go.
I should have gone.

da me bi go.
He / she / it may be going.
```

The lexical verb remains unchanged.

## 5. Perfect before progressive — CONFIRMED

When both are explicitly present:

```text
hav + bi + VERB
```

Example:

```text
mi did hav bi go.
I had been going.
```

STRING does not reverse these operators.

## 6. Copular `bi` — CONFIRMED

When `bi` links a subject to a description, identity, or location, it is the lexical predicate itself rather than a progressive operator.

```text
buk bi gud.
The book is good.

mi bi hir.
I am here.
```

When `bi` directly precedes another lexical verb, it marks progressive aspect.

```text
mi bi go.
I am going.
```

## 7. Possessive `hav` — CONFIRMED

When `hav` takes a noun phrase as its complement, it is the lexical verb **have**.

```text
mi hav buk.
I have a book / books.
```

When `hav` precedes another lexical verb, it marks perfect aspect.

```text
mi hav go.
I have gone.
```

The following word and context distinguish these uses.

## 8. Negation scope — WORKING STANDARD

`not` is placed immediately before the predicate element it negates.

Simple predicate:

```text
mi not go.
I do not go.
```

Modal:

```text
mi not kan go.
I cannot go.
```

Lexical action inside a modal:

```text
mi kan not go.
I can refrain from going.
```

Explicit tense:

```text
mi did not go.
I did not go.
```

This rule makes scope visible without creating contracted or irregular negative forms.

## 9. Canonical negation with tense — CONFIRMED

When the intended meaning is ordinary negation of the whole tensed predicate, place `not` immediately after the tense marker.

```text
mi did not go.
mi wil not go.
mi wud not go.
```

More internal placement is reserved for a deliberate narrower scope.

## 10. Yes/no question transformation — CONFIRMED

Move the first predicate element before the subject.

Statement:

```text
yu wil kan go.
```

Question:

```text
wil yu kan go?
```

Statement:

```text
da me bi go.
```

Question:

```text
me da bi go?
```

The remainder of the predicate chain keeps its order.

## 11. Negative questions — WORKING STANDARD

The same transformation applies.

With tense:

```text
yu did not go.
→ did yu not go?
```

Without an earlier predicate operator:

```text
yu not go.
→ not yu go?
```

This means approximately **do you not go? / aren't you going?** according to context.

STRING does not create contracted forms equivalent to English *don't*, *can't*, or *won't*.

## 12. Question word plus predicate inversion — CONFIRMED

A question word comes first.

The ordinary predicate inversion follows it.

```text
wen wil yu go?
When will you go?

wat did yu si?
What did you see?

ha me da go?
How may he / she / it go?
```

The question word does not change the internal predicate order.

## 13. Direct object after the lexical predicate — CONFIRMED

After the predicate chain, the direct object comes before additional relational phrases.

```text
mi wil giv buk tu yu.
I will give a book to you.
```

Canonical analysis:

```text
mi   wil   giv   buk   tu yu
SUBJ TENSE VERB  OBJ   REL
```

## 14. Clause-level context — WORKING STANDARD

A time expression, condition, or other clear clause-level context may be placed before the subject when useful.

A comma may mark this boundary in writing.

The internal subject–predicate order does not change.

Conditional clauses already use this pattern:

```text
hif yu go, mi wil go.
```

## 15. Prefer the shortest sufficient chain — CONFIRMED

Do not add tense, modality, perfect, or progressive marking merely because an English translation contains auxiliary verbs.

Use only the layers needed for the intended meaning.

The unmarked lexical verb remains the default when context already supplies the necessary time and aspect.
