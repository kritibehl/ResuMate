from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.export import ExportFormat, ExportResponse
from app.services.diff_service import compare_jobs
from app.services.export_service import export_job
from app.storage.repositories.jobs import JobRepository

router = APIRouter(tags=["exports"])
job_repo = JobRepository()


class DiffRequest(BaseModel):
    left_job_id: str
    right_job_id: str


class ExportRequest(BaseModel):
    format: ExportFormat


@router.post("/diff")
def diff_jobs(payload: DiffRequest):
    left = job_repo.get_job_by_id(payload.left_job_id)
    right = job_repo.get_job_by_id(payload.right_job_id)

    if not left or not right:
        raise HTTPException(status_code=404, detail="One or both jobs not found")

    return compare_jobs(left, right)


@router.post("/exports/job/{job_id}", response_model=ExportResponse)
def export_job_route(job_id: str, payload: ExportRequest) -> ExportResponse:
    job = job_repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return export_job(job, payload.format)
