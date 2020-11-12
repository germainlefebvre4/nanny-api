import random
import string
from datetime import date, time, datetime, timedelta

from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_int_range(start, end) -> int:
    return random.randint(start, end)


def random_float_range(start, end, precision=2) -> float:
    return round(random.uniform(start, end), precision)


def random_date_range(start, end) -> date:
    d1 = datetime.strptime(f"{start}", "%Y-%d-%m")
    d2 = datetime.strptime(f"{end}", "%Y-%d-%m")
    delta = d2 - d1
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    random_datetime = d1 + timedelta(seconds=random_second)
    return random_datetime.date()


def random_time_range(start, end) -> time:
    hour = random.randint(start, end)
    minute = random.randint(0, 59)
    return datetime.strptime(f"{hour}:{minute}", "%H:%M").time()


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.USER_ADMIN_EMAIL,
        "firstname": settings.USER_ADMIN_FIRSTNAME,
        "password": settings.USER_ADMIN_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
