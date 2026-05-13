#!/usr/bin/env bash
set -euo pipefail

SERVICE="${ODOO_SERVICE:-odoo}"

echo "Starting Odoo Docker service in background: $SERVICE"

docker compose up -d "$SERVICE"

echo "Odoo started"
echo "Logs: docker compose logs -f $SERVICE"