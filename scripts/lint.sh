#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

echo "Running Python lint..."

run_workspace_command ruff check addons scripts

echo "Lint passed"
