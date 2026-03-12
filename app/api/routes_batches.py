from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from app.api.routes_jobs import create_job_and_version
from app.schemas.request import JobCreateRequest
from app.schemas.response import BatchResponse
from app.storage.repositories.batches import BatchRepository

router = APIRouter(tags=["batches"])
repo = BatchRepository()


class BatchCreateRequest(BaseModel):
    jobs: list[JobCreateRequest] = Field(default_factory=list)


@router.post("/batches", response_model=BatchResponse)
def create_batch(payload: BatchCreateRequest, background_tasks: BackgroundTasks) -> BatchResponse:
    created_jobs = []
    for job in payload.jobs:
        created_jobs.append(
            create_job_and_version(
                job.model_dump(mode="json"),
                background_tasks=background_tasks,
            )
        )

    batch_record = {
        "batch_id": f"batch_{uuid4().hex[:12]}",
        "status": "completed",
        "total_jobs": len(created_jobs),
        "success_count": len(created_jobs),
        "failure_count": 0,
        "job_ids": [job["job_id"] for job in created_jobs],
        "created_at": datetime.now(timezone.utc),
    }
    repo.create_batch(batch_record)
    return BatchResponse.model_validate(batch_record)


@router.get("/batches/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: str) -> BatchResponse:
    record = repo.get_batch_by_id(batch_id)
    if not record:
        raise HTTPException(status_code=404, detail="Batch not found")
    return BatchResponse.model_validate(record)
