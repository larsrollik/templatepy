# Local CI with act

[act](https://github.com/nektos/act) runs GitHub Actions workflows locally using Docker. Useful for debugging CI without pushing.

## Install

```sh
# macOS
brew install act

# Linux
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (winget)
winget install nektos.act
```

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) to be running.

## Usage

```sh
# Run all workflows triggered by push
act push

# Run a specific workflow
act push -W .github/workflows/ci.yml

# Run with verbose output
act push --verbose

# List available workflows and jobs
act -l

# Run a specific job
act push -j lint
```

## First run

On first run, `act` asks which Docker image size to use:

- **Micro** — minimal, fast to download, may lack some tools
- **Medium** — recommended for most workflows
- **Large** — full GitHub Actions environment, ~20 GB

For this template's workflows, **Medium** is sufficient.

## Known limitations

- `act` doesn't support all GitHub Actions features (e.g. `workflow_run`, some contexts)
- Some actions that call back to GitHub APIs may behave differently
- `gitleaks` uses the `golang` language in its pre-commit hook and requires Go to be installed locally — see [Pre-commit hooks](pre-commit.md)
- OIDC trusted publishing (`uv publish --trusted-publishing auto`) does not work locally; skip the publish step when testing `release.yml` with act
