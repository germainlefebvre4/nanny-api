from pydantic import BaseModel


class DayTypeBase(BaseModel):
    name: str


class DayTypeCreate(DayTypeBase):
    name: str
    pass


class DayTypeUpdate(DayTypeBase):
    name: str


class DayTypeInDBBase(DayTypeBase):
    id: int

    class Config:
        orm_mode = True


class DayType(DayTypeInDBBase):
    pass


class DayTypeInDB(DayTypeInDBBase):
    pass
