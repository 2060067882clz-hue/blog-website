from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=500)


class CommentAuthor(BaseModel):
    id: int
    username: str
    nickname: str


class CommentSchema(BaseModel):
    id: int
    article_id: int
    content: str
    create_time: datetime
    author: CommentAuthor


class CommentListData(BaseModel):
    comments: List[CommentSchema]


class CommentListResponse(BaseModel):
    success: bool = True
    message: str = "获取评论成功。"
    data: CommentListData


class CommentDeleteResponse(BaseModel):
    success: bool = True
    message: str
    data: CommentSchema
