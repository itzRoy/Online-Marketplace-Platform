from typing import Dict

from fastapi.testclient import TestClient
from motor.core import AgnosticDatabase

from backend import controllers
from backend.config import settings
from backend.schemas.user import UserCreate, UserUpdate
from backend.tests.utils.utils import random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_email(
    *, client: TestClient, email: str, db: AgnosticDatabase
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await controllers.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(
            username=email, email=email, password=password
        )
        user = await controllers.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = await controllers.user.update(
            db, db_obj=user, obj_in=user_in_update
        )

    return user_authentication_headers(
        client=client, email=email, password=password
    )


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )
