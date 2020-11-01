import json
import random
import string

from fastapi import status
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_day_types():
    res = client.get("/day_types/")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)

def test_read_day_type_nonExist():
    res = client.get("/day_types/99999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(res.json(), dict)

def test_create_day_type():
    day_type_name = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "name": f"{day_type_name}"
    }
    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), dict)

def test_create_day_type_alreadyExist():
    day_type_name = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "name": f"{day_type_name}"
    }
    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(res.json(), dict)
    assert res.json()["detail"] == "Day Type already exists"

def test_read_day_type_by_name():
    day_type_name = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "name": f"{day_type_name}"
    }
    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.get(f"/day_types/search/?name={day_type_name}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == f"{day_type_name}"

def test_delete_day_type():
    day_type_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "name": f"{day_type_name}"
    }
    res = client.post("/day_types/", json=data)
    assert res.status_code == status.HTTP_201_CREATED
    day_type_id = str(res.json()["id"])

    res = client.delete(f"/day_types/{day_type_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), dict)
    assert res.json().get("message") == f"Deleted Day Type {day_type_id}"

    res = client.get(f"/day_types/search/?name={day_type_name}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 0
