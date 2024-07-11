import io
from typing import Dict

from fastapi.testclient import TestClient

from backend.config import settings


def test_post_product(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:

    image_content = io.BytesIO(b"test image content")
    image_content.name = "test_image.png"
    product_name = "autotest"
    product_price = 55
    r = client.post(
        f"{settings.API_V1_STR}/product",
        files={"image": ("test_image.png", image_content, "image/png")},
        data={"name": product_name, "price": product_price},
        headers=superuser_token_headers,
    )
    response = r.json()

    assert r.status_code == 200
    assert len(response["image"])
    assert response["name"] == product_name
    assert int(response["price"]) == product_price


def test_get_products(client: TestClient) -> None:

    r_all = client.get(f"{settings.API_V1_STR}/product/all")
    response_all = r_all.json()

    assert len(response_all)

    product_id = response_all[0]["id"]
    r = client.get(f"{settings.API_V1_STR}/product/{product_id}")
    response = r.json()

    assert response["id"] == product_id
