#!/usr/bin/env python3
"""Build the static STRING documentation and searchable dictionary site."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def load_entries() -> list[dict]:
    path = ROOT / "dictionary" / "entries.jsonl"
    entries: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            item = json.loads(raw)
            if item.get("status") == "accepted":
                entries.append(item)
    entries.sort(key=lambda e: (e.get("string", ""), e.get("english", "")))
    return entries


def page(title: str, body: str, version: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="STRING universal language documentation">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="index.html">STRING</a>
    <nav>
      <a href="grammar.html">Grammar</a>
      <a href="dictionary.html">Dictionary</a>
      <a href="https://github.com/KeyserDSoze/NewLanguage/releases/latest">Releases</a>
      <a href="https://github.com/KeyserDSoze/NewLanguage">GitHub</a>
    </nav>
  </header>
  <main>
    {body}
  </main>
  <footer>STRING v{html.escape(version)} · generated from the repository</footer>
</body>
</html>
"""


def build_index(version: str, count: int) -> None:
    body = f"""
<section class="hero">
  <p class="eyebrow">Universal · phonemic · regular</p>
  <h1>STRING</h1>
  <p class="lead">A language designed to be written exactly as it is pronounced, with simple grammar and vocabulary derived primarily from recognizable English pronunciation.</p>
  <div class="actions">
    <a class="button" href="grammar.html">Read the grammar</a>
    <a class="button secondary" href="dictionary.html">Search the dictionary</a>
  </div>
</section>

<section class="grid">
  <article class="card">
    <h2>One spelling, one sound</h2>
    <p>No silent letters, no contextual pronunciation rules, no hidden spelling exceptions.</p>
  </article>
  <article class="card">
    <h2>Small grammar</h2>
    <p>Invariant verbs, no grammatical gender, no noun plural inflection, and explicit regular particles.</p>
  </article>
  <article class="card">
    <h2>English sound as the lexical anchor</h2>
    <p>IPA is used internally to normalize English pronunciation into legal STRING words.</p>
  </article>
</section>

<section class="stats">
  <div><strong>{count}</strong><span>accepted dictionary entries</span></div>
  <div><strong>5</strong><span>vowels</span></div>
  <div><strong>(CV)+C?</strong><span>canonical word shape</span></div>
</section>

<section>
  <h2>Single-source publication</h2>
  <p>The grammar book, dictionary book, this website, machine-readable data, and release artifacts are generated from the same versioned repository sources.</p>
</section>
"""
    (PUBLIC / "index.html").write_text(page("STRING", body, version), encoding="utf-8")


def build_dictionary(version: str, entries: list[dict]) -> None:
    data_dir = PUBLIC / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    export = [
        {
            "string": e.get("string"),
            "english": e.get("english"),
            "part_of_speech": e.get("part_of_speech"),
            "definition_en": e.get("definition_en"),
            "ipa_reference": e.get("ipa_reference"),
            "string_segments": e.get("string_segments"),
            "sense_id": e.get("sense_id"),
            "notes": e.get("notes", ""),
        }
        for e in entries
    ]
    (data_dir / "dictionary.json").write_text(
        json.dumps(export, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    body = f"""
<section class="page-head">
  <p class="eyebrow">STRING Dictionary</p>
  <h1>Search {len(entries)} accepted words</h1>
  <p>Search by STRING spelling, English source, meaning, or part of speech.</p>
</section>

<section class="search-panel">
  <label for="search">Dictionary search</label>
  <input id="search" type="search" autocomplete="off" placeholder="Try: go, book, question, pronoun…">
  <p id="result-count" class="muted"></p>
</section>

<div id="dictionary-results" class="dictionary-results" aria-live="polite"></div>
<script src="assets/search.js"></script>
"""
    (PUBLIC / "dictionary.html").write_text(
        page("STRING Dictionary", body, version),
        encoding="utf-8",
    )


def write_assets() -> None:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    css = """
:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #171717;
  background: #fafafa;
  line-height: 1.6;
}
* { box-sizing: border-box; }
body { margin: 0; }
a { color: inherit; }
.topbar {
  position: sticky; top: 0; z-index: 10;
  display: flex; justify-content: space-between; align-items: center;
  gap: 2rem; padding: 1rem max(1.25rem, calc((100vw - 1080px) / 2));
  background: rgba(250,250,250,.94); border-bottom: 1px solid #e5e5e5;
  backdrop-filter: blur(12px);
}
.brand { font-weight: 850; letter-spacing: .08em; text-decoration: none; }
nav { display: flex; gap: 1rem; flex-wrap: wrap; }
nav a { text-decoration: none; color: #525252; }
main { max-width: 1080px; margin: 0 auto; padding: 4rem 1.25rem 6rem; }
.hero { max-width: 800px; padding: 4rem 0 3rem; }
h1 { font-size: clamp(3rem, 10vw, 7rem); line-height: .95; margin: .2rem 0 1.5rem; letter-spacing: -.06em; }
h2 { margin-top: 2.4rem; }
.lead { font-size: 1.35rem; color: #404040; max-width: 720px; }
.eyebrow { text-transform: uppercase; letter-spacing: .16em; font-size: .76rem; font-weight: 750; color: #737373; }
.actions { display: flex; gap: .75rem; flex-wrap: wrap; margin-top: 2rem; }
.button { display: inline-block; padding: .78rem 1rem; border: 1px solid #171717; background: #171717; color: white; text-decoration: none; border-radius: .55rem; font-weight: 700; }
.button.secondary { color: #171717; background: transparent; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0; }
.card { padding: 1.4rem; border: 1px solid #e5e5e5; border-radius: .8rem; background: white; }
.card h2 { margin-top: 0; font-size: 1.15rem; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 3rem 0; }
.stats div { padding: 1rem 0; border-top: 2px solid #171717; }
.stats strong, .stats span { display: block; }
.stats strong { font-size: 1.4rem; }
.stats span, .muted { color: #737373; }
.page-head { max-width: 760px; }
.page-head h1 { font-size: clamp(2.5rem, 7vw, 5rem); }
.search-panel { margin: 2rem 0; }
.search-panel label { display: block; font-weight: 700; margin-bottom: .5rem; }
.search-panel input { width: 100%; padding: 1rem; font: inherit; border: 1px solid #a3a3a3; border-radius: .6rem; background: white; }
.dictionary-results { display: grid; gap: .75rem; }
.entry { padding: 1.1rem 1.25rem; background: white; border: 1px solid #e5e5e5; border-radius: .7rem; }
.entry-head { display: flex; align-items: baseline; gap: .8rem; flex-wrap: wrap; }
.entry-word { font-size: 1.45rem; font-weight: 850; }
.entry-english { color: #525252; }
.entry-meta { color: #737373; font-size: .9rem; }
.entry p { margin-bottom: 0; }
footer { max-width: 1080px; margin: 0 auto; padding: 2rem 1.25rem; color: #737373; border-top: 1px solid #e5e5e5; }
main table { border-collapse: collapse; width: 100%; }
main th, main td { border-bottom: 1px solid #e5e5e5; padding: .6rem; text-align: left; }
main code { background: #f0f0f0; padding: .1rem .3rem; border-radius: .25rem; }
main pre { overflow-x: auto; padding: 1rem; background: #f0f0f0; border-radius: .5rem; }
@media (max-width: 760px) {
  .topbar { align-items: flex-start; flex-direction: column; gap: .5rem; }
  .grid, .stats { grid-template-columns: 1fr; }
  main { padding-top: 2rem; }
}
"""
    (assets / "style.css").write_text(css.strip() + "\n", encoding="utf-8")

    js = """
const input = document.querySelector("#search");
const container = document.querySelector("#dictionary-results");
const count = document.querySelector("#result-count");
let entries = [];

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[ch]);
}

function render() {
  const q = input.value.trim().toLowerCase();
  const matches = entries.filter(entry => {
    if (!q) return true;
    return [
      entry.string,
      entry.english,
      entry.part_of_speech,
      entry.definition_en,
      entry.sense_id,
      entry.ipa_reference
    ].some(value => String(value ?? "").toLowerCase().includes(q));
  });

  count.textContent = matches.length + " result" + (matches.length === 1 ? "" : "s");
  container.innerHTML = matches.slice(0, 200).map(entry =>
    '<article class="entry">' +
      '<div class="entry-head">' +
        '<span class="entry-word">' + escapeHtml(entry.string) + '</span>' +
        '<span class="entry-english">' + escapeHtml(entry.english) + '</span>' +
      '</div>' +
      '<div class="entry-meta">' +
        escapeHtml(entry.part_of_speech) + ' · ' +
        escapeHtml(entry.ipa_reference) + ' · ' +
        escapeHtml(entry.string_segments) +
      '</div>' +
      '<p>' + escapeHtml(entry.definition_en) + '</p>' +
    '</article>'
  ).join("");

  if (matches.length > 200) {
    container.insertAdjacentHTML("beforeend", '<p class="muted">Showing the first 200 matches. Refine the search to narrow the results.</p>');
  }
}

fetch("data/dictionary.json")
  .then(response => {
    if (!response.ok) throw new Error("HTTP " + response.status);
    return response.json();
  })
  .then(data => {
    entries = data;
    render();
    input.addEventListener("input", render);
  })
  .catch(error => {
    count.textContent = "Dictionary could not be loaded.";
    console.error(error);
  });
"""
    (assets / "search.js").write_text(js.strip() + "\n", encoding="utf-8")


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    PUBLIC.mkdir(parents=True, exist_ok=True)
    write_assets()
    entries = load_entries()
    build_index(version, len(entries))
    build_dictionary(version, entries)
    (PUBLIC / ".nojekyll").write_text("", encoding="utf-8")
    print(json.dumps({"version": version, "accepted_entries": len(entries), "output": "public"}))


if __name__ == "__main__":
    main()
