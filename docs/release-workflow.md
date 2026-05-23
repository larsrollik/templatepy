# Release workflow

## Branch topology

```
prod  ←── squash merge on each release (automated by release.yml)
main  ←── PR merges from feature/bug/hotfix branches
feature/*, bug/*, hotfix/*  ←── created from main
```

`prod` always reflects the latest released state. `main` is the integration branch.

## Step-by-step

```sh
# 1. Create a branch
git checkout main && git pull
git checkout -b feature/my-feature

# 2. Do your work, committing with cz
cz commit        # interactive prompt enforcing Conventional Commits

# 3. Bump version before merging
cz bump          # reads commits since last tag, determines patch/minor/major
                 # creates a version tag (e.g. v1.3.0)

# 4. Push branch + tag
git push --follow-tags

# 5. Open PR to main
gh pr create --base main --title "feat: my feature"

# 6. CI runs: lint on push, tests on PR
# 7. Merge PR
gh pr merge --squash --delete-branch

# 8. Tag push triggers release.yml automatically:
#    - squash-merges main → prod
#    - generates changelog from commits since previous tag
#    - creates GitHub release with those notes
#    - publishes to PyPI if UV_PUBLISH_TOKEN is configured
```

## How `cz bump` determines the version increment

Commitizen reads all commits since the previous tag and applies these rules:

| Commits contain | Bump |
|---|---|
| only `fix:`, `docs:`, `chore:`, `refactor:`, `test:` | **patch** `0.0.x` |
| at least one `feat:` | **minor** `0.x.0` |
| `BREAKING CHANGE:` footer or `feat!:`/`fix!:` | **major** `x.0.0` |

Override manually if needed:

```sh
cz bump --increment PATCH
cz bump --increment MINOR
cz bump --increment MAJOR
cz bump --yes               # skip confirmation prompt
```

## Conventional Commits format

The `commitizen` pre-commit hook rejects messages that don't conform:

```
<type>[optional scope]: <short description>

[optional body]

[optional footer: BREAKING CHANGE: ...]
```

Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`.

## Common issues

**`cz bump` fails with exit status 128**

- Detached HEAD → `git checkout main` first
- Uncommitted changes → `git commit` or `git stash`
- Tag already exists → `git tag` to list, `git tag -d <tag>` to remove
- GPG signing failure → see [GPG signing](gpg-signing.md)

**Tag pushed but `release.yml` didn't trigger**

- Verify the tag matches `v[0-9]*` pattern
- Check Actions tab on GitHub for workflow runs
- If CI pushed the tag using `GITHUB_TOKEN`, downstream `push` triggers won't fire (GitHub loop prevention). Use a PAT stored as `BUMP_TOKEN` instead, and configure the checkout step: `token: ${{ secrets.BUMP_TOKEN }}`
