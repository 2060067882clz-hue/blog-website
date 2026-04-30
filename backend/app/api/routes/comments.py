from fastapi import APIRouter, Depends

from app.api.deps import get_bearer_token, get_comment_service
from app.schemas.comment import CommentDeleteResponse
from app.services.comment_service import CommentService

router = APIRouter()


@router.delete("/{comment_id}", response_model=CommentDeleteResponse)
def delete_comment(
    comment_id: int,
    token: str = Depends(get_bearer_token),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentDeleteResponse:
    return comment_service.delete_comment(token, comment_id)
