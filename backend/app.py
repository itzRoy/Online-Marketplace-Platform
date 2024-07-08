from contextlib import asynccontextmanager

from fastapi import FastAPI

from .router import router


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(router)
    yield


app = FastAPI(lifespan=app_init)
