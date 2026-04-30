from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)
    email: EmailStr
    nickname: Optional[str] = Field(default=None, max_length=32)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=128)


class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: int
    nickname: str
    create_time: datetime


class AuthData(BaseModel):
    token: str
    user: CurrentUserSchema


class AuthResponse(BaseModel):
    success: bool = True
    message: str
    data: AuthData


class UserResponse(BaseModel):
    success: bool = True
    data: CurrentUserSchema
