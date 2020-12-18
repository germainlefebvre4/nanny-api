# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.day_type import create_random_day_type


def test_create_day_type_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo"}
    response = client.post(
        f"{settings.API_V1_STR}/day_types/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["name"] == data["name"]


def test_create_day_type_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo2"}
    response = client.post(
        f"{settings.API_V1_STR}/day_types/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400


def test_read_day_types_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    day_types_length = len(content)-1
    assert content[day_types_length]["id"] == day_type.id
    assert content[day_types_length]["name"] == day_type.name


def test_read_day_types_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    day_types_length = len(content)-1
    assert content[day_types_length]["id"] == day_type.id
    assert content[day_types_length]["name"] == day_type.name


def test_read_day_type_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == day_type.name


def test_read_day_type_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == day_type.name


def test_read_day_type_with_name_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types/_search?name={day_type.name}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == day_type.name


def test_read_day_type_with_name_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/day_types/_search?name={day_type.name}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == day_type.name


def test_update_day_type_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    data = {"name": "Foo3"}
    response = client.put(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=superuser_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == data["name"]


def test_update_day_type_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    data = {"name": "Foo4"}
    response = client.put(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 400


def test_delete_day_type_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.delete(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == day_type.id
    assert content["name"] == day_type.name


def test_delete_day_type_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    day_type = create_random_day_type(db)
    response = client.delete(
        f"{settings.API_V1_STR}/day_types/{day_type.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
