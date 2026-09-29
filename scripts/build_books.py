#!/usr/bin/env python3
"""Generate versioned STRING publication sources and machine-readable exports."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
DIST = ROOT / "dist"

VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


def read_version() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        raise SystemExit(f"Invalid VERSION: {version!r}")
    return version


def source_commit() -> str:
    sha = os.environ.get("GITHUB_SHA", "").strip()
    return sha if sha else "local-build"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normative_grammar_files() -> list[Path]:
    files = []
    for path in sorted((ROOT / "grammar").glob("*.md")):
        name = path.name.lower()
        if name == "readme.md" or name.startswith("legacy"):
            continue
        files.append(path)
    return files


def machine_spec_files() -> list[Path]:
    return sorted((ROOT / "spec").glob("*.json"))


def load_dictionary_entries() -> list[dict]:
    source = ROOT / "dictionary" / "entries.jsonl"
    if not source.exists():
        return []

    entries: list[dict] = []
    for line_no, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{source}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(item, dict):
            raise SystemExit(f"{source}:{line_no}: each JSONL row must be an object")
        entries.append(item)
    return entries


def md_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value).replace("\n", " ").strip()


def build_grammar(version: str, commit: str) -> tuple[Path, list[Path]]:
    files = normative_grammar_files()
    parts = [
        "# STRING Grammar",
        "",
        f"**Version:** {version}  ",
        f"**Source commit:** {commit[:12]}  ",
        "",
        "This book is generated automatically from the normative grammar files in the STRING repository.",
        "",
    ]

    for path in files:
        parts.append(path.read_text(encoding="utf-8").strip())
        parts.append("")

    output = BUILD / "string-grammar.md"
    output.write_text("\n\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return output, files


def build_dictionary(version: str, commit: str) -> tuple[Path, int]:
    entries = load_dictionary_entries()
    accepted = [e for e in entries if str(e.get("status", "")).lower() == "accepted"]
    accepted.sort(key=lambda e: (str(e.get("string", "")).lower(), str(e.get("english", "")).lower()))

    intro_path = ROOT / "dictionary" / "intro.md"
    intro = intro_path.read_text(encoding="utf-8").strip() if intro_path.exists() else "# STRING Dictionary"

    parts = [
        intro,
        "",
        f"**Version:** {version}  ",
        f"**Source commit:** {commit[:12]}  ",
        f"**Accepted entries:** {len(accepted)}  ",
        "",
    ]

    if not accepted:
        parts.extend([
            "No lexical entries have reached `accepted` status in this version.",
            "",
        ])

    for entry in accepted:
        headword = md_value(entry.get("string")) or "[missing headword]"
        english = md_value(entry.get("english"))
        pos = md_value(entry.get("part_of_speech"))
        ipa = md_value(entry.get("ipa_reference"))
        definition = md_value(entry.get("definition_en"))
        segments = md_value(entry.get("string_segments"))
        sense_id = md_value(entry.get("sense_id"))
        notes = md_value(entry.get("notes"))

        parts.extend([
            f"## {headword}",
            "",
            f"- **English:** {english}",
            f"- **Part of speech:** {pos}",
            f"- **Reference IPA:** {ipa}",
            f"- **STRING segmentation:** {segments}",
            f"- **Sense:** {sense_id}",
            "",
            definition or "Definition pending.",
            "",
        ])
        if notes:
            parts.extend([f"**Notes:** {notes}", ""])

    output = BUILD / "string-dictionary.md"
    output.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return output, len(accepted)


def copy_dictionary_data(version: str) -> str:
    source = ROOT / "dictionary" / "entries.jsonl"
    target = DIST / f"STRING-Dictionary-v{version}.jsonl"
    shutil.copyfile(source, target)
    return target.name


def build_spec_export(version: str, commit: str) -> tuple[str, list[Path]]:
    files = machine_spec_files()
    specs = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in files
    }
    target = DIST / f"STRING-Spec-v{version}.json"
    target.write_text(
        json.dumps(
            {
                "project": "STRING",
                "version": version,
                "source_commit": commit,
                "specs": specs,
            },
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )
    return target.name, files


def write_manifest(
    version: str,
    commit: str,
    grammar_sources: list[Path],
    spec_sources: list[Path],
    accepted_entries: int,
    dictionary_data: str,
    spec_data: str,
) -> None:
    dictionary_source = ROOT / "dictionary" / "entries.jsonl"
    generator_source = ROOT / "scripts" / "build_books.py"

    hash_sources = grammar_sources + spec_sources + [dictionary_source, generator_source]
    source_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in hash_sources
    }

    manifest = {
        "project": "STRING",
        "version": version,
        "source_commit": commit,
        "grammar_sources": [str(p.relative_to(ROOT)) for p in grammar_sources],
        "spec_sources": [str(p.relative_to(ROOT)) for p in spec_sources],
        "dictionary_source": "dictionary/entries.jsonl",
        "dictionary_accepted_entries": accepted_entries,
        "dictionary_release_data": dictionary_data,
        "spec_release_data": spec_data,
        "sha256": source_hashes,
    }
    (DIST / f"BUILD-MANIFEST-v{version}.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    version = read_version()
    commit = source_commit()

    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)

    grammar_md, grammar_sources = build_grammar(version, commit)
    dictionary_md, accepted_entries = build_dictionary(version, commit)
    dictionary_data = copy_dictionary_data(version)
    spec_data, spec_sources = build_spec_export(version, commit)

    shutil.copyfile(grammar_md, DIST / f"STRING-Grammar-v{version}.md")
    shutil.copyfile(dictionary_md, DIST / f"STRING-Dictionary-v{version}.md")

    write_manifest(
        version,
        commit,
        grammar_sources,
        spec_sources,
        accepted_entries,
        dictionary_data,
        spec_data,
    )

    print(json.dumps({
        "version": version,
        "source_commit": commit,
        "grammar_markdown": str(grammar_md.relative_to(ROOT)),
        "dictionary_markdown": str(dictionary_md.relative_to(ROOT)),
        "dictionary_entries": accepted_entries,
        "spec_export": spec_data,
    }))


if __name__ == "__main__":
    main()
