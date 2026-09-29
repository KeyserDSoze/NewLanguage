# Changelog

All released versions of STRING are tracked here.

The canonical version is stored in `VERSION`. A release is built entirely from the repository sources at the commit associated with that version.

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
