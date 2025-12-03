# VizAI Frontend (React)

This is a minimal React app used for preview. It is intentionally small and only verifies connectivity with the backend.

How to run locally:
- Ensure Node 18+ and npm are available.
- Copy `.env` with required REACT_APP_* variables.
- Install deps: `npm install`
- Start: `npm start`

Notes:
- The app serves a static health file at `/healthz` (public/healthz.txt) for container health probes.
- Startup scripts run from this directory and do NOT chdir into any backend path.
- The preview uses .init/run.sh as the authoritative start script, which forces cwd to this directory and prevents accidental runs from backend_fastapi.
