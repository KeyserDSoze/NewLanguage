# Machine-readable STRING specification

This directory contains the parts of STRING that must be consumed by tools as well as humans.

The Markdown grammar is the human explanation. Files in `spec/` are the machine-readable counterpart used by validators, dictionary generators, the website, and publishing jobs.

## Current files

- `phonology.json` — alphabet, sound values, IPA normalization, and phonotactic repair rules.

A build must fail when canonical dictionary data violates the current machine-readable specification.
