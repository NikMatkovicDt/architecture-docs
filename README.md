# architecture-docs

Shared Architecture Decision Records (ADRs) and RFCs, consumed by [PR-Agent](https://docs.pr-agent.ai/)
as sibling-repo context when reviewing pull requests in other repositories under the
`NikMatkovicDt` GitHub account.

## Structure

- `docs/adr/`: Architecture Decision Records
- `docs/rfcs/`: Request for Comments proposals
- `docs/research/`: the research note template (notes live next to the work that asked)
- `docs/FORMAT.md`: the format every record follows
- `.claude/skills/`: the `adr`, `rfc` and `research` skills, and `INDEX.md`
- `scripts/check_records.py`: the format checker

## Writing a record

Every ADR, RFC and research note follows [docs/FORMAT.md](docs/FORMAT.md). Start from the
template in its folder, then check it:

```sh
python3 scripts/check_records.py docs/
```

CI runs the same check on every pull request. Claude Code picks up the skills in
`.claude/skills/` when you work in this repo. ai-devbox agents read them through cocoindex,
starting from `.claude/skills/INDEX.md`, so changes reach them only after they're merged
and cocoindex has re-indexed this repo.

## Usage

Consuming repositories reference specific files here via `.pr_agent.toml`:

```toml
[config]
repo_context_files = [
    {repo_id = "NikMatkovicDt/architecture-docs", file_path = "docs/adr/0001-schema-validation.md"},
]
```

The consuming repository's PR-Agent deployment must first allowlist this repo via the
host-only `repo_context_sibling_repos` setting (set in the CI workflow, not in
`.pr_agent.toml`).
