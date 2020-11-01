import json
import random
import string

from fastapi import status
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_users():
    res = client.get("/users/")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)

def test_read_user_nonExist():
    res = client.get("/users/99999")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(res.json(), dict)

def test_read_user_badParam():
    res = client.get("/users/test")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert isinstance(res.json(), dict)

def test_create_user():
    user_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password
    }
    res = client.post("/users/",json=data)
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(res.json(), dict)
    assert res.json()["email"] == user_email
    assert res.json()["firstname"] == user_firstname

def test_create_user_alreadyExist():
    user_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))

    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password
    }
    res = client.post("/users/",json=data)
    assert res.status_code == status.HTTP_201_CREATED

    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password
    }
    res = client.post("/users/",json=data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(res.json(), dict)
    assert res.json().get("detail") == "Email already exists"

def test_read_user_by_email():
    user_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password
    }
    res = client.post("/users/",json=data)
    
    res = client.get(f"/users/search/?email={user_email}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) == 1
    assert res.json()[0]["email"] == f"{user_email}"

def test_delete_user():
    user_email = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_firstname = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    user_password = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    data = {
        "email": user_email,
        "firstname": user_firstname,
        "password": user_password
    }
    res = client.post("/users/",json=data)
    assert res.status_code == status.HTTP_201_CREATED

    res = client.get(f"/users/search/?email={user_email}")
    user_id = res.json()[0]["id"]
    assert res.status_code == status.HTTP_200_OK

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(res.json(), dict)
    assert res.json().get("message") == f"Deleted User {user_id}"



# def test_getUserProfile_badUser():
#     res = client.get("/api/users/profile")
#     json_data = res.get_json()

#     assert res.status_code == status.HTTP_401_UNAUTHORIZED
#     assert isinstance(json_data, dict)
#     assert "msg" in json_data.keys()

# def test_getUserContracts():
#     res = client.get("/api/users/contracts")
#     json_data = res.get_json()

#     assert res.status_code == status.HTTP_200_OK
#     assert isinstance(json_data, list)
#     assert len(json_data) == 1

# def test_getUserContractsOrphans():
#     res = client.get("/api/users/contracts/orphans")
#     json_data = res.get_json()

#     assert res.status_code == status.HTTP_200_OK
#     assert isinstance(json_data, list)
#     assert len(json_data) == 0

# def test_getUserContractsOrphans_addContract():
#     data = {
#         "user_id": 1,
#         "nanny_id": 2,
#         "weeks": 45,
#         "hours": 9.5,
#         "weekdays": ["True","True","True","True","True","",""],
#         "price_hour_standard": 3.5,
#         "price_hour_extra": 3.8,
#         "price_fees": 3.08
#     }
#     res = client.post(
#         "/api/contracts",
#         json=json.dumps(data),
#         content_type="application/json"
#     )

#     res = client.get("/api/users/contracts/orphans")
#     json_data = res.get_json()

#     assert res.status_code == status.HTTP_200_OK
#     assert isinstance(json_data, list)
#     assert len(json_data) == 1

