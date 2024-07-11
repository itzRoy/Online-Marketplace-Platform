from pymongo.database import Database

from backend import controllers, schemas
from backend.config import settings


async def init_db(db: Database) -> None:
    user = await controllers.user.get_by_email(
        db, email=settings.FIRST_SUPERUSER
    )

    product = await controllers.product.get_multi(db=db, limit=1)

    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        await controllers.user.create(db, obj_in=user_in)

    if not product:
        product_in = schemas.ProductCreate(
            name="t-shirt",
            desctiption="some dummy description now hopping i had Emmit",
            image="https://storage.googleapis.com/marketplace-4b18e.appspot.com/Slack_Mark.svg",
            price=66.6666,
        )
        await controllers.product.create(db=db, obj_in=product_in)
