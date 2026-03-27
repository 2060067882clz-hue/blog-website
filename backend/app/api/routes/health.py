from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import HealthResponse

# 健康检查路由，便于联调和部署时快速确认服务状态。
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        success=True,
        service=settings.app_name,
        version=settings.app_version,
        status="ok",
    )
