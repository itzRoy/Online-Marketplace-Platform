from datetime import datetime
from typing import List

from odmantic import ObjectId
from pydantic import BaseModel, Field, HttpUrl, model_validator


class BaseProduct(BaseModel):
    name: str
    price: float


class ProductCompact(BaseProduct):
    id: ObjectId | None = None


class ProductCreate(BaseProduct):
    image: str
    desctiption: str = ""

    @model_validator(mode="after")
    def validator(cls, values):
        values.price = round(values.price, 2)
        return values


class Product(ProductCompact, ProductCreate):
    created: datetime
    modified: datetime


# to be used in stripe checkout


class ProductData(BaseModel):
    name: str
    images: List[HttpUrl] = Field(..., description="List of image URLs")


class PriceData(BaseModel):
    currency: str = "usd"
    product_data: ProductData
    unit_amount_decimal: float | str = Field(
        ..., description="Product price amount"
    )


class ProductLineItem(BaseModel):
    price_data: PriceData
    quantity: int = 1

    @model_validator(mode="after")
    def validator(cls, values):
        if values.price_data.currency == "usd":
            values.price_data.unit_amount_decimal = str(
                float(values.price_data.unit_amount_decimal) * 100
            )
        return values
