---
name: rfc
description: Write a Request for Comments (RFC) - a proposed change that needs buy-in from other teams or everyone (a practice all teams follow, a cross-team architecture change) - in the strict format of NikMatkovicDt/architecture-docs, as a pull request collecting feedback until a deadline. Not for a decision the people concerned can make quickly themselves (that's the adr skill) or for researching options (that's the research skill).
---

# RFC

An RFC **drives a change that needs others to agree**: other teams, or everyone. It
collects feedback until a deadline, and applies only once a person accepts it. An accepted
RFC can then lead to one or more ADRs (`adr` skill) recording how it's carried out. A
decision the people concerned can make quickly themselves is an ADR from the start.

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
   - Title: the change ("Every service exposes a health endpoint").
   - Summary: two to four sentences on what changes and for whom.
   - Need: why, with examples (incidents, review findings).
   - Approach: how, with must / should / may, each rule checkable in a review.
   - Pros & Cons: the approach's factual benefits and drawbacks.
   - Alternatives: **at least two**, one bullet each, with pros, cons and why not
     chosen.
   - Appendix / References: or `None.`
5. **Status:**
   - You write `Draft`. When you open the pull request, set `Collecting Feedback` with a
     `Feedback Deadline` two weeks out (unless told otherwise), and update `Last Update`.
   - You never set `Accepted`, `Rejected` or `Abandoned`.
   - `Authors`: your name or `seat@team`.
6. **Check it:** run `scripts/check_records.py` on the file. Outside the repo, fetch it
   from cocoindex, save it as `/tmp/check_records.py` exactly, and run
   `python3 /tmp/check_records.py <file>`. Fix every problem, and paste the clean output
   into your handoff (reviewers check for it).
7. **Open a pull request** to architecture-docs and never merge it yourself. Accepted
   RFCs become review context for every repo, so a person decides.
