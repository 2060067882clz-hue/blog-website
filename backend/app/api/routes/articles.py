from fastapi import APIRouter, Depends, status

from app.api.deps import get_article_service, get_bearer_token, get_comment_service
from app.schemas.article import (
    ArticleCreateRequest,
    ArticleDetailResponse,
    ArticleListResponse,
    ArticleResponse,
    ArticleUpdateRequest,
)
from app.schemas.comment import CommentCreateRequest, CommentListResponse
from app.services.article_service import ArticleService
from app.services.comment_service import CommentService

router = APIRouter()


@router.get("", response_model=ArticleListResponse)
def list_articles(
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleListResponse:
    return article_service.list_articles()


@router.get("/me", response_model=ArticleListResponse)
def list_my_articles(
    token: str = Depends(get_bearer_token),
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleListResponse:
    return article_service.list_my_articles(token)


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: ArticleCreateRequest,
    token: str = Depends(get_bearer_token),
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    return article_service.create_article(token, payload)


@router.get("/{article_id}", response_model=ArticleDetailResponse)
def get_article_detail(
    article_id: int,
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleDetailResponse:
    return article_service.get_article_detail(article_id)


@router.patch("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    payload: ArticleUpdateRequest,
    token: str = Depends(get_bearer_token),
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    return article_service.update_article(token, article_id, payload)


@router.delete("/{article_id}", response_model=ArticleResponse)
def delete_article(
    article_id: int,
    token: str = Depends(get_bearer_token),
    article_service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    return article_service.delete_article(token, article_id)


@router.get("/{article_id}/comments", response_model=CommentListResponse)
def list_article_comments(
    article_id: int,
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return comment_service.list_article_comments(article_id)


@router.post(
    "/{article_id}/comments",
    response_model=CommentListResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    article_id: int,
    payload: CommentCreateRequest,
    token: str = Depends(get_bearer_token),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentListResponse:
    return comment_service.create_comment(token, article_id, payload)
