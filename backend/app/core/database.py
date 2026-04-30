from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from app.core.config import settings
from app.core.security import hash_password


SCHEMA_FILE = Path(__file__).resolve().parents[2] / "docs" / "mysql_schema.sql"


class MySQLDatabase:
    def __init__(self) -> None:
        self.connection_kwargs = {
            "host": settings.mysql_host,
            "port": settings.mysql_port,
            "user": settings.mysql_user,
            "password": settings.mysql_password,
            "database": settings.mysql_database,
            "charset": settings.mysql_charset,
            "cursorclass": DictCursor,
            "autocommit": True,
        }

    @contextmanager
    def connection(self) -> Iterator[Connection]:
        connection = pymysql.connect(**self.connection_kwargs)
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
        statements = [statement.strip() for statement in schema_sql.split(";") if statement.strip()]

        with self.connection() as connection:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)

                cursor.execute(
                    """
                    SELECT id FROM users WHERE username = %s
                    """,
                    (settings.demo_admin_username,),
                )
                demo_user = cursor.fetchone()

                if not demo_user:
                    cursor.execute(
                        """
                        INSERT INTO users (username, password, email, role, nickname)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            settings.demo_admin_username,
                            hash_password(settings.demo_admin_password),
                            settings.demo_admin_email,
                            1,
                            settings.demo_admin_nickname,
                        ),
                    )
                    demo_user_id = cursor.lastrowid
                else:
                    demo_user_id = demo_user["id"]

                cursor.execute("SELECT COUNT(*) AS total FROM articles")
                article_count = cursor.fetchone()["total"]
                if article_count == 0:
                    cursor.executemany(
                        """
                        INSERT INTO articles (title, content, author_id)
                        VALUES (%s, %s, %s)
                        """,
                        [
                            (
                                "欢迎来到博客网站",
                                "这是系统初始化的第一篇演示文章，当前已经接入 MySQL 持久化。",
                                demo_user_id,
                            ),
                            (
                                "后端 MySQL 模式说明",
                                "当前文章、评论、用户和已失效 token 都可以通过 MySQL 持久化存储。",
                                demo_user_id,
                            ),
                        ],
                    )

                cursor.execute("SELECT COUNT(*) AS total FROM comments")
                comment_count = cursor.fetchone()["total"]
                if comment_count == 0:
                    cursor.execute("SELECT id FROM articles ORDER BY id ASC LIMIT 1")
                    article = cursor.fetchone()
                    if article:
                        cursor.execute(
                            """
                            INSERT INTO comments (article_id, user_id, content)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                article["id"],
                                demo_user_id,
                                "欢迎使用 MySQL 持久化后的评论功能。",
                            ),
                        )


mysql_database = MySQLDatabase()
