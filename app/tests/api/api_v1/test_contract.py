from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract


def test_create_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    date_today = date.today()
    data = {
        "child": random_lower_string(),
        "duration_mode": "daily",
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
    assert isinstance(content["user"], dict)
    assert content["user"]["id"] == user.id
    assert content["user"]["firstname"] == user.firstname
    assert content["nanny_id"] == nanny.id
    assert content["child"] == data["child"]
    assert content["duration_mode"] == data["duration_mode"]
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
    assert content["child"] == data["child"]
    assert content["duration_mode"] == data["duration_mode"]
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
        headers=superuser_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user_id"] == user.id
    assert isinstance(content["user"], dict)
    assert content["user"]["id"] == user.id
    assert content["user"]["firstname"] == user.firstname
    assert content["user"]["id"] == user.id
    assert content["user"]["id"] == user.id
    assert content["user"]["firstname"] == user.firstname
    assert content["child"] == data["child"]
    assert content["duration_mode"] == data["duration_mode"]
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
    assert content["user"]["id"] == user_id
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
    assert content["user_id"] == user_id
    assert content["user"]["id"] == user_id
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
        "child": random_lower_string(),
        "duration_mode": "daily",
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
    assert content["child"] == contract.child
    assert content["duration_mode"] == contract.duration_mode
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
    assert content["child"] == contract.child
    assert content["duration_mode"] == contract.duration_mode
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
    assert content["child"] == contract.child
    assert content["duration_mode"] == contract.duration_mode
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
    assert content["child"] == contract.child
    assert content["duration_mode"] == contract.duration_mode
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


def test_read_contract_month_summary_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    
    start = contract.start + relativedelta(months=-1)
    month = start.month
    year = start.year
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    # assert response.status_code == 400 # Passed IF range date is included in the contract start/end date
    
    start = contract.start + relativedelta(months=+13)
    month = start.month
    year = start.year
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    # assert response.status_code == 400 # Passed IF range date is included in the contract start/end date

    start = contract.start + relativedelta(months=+1)
    month = start.month
    year = start.year
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)
    assert "business_days" in list(content.keys())
    assert "working_days" in list(content.keys())
    assert "presence_child" in list(content.keys())
    assert "absence_child" in list(content.keys())
    assert "disease_child" in list(content.keys())
    assert "disease_nanny" in list(content.keys())
    assert "daysoff_child" in list(content.keys())
    assert "daysoff_nanny" in list(content.keys())
    assert "hours_standard" in list(content.keys())
    assert "hours_complementary" in list(content.keys())
    assert "hours_extra" in list(content.keys())
    assert "monthly_hours" in list(content.keys())
    assert "monthly_salary" in list(content.keys())
    assert "monthly_fees" in list(content.keys())
    assert "price_hour_standard" in list(content.keys())


def test_read_contract_month_summary_specific_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    # Create User
    # contract = create_random_contract(db, user_id=user_id)
    nanny = create_random_user(db)

    # Create Contract
    date_today = datetime.strptime("2020-09-01", "%Y-%m-%d").date()
    data = {
        "child": random_lower_string(),
        "duration_mode": "daily",
        "weekdays": {
            "Mon": {
                "hours": "9"
            },
            "Tue": {
                "hours": "9"
            },
            "Thu": {
                "hours": "9"
            },
            "Fri": {
                "hours": "9"
            }
        },
        "weeks": 47,
        "hours": 42.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.85,
        "price_fees": 3.11,
        "price_meals": 0.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user_id}&nanny_id={nanny.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    contract = response.json()

    # CASE FULL TIME
    # Get contract Summary
    month = 9
    year = 2020
    
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)
    assert "business_days" in list(content.keys())
    assert "working_days" in list(content.keys())
    assert "presence_child" in list(content.keys())
    assert "absence_child" in list(content.keys())
    assert "disease_child" in list(content.keys())
    assert "disease_nanny" in list(content.keys())
    assert "daysoff_child" in list(content.keys())
    assert "daysoff_nanny" in list(content.keys())
    assert "hours_standard" in list(content.keys())
    assert "hours_complementary" in list(content.keys())
    assert "hours_extra" in list(content.keys())
    assert "monthly_hours" in list(content.keys())
    assert "monthly_salary" in list(content.keys())
    assert "monthly_fees" in list(content.keys())
    assert "price_hour_standard" in list(content.keys())

    # assert content["business_days"] == 17
    assert content["working_days"] == 17
    assert content["presence_child"] == 17
    assert content["absence_child"] == 0
    assert content["disease_child"] == 0
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 179
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 179
    assert content["monthly_salary"] == 626.5
    assert content["monthly_fees"] == 52.87
    assert content["price_hour_standard"] == 3.50


    # CASE PRESENCE CHILD
    # Create working day
    day_type_id = 3 # Presence child
    data = {
        "day": "2020-10-09",
        "start": "08:00:00",
        "end": "18:30:00"
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type_id}&contract_id={contract['id']}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()

    # Get contract summary
    month = 10
    year = 2020

    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)

    assert content["business_days"] == 22
    assert content["working_days"] == 18
    assert content["presence_child"] == 18
    assert content["absence_child"] == 0
    assert content["disease_child"] == 0
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 189
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 189
    assert content["monthly_salary"] == 661.50
    assert content["monthly_fees"] == 55.98
    assert content["price_hour_standard"] == contract["price_hour_standard"]


    ## CASE DISEASE CHILD
    # Create working day
    day_type_id = 5 # Disease child
    data = {
        "day": "2020-10-12",
        "start": "00:00:00",
        "end": "00:00:00"
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type_id}&contract_id={contract['id']}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()

    # Get contract summary
    month = 10
    year = 2020

    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)

    assert content["business_days"] == 22
    assert content["working_days"] == 17
    assert content["presence_child"] == 17
    assert content["absence_child"] == 0
    assert content["disease_child"] == 1
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 179
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 179
    assert content["monthly_salary"] == 626.50
    assert content["monthly_fees"] == 52.87
    assert content["price_hour_standard"] == contract["price_hour_standard"]


    ## CASE ABSENCE CHILD
    # Create working day
    day_type_id = 4 # Absence child
    data = {
        "day": "2020-10-13",
        "start": "00:00:00",
        "end": "00:00:00"
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type_id}&contract_id={contract['id']}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()

    # Get contract summary
    month = 10
    year = 2020

    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)

    assert content["business_days"] == 22
    assert content["working_days"] == 17
    assert content["presence_child"] == 16
    assert content["absence_child"] == 1
    assert content["disease_child"] == 1
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 177.0
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 177.0
    assert content["monthly_salary"] == 619.5
    assert content["monthly_fees"] == 49.76
    assert content["price_hour_standard"] == contract["price_hour_standard"]


def test_read_contract_month_summary_specific_real_december_2020_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    
    # Create User
    # contract = create_random_contract(db, user_id=user_id)
    nanny = create_random_user(db)

    # Create Contract
    date_today = datetime.strptime("2020-09-01", "%Y-%m-%d").date()
    data = {
        "child": random_lower_string(),
        "duration_mode": "daily",
        "weekdays": {
            "Mon": {
                "hours": "8"
            },
            "Tue": {
                "hours": "8"
            },
            "Wed": {
                "hours": "8"
            },
            "Thu": {
                "hours": "8"
            },
            "Fri": {
                "hours": "8"
            }
        },
        "weeks": 42,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.85,
        "price_fees": 3.11,
        "price_meals": 0.0,
        "start": "2020-09-01",
        "end": "2021-08-31"
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user_id}&nanny_id={nanny.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    contract = response.json()

    # Day Types List:
    #   1 : Dayoff
    #   2 : Inherited contract
    #   3 : Presence child
    #   4 : Absence child
    #   5 : Disease child
    #   6 : Disease nanny
    #   7 : Dayoff child
    #   8 : Dayoff nanny

    working_days_list = [
        {"data": {"day": "2021-01-04", "start": "8:35:00","end": "18:30:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-05", "start": "8:35:00","end": "18:20:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-06", "start": "9:10:00","end": "17:55:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-07", "start": "8:50:00","end": "17:30:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-08", "start": "00:00:00","end": "00:00:00"}, "day_type_id": 6},
        {"data": {"day": "2021-01-11", "start": "8:45:00","end": "18:10:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-12", "start": "8:20:00","end": "17:45:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-13", "start": "8:20:00","end": "18:05:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-14", "start": "8:45:00","end": "18:30:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-15", "start": "8:50:00","end": "18:20:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-18", "start": "8:45:00","end": "17:50:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-19", "start": "8:40:00","end": "16:00:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-20", "start": "8:50:00","end": "18:00:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-21", "start": "8:45:00","end": "17:45:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-22", "start": "8:40:00","end": "18:10:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-25", "start": "9:05:00","end": "18:10:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-26", "start": "8:25:00","end": "18:05:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-27", "start": "8:40:00","end": "17:55:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-28", "start": "9:15:00","end": "17:50:00"}, "day_type_id": 3},
        {"data": {"day": "2021-01-29", "start": "8:35:00","end": "18:15:00"}, "day_type_id": 3}
    ]
    # Create working days
    for working_day in working_days_list:
        response = client.post(
            f"{settings.API_V1_STR}/contracts/{contract['id']}/working_days" +
            f"?day_type_id={working_day['day_type_id']}",
            headers=normal_user_token_headers, json=working_day['data'],
        )
        assert response.status_code == 200



    # Get contract summary
    month = 1
    year = 2021

    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, dict)

    assert content["business_days"] == 20
    assert content["working_days"] == 19
    assert content["presence_child"] == 19
    assert content["absence_child"] == 0
    assert content["disease_child"] == 0
    assert content["disease_nanny"] == 1
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 158
    assert content["hours_complementary"] == 15
    assert content["hours_extra"] == 5
    assert content["monthly_hours"] == 178
    assert content["monthly_salary"] == 624.75
    assert content["monthly_fees"] == 59.09
    # assert content["price_hour_standard"] == contract["price_hour_standard"]
