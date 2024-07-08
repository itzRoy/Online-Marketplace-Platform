from pymongo.database import Database

from backend import controllers, schemas
from backend.config import settings


async def init_db(db: Database) -> None:
    user = await controllers.user.get_by_email(
        db, email=settings.FIRST_SUPERUSER
    )

    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user = await controllers.user.create(db, obj_in=user_in)
