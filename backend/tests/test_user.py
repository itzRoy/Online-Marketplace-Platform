from typing import Dict

import pytest
from fastapi.testclient import TestClient

from backend import controllers
from backend.config import settings
from backend.tests.utils.utils import random_email, random_lower_string


def test_use_access_token(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/order/all",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/user", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/user", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


@pytest.mark.asyncio
async def test_create_user_new_email(client: TestClient, db) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/register",
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = await controllers.user.get_by_email(db, email=email)
    assert user
    assert user.email == created_user["email"]


@pytest.mark.asyncio
async def test_user_add_to_cart(
    client: TestClient, db, normal_user_token_headers: dict
) -> None:

    products = await controllers.product.get_multi(db=db, limit=1)
    assert len(products)
    product = products[0]
    user = client.get(
        f"{settings.API_V1_STR}/user", headers=normal_user_token_headers
    )
    user_in = user.json()

    if str(product.id) in user_in["cart"]:
        user_in["cart"] = []
        db_user = await controllers.user.get_by_email(
            db=db, email=user_in["email"]
        )

        user = await controllers.user.update(
            db=db, db_obj=db_user, obj_in=user_in
        )

    r_add_to_cart = client.post(
        f"{settings.API_V1_STR}/add-to-cart/{product.id}",
        headers=normal_user_token_headers,
    )
    r_user_cart = client.get(
        f"{settings.API_V1_STR}/cart", headers=normal_user_token_headers
    )
    add_to_cart_response = r_add_to_cart.json()
    user_cart_response = r_user_cart.json()
    assert add_to_cart_response["msg"] == f"{product.name} added to cart"
    assert str(product.id) in [i["id"] for i in user_cart_response]
