# ADR-0001: Validate diagram JSON against schema before rendering

- **Status:** Accepted
- **Authors:** Nikola Matkovic
- **Decision Date:** 2026-11-18
- **Scope:** org

## Context / Problem

Diagram-generation tools (such as diagram-toolkit) accept a JSON payload describing
nodes, edges, and metadata, then render it into a diagram format (e.g. D2, Mermaid).
Malformed or incomplete JSON that reaches the renderer without validation can produce
confusing runtime errors, partially-rendered diagrams, or silently wrong output.

## Decision & Rationale

Any code path that accepts diagram JSON (from a file, stdin, or an API/CLI argument)
**must validate that JSON against its published schema before passing it to a
renderer**. Validation must run first, and rendering must not be attempted on
unvalidated input, even for "trusted" internal callers.

Concretely:

- Every new diagram type or renderer must expose a `schema` command/function that
  returns its JSON schema.
- Every new diagram type or renderer must expose (or reuse) a `validate` step, and all
  render entry points must call it before rendering.
- CLI commands that skip validation (e.g. a `--force` or `--skip-validation` flag) must
  default to `false`/off, and must not be used in CI or automated pipelines.

## Consequences

- Slightly more upfront work when adding a new diagram type (schema + validation must
  ship together).
- Rendering failures surface as clear, actionable schema validation errors instead of
  opaque renderer stack traces.
- Reviewers should flag any PR that adds or modifies a render/export code path without
  a corresponding validation call.

## Considered Options

- Not recorded when this ADR was accepted.

## Appendix / References

- [diagram-toolkit](https://github.com/NikMatkovicDt/diagram-toolkit), where this applies first.
