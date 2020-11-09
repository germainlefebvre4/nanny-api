from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Contract])
def read_contracts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve contracts.
    """
    if crud.user.is_superuser(current_user):
        contracts = crud.contract.get_multi(db, skip=skip, limit=limit)
    else:
        contracts = crud.contract.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return contracts


@router.post("/", response_model=schemas.Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: schemas.ContractCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new contract.
    """
    contract = crud.contract.create_with_owner(db=db, obj_in=contract_in, owner_id=current_user.id)
    return contract


@router.put("/{id}", response_model=schemas.Contract)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    contract_in: schemas.ContractUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contract.
    """
    contract = crud.contract.get(db=db, id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    if not crud.user.is_superuser(current_user) and (contract.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    contract = crud.contract.update(db=db, db_obj=contract, obj_in=contract_in)
    return contract


@router.get("/{id}", response_model=schemas.Contract)
def read_contract(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get contract by ID.
    """
    contract = crud.contract.get(db=db, id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    if not crud.user.is_superuser(current_user) and (contract.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return contract


@router.delete("/{id}", response_model=schemas.Contract)
def delete_contract(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an contract.
    """
    contract = crud.contract.get(db=db, id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    if not crud.user.is_superuser(current_user) and (contract.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    contract = crud.contract.remove(db=db, id=id)
    return contract
