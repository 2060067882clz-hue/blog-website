from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Blog Website Backend")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    db_backend: str = os.getenv("DB_BACKEND", "memory").lower()
    mysql_host: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "123456")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "blog_website")
    mysql_charset: str = os.getenv("MYSQL_CHARSET", "utf8mb4")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
    demo_admin_username: str = os.getenv("DEMO_ADMIN_USERNAME", "admin")
    demo_admin_password: str = os.getenv("DEMO_ADMIN_PASSWORD", "Admin123456")
    demo_admin_email: str = os.getenv("DEMO_ADMIN_EMAIL", "admin@example.com")
    demo_admin_nickname: str = os.getenv("DEMO_ADMIN_NICKNAME", "博客管理员")

    @property
    def use_mysql(self) -> bool:
        return self.db_backend == "mysql"


settings = Settings()
