from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from typing import List, Union, Dict, Any

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
        created_on = datetime.now()
        db_obj = self.model(
            **obj_in_data, day_type_id=day_type_id, contract_id=contract_id,
            created_on=created_on)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def get_by_user(
    #     self, db: Session, *,
    #     id: int, user_id: int,
    #     skip: int = 0, limit: int = 100,
    # ) -> List[WorkingDay]:
    #     return (
    #         db.query(self.model)
    #         .join(WorkingDay.contract)
    #         .filter(
    #             Contract.user_id == user_id
    #         )
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    def get_multi_by_contract(
        self, db: Session, *,
        contract_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(
                Contract.id == contract_id
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_contract_by_date(
        self, db: Session, *,
        contract_id: int,
        start: date,
        end: date,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(
                and_(
                    Contract.id == contract_id,
                    start <= WorkingDay.day,
                    WorkingDay.day <= end,
                )
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
        day_type_id: int,
        contract_id: int,
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

    def get_multi_by_month_by_contract(
        self, db: Session, *,
        month: str,
        contract_id: int,
        skip: int = 0, limit: int = 100,
    ) -> List[WorkingDay]:
        month_start = datetime.strptime(month+"-01", "%Y-%m-%d")
        month_start_str = str(month_start)
        month_end = (month_start + relativedelta(months=+1))
        month_end_str = str(month_end)
        return (
            db.query(self.model)
            .join(WorkingDay.contract)
            .filter(and_(
                WorkingDay.contract_id == contract_id,
                WorkingDay.day >= month_start_str,
                WorkingDay.day < month_end_str,
            ))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: WorkingDay,
        obj_in: Union[WorkingDayUpdate, Dict[str, Any]]
    ) -> WorkingDay:
        obj_data = jsonable_encoder(db_obj)
        updated_on = datetime.now()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data = {**update_data, **dict(updated_on=updated_on)}
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


working_day = CRUDWorkingDay(WorkingDay)
