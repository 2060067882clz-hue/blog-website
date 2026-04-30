from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.core.database import MySQLDatabase

class TokenRepository(ABC):
    @abstractmethod
    def revoke(self, token: str, expires_at: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_revoked(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def cleanup_expired(self) -> None:
        raise NotImplementedError


class InMemoryTokenRepository(TokenRepository):
    def __init__(self) -> None:
        self._revoked_tokens: dict[str, datetime] = {}

    def revoke(self, token: str, expires_at: datetime) -> None:
        self._revoked_tokens[token] = expires_at

    def is_revoked(self, token: str) -> bool:
        self.cleanup_expired()
        return token in self._revoked_tokens

    def cleanup_expired(self) -> None:
        now = datetime.now(timezone.utc)
        expired_tokens = [
            token
            for token, expires_at in self._revoked_tokens.items()
            if expires_at <= now
        ]
        for token in expired_tokens:
            self._revoked_tokens.pop(token, None)


class MySQLTokenRepository(TokenRepository):
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def revoke(self, token: str, expires_at: datetime) -> None:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO revoked_tokens (token, expires_at)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE expires_at = VALUES(expires_at)
                    """,
                    (token, expires_at),
                )

    def is_revoked(self, token: str) -> bool:
        self.cleanup_expired()
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT token FROM revoked_tokens WHERE token = %s
                    """,
                    (token,),
                )
                return cursor.fetchone() is not None

    def cleanup_expired(self) -> None:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM revoked_tokens
                    WHERE expires_at <= %s
                    """,
                    (datetime.now(timezone.utc),),
                )
