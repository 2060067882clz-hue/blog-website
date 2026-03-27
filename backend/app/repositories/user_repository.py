from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import uuid4

from app.core.config import Settings
from app.core.security import hash_password
from app.models.user import User
from app.schemas.auth import RegisterRequest


class AbstractUserRepository(ABC):
    """用户仓储抽象，后续接数据库时只需要实现这里定义的方法。"""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, payload: RegisterRequest) -> User:
        raise NotImplementedError


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self, settings: Settings) -> None:
        # 初始化一个演示账号，便于前后端在数据库未完成前先联调。
        demo_user = User(
            id=str(uuid4()),
            username=settings.demo_user_username,
            display_name=settings.demo_user_display_name,
            password_hash=hash_password(settings.demo_user_password),
            role="admin",
        )
        self._users_by_id: Dict[str, User] = {demo_user.id: demo_user}
        self._users_by_username: Dict[str, User] = {demo_user.username: demo_user}

    def get_by_username(self, username: str) -> Optional[User]:
        return self._users_by_username.get(username)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users_by_id.get(user_id)

    def exists_by_username(self, username: str) -> bool:
        return username in self._users_by_username

    def create_user(self, payload: RegisterRequest) -> User:
        # 当前阶段把新用户直接写入内存，服务重启后数据会丢失。
        user = User(
            id=str(uuid4()),
            username=payload.username,
            display_name=payload.display_name,
            password_hash=hash_password(payload.password),
            role="user",
        )
        self._users_by_id[user.id] = user
        self._users_by_username[user.username] = user
        return user
