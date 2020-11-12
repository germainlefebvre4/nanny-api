from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.contract import ContractCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range)

from app.tests.utils.user import create_random_user


def create_random_contract(
        db: Session,
        user_id: int = None,
        nanny_id: int = None,
        ) -> models.Contract:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    if not nanny_id:
        nanny = create_random_user(db)
        nanny_id = nanny.id

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
            price_fees=price_fees, price_meals=price_meals, start=start, end=end,
        )
    return crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user_id, nanny_id=nanny_id)
