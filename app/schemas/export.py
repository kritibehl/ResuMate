from typing import Literal

from pydantic import BaseModel, Field


ExportFormat = Literal["json", "markdown"]


class ExportRequest(BaseModel):
    format: ExportFormat = "json"


class ExportResponse(BaseModel):
    export_id: str
    format: ExportFormat
    content: str


class DiffRequest(BaseModel):
    left_job_id: str
    right_job_id: str


class DiffResponse(BaseModel):
    left_job_id: str
    right_job_id: str
    coverage_score_change: float
    added_requirements: list[str] = Field(default_factory=list)
    removed_requirements: list[str] = Field(default_factory=list)
    changed_suggestions: list[str] = Field(default_factory=list)
