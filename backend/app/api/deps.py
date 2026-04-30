from functools import lru_cache

from fastapi import Depends, Header

from app.core.config import settings
from app.core.database import mysql_database
from app.core.exceptions import AppException
from app.repositories.article_repository import InMemoryArticleRepository, MySQLArticleRepository
from app.repositories.comment_repository import InMemoryCommentRepository, MySQLCommentRepository
from app.repositories.token_repository import InMemoryTokenRepository, MySQLTokenRepository
from app.repositories.user_repository import InMemoryUserRepository, MySQLUserRepository
from app.services.article_service import ArticleService
from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.admin_service import AdminService


@lru_cache
def get_user_repository():
    if settings.use_mysql:
        return MySQLUserRepository(mysql_database)
    return InMemoryUserRepository.bootstrap_demo_data()


@lru_cache
def get_token_repository():
    if settings.use_mysql:
        return MySQLTokenRepository(mysql_database)
    return InMemoryTokenRepository()


@lru_cache
def get_article_repository():
    if settings.use_mysql:
        return MySQLArticleRepository(mysql_database)
    return InMemoryArticleRepository.bootstrap_demo_data()


@lru_cache
def get_comment_repository():
    if settings.use_mysql:
        return MySQLCommentRepository(mysql_database)
    return InMemoryCommentRepository.bootstrap_demo_data()


def get_auth_service(
    user_repository = Depends(get_user_repository),
    token_repository = Depends(get_token_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        token_repository=token_repository,
    )


def get_article_service(
    article_repository = Depends(get_article_repository),
    comment_repository = Depends(get_comment_repository),
    user_repository = Depends(get_user_repository),
    token_repository = Depends(get_token_repository),
) -> ArticleService:
    return ArticleService(
        article_repository=article_repository,
        comment_repository=comment_repository,
        user_repository=user_repository,
        token_repository=token_repository,
    )


def get_comment_service(
    comment_repository = Depends(get_comment_repository),
    article_repository = Depends(get_article_repository),
    user_repository = Depends(get_user_repository),
    token_repository = Depends(get_token_repository),
) -> CommentService:
    return CommentService(
        comment_repository=comment_repository,
        article_repository=article_repository,
        user_repository=user_repository,
        token_repository=token_repository,
    )


def get_admin_service(
    article_repository = Depends(get_article_repository),
    comment_repository = Depends(get_comment_repository),
    user_repository = Depends(get_user_repository),
    token_repository = Depends(get_token_repository),
) -> AdminService:
    return AdminService(
        article_repository=article_repository,
        comment_repository=comment_repository,
        user_repository=user_repository,
        token_repository=token_repository,
    )


def get_bearer_token(authorization: str = Header(default="")) -> str:
    if not authorization:
        raise AppException(status_code=401, code="UNAUTHORIZED", message="缺少登录凭证。")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AppException(status_code=401, code="UNAUTHORIZED", message="登录凭证格式错误。")

    return token.strip()
