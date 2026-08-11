#!/usr/bin/env bash
# Install (or update) the `main-protected` branch ruleset on this repo.
#
# The ruleset requires a PR + approving review + the CI status check on the
# default branch, blocks force-pushes and deletion, and bypasses:
#   - Repository admins (so you can merge/manage), and
#   - the release-bot GitHub App (so versioning.yml can push the bump).
#
# Prereqs: `gh` authenticated; the repo exists on GitHub; and the release-bot
# App is installed with its id in the CI_BOT_APP_ID variable (see
# docs/repository-setup.md). Idempotent — safe to re-run.
#
# Usage:
#   bash scripts/setup_branch_protection.sh [--repo owner/name] [--app-id N]
#                                           [--check CI] [--reviews 1]
set -euo pipefail

REPO="" APP_ID="" CHECK="CI" REVIEWS="1" NAME="main-protected"
while [ $# -gt 0 ]; do
  case "$1" in
    --repo)    REPO="$2"; shift 2 ;;
    --app-id)  APP_ID="$2"; shift 2 ;;
    --check)   CHECK="$2"; shift 2 ;;
    --reviews) REVIEWS="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

# Resolve owner/repo from the git remote unless given.
if [ -z "$REPO" ]; then
  REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null) || {
    echo "No repo: pass --repo owner/name or run inside a repo with a GitHub remote." >&2
    exit 1
  }
fi
echo "==> Repo: $REPO"

# Resolve the release-bot App id for the Integration bypass actor. Try the flag,
# then the CI_BOT_APP_ID variable, then the repo's App installation.
if [ -z "$APP_ID" ]; then
  APP_ID=$(gh api "repos/$REPO/actions/variables/CI_BOT_APP_ID" --jq .value 2>/dev/null || true)
fi
if [ -z "$APP_ID" ]; then
  APP_ID=$(gh api "repos/$REPO/installation" --jq .app_id 2>/dev/null || true)
fi
if [ -z "$APP_ID" ]; then
  echo "WARNING: no release-bot App id found (flag / CI_BOT_APP_ID var / installation)." >&2
  echo "         Protecting main WITHOUT an App bypass will block versioning.yml's" >&2
  echo "         auto-bump push. Install the App first (docs/repository-setup.md)," >&2
  echo "         or pass --app-id. Aborting." >&2
  exit 1
fi
echo "==> Release-bot App id: $APP_ID"

# Build the ruleset payload (RepositoryRole 5 = admin).
PAYLOAD=$(cat <<JSON
{
  "name": "$NAME",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request" },
    { "actor_id": $APP_ID, "actor_type": "Integration", "bypass_mode": "always" }
  ],
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": {
        "allowed_merge_methods": ["merge", "squash", "rebase"],
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_approving_review_count": $REVIEWS,
        "required_review_thread_resolution": false
    } },
    { "type": "required_status_checks", "parameters": {
        "do_not_enforce_on_create": false,
        "strict_required_status_checks_policy": false,
        "required_status_checks": [ { "context": "$CHECK" } ]
    } }
  ]
}
JSON
)

# Create or update (idempotent) by ruleset name.
RID=$(gh api "repos/$REPO/rulesets" --jq ".[] | select(.name==\"$NAME\") | .id" 2>/dev/null || true)
if [ -n "$RID" ]; then
  echo "==> Updating existing ruleset '$NAME' (id $RID)..."
  echo "$PAYLOAD" | gh api -X PUT "repos/$REPO/rulesets/$RID" --input - >/dev/null
else
  echo "==> Creating ruleset '$NAME'..."
  echo "$PAYLOAD" | gh api -X POST "repos/$REPO/rulesets" --input - >/dev/null
fi
echo "==> Done. main is protected (PR + $REVIEWS review + '$CHECK'), admins and the App bypass."
