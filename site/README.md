# STRING Static Site

The public website is generated from the same canonical sources as the books and dictionary exports.

Nothing inside the generated `public/` directory is maintained manually.

## Generator

```text
scripts/build_site.py
```

It reads:

- `VERSION`;
- accepted entries from `dictionary/entries.jsonl`;
- generated grammar source assembled by `scripts/build_books.py`.

Pandoc renders the assembled grammar to HTML.

## Published sections

- project introduction;
- full generated grammar;
- searchable accepted dictionary;
- links to versioned GitHub Releases;
- links back to the source repository.

Dictionary search runs entirely in the browser and requires no server.

## GitHub Pages

`.github/workflows/pages.yml` rebuilds and deploys the site from `main` when language sources change.

The deployment uses the official GitHub Pages Actions flow:

- `actions/checkout@v6`;
- `actions/configure-pages@v5`;
- `actions/upload-pages-artifact@v4`;
- `actions/deploy-pages@v4`.

The repository must have GitHub Pages configured to use **GitHub Actions** as its publishing source.
