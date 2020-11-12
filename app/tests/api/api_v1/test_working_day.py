# from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import (
    random_date_range, random_time_range)
from app.tests.utils.day_type import create_random_day_type
from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract
from app.tests.utils.working_day import create_random_working_day


def test_create_working_day_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    contract = create_random_contract(db, user_id=user.id)
    day_type = create_random_day_type(db)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type.id}&contract_id={contract.id}",
        headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["day_type_id"] == day_type.id
    assert content["contract_id"] == contract.id
    assert content["day"] == data["day"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_working_day_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    day_type = create_random_day_type(db)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type.id}&contract_id={contract.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["day_type_id"] == day_type.id
    assert content["contract_id"] == contract.id
    assert content["day"] == data["day"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_working_day_for_another_user_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    contract = create_random_contract(db, user_id=user.id)
    day_type = create_random_day_type(db)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.post(
        f"{settings.API_V1_STR}/working_days/" +
        f"?day_type_id={day_type.id}&contract_id={contract.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 400


def test_read_working_day_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    working_day = create_random_working_day(db)
    response = client.get(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == str(working_day.day)
    assert content["start"] == str(working_day.start)
    assert content["end"] == str(working_day.end)


def test_read_working_day_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    day_type = create_random_day_type(db)
    working_day = create_random_working_day(
        db, day_type_id=day_type.id, contract_id=contract.id)
    response = client.get(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == str(working_day.day)
    assert content["start"] == str(working_day.start)
    assert content["end"] == str(working_day.end)


def test_read_working_day_for_another_user_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    working_day = create_random_working_day(db)
    response = client.get(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,)
    assert response.status_code == 400


def test_update_working_day_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    working_day = create_random_working_day(db, contract_id=contract.id)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.put(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=superuser_token_headers,
        json=data)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == data["day"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_working_day_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    nanny = create_random_user(db)
    contract = create_random_contract(
        db, user_id=user_id, nanny_id=nanny.id)
    day_type = create_random_day_type(db)
    working_day = create_random_working_day(
        db, day_type_id=day_type.id, contract_id=contract.id)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.put(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == data["day"]
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_working_day_for_another_user_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    working_day = create_random_working_day(db, contract_id=contract.id)
    data = {
        "day": str(random_date_range(contract.start, contract.end)),
        "start": str(random_time_range(8, 12)),
        "end": str(random_time_range(14, 19))
    }
    response = client.put(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 400


def test_delete_working_day_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    working_day = create_random_working_day(db)
    response = client.delete(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == str(working_day.day)
    assert content["start"] == str(working_day.start)
    assert content["end"] == str(working_day.end)


def test_delete_working_day_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers)
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    day_type = create_random_day_type(db)
    working_day = create_random_working_day(
        db, day_type_id=day_type.id, contract_id=contract.id)
    response = client.delete(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "day_type_id" in content
    assert "contract_id" in content
    assert content["day"] == str(working_day.day)
    assert content["start"] == str(working_day.start)
    assert content["end"] == str(working_day.end)


def test_delete_working_day_another_user_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    working_day = create_random_working_day(db)
    response = client.delete(
        f"{settings.API_V1_STR}/working_days/{working_day.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
