from typing import Dict

from fastapi.testclient import TestClient

from backend.config import settings


def test_checkout(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:

    r_user_cart = client.get(
        f"{settings.API_V1_STR}/cart", headers=normal_user_token_headers
    )
    user_cart = r_user_cart.json()

    if not len(user_cart):
        r_products = client.get(f"{settings.API_V1_STR}/product/all")
        products = r_products.json()
        product_id = products[0]["id"]
        client.post(
            f"{settings.API_V1_STR}/add-to-cart/{product_id}",
            headers=normal_user_token_headers,
        )

    r = client.get(
        f"{settings.API_V1_STR}/checkout", headers=normal_user_token_headers
    )
    response = r.json()
    assert r.status_code == 200
    assert len(response)
