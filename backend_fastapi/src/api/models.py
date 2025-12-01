from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class Animal(BaseModel):
    """Animal metadata."""

    id: str = Field(..., description="Unique identifier for the animal.")
    name: str = Field(..., description="Display name.")
    species: str = Field(..., description="Species.")
    age_years: float = Field(..., description="Age in years.")
    tags: List[str] = Field(default_factory=list, description="Arbitrary tags.")


# PUBLIC_INTERFACE
class Behavior(BaseModel):
    """Behavior definition."""

    id: str = Field(..., description="Unique identifier for the behavior.")
    label: str = Field(..., description="Human readable name.")
    category: str = Field(..., description="Category for grouping.")
    color: str = Field(..., description="Recommended color for charts.")


# PUBLIC_INTERFACE
class BehaviorEvent(BaseModel):
    """An annotated behavior occurrence in a session timeline."""

    id: str = Field(..., description="Unique identifier for this event.")
    animal_id: str = Field(..., description="Animal identifier.")
    behavior_id: str = Field(..., description="Behavior identifier.")
    session_id: str = Field(..., description="Session identifier.")
    camera_id: str = Field(..., description="Camera identifier in the session.")
    start_ts: datetime = Field(..., description="Event start timestamp (UTC).")
    end_ts: datetime = Field(..., description="Event end timestamp (UTC).")
    confidence: float = Field(..., description="0-1 confidence score.")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Arbitrary metadata like annotator or marker.")


# PUBLIC_INTERFACE
class Report(BaseModel):
    """Saved report snapshot."""

    id: str = Field(..., description="Report ID.")
    name: str = Field(..., description="Report name.")
    sessions: List[str] = Field(..., description="Session IDs included.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    notes: Optional[str] = Field(None, description="Optional notes.")


# PUBLIC_INTERFACE
class AnalyticsSummary(BaseModel):
    """Summary analytics for given sessions."""

    sessions: List[str] = Field(..., description="Session IDs considered in this summary.")
    counts_by_behavior: Dict[str, int] = Field(..., description="Event counts by behavior id.")
    durations_by_behavior: Dict[str, float] = Field(..., description="Total durations (seconds) by behavior id.")
    trendlines: Dict[str, List[Tuple[str, int]]] = Field(
        ..., description="Behavior trend lines as (ISO minute bin start, count)."
    )
    heatmap: Dict[str, Dict[str, int]] = Field(
        ..., description="Heatmap bins: camera_id -> minute_iso -> count."
    )
    heatmap_meta: Dict[str, str] = Field(
        ..., description="Metadata describing scaling mode and thresholds."
    )


# PUBLIC_INTERFACE
class BaselineComparison(BaseModel):
    """Comparison metrics between a target session and a baseline session."""

    session_id: str = Field(..., description="Target session id.")
    baseline_id: str = Field(..., description="Baseline session id.")
    metric_deltas: Dict[str, Dict[str, float]] = Field(
        ..., description="Per behavior: count_delta_pct, duration_delta_pct."
    )
    notable_flags: List[str] = Field(..., description="Human-readable flags for significant changes.")


# PUBLIC_INTERFACE
class DiversityIndexResult(BaseModel):
    """Shannon-like diversity index computed over behavior frequencies or time share."""

    session_id: str = Field(..., description="Session id.")
    index: float = Field(..., description="Shannon-like entropy score (0 = single behavior).")
    max_index: float = Field(..., description="Theoretical max for n behaviors observed.")
    normalized: float = Field(..., description="Index normalized to 0..1 by max_index.")
    color_band: str = Field(..., description="Qualitative band mapping to UI color.")
    interpretation: str = Field(..., description="Guidance for interpreting the index.")
    support: Dict[str, float] = Field(..., description="Behavior -> proportion used for computation.")


# In-memory repositories with seed data enabling multi-camera synchronized playback

ANIMALS: Dict[str, Animal] = {}
BEHAVIORS: Dict[str, Behavior] = {}
EVENTS: List[BehaviorEvent] = []
REPORTS: Dict[str, Report] = {}


def _seed_data():
    # Animals
    ANIMALS["a-1"] = Animal(id="a-1", name="Luna", species="Canis familiaris", age_years=4.2, tags=["alpha", "gps"])
    ANIMALS["a-2"] = Animal(id="a-2", name="Milo", species="Felis catus", age_years=2.1, tags=["indoor"])
    ANIMALS["a-3"] = Animal(id="a-3", name="Koda", species="Ursus arctos", age_years=7.0, tags=["wild", "collared"])

    # Behaviors
    BEHAVIORS["b-rest"] = Behavior(id="b-rest", label="Resting", category="State", color="#6B7280")
    BEHAVIORS["b-feed"] = Behavior(id="b-feed", label="Feeding", category="Activity", color="#10B981")
    BEHAVIORS["b-play"] = Behavior(id="b-play", label="Play", category="Activity", color="#3B82F6")
    BEHAVIORS["b-groom"] = Behavior(id="b-groom", label="Grooming", category="Maintenance", color="#F59E0B")
    BEHAVIORS["b-alert"] = Behavior(id="b-alert", label="Alert", category="State", color="#EF4444")

    # Sessions implicitly referenced below: s-100, s-101, s-200 with camera ids per session

    base = datetime(2024, 1, 1, 12, 0, 0)
    eid = 1

    # Helper to create event with synchronized timestamps across cameras
    def add_event(animal_id: str, behavior_id: str, session_id: str, camera_id: str, start: datetime, dur_s: int, conf=0.9):
        nonlocal eid
        EVENTS.append(
            BehaviorEvent(
                id=f"e-{eid}",
                animal_id=animal_id,
                behavior_id=behavior_id,
                session_id=session_id,
                camera_id=camera_id,
                start_ts=start,
                end_ts=start + timedelta(seconds=dur_s),
                confidence=conf,
                metadata={"annotator": "seed", "marker": "sync"}
            )
        )
        eid += 1

    # Seed synchronized windows for s-100 with two cameras
    for i in range(12):  # 12 minutes window
        t = base + timedelta(minutes=i)
        # cam-A sees feeding/resting alternating
        add_event("a-1", "b-feed" if i % 2 == 0 else "b-rest", "s-100", "cam-A", t, 40 if i % 2 == 0 else 55)
        # cam-B sees play/grooming pattern
        add_event("a-1", "b-play" if i % 3 == 0 else "b-groom", "s-100", "cam-B", t + timedelta(seconds=5), 35)

    # Baseline session s-101 similar but with fewer feeding and more resting
    for i in range(12):
        t = base + timedelta(minutes=i)
        add_event("a-1", "b-rest" if i % 2 == 0 else "b-feed", "s-101", "cam-A", t, 50)
        add_event("a-1", "b-groom" if i % 3 == 0 else "b-play", "s-101", "cam-B", t + timedelta(seconds=6), 30)

    # Different session s-200 single camera with alerts
    for i in range(8):
        t = base + timedelta(minutes=i)
        add_event("a-3", "b-alert" if i % 4 == 0 else "b-rest", "s-200", "cam-C", t, 20 if i % 4 == 0 else 45, conf=0.8)

    # Reports
    REPORTS["r-1"] = Report(
        id="r-1",
        name="Daily Summary - Luna",
        sessions=["s-100", "s-101"],
        created_at=base + timedelta(hours=1),
        notes="Preview report with baseline comparison."
    )
    REPORTS["r-2"] = Report(
        id="r-2",
        name="Alert Monitor - Koda",
        sessions=["s-200"],
        created_at=base + timedelta(hours=2),
        notes="High alert frequency check."
    )


_seed_data()


# Utility analytics

def _events_for_sessions(session_ids: List[str]) -> List[BehaviorEvent]:
    return [e for e in EVENTS if e.session_id in set(session_ids)]


def _bin_key_minute(ts: datetime) -> str:
    return ts.replace(second=0, microsecond=0).isoformat()


# PUBLIC_INTERFACE
def compute_summary(
    session_ids: List[str],
    heatmap_scaling: str = "auto",  # fixed | auto | session
) -> AnalyticsSummary:
    """Compute basic summary metrics for the provided sessions.

    heatmap_scaling:
      - fixed: use a fixed 0..10 scale
      - auto: normalize to global min/max of these sessions
      - session: normalize per-session maxima
    """
    evs = _events_for_sessions(session_ids)
    counts: Dict[str, int] = {}
    durations: Dict[str, float] = {}
    trendlines: Dict[str, Dict[str, int]] = {}
    heatmap: Dict[str, Dict[str, int]] = {}

    for e in evs:
        counts[e.behavior_id] = counts.get(e.behavior_id, 0) + 1
        dur = (e.end_ts - e.start_ts).total_seconds()
        durations[e.behavior_id] = durations.get(e.behavior_id, 0.0) + dur

        # trendline per behavior per minute
        minute = _bin_key_minute(e.start_ts)
        if e.behavior_id not in trendlines:
            trendlines[e.behavior_id] = {}
        trendlines[e.behavior_id][minute] = trendlines[e.behavior_id].get(minute, 0) + 1

        # heatmap per camera per minute
        if e.camera_id not in heatmap:
            heatmap[e.camera_id] = {}
        heatmap[e.camera_id][minute] = heatmap[e.camera_id].get(minute, 0) + 1

    # Convert trendlines dict->list sorted
    tl_out: Dict[str, List[Tuple[str, int]]] = {}
    for b, series in trendlines.items():
        tl_out[b] = sorted(series.items(), key=lambda x: x[0])

    # Heatmap scaling metadata
    all_vals = [v for cam in heatmap.values() for v in cam.values()]
    max_val = max(all_vals) if all_vals else 1
    meta: Dict[str, str] = {"scaling": heatmap_scaling}
    if heatmap_scaling == "fixed":
        meta.update({"min": "0", "max": "10", "palette": "viridis"})
    elif heatmap_scaling == "session":
        # compute per-session maxima
        session_peaks: Dict[str, int] = {}
        for s in session_ids:
            session_vals = [1 for e in evs if e.session_id == s]  # simple density proxy
            session_peaks[s] = max(session_vals) if session_vals else 1
        meta.update({f"session_max_{s}": str(v) for s, v in session_peaks.items()})
        meta["palette"] = "magma"
    else:
        # auto
        meta.update({"min": "0", "max": str(max_val), "palette": "plasma"})

    return AnalyticsSummary(
        sessions=session_ids,
        counts_by_behavior=counts,
        durations_by_behavior=durations,
        trendlines=tl_out,
        heatmap=heatmap,
        heatmap_meta=meta,
    )


# PUBLIC_INTERFACE
def compute_baseline_comparison(session_id: str, baseline_id: str) -> BaselineComparison:
    """Compute percent deltas for counts and durations between a session and its baseline."""
    def agg(session: str) -> Tuple[Dict[str, int], Dict[str, float]]:
        evs = _events_for_sessions([session])
        counts: Dict[str, int] = {}
        durations: Dict[str, float] = {}
        for e in evs:
            counts[e.behavior_id] = counts.get(e.behavior_id, 0) + 1
            dur = (e.end_ts - e.start_ts).total_seconds()
            durations[e.behavior_id] = durations.get(e.behavior_id, 0.0) + dur
        return counts, durations

    c_t, d_t = agg(session_id)
    c_b, d_b = agg(baseline_id)
    all_behaviors: Set[str] = set(c_t) | set(c_b) | set(d_t) | set(d_b)

    deltas: Dict[str, Dict[str, float]] = {}
    flags: List[str] = []
    for b in all_behaviors:
        ct = float(c_t.get(b, 0))
        cb = float(c_b.get(b, 0))
        dt = float(d_t.get(b, 0.0))
        db = float(d_b.get(b, 0.0))
        count_delta_pct = ((ct - cb) / cb * 100.0) if cb > 0 else (100.0 if ct > 0 else 0.0)
        dur_delta_pct = ((dt - db) / db * 100.0) if db > 0 else (100.0 if dt > 0 else 0.0)
        deltas[b] = {"count_delta_pct": round(count_delta_pct, 2), "duration_delta_pct": round(dur_delta_pct, 2)}

        # Flag notable changes
        if count_delta_pct >= 50:
            flags.append(f"Significant increase in {b} (+{round(count_delta_pct)}%).")
        if count_delta_pct <= -50:
            flags.append(f"Significant decrease in {b} ({round(count_delta_pct)}%).")

    return BaselineComparison(session_id=session_id, baseline_id=baseline_id, metric_deltas=deltas, notable_flags=flags)


# PUBLIC_INTERFACE
def compute_diversity_index(session_id: str) -> DiversityIndexResult:
    """Compute Shannon-like entropy H = -sum(p_i * ln p_i), normalized by ln(N)."""
    import math

    evs = _events_for_sessions([session_id])
    total_duration = sum((e.end_ts - e.start_ts).total_seconds() for e in evs) or 1.0
    by_behavior: Dict[str, float] = {}
    for e in evs:
        by_behavior[e.behavior_id] = by_behavior.get(e.behavior_id, 0.0) + (e.end_ts - e.start_ts).total_seconds()

    proportions: Dict[str, float] = {b: v / total_duration for b, v in by_behavior.items() if v > 0}
    n = max(len(proportions), 1)
    H = -sum(p * math.log(p) for p in proportions.values()) if proportions else 0.0
    H_max = math.log(n)
    normalized = (H / H_max) if H_max > 0 else 0.0

    # Map to color bands
    if normalized < 0.33:
        color = "low:red"
        interp = "Low diversity: dominated by few behaviors."
    elif normalized < 0.66:
        color = "medium:amber"
        interp = "Moderate diversity: mixed behavior profile."
    else:
        color = "high:green"
        interp = "High diversity: balanced behavior distribution."

    return DiversityIndexResult(
        session_id=session_id,
        index=round(H, 4),
        max_index=round(H_max, 4),
        normalized=round(normalized, 4),
        color_band=color,
        interpretation=interp,
        support=proportions,
    )
