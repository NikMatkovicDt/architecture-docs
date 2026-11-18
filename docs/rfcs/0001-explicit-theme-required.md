# RFC-0001: Every rendered diagram must declare an explicit theme

- **Status:** Collecting Feedback
- **Authors:** Nikola Matkovic
- **Feedback Deadline:** 2026-12-02
- **Last Update:** 2026-11-18

## Summary

Diagram rendering tools support multiple visual themes (e.g. `studio`, `technical`,
`dark`). This RFC proposes that every render/export call site — CLI invocation,
library call, or automated script — must pass an explicit `theme` argument rather than
relying on an implicit default.

## Need

Relying on a silent default theme has caused confusion when diagrams intended for a
client presentation were generated with the `technical` theme (or vice versa) because
a script omitted the `--theme` flag. Explicit is better than implicit for anything that
ends up in front of a client or in a slide deck.

## Approach

- Any `render` call (CLI: `python -m diagram_toolkit render ...`, library:
  `render(type, data, theme)`) must pass `theme` explicitly. Omitting it should be
  treated as a review finding, not silently accepted.
- CI/example scripts and documentation snippets should always show the theme argument,
  so copy-pasted examples don't propagate the omission.
- If a genuine "use the default theme" use case exists, it must be written as
  `theme="studio"` explicitly, not omitted.

## Pros & Cons

Not recorded when this RFC was written.

## Alternatives

- Keep relying on the default theme. Rejected: silent defaults are exactly the kind of
  thing that leads to inconsistent output being merged and only caught by a human at
  presentation time.
- **Not recorded.** A second alternative wasn't written down when this RFC was
  drafted; add one before it's accepted.

## Appendix / References

- Once accepted, this RFC may be promoted to an ADR.
- [diagram-toolkit](https://github.com/NikMatkovicDt/diagram-toolkit), where this applies first.
