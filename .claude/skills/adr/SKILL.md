---
name: adr
description: Write or update an Architecture Decision Record (ADR) - one decision that can be made and carried out quickly by the people it concerns, with rationale, consequences and the options weighed - in the strict format of NikMatkovicDt/architecture-docs. Not for a change that needs buy-in from other teams (that's the rfc skill) or for answering an open question (that's the research skill).
---

# ADR

An ADR records **one decision**: "we decided X for this system". If the change needs
other teams to agree first, it's an RFC (`rfc` skill); an accepted RFC can then lead to
ADRs. If you're still comparing options, write a research note first (`research` skill).

Everything below lives in the **architecture-docs** repo. Inside ai-devbox, read it through
cocoindex: `get_document(repo="architecture-docs", filename="<path>")`.

## Steps
1. **Read the rules:** `docs/FORMAT.md` (layout, statuses, numbering) and the template
   `docs/adr/TEMPLATE.md`. Follow them exactly; don't add or rename sections.
2. **Check what exists:** search cocoindex for ADRs and RFCs on the topic. A new ADR must
   not contradict an accepted one silently. Either follow it, or supersede it
   (`Supersedes: ADR-NNNN`) and say why under Context / Problem. If an RFC led to this
   decision, link it.
3. **Place and number it:**
   - **Scope: repo**: the repo's ADR folder (its existing one, else `docs/adr/`), or
     wherever your team's process keeps drafts.
   - **Scope: org** (applies across repos): `docs/adr/` in architecture-docs.
   - The number is the next free one **in that folder**. Name the file
     `NNNN-kebab-slug.md`, with the same number in the title.
4. **Write it:**
   - Title: the decision as a statement ("Use PostgreSQL for order storage", not
     "Database choice").
   - Context / Problem: the problem and what drives it, not the solution.
   - Decision & Rationale: **one sentence** of decision (must / should / may), then the
     reasons as bullets.
   - Consequences: good and bad, including second-order effects.
   - Considered Options: each real option, one bullet each, with **pros, cons and why
     it was rejected**.
   - Appendix / References: the RFC, research notes and ADRs it builds on, or `None.`
5. **Status:**
   - You write `Draft`, and set `In Discussion` when you hand it to a person to decide.
   - You never set `Accepted`, `Implemented`, `Abandoned` or `Superseded`, and never fill
     in `Decision Date`; a person does.
   - `Authors`: your name or `seat@team`.
6. **Check it:** run `scripts/check_records.py` on the file. Outside the repo, fetch it
   from cocoindex, save it as `/tmp/check_records.py` exactly, and run
   `python3 /tmp/check_records.py <file>`. Fix every problem, and paste the clean output
   into your handoff (reviewers check for it).
7. **Diagrams:** next to the ADR in `diagrams/`, with the diagram-toolkit skill when
   available, else Mermaid.

An org-scope ADR reaches architecture-docs as a pull request. CI there runs the same
checker.
