#!/usr/bin/env bash
# Enforce execution from the frontend_react_js directory and start the CRA dev server.
# This script is the authoritative entry for the preview system.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[frontend_react_js] Using working directory: ${FRONTEND_DIR}"
cd "${FRONTEND_DIR}"

# Basic sanity check to avoid accidental execution from backend_fastapi
if [[ ! -f "package.json" ]]; then
  echo "[frontend_react_js] ERROR: package.json not found in ${FRONTEND_DIR}. Aborting." >&2
  exit 1
fi

# Print environment for debugging
echo "[frontend_react_js] Node version: $(node -v || echo 'node not found')"
echo "[frontend_react_js] NPM version: $(npm -v || echo 'npm not found')"
echo "[frontend_react_js] CONTAINER_NAME=${CONTAINER_NAME:-unset}"

# Install dependencies if node_modules is missing or empty
if [[ ! -d "node_modules" || -z "$(ls -A node_modules 2>/dev/null || true)" ]]; then
  echo "[frontend_react_js] Installing dependencies..."
  npm install --no-audit --no-fund --loglevel=error
else
  echo "[frontend_react_js] Dependencies present. Skipping install."
fi

# Start the dev server
echo "[frontend_react_js] Starting npm start..."
# Use CI-friendly env to suppress prompts
CI=true npm start
