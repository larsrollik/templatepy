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
uv sync --extra dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

## Running tests

```sh
uv run pytest
```

## Release workflow

1. Work on a `feature/` or `fix/` branch, committing with `cz commit`
2. Open a PR — CI (lint + tests + secrets scan) must pass before merge
3. Merge to main → version bump and tag are created automatically
4. Tag triggers release: GitHub release + PyPI publish

## License

See [LICENSE](LICENSE).
