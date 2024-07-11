import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.services import notification

from .router import router

# Define tags metadata
tags_metadata = [
    {"name": "users", "description": "Operations with users.", "order": 2},
    {"name": "items", "description": "Manage items.", "order": 1},
]


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(router)
    consumers = []
    for q in notification.queues:
        consumers.append(
            asyncio.create_task(notification.consume_notifications(q))
        )
    yield
    for consumer_task in consumers:
        consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=app_init)
