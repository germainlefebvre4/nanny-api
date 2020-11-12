from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from sqlalchemy.orm import Session

from app import crud
from app.schemas.contract import ContractCreate, ContractUpdate
from app.tests.utils.utils import (random_lower_string, random_int_range,
    random_float_range)

from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract


def test_create_contract(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start_date = date_today
    start = str(start_date)
    end_date = date_today + relativedelta(months=+12, days=-1)
    end = str(end_date)
    
    contract_in = ContractCreate(
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)

    assert contract.user_id == user.id
    assert contract.nanny_id == nanny.id
    assert contract.weekdays == weekdays
    assert contract.weeks == weeks
    assert contract.hours == hours
    assert contract.price_hour_standard == price_hour_standard
    assert contract.price_hour_extra == price_hour_extra
    assert contract.price_fees == price_fees
    assert contract.start == start_date
    assert contract.end == end_date


def test_get_contract(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    
    contract_in = ContractCreate(
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)
    stored_contract = crud.contract.get(db=db, id=contract.id)

    assert stored_contract
    assert contract.id == stored_contract.id
    assert contract.user_id == stored_contract.user_id
    assert contract.nanny_id == stored_contract.nanny_id
    assert contract.weekdays == stored_contract.weekdays
    assert contract.weeks == stored_contract.weeks
    assert contract.hours == stored_contract.hours
    assert contract.price_hour_standard == stored_contract.price_hour_standard
    assert contract.price_hour_extra == stored_contract.price_hour_extra
    assert contract.price_fees == stored_contract.price_fees
    assert contract.price_meals == stored_contract.price_meals
    assert contract.start == stored_contract.start
    assert contract.end == stored_contract.end


def test_get_contract_by_user(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    
    contract_in = ContractCreate(
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)
    stored_contracts = crud.contract.get_multi_by_user(db=db, user_id=contract.user_id)
    stored_contract = [x for x in stored_contracts if x.id == contract.id][0]
    assert isinstance(stored_contracts, list)
    assert stored_contract
    assert contract.id == stored_contract.id
    assert contract.user_id == stored_contract.user_id
    assert contract.nanny_id == stored_contract.nanny_id
    assert contract.weekdays == stored_contract.weekdays
    assert contract.weeks == stored_contract.weeks
    assert contract.hours == stored_contract.hours
    assert contract.price_hour_standard == stored_contract.price_hour_standard
    assert contract.price_hour_extra == stored_contract.price_hour_extra
    assert contract.price_fees == stored_contract.price_fees
    assert contract.price_meals == stored_contract.price_meals
    assert contract.start == stored_contract.start
    assert contract.end == stored_contract.end


def test_get_contract_by_nanny(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    
    contract_in = ContractCreate(user_id=user.id, nanny_id=nanny.id,
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)
    stored_contracts = crud.contract.get_multi_by_nanny(db=db, nanny_id=contract.nanny_id)
    stored_contract = [x for x in stored_contracts if x.id == contract.id][0]
    assert isinstance(stored_contracts, list)
    assert stored_contract
    assert contract.id == stored_contract.id
    assert contract.user_id == stored_contract.user_id
    assert contract.nanny_id == stored_contract.nanny_id
    assert contract.weekdays == stored_contract.weekdays
    assert contract.weeks == stored_contract.weeks
    assert contract.hours == stored_contract.hours
    assert contract.price_hour_standard == stored_contract.price_hour_standard
    assert contract.price_hour_extra == stored_contract.price_hour_extra
    assert contract.price_fees == stored_contract.price_fees
    assert contract.price_meals == stored_contract.price_meals
    assert contract.start == stored_contract.start
    assert contract.end == stored_contract.end


def test_update_contract(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    
    contract_in = ContractCreate(user_id=user.id, nanny_id=nanny.id,
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)
    contract_update = ContractUpdate(weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end)
    contract2 = crud.contract.update(db=db, db_obj=contract, obj_in=contract_update)
    assert contract.id == contract2.id
    assert contract.user_id == contract2.user_id
    assert contract.nanny_id == contract2.nanny_id
    assert contract.weekdays == contract2.weekdays
    assert contract.weeks == contract2.weeks
    assert contract.hours == contract2.hours
    assert contract.price_hour_standard == contract2.price_hour_standard
    assert contract.price_hour_extra == contract2.price_hour_extra
    assert contract.price_fees == contract2.price_fees
    assert contract.price_meals == contract2.price_meals
    assert contract.start == contract2.start
    assert contract.end == contract2.end


def test_delete_contract(db: Session) -> None:
    user = create_random_user(db)
    nanny = create_random_user(db)
    
    date_today = date.today()
    weekdays = random_int_range(1, 5)
    weeks = random_int_range(20, 47)
    hours = random_int_range(10, 50)
    price_hour_standard = random_float_range(2.5, 4, 1)
    price_hour_extra = random_float_range(2.5, 4, 1)
    price_fees = random_float_range(3.08, 5, 2)
    price_meals = random_float_range(2, 6, 1)
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    
    contract_in = ContractCreate(user_id=user.id, nanny_id=nanny.id,
            weekdays=weekdays, weeks=weeks, hours=hours,
            price_hour_standard=price_hour_standard, price_hour_extra=price_hour_extra,
            price_fees=price_fees, price_meals=price_meals, start=start, end=end
        )
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, user_id=user.id, nanny_id=nanny.id)
    contract2 = crud.contract.remove(db=db, id=contract.id)
    contract3 = crud.contract.get(db=db, id=contract.id)
    assert contract3 is None
    assert contract.id == contract.id
    assert contract2.user_id == contract.user_id
    assert contract2.nanny_id == contract.nanny_id
    assert contract2.weekdays == contract.weekdays
    assert contract2.weeks == contract.weeks
    assert contract2.hours == contract.hours
    assert contract2.price_hour_standard == contract.price_hour_standard
    assert contract2.price_hour_extra == contract.price_hour_extra
    assert contract2.price_fees == contract.price_fees
    assert contract2.price_meals == contract.price_meals
    assert contract2.start == contract.start
    assert contract2.end == contract.end
