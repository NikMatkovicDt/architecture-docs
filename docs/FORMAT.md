# Record format

The rules every ADR, RFC and research note follows, whoever writes it: a person, their
own Claude, or an agent team. `scripts/check_records.py` checks them, and CI runs it on
every pull request. The ADR and RFC layouts follow Candost Dagdeviren's
[ADRs and RFCs: their differences and when to use which](https://candost.blog/adrs-rfcs-differences-when-which/),
with a few local changes listed at the end.

## Which record

| Record | Use it for | Lives in |
|---|---|---|
| **RFC** (Request for Comments) | **driving a change that needs buy-in from others**: other teams, or everyone (a practice every team follows, a cross-team architecture change). Collects feedback, often over days | `docs/rfcs/` here |
| **ADR** (Architecture Decision Record) | **recording one decision that can be made and executed quickly** by the people it concerns, with its rationale, consequences and the options weighed | the repo's own ADR folder (its existing one, else `docs/adr/`) for **Scope: repo**; `docs/adr/` here for **Scope: org**, a decision that applies across repos |
| **Research note** | **answering a question with evidence**: options compared, a recommendation and its confidence. Often the input to an RFC or ADR | next to the work that asked the question, usually `docs/research/` |

The test:
- *"We need others to agree before this changes"* is an RFC.
- *"We decided X for this system"* is an ADR.
- *"Should we do X or Y? Here's what we found"* is a research note.

**RFCs come first.** Anything that needs wider buy-in starts as an RFC. An accepted RFC
can then lead to one or more ADRs that record how it's carried out, each linking back to
it under `Appendix / References`.

## Files and numbers

- ADRs and RFCs: `NNNN-kebab-case-slug.md`. `NNNN` is four digits, the next free number
  **in the folder the file lands in**. The title's number is the same as the file's.
- When a record moves to another folder (a repo ADR promoted to this repo), it takes the
  next free number there; update links to it.
- If two pull requests take the same number, the one merged second renumbers. CI fails on
  a duplicate.
- Research notes: `kebab-case-slug.md`, no number.

## Layout

The title is the first line. A metadata list follows straight after it, one
`- **Key:** value` per line in the order below, then the `##` sections in the order below,
each one present and not empty. `###` subsections are free. No other `##` sections.
Dates are `YYYY-MM-DD`. Authors are people, or agents as `seat@team`, comma-separated.
Templates: [ADR](adr/TEMPLATE.md), [RFC](rfcs/TEMPLATE.md), [research note](research/TEMPLATE.md).

### ADR
- Title: `# ADR-NNNN: <the decision, as a statement>`
- Metadata, in order:
  - `Status`;
  - `Authors`;
  - `Decision Date`: required once the status is `Accepted`, `Implemented` or
    `Superseded`;
  - `Scope`: `org` or `repo`;
  - optional `Supersedes` and `Superseded by`: `ADR-NNNN`, comma-separated for several.
- Sections:
  1. `Context / Problem`: the problem and the context driving it.
  2. `Decision & Rationale`: the decision in one sentence, then the reasons as bullets.
  3. `Consequences`: expected and known consequences, including second-order effects.
  4. `Considered Options`: at least one option besides the chosen one, each with its
     pros and cons and why it was rejected. One `- ` bullet or `###` subsection per
     option.
  5. `Appendix / References`: links to the RFC, research notes, other ADRs, issues or
     repos it builds on, or `None.`

### RFC
- Title: `# RFC-NNNN: <the proposed change>`
- Metadata, in order:
  - `Status`;
  - `Authors`;
  - `Feedback Deadline`: required while the status is `Collecting Feedback`;
  - `Last Update`.
- Sections:
  1. `Summary`: two to four sentences on what changes and for whom.
  2. `Need`: why the change is needed (context and problem), with examples.
  3. `Approach`: how to meet the need. Rules use **must** / **should** / **may**.
  4. `Pros & Cons`: the factual benefits and drawbacks of the approach.
  5. `Alternatives`: **at least two**, each with pros and cons and why it wasn't
     chosen. One `- ` bullet or `###` subsection per alternative.
  6. `Appendix / References`: links, or `None.`

### Research note
- Title: `# Research: <the question, as one sentence>`
- Metadata, in order:
  - `Status`, `Date`, `Authors`;
  - `Type`: `question` or `spike`;
  - optional `Requested by` and `Time-box` (a spike has a time-box).
- Sections:
  1. `Question`;
  2. `Answer`: the recommendation in two to four sentences, with confidence (high,
     medium or low);
  3. `Criteria`;
  4. `Options`;
  5. `Prototype`: optional, only when one was built;
  6. `Risks and unknowns`;
  7. `Recommendation`;
  8. `Sources`.

Every section has text. Only a research note with status `Open` or `In progress` may have
empty sections while it's being written.

Template placeholders (`NNNN`, `YYYY-MM-DD`, `<...>`) must be gone. Anything in angle
brackets outside `code` counts as one, so write generics such as `Optional<T>` in
backticks.

## Status values

| Record | Values |
|---|---|
| ADR | `Draft`, `In Discussion`, `Accepted`, `Implemented`, `Abandoned`, `Superseded` (needs `Superseded by`; the newer ADR names it in `Supersedes`) |
| RFC | `Draft`, `Collecting Feedback`, `Accepted`, `Rejected`, `Abandoned` |
| Research note | `Open`, `In progress`, `Answered`, `Time-boxed out` |

**Only people decide.**
- An agent writes ADRs as `Draft`, then sets `In Discussion` when it hands the ADR to a
  person.
- An agent writes RFCs as `Draft`, then sets `Collecting Feedback` with a
  `Feedback Deadline` (default: two weeks later) when it opens the pull request.
- An agent never sets `Accepted`, `Implemented`, `Rejected`, `Abandoned` or `Superseded`.
  A person does, and fills in `Decision Date` or `Last Update`.

Records change in git. The commit history is the update log, so commit messages say what
changed and why.

## Writing well

- Context / Problem and Need describe the problem, not the solution.
- Decisions and approaches use **must** / **should** / **may** deliberately. Every rule
  can be checked in a review.
- Options and alternatives are real ones, each with pros and cons. "Not recorded" is
  allowed only in records written before this format.
- Separate facts (with a source) from inferences, especially in research notes.
- Diagrams go next to the record (`diagrams/<name>.*` in the same folder), made with the
  diagram-toolkit when it's available, else Mermaid.

## Local changes to the blog's format
- ADR status `Accepted` instead of `Decided`.
- ADRs have a `Scope` (`org` or `repo`).
- RFCs start with a `Summary`, because PR-Agent reads these files as review context.
- No `Update Log` section: git history is the log.

## Checking

```sh
python3 scripts/check_records.py docs/                  # a folder
python3 scripts/check_records.py path/to/0003-foo.md    # one or more files
```

A folder is searched for records (files whose title starts `# ADR-`, `# RFC-` or
`# Research:`). Templates and other Markdown files are skipped. A file named on the command
line must be a record. The checker exits non-zero and lists `file:line: problem` for every
problem.
