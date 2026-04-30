from app.core.exceptions import AppException
from app.models.article import Article
from app.models.user import User
from app.repositories.article_repository import ArticleRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.article import (
    ArticleAuthor,
    ArticleCreateRequest,
    ArticleDetailData,
    ArticleDetailResponse,
    ArticleListResponse,
    ArticleResponse,
    ArticleSchema,
    ArticleUpdateRequest,
)
from app.services.auth_service import resolve_current_user


class ArticleService:
    def __init__(
        self,
        *,
        article_repository: ArticleRepository,
        comment_repository: CommentRepository,
        user_repository: UserRepository,
        token_repository: TokenRepository,
    ) -> None:
        self.article_repository = article_repository
        self.comment_repository = comment_repository
        self.user_repository = user_repository
        self.token_repository = token_repository

    def _serialize_article(self, article: Article) -> ArticleSchema:
        author = self.user_repository.get_by_id(article.author_id)
        if not author:
            raise AppException(status_code=404, code="AUTHOR_NOT_FOUND", message="文章作者不存在。")

        return ArticleSchema(
            id=article.id,
            title=article.title,
            content=article.content,
            create_time=article.create_time,
            update_time=article.update_time,
            author=ArticleAuthor(
                id=author.id,
                username=author.username,
                nickname=author.nickname,
            ),
        )

    def _get_article_or_raise(self, article_id: int) -> Article:
        article = self.article_repository.get_by_id(article_id)
        if not article:
            raise AppException(status_code=404, code="ARTICLE_NOT_FOUND", message="文章不存在。")
        return article

    def list_articles(self) -> ArticleListResponse:
        articles = [self._serialize_article(article) for article in self.article_repository.list_articles()]
        return ArticleListResponse(data=articles)

    def list_my_articles(self, token: str) -> ArticleListResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        articles = [self._serialize_article(article) for article in self.article_repository.list_by_author(user.id)]
        return ArticleListResponse(data=articles)

    def create_article(self, token: str, payload: ArticleCreateRequest) -> ArticleResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        article = self.article_repository.create_article(
            title=payload.title.strip(),
            content=payload.content.strip(),
            author_id=user.id,
        )
        return ArticleResponse(message="文章发布成功。", data=self._serialize_article(article))

    def get_article_detail(self, article_id: int) -> ArticleDetailResponse:
        article = self._get_article_or_raise(article_id)
        comment_count = len(self.comment_repository.list_by_article(article_id))
        return ArticleDetailResponse(
            data=ArticleDetailData(
                article=self._serialize_article(article),
                comment_count=comment_count,
            )
        )

    def update_article(self, token: str, article_id: int, payload: ArticleUpdateRequest) -> ArticleResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        article = self._get_article_or_raise(article_id)
        self._assert_article_permission(user, article)

        if payload.title is not None:
            article.title = payload.title.strip()
        if payload.content is not None:
            article.content = payload.content.strip()

        updated_article = self.article_repository.update_article(article)
        return ArticleResponse(message="文章更新成功。", data=self._serialize_article(updated_article))

    def delete_article(self, token: str, article_id: int) -> ArticleResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        article = self._get_article_or_raise(article_id)
        self._assert_article_permission(user, article)
        self.comment_repository.delete_by_article(article_id)
        deleted_article = self.article_repository.delete_article(article_id)
        return ArticleResponse(message="文章删除成功。", data=self._serialize_article(deleted_article))

    def _assert_article_permission(self, user: User, article: Article) -> None:
        if user.role != 1 and user.id != article.author_id:
            raise AppException(status_code=403, code="FORBIDDEN", message="没有权限操作这篇文章。")
