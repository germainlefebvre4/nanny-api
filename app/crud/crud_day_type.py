from typing import Optional

# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.day_type import DayType
from app.schemas.day_type import DayTypeCreate, DayTypeUpdate


class CRUDDayType(CRUDBase[DayType, DayTypeCreate, DayTypeUpdate]):
    def get_multi(
        self, db: Session, *, filtered: bool = False, skip: int = 0, limit: int = 100
    ) -> Optional[DayType]:
        if filtered:
            return db.query(DayType).filter(
                DayType.id > 2
            ).offset(skip).limit(limit).all()
        else:
            return db.query(DayType).offset(skip).limit(limit).all()

    def get_by_name(
        self, db: Session, *, name: str
    ) -> Optional[DayType]:
        return db.query(DayType).filter(DayType.name == name).first()


day_type = CRUDDayType(DayType)
