from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Optional

from app.core.config import settings
from app.core.database import MySQLDatabase
from app.core.security import hash_password
from app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, *, username: str, password: str, email: str, role: int, nickname: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def list_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: int) -> Optional[User]:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    def __init__(self, initial_users: Optional[List[User]] = None) -> None:
        self._users: list[User] = initial_users or []
        self._next_id = max((user.id for user in self._users), default=0) + 1

    @classmethod
    def bootstrap_demo_data(cls) -> "InMemoryUserRepository":
        return cls(
            initial_users=[
                User(
                    id=1,
                    username=settings.demo_admin_username,
                    password=hash_password(settings.demo_admin_password),
                    email=settings.demo_admin_email,
                    role=1,
                    create_time=datetime.now(timezone.utc),
                    nickname=settings.demo_admin_nickname,
                )
            ]
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)

    def get_by_username(self, username: str) -> Optional[User]:
        normalized_username = username.strip().lower()
        return next(
            (user for user in self._users if user.username.lower() == normalized_username),
            None,
        )

    def get_by_email(self, email: str) -> Optional[User]:
        normalized_email = email.strip().lower()
        return next(
            (user for user in self._users if user.email.lower() == normalized_email),
            None,
        )

    def create_user(
        self,
        *,
        username: str,
        password: str,
        email: str,
        role: int,
        nickname: str,
    ) -> User:
        user = User(
            id=self._next_id,
            username=username,
            password=password,
            email=email,
            role=role,
            create_time=datetime.now(timezone.utc),
            nickname=nickname,
        )
        self._users.append(user)
        self._next_id += 1
        return user

    def list_users(self) -> List[User]:
        return list(self._users)

    def delete_user(self, user_id: int) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        self._users = [item for item in self._users if item.id != user_id]
        return user


class MySQLUserRepository(UserRepository):
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def _row_to_user(self, row: dict) -> User:
        return User(
            id=row["id"],
            username=row["username"],
            password=row["password"],
            email=row["email"],
            role=row["role"],
            create_time=row["create_time"].astimezone(timezone.utc),
            nickname=row["nickname"],
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def get_by_username(self, username: str) -> Optional[User]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)",
                    (username.strip(),),
                )
                row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE LOWER(email) = LOWER(%s)",
                    (email.strip(),),
                )
                row = cursor.fetchone()
        return self._row_to_user(row) if row else None

    def create_user(
        self,
        *,
        username: str,
        password: str,
        email: str,
        role: int,
        nickname: str,
    ) -> User:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (username, password, email, role, nickname)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (username, password, email, role, nickname),
                )
                user_id = cursor.lastrowid
        return self.get_by_id(user_id)

    def list_users(self) -> List[User]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users ORDER BY create_time DESC")
                rows = cursor.fetchall()
        return [self._row_to_user(row) for row in rows]

    def delete_user(self, user_id: int) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        return user
