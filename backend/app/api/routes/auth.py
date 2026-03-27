from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_bearer_token
from app.schemas.auth import AuthResponse, CurrentUserResponse, LoginRequest, MessageResponse, RegisterRequest
from app.services.auth_service import AuthService

# 认证模块路由：注册、登录、退出登录、获取当前用户。
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    # 注册成功后直接返回 token，前端可以无缝进入登录态。
    return auth_service.register(payload)


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    # 登录接口只负责接收请求，核心逻辑都下沉到服务层。
    return auth_service.login(payload)


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    # 当前阶段通过记录已失效 token 来实现退出登录。
    return auth_service.logout(token)


@router.get("/me", response_model=CurrentUserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> CurrentUserResponse:
    # 用于前端刷新页面后重新获取当前登录用户信息。
    return auth_service.get_current_user(token)
