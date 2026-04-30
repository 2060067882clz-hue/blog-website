from fastapi import APIRouter, Depends

from app.api.deps import get_admin_service, get_bearer_token
from app.schemas.admin import AdminArticleListResponse, AdminUserListResponse
from app.schemas.article import ArticleResponse
from app.schemas.common import MessageResponse
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/users", response_model=AdminUserListResponse)
def list_users(
    token: str = Depends(get_bearer_token),
    admin_service: AdminService = Depends(get_admin_service),
) -> AdminUserListResponse:
    return admin_service.list_users(token)


@router.get("/articles", response_model=AdminArticleListResponse)
def list_articles(
    token: str = Depends(get_bearer_token),
    admin_service: AdminService = Depends(get_admin_service),
) -> AdminArticleListResponse:
    return admin_service.list_articles(token)


@router.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    token: str = Depends(get_bearer_token),
    admin_service: AdminService = Depends(get_admin_service),
) -> MessageResponse:
    return admin_service.delete_user(token, user_id)


@router.delete("/articles/{article_id}", response_model=ArticleResponse)
def delete_article(
    article_id: int,
    token: str = Depends(get_bearer_token),
    admin_service: AdminService = Depends(get_admin_service),
) -> ArticleResponse:
    return admin_service.delete_article(token, article_id)
