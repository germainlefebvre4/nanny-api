import pytest
from flask_api import status
import json

def test_getDayType(client):
    res = client.get('/api/daytype')
    json_data = res.get_json()

    assert res.status_code == status.HTTP_200_OK
    assert isinstance(json_data, list)
    assert len(json_data) == 8
