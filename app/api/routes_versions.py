from fastapi import APIRouter

from app.api.routes_jobs import _IN_MEMORY_VERSIONS
from app.schemas.domain import VersionRecord, VersionsResponse

router = APIRouter(tags=["versions"])


@router.get("/versions", response_model=VersionsResponse)
def list_versions() -> VersionsResponse:
    items = sorted(
        _IN_MEMORY_VERSIONS.values(),
        key=lambda item: item["created_at"],
        reverse=True,
    )
    return VersionsResponse(items=[VersionRecord.model_validate(item) for item in items])
