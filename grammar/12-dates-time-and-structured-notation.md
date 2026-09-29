# 12 — Dates, Time, and Structured Notation

STRING uses international numeric notation whenever a stable symbol system is already simpler than inventing many grammatical words.

## 1. Date label — WORKING STANDARD

`det` means **date**.

The preferred written date format is ISO-style:

```text
YYYY-MM-DD
```

Example:

```text
det 2026-09-29
```

This order is fixed from largest unit to smallest unit and avoids locale-dependent day/month reversal.

## 2. Reading a date — WORKING STANDARD

Within a date, each numeric group is read using the canonical digit-by-digit number system.

Group boundaries are preserved by a short pause in speech.

Example:

```text
det 2026-09-29
```

is read conceptually as:

```text
det
tun ziro tun sikas
ziro nayan
tun nayan
```

The hyphens are date separators. They are not spoken as negative signs.

## 3. Time label — WORKING STANDARD

`tam` means **time**.

The preferred written clock format is the 24-hour form:

```text
HH:MM
```

Example:

```text
tam 14:30
```

This avoids a mandatory AM/PM system.

## 4. Reading clock time — WORKING STANDARD

Read the hour group and minute group digit by digit, with a short boundary between them.

```text
tam 14:30
→ tam wan foro | tiri ziro
```

Leading zeroes remain audible.

```text
tam 08:05
→ tam ziro het | ziro fav
```

## 5. Seconds — CONFIRMED

Seconds may be added:

```text
HH:MM:SS
```

Each group follows the same rule.

No separate grammatical construction is created for seconds.

## 6. Exact machine timestamps — CONFIRMED

ISO 8601 timestamps, UTC offsets, and similar machine identifiers may appear as structured technical notation.

Their punctuation is part of the technical notation rather than ordinary STRING word morphology.

A speaker may read the meaningful numeric components when necessary.

## 7. Calendar words — PROVISIONAL

Names for weekdays, months, relative days, seasons, and other calendar concepts are ordinary dictionary vocabulary.

They should be derived and reviewed through the normal lexical pipeline rather than embedded as irregular grammar.

## 8. Duration — CONFIRMED

Duration uses ordinary quantities plus ordinary time-unit dictionary words.

The time-unit noun does not receive a plural suffix.

The general pattern is:

```text
NUMBER + TIME-UNIT
```

Once the relevant unit words are accepted, the same pattern works for seconds, minutes, hours, days, weeks, months, and years.

## 9. Relative temporal relations — CONFIRMED

Existing prepositions continue to apply:

- `bifor` — before;
- `hafer` — after;
- `durin` — during;
- `til` — until;
- `fam` — from / since a starting point.

STRING does not require a second grammatical system specifically for time.
