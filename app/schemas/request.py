from typing import Literal

from pydantic import BaseModel, Field


DocumentType = Literal["resume", "document", "cover_letter", "other"]
ReferenceType = Literal["job_description", "rubric", "document", "other"]


class JobMetadata(BaseModel):
    document_name: str | None = None
    reference_name: str | None = None


class JobCreateRequest(BaseModel):
    document_text: str = Field(..., min_length=1)
    reference_text: str = Field(..., min_length=1)
    document_type: DocumentType = "resume"
    reference_type: ReferenceType = "job_description"
    metadata: JobMetadata = Field(default_factory=JobMetadata)
