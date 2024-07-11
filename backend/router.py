from fastapi import APIRouter

from backend.endpoints import (
    auth,
    order,
    payment,
    product,
    user,
    webhooks,
    websocket,
)

router = APIRouter(prefix="/api")

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(product.router)
router.include_router(payment.router)
router.include_router(webhooks.router)
router.include_router(websocket.router)
router.include_router(order.router)
