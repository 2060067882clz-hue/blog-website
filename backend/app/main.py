from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.router import api_router
from app.core.config import settings
from app.core.database import mysql_database
from app.core.exceptions import register_exception_handlers


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Blog website backend service",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_router)

    if settings.use_mysql:
        @app.on_event("startup")
        def initialize_mysql() -> None:
            mysql_database.initialize()

    @app.get("/", tags=["root"])
    async def root() -> dict:
        return {
            "success": True,
            "data": {
                "message": f"{settings.app_name} is running",
                "version": settings.app_version,
            },
        }

    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
