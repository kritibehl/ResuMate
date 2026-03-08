from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.errors import ErrorItem


CoverageLevel = Literal["strong", "partial", "none"]
GapType = Literal["missing", "partial", "unclear"]
JobStatus = Literal["completed", "failed"]


class MatchedRequirement(BaseModel):
    requirement_id: str
    requirement_text: str
    coverage: CoverageLevel
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class GapItem(BaseModel):
    requirement_id: str
    requirement_text: str
    gap_type: GapType
    reason: str


class AnalysisResult(BaseModel):
    coverage_score: float = 0.0
    matched_requirements: list[MatchedRequirement] = Field(default_factory=list)
    gaps: list[GapItem] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    schema_version: str = "1.0.0"
    created_at: datetime
    processing_time_ms: int
    input_fingerprint: str
    analysis: AnalysisResult
    errors: list[ErrorItem] = Field(default_factory=list)
