from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from src.api.models import (
    REPORTS,
    AnalyticsSummary,
    BaselineComparison,
    DiversityIndexResult,
    compute_baseline_comparison,
    compute_diversity_index,
    compute_summary,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# PUBLIC_INTERFACE
@router.get(
    "/summary",
    summary="Analytics summary",
    response_model=AnalyticsSummary,
    description="Compute counts, durations, trendlines, and heatmap bins for given sessions. "
    "Supports heatmap scaling modes: fixed, auto (default), and session.",
)
def analytics_summary(
    sessionId: Optional[List[str]] = Query(default=None, alias="sessionId"),
    reportId: Optional[str] = Query(default=None, alias="reportId"),
    heatmapScaling: str = Query(default="auto", pattern="^(fixed|auto|session)$", alias="heatmapScaling"),
):
    """Return analytics summary for provided session IDs (or a report's sessions)."""
    sessions: List[str]
    if reportId:
        if reportId not in REPORTS:
            raise HTTPException(status_code=404, detail="Report not found")
        sessions = REPORTS[reportId].sessions
    else:
        sessions = sessionId or []
        if not sessions:
            raise HTTPException(status_code=400, detail="sessionId or reportId is required")

    return compute_summary(sessions, heatmap_scaling=heatmapScaling)


# PUBLIC_INTERFACE
@router.get(
    "/baseline-comparison",
    summary="Baseline comparison",
    response_model=BaselineComparison,
)
def baseline_comparison(sessionId: str, baselineId: str):
    """Compare a target session to a baseline session, returning percent deltas and notable flags."""
    return compute_baseline_comparison(sessionId, baselineId)


# PUBLIC_INTERFACE
@router.get(
    "/diversity-index",
    summary="Behavior diversity index",
    response_model=DiversityIndexResult,
)
def diversity_index(sessionId: str):
    """Compute Shannon-like diversity index over behavior time share for a session."""
    return compute_diversity_index(sessionId)
