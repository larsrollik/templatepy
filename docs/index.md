# templatepy

Copier template for modern Python packages.

## Stack

| Tool | Role |
|---|---|
| **uv** | Dependency management, virtual environments, running tools |
| **hatchling + hatch-vcs** | Build backend; version derived from git tags |
| **commitizen** | Conventional Commits enforcement; auto version bump on merge |
| **ruff** | Linting and formatting |
| **mypy** | Static type checking |
| **pytest + pytest-cov** | Testing with coverage |
| **MkDocs Material** | Documentation (this site) |

## Requirements

- Python ≥ 3.10
- [uv](https://docs.astral.sh/uv/)
- [copier](https://copier.readthedocs.io/) ≥ 9.0

```sh
uv tool install copier
# or run without installing:
uvx copier ...
```

## Create a new project

```sh
copier copy gh:larsrollik/templatepy my-new-project
cd my-new-project
git init && git add -A && git commit -m "chore: initial commit from templatepy"
uv sync --extra dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Template questions

| Question | Choices / default | Notes |
|---|---|---|
| `project_name` | free text | Display name, e.g. `My Package` |
| `project_slug` | free text | Import name, e.g. `my_package` |
| `project_description` | free text | One line; quote if it contains `:` |
| `author_name` | free text | |
| `author_email` | free text | |
| `github_username` | free text | GitHub org or personal account |
| `github_repo` | free text | Repository name on GitHub |
| `year` | free text | Copyright year |
| `python_requires` | `3.10`-`3.14`, default `3.13` | Minimum supported Python version; controls `requires-python` and test matrix |
| `license_type` | `noncommercial` / `bsd3` | `noncommercial` for MSW-core packages; `bsd3` for standalone hardware drivers |
| `private_repo_deps` | `false` / `true`, default `false` | Set `true` only if the repo has private GitHub dependencies; injects a git auth step in CI. All standard repos use `false` (PyPI deps only). |
| `private_repo_auth` | `app` / `pat`, default `app` (asked only when `private_repo_deps=true`) | How CI authenticates to clone the private deps. **app** = org-owned GitHub App, per-run token via `actions/create-github-app-token@v3` (org secrets `CI_APP_ID` + `CI_APP_PRIVATE_KEY`; the App needs Contents:read on the private repos). **pat** = the `PRIVATE_REPO_ACCESS_TOKEN` secret. See [Private repo auth](private-repo-auth.md). |
| `test_on_windows` | `false` / `true`, default `false` | Adds `windows-latest` to the CI test matrix (for path-sensitive or Windows-targeted packages). |

## Apply template updates to an existing project

### Dry-run first (safe, writes nothing)

```sh
uvx copier update --pretend --defaults
```

If the output is `Keeping template version X.Y.Z`, no changes are needed and the working tree is untouched.

### Apply the update

```sh
cd my-existing-project
uvx copier update --defaults
```

Copier reads `.copier-answers.yml` to know the template source, baseline version, and all previous answers. Commit the result.

### Changing an answer without running a full update

Edit `.copier-answers.yml` directly, commit the change, then run:

```sh
uvx copier update --defaults
```

Copier uses the updated answers as the new baseline and applies only the incremental diff. This is the correct way to change `python_requires`, `license_type`, or any other question after initial generation.

### Installing hooks after a rename or first sync

If `git commit` complains that `pre-commit` is not found (stale hook path after renaming the directory), reinstall:

```sh
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Day-to-day commands

```sh
cz commit                          # structured commit (enforces Conventional Commits)
uv run pytest                      # run tests
uv run pre-commit run --all-files  # run all lint checks manually
```

Version bumping and releasing are handled automatically by `release.yml` on every merge to `main` (it runs `cz bump`, tags, builds, and publishes in one job). Manual override:

```sh
cz bump && git push --follow-tags
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
│       ├── release.yml          # on merge to main: cz bump → build → GitHub release + PyPI (OIDC)
│       ├── pr-review.yml        # automated PR review
│       └── docs.yml             # deploy MkDocs to GitHub Pages on push to main
├── pyproject.toml
├── CITATION.cff                 # citation metadata for Zenodo + GitHub
├── .pre-commit-config.yaml
└── LICENSE
```
