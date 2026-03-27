from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """系统内部使用的用户实体，连接仓储层和服务层。"""

    id: str
    username: str
    display_name: str
    password_hash: str
    role: str
    is_active: bool = True
