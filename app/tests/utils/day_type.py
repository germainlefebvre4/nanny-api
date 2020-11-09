from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.day_type import DayTypeCreate
from app.tests.utils.utils import random_lower_string


def create_random_day_type(db: Session) -> models.DayType:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name, id=id)
    return crud.day_type.create(db=db, obj_in=day_type_in)
