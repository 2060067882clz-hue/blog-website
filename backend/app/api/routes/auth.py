from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_bearer_token
from app.schemas.auth import (
    LoginRequest,
    AuthResponse,
    RegisterRequest,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return auth_service.register(payload)


@router.post("/login", response_model=AuthResponse)
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    return auth_service.login(payload)


@router.post("/logout", response_model=MessageResponse)
def logout(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    return auth_service.logout(token)


@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return auth_service.get_current_user(token)
