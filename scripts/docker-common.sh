#!/usr/bin/env bash
set -euo pipefail

ODOO_SERVICE="${ODOO_SERVICE:-web}"
DB_SERVICE="${DB_SERVICE:-db}"
WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
HOST_UID="${HOST_UID:-$(id -u)}"
HOST_GID="${HOST_GID:-$(id -g)}"

docker_compose() {
  docker compose "$@"
}

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is required but not installed or not on PATH"
    exit 127
  fi
  docker compose version >/dev/null
}

build_odoo_image() {
  require_docker
  docker_compose build "$ODOO_SERVICE"
}

ensure_services() {
  require_docker
  docker_compose up -d "$@"
}

run_workspace_command() {
  build_odoo_image
  docker_compose run --rm --no-deps \
    --user "${HOST_UID}:${HOST_GID}" \
    -e HOME=/tmp \
    -e RUFF_CACHE_DIR=/tmp/.ruff_cache \
    --workdir "$WORKSPACE_DIR" \
    "$ODOO_SERVICE" "$@"
}

run_odoo_command() {
  build_odoo_image
  ensure_services "$DB_SERVICE"
  docker_compose run --rm --no-deps "$ODOO_SERVICE" "$@"
}
