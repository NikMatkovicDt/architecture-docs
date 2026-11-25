---
name: rfc
description: Writes a Request for Comments (RFC) in the strict NikMatkovicDt/architecture-docs format, checks it and opens it as a pull request collecting feedback. Use when a change needs buy-in from other teams or everyone - a practice all teams should follow, a cross-team architecture change - or when asked for an RFC. Not for a decision the people concerned can make themselves (adr skill) or for researching options (research skill).
---

# RFC

Drives a change that needs others to agree. It collects feedback until a deadline and
applies only once a person accepts it. An accepted RFC can lead to ADRs (`adr` skill). A
decision the people concerned can make quickly themselves is an ADR from the start.

**Who:** in an agent team, only the **architect** writes RFCs; other seats suggest one to
the architect. A person may write one directly.

All paths are in the **architecture-docs** repo. Inside ai-devbox, read them through
cocoindex: `get_document(repo="architecture-docs", filename="<path>")`.

## Workflow

Progress:
- [ ] 1. Read `docs/rfcs/TEMPLATE.md`, and `docs/FORMAT.md` sections **RFC** and **Status values**
- [ ] 2. Search cocoindex for RFCs and ADRs on the topic
- [ ] 3. Place and number the file
- [ ] 4. Fill in the template
- [ ] 5. Run the checker; fix and re-run until it passes
- [ ] 6. Open the pull request and set Collecting Feedback

1. **Template and rules.** Copy the template's headings exactly. For a complete, valid
   example, read `docs/rfcs/0004-dotnet-good-practices.md`.
2. **Existing RFCs.** Extend or reference an existing RFC rather than writing a competing
   one.
3. **Place and number.** `docs/rfcs/` in architecture-docs, file `NNNN-kebab-slug.md`, with
   NNNN the next free number there. The title uses the same number.
4. **Fill in.**
   - Title: the change ("Every service exposes a health endpoint").
   - Need: why, with real examples (incidents, review findings).
   - Approach: must / should / may, each rule checkable in a review.
   - Pros & Cons: the approach's own, factual.
   - Alternatives: **at least two**, one bullet each, with pros, cons and why not chosen.
   - Status `Draft`, `Authors` your name or `seat@team`, `Last Update` today.
5. **Validate**, before opening the pull request:
   ```sh
   python3 scripts/check_records.py <file>          # inside architecture-docs
   python3 /tmp/check_records.py <file>             # anywhere else
   ```
   Outside the repo, first fetch `scripts/check_records.py` through cocoindex and save the
   `content` field to `/tmp/check_records.py` byte for byte. If it reports problems, fix
   them and run it again. Only continue when it prints `0 problem(s)`.
6. **Open the pull request.** Set `Collecting Feedback` with `Feedback Deadline` two weeks
   from today (unless told otherwise), re-run the checker, and open the PR to
   architecture-docs. Paste the checker output into your handoff and tell the PM it's open.

## Gotchas
- **Never merge it, never accept it.** Accepted RFCs become review context (PR-Agent) for
  every repo, so only a person sets `Accepted`, `Rejected` or `Abandoned`.
- **`Collecting Feedback` needs `Feedback Deadline`.** The checker fails without it.
- **One alternative isn't enough.** The checker counts `- ` bullets (or `###`
  subsections) under Alternatives and needs two.
- **The index lags.** cocoindex only has merged RFCs. Check open pull requests on
  architecture-docs before picking a number.
- **Section names are exact**: `Need`, not Motivation; `Approach`, not Proposed rules;
  `Pros & Cons`. Angle brackets in prose fail the checker, so write generics like
  `List<T>` in backticks.
