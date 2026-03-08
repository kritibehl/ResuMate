from fastapi import APIRouter, HTTPException

from app.api.routes_jobs import _IN_MEMORY_JOBS
from app.schemas.export import DiffRequest, DiffResponse, ExportRequest, ExportResponse
from app.services.diff_service import compare_jobs
from app.services.export_service import export_job

router = APIRouter(tags=["exports"])


@router.post("/diff", response_model=DiffResponse)
def diff_jobs(payload: DiffRequest) -> DiffResponse:
    left_job = _IN_MEMORY_JOBS.get(payload.left_job_id)
    right_job = _IN_MEMORY_JOBS.get(payload.right_job_id)

    if not left_job:
        raise HTTPException(status_code=404, detail="Left job not found")
    if not right_job:
        raise HTTPException(status_code=404, detail="Right job not found")

    return compare_jobs(left_job, right_job)


@router.post("/exports/job/{job_id}", response_model=ExportResponse)
def export_job_route(job_id: str, payload: ExportRequest) -> ExportResponse:
    job = _IN_MEMORY_JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return export_job(job, payload.format)
