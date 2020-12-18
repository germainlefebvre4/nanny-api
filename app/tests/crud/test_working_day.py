from datetime import datetime

from sqlalchemy.orm import Session

from app import crud
from app.schemas.working_day import WorkingDayCreate, WorkingDayUpdate
from app.tests.utils.utils import (
    random_date_range, random_time_range)

from app.tests.utils.day_type import create_random_day_type
from app.tests.utils.contract import create_random_contract
from app.tests.utils.working_day import create_random_working_day


def test_create_working_day(db: Session) -> None:
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(str(contract.start), str(contract.end))
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)
    created_on = datetime.now()

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end)
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id)

    assert working_day.day_type_id == day_type.id
    assert working_day.contract_id == contract.id
    assert working_day.day == day
    assert working_day.start == start_time
    assert working_day.end == end_time
    assert isinstance(working_day.created_on, datetime)
    assert working_day.updated_on == None


def test_get_working_day(db: Session) -> None:
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(contract.start, contract.end)
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end,
    )
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id,
    )
    stored_working_day = crud.working_day.get(db=db, id=working_day.id)

    assert stored_working_day
    assert working_day.id == stored_working_day.id
    assert working_day.day_type_id == stored_working_day.day_type_id
    assert stored_working_day.day_type
    assert stored_working_day.day_type.id == day_type.id
    assert stored_working_day.day_type.name == day_type.name
    assert working_day.contract_id == stored_working_day.contract_id
    assert working_day.day == stored_working_day.day
    assert working_day.start == stored_working_day.start
    assert working_day.end == stored_working_day.end
    assert isinstance(stored_working_day.created_on, datetime)
    assert stored_working_day.updated_on == None

def test_get_working_day_by_day(db: Session) -> None:
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(contract.start, contract.end)
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)

    stored_working_day = crud.working_day.get_by_day(
        db=db, day_type_id=day_type.id, contract_id=contract.id, day=day)
    assert not stored_working_day
    

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end,
    )
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id,
    )
    stored_working_day = crud.working_day.get_by_day(
        db=db, day_type_id=day_type.id, contract_id=contract.id, day=day)

    assert stored_working_day
    assert working_day.id == stored_working_day.id
    assert working_day.day_type_id == stored_working_day.day_type_id
    assert working_day.contract_id == stored_working_day.contract_id
    assert working_day.day == stored_working_day.day
    assert working_day.start == stored_working_day.start
    assert working_day.end == stored_working_day.end
    assert isinstance(stored_working_day.created_on, datetime)
    assert stored_working_day.updated_on == None


# def test_get_working_days(db: Session) -> None:
#     day_type = create_random_day_type(db)
#     contract = create_random_contract(db)

#     day = random_date_range(contract.start, contract.end)
#     start_time = random_time_range(8, 12)
#     start = str(start_time)
#     end_time = random_time_range(14, 19)
#     end = str(end_time)

#     working_day_in = WorkingDayCreate(
#         day=day, start=start, end=end,)
#     working_day = crud.working_day.create_with_owner(
#         db=db, obj_in=working_day_in,
#         day_type_id=day_type.id, contract_id=contract.id,)
#     stored_working_days = crud.working_day.get_multi(
#         db=db, day_type_id=day_type.id, contract_id=contract.id)
#     stored_working_day = [x for x in stored_working_days if x.id == working_day.id][0]
#     assert isinstance(stored_working_days, list)
#     assert stored_working_day
#     assert working_day.id == stored_working_day.id
#     assert working_day.day_type_id == stored_working_day.day_type_id
#     assert working_day.contract_id == stored_working_day.contract_id
#     assert working_day.day == stored_working_day.day
#     assert working_day.start == stored_working_day.start
#     assert working_day.end == stored_working_day.end


def test_update_working_day(db: Session) -> None:
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(contract.start, contract.end)
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)
    created_on = datetime.now()
    updated_on = datetime.now()

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end)
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id)
    working_day_update = WorkingDayUpdate(
        day=day, start=start, end=end)
    working_day2 = crud.working_day.update(
        db=db, db_obj=working_day,
        obj_in=working_day_update)
    assert working_day.id == working_day2.id
    assert working_day.day_type_id == working_day2.day_type_id
    assert working_day.contract_id == working_day2.contract_id
    assert working_day.day == working_day2.day
    assert working_day.start == working_day2.start
    assert working_day.end == working_day2.end
    assert isinstance(working_day2.created_on, datetime)
    assert isinstance(working_day2.updated_on, datetime)


def test_delete_working_day(db: Session) -> None:
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(contract.start, contract.end)
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end)
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id)
    working_day2 = crud.working_day.remove(db=db, id=working_day.id)
    working_day3 = crud.working_day.get(db=db, id=working_day.id)
    assert working_day3 is None
    assert working_day2.id == working_day.id
    assert working_day2.day_type_id == working_day.day_type_id
    assert working_day2.contract_id == working_day.contract_id
    assert working_day2.day == working_day.day
    assert working_day2.start == working_day.start
    assert working_day2.end == working_day.end


def test_get_multi_by_month_by_contract(db: Session) -> None:
    create_random_working_day(db)
    
    day_type = create_random_day_type(db)
    contract = create_random_contract(db)

    day = random_date_range(str(contract.start), str(contract.end))
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)
    created_on = datetime.now()
    updated_on = datetime.now()

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end,
    )
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id,
    )
    
    month_str = str(day)[:7]
    working_day2 = crud.working_day.get_multi_by_month_by_contract(
        db=db, month=month_str, contract_id=contract.id
    )
    
    assert isinstance(working_day2, list)
    assert len(working_day2) == 1
    assert working_day2[0].id == working_day.id
    assert working_day2[0].day_type_id == working_day.day_type_id
    assert working_day2[0].contract_id == working_day.contract_id
    assert working_day2[0].day == working_day.day
    assert working_day2[0].start == working_day.start
    assert working_day2[0].end == working_day.end
