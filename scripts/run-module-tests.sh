#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-custom_module}"
DB="${2:-odoo_test}"

ODOO_BIN="${ODOO_BIN:-./odoo/odoo-bin}"
ODOO_CONF="${ODOO_CONF:-./config/odoo.conf}"
ADDONS_PATH="${ADDONS_PATH:-./addons,./odoo/addons}"

"$ODOO_BIN" \
  -c "$ODOO_CONF" \
  -d "$DB" \
  -i "$MODULE" \
  --addons-path="$ADDONS_PATH" \
  --test-enable \
  --stop-after-init
