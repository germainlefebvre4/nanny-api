from datetime import datetime, date, time
from typing import List, Optional

from pydantic import BaseModel


# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True



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
    User
"""
class UserBase(BaseModel):
    email: str
    firstname: str

class UserCreate(UserBase):
    password: str
    pass

class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    is_user: bool
    is_nanny: bool
    is_admin: bool
    
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