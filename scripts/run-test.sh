#!/usr/bin/env bash
set -euo pipefail

DB="${1:-odoo_test}"

ODOO_BIN="${ODOO_BIN:-./odoo/odoo-bin}"
ODOO_CONF="${ODOO_CONF:-./config/odoo.conf}"

"$ODOO_BIN" \
  -c "$ODOO_CONF" \
  -d "$DB" \
  --test-enable \
  --stop-after-init