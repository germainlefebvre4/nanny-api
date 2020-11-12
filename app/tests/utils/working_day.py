from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.working_day import WorkingDayCreate
from app.tests.utils.utils import (
    random_date_range, random_time_range)

from app.tests.utils.day_type import create_random_day_type
from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract


def create_random_working_day(
        db: Session,
        user_id: int = None,
        nanny_id: int = None,
        day_type_id: int = None,
        contract_id: int = None,
        ) -> models.WorkingDay:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    if not nanny_id:
        nanny = create_random_user(db)
        nanny_id = nanny.id
    if day_type_id:
        day_type = crud.day_type.get(db, id=day_type_id)
    else:
        day_type = create_random_day_type(db)
    if contract_id:
        contract = crud.contract.get(db, id=contract_id)
    else:
        contract = create_random_contract(db, user_id=user.id, nanny_id=nanny.id)

    day = random_date_range(contract.start, contract.end)
    start_time = random_time_range(8, 12)
    start = str(start_time)
    end_time = random_time_range(14, 19)
    end = str(end_time)

    working_day_in = WorkingDayCreate(
        day=day, start=start, end=end,
    )
    return crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type.id, contract_id=contract.id,
    )
