from datetime import datetime

from typing import List, Dict, Union, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate


class CRUDContract(CRUDBase[Contract, ContractCreate, ContractUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ContractCreate, user_id: int, nanny_id: int
    ) -> Contract:
        obj_in_data = jsonable_encoder(obj_in)
        created_on = datetime.now()
        db_obj = self.model(**obj_in_data, user_id=user_id, nanny_id=nanny_id,
            created_on=created_on)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Contract]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contract]:
        return (
            db.query(self.model)
            .filter(Contract.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_nanny(
        self, db: Session, *, nanny_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contract]:
        return (
            db.query(self.model)
            .filter(Contract.nanny_id == nanny_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Contract,
        obj_in: Union[ContractUpdate, Dict[str, Any]]
    ) -> Contract:
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

contract = CRUDContract(Contract)
