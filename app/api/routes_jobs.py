from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.domain import HistoryItem, HistoryResponse, JobCreateResult, VersionRecord
from app.schemas.request import JobCreateRequest
from app.schemas.response import JobResponse
from app.services.analyzer import analyze_document
from app.utils.hashing import compute_input_fingerprint
from app.utils.timing import timed

router = APIRouter(tags=["jobs"])
_IN_MEMORY_JOBS: dict[str, dict] = {}
_IN_MEMORY_VERSIONS: dict[str, dict] = {}


def create_job_and_version(payload: JobCreateRequest) -> JobCreateResult:
    with timed() as timer:
        analysis, errors = analyze_document(
            document_text=payload.document_text,
            reference_text=payload.reference_text,
        )

    elapsed = timer.elapsed_ms
    if elapsed < 1:
        elapsed = 1

    fingerprint = compute_input_fingerprint(
        payload.document_text,
        payload.reference_text,
    )

    job = JobResponse(
        job_id=f"job_{uuid4().hex[:12]}",
        status="completed",
        created_at=datetime.now(timezone.utc),
        processing_time_ms=elapsed,
        input_fingerprint=fingerprint,
        analysis=analysis,
        errors=errors,
    )

    version = VersionRecord(
        version_id=f"ver_{uuid4().hex[:12]}",
        document_name=payload.metadata.document_name,
        reference_name=payload.metadata.reference_name,
        input_fingerprint=fingerprint,
        created_at=job.created_at,
    )

    _IN_MEMORY_JOBS[job.job_id] = {
        **job.model_dump(mode="json"),
        "request": payload.model_dump(mode="json"),
    }
    _IN_MEMORY_VERSIONS[version.version_id] = version.model_dump(mode="json")

    return JobCreateResult(job=job, version=version)


@router.post("/jobs", response_model=JobResponse)
def create_job(payload: JobCreateRequest) -> JobResponse:
    result = create_job_and_version(payload)
    return result.job


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str) -> JobResponse:
    record = _IN_MEMORY_JOBS.get(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(record)


@router.get("/history", response_model=HistoryResponse)
def get_history() -> HistoryResponse:
    items = sorted(
        _IN_MEMORY_JOBS.values(),
        key=lambda item: item["created_at"],
        reverse=True,
    )

    history_items = [
        HistoryItem(
            job_id=item["job_id"],
            created_at=item["created_at"],
            document_name=item.get("request", {}).get("metadata", {}).get("document_name"),
            reference_name=item.get("request", {}).get("metadata", {}).get("reference_name"),
            input_fingerprint=item["input_fingerprint"],
            status=item["status"],
        )
        for item in items
    ]

    return HistoryResponse(items=history_items)
