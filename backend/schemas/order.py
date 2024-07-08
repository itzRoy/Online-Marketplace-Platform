from datetime import datetime
from typing import List

from odmantic import ObjectId
from pydantic import BaseModel

from .product import Product


class BaseOrder(BaseModel):
    status: str
    products: List[Product]
    created: datetime
    modified: datetime


class OrderCreate(BaseOrder):
    user: ObjectId


class OrderUpdate(OrderCreate):
    pass


class OrderListItem(OrderCreate):
    pass
