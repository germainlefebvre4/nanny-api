from sqlalchemy.orm import Session

from app import crud
from app.schemas.day_type import DayTypeCreate, DayTypeUpdate
from app.tests.utils.utils import random_lower_string


def test_create_day_type(db: Session) -> None:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name)
    day_type = crud.day_type.create(db=db, obj_in=day_type_in,)
    assert day_type.name == name


def test_get_day_type(db: Session) -> None:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name)
    day_type = crud.day_type.create(db=db, obj_in=day_type_in)
    stored_day_type = crud.day_type.get(db=db, id=day_type.id)
    assert stored_day_type
    assert day_type.id == stored_day_type.id
    assert day_type.name == stored_day_type.name


def test_get_day_type_by_name(db: Session) -> None:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name)
    day_type = crud.day_type.create(db=db, obj_in=day_type_in)
    stored_day_type = crud.day_type.get_by_name(db=db, name=day_type.name)
    assert stored_day_type
    assert day_type.name == stored_day_type.name


def test_update_day_type(db: Session) -> None:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name)
    day_type = crud.day_type.create(db=db, obj_in=day_type_in)
    day_type_update = DayTypeUpdate(name=name)
    day_type2 = crud.day_type.update(db=db, db_obj=day_type, obj_in=day_type_update)
    assert day_type.id == day_type2.id
    assert day_type.name == day_type2.name


def test_delete_day_type(db: Session) -> None:
    name = random_lower_string()
    day_type_in = DayTypeCreate(name=name)
    day_type = crud.day_type.create(db=db, obj_in=day_type_in)
    day_type2 = crud.day_type.remove(db=db, id=day_type.id)
    day_type3 = crud.day_type.get(db=db, id=day_type.id)
    assert day_type3 is None
    assert day_type2.id == day_type.id
    assert day_type2.name == name
