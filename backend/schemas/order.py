from datetime import datetime
from typing import List

from odmantic import ObjectId
from pydantic import AnyHttpUrl, BaseModel

from .product import Product


class BaseOrder(BaseModel):
    status: str
    products: List[Product]
    created: datetime
    modified: datetime


class OrderCreate(BaseOrder):
    pass


class OrderUpdate(OrderCreate):
    pass


class OrderListItem(OrderCreate):
    id: ObjectId


class OrderGet(OrderCreate):
    pass


class OrderCheckout(OrderListItem):
    checkout: AnyHttpUrl
