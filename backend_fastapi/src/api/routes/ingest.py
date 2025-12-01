from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.api.models import EVENTS, BehaviorEvent, compute_summary
from src.api.sockets import broadcast_event, broadcast_analytics_delta

router = APIRouter(prefix="/ingest", tags=["Ingest"])


class IngestEvent(BaseModel):
    """Incoming event payload to be added to the in-memory store."""

    id: str = Field(..., description="Event id.")
    animal_id: str
    behavior_id: str
    session_id: str
    camera_id: str
    start_ts: datetime
    end_ts: datetime
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# PUBLIC_INTERFACE
@router.post("/event", summary="Ingest a behavior event")
def ingest_event(payload: IngestEvent):
    """Append an event to the in-memory repository and broadcast to WebSocket clients."""
    if any(e.id == payload.id for e in EVENTS):
        raise HTTPException(status_code=409, detail="Event id already exists")
    event = BehaviorEvent(**payload.model_dump())
    EVENTS.append(event)

    # Broadcast new event
    broadcast_event(event)

    # Broadcast lightweight analytics delta: just the last minute summary for the event's session
    summary = compute_summary([event.session_id], heatmap_scaling="session")
    broadcast_analytics_delta(summary)

    return {"status": "ok"}
