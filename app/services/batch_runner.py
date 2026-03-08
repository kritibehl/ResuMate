from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.domain import BatchCreateRequest, BatchResponse, JobCreateResult
from app.schemas.request import JobCreateRequest
from app.schemas.response import JobResponse
from app.services.analyzer import analyze_document
from app.utils.hashing import compute_input_fingerprint
from app.utils.timing import timed


def build_job(payload: JobCreateRequest) -> JobResponse:
    with timed() as timer:
        analysis, errors = analyze_document(
            document_text=payload.document_text,
            reference_text=payload.reference_text,
        )

    elapsed = timer.elapsed_ms
    if elapsed < 1:
        elapsed = 1

    return JobResponse(
        job_id=f"job_{uuid4().hex[:12]}",
        status="completed",
        created_at=datetime.now(timezone.utc),
        processing_time_ms=elapsed,
        input_fingerprint=compute_input_fingerprint(
            payload.document_text,
            payload.reference_text,
        ),
        analysis=analysis,
        errors=errors,
    )


def run_batch(batch_payload: BatchCreateRequest, create_one_fn) -> BatchResponse:
    job_ids: list[str] = []
    success_count = 0
    failure_count = 0

    for item in batch_payload.jobs:
        try:
            result: JobCreateResult = create_one_fn(item)
            job_ids.append(result.job.job_id)
            success_count += 1
        except Exception:
            failure_count += 1

    return BatchResponse(
        batch_id=f"batch_{uuid4().hex[:12]}",
        status="completed" if failure_count == 0 else "failed",
        total_jobs=len(batch_payload.jobs),
        success_count=success_count,
        failure_count=failure_count,
        job_ids=job_ids,
        created_at=datetime.now(timezone.utc),
    )
