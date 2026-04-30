from app.core.exceptions import AppException
from app.models.comment import Comment
from app.models.user import User
from app.repositories.article_repository import ArticleRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.comment import (
    CommentAuthor,
    CommentCreateRequest,
    CommentDeleteResponse,
    CommentListData,
    CommentListResponse,
    CommentSchema,
)
from app.services.auth_service import resolve_current_user


class CommentService:
    def __init__(
        self,
        *,
        comment_repository: CommentRepository,
        article_repository: ArticleRepository,
        user_repository: UserRepository,
        token_repository: TokenRepository,
    ) -> None:
        self.comment_repository = comment_repository
        self.article_repository = article_repository
        self.user_repository = user_repository
        self.token_repository = token_repository

    def _serialize_comment(self, comment: Comment) -> CommentSchema:
        author = self.user_repository.get_by_id(comment.user_id)
        if not author:
            raise AppException(status_code=404, code="AUTHOR_NOT_FOUND", message="评论作者不存在。")
        return CommentSchema(
            id=comment.id,
            article_id=comment.article_id,
            content=comment.content,
            create_time=comment.create_time,
            author=CommentAuthor(
                id=author.id,
                username=author.username,
                nickname=author.nickname,
            ),
        )

    def _ensure_article_exists(self, article_id: int) -> None:
        article = self.article_repository.get_by_id(article_id)
        if not article:
            raise AppException(status_code=404, code="ARTICLE_NOT_FOUND", message="文章不存在。")

    def list_article_comments(self, article_id: int) -> CommentListResponse:
        self._ensure_article_exists(article_id)
        comments = [self._serialize_comment(item) for item in self.comment_repository.list_by_article(article_id)]
        return CommentListResponse(data=CommentListData(comments=comments))

    def create_comment(self, token: str, article_id: int, payload: CommentCreateRequest) -> CommentListResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        self._ensure_article_exists(article_id)
        self.comment_repository.create_comment(
            article_id=article_id,
            user_id=user.id,
            content=payload.content.strip(),
        )
        return self.list_article_comments(article_id)

    def delete_comment(self, token: str, comment_id: int) -> CommentDeleteResponse:
        user = resolve_current_user(token, self.user_repository, self.token_repository)
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise AppException(status_code=404, code="COMMENT_NOT_FOUND", message="评论不存在。")
        self._assert_comment_permission(user, comment)
        deleted_comment = self.comment_repository.delete_comment(comment_id)
        return CommentDeleteResponse(
            message="评论删除成功。",
            data=self._serialize_comment(deleted_comment),
        )

    def _assert_comment_permission(self, user: User, comment: Comment) -> None:
        if user.role != 1 and user.id != comment.user_id:
            raise AppException(status_code=403, code="FORBIDDEN", message="没有权限操作这条评论。")
