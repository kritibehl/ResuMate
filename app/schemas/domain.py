from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.request import JobCreateRequest
from app.schemas.response import JobResponse


BatchStatus = Literal["pending", "running", "completed", "failed"]


class StoredJobRecord(BaseModel):
    job_id: str
    status: str
    schema_version: str
    created_at: datetime
    processing_time_ms: int
    input_fingerprint: str
    request: dict = Field(default_factory=dict)
    analysis: dict = Field(default_factory=dict)
    errors: list[dict] = Field(default_factory=list)


class BatchCreateRequest(BaseModel):
    jobs: list[JobCreateRequest] = Field(default_factory=list)


class BatchResponse(BaseModel):
    batch_id: str
    status: BatchStatus
    total_jobs: int
    success_count: int
    failure_count: int
    job_ids: list[str] = Field(default_factory=list)
    created_at: datetime


class HistoryItem(BaseModel):
    job_id: str
    created_at: datetime
    document_name: str | None = None
    reference_name: str | None = None
    input_fingerprint: str
    status: str


class HistoryResponse(BaseModel):
    items: list[HistoryItem] = Field(default_factory=list)


class VersionRecord(BaseModel):
    version_id: str
    document_name: str | None = None
    reference_name: str | None = None
    input_fingerprint: str
    created_at: datetime


class VersionsResponse(BaseModel):
    items: list[VersionRecord] = Field(default_factory=list)


class JobCreateResult(BaseModel):
    job: JobResponse
    version: VersionRecord
