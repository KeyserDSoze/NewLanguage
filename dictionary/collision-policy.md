# Dictionary Collision Policy

STRING has a deliberately small sound inventory, so lexical collisions are expected during large-scale English-to-STRING normalization.

A collision exists when two unrelated meanings would otherwise receive the same accepted STRING headword.

## Priority order

When a collision occurs:

1. preserve already accepted high-frequency grammar words;
2. prefer the form that stays closer to the most common English pronunciation;
3. use a documented pronunciation variant when that produces a natural legal distinction;
4. preserve another audible source consonant or vowel by adding a legal CV unit;
5. if necessary, shorten one candidate differently during human review.

## Forbidden collision fixes

Never distinguish words only by:

- capitalization;
- stress;
- silent letters;
- an unpronounced spelling difference;
- an illegal consonant cluster;
- adjacent vowels.

## Homophones

Unrelated accepted dictionary entries should not normally be homophones.

Related senses may share one STRING word when the relationship is intentional and documented in one lexical entry. This is polysemy, not an accidental collision.

## Short forms

Very short forms are scarce and valuable. They should preferentially be reserved for:

- pronouns;
- grammatical particles;
- extremely frequent verbs;
- extremely frequent everyday words.

The 50,000-word generator must therefore check candidates against the accepted core vocabulary before assigning them.
