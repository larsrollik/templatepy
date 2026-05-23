# templatepy

Copier template for modern Python packages.

## Stack

| Tool | Role |
|---|---|
| **uv** | Dependency management, virtual environments, running tools |
| **hatchling + hatch-vcs** | Build backend; version derived from git tags |
| **commitizen** | Conventional Commits enforcement; version bumping via `cz bump` |
| **ruff** | Linting and formatting (replaces flake8 + black) |
| **mypy** | Static type checking |
| **pytest + pytest-cov** | Testing with coverage |
| **MkDocs Material** | Documentation (this site) |

## Requirements

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/)
- [copier](https://copier.readthedocs.io/) ≥ 9.0

```sh
uv tool install copier
```

## Create a new project

```sh
copier copy gh:YOUR_ORG/templatepy my-new-project
cd my-new-project
git init && git add -A && git commit -m "chore: initial commit from templatepy"
uv sync --group dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Apply template updates to an existing project

```sh
cd my-existing-project
copier update
```

Copier reads `.copier-answers.yml` (committed in the generated repo) to know what answers were given and which template version was used.

## Day-to-day commands

```sh
cz commit                        # structured commit (enforces Conventional Commits)
uv run pytest                    # run tests
uv run pre-commit run --all-files  # run all lint checks manually
cz bump                          # bump version, create tag
git push --follow-tags           # push commits + tag → triggers release workflow
```

## Project structure (generated)

```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py          # version via importlib.metadata
│       └── py.typed             # PEP 561 typed marker
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── .github/
│   └── workflows/
│       ├── ci.yml               # lint on push; tests on PR to main
│       ├── release.yml          # on v* tag: squash→prod, release notes, PyPI
│       └── pr-review.yml        # optional LLM review (commented out)
├── pyproject.toml
├── .pre-commit-config.yaml
└── LICENSE                      # copyright + all rights reserved (replace before publishing)
```
