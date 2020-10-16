import pytest
from flask_api import status
import json

def test_getUserProfile(client):
    res = client.get('/api/users/profile')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)

# def test_getUserProfile_badUser(client):
#     res = client.get('/api/users/profile')
#     json_data = res.get_json()

#     assert res.status_code == status.HTTP_401_UNAUTHORIZED
#     assert isinstance(json_data, dict)
#     assert "msg" in json_data.keys()

def test_getUserContracts(client):
    res = client.get('/api/users/contracts')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 1

def test_getUserContractsOrphans(client):
    res = client.get('/api/users/contracts/orphans')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 0

def test_getUserContractsOrphans_addContract(client):
    data = {
        "user_id": 1,
        "nanny_id": 2,
        "weeks": 45,
        "hours": 9.5,
        "weekdays": ["True","True","True","True","True","",""],
        "price_hour_standard": 3.5,
        "price_hour_extra": 3.8,
        "price_fees": 3.08
    }
    res = client.post(
        '/api/contracts',
        data=json.dumps(data),
        content_type='application/json'
    )

    res = client.get('/api/users/contracts/orphans')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 1

