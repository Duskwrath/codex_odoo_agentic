#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

DB="${1:-odoo_test}"

ODOO_CONF="${ODOO_CONF:-/etc/odoo/odoo.conf}"

run_odoo_command \
  --config="$ODOO_CONF" \
  -d "$DB" \
  --test-enable \
  --stop-after-init
