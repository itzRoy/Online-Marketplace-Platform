from fastapi.testclient import TestClient

from backend.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    response = r.json()
    assert r.status_code == 200
    assert len(response["access_token"])
