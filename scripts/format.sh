#!/usr/bin/env bash
set -euo pipefail

echo "Running Python formatter..."

ruff format addons scripts

echo "Format completed"
