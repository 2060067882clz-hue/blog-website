from app.core.exceptions import AppException
from app.repositories.article_repository import ArticleRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import AdminArticleListResponse, AdminUserListResponse
from app.schemas.article import ArticleResponse
from app.schemas.auth import CurrentUserSchema
from app.schemas.common import MessageResponse
from app.services.article_service import ArticleService
from app.services.auth_service import resolve_current_user


class AdminService:
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

    def _ensure_admin(self, token: str):
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        if user.role != 1:
            raise AppException(status_code=403, code="FORBIDDEN", message="需要管理员权限。")
        return user

    def list_users(self, token: str) -> AdminUserListResponse:
        self._ensure_admin(token)
        users = [CurrentUserSchema.model_validate(user) for user in self.user_repository.list_users()]
        return AdminUserListResponse(data=users)

    def list_articles(self, token: str) -> AdminArticleListResponse:
        self._ensure_admin(token)
        serializer = ArticleService(
            article_repository=self.article_repository,
            comment_repository=self.comment_repository,
            user_repository=self.user_repository,
            token_repository=self.token_repository,
        )
        articles = [serializer._serialize_article(article) for article in self.article_repository.list_articles()]
        return AdminArticleListResponse(data=articles)

    def delete_user(self, token: str, user_id: int) -> MessageResponse:
        admin_user = self._ensure_admin(token)
        if user_id == admin_user.id:
            raise AppException(status_code=400, code="INVALID_OPERATION", message="不能删除当前管理员自己。")
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise AppException(status_code=404, code="USER_NOT_FOUND", message="用户不存在。")
        self.user_repository.delete_user(user_id)
        self.comment_repository.delete_by_user(user_id)
        authored_articles = self.article_repository.list_by_author(user_id)
        for article in authored_articles:
            self.comment_repository.delete_by_article(article.id)
            self.article_repository.delete_article(article.id)
        return MessageResponse(message="用户删除成功。")

    def delete_article(self, token: str, article_id: int) -> ArticleResponse:
        self._ensure_admin(token)
        serializer = ArticleService(
            article_repository=self.article_repository,
            comment_repository=self.comment_repository,
            user_repository=self.user_repository,
            token_repository=self.token_repository,
        )
        article = self.article_repository.get_by_id(article_id)
        if not article:
            raise AppException(status_code=404, code="ARTICLE_NOT_FOUND", message="文章不存在。")
        self.comment_repository.delete_by_article(article_id)
        deleted_article = self.article_repository.delete_article(article_id)
        return ArticleResponse(message="管理员删除文章成功。", data=serializer._serialize_article(deleted_article))
