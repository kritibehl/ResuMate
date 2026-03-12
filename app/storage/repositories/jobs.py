from datetime import datetime, timezone
from typing import Any

from app.schemas.domain import JobStatus


_JOBS: dict[str, dict[str, Any]] = {}


class JobRepository:
    def create_job(self, job_record: dict[str, Any]) -> None:
        _JOBS[job_record["job_id"]] = job_record

    def get_job_by_id(self, job_id: str) -> dict[str, Any] | None:
        return _JOBS.get(job_id)

    def list_jobs(self) -> list[dict[str, Any]]:
        return sorted(
            _JOBS.values(),
            key=lambda item: item["created_at"],
            reverse=True,
        )

    def update_job(self, job_id: str, **updates: Any) -> dict[str, Any] | None:
        job = _JOBS.get(job_id)
        if not job:
            return None
        job.update(updates)
        job["updated_at"] = datetime.now(timezone.utc)
        return job

    def append_timeline(self, job_id: str, status: JobStatus, message: str | None = None) -> dict[str, Any] | None:
        job = _JOBS.get(job_id)
        if not job:
            return None
        job["status"] = status
        job["updated_at"] = datetime.now(timezone.utc)
        job.setdefault("timeline", []).append(
            {
                "status": status,
                "timestamp": datetime.now(timezone.utc),
                "message": message,
            }
        )
        return job
