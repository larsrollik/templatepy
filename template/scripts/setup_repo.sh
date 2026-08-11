#!/usr/bin/env bash
# Guided post-generation setup, in order:
#   1. create the GitHub repo (or use the existing remote)
#   2. install the release-bot App + set its secret  (manual — see docs)
#   3. install the branch-protection ruleset
#
# Each step is optional and idempotent; skip any with the matching flag. Run
# after `copier copy`, from the generated project root.
#
# Usage: bash scripts/setup_repo.sh [--repo owner/name] [--private]
#                                   [--skip-create] [--skip-protect]
set -euo pipefail

REPO="" VISIBILITY="--public" SKIP_CREATE="" SKIP_PROTECT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --repo)         REPO="$2"; shift 2 ;;
    --private)      VISIBILITY="--private"; shift ;;
    --skip-create)  SKIP_CREATE=1; shift ;;
    --skip-protect) SKIP_PROTECT=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

pause() { printf '\n%s\n' "$1"; read -r -p "Press enter to continue (Ctrl-C to stop)... " _; }

# ── Step 1: repo on GitHub ────────────────────────────────────────────────────
if [ -z "$SKIP_CREATE" ] && ! git remote get-url origin >/dev/null 2>&1; then
  if [ -z "$REPO" ]; then
    read -r -p "Step 1/3 — create GitHub repo as (owner/name): " REPO
  fi
  echo "==> Creating $REPO ($VISIBILITY) and pushing..."
  git add -A && git commit -m "chore: initial commit from templatepy" -q || true
  gh repo create "$REPO" "$VISIBILITY" --source=. --remote=origin --push
else
  REPO="${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}"
  echo "==> Step 1/3 — using existing repo: $REPO"
fi

# ── Step 2: release-bot App + secret (manual) ─────────────────────────────────
# App install is an interactive GitHub flow — it cannot be scripted here.
if [ -z "$SKIP_PROTECT" ]; then
  cat <<EOF

Step 2/3 — install the release-bot GitHub App on $REPO (manual).
See docs/repository-setup.md for the exact permissions and secret setup:
  - install the App on this repo (same account/org as the remote),
  - set the repo/org variable CI_BOT_APP_ID = the App's id,
  - set the repo/org secret   CI_BOT_PRIVATE_KEY = the App's private key.
Skip this (and step 3) with --skip-protect if you don't want a protected main.
EOF
  pause "Do the above, then continue to install branch protection."

  # ── Step 3: branch protection ───────────────────────────────────────────────
  echo "==> Step 3/3 — installing branch protection..."
  bash "$(dirname "$0")/setup_branch_protection.sh" --repo "$REPO"
else
  echo "==> Skipping steps 2-3 (--skip-protect): main left unprotected."
fi

echo "==> Setup complete."
