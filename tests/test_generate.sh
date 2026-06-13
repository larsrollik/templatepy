#!/usr/bin/env bash
# Smoke-test the copier template end-to-end:
#   1. generate a project with dummy answers via `uvx copier`
#   2. assert generation succeeds
#   3. assert content is rendered (slug present, no literal Jinja tokens)
#   4. assert generated CI workflow is valid YAML
#   5. (best effort) assert the generated project imports
#
# Usage: bash tests/test_generate.sh [OUT_DIR]
# Run from the template repo root.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$(mktemp -d)/generated}"
SLUG="dummy_project"

echo "==> Repo:   $REPO_ROOT"
echo "==> Output: $OUT"
rm -rf "$OUT"

# Copier reads a git source from its last commit, ignoring uncommitted working-
# tree changes. To smoke-test what is *currently on disk* (the state about to be
# committed, and the checked-out state in CI), generate from a .git-less copy.
SRC="$(mktemp -d)/template"
cp -r "$REPO_ROOT" "$SRC"
rm -rf "$SRC/.git"
trap 'rm -rf "$(dirname "$SRC")"' EXIT

echo "==> Generating project with copier (from working-tree copy)..."
uvx copier copy --defaults --trust \
  --data project_name="Dummy Project" \
  --data project_slug="$SLUG" \
  --data project_description="A dummy project for smoke testing" \
  --data author_name="Test Author" \
  --data author_email="test@example.com" \
  --data github_username="testuser" \
  --data github_repo="dummy-project" \
  --data python_requires="3.12" \
  --data license_type="noncommercial" \
  --data private_repo_deps=false \
  "$SRC" "$OUT"

echo "==> Asserting generation produced expected files..."
test -f "$OUT/pyproject.toml"            || { echo "FAIL: pyproject.toml missing"; exit 1; }
test -d "$OUT/src/$SLUG"                 || { echo "FAIL: src/$SLUG missing (slug not rendered into path)"; exit 1; }
test -f "$OUT/.github/workflows/ci.yml"  || { echo "FAIL: ci.yml missing"; exit 1; }

echo "==> Asserting pyproject.toml content was rendered..."
grep -q "name = \"$SLUG\"" "$OUT/pyproject.toml" \
  || { echo "FAIL: rendered slug not found in pyproject.toml"; cat "$OUT/pyproject.toml"; exit 1; }

echo "==> Asserting no unrendered Jinja tokens leaked into generated project..."
# The only legitimate occurrences are bash [[ ... ]] inside the generated
# ci.yml aggregate gate. Exclude that one file and assert nothing else has
# [[ or [% tokens.
if grep -RInE '\[\[|\[%' "$OUT" \
      --exclude-dir=.git \
      | grep -v '/.github/workflows/ci.yml:' \
      | grep -v '/.forgejo/workflows/ci.yml:' ; then
  echo "FAIL: found unrendered Jinja tokens (above) in generated project"
  exit 1
fi

echo "==> Asserting generated ci.yml is valid YAML..."
python -c "import yaml; yaml.safe_load(open('$OUT/.github/workflows/ci.yml'))" \
  || { echo "FAIL: generated ci.yml is not valid YAML"; exit 1; }

echo "==> Asserting all generated workflows are valid YAML..."
for wf in "$OUT"/.github/workflows/*.yml; do
  python -c "import yaml; yaml.safe_load(open('$wf'))" \
    || { echo "FAIL: $wf is not valid YAML"; exit 1; }
done

echo "==> (best effort) Installing generated project and importing it..."
if ( cd "$OUT" && git init -q && git add -A \
     && uv sync --extra dev >/dev/null \
     && uv run python -c "import $SLUG; print('import OK:', $SLUG.__name__)" ); then
  echo "==> Install + import OK"
else
  echo "WARN: install/import step failed or was skipped (non-fatal)"
fi

echo "==> SMOKE TEST PASSED"
