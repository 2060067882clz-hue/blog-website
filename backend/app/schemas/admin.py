from typing import List

from pydantic import BaseModel

from app.schemas.article import ArticleSchema
from app.schemas.auth import CurrentUserSchema


class AdminUserListResponse(BaseModel):
    success: bool = True
    data: List[CurrentUserSchema]


class AdminArticleListResponse(BaseModel):
    success: bool = True
    data: List[ArticleSchema]
