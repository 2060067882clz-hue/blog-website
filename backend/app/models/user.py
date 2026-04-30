from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    password: str
    email: str
    role: int
    create_time: datetime
    nickname: str
