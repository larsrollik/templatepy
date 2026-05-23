# Pre-commit hooks

This template ships a `.pre-commit-config.yaml` with the following hooks:

| Hook | Purpose |
|---|---|
| `pre-commit-hooks` | Trailing whitespace, line endings, YAML/TOML syntax, merge conflict markers |
| `ruff` | Linting with auto-fix |
| `ruff-format` | Formatting |
| `mypy` | Static type checking |
| `commitizen` | Conventional Commits enforcement on commit messages |
| `gitleaks` | Secret scanning — blocks commits containing API keys, tokens, passwords |

## Setup

```sh
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Run all hooks manually against every file:

```sh
uv run pre-commit run --all-files
```

## Gitleaks — handling false positives

[Gitleaks](https://github.com/gitleaks/gitleaks) scans staged content against a large ruleset of known secret patterns. Occasionally it flags test fixtures, example keys, or other non-sensitive strings.

### Option 1 — inline allowlist (single occurrence)

Add a `gitleaks:allow` comment on the offending line:

```python
EXAMPLE_API_KEY = "AKIAIOSFODNN7EXAMPLE"  # gitleaks:allow
```

### Option 2 — allowlist in `.gitleaks.toml` (recurring pattern)

The template includes a `.gitleaks.toml` at the repo root. Uncomment and extend the relevant section:

```toml
[allowlist]
description = "Global allowlist"

# Ignore an entire directory (e.g. test fixtures)
paths = [
  '''tests/fixtures/''',
]

# Ignore a specific pattern everywhere
regexes = [
  '''EXAMPLE_[A-Z0-9]{20}''',
]
```

See the [gitleaks allowlist docs](https://github.com/gitleaks/gitleaks#allowlisting) for the full set of options (per-rule allowlists, commit SHAs, etc.).

### Option 3 — skip for one commit (last resort)

```sh
SKIP=gitleaks git commit -m "chore: ..."
```

Use this sparingly — it bypasses the check entirely for that commit.

## Gitleaks — Go requirement

Gitleaks uses `language: golang` in its pre-commit hook definition. pre-commit will download and compile it automatically, but **Go must be installed on the machine**.

```sh
# macOS
brew install go

# or via the official installer: https://go.dev/dl/
```
