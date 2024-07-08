from fastapi import Depends, Request
from motor.core import AgnosticDatabase
from odmantic import ObjectId

from backend import controllers, deps
from backend.custom_router import router
from backend.services import stripe_service

router.prefix = "/webhooks"


@router.post("/stripe")
async def stripe_event(
    event: dict, request: Request, db: AgnosticDatabase = Depends(deps.get_db)
):
    supported_events = [
        "charge.succeeded",
        "charge.failed",
        "charge.expired",
        "checkout.session.payment_failed",
        "checkout.session.completed",
        "checkout.session.expired",
        "payment_intent.succeeded",
        "payment_intent.canceled",
        "payment_intent.payment_failed",
    ]

    if event["type"] not in supported_events:
        return

    e = await stripe_service.get_webhook_event(request=request)
    order_id = e.data["object"]["metadata"].get("order_id")

    if not order_id:
        return

    order = await controllers.order.get(db=db, id=ObjectId(order_id))

    if e.type in [
        "checkout.session.payment_failed",
        "charge.failed",
        "payment_intent.canceled",
    ]:
        order.status = "failed"
    elif e.type in [
        "checkout.session.completed",
        "charge.succeeded",
        "payment_intent.succeeded",
    ]:
        order.user.cart = []
        order.status = "succeeded"
    elif e.type == ["checkout.session.expired", "charge_expired"]:
        order.status = "session expired"

    await controllers.order.engine.save(order)
