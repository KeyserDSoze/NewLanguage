# Dictionary Data Schema

The canonical dictionary is stored as UTF-8 JSON Lines in `dictionary/entries.jsonl`.

Each line is one lexical entry.

## Canonical fields

| Field | Required for accepted entries | Purpose |
|---|---:|---|
| `id` | yes | Stable internal identifier |
| `english` | yes | English source or lexical anchor |
| `sense_id` | yes | Stable identifier for the intended meaning |
| `part_of_speech` | yes | Noun, verb, pronoun, particle, etc. |
| `frequency_rank` | no | Rank in the selected English corpus |
| `definition_en` | yes | Original short English definition |
| `ipa_reference` | yes | Broad reference English pronunciation |
| `ipa_variants` | no | Common pronunciation variants |
| `string` | yes | Canonical STRING headword |
| `string_segments` | yes | Explicit STRING segmentation, e.g. `ha-v` |
| `status` | yes | `proposed`, `reviewed`, `accepted`, or `deprecated` |
| `source` | yes | Lexical/frequency/design source |
| `notes` | no | Review, collision, or derivation notes |

## Canonical spelling

Dictionary headwords are stored in lowercase.

Capitalization is typographic and does not change pronunciation or meaning.

Every non-empty `string` value must satisfy the current machine-readable phonology in `spec/phonology.json`.

The build validator checks:

- legal STRING letters;
- `(CV)+C?` word shape;
- exact `string_segments`;
- unique entry IDs;
- accidental duplicate accepted headwords;
- required metadata for accepted words.

## Status meaning

### proposed

A generated or human-suggested candidate. It is not standard STRING.

### reviewed

A candidate that has been examined but is not yet part of the accepted standard.

### accepted

A normative dictionary word. Accepted entries are included in released dictionary books and the public standard.

### deprecated

A former form retained for migration/history and excluded from the current standard.

## Example

```json
{
  "id": "core-hav",
  "english": "have",
  "sense_id": "verb.have",
  "part_of_speech": "verb",
  "frequency_rank": null,
  "definition_en": "Possessive verb and perfect-aspect auxiliary.",
  "ipa_reference": "/hæv/",
  "ipa_variants": [],
  "string": "hav",
  "string_segments": "ha-v",
  "status": "accepted",
  "source": "STRING core grammar v0.2",
  "notes": "Invariant."
}
```

## Definitions and external sources

The future 50,000-word import must use sources whose licenses permit the intended redistribution.

Definitions should not be copied from an incompatible copyrighted dictionary. Frequency source, pronunciation source, sense source, and license information must be recorded by the import pipeline.
