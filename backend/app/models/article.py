from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    id: int
    title: str
    content: str
    author_id: int
    create_time: datetime
    update_time: datetime
