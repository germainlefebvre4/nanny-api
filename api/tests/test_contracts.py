import json
import random
import string
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from fastapi import status
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def bundle_create_user():
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
    res = client.post(f"/users/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    nanny_id = res.json()["id"]

    return user_id, nanny_id


def test_read_contracts():
    res = client.get("/contracts/")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 0


def test_read_contract_nonExist():
    res = client.get("/contracts/99999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(res.json(), dict)


def test_create_contract():
    user_id, nanny_id = bundle_create_user()
    date_today = date.today()

    # Create Contract
    contract_start = str(date_today)
    contract_end = str(date_today + relativedelta(months=+12, days=-1))
    data = {
        "weekdays": 5,
        "weeks": 44,
        "hours": 40.0,
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08,
        "price_meals": 4.0,
        "start": contract_start,
        "end": contract_end
    }
    res = client.post(f"/contracts/?user_id={user_id}&nanny_id={nanny_id}",json=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), dict)
    assert res.json()["user_id"] == user_id
    assert res.json()["nanny_id"] == nanny_id
    assert res.json()["start"] == contract_start
    assert res.json()["end"] == contract_end

    res = client.get(f"/contracts/search/?user_id={user_id}&nanny_id={nanny_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1


def test_create_contract_alreadyExist():
    user_id, nanny_id = bundle_create_user()
    date_today = date.today()

    # Create Contract
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
    res = client.post(f"/contracts/?user_id={user_id}&nanny_id={nanny_id}",json=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), dict)
    
    # Create the same Contract
    res = client.post(f"/contracts/?user_id={user_id}&nanny_id={nanny_id}",json=data)
    print(res.json())
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(res.json(), dict)
    assert res.json()["detail"] == "Contract already exists"
    

def test_delete_contract():
    user_id, nanny_id = bundle_create_user()
    date_today = date.today()

    # Create Contract
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
    res = client.post(f"/contracts/?user_id={user_id}&nanny_id={nanny_id}",json=data)
    contract_id = res.json()["id"]

    res = client.delete(f"/contracts/{contract_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), dict)
    assert res.json().get("message") == f"Deleted Contract {contract_id}"
    