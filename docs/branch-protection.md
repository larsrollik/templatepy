# Branch protection

Protect `main` so changes go through a reviewed PR and a green CI gate, while the
auto-bump workflow can still push the version tag. Protection is optional — a
fresh project works unprotected out of the box.

## Automated setup (recommended)

Generated projects ship scripts for this. From the project root:

```sh
bash scripts/setup_repo.sh          # guided: create repo → install App → protect
# or, on a repo that already exists:
bash scripts/setup_branch_protection.sh
```

`setup_branch_protection.sh` installs a `main-protected` ruleset via the GitHub
API: require a PR + approving review + the `CI` status check on the default
branch, block force-pushes and deletion, and bypass **repository admins** and the
**release-bot App**. It is idempotent; tune with `--reviews N` / `--check <job>`.

The full setup — including the App, the exact permissions it needs, and the
`CI_BOT_APP_ID` / `CI_BOT_PRIVATE_KEY` credentials — is documented in the
generated project's own `docs/repository-setup.md`.

## Why an App (not `github-actions[bot]`)

A protected `main` blocks direct pushes, including `versioning.yml`'s bump. A
GitHub App is an identifiable actor the ruleset can add to its bypass list, and
(unlike `github-actions[bot]`) an App-pushed tag triggers `release.yml`.
`versioning.yml` is adaptive: it uses the App when `CI_BOT_APP_ID` is set, else
falls back to `github-actions[bot]` on an unprotected repo. So the same repo
works before and after you protect it — no file changes.

## Required status check name

The aggregate job in `ci.yml` is named `CI`; that is the context the ruleset
requires. It passes only when `lint` and `test` both succeed (gitleaks runs
inside pre-commit, not as a separate job).

## Manual alternative

If you prefer to click through it, **Settings → Rules → Rulesets → New branch
ruleset** targeting the default branch, with the same rules and bypass actors as
above. Classic **Settings → Branches** protection also works, but Rulesets are
the modern path and are what the script uses.
