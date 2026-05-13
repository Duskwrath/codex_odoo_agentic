#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

MODULE="${1:-custom_module}"
DB="${2:-odoo_test}"

ODOO_CONF="${ODOO_CONF:-/etc/odoo/odoo.conf}"
TEST_TAGS="${TEST_TAGS:-${MODULE}}"

run_odoo_command \
  --config="$ODOO_CONF" \
  -d "$DB" \
  -i "$MODULE" \
  --test-tags "$TEST_TAGS" \
  --test-enable \
  --stop-after-init
