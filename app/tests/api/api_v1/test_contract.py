from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.contract import create_random_contract


def test_create_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo"}
    response = client.post(
        f"{settings.API_V1_STR}/contracts/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["name"] == data["name"]


def test_create_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    data = {"name": "Foo2"}
    response = client.post(
        f"{settings.API_V1_STR}/contracts/", headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 400


def test_read_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == contract.id
    assert content["name"] == contract.name


def test_read_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    data = {"name": "Foo3"}
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=superuser_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == contract.id
    assert content["name"] == data["name"]


def test_update_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    data = {"name": "Foo4"}
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 400


def test_delete_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == contract.id
    assert content["name"] == contract.name


def test_delete_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}", headers=normal_user_token_headers,
    )
    assert response.status_code == 400
