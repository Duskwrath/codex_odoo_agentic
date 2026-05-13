#!/usr/bin/env bash
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

PROTECTED_BRANCHES=("main" "master" "production" "staging")

for protected in "${PROTECTED_BRANCHES[@]}"; do
  if [[ "$BRANCH" == "$protected" ]]; then
    echo "ERROR: refusing to push protected branch: $BRANCH"
    exit 1
  fi
done

make format
make lint
make test-all
make smoke

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: working tree has uncommitted changes"
  git status --short
  exit 1
fi

git push origin "$BRANCH"

echo "Pushed branch: $BRANCH"