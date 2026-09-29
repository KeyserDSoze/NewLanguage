# Dictionary Data Schema

The canonical dictionary should be representable as JSONL and exportable to CSV.

Recommended fields:

| Field | Purpose |
|---|---|
| `id` | Stable internal identifier |
| `english` | English source lemma |
| `sense_id` | Identifier for the intended meaning |
| `part_of_speech` | Noun, verb, adjective, etc. |
| `frequency_rank` | Rank in the selected English corpus |
| `definition_en` | Short English definition of the sense |
| `ipa_reference` | Normalized source pronunciation |
| `ipa_variants` | Optional common pronunciation variants |
| `string` | Accepted STRING form |
| `string_segments` | Explicit CV segmentation, e.g. `MA-R` |
| `status` | proposed, reviewed, accepted, deprecated |
| `source` | Lexical/frequency source reference |
| `notes` | Collision or normalization notes |

## Example shape

```json
{
  "id": "example-000001",
  "english": "example",
  "sense_id": "example.n.01",
  "part_of_speech": "noun",
  "frequency_rank": 1,
  "definition_en": "placeholder only",
  "ipa_reference": "/.../",
  "ipa_variants": [],
  "string": "PLACEHOLDER",
  "string_segments": "CV-CV-C",
  "status": "proposed",
  "source": "TBD",
  "notes": "Not a normative lexical entry."
}
```

The example above illustrates structure only. It does not define a STRING word.
