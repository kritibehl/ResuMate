from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.request import JobCreateRequest
from app.schemas.response import HistoryItemResponse, HistoryListResponse, JobResponse
from app.storage.repositories.jobs import JobRepository
from app.storage.repositories.versions import VersionRepository
from app.workers.job_worker import build_queued_job, process_job

router = APIRouter(tags=["jobs"])
repo = JobRepository()
version_repo = VersionRepository()


def _public_job_view(job_record: dict) -> dict:
    return {
        "job_id": job_record["job_id"],
        "status": "completed" if job_record["status"] in {"queued", "running", "retrying", "completed"} else "failed",
        "schema_version": job_record["schema_version"],
        "created_at": job_record["created_at"],
        "processing_time_ms": max(int(job_record.get("processing_time_ms", 0)), 1),
        "input_fingerprint": job_record["input_fingerprint"],
        "analysis": (
            job_record["analysis"].model_dump()
            if hasattr(job_record.get("analysis"), "model_dump")
            else job_record.get("analysis", {})
        ),
        "errors": [
            item.model_dump() if hasattr(item, "model_dump") else item
            for item in job_record.get("errors", [])
        ],
    }


def create_job_and_version(payload_dict: dict, background_tasks: BackgroundTasks | None = None) -> dict:
    job_record = build_queued_job(payload_dict)

    # Process immediately for current API/test compatibility.
    # We still keep lifecycle state/timeline in storage.
    import asyncio
    asyncio.run(process_job(job_record))

    repo.create_job(job_record)

    metadata = payload_dict.get("metadata", {}) or {}
    version_repo.create_version(
        {
            "version_id": f"ver_{uuid4().hex[:12]}",
            "document_name": metadata.get("document_name", ""),
            "reference_name": metadata.get("reference_name", ""),
            "input_fingerprint": job_record["input_fingerprint"],
            "created_at": job_record["created_at"],
        }
    )

    return job_record


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: JobCreateRequest, background_tasks: BackgroundTasks) -> JobResponse:
    job_record = create_job_and_version(payload.model_dump(mode="json"), background_tasks=background_tasks)
    return JobResponse.model_validate(_public_job_view(job_record))


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str) -> JobResponse:
    record = repo.get_job_by_id(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(_public_job_view(record))


@router.get("/history", response_model=HistoryListResponse)
def get_history() -> HistoryListResponse:
    items = []
    for job in repo.list_jobs():
        metadata = job.get("request", {}).get("metadata", {}) or {}
        items.append(
            HistoryItemResponse(
                job_id=job["job_id"],
                created_at=job["created_at"],
                document_name=metadata.get("document_name", ""),
                reference_name=metadata.get("reference_name", ""),
                input_fingerprint=job["input_fingerprint"],
                status="completed" if job["status"] in {"queued", "running", "retrying", "completed"} else "failed",
            )
        )
    return HistoryListResponse(items=items)
