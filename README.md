# templatepy

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.20360320.svg)](https://doi.org/10.5281/zenodo.20360320)

Copier template for modern Python packages.

**[→ Full documentation](https://larsrollik.github.io/templatepy)**

## Stack

| Tool | Role |
|---|---|
| uv | dependency management, virtual environments |
| hatchling + hatch-vcs | build backend; version from git tags |
| commitizen | Conventional Commits enforcement; auto bump on merge |
| ruff | linting + formatting |
| mypy | static type checking |
| pytest + pytest-cov | testing with coverage |
| gitleaks | secret scanning |

## Quickstart

```sh
uv tool install copier
copier copy gh:larsrollik/templatepy my-new-project
cd my-new-project
git init && git add -A && git commit -m "chore: initial commit from templatepy"
uv sync --extra dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Update existing project

```sh
cd my-existing-project && copier update
```

## Release flow

```
feature branch  →  PR  →  CI gate (lint + test) must pass
                           merge blocked until green
                               ↓
                           merge to main (merge commit)
                               ↓
                           versioning.yml fires on push to main:
                           → cz bump → tag vX.Y.Z → dispatch release.yml
                               ↓
                           release.yml (on tag / dispatch):
                           → GitHub release (wheel + sdist attached)
                           → PyPI via OIDC trusted publishing (if enable_pypi_publishing)
                           → Zenodo webhook (if enabled)
```

## PyPI setup (one-time per repo)

Only if you answered `enable_pypi_publishing: true` (otherwise `release.yml`
makes the GitHub/Forgejo release but skips the publish step). Uses OIDC trusted
publishing — no API token stored in GitHub secrets.

1. pypi.org → project → Settings → Publishing → Add trusted publisher
2. Owner: `<github-user>`, Repository: `<repo>`, Workflow: `release.yml`
3. Done — the workflow handles authentication automatically.

## Branch protection (required for CI gate)

Repo settings → Branches → Add rule for `main`:
- ✅ Require status checks: `CI` job
- ✅ Require branches to be up to date
- ✅ Require linear history

For the auto-bump workflow to push the bump commit back to main:
- ✅ Allow specified actors to bypass → add `github-actions[bot]`

## Docs

```sh
uv run mkdocs serve
```

`mkdocs.yml` + the `docs` extra are always generated (build locally as above).
Deploy to GitHub Pages on push to main via `docs.yml` is added only when
`enable_docs_publishing: true`.

## Optional workflows (copier answers)

Three publish/automation extras are off by default; enable per project:

- `enable_pypi_publishing` — PyPI publish step in `release.yml` (+ OIDC `id-token`).
- `enable_docs_publishing` — the GitHub Pages / Forgejo `docs.yml` deploy workflow.
- `enable_llm_pr_review` — the optional LLM PR-review workflow (`pr-review.yml`).

When off, the corresponding workflow file is not generated at all (no
"not configured" placeholder checks).
