import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 兼容直接运行 `python app/main.py` 的场景，
# 手动把 backend 目录加入模块搜索路径。
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AppException


def create_application() -> FastAPI:
    # 统一在应用启动时读取配置，后续各模块按依赖注入复用。
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 允许前端项目在联调阶段直接跨域访问当前后端。
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 处理业务层主动抛出的自定义异常，保证返回格式统一。
    @app.exception_handler(AppException)
    async def handle_app_exception(_, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                },
            },
        )

    # 处理请求参数校验失败，例如字段缺失、长度不满足要求等。
    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(_, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed.",
                    "details": exc.errors(),
                },
            },
        )

    # 根路径主要用于快速确认服务是否已经正常启动。
    @app.get("/", tags=["root"])
    async def root() -> dict:
        return {
            "success": True,
            "message": "Blog backend is running.",
            "docs": "/docs",
        }

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    # 直接运行当前文件时，默认启动本地开发服务器,修改代码后自动重启。
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
