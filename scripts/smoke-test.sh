#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

URL="${ODOO_URL:-http://localhost:8069}"
ATTEMPTS="${SMOKE_ATTEMPTS:-30}"
SLEEP_SECONDS="${SMOKE_SLEEP_SECONDS:-2}"

echo "Checking Odoo server: $URL"

ensure_services "$DB_SERVICE" "$ODOO_SERVICE"

for ((attempt=1; attempt<=ATTEMPTS; attempt++)); do
  if curl --fail --silent --show-error "$URL/web/login" >/dev/null; then
    echo "Smoke test passed"
    exit 0
  fi
  sleep "$SLEEP_SECONDS"
done

echo "ERROR: Odoo server did not become ready at $URL"
docker_compose ps
exit 1
