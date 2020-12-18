from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.WorkingDay])
def read_working_days(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    day_type_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve working_days.
    """
    if crud.user.is_superuser(current_user):
        working_days = crud.working_day.get_multi(db, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return working_days


@router.post("/", response_model=schemas.WorkingDay)
def create_working_day(
    *,
    db: Session = Depends(deps.get_db),
    working_day_in: schemas.WorkingDayCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    day_type_id: str,
    contract_id: str,
) -> Any:
    """
    Create new working_day.
    """
    contract = crud.contract.get(db, id=contract_id)
    if (int(current_user.id) == int(contract.user_id)) \
            or (int(current_user.id) == int(contract.nanny_id)) \
            or bool(current_user.is_superuser):
        if (crud.user.get(db, id=contract.user_id) and
                crud.user.get(db, id=contract.nanny_id)):
            pass
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User not responsible")

    working_day_exists = crud.working_day.get_by_day(
        db, day_type_id=day_type_id,
        contract_id=contract_id, day=working_day_in.day)
    if working_day_exists:
        raise HTTPException(status_code=400, detail="Working day already exists")

    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type_id, contract_id=contract_id)
    return working_day


@router.put("/{id}", response_model=schemas.WorkingDay)
def update_working_day(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    working_day_in: schemas.WorkingDayUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an working_day.
    """
    working_day = crud.working_day.get(db=db, id=id)
    contract = crud.contract.get(db=db, id=working_day.contract_id)
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    working_day = crud.working_day.update(
        db=db, db_obj=working_day, obj_in=working_day_in)
    return working_day


@router.get("/{id}", response_model=schemas.WorkingDay)
def read_working_day(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get working_day by ID.
    """
    working_day = crud.working_day.get(db=db, id=id)
    contract = crud.contract.get(db=db, id=working_day.contract_id)
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return working_day


@router.delete("/{id}", response_model=schemas.WorkingDayDelete)
def delete_working_day(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an working_day.
    """
    working_day = crud.working_day.get(db=db, id=id)
    contract = crud.contract.get(db=db, id=working_day.contract_id)
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    working_day = crud.working_day.remove(db=db, id=id)
    return working_day
