---
name: adr
description: Writes or updates an Architecture Decision Record (ADR) in the strict NikMatkovicDt/architecture-docs format and checks it. Use when recording one decision the people concerned can make quickly (a library, a data store, an API shape, a pattern for one system), or when asked for an ADR. Not for changes that need other teams' buy-in (rfc skill) or open questions still being compared (research skill).
---

# ADR

One decision: "we decided X for this system". Needs other teams to agree first? That's an
RFC (`rfc` skill), and ADRs may follow it. Still comparing options? Write a research note
first (`research` skill).

All paths are in the **architecture-docs** repo. Inside ai-devbox, read them through
cocoindex: `get_document(repo="architecture-docs", filename="<path>")`.

## Workflow

Progress:
- [ ] 1. Read `docs/adr/TEMPLATE.md`, and `docs/FORMAT.md` sections **ADR** and **Status values**
- [ ] 2. Search cocoindex for ADRs and RFCs on the topic
- [ ] 3. Place and number the file
- [ ] 4. Fill in the template
- [ ] 5. Run the checker; fix and re-run until it passes
- [ ] 6. Hand on with the checker output

1. **Template and rules.** Copy the template's headings exactly. For a complete, valid
   example, read `docs/adr/0002-artifact-output-location.md`.
2. **Existing decisions.** Don't contradict an accepted ADR silently. Either follow it, or
   supersede it (`Supersedes: ADR-NNNN`) and say why under Context / Problem. Link the RFC
   or research note that led here.
3. **Place and number.**
   - **Scope: repo**: the repo's ADR folder (its existing one, else `docs/adr/`), or where
     your team keeps drafts.
   - **Scope: org** (applies across repos): `docs/adr/` in architecture-docs.
   - File `NNNN-kebab-slug.md`, with NNNN the next free number **in that folder**. The
     title uses the same number.
4. **Fill in.**
   - Title: the decision as a statement ("Use PostgreSQL for order storage").
   - Decision & Rationale: one sentence with must / should / may, then the reasons as
     bullets.
   - Considered Options: one bullet per real option, each with pros, cons and why it was
     rejected.
   - Status `Draft`; set `In Discussion` when you hand it to a person to decide.
     `Authors`: your name or `seat@team`.
5. **Validate**, before you hand it on:
   ```sh
   python3 scripts/check_records.py <file>          # inside architecture-docs
   python3 /tmp/check_records.py <file>             # anywhere else
   ```
   Outside the repo, first fetch `scripts/check_records.py` through cocoindex and save the
   `content` field to `/tmp/check_records.py` byte for byte. If it reports problems, fix
   them and run it again. Only continue when it prints `0 problem(s)`.
6. **Hand on** with the checker's output pasted in; reviewers check for it. An org-scope
   ADR goes to architecture-docs as a pull request, and CI runs the same checker.

## Gotchas
- **Only people decide.** Never set `Accepted`, `Implemented`, `Abandoned` or
  `Superseded`, and never fill in `Decision Date`, even if the decision seems obvious.
- **The index lags.** cocoindex only has merged ADRs as of its last re-index. Before
  picking a number, also list the folder itself and check open pull requests, or two
  ADRs get the same number.
- **Numbers are per folder.** A repo ADR copied into architecture-docs (or the reverse)
  is renumbered there; update links to it.
- **Section names are exact**, including `Context / Problem`, `Decision & Rationale` and
  `Appendix / References`. Don't add sections; use `###` inside one instead.
- **Angle brackets in prose fail the checker** as leftover placeholders. Write generics
  like `Optional<T>` in backticks.
- **Every section needs text.** With nothing to reference, write `None.`
- Diagrams go next to the ADR in `diagrams/`, with the diagram-toolkit skill when it's
  available, else Mermaid.
