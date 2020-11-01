import json
import random
import string
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from fastapi import status
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def bundle_create_contract():
    # Create User : User
    user_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password,
        "is_user": True,
        "is_nanny": False
    }
    res = client.post("/users/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    user_id = res.json()["id"]
    
    # Create User : Nanny
    nanny_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    nanny_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    nanny_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "email": nanny_email,
        "firstname": nanny_firstname,
        "password": nanny_password,
        "is_user": False,
        "is_nanny": True
    }
    res = client.post("/users/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    nanny_id = res.json()["id"]

    # Create Contract
    date_today = date.today()
    data = {
        "weekdays": 5,
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": str(date_today + relativedelta(months=-2)),
        "end": str(date_today + relativedelta(months=+10, days=-1))
    }
    res = client.post(f"/contracts/?user_id={user_id}&nanny_id={nanny_id}", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    contract_id = res.json()["id"]

    # Create Day Type
    day_type_name = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "name": f"{day_type_name}"
    }
    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    day_type_id = res.json()["id"]

    return day_type_id, user_id, nanny_id, contract_id

def test_read_working_days():
    res = client.get("/working_days/")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)

def test_read_working_day_dontExist():
    res = client.get("/working_days/99999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(res.json(), dict)

def test_create_working_day():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    data = {
        "day": str(date_today),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), dict)

    res = client.get(f"/working_days/search/?contract_id={contract_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1

def test_create_working_days_badDuplicates():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    data = {
        "day": str(date_today),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_read_working_days_byDate():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    data = {
        "day": str(date_today),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.get(f"/working_days/search/?contract_id={contract_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1

    # Create Working Day
    data = {
        "day": str(date_today + relativedelta(days=+1)),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.get(f"/working_days/search/?contract_id={contract_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 2

def test_read_working_day_byDateRange():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    data = {
        "day": str(date_today),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    print(res.json())
    assert res.status_code == status.HTTP_201_CREATED

    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

def test_create_working_day_badDateFormat():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    date_today = reversed(str(date.today()).split("-"))
    date_today_reverse = "-".join(date_today)
    data = {
        "day": date_today_reverse,
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == 422
    assert isinstance(res.json(), dict)
    assert res.json()["detail"][0]["msg"] == "invalid date format"

def test_create_working_day_inWrongRangeTimeContract():
    day_type_id, user_id, nanny_id, contract_id = bundle_create_contract()
    date_today = date.today()

    # Create Working Day
    data = {
        "day": str(date_today + relativedelta(months=+18)),
        "start": "09:00:00",
        "end": "17:00:00"
    }
    res = client.post(f"/working_days/?contract_id={contract_id}&day_type_id={day_type_id}", json=data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json()["detail"] == "Working Day not in Contract date range"
