from typing import List

import stripe
from fastapi import Request
from pydantic import HttpUrl

from backend import schemas
from backend.config import settings


class Stripe:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_API_KEY

    def get_checkout_session(
        self, products: List[schemas.ProductLineItem], order_id: str
    ) -> HttpUrl:

        line_products = [product.model_dump() for product in products]
        checkout_session = stripe.checkout.Session.create(
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            payment_method_types=["card"],
            mode="payment",
            line_items=line_products,
            metadata={"order_id": order_id},
            payment_intent_data={"metadata": {"order_id": order_id}},
        )

        return checkout_session.url

    async def get_webhook_event(self, request: Request):
        stripe_signature = request.headers.get("stripe-signature")

        payload = await request.body()
        event = self.stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
        self.stripe.Event
        return event


stripe_service = Stripe()
