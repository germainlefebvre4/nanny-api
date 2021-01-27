from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.DayType])
def read_day_types(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    filtered: bool = False,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve day_types.
    """
    day_types = crud.day_type.get_multi(db, filtered=filtered, skip=skip, limit=limit)
    return day_types


@router.get("/_search", response_model=schemas.DayType)
def read_day_type_with_email(
    db: Session = Depends(deps.get_db),
    name: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve day_type with name.
    """
    day_type = crud.day_type.get_by_name(db, name=name)
    return day_type


@router.post("/", response_model=schemas.DayType)
def create_day_type(
    *,
    db: Session = Depends(deps.get_db),
    day_type_in: schemas.DayTypeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new day_type.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    day_type = crud.day_type.create(db=db, obj_in=day_type_in)
    return day_type


@router.put("/{id}", response_model=schemas.DayType)
def update_day_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    day_type_in: schemas.DayTypeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an day_type.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    day_type = crud.day_type.get(db=db, id=id)
    if not day_type:
        raise HTTPException(status_code=404, detail="DayType not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    day_type = crud.day_type.update(db=db, db_obj=day_type, obj_in=day_type_in)
    return day_type


@router.get("/{id}", response_model=schemas.DayType)
def read_day_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get day_type by ID.
    """
    day_type = crud.day_type.get(db=db, id=id)
    if not day_type:
        raise HTTPException(status_code=404, detail="DayType not found")
    return day_type


@router.delete("/{id}", response_model=schemas.DayType)
def delete_day_type(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an day_type.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    day_type = crud.day_type.get(db=db, id=id)
    if not day_type:
        raise HTTPException(status_code=404, detail="DayType not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    day_type = crud.day_type.remove(db=db, id=id)
    return day_type
