from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Optional

from app.core.database import MySQLDatabase
from app.models.article import Article


class ArticleRepository(ABC):
    @abstractmethod
    def list_articles(self) -> List[Article]:
        raise NotImplementedError

    @abstractmethod
    def list_by_author(self, author_id: int) -> List[Article]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, article_id: int) -> Optional[Article]:
        raise NotImplementedError

    @abstractmethod
    def create_article(self, *, title: str, content: str, author_id: int) -> Article:
        raise NotImplementedError

    @abstractmethod
    def update_article(self, article: Article) -> Article:
        raise NotImplementedError

    @abstractmethod
    def delete_article(self, article_id: int) -> Optional[Article]:
        raise NotImplementedError


class InMemoryArticleRepository(ArticleRepository):
    def __init__(self, initial_articles: Optional[List[Article]] = None) -> None:
        self._articles = initial_articles or []
        self._next_id = max((article.id for article in self._articles), default=0) + 1

    @classmethod
    def bootstrap_demo_data(cls) -> "InMemoryArticleRepository":
        now = datetime.now(timezone.utc)
        return cls(
            initial_articles=[
                Article(
                    id=1,
                    title="欢迎来到博客网站",
                    content="这是系统初始化的第一篇演示文章，后续可以替换为真实数据库实现。",
                    author_id=1,
                    create_time=now,
                    update_time=now,
                ),
                Article(
                    id=2,
                    title="后端认证模块说明",
                    content="当前已经完成注册、登录、获取当前用户、退出登录等认证基础接口。",
                    author_id=1,
                    create_time=now,
                    update_time=now,
                ),
            ]
        )

    def list_articles(self) -> List[Article]:
        return sorted(self._articles, key=lambda article: article.create_time, reverse=True)

    def list_by_author(self, author_id: int) -> List[Article]:
        return [article for article in self.list_articles() if article.author_id == author_id]

    def get_by_id(self, article_id: int) -> Optional[Article]:
        return next((article for article in self._articles if article.id == article_id), None)

    def create_article(self, *, title: str, content: str, author_id: int) -> Article:
        now = datetime.now(timezone.utc)
        article = Article(
            id=self._next_id,
            title=title,
            content=content,
            author_id=author_id,
            create_time=now,
            update_time=now,
        )
        self._articles.append(article)
        self._next_id += 1
        return article

    def update_article(self, article: Article) -> Article:
        article.update_time = datetime.now(timezone.utc)
        return article

    def delete_article(self, article_id: int) -> Optional[Article]:
        article = self.get_by_id(article_id)
        if not article:
            return None
        self._articles = [item for item in self._articles if item.id != article_id]
        return article


class MySQLArticleRepository(ArticleRepository):
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def _row_to_article(self, row: dict) -> Article:
        return Article(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            author_id=row["author_id"],
            create_time=row["create_time"].astimezone(timezone.utc),
            update_time=row["update_time"].astimezone(timezone.utc),
        )

    def list_articles(self) -> List[Article]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM articles ORDER BY create_time DESC")
                rows = cursor.fetchall()
        return [self._row_to_article(row) for row in rows]

    def list_by_author(self, author_id: int) -> List[Article]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM articles WHERE author_id = %s ORDER BY create_time DESC",
                    (author_id,),
                )
                rows = cursor.fetchall()
        return [self._row_to_article(row) for row in rows]

    def get_by_id(self, article_id: int) -> Optional[Article]:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
                row = cursor.fetchone()
        return self._row_to_article(row) if row else None

    def create_article(self, *, title: str, content: str, author_id: int) -> Article:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO articles (title, content, author_id)
                    VALUES (%s, %s, %s)
                    """,
                    (title, content, author_id),
                )
                article_id = cursor.lastrowid
        return self.get_by_id(article_id)

    def update_article(self, article: Article) -> Article:
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE articles
                    SET title = %s, content = %s
                    WHERE id = %s
                    """,
                    (article.title, article.content, article.id),
                )
        return self.get_by_id(article.id)

    def delete_article(self, article_id: int) -> Optional[Article]:
        article = self.get_by_id(article_id)
        if not article:
            return None
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
        return article
