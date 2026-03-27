from functools import lru_cache

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthError
from app.repositories.token_repository import InMemoryTokenRepository
from app.repositories.user_repository import InMemoryUserRepository
from app.services.auth_service import AuthService

# Bearer 鉴权方案，供需要登录态的接口复用。
bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache()
def get_user_repository() -> InMemoryUserRepository:
    # 当前阶段先返回内存仓储，后续可平滑替换为数据库实现。
    return InMemoryUserRepository(get_settings())


@lru_cache()
def get_token_repository() -> InMemoryTokenRepository:
    # 当前阶段使用内存方式记录已退出的 token。
    return InMemoryTokenRepository()


def get_auth_service(
    settings: Settings = Depends(get_settings),
    user_repository: InMemoryUserRepository = Depends(get_user_repository),
    token_repository: InMemoryTokenRepository = Depends(get_token_repository),
) -> AuthService:
    # 在路由层统一组装认证服务，避免每个接口自己创建对象。
    return AuthService(
        settings=settings,
        user_repository=user_repository,
        token_repository=token_repository,
    )


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    # 对外只暴露纯 token 字符串，业务层无需关心 HTTP 头细节。
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthError(code="UNAUTHORIZED", message="Missing bearer token.")
    return credentials.credentials
