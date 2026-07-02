# Release workflow

## Branch topology

```
main  ←── PR merges from feature/bug/hotfix branches
feature/*, fix/*, chore/*  ←── created from main, deleted after merge
```

Tags on `main` are the release record. There is no `prod` branch — `git checkout v1.2.3` gives you any released state.

## Step-by-step

```sh
# 1. Create a branch
git checkout main && git pull
git checkout -b feature/my-feature

# 2. Do your work, committing with cz
cz commit        # interactive prompt enforcing Conventional Commits

# 3. Push branch and open PR
git push -u origin feature/my-feature
gh pr create --base main --title "feat: my feature"

# 4. CI runs: lint on push, tests on PR to main — merge is blocked until green

# 5. Merge PR (rebase or squash)
gh pr merge --rebase --delete-branch

# 6. release.yml fires automatically on push to main (one job):
#    → reads commits since last tag, runs cz bump --yes (patch/minor/major)
#    → creates + pushes version tag (e.g. v1.3.0)
#    → builds wheel + sdist
#    → creates GitHub release with dist files attached
#    → publishes to PyPI via OIDC trusted publishing (no stored token)
#    → Zenodo webhook archives the release (if enabled)
```

## How version bumps are determined

Commitizen reads all commits since the previous tag:

| Commits contain | Bump |
|---|---|
| only `fix:`, `docs:`, `chore:`, `refactor:`, `test:` | **patch** `0.0.x` |
| at least one `feat:` | **minor** `0.x.0` |
| `BREAKING CHANGE:` footer or `feat!:`/`fix!:` | **major** `x.0.0` |

If there are no bumpable commits since the last tag, `release.yml` exits silently — no error, no tag.

## Manual bump (override)

Automated bumping covers most cases. Override when needed:

```sh
cz bump --increment PATCH
cz bump --increment MINOR
cz bump --increment MAJOR
git push --follow-tags
```

## Conventional Commits format

```
<type>[optional scope]: <short description>

[optional body]

[optional footer: BREAKING CHANGE: ...]
```

Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`.

## Common issues

**`cz bump` fails with exit code 128**

- Detached HEAD → `git checkout main` first
- Uncommitted changes → commit or stash first
- Tag already exists → `git tag` to list, `git tag -d <tag>` to remove locally

**GPG signing failure**

See [GPG signing](gpg-signing.md).
