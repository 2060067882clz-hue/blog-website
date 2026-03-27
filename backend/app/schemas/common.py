from pydantic import BaseModel


class HealthResponse(BaseModel):
    """健康检查接口的返回结构。"""

    success: bool
    service: str
    version: str
    status: str
