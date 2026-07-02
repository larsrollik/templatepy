# PyPI publishing

The `release.yml` workflow publishes to PyPI automatically when a `v*` tag is pushed. Authentication uses **OIDC trusted publishing** — no API token stored in GitHub secrets.

## One-time setup on PyPI

1. Register at [pypi.org](https://pypi.org) and enable 2FA (required since 2024)
2. Go to **Account → Publishing → Add a new pending publisher**
3. Fill in:
   - PyPI project name: your package name
   - GitHub owner: your GitHub username or org
   - Repository name: your repo name
   - Workflow filename: `release.yml`
   - Environment name: *(leave blank)*
4. Click **Add**

That's it. The workflow handles authentication automatically — no token, no secret.

## Trigger a release

Releases are triggered automatically on every merge to `main` (`versioning.yml` bumps + tags, then dispatches `release.yml`). To trigger manually:

```sh
cz bump
git push --follow-tags
```

The `release.yml` workflow will:

1. Build wheel + sdist with `uv build`
2. Create a GitHub release with the dist files attached
3. Publish to PyPI with `uv publish --trusted-publishing auto`

## Test PyPI

To publish to [test.pypi.org](https://test.pypi.org) first, add a pending publisher there (same steps). Then temporarily edit `release.yml`:

```yaml
- name: Publish to Test PyPI
  run: uv publish --trusted-publishing auto --publish-url https://test.pypi.org/legacy/
```

## Manual publish (local)

Requires a PyPI API token:

```sh
uv build
UV_PUBLISH_TOKEN=pypi-... uv publish
```

## Zenodo archiving

If the Zenodo webhook is enabled, every GitHub release automatically creates a Zenodo record. See `CITATION.cff` for the metadata format. After the first release, copy the concept DOI from Zenodo and add it to `CITATION.cff`.
