# Contributing

Contributions are welcome — bug fixes, features, and documentation improvements.

## Getting started

```bash
uv sync --extra dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

The second command installs two hook types:
- `pre-commit` — runs ruff, mypy, gitleaks on staged files
- `commit-msg` — auto-fixes commit message formatting, then lints with gitlint and commitizen

## Commit format

This project uses [Conventional Commits](https://www.conventionalcommits.org/).
Commitizen enforces the format; use `cz commit` for an interactive prompt.

```
feat: add new feature
fix: correct a bug
docs: update README
chore: update dependencies
```

Breaking changes: add `!` after the type or a `BREAKING CHANGE:` footer.

## Commit message hooks

The `commit-msg` hooks run automatically on every commit:

1. **fix-commit-msg** — auto-fixes leading/trailing whitespace, hard tabs, missing blank line between subject and body
2. **gitlint** — flags remaining issues (subject too long, etc.) that need manual correction
3. **commitizen** — rejects messages that don't follow Conventional Commits

## Questions

Open an issue or email [[author_email]].
