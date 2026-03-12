from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.storage.repositories.batches import BatchRepository
from app.storage.repositories.jobs import JobRepository

router = APIRouter(tags=["dashboard"])

job_repo = JobRepository()
batch_repo = BatchRepository()


class DashboardSummaryResponse(BaseModel):
    total_jobs: int
    total_batches: int
    avg_processing_time_ms: float
    success_rate: float


class DashboardJobItem(BaseModel):
    job_id: str
    status: str
    created_at: str
    updated_at: str
    input_fingerprint: str
    retry_count: int = 0


class DashboardJobsResponse(BaseModel):
    items: list[DashboardJobItem] = Field(default_factory=list)


class StabilityItem(BaseModel):
    input_fingerprint: str
    repeat_count: int
    job_ids: list[str] = Field(default_factory=list)


class DashboardStabilityResponse(BaseModel):
    items: list[StabilityItem] = Field(default_factory=list)


@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary() -> DashboardSummaryResponse:
    jobs = job_repo.list_jobs()
    batches = batch_repo.list_batches()

    total_jobs = len(jobs)
    total_batches = len(batches)
    avg_processing_time_ms = (
        round(sum(job.get("processing_time_ms", 0) for job in jobs) / total_jobs, 2)
        if total_jobs
        else 0.0
    )
    completed_jobs = sum(1 for job in jobs if job.get("status") == "completed")
    success_rate = round(completed_jobs / total_jobs, 2) if total_jobs else 0.0

    return DashboardSummaryResponse(
        total_jobs=total_jobs,
        total_batches=total_batches,
        avg_processing_time_ms=avg_processing_time_ms,
        success_rate=success_rate,
    )


@router.get("/dashboard/jobs", response_model=DashboardJobsResponse)
def get_dashboard_jobs() -> DashboardJobsResponse:
    items = [
        DashboardJobItem(
            job_id=job["job_id"],
            status=job["status"],
            created_at=job["created_at"].isoformat(),
            updated_at=job["updated_at"].isoformat(),
            input_fingerprint=job["input_fingerprint"],
            retry_count=job.get("retry_count", 0),
        )
        for job in job_repo.list_jobs()[:20]
    ]
    return DashboardJobsResponse(items=items)


@router.get("/dashboard/stability", response_model=DashboardStabilityResponse)
def get_dashboard_stability() -> DashboardStabilityResponse:
    groups: dict[str, list[str]] = {}

    for job in job_repo.list_jobs():
        fingerprint = job["input_fingerprint"]
        groups.setdefault(fingerprint, []).append(job["job_id"])

    items = [
        StabilityItem(
            input_fingerprint=fingerprint,
            repeat_count=len(job_ids),
            job_ids=job_ids,
        )
        for fingerprint, job_ids in groups.items()
    ]
    items.sort(key=lambda item: item.repeat_count, reverse=True)

    return DashboardStabilityResponse(items=items)
