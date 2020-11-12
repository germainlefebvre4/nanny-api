from typing import List

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
        db_obj = self.model(**obj_in_data, user_id=user_id, nanny_id=nanny_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
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


contract = CRUDContract(Contract)
