# Changelog

All released versions of STRING are tracked here.

The canonical version is stored in `VERSION`. A release is built entirely from the repository sources at the commit associated with that version.

## 0.8.0-dev

Current development cycle after stable `v0.7.0`:

- define one canonical noun-phrase order: selector → possessor → quantity → modifier(s) → noun → relative clause;
- define one canonical predicate/operator order for tense, modality, perfect, progressive, lexical verb, object, and relational phrases;
- clarify negation scope by placing `not` immediately before the predicate element it negates;
- distinguish the external project name **STRING** from canonical in-language lexical forms;
- add focused collision and pronunciation review queues to dictionary candidate artifacts;
- add a dedicated full dictionary-generation workflow;
- request the first full 50,000-lemma candidate analysis;
- introduce explicit development versions such as `0.8.0-dev`;
- restrict GitHub tags and Releases to stable `X.Y.Z` versions only.

## 0.7.0

Expand everyday reference and make verb participant roles explicit:

- add `tin` for thing and `yuman` for human/person;
- add `heni` for any, `hic` for each/every, `bot` for both, and `sem` for same;
- build someone/anyone/nobody/everyone compositionally from existing quantifiers plus `yuman`;
- build something/anything/nothing/everything compositionally from existing quantifiers plus `tin`;
- use `wan hader + NOUN` for another rather than adding a special article;
- use `wat + NOUN` for ordinary what/which selection;
- derive whose from the existing possessor pattern `hu + NOUN`;
- derive how many as `ha meni + NOUN`;
- add explicit direct-object and relational-complement ordering;
- require recipient/destination `tu` instead of English-style double-object grammar;
- clarify that `tu` is a real relation word and never an automatic infinitive marker;
- add invariant core verb `giv`;
- expand automated phonological tests for the new core vocabulary;
- expand the accepted core dictionary to 90 entries.

## 0.6.0

Make STRING easier to learn and make the 50,000-word pipeline sense-aware:

- add a deliberately redundant core sentence-pattern reference covering the main grammar in one chapter;
- add a regular invariant modal system for ability, possibility, need, necessity, advice, and intention;
- add accepted `me`, `mas`, `xud`, and `won`;
- define modal negation scope with ordinary `not` placement instead of negative modal forms;
- integrate Open English WordNet 2025 as the lemma/sense inventory for candidate generation;
- pin `wn==1.1.1` and the CI-available `wordfreq==3.1.1`;
- continue using the pinned upstream CMU Pronouncing Dictionary revision for US-English pronunciation;
- generate one review candidate per English lemma, carrying all WordNet parts of speech and senses;
- rank lemmas by frequency while flagging spellings whose score is contaminated by use as an inflected form of another lemma;
- classify already accepted core lemmas separately from true lexical collisions;
- exclude resolved core lemmas from new-candidate collision statistics;
- add a documented proposed → reviewed → accepted dictionary review process;
- keep the full 50,000-candidate run manual and non-normative, with an automatic 100-lemma smoke test when the generator changes;
- verify the latest 100-lemma smoke test with 100 pronunciation candidates, zero unsupported pronunciations, six true core collisions, and zero collisions among unresolved new candidates;
- expand the accepted core dictionary to 83 entries.

## 0.5.0

Add compact reference grammar and universal structured time notation:

- add `hir` and `der` for here/there;
- define regular existential clauses with `der bi ...`;
- reuse normal negation and question inversion for existential clauses;
- add `selaf` and build all reflexive forms compositionally from ordinary pronouns;
- add `hader` and `wan hader` for other and reciprocal reference;
- allow `de` as a generic human/agentive "they" where this avoids unnecessary passive morphology;
- keep declarative subjects explicit except in commands and clear same-subject coordination;
- define ISO-style `det YYYY-MM-DD` dates;
- define 24-hour `tam HH:MM[:SS]` clock notation;
- add machine-readable `spec/datetime.json`;
- add deterministic date/time reading with calendar-value validation;
- expand the accepted core dictionary to 79 entries.

## 0.4.0

Extend STRING into a more complete usable language and prepare large-scale lexical generation:

- add a canonical digit-by-digit decimal number system;
- add spoken forms for digits 0–9, decimal point, and negative sign;
- add a deterministic numeric reader and machine-readable `spec/numbers.json`;
- define punctuation, capitalization, proper-name adaptation, external identifiers, and transparent compounds;
- define direct and negative commands without special verb morphology;
- add optional politeness marker `piliz`;
- extend `dat` as a content-clause and relative-clause linker;
- define regular conditional, reason, result, and coordinated complex clauses;
- define word classes without mandatory grammatical endings;
- explicitly reject automatic import of English inflectional and derivational suffixes;
- prefer transparent composition before lexical derivation;
- expand the accepted core dictionary to 73 entries;
- export a versioned machine-readable STRING specification in releases;
- define reproducible lexical source policy for frequency, pronunciation, and senses;
- add a manual candidate-generation workflow targeting 50,000 English frequency candidates;
- pin wordfreq 3.2.0 for frequency prioritization;
- pin the upstream CMU Pronouncing Dictionary source revision used by the candidate generator;
- keep generated candidates non-normative until explicit review and promotion.

## 0.3.0

Expand the minimal grammar beyond the core clause:

- add invariant modifier rules;
- add explicit quantifiers without noun plural inflection;
- replace comparative and superlative endings with `mor`, `les`, `mos`, and `lis`;
- add `dan` for explicit comparison targets;
- define a deliberately small core preposition inventory;
- use `not` compositionally instead of creating separate negative prepositions;
- prefer compositional complex relations over a large memorized preposition list;
- add temporal relations using the same invariant relation grammar;
- add core conjunctions for coordination, conditions, reasons, and results;
- add accepted dictionary entries for the new grammar vocabulary;
- update the generated grammar book and searchable dictionary automatically.

## 0.2.0

First executable language standard:

- define the five-vowel working standard;
- define the one-symbol/one-sound consonant inventory;
- add machine-readable `spec/phonology.json`;
- add deterministic English IPA → STRING candidate generation;
- define vowel-initial, hiatus, and consonant-cluster repair;
- confirm a five-form personal pronoun system;
- remove grammatical gender from the core grammar;
- remove noun plural inflection and obligatory articles;
- define invariant verbs;
- define regular past, future, and conditional words: `did`, `wil`, `wud`;
- define regular progressive and perfect constructions with `bi` and `hav`;
- confirm explicit `not` negation;
- confirm regular predicate–subject question inversion;
- add six core question words;
- add the first 30 accepted dictionary entries;
- add collision policy for large-scale dictionary generation;
- add source validation and phonology unit tests;
- include source SHA-256 hashes in generated build manifests;
- add a generated static GitHub Pages site with searchable dictionary;
- keep PDF, EPUB, website, and machine-readable outputs generated from one source.

## 0.1.0

Initial project structure:

- core design principles;
- English-pronunciation-first lexical policy;
- initial phonotactic rules;
- initial core grammar;
- dictionary data model;
- LLM prompt;
- automated book and release pipeline.
