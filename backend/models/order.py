from datetime import datetime
from typing import List, Literal

from odmantic import Field
from odmantic.reference import Reference

from backend.db.base_class import Base

from .product import Product
from .user import User


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class Order(Base):
    user: User = Reference()
    products: List[Product]
    status: Literal["pending", "failed", "succeeded", "session expired"] = (
        "pending"
    )
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
