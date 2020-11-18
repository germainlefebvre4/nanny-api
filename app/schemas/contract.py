from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel


class ContractBase(BaseModel):
    weekdays: str
    weeks: int
    hours: float
    price_hour_standard: float
    price_hour_extra: Optional[float] = None
    price_fees: float
    price_meals: Optional[float] = None
    start: date
    end: date


class ContractCreate(ContractBase):
    weekdays: str
    weeks: int
    hours: float
    price_hour_standard: float
    price_hour_extra: Optional[float] = None
    price_fees: float
    price_meals: Optional[float] = None


class ContractUpdate(ContractBase):
    weekdays: str
    weeks: int
    hours: float
    price_hour_standard: float
    price_hour_extra: Optional[float] = None
    price_fees: float
    price_meals: Optional[float] = None
    start: date
    end: date


class ContractInDBBase(ContractBase):
    id: int
    user_id: int
    nanny_id: int
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class Contract(ContractInDBBase):
    pass


class ContractInDB(ContractInDBBase):
    pass
