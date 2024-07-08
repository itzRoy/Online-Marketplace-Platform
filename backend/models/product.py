from datetime import datetime
from typing import Optional

from odmantic import Field

from backend.db.base_class import Base


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class Product(Base):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    stripe_price: Optional[str] = Field(default=None)
    stripe_product: Optional[str] = Field(default=None)
