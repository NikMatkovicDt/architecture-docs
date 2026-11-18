# Skills index

The skills in architecture-docs. **Agents read this before a task** (through cocoindex:
`get_document(repo="architecture-docs", filename=".claude/skills/INDEX.md")`). If one matches
the task, they fetch its `SKILL.md` the same way and follow it. People's own Claude Code
loads these automatically when working in this repo.

| Skill | Use when | Not for | File |
|---|---|---|---|
| `adr` | recording one decision the people concerned can make quickly: rationale, consequences, options weighed | changes that need other teams' buy-in (`rfc`), open questions (`research`) | `.claude/skills/adr/SKILL.md` |
| `rfc` | a change that needs buy-in from other teams or everyone (practices, cross-team architecture); collects feedback until a deadline; architect only in agent teams | a decision the people concerned can make themselves (`adr`) | `.claude/skills/rfc/SKILL.md` |
| `research` | answering a question with evidence: research notes and spike write-ups | recording the decision that follows (`adr` or `rfc`) | `.claude/skills/research/SKILL.md` |

Shared by all three: the format in `docs/FORMAT.md`, templates in `docs/adr/`, `docs/rfcs/`
and `docs/research/` (`TEMPLATE.md`), and the checker `scripts/check_records.py`.

Diagrams are not here: use the diagram-toolkit skill when it's available, else Mermaid.
