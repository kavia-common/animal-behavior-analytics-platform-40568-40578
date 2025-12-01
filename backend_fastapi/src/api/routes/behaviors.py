from typing import List

from fastapi import APIRouter

from src.api.models import BEHAVIORS, Behavior

router = APIRouter(prefix="/behaviors", tags=["Behaviors"])


# PUBLIC_INTERFACE
@router.get("", summary="List behaviors")
def list_behaviors() -> List[Behavior]:
    """Return all behavior definitions."""
    return list(BEHAVIORS.values())
