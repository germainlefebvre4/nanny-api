from datetime import datetime, date, time
from typing import List, Optional

from pydantic import BaseModel


"""
    Day Type
"""
class DayTypeBase(BaseModel):
    name: str

class DayTypeCreate(DayTypeBase):
    pass

class DayType(DayTypeBase):
    id: int
    
    class Config:
        orm_mode = True


"""
    Status
"""
class Status(BaseModel):
    message: str


"""
    Token
"""
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

"""
    User
"""
class UserBase(BaseModel):
    email: str
    firstname: str
    is_user: Optional[bool] = True
    is_nanny: Optional[bool] = False
    # username: str
    # full_name: Optional[str] = None
    # disabled: Optional[bool] = None
    # email: Optional[str] = None
    pass

class UserCreate(UserBase):
    password: str
    pass

class User(UserBase):
    id: int
    is_active: bool
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True


"""
    Contract
"""
class ContractBase(BaseModel):
    weekdays: int
    weeks: int
    hours: float
    price_hour_standard: float
    price_hour_extra: float
    price_fees: float
    price_meals: float
    start: date
    end: date

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    user_id: int
    nanny_id: int
    id: int
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    
    class Config:
        orm_mode = True



"""
    Working Day
"""
class WorkingDayBase(BaseModel):
    day: date
    start: time
    end: time

class WorkingDayCreate(WorkingDayBase):
    pass

class WorkingDay(WorkingDayBase):
    id: int
    contract_id: int
    day_type_id: int
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    
    class Config:
        orm_mode = True