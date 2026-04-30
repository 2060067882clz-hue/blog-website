from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    id: int
    article_id: int
    user_id: int
    content: str
    create_time: datetime
