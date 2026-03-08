from fastapi import APIRouter

from app.api.routes_batches import _IN_MEMORY_BATCHES
from app.api.routes_jobs import _IN_MEMORY_JOBS
from app.services.metrics_service import build_summary, recent_jobs
from app.services.stability_service import build_stability_report

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/summary")
def dashboard_summary() -> dict:
    return build_summary(_IN_MEMORY_JOBS, _IN_MEMORY_BATCHES)


@router.get("/dashboard/jobs")
def dashboard_jobs() -> dict:
    return {"items": recent_jobs(_IN_MEMORY_JOBS)}


@router.get("/dashboard/stability")
def dashboard_stability() -> dict:
    return {"items": build_stability_report(_IN_MEMORY_JOBS)}
