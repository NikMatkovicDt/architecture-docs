---
name: adr
description: Write or update an Architecture Decision Record (ADR) - one decision made or proposed for a system, with context, alternatives and consequences - in the strict format of NikMatkovicDt/architecture-docs. Not for org-wide rules every team must follow (that's the rfc skill) or for answering an open question (that's the research skill).
---

# ADR

An ADR records **one decision**: "we decided X for this system". If it reads as
"everyone should do X from now on", it's an RFC (`rfc` skill). If the decision isn't
made yet and you're still comparing options, write a research note first (`research`
skill) and propose the ADR from it.

Everything below lives in the **architecture-docs** repo. Inside ai-devbox, read it through
cocoindex: `get_document(repo="architecture-docs", filename="<path>")`.

## Steps
1. **Read the rules:** `docs/FORMAT.md` (layout, statuses, numbering) and the template
   `docs/adr/TEMPLATE.md`. Follow them exactly; don't add or rename sections.
2. **Check what exists:** search cocoindex for ADRs and RFCs on the topic. A new ADR must
   not contradict an accepted one silently. Either follow it, or supersede it
   (`Supersedes: ADR-NNNN`) and say why in Context.
3. **Place and number it:**
   - **Scope: org** (applies across repos): `docs/adr/` in architecture-docs.
   - **Scope: repo**: that repo's ADR folder (its existing one, else `docs/adr/`), or
     wherever your team's process keeps drafts.
   - The number is the next free one **in that folder**. Name the file
     `NNNN-kebab-slug.md`, with the same number in the title.
4. **Write it:**
   - Title: the decision as a statement ("Use PostgreSQL for order storage", not
     "Database choice").
   - Context: the problem, not the solution.
   - Decision: must / should / may, checkable in a review.
   - Alternatives considered: every real option and why it lost.
   - Consequences: good and bad.
   - Related: research notes, RFCs and ADRs it builds on, or `None.`
5. **Status:** you write `Proposed`. Only a person sets `Accepted`, `Rejected`,
   `Deprecated` or `Superseded`. `Date` is today; `Author` is your name or `seat@team`.
6. **Check it:** run `scripts/check_records.py` on the file. Outside the repo, fetch it
   from cocoindex, save it as `/tmp/check_records.py` exactly, and run
   `python3 /tmp/check_records.py <file>`. Fix every problem, and paste the clean output
   into your handoff (reviewers check for it).
7. **Diagrams:** next to the ADR in `diagrams/`, with the diagram-toolkit skill when
   available, else Mermaid.

An org-scope ADR reaches architecture-docs as a pull request. CI there runs the same
checker.
