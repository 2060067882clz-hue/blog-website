from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """返回给前端的用户公开信息，不包含敏感字段。"""

    id: str
    username: str
    display_name: str
    role: str


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    """注册请求体。"""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    display_name: str = Field(..., min_length=2, max_length=50)


class AuthResponse(BaseModel):
    """注册和登录成功后的统一返回结构。"""

    success: bool = True
    message: str
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile


class MessageResponse(BaseModel):
    """仅返回提示信息的通用响应结构。"""

    success: bool = True
    message: str


class CurrentUserResponse(BaseModel):
    """获取当前登录用户信息时的返回结构。"""

    success: bool = True
    user: UserProfile
