from typing import Optional
from datetime import date, time, datetime

from pydantic import BaseModel
from app.schemas.day_type import DayType


class WorkingDayBase(BaseModel):
    day: date
    start: time
    end: time


class WorkingDayCreate(WorkingDayBase):
    day: date
    start: time
    end: time


class WorkingDayUpdate(WorkingDayBase):
    day: date
    start: time
    end: time


class WorkingDayDelete(WorkingDayBase):
    id: int
    day_type_id: int
    contract_id: int
    day: date
    start: time
    end: time

    class Config:
        orm_mode = True


class WorkingDayInDBBase(WorkingDayBase):
    id: int
    contract_id: int
    day_type_id: int
    day_type: DayType
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class WorkingDay(WorkingDayInDBBase):
    pass


class WorkingDayInDB(WorkingDayInDBBase):
    pass
