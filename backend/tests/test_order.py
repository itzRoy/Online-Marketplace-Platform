from typing import Dict

from fastapi.testclient import TestClient

from backend.config import settings


def test_order(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:

    r_products = client.get(f"{settings.API_V1_STR}/product/all")
    producst = r_products.json()
    product_id = producst[0]["id"]
    client.post(
        f"{settings.API_V1_STR}/add-to-cart/{product_id}",
        headers=normal_user_token_headers,
    )
    r_checkout = client.get(
        f"{settings.API_V1_STR}/checkout", headers=normal_user_token_headers
    )
    checkout = r_checkout.json()
    checkout.pop("checkout")
    order_id = checkout["id"]

    r_order = client.get(
        f"{settings.API_V1_STR}/order/{order_id}",
        headers=normal_user_token_headers,
    )
    order = r_order.json()

    assert r_order.status_code == 200
    assert order == checkout
