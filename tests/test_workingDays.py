import pytest
from flask_api import status
import json

def test_getWorkingDaysAll(client):
    res = client.get('/api/workingdays')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 0

def test_getWorkingDaysById(client):
    res = client.get('/api/workingdays/1')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert "msg" in json_data.keys()

def test_getWorkingDaysByRangeDate_byYear(client):
    # Year
    res = client.get('/api/workingdays/search?year=2020')
    json_data = res.get_json()

    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_getWorkingDaysByRangeDate_byMonth(client):
    # Year and month
    res = client.get('/api/workingdays/search?year=2020&month=01')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 1
    
def test_getWorkingDaysByRangeDate_byDay(client):
    # Year, month and day
    res = client.get('/api/workingdays/search?year=2020&month=01&day=01')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)

def test_getWorkingDaysByRangeDate_missingParams(client):
    res = client.get('/api/workingdays/search')
    json_data = res.get_json()

    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_addWorkingDays(client):
    data = {
        "day": "2020-02-04",
        "absence": 4
    }
    res = client.post(
        '/api/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

    res = client.get('/api/workingdays/search?year=2020&month=02&day=04')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert json_data[0].get("day") == "2020-02-04"

def test_addWorkingDays_missingParams(client):
    data = {}
    res = client.post(
        '/api/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == 422
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()


def test_delWorkingDays(client):
    data = {
        "day": "2020-02-01",
        "absence": 4
    }
    res = client.post(
        '/api/workingdays',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_201_CREATED
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

    res = client.get('/api/workingdays/search?year=2020&month=02&day=01')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert json_data[0].get("day") == "2020-02-01"

    workingDayId = json_data[0].get("id")


    res = client.delete(
        f'/api/workingdays/{workingDayId}',
        data=json.dumps(data),
        content_type='application/json'
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_delWorkingDays_wrongParams(client):
    res = client.delete(
        '/api/workingdays/1',
    )
    json_data = res.get_json()
    
    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, dict)
    assert "msg" in json_data.keys()

def test_delWorkingDays_missingParams(client):
    res = client.delete(
        '/api/workingdays',
    )
    
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
