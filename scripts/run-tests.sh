#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker-common.sh"

DB="${1:-odoo_test}"

ODOO_CONF="${ODOO_CONF:-/etc/odoo/odoo.conf}"

mapfile -t MODULES < <(
  find addons -mindepth 2 -maxdepth 2 -name "__manifest__.py" \
    -printf "%h\n" \
    | sed "s#^addons/##" \
    | sort
)

if [[ ${#MODULES[@]} -eq 0 ]]; then
  echo "ERROR: no custom addons found under addons/"
  exit 1
fi

MODULE_LIST="$(IFS=,; echo "${MODULES[*]}")"

run_odoo_command \
  --config="$ODOO_CONF" \
  -d "$DB" \
  -i "$MODULE_LIST" \
  -u "$MODULE_LIST" \
  --test-tags "$MODULE_LIST" \
  --test-enable \
  --stop-after-init
