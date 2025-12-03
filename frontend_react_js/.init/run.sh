#!/usr/bin/env bash
# Purpose: Authoritative run script for the frontend_react_js container.
# Ensures we run npm commands from the frontend directory, never from backend_fastapi.
# - Installs dependencies without audit/fund prompts
# - Starts CRA dev server
# Guard: If CONTAINER_NAME is set and not 'frontend_react_js', exit to avoid misrouting.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Optional guard: prevent accidental execution if the orchestrator misroutes
if [[ "${CONTAINER_NAME:-frontend_react_js}" != "frontend_react_js" ]]; then
  echo "This run script is intended for CONTAINER_NAME=frontend_react_js. Current: ${CONTAINER_NAME:-unset}" >&2
  exit 1
fi

# Always operate from the frontend directory
cd "${FRONTEND_DIR}"

# Assert current working directory is exactly the frontend directory
CWD="$(pwd)"
if [[ "${CWD}" != "${FRONTEND_DIR}" ]]; then
  echo "ERROR: Current working directory (${CWD}) does not match FRONTEND_DIR (${FRONTEND_DIR}). Aborting." >&2
  exit 2
fi

echo "Frontend run hook starting in: ${CWD}"
echo "Expecting package.json at: ${CWD}/package.json"

# Sanity check: ensure package.json is present
if [[ ! -f "package.json" ]]; then
  echo "ERROR: package.json not found in ${FRONTEND_DIR}. Aborting to avoid ENOENT." >&2
  ls -la
  exit 3
fi

# Install and start
# --no-audit/--no-fund reduce noise and avoid network calls that can fail in CI
npm install --no-audit --no-fund
npm start
