---
name: rfc
description: Propose an org-wide rule or practice every team should follow (an RFC) in the strict format of NikMatkovicDt/architecture-docs, as a pull request with status Proposed. Not for a single decision about one system (that's the adr skill) or for researching options (that's the research skill).
---

# RFC

An RFC proposes **a rule for every team**: "everyone should do X from now on". It applies
only once a person accepts it. If it's one decision for one system, write an ADR (`adr`
skill) instead.

**Who:** in an agent team, only the **architect** writes RFCs. Other seats suggest one to
the architect. A person may write one directly.

Everything below lives in the **architecture-docs** repo. Inside ai-devbox, read it through
cocoindex: `get_document(repo="architecture-docs", filename="<path>")`.

## Steps
1. **Read the rules:** `docs/FORMAT.md` and the template `docs/rfcs/TEMPLATE.md`. Follow
   them exactly; don't add or rename sections.
2. **Check what exists:** search cocoindex for RFCs and ADRs on the topic. Extend or
   reference an existing RFC rather than writing a competing one.
3. **Place and number it:** `docs/rfcs/` in architecture-docs, the next free number there,
   `NNNN-kebab-slug.md`, with the same number in the title.
4. **Write it:**
   - Title: the rule ("Every service exposes a health endpoint").
   - Summary: what changes for teams.
   - Motivation: the problem, with evidence (incidents, review findings).
   - Proposed rules: must / should / may, each checkable in a review, each with its
     reason.
   - Alternatives considered: each real option and why it lost.
   - Related: or `None.`
5. **Status:** you write `Proposed` (or `Draft` while it's unfinished). An agent never
   sets `Accepted`, `Rejected` or `Withdrawn`. `Date` is today; `Author` is your name or
   `seat@team`.
6. **Check it:** run `scripts/check_records.py` on the file. Outside the repo, fetch it
   from cocoindex, save it as `/tmp/check_records.py` exactly, and run
   `python3 /tmp/check_records.py <file>`. Fix every problem, and paste the clean output
   into your handoff (reviewers check for it).
7. **Open a pull request** to architecture-docs with status `Proposed`, and never merge it
   yourself. Accepted RFCs become review context for every repo, so a person decides.
