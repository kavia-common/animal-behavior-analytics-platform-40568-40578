from typing import List

from fastapi import APIRouter, HTTPException, Response

from src.api.models import REPORTS, Report
from src.api.utils.exporters import export_report_json, export_report_csv

router = APIRouter(prefix="", tags=["Reports"])


# PUBLIC_INTERFACE
@router.get("/reports", summary="List reports")
def list_reports() -> List[Report]:
    """Return all saved reports."""
    return list(REPORTS.values())


# PUBLIC_INTERFACE
@router.get("/reports/{report_id}", summary="Get report")
def get_report(report_id: str) -> Report:
    """Return a report by id."""
    if report_id not in REPORTS:
        raise HTTPException(status_code=404, detail="Report not found")
    return REPORTS[report_id]


# PUBLIC_INTERFACE
@router.get(
    "/export/reports/{report_id}.json",
    summary="Export report as JSON",
    responses={200: {"content": {"application/json": {}}}},
)
def export_report_as_json(report_id: str):
    """Return a JSON export of the report, including chart-ready data."""
    if report_id not in REPORTS:
        raise HTTPException(status_code=404, detail="Report not found")
    return export_report_json(REPORTS[report_id])


# PUBLIC_INTERFACE
@router.get(
    "/export/reports/{report_id}.csv",
    summary="Export report as CSV",
    responses={200: {"content": {"text/csv": {}}}},
)
def export_report_as_csv(report_id: str):
    """Return a CSV export of the report, including chart-ready data."""
    if report_id not in REPORTS:
        raise HTTPException(status_code=404, detail="Report not found")
    csv_text = export_report_csv(REPORTS[report_id])
    return Response(content=csv_text, media_type="text/csv")
