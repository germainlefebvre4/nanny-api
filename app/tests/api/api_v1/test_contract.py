from datetime import date, datetime
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
    assert response.status_code == 400
    
    start = contract.start + relativedelta(months=+13)
    month = start.month
    year = start.year
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400

    start = contract.start + relativedelta(months=+1)
    month = start.month
    year = start.year
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    print(response.json())
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
        "weekdays": "Mon Tue Thu Fri",
        "weeks": 47,
        "hours": 42.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 0.0,
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/" +
        f"?user_id={user_id}&nanny_id={nanny.id}",
        headers=normal_user_token_headers, json=data,
    )
    # print(response.json())
    assert response.status_code == 200
    contract = response.json()

    # Get contract Summary
    month = 9
    year = 2020
    
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract['id']}/summary/?year={year}&month={month}",
        headers=normal_user_token_headers,
    )
    # print(response.json())
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

    # assert content["business_days"] == 17
    assert content["working_days"] == 17
    assert content["presence_child"] == 17
    assert content["absence_child"] == 0
    assert content["disease_child"] == 0
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 178.5
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 178.5
    assert content["monthly_salary"] == 624.75
    assert content["monthly_fees"] == 52.36

    # Get day type
    # response = client.get(
    #     f"{settings.API_V1_STR}/day_types/",
    #     headers=normal_user_token_headers,
    # )
    # assert response.status_code == 200
    # content = response.json()
    # print(content)


    # CASE PRESENCE ENFANT
    # Create working day
    day_type_id = 1 # Présence enfant
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
    # print(response.json())
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
    assert content["monthly_fees"] == 55.44


    ## CASE MALADIE ENFANT
    # Create working day
    day_type_id = 2 # Maladie enfant
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
    assert content["absence_child"] == 1
    assert content["disease_child"] == 0
    assert content["disease_nanny"] == 0
    assert content["daysoff_child"] == 0
    assert content["daysoff_nanny"] == 0
    assert content["hours_standard"] == 178.5
    assert content["hours_complementary"] == 0
    assert content["hours_extra"] == 0
    assert content["monthly_hours"] == 178.5
    assert content["monthly_salary"] == 624.75
    assert content["monthly_fees"] == 52.36
