from typing import List

from fastapi import Depends, HTTPException, status
from motor.core import AgnosticDatabase

from backend import controllers, deps, models, schemas
from backend.custom_router import router
from backend.services import stripe_service


@router.get("/checkout", response_model=str)
async def chekout(
    user: models.User = Depends(deps.get_current_user),
    db: AgnosticDatabase = Depends(deps.get_db),
):
    if not user.cart:
        raise HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail="cart is empty",
        )

    user_cart_products: List[models.Product] = (
        await controllers.product.get_by_ids(db=db, ids=user.cart)
    )
    line_products = []

    order = models.Order(user=user, products=user_cart_products)

    for product in user_cart_products:
        line_products.append(
            schemas.ProductLineItem(
                **{
                    "price_data": {
                        "unit_amount_decimal": product.price,
                        "product_data": {
                            "name": product.name,
                            "images": [product.image],
                        },
                    }
                }
            )
        )

    order = await controllers.order.engine.save(order)
    return stripe_service.get_checkout_session(
        products=line_products, order_id=str(order.id)
    )
