import os
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.animals import router as animals_router
from src.api.routes.behaviors import router as behaviors_router
from src.api.routes.reports import router as reports_router
from src.api.routes.analytics import router as analytics_router
from src.api.routes.ingest import router as ingest_router
from src.api.sockets import router as sockets_router

# Configure app with OpenAPI metadata and tags
openapi_tags = [
    {"name": "Health", "description": "Service health and diagnostics."},
    {"name": "Animals", "description": "Animal registry and lookup."},
    {"name": "Behaviors", "description": "Behavior definitions."},
    {"name": "Reports", "description": "Saved reports and exports."},
    {"name": "Analytics", "description": "Analytics summaries and comparisons."},
    {"name": "Ingest", "description": "Data ingestion for behavior events."},
    {"name": "Sockets", "description": "WebSocket endpoints for real-time updates."},
]

app = FastAPI(
    title="VizAI Animal Behavior Analytics API",
    description="Preview backend providing in-memory data, analytics, and real-time updates for UI development.",
    version="0.1.0-preview",
    openapi_tags=openapi_tags,
)

# CORS configuration
frontend_url: Optional[str] = os.getenv("REACT_APP_FRONTEND_URL")
allow_origins: List[str] = [frontend_url] if frontend_url else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Root health check endpoint returning a simple status payload."""
    return {"message": "Healthy", "service": "VizAI Animal Behavior Analytics API"}


# Mount routers
app.include_router(animals_router, prefix="")
app.include_router(behaviors_router, prefix="")
app.include_router(reports_router, prefix="")
app.include_router(analytics_router, prefix="")
app.include_router(ingest_router, prefix="")
app.include_router(sockets_router, prefix="")
