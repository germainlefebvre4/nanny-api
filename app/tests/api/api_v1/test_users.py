from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.USER_ADMIN_EMAIL
    assert current_user["firstname"] == settings.USER_ADMIN_FIRSTNAME


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.USER_TEST_EMAIL
    assert current_user["firstname"] == settings.USER_TEST_FIRSTNAME


def test_create_user_new_email_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=email)
    assert user
    assert created_user["email"] == user.email
    assert created_user["is_user"] is True
    assert created_user["is_nanny"] is False
    assert created_user["is_superuser"] is False


def test_create_user_new_email_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_create_user_existing_email_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_existing_email_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    # email = email
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_get_user_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_user_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=normal_user_token_headers,
    )
    assert r.status_code == 400


def test_get_nanny_with_email_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    firstname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, firstname=firstname, password=password, is_user=False, is_nanny=True)
    user = crud.user.create(db, obj_in=user_in)
    response = client.get(
        f"{settings.API_V1_STR}/users/nanny/_search?email={email}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    api_user = response.json()
    assert api_user["email"] == email
    assert api_user["firstname"] == firstname
    existing_user = crud.user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]
    assert existing_user.email == email
    assert existing_user.firstname == api_user["firstname"]
    assert existing_user.firstname == firstname


def test_get_nanny_with_email_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    email = random_email()
    firstname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, firstname=firstname, password=password, is_user=False, is_nanny=True)
    user = crud.user.create(db, obj_in=user_in)
    response = client.get(
        f"{settings.API_V1_STR}/users/nanny/_search?email={email}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    api_user = response.json()
    assert api_user["email"] == email
    assert api_user["firstname"] == firstname
    existing_user = crud.user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == email
    assert existing_user.firstname == api_user["firstname"]
    assert existing_user.firstname == firstname

def test_get_users_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(db, obj_in=user_in)

    email2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=email2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item


def test_get_users_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers)

    assert r.status_code == 400


def test_create_nanny_by_admin(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password, "is_user": False, "is_nanny": True}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=email)
    assert user
    assert created_user["email"] == user.email
    assert created_user["is_user"] is False
    assert created_user["is_nanny"] is True
    assert created_user["is_superuser"] is False
