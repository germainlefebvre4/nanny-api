import pytest
from flask_api import status
import json
from collections import Counter

def test_getContractWorkingDays(client):
    res = client.get('/api/contracts/1/workingdays')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 1

def test_getWorkingDaysById(client):
    res = client.get('/api/contracts/1/workingdays/1')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    dict_keys = ["id", "userid", "daytype_id", "day", "kind"]
    assert Counter(dict_keys) == Counter(list(json_data.keys()))

def test_getWorkingDaysByRangeDate_byYear(client):
    # Year
    res = client.get('/api/contracts/1/workingdays/search?year=2020')
    json_data = res.get_json()

    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_getContractWorkingDaysByRangeDate_byMonth(client):
    # Year and month
    res = client.get('/api/contracts/1/workingdays/search?year=2020&month=01')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 24
    # Inerited from contract
    assert len([x for x in json_data if x["daytype_id"] == 50]) == 22
    # Excluded from contract
    assert len([x for x in json_data if x["daytype_id"] == 49]) == 0
    # Days off
    assert len([x for x in json_data if x["daytype_id"] == 51]) == 1
    
    res = client.get('/api/contracts/1/workingdays/search?year=2020&month=9')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)


def test_getWorkingDaysByRangeDate_byDay(client):
    # Year, month and day
    res = client.get('/api/contracts/1/workingdays/search?year=2020&month=01&day=01')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 1
    assert json_data[0]["daytype_id"] == 51

    for day in range(11, 13):
        res = client.get(f'/api/contracts/1/workingdays/search?year=2020&month=01&day={day}')
        json_data = res.get_json()
        assert res.status_code == status.HTTP_200_OK
        assert len(json_data) == 0
    
    for day in range(7, 11):
        res = client.get(f'/api/contracts/1/workingdays/search?year=2020&month=01&day={day}')
        json_data = res.get_json()
        assert res.status_code == status.HTTP_200_OK
        assert len(json_data) == 1
        assert json_data[0]["daytype_id"] == 50

def test_getWorkingDaysByRangeDate_missingParams(client):
    res = client.get('/api/contracts/1/workingdays/search')
    json_data = res.get_json()

    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_addContractWorkingDays(client):
    data = {
        "day": "2020-02-04",
        "daytype_id": 4
    }
    res = client.post(
        '/api/contracts/1/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

    res = client.get('/api/contracts/1/workingdays/search?year=2020&month=02&day=04')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert json_data[0].get("day") == "2020-02-04"

def test_addWorkingDays_missingParams(client):
    data = {}
    res = client.post(
        '/api/contracts/1/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()


def test_delWorkingDays(client):
    data = {
        "day": "2020-03-04",
        "daytype_id": 4
    }
    res = client.post(
        '/api/contracts/1/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

    res = client.get('/api/contracts/1/workingdays/search?year=2020&month=03&day=04')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert json_data[0].get("day") == "2020-03-04"

    print(json_data)
    workingDayId = json_data[0].get("id")
    print(workingDayId)


    res = client.delete(
        f'/api/contracts/1/workingdays/{workingDayId}',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_delWorkingDays_wrongParams(client):
    res = client.delete(
        '/api/contracts/1/workingdays/1',
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_delWorkingDays_missingParams(client):
    res = client.delete(
        '/api/contracts/1/workingdays',
    )
    
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
