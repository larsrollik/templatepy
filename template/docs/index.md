# [[ project_name ]]

[[ project_description ]]

## Installation

```sh
pip install [[ project_slug ]]
```

## Usage

_Add usage examples here._

## Development

```sh
git clone https://github.com/[[ github_username ]]/[[ github_repo ]].git
cd [[ github_repo ]]
uv sync --extra dev
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run pytest
```

## Docs

```sh
uv sync --extra docs
uv run mkdocs serve
```
