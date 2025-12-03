# animal-behavior-analytics-platform-40568-40578

This workspace contains:
- frontend_react_js: React preview app
- backend_fastapi: FastAPI preview backend

Important:
- The ONLY supported way to start the frontend in preview is via the container-local script:
  updated--animal-behavior-analytics-platform-animal-behavior-analytics-platform-40568-40578-40605/frontend_react_js/.init/run.sh
- preview.config.json is configured to run that script with working_directory set to the frontend directory.
- Do NOT create or use any root-level hooks that start npm from backend_fastapi or from the repo root.

Note: Any preview/init/CI configs must reference working directories under:
/home/kavia/workspace/code-generation/updated--animal-behavior-analytics-platform-animal-behavior-analytics-platform-40568-40578-40605/...
Do not reference the old path `/home/kavia/workspace/code-generation/animal-behavior-analytics-platform-40568-40578/...`.
