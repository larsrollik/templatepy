# PyPI publishing

The `release.yml` workflow builds and publishes to PyPI automatically when a `v*` tag is pushed. It exits cleanly (green) if no token is configured, so the step is safe to leave in even for private packages.

## Setup

### 1. Create a PyPI account

Register at [pypi.org](https://pypi.org). Enable 2FA (required for publishing since 2024).

### 2. Generate an API token

- Go to **PyPI → Account settings → API tokens → Add API token**
- Scope: **Entire account** for a new project (switch to per-project once the package exists)
- Copy the token — it is only shown once

### 3. Add the token to GitHub

- **Repository → Settings → Secrets and variables → Actions → New repository secret**
- Name: `UV_PUBLISH_TOKEN`
- Value: paste the PyPI token

### 4. Trigger a release

Push a version tag from your feature branch:

```sh
cz bump
git push --follow-tags
```

The `release.yml` workflow will:

1. Squash-merge `main` → `prod`
2. Generate changelog
3. Create a GitHub release
4. Run `uv build` + `uv publish` using the token

## Test PyPI

To publish to [test.pypi.org](https://test.pypi.org) first:

1. Register separately at test.pypi.org and generate a token there
2. Edit `release.yml` — replace the publish step with:

```yaml
- name: Build and publish to Test PyPI
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.TEST_PYPI_TOKEN }}
  run: |
    if [ -z "$UV_PUBLISH_TOKEN" ]; then
      echo "TEST_PYPI_TOKEN not configured — skipping."
      exit 0
    fi
    uv build
    uv publish --publish-url https://test.pypi.org/legacy/
```

## Manual publish

```sh
uv build
UV_PUBLISH_TOKEN=<token> uv publish
```

## Trusted publishing (recommended alternative)

PyPI supports [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) via OIDC — no long-lived token needed. Configure in `release.yml`:

```yaml
permissions:
  contents: write
  id-token: write   # required for trusted publishing

- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    skip-existing: true
```

And on PyPI: **Manage project → Publishing → Add a new publisher** with your GitHub org/repo/workflow details.
