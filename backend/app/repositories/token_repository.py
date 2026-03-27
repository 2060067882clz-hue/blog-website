from abc import ABC, abstractmethod
from typing import Set


class AbstractTokenRepository(ABC):
    """token 仓储抽象，便于后续切换成 Redis 等外部存储。"""

    @abstractmethod
    def revoke(self, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_revoked(self, token: str) -> bool:
        raise NotImplementedError


class InMemoryTokenRepository(AbstractTokenRepository):
    def __init__(self) -> None:
        # 用集合记录已退出登录的 token，查询效率较高。
        self._revoked_tokens: Set[str] = set()

    def revoke(self, token: str) -> None:
        self._revoked_tokens.add(token)

    def is_revoked(self, token: str) -> bool:
        return token in self._revoked_tokens
