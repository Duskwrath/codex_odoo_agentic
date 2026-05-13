#!/usr/bin/env bash
set -euo pipefail

echo "Running Python lint..."

ruff check addons scripts

echo "Lint passed"