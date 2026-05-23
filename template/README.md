# [[ project_name ]]

[[ project_description ]]

## Installation

```sh
pip install [[ project_slug ]]
```

Or with uv:

```sh
uv add [[ project_slug ]]
```

## Development setup

```sh
git clone https://github.com/[[ github_username ]]/[[ github_repo ]].git
cd [[ github_repo ]]
uv sync --group dev
uv run pre-commit install --hook-type commit-msg --hook-type pre-commit
```

## Running tests

```sh
uv run pytest
```

## Release workflow

1. Work on a `feature/` or `bug/` branch, committing with `cz commit`
2. Before merging: `cz bump` → creates version tag on the branch
3. `git push --follow-tags` → opens PR, CI runs lint + tests
4. Merge PR → tag triggers automated release

## License

See [LICENSE](LICENSE).
