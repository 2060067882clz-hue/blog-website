from pydantic import BaseModel


class HealthData(BaseModel):
    service: str
    version: str
    status: str


class HealthResponse(BaseModel):
    success: bool = True
    data: HealthData


class MessageResponse(BaseModel):
    success: bool = True
    message: str
