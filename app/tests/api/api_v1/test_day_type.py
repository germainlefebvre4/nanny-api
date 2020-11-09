from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.day_type import create_random_day_type


def test_create_day_type(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo"}
    response = client.post(
        f"{settings.API_V1_STR}/day_types/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_day_type(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types/{day_type.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == day_type.name
    assert content["id"] == day_type.id
