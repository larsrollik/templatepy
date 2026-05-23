# templatepy

Copier template for modern Python packages.

**[→ Full documentation](https://YOUR_ORG.github.io/templatepy)**

## Stack

| Tool | Role |
|---|---|
| uv | dependency management, virtual environments |
| hatchling + hatch-vcs | build backend; version from git tags |
| commitizen | Conventional Commits enforcement; `cz bump` |
| ruff | linting + formatting |
| mypy | static type checking |
| pytest + pytest-cov | testing with coverage |

## Quickstart

```sh
uv tool install copier
copier copy gh:YOUR_ORG/templatepy my-new-project
cd my-new-project
git init && git add -A && git commit -m "chore: initial commit from templatepy"
uv sync --group dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Update existing project

```sh
cd my-existing-project && copier update
```

## Release flow

```
feature/bug branch  →  cz commit  →  cz bump  →  git push --follow-tags
                                                         ↓
                                       PR to main  →  lint + tests  →  merge
                                                         ↓
                                              tag triggers release.yml
                                              → squash to prod
                                              → GitHub release + changelog
                                              → PyPI (if UV_PUBLISH_TOKEN set)
```

## Required secrets

| Secret | Purpose |
|---|---|
| `UV_PUBLISH_TOKEN` | PyPI publish — skipped gracefully if absent |

## Docs

```sh
uv tool install mkdocs-material
mkdocs serve
```
