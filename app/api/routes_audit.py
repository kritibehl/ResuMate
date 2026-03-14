from fastapi import APIRouter, Depends

from app.auth.dependencies import require_admin
from app.schemas.audit import AuditEvent, AuditListResponse
from app.storage.repositories.audit import AuditRepository

router = APIRouter(tags=["audit"])
repo = AuditRepository()


@router.get("/audit", response_model=AuditListResponse)
def list_audit_events(_actor=Depends(require_admin)) -> AuditListResponse:
    items = [AuditEvent.model_validate(item) for item in repo.list_events()]
    return AuditListResponse(items=items)
