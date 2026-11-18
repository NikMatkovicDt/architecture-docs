# Record format

The rules every ADR, RFC and research note follows, whoever writes it: a person, their
own Claude, or an agent team. `scripts/check_records.py` checks them, and CI runs it on
every pull request.

## Which record

| Record | Use it for | Lives in |
|---|---|---|
| **ADR** (Architecture Decision Record) | **one decision that has been made** (or is proposed), with its context, the options weighed and the consequences | `docs/adr/` here for decisions that apply across repos (**Scope: org**); the repo's own ADR folder (its existing one, else `docs/adr/`) for decisions about one repo (**Scope: repo**) |
| **RFC** (Request for Comments) | **a proposed rule or practice for every team**, which needs review before it applies | `docs/rfcs/` here |
| **Research note** | **a question answered with evidence**: options compared, a recommendation and its confidence. Often the input to an ADR | next to the work that asked the question, usually `docs/research/` |

The test: *"we decided X for this system"* is an ADR. *"Everyone should do X from now on"*
is an RFC. *"Should we do X or Y? Here's what we found"* is a research note. An accepted
RFC that settles one decision may be followed by an ADR that records it.

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
Templates: [ADR](adr/TEMPLATE.md), [RFC](rfcs/TEMPLATE.md), [research note](research/TEMPLATE.md).

### ADR
- Title: `# ADR-NNNN: <the decision, as a statement>`
- Metadata:
  - `Status`;
  - `Date` (`YYYY-MM-DD`, the last status change);
  - `Author`: a person, or an agent as `seat@team`;
  - `Scope`: `org` or `repo`;
  - optional `Supersedes` and `Superseded by`: `ADR-NNNN`, comma-separated for several.
- Sections: `Context`, `Decision`, `Alternatives considered`, `Consequences`, `Related`.

### RFC
- Title: `# RFC-NNNN: <the proposed rule>`
- Metadata: `Status`, `Date`, `Author`.
- Sections: `Summary`, `Motivation`, `Proposed rules`, `Alternatives considered`, `Related`.

### Research note
- Title: `# Research: <the question, as one sentence>`
- Metadata:
  - `Status`, `Date`, `Author`;
  - `Type`: `question` or `spike`;
  - optional `Requested by` and `Time-box` (a spike has a time-box).
- Sections:
  - `Question`;
  - `Answer` (the recommendation in two to four sentences, with confidence: high, medium or low);
  - `Criteria`;
  - `Options`;
  - `Prototype` (optional; only when one was built);
  - `Risks and unknowns`;
  - `Recommendation`;
  - `Sources`.

`Related` lists links to the records, research notes, issues or repos this one builds on,
or says `None.`

Every section has text. Only a research note with status `Open` or `In progress` may have
empty sections while it's being written.

Template placeholders (`NNNN`, `YYYY-MM-DD`, `<...>`) must be gone. Anything in angle
brackets outside `code` counts as one, so write generics such as `Optional<T>` in
backticks.

## Status values

| Record | Values | Notes |
|---|---|---|
| ADR | `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded` | `Superseded` needs `Superseded by`; the newer ADR names it in `Supersedes` |
| RFC | `Draft`, `Proposed`, `Accepted`, `Rejected`, `Withdrawn` | |
| Research note | `Open`, `In progress`, `Answered`, `Time-boxed out` | |

**Only people accept.** An agent writes ADRs and RFCs as `Proposed` (or `Draft`) and never
sets `Accepted`, `Rejected`, `Deprecated` or `Withdrawn`. A human does that when merging or
reviewing, and updates `Date`.

## Writing well

- Context and Motivation give the problem, not the solution.
- Decision and Proposed rules use **must** / **should** / **may** deliberately. Every rule
  can be checked in a review.
- Alternatives considered: each real option and why it lost. "Not recorded" is allowed
  only for records written before this format.
- Separate facts (with a source) from inferences, especially in research notes.
- Diagrams go next to the record (`diagrams/<name>.*` in the same folder), made with the
  diagram-toolkit when it's available, else Mermaid.

## Checking

```sh
python3 scripts/check_records.py docs/                  # a folder
python3 scripts/check_records.py path/to/0003-foo.md    # one or more files
```

A folder is searched for records (files whose title starts `# ADR-`, `# RFC-` or
`# Research:`). Templates and other Markdown files are skipped. A file named on the command
line must be a record. The checker exits non-zero and lists `file:line: problem` for every
problem.
