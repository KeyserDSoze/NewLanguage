# Dictionary Review Process

Generated dictionary candidates are evidence for review. They are never standard STRING by themselves.

## 1. Generate

Run the **Generate dictionary candidates** workflow.

A normal manual full run uses:

```text
limit = 50000
```

The workflow produces:

- `dictionary-candidates.jsonl`;
- `dictionary-candidates.meta.json`.

Each candidate contains:

- English lemma;
- Open English WordNet parts of speech;
- WordNet senses and definitions;
- frequency priority;
- pronunciation variants;
- broad IPA;
- mechanical STRING form;
- STRING segmentation;
- accepted-word matches;
- collision information;
- inflection-frequency warnings.

## 2. Already accepted

If a lemma is already represented by an accepted core STRING entry, the generator marks it:

```text
already-accepted
```

This is not a collision.

The reviewer checks whether newly surfaced WordNet senses are legitimately covered by the existing entry or whether an unrelated sense requires a separate lexical solution.

## 3. Decide sense scope

One English spelling can contain unrelated meanings.

Review is therefore about **meaning**, not only spelling.

Related meanings may remain under one STRING headword when doing so is natural and understandable.

Unrelated meanings should normally become distinct STRING lexical entries, even when English happens to spell and pronounce them identically.

## 4. Review the mechanical form

The mechanical form is the deterministic baseline.

A reviewer may:

- keep it unchanged;
- shorten it while preserving recognizable source pronunciation;
- choose a documented pronunciation variant;
- preserve an additional source sound to resolve a collision;
- add a legal CV unit when necessary for disambiguation.

The final form must still satisfy the current phonological specification.

## 5. Resolve collisions

A real collision exists when unrelated lexical meanings would receive the same accepted STRING form.

Use `collision-policy.md`.

Never resolve a collision with:

- silent spelling;
- stress only;
- capitalization only;
- an illegal consonant cluster;
- adjacent vowels.

## 6. Promote through statuses

Canonical records use:

```text
proposed
reviewed
accepted
deprecated
```

A practical path is:

```text
generated candidate
      ↓
proposed
      ↓
reviewed
      ↓
accepted
```

Only `accepted` entries appear as standard words in released dictionary books and the public site.

## 7. Preserve provenance

When a candidate becomes canonical, keep enough metadata to reconstruct why it exists:

- source lemma;
- sense identifier;
- frequency rank;
- source IPA;
- pronunciation variants where useful;
- source/license reference;
- collision or shortening notes.

## 8. Never bulk-accept automatically

Large batches may be generated automatically.

Acceptance is intentionally explicit.

The language should remain small, predictable, and understandable rather than becoming a blind transliteration of every English dictionary entry.
