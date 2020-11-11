from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.contract import ContractCreate
from app.tests.utils.utils import random_lower_string


def create_random_contract(db: Session) -> models.Contract:
    name = random_lower_string()
    contract_in = ContractCreate(name=name, id=id)
    return crud.contract.create(db=db, obj_in=contract_in)
