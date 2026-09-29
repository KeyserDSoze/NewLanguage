# Static Site

This directory is reserved for the public STRING website.

The site will be published through GitHub Pages and will expose the same canonical sources used for the books and machine-readable dictionary.

## Planned sections

- project introduction;
- complete grammar;
- pronunciation guide;
- searchable dictionary;
- English → STRING lookup;
- STRING → English lookup;
- entry pages showing English lemma, IPA source pronunciation, STRING form, part of speech, definition, and status;
- downloadable PDF and EPUB editions.

## Search architecture

The dictionary should remain usable as a static website.

A build step will generate a compact client-side search index from the canonical dictionary data. No server is required for normal lookup.

## Single-source principle

Grammar, website, PDF, EPUB, and machine-readable exports must be generated from shared source files so that the project cannot drift into multiple incompatible versions.
