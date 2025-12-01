import csv
import io
from typing import Dict

from src.api.models import Report, compute_summary


# PUBLIC_INTERFACE
def export_report_json(report: Report) -> Dict:
    """Return a JSON export for the report containing sessions and analytics summaries."""
    summary = compute_summary(report.sessions, heatmap_scaling="auto")
    return {
        "report": report.model_dump(),
        "analytics": summary.model_dump(),
    }


# PUBLIC_INTERFACE
def export_report_csv(report: Report) -> str:
    """Return a CSV text containing flattened analytics data suitable for spreadsheets."""
    summary = compute_summary(report.sessions, heatmap_scaling="auto")

    out = io.StringIO()
    writer = csv.writer(out)

    writer.writerow(["Section", "Key", "SubKey", "Value"])

    # Counts
    for b, c in summary.counts_by_behavior.items():
        writer.writerow(["counts_by_behavior", b, "", c])

    # Durations
    for b, d in summary.durations_by_behavior.items():
        writer.writerow(["durations_by_behavior", b, "", round(d, 2)])

    # Trendlines
    for b, points in summary.trendlines.items():
        for minute_iso, count in points:
            writer.writerow(["trendlines", b, minute_iso, count])

    # Heatmap
    for cam, bins in summary.heatmap.items():
        for minute_iso, count in bins.items():
            writer.writerow(["heatmap", cam, minute_iso, count])

    # Metadata
    for k, v in summary.heatmap_meta.items():
        writer.writerow(["heatmap_meta", k, "", v])

    return out.getvalue()
