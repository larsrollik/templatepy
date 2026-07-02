# Branch protection

Configure branch protection rules on GitHub to enforce the CI gate and allow automated version bumping.

## Recommended rules for `main`

**Repository → Settings → Branches → Add rule**, branch name pattern: `main`

| Setting | Value | Reason |
|---|---|---|
| Require a pull request before merging | ✓ | No direct pushes to main |
| Required approvals | 1+ | At least one review |
| Dismiss stale reviews on new commits | ✓ | Re-review after force-push |
| Require status checks to pass | ✓ | Blocks merge on CI failure |
| Required status checks | `CI` | The aggregate job in `ci.yml` |
| Require branches to be up to date | ✓ | No stale merges |
| Require linear history | ✓ | Keeps git log readable |

## Allow `release.yml` to push back to `main`

`release.yml` creates a version tag and pushes it after merging. GitHub's default branch protection blocks this. Fix:

**Repository → Settings → Branches → main rule → Allow specified actors to bypass required pull requests**

Add: `github-actions[bot]`

Without this, the release workflow will fail with a 403 when trying to push the tag.

## Required status check name

The aggregate job in `ci.yml` is named `CI`. This is what to enter in the required status checks field. It passes only when `lint` and `test` both succeed (gitleaks runs inside pre-commit, not a separate job).

## Rulesets (modern alternative)

GitHub now offers **Rulesets** (Repository → Settings → Rules → Rulesets) as a more flexible replacement for classic branch protection. Rulesets support bypass lists, actor-based rules, and can be applied to tag patterns (useful for protecting `v*` tags from deletion or force-push).
