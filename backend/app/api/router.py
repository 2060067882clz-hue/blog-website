from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.articles import router as articles_router
from app.api.routes.auth import router as auth_router
from app.api.routes.comments import router as comments_router
from app.api.routes.health import router as health_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.api_v1_prefix)
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(articles_router, prefix="/articles", tags=["articles"])
api_router.include_router(comments_router, prefix="/comments", tags=["comments"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
