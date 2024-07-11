from typing import List

from fastapi import Depends
from motor.core import AgnosticDatabase
from odmantic import ObjectId

from backend import controllers, deps, schemas
from backend.custom_router import router
from backend.models.user import User

router.tags = ["order"]


@router.get("/order/all", response_model=List[schemas.OrderListItem])
async def get_orders(
    current_user: User = Depends(deps.get_current_user),
    db: AgnosticDatabase = Depends(deps.get_db),
):
    if current_user.is_superuser:
        return await controllers.order.get_multi(db=db)
    return await controllers.order.get_multi(db, user=current_user.id)


@router.get("/order/{order_id}", response_model=schemas.OrderListItem)
async def get_order(
    order_id: ObjectId,
    current_user: User = Depends(deps.get_current_user),
    db: AgnosticDatabase = Depends(deps.get_db),
):
    if current_user.is_superuser:
        return await controllers.order.get(db=db)
    return await controllers.order.get(
        db=db, user=current_user.id, id=order_id
    )
