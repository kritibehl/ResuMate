from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str


class GapItem(BaseModel):
    requirement_id: str
    requirement_text: str
    gap_type: Literal["missing", "weak", "partial"] = "missing"
    reason: str


class MatchedRequirement(BaseModel):
    requirement_id: str
    requirement_text: str
    coverage: Literal["none", "partial", "full"]
    evidence: list[str] = Field(default_factory=list)
    confidence: float


class AnalysisResult(BaseModel):
    coverage_score: float = 0.0
    matched_requirements: list[MatchedRequirement] = Field(default_factory=list)
    gaps: list[GapItem] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)


class JobResponse(BaseModel):
    job_id: str
    status: Literal["completed", "failed"]
    schema_version: str = "1.0.0"
    created_at: datetime
    processing_time_ms: int = 0
    input_fingerprint: str
    analysis: AnalysisResult = Field(default_factory=AnalysisResult)
    errors: list[ErrorDetail] = Field(default_factory=list)


class BatchResponse(BaseModel):
    batch_id: str
    status: Literal["queued", "running", "failed", "completed"] = "completed"
    total_jobs: int
    success_count: int
    failure_count: int
    job_ids: list[str] = Field(default_factory=list)
    created_at: datetime


class VersionRecordResponse(BaseModel):
    version_id: str
    document_name: str
    reference_name: str
    input_fingerprint: str
    created_at: datetime


class VersionListResponse(BaseModel):
    items: list[VersionRecordResponse] = Field(default_factory=list)


class HistoryItemResponse(BaseModel):
    job_id: str
    created_at: datetime
    document_name: str
    reference_name: str
    input_fingerprint: str
    status: str


class HistoryListResponse(BaseModel):
    items: list[HistoryItemResponse] = Field(default_factory=list)
