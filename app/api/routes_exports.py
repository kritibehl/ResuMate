from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.dependencies import AuthContext, require_editor_or_admin
from app.schemas.export import ExportFormat, ExportResponse
from app.services.diff_service import compare_jobs
from app.services.export_service import export_job
from app.storage.repositories.audit import AuditRepository
from app.storage.repositories.jobs import JobRepository

router = APIRouter(tags=["exports"])
job_repo = JobRepository()
audit_repo = AuditRepository()


class DiffRequest(BaseModel):
    left_job_id: str
    right_job_id: str


class ExportRequest(BaseModel):
    format: ExportFormat


def log_export_event(
    actor: AuthContext,
    action: str,
    resource_type: str,
    resource_id: str,
    details: dict | None = None,
) -> None:
    audit_repo.create_event(
        {
            "event_id": f"audit_{uuid4().hex[:12]}",
            "actor_id": actor.user_id,
            "actor_role": actor.role,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "created_at": datetime.now(timezone.utc),
            "details": details or {},
        }
    )


@router.post("/diff")
def diff_jobs(payload: DiffRequest):
    left = job_repo.get_job_by_id(payload.left_job_id)
    right = job_repo.get_job_by_id(payload.right_job_id)

    if not left or not right:
        raise HTTPException(status_code=404, detail="One or both jobs not found")

    return compare_jobs(left, right)


@router.post("/exports/job/{job_id}", response_model=ExportResponse)
def export_job_route(
    job_id: str,
    payload: ExportRequest,
    actor: AuthContext = Depends(require_editor_or_admin),
) -> ExportResponse:
    job = job_repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    log_export_event(
        actor=actor,
        action="job.export",
        resource_type="job",
        resource_id=job_id,
        details={"format": payload.format},
    )

    return export_job(job, payload.format)
