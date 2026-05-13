#!/usr/bin/env bash
set -euo pipefail

URL="${ODOO_URL:-http://localhost:8069}"

echo "Checking Odoo server: $URL"

curl --fail --silent --show-error "$URL/web/login" > /dev/null

echo "Smoke test passed"