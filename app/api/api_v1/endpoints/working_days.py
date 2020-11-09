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
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve working_days.
    """
    if crud.user.is_superuser(current_user):
        working_days = crud.working_day.get_multi(db, skip=skip, limit=limit)
    else:
        working_days = crud.working_day.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return working_days


@router.post("/", response_model=schemas.WorkingDay)
def create_working_day(
    *,
    db: Session = Depends(deps.get_db),
    working_day_in: schemas.WorkingDayCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new working_day.
    """
    working_day = crud.working_day.create_with_owner(db=db, obj_in=working_day_in, owner_id=current_user.id)
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
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if not crud.user.is_superuser(current_user) and (working_day.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    working_day = crud.working_day.update(db=db, db_obj=working_day, obj_in=working_day_in)
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
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if not crud.user.is_superuser(current_user) and (working_day.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return working_day


@router.delete("/{id}", response_model=schemas.WorkingDay)
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
    if not working_day:
        raise HTTPException(status_code=404, detail="WorkingDay not found")
    if not crud.user.is_superuser(current_user) and (working_day.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    working_day = crud.working_day.remove(db=db, id=id)
    return working_day
