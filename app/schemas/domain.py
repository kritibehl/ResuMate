from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


JobStatus = Literal["queued", "running", "retrying", "failed", "completed"]


class JobTimelineEvent(BaseModel):
    status: JobStatus
    timestamp: datetime
    message: str | None = None


class StoredJobRecord(BaseModel):
    job_id: str
    status: JobStatus
    schema_version: str
    created_at: datetime
    updated_at: datetime
    processing_time_ms: int = 0
    input_fingerprint: str
    request: dict = Field(default_factory=dict)
    analysis: dict = Field(default_factory=dict)
    errors: list[dict] = Field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 2
    timeline: list[JobTimelineEvent] = Field(default_factory=list)
