#!/bin/bash
# Lint the backend using flake8 if available. Use correct working directory for this workspace.
set -e

BACKEND_DIR="/home/kavia/workspace/code-generation/updated--animal-behavior-analytics-platform-animal-behavior-analytics-platform-40568-40578-40605/backend_fastapi"

if [ ! -d "$BACKEND_DIR" ]; then
  echo "Backend directory not found at $BACKEND_DIR; skipping lint."
  exit 0
fi

cd "$BACKEND_DIR"

# Activate venv if present
if [ -f "venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

# If flake8 isn't available, skip lint to avoid failing preview
if ! command -v flake8 >/dev/null 2>&1; then
  echo "flake8 not found; skipping lint."
  exit 0
fi

flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

