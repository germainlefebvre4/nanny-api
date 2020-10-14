import pytest
from flask_api import status
import json
from collections import Counter
from datetime import datetime

def test_getContracts(client):
    res = client.get('/api/contracts')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 2

def test_getContractsById(client):
    res = client.get('/api/contracts/1')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    
    dict_keys = ["id", "user_id", "nanny_id"]
    assert Counter(dict_keys) == Counter(list(json_data.keys()))

def test_addContracts(client):
    data = {
        "user_id": 1,
        "nanny_id": 2,
        "weekdays": [1,2,3,4,5]
    }
    res = client.post(
        '/api/contracts',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

    contractId = json_data.get("id")

    print(json_data)
    print(contractId)

    res = client.get(f'/api/contracts/{contractId}')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)

def test_addContracts_missingParams(client):
    data = {}
    res = client.post(
        '/api/contracts',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()


def test_updateContracts(client):
    data = {
        "weekdays": [1,2,4,5],
        "start_date": "2019-09-01",
        "end_date": "2020-08-31"
    }
    res = client.put(
        '/api/contracts/1',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()


def test_deleteContracts(client):
    res = client.delete(
        f'/api/contracts/1',
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_deleteContracts_wrongParams(client):
    res = client.delete(
        '/api/contracts/1',
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_deleteContracts_missingParams(client):
    res = client.delete(
        '/api/contracts',
    )
    
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED