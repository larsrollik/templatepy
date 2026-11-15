# Developer convenience targets for a generated project.
#
# The CI Lint job runs exactly `uv run pre-commit run --all-files` under the synced
# uv workspace. Running the hooks any other way can pass while CI fails: `git commit`
# checks only staged files with a possibly-stale cache, and a bare `pre-commit run`
# cannot resolve cross-package types in the isolated mypy env. So run `make lint`
# before pushing - it is the same command CI uses.

.PHONY: lint test check

lint: ## Run the full pre-commit gate (ruff + mypy + ...), exactly as CI does.
	uv run pre-commit run --all-files

test: ## Run the test suite.
	uv run pytest

check: lint test ## Run the lint gate and the tests.
