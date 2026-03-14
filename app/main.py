from fastapi import FastAPI

from app.api.routes_audit import router as audit_router
from app.api.routes_batches import router as batches_router
from app.api.routes_dashboard import router as dashboard_router
from app.api.routes_exports import router as exports_router
from app.api.routes_health import router as health_router
from app.api.routes_jobs import router as jobs_router
from app.api.routes_versions import router as versions_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API-first workflow engine for structured document analysis and repeatable automation.",
)

app.include_router(health_router)
app.include_router(jobs_router, prefix=settings.api_prefix)
app.include_router(batches_router, prefix=settings.api_prefix)
app.include_router(versions_router, prefix=settings.api_prefix)
app.include_router(exports_router, prefix=settings.api_prefix)
app.include_router(dashboard_router, prefix=settings.api_prefix)
app.include_router(audit_router, prefix=settings.api_prefix)
