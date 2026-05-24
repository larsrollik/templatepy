# Contributing

Contributions are welcome — bug fixes, features, and documentation improvements.

## Getting started

1. Fork the repository and create a branch from `main`
2. Set up the dev environment: `uv sync --group dev && uv run pre-commit install --hook-type commit-msg --hook-type pre-commit`
3. Make your changes with tests
4. Commit using `cz commit` (Conventional Commits format is enforced)
5. Open a pull request targeting `main`

## Commit format

This project uses [Conventional Commits](https://www.conventionalcommits.org/).
The `commitizen` pre-commit hook will reject messages that don't conform.

```
feat: add new feature
fix: correct a bug
docs: update README
chore: update dependencies
```

Breaking changes: add `!` after the type or a `BREAKING CHANGE:` footer.

## Questions

Open an issue or email [[author_email]].
