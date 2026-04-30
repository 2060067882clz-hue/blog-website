from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Optional

from app.core.database import MySQLDatabase
from app.models.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def list_by_article(self, article_id: int) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def create_comment(self, *, article_id: int, user_id: int, content: str) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def delete_comment(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_article(self, article_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_user(self, user_id: int) -> None:
        raise NotImplementedError


class InMemoryCommentRepository(CommentRepository):
    def __init__(self, initial_comments: Optional[List[Comment]] = None) -> None:
        self._comments = initial_comments or []
        self._next_id = max((comment.id for comment in self._comments), default=0) + 1

    @classmethod
    def bootstrap_demo_data(cls) -> "InMemoryCommentRepository":
        now = datetime.now(timezone.utc)
        return cls(
            initial_comments=[
                Comment(
                    id=1,
                    article_id=1,
                    user_id=1,
                    content="欢迎使用评论功能，这里后续也可以接真实数据库。",
                    create_time=now,
                )
            ]
        )

    def list_by_article(self, article_id: int) -> List[Comment]:
        comments = [comment for comment in self._comments if comment.article_id == article_id]
        return sorted(comments, key=lambda comment: comment.create_time)

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        return next((comment for comment in self._comments if comment.id == comment_id), None)

    def create_comment(self, *, article_id: int, user_id: int, content: str) -> Comment:
        comment = Comment(
            id=self._next_id,
            article_id=article_id,
            user_id=user_id,
            content=content,
            create_time=datetime.now(timezone.utc),
        )
        self._comments.append(comment)
        self._next_id += 1
        return comment

    def delete_comment(self, comment_id: int) -> Optional[Comment]:
        comment = self.get_by_id(comment_id)
        if not comment:
            return None
        self._comments = [item for item in self._comments if item.id != comment_id]
        return comment

    def delete_by_article(self, article_id: int) -> None:
        self._comments = [comment for comment in self._comments if comment.article_id != article_id]

    def delete_by_user(self, user_id: int) -> None:
        self._comments = [comment for comment in self._comments if comment.user_id != user_id]


class MySQLCommentRepository(CommentRepository):
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def _row_to_comment(self, row: dict) -> Comment:
        return Comment(
            id=row["id"],
            article_id=row["article_id"],
            user_id=row["user_id"],
            content=row["content"],
            create_time=row["create_time"].astimezone(timezone.utc),
        )

    def list_by_article(self, article_id: int) -> List[Comment]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM comments WHERE article_id = %s ORDER BY create_time ASC",
                    (article_id,),
                )
                rows = cursor.fetchall()
        return [self._row_to_comment(row) for row in rows]

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
                row = cursor.fetchone()
        return self._row_to_comment(row) if row else None

    def create_comment(self, *, article_id: int, user_id: int, content: str) -> Comment:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO comments (article_id, user_id, content)
                    VALUES (%s, %s, %s)
                    """,
                    (article_id, user_id, content),
                )
                comment_id = cursor.lastrowid
        return self.get_by_id(comment_id)

    def delete_comment(self, comment_id: int) -> Optional[Comment]:
        comment = self.get_by_id(comment_id)
        if not comment:
            return None
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        return comment

    def delete_by_article(self, article_id: int) -> None:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM comments WHERE article_id = %s", (article_id,))

    def delete_by_user(self, user_id: int) -> None:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM comments WHERE user_id = %s", (user_id,))
