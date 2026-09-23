# architecture-docs

Shared Architecture Decision Records (ADRs) and RFCs, consumed by [PR-Agent](https://docs.pr-agent.ai/)
as sibling-repo context when reviewing pull requests in other repositories under the
`NikMatkovicDt` GitHub account.

## Structure

- `docs/adr/` — Architecture Decision Records
- `docs/rfcs/` — Request for Comments proposals

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
