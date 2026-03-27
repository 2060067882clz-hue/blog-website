from app.core.config import Settings
from app.core.exceptions import AuthError, ConflictError
from app.core.security import create_access_token, decode_access_token, verify_password
from app.models.user import User
from app.repositories.token_repository import AbstractTokenRepository
from app.repositories.user_repository import AbstractUserRepository
from app.schemas.auth import AuthResponse, CurrentUserResponse, LoginRequest, MessageResponse, RegisterRequest, UserProfile


class AuthService:
    """认证业务层，负责组织登录注册的完整流程。"""

    def __init__(
        self,
        settings: Settings,
        user_repository: AbstractUserRepository,
        token_repository: AbstractTokenRepository,
    ) -> None:
        self.settings = settings
        self.user_repository = user_repository
        self.token_repository = token_repository

    def login(self, payload: LoginRequest) -> AuthResponse:
        # 先查用户，再校验密码和账号状态。
        user = self.user_repository.get_by_username(payload.username)

        if user is None or not verify_password(payload.password, user.password_hash):
            raise AuthError(code="INVALID_CREDENTIALS", message="Username or password is incorrect.")

        if not user.is_active:
            raise AuthError(code="ACCOUNT_DISABLED", message="User account is disabled.")

        access_token, expires_in = create_access_token(
            subject=user.id,
            secret_key=self.settings.secret_key,
            expires_in_minutes=self.settings.access_token_expire_minutes,
        )

        return AuthResponse(
            message="Login successful.",
            access_token=access_token,
            expires_in=expires_in,
            user=self._build_profile(user),
        )

    def register(self, payload: RegisterRequest) -> AuthResponse:
        # 注册前先做用户名唯一性检查，避免覆盖已有用户。
        if self.user_repository.exists_by_username(payload.username):
            raise ConflictError(code="USERNAME_ALREADY_EXISTS", message="Username is already taken.")

        user = self.user_repository.create_user(payload)
        access_token, expires_in = create_access_token(
            subject=user.id,
            secret_key=self.settings.secret_key,
            expires_in_minutes=self.settings.access_token_expire_minutes,
        )

        return AuthResponse(
            message="Registration successful.",
            access_token=access_token,
            expires_in=expires_in,
            user=self._build_profile(user),
        )

    def logout(self, token: str) -> MessageResponse:
        # 退出登录的本质是把当前 token 标记为失效。
        self.token_repository.revoke(token)
        return MessageResponse(message="Logout successful.")

    def get_current_user(self, token: str) -> CurrentUserResponse:
        # 先判断 token 是否已被主动注销，再解析 token 里的用户 ID。
        if self.token_repository.is_revoked(token):
            raise AuthError(code="TOKEN_REVOKED", message="Token has been revoked.")

        payload = decode_access_token(token, self.settings.secret_key)
        user_id = str(payload.get("sub", ""))
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise AuthError(code="USER_NOT_FOUND", message="User in token does not exist.")

        return CurrentUserResponse(user=self._build_profile(user))

    @staticmethod
    def _build_profile(user: User) -> UserProfile:
        # 把内部用户实体转换成对外输出的用户信息。
        return UserProfile(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            role=user.role,
        )
