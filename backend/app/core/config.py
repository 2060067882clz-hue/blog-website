from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings

# backend 根目录，用于稳定定位 .env 文件。
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """集中管理项目运行配置，避免硬编码散落在各文件中。"""

    app_name: str = "Blog Backend"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = "*"
    secret_key: str = "change-this-before-production"
    access_token_expire_minutes: int = 120
    demo_user_username: str = "admin"
    demo_user_password: str = "Admin123456"
    demo_user_display_name: str = "Demo Admin"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        # 兼容 `*` 和逗号分隔两种配置写法。
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    # 配置只初始化一次，避免重复读取环境变量。
    return Settings()
