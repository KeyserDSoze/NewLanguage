# 07 — Numbers

## 1. Decimal digits are universal symbols — CONFIRMED

STRING uses the ordinary decimal digits:

```text
0 1 2 3 4 5 6 7 8 9
```

Digits are symbols, not alphabetic STRING words. They may appear directly in normal text.

## 2. Canonical spoken digit names — WORKING STANDARD

Each decimal digit has one spoken STRING name.

| Digit | STRING | English anchor |
|---:|---|---|
| 0 | `ziro` | zero |
| 1 | `wan` | one |
| 2 | `tun` | two |
| 3 | `tiri` | three |
| 4 | `foro` | four |
| 5 | `fav` | five |
| 6 | `sikas` | six |
| 7 | `sevan` | seven |
| 8 | `het` | eight |
| 9 | `nayan` | nine |

The forms for 2, 4, and 9 are intentionally disambiguated from existing accepted words:

- `tu` already means **to**;
- `for` already means **for**;
- `nan` already means **none**.

This is a direct application of the dictionary collision policy.

## 3. Numbers are read digit by digit — CONFIRMED

The canonical spoken form of a written number reads its decimal digits from left to right.

```text
10  → wan ziro
25  → tun fav
204 → tun ziro foro
2026 → tun ziro tun sikas
```

There are no mandatory special words for ten, eleven, hundred, thousand, million, and so on.

This gives STRING one rule for every non-negative integer, regardless of size.

## 4. Quantity — CONFIRMED

A written number can appear directly before a noun.

```text
3 buk
three books
```

The noun does not receive a plural ending.

In speech:

```text
tiri buk
```

## 5. Leading zeroes — CONFIRMED

When leading zeroes are written, they are pronounced.

This is useful for identifiers, phone numbers, codes, and other exact digit strings.

```text
007 → ziro ziro sevan
```

## 6. Decimal point — WORKING STANDARD

The decimal point is read as `dot`.

```text
3.14 → tiri dot wan foro
```

Digits after the decimal point continue to be read one by one.

## 7. Negative numbers — WORKING STANDARD

A leading minus sign is read as `manas`.

```text
-5 → manas fav
```

## 8. Grouping separators — CONFIRMED

Thousands separators are typographic only and do not change the digit sequence.

Where a comma is used as a grouping separator:

```text
1,000 → wan ziro ziro ziro
```

A locale must not reinterpret the decimal point while reading canonical STRING numeric notation. Machine-readable STRING uses `.` as the decimal separator.

## 9. Optional lexical shortcuts — PROVISIONAL

Very common powers or mathematical concepts may later receive ordinary dictionary words.

Such shortcuts never replace the canonical digit-by-digit reading and never create irregular number morphology.

## 10. Machine-readable authority

Digit names are mirrored in:

```text
spec/numbers.json
```

Tooling can therefore render and validate numeric readings without embedding a second copy of the rules.
