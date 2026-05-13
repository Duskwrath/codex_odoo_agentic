#!/usr/bin/env bash
set -euo pipefail

ODOO_SERVICE="${ODOO_SERVICE:-web}"
DB_SERVICE="${DB_SERVICE:-db}"
WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
HOST_UID="${HOST_UID:-$(id -u)}"
HOST_GID="${HOST_GID:-$(id -g)}"
DOCKER_CMD=()

select_docker_cmd() {
  if [ "${#DOCKER_CMD[@]}" -gt 0 ]; then
    return
  fi

  if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker is required but not installed or not on PATH"
    exit 127
  fi

  if docker compose version >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    DOCKER_CMD=(docker)
    return
  fi

  if command -v sudo >/dev/null 2>&1; then
    DOCKER_CMD=(sudo docker)
    return
  fi

  echo "ERROR: docker compose is not available or cannot access the Docker daemon"
  echo "Try running with Docker permissions or ensure 'sudo docker compose' works."
  exit 1
}

docker_compose() {
  select_docker_cmd
  "${DOCKER_CMD[@]}" compose "$@"
}

require_docker() {
  select_docker_cmd
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
