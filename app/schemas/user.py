from typing import Optional

from pydantic import BaseModel, EmailStr


class NannyBase(BaseModel):
    email: EmailStr
    firstname: str


class NannyInDBBase(NannyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Nanny(NannyInDBBase):
    pass


class NannyInDB(NannyInDBBase):
    pass


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    is_active: Optional[bool] = True
    is_user: Optional[bool] = True
    is_nanny: Optional[bool] = False
    is_superuser: bool = False


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
