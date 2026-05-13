#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

echo "Starting Docker services: $DB_SERVICE, $ODOO_SERVICE"

build_odoo_image
ensure_services "$DB_SERVICE" "$ODOO_SERVICE"

echo "Odoo started"
echo "Logs: docker compose logs -f $ODOO_SERVICE"
