# Preview Init Notes

This directory contains preview/init settings for the workspace.

Frontend (React) runner MUST execute npm commands from:
`/home/kavia/workspace/code-generation/updated--animal-behavior-analytics-platform-animal-behavior-analytics-platform-40568-40578-40605/frontend_react_js`

Validated files:
- ./.init-run-tool-frontend -> runs `npm start` with correct working_directory
- ./start-preview.json -> maps frontend_react_js container to the correct working_directory
- ../preview.config.json -> maps frontend_react_js container to the correct working_directory

Do not run `npm start` from any backend_fastapi path; that causes ENOENT for package.json.
