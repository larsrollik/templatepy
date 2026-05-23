# Branch protection

Configure branch protection rules on GitHub to enforce the gitflow.

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
| Restrict who can push | maintainers only | Prevents accidental direct pushes |

## Recommended rules for `prod`

Branch name pattern: `prod`

| Setting | Value | Reason |
|---|---|---|
| Restrict who can push | nobody / automation only | Only `release.yml` (via GITHUB_TOKEN) should write here |
| Require a pull request | optional | `release.yml` pushes directly; a PR rule would block it unless the token has admin bypass |

!!! note
    `release.yml` pushes to `prod` using `GITHUB_TOKEN` with `permissions: contents: write`. If you enable "Require PR" on `prod`, you'll need to add a bypass rule for the `github-actions[bot]` actor (GitHub's branch protection UI supports this).

## Required status check name

The aggregate job in `ci.yml` is named `CI`. This is what to enter in the required status checks field. It only passes when both `lint` and `secrets-scan` succeed, and only runs when both have completed.

## Rulesets (modern alternative)

GitHub now offers **Rulesets** (Repository → Settings → Rules → Rulesets) as a more flexible replacement for classic branch protection. Rulesets support bypass lists, actor-based rules, and can be applied to tag patterns too (useful for protecting `v*` tags from deletion).
