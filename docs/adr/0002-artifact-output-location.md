# ADR-0002: Exported diagram artifacts must live under `artifacts/`

## Status

Accepted

## Context

diagram-toolkit exports rendered diagrams to SVG, PNG, and PDF via the `export`
command. Output paths are currently caller-supplied, and inconsistent output locations
have made it hard to find, clean up, and gitignore generated files across the
repository (some ended up under `test_result/`, some in the repo root, some in
ad-hoc temp folders).

## Decision

All generated diagram artifacts (SVG/PNG/PDF exports, rendered `.d2` files intended as
build output rather than source) **must be written under a top-level `artifacts/`
directory**, using a path structure of `artifacts/<diagram-name>/<file>`.

- Example commands and documentation should default to `--output artifacts/...`.
- `artifacts/` must be listed in `.gitignore` — generated output is not committed.
- One-off exploratory scripts and CI jobs must not write generated diagrams to the
  repository root, `test_result/`, or any other ad-hoc location.

## Consequences

- Easier repo hygiene: a single directory to gitignore and clean.
- Predictable location for CI to pick up artifacts for upload as build outputs.
- Reviewers should flag any PR whose export/output path does not resolve under
  `artifacts/`.
