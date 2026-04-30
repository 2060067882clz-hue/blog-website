from datetime import datetime, timezone

from app.core.exceptions import AppException
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthData, AuthResponse, CurrentUserSchema, LoginRequest, RegisterRequest, UserResponse
from app.schemas.common import MessageResponse


def resolve_current_user(token: str, user_repository: UserRepository, token_repository: TokenRepository):
    if token_repository.is_revoked(token):
        raise AppException(status_code=401, code="TOKEN_REVOKED", message="登录已失效，请重新登录。")

    payload = decode_access_token(token)
    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise AppException(status_code=401, code="INVALID_TOKEN", message="登录凭证无效。") from exc

    user = user_repository.get_by_id(user_id)
    if not user:
        raise AppException(status_code=404, code="USER_NOT_FOUND", message="用户不存在。")

    return user


class AuthService:
    def __init__(self, *, user_repository: UserRepository, token_repository: TokenRepository) -> None:
        self.user_repository = user_repository
        self.token_repository = token_repository

    def register(self, payload: RegisterRequest) -> AuthResponse:
        if self.user_repository.get_by_username(payload.username):
            raise AppException(status_code=409, code="USERNAME_EXISTS", message="用户名已存在。")

        if self.user_repository.get_by_email(payload.email):
            raise AppException(status_code=409, code="EMAIL_EXISTS", message="邮箱已被使用。")

        user = self.user_repository.create_user(
            username=payload.username.strip(),
            password=hash_password(payload.password),
            email=str(payload.email).strip().lower(),
            role=0,
            nickname=(payload.nickname or payload.username).strip(),
        )
        token, _ = create_access_token(str(user.id))
        return AuthResponse(
            message="注册成功。",
            data=AuthData(token=token, user=CurrentUserSchema.model_validate(user)),
        )

    def login(self, payload: LoginRequest) -> AuthResponse:
        user = self.user_repository.get_by_username(payload.username)
        if not user or not verify_password(payload.password, user.password):
            raise AppException(status_code=401, code="INVALID_CREDENTIALS", message="用户名或密码错误。")

        token, _ = create_access_token(str(user.id))
        return AuthResponse(
            message="登录成功。",
            data=AuthData(token=token, user=CurrentUserSchema.model_validate(user)),
        )

    def logout(self, token: str) -> MessageResponse:
        payload = decode_access_token(token)
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        self.token_repository.revoke(token, expires_at)
        return MessageResponse(message="已退出登录。")

    def get_current_user(self, token: str) -> UserResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        return UserResponse(data=CurrentUserSchema.model_validate(user))
