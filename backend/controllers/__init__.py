from backend import models, schemas

from .base import BaseController
from .user import user

# For basic set of controller operations


product = BaseController[
    models.Product, schemas.ProductCreate, schemas.Product
](models.Product)
order = BaseController[
    models.Order, schemas.OrderCreate, schemas.OrderUpdate
](models.Order)
