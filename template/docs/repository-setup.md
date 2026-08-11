# Repository setup

Getting a generated project onto GitHub with a protected `main` and automated
releases. Run these **after** `copier copy`, in order. The guided script
`scripts/setup_repo.sh` walks the same sequence; this page is the reference for
the one manual step (installing the App).

Protection is entirely optional — skip it and the repo works out of the box with
`github-actions[bot]` pushing bumps to an unprotected `main`. The moment you add
the App below, `versioning.yml` uses it automatically (no file change).

## 1. Create the repo

```sh
gh repo create [[ github_username ]]/[[ github_repo ]] --public --source=. --remote=origin --push
```

## 2. Install the release-bot App

Protection blocks direct pushes to `main`, but `versioning.yml` still needs to
push the auto-bump commit + tag. A **GitHub App** solves this: it is an
identifiable actor the ruleset can add as a bypass, and (unlike
`github-actions[bot]`) its tag push triggers `release.yml`.

Use **one App per account/org**, owned by the same account/org as the repo, and
install it on every repo that needs it — do not create one App per repo.

1. **Create the App** (once per account/org):
   `https://github.com/settings/apps/new` (personal) or the org's
   *Settings → Developer settings → GitHub Apps → New*.
   - Homepage URL: any (e.g. the repo URL).
   - Uncheck **Webhook → Active**.
   - **Repository permissions:**
     - **Contents: Read and write** — push the bump commit/tag.
     - **Administration: Read and write** — only if you want the App to also be
       able to manage rulesets; not required just to bypass one.
     - **Metadata: Read-only** (mandatory, auto-selected).
     - **Contents: Read-only on dependency repos** — only if `private_repo_deps`.
   - Create, then **Generate a private key** (downloads a `.pem`).
   - Note the **App ID** (shown on the App's page).

2. **Install it** on this repo: the App page → *Install App* → pick the
   account/org → select this repository (or *All repositories*).

3. **Set the credentials** on the repo (or at org level to share across repos):

   ```sh
   gh variable set CI_BOT_APP_ID    --repo [[ github_username ]]/[[ github_repo ]] --body "<APP_ID>"
   gh secret   set CI_BOT_PRIVATE_KEY --repo [[ github_username ]]/[[ github_repo ]] < path/to/app.private-key.pem
   ```

   `versioning.yml` keys off the `CI_BOT_APP_ID` **variable**: present → push as
   the App; absent → fall back to `github.token`.

## 3. Install branch protection

```sh
bash scripts/setup_branch_protection.sh
```

This installs the `main-protected` ruleset: require a PR + 1 approving review +
the `CI` status check on the default branch, block force-pushes and deletion,
and bypass **repository admins** and **the App**. It resolves the App id from the
`CI_BOT_APP_ID` variable; re-running updates in place.

For a solo repo you approve/merge via your admin bypass; with collaborators the
review requirement is real. Tune with `--reviews N` / `--check <job-name>`.

## How the pieces fit

| Actor | Role |
|-------|------|
| `GITHUB_TOKEN` (`github-actions[bot]`) | Runs CI; `contents: write` lets it push bumps on an **unprotected** repo. Cannot bypass a ruleset, and its tag pushes cannot trigger `release.yml`. |
| Release-bot **App** | Bypass actor on the ruleset; pushes the bump + tag to **protected** `main`; its tag push triggers `release.yml` directly. |
| Repository **admin** (you) | Bypass actor (PR mode) so you can merge; still goes through PRs. |

`versioning.yml` is adaptive: it uses the App when `CI_BOT_APP_ID` is set and
falls back to `github.token` otherwise, so the same file serves both an
unprotected fresh repo and a protected one — no re-generation needed.
