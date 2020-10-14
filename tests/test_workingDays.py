import pytest
from flask_api import status

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
    assert isinstance(json_data, dict)