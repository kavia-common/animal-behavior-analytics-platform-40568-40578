import asyncio
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.models import AnalyticsSummary, BehaviorEvent

router = APIRouter(tags=["Sockets"])

_clients: Set[WebSocket] = set()


def _prune(ws: WebSocket):
    try:
        _clients.remove(ws)
    except KeyError:
        pass


async def _send_safe(ws: WebSocket, message):
    try:
        await ws.send_json(message)
    except Exception:
        _prune(ws)


# PUBLIC_INTERFACE
@router.websocket(
    "/ws/events",
)
async def ws_events(websocket: WebSocket):
    """
    WebSocket endpoint for real-time events and analytics deltas.

    Usage:
    - Connect, then receive JSON messages with type=event or type=analytics_delta.
    - Periodic pings keep the connection alive.
    """
    await websocket.accept()
    _clients.add(websocket)

    try:
        while True:
            try:
                # Receive ping/pong or client messages to keep connection active
                _ = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({"type": "heartbeat"})
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        _prune(websocket)
    except Exception:
        _prune(websocket)


# PUBLIC_INTERFACE
def broadcast_event(event: BehaviorEvent):
    """Broadcast a new BehaviorEvent to all connected websocket clients."""
    payload = {"type": "event", "data": event.model_dump()}
    # Fire-and-forget
    for ws in list(_clients):
        asyncio.create_task(_send_safe(ws, payload))


# PUBLIC_INTERFACE
def broadcast_analytics_delta(summary: AnalyticsSummary):
    """Broadcast a lightweight analytics delta to connected clients."""
    payload = {"type": "analytics_delta", "data": summary.model_dump()}
    for ws in list(_clients):
        asyncio.create_task(_send_safe(ws, payload))
