from datetime import date
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract


def test_create_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user.id}&nanny_id={nanny.id}",
        headers=superuser_token_headers,
        json=data)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user_id"] == user.id
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    nanny = create_random_user(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user_id}&nanny_id={nanny.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user_id"] == user_id
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_without_nanny_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user.id}",
        headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user_id"] == user.id
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_without_nanny_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user_id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user_id"] == user_id
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user.id}&nanny_id={nanny.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 400


def test_read_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_read_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_read_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["weekdays"] == data["weekdays"]
    assert content["weeks"] == data["weeks"]
    assert content["hours"] == data["hours"]
    assert content["price_hour_standard"] == data["price_hour_standard"]
    assert content["price_hour_extra"] == data["price_hour_extra"]
    assert content["price_fees"] == data["price_fees"]
    assert content["price_meals"] == data["price_meals"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    date_today = date.today()
    data = {
        "weekdays": random_weekdays(),
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 400


def test_update_contract_attach_nanny_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)

    nanny = create_random_user(db)
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}/nanny",
        headers=superuser_token_headers,
        json=f"{nanny.id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)
    
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_update_contract_attach_nanny_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id, has_nanny=False)
    assert contract.user_id == user_id
    assert contract.nanny_id == None
    assert not contract.nanny_id

    nanny = create_random_user(db)
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}/nanny",
        headers=normal_user_token_headers,
        json=f"{nanny.id}"
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["user_id"] == user_id
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)
    
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["user_id"] == user_id
    assert content["nanny_id"] == nanny.id
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_update_contract_attach_nanny_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db, has_nanny=False)
    assert contract.nanny_id == None
    assert not contract.nanny_id

    nanny = create_random_user(db)
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}/nanny",
        headers=normal_user_token_headers,
        json=f"{nanny.id}"
    )
    assert response.status_code == 400
    

def test_delete_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_delete_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "user_id" in content
    assert "nanny_id" in content
    assert content["weekdays"] == contract.weekdays
    assert content["weeks"] == contract.weeks
    assert content["hours"] == contract.hours
    assert content["price_hour_standard"] == contract.price_hour_standard
    assert content["price_hour_extra"] == contract.price_hour_extra
    assert content["price_fees"] == contract.price_fees
    assert content["price_meals"] == contract.price_meals
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)



def test_delete_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


