from fastapi import APIRouter

from app.core.config import settings
from app.schemas.common import HealthResponse, HealthData

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(
        success=True,
        data=HealthData(
            service=settings.app_name,
            version=settings.app_version,
            status="ok",
        ),
    )
