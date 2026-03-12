from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.response import AnalysisResult
from app.services.analyzer import analyze_document
from app.utils.hashing import compute_input_fingerprint
from app.utils.timing import timed


def _append_timeline(job: dict, status: str, message: str | None = None) -> None:
    now = datetime.now(timezone.utc)
    job["status"] = status
    job["updated_at"] = now
    job.setdefault("timeline", []).append(
        {
            "status": status,
            "timestamp": now,
            "message": message,
        }
    )


async def process_job(job: dict) -> None:
    _append_timeline(job, "running", "Worker picked up queued job.")

    try:
        with timed() as timer:
            analysis, errors = analyze_document(
                document_text=job["request"]["document_text"],
                reference_text=job["request"]["reference_text"],
            )

        job["analysis"] = analysis
        job["errors"] = errors
        job["processing_time_ms"] = max(timer.elapsed_ms, 1)
        _append_timeline(job, "completed", "Job completed successfully.")
    except Exception as exc:
        retry_count = int(job.get("retry_count", 0))
        max_retries = int(job.get("max_retries", 2))

        if retry_count < max_retries:
            job["retry_count"] = retry_count + 1
            _append_timeline(job, "retrying", f"Retrying after error: {exc}")
            await process_job(job)
            return

        job["errors"] = [{"code": "worker_failed", "message": str(exc)}]
        job["analysis"] = AnalysisResult()
        _append_timeline(job, "failed", f"Job failed after retries: {exc}")


def build_queued_job(payload: dict) -> dict:
    now = datetime.now(timezone.utc)
    job_id = f"job_{uuid4().hex[:12]}"
    return {
        "job_id": job_id,
        "status": "queued",
        "schema_version": "1.0.0",
        "created_at": now,
        "updated_at": now,
        "processing_time_ms": 0,
        "input_fingerprint": compute_input_fingerprint(
            payload["document_text"],
            payload["reference_text"],
        ),
        "analysis": AnalysisResult(),
        "errors": [],
        "retry_count": 0,
        "max_retries": 2,
        "timeline": [
            {
                "status": "queued",
                "timestamp": now,
                "message": "Job accepted by API and queued for processing.",
            }
        ],
        "request": payload,
    }
