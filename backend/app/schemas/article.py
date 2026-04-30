from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ArticleCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(min_length=1)


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    content: Optional[str] = Field(default=None, min_length=1)


class ArticleAuthor(BaseModel):
    id: int
    username: str
    nickname: str


class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    create_time: datetime
    update_time: datetime
    author: ArticleAuthor


class ArticleListResponse(BaseModel):
    success: bool = True
    data: List[ArticleSchema]


class ArticleResponse(BaseModel):
    success: bool = True
    message: str
    data: ArticleSchema


class ArticleDetailData(BaseModel):
    article: ArticleSchema
    comment_count: int


class ArticleDetailResponse(BaseModel):
    success: bool = True
    data: ArticleDetailData
