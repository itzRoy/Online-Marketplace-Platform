from motor import core, motor_asyncio
from odmantic import AIOEngine
from pymongo.driver_info import DriverInfo

from backend.config import settings

DRIVER_INFO = DriverInfo(
    name=(
        settings.MONGO_DATABASE_TEST
        if settings.IS_TESTING
        else settings.MONGO_DATABASE
    )
)


class _MongoClientSingleton:
    mongo_client: motor_asyncio.AsyncIOMotorClient | None
    engine: AIOEngine

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                settings.MONGO_DATABASE_URI, driver=DRIVER_INFO
            )
            cls.instance.engine = AIOEngine(
                client=cls.instance.mongo_client,
                database=(
                    settings.MONGO_DATABASE_TEST
                    if settings.IS_TESTING
                    else settings.MONGO_DATABASE
                ),
            )
        return cls.instance


def MongoDatabase() -> core.AgnosticDatabase:
    mongo_db = (
        settings.MONGO_DATABASE_TEST
        if settings.IS_TESTING
        else settings.MONGO_DATABASE
    )
    return _MongoClientSingleton().mongo_client[mongo_db]


def get_engine() -> AIOEngine:
    return _MongoClientSingleton().engine


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping"]
