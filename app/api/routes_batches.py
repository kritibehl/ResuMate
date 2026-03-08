from fastapi import APIRouter

from app.api.routes_jobs import create_job_and_version
from app.schemas.domain import BatchCreateRequest, BatchResponse
from app.services.batch_runner import run_batch

router = APIRouter(tags=["batches"])
_IN_MEMORY_BATCHES: dict[str, dict] = {}


@router.post("/batches", response_model=BatchResponse)
def create_batch(payload: BatchCreateRequest) -> BatchResponse:
    batch = run_batch(payload, create_job_and_version)
    _IN_MEMORY_BATCHES[batch.batch_id] = batch.model_dump(mode="json")
    return batch


@router.get("/batches/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: str) -> BatchResponse:
    return BatchResponse.model_validate(_IN_MEMORY_BATCHES[batch_id])
