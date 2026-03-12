from fastapi import APIRouter

from app.schemas.response import VersionListResponse, VersionRecordResponse
from app.storage.repositories.versions import VersionRepository

router = APIRouter(tags=["versions"])
repo = VersionRepository()


@router.get("/versions", response_model=VersionListResponse)
def get_versions() -> VersionListResponse:
    items = [VersionRecordResponse.model_validate(item) for item in repo.list_versions()]
    return VersionListResponse(items=items)
