from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.contract import Contract
from app.models.working_day import WorkingDay
from app.schemas.working_day import WorkingDayCreate, WorkingDayUpdate


class CRUDWorkingDay(CRUDBase[WorkingDay, WorkingDayCreate, WorkingDayUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: WorkingDayCreate,
        day_type_id: int, contract_id: int,
    ) -> WorkingDay:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, day_type_id=day_type_id, contract_id=contract_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(
        self, db: Session, *,
        id: int, user_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(
                Contract.user_id == user_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_contract(
        self, db: Session, *,
        contract_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(
                WorkingDay.contract_id == contract_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
        self, db: Session, *,
        day_type_id: int, contract_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(and_(
                WorkingDay.day_type_id == day_type_id,
                WorkingDay.contract_id == contract_id
            ))
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_multi_by_user(
        self, db: Session, *, 
        day_type_id: int, contract_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(and_(
                WorkingDay.day_type_id == day_type_id,
                WorkingDay.contract_id == contract_id
            ))
            # .filter(Contract.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

working_day = CRUDWorkingDay(WorkingDay)
