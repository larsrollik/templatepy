# Private repo dependencies (CI auth)

If your package depends on **private** GitHub repos (e.g. `git+`/workspace deps that
aren't on PyPI), CI needs credentials to clone them. Set `private_repo_deps=true` at
generation time and pick how CI authenticates via `private_repo_auth`.

Only **private** dependency repos need this — public deps clone anonymously.

## `app` — org-owned GitHub App (default, recommended)

CI mints a short-lived, per-run installation token via
`actions/create-github-app-token@v3`, then rewrites git to use it:

```yaml
- uses: actions/create-github-app-token@v3
  id: app-token
  with:
    app-id: ${{ secrets.CI_APP_ID }}
    private-key: ${{ secrets.CI_APP_PRIVATE_KEY }}
    owner: ${{ github.repository_owner }}
- run: git config --global url."https://x-access-token:${{ steps.app-token.outputs.token }}@github.com/".insteadOf "https://github.com/"
```

Setup (once per org):

1. Create an **org-owned** GitHub App: `https://github.com/organizations/<ORG>/settings/apps/new` — **Contents: Read-only**, webhook off.
2. Generate a private key (`.pem`) and note the **App ID**.
3. **Install** the App on the **private** repos that CI clones (Contents:read). The
   repo running the workflow does *not* need to be installed (it mints via `owner:`
   and checks itself out with the default `GITHUB_TOKEN`).
4. Add two **org** secrets: `CI_APP_ID` (the App ID) and `CI_APP_PRIVATE_KEY` (the `.pem`).

Why this over a PAT: not tied to any user, tokens are short-lived and auto-expire
(nothing to rotate), and access is scoped to the installed repos.

## `pat` — personal access token

CI uses a `PRIVATE_REPO_ACCESS_TOKEN` secret:

```yaml
- env:
    PRIVATE_REPO_ACCESS_TOKEN: ${{ secrets.PRIVATE_REPO_ACCESS_TOKEN }}
  run: |
    if [ -n "$PRIVATE_REPO_ACCESS_TOKEN" ]; then
      git config --global url."https://${PRIVATE_REPO_ACCESS_TOKEN}@github.com/".insteadOf "https://github.com/"
    fi
```

Setup: create a fine-grained PAT with **Contents: Read-only** on the private dep repos
and store it as the `PRIVATE_REPO_ACCESS_TOKEN` secret (repo or org level). Simpler, but
tied to a user account and expires (≤1 year) — prefer `app` for shared/long-lived infra.
