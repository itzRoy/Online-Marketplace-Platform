from __future__ import annotations

from datetime import datetime
from typing import Any, List

from odmantic import Field, ObjectId
from pydantic import EmailStr

from backend.db.base_class import Base


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class User(Base):
    email: EmailStr
    password: Any = Field(default=None)
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    cart: List[ObjectId] = Field(default_factory=list)
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
