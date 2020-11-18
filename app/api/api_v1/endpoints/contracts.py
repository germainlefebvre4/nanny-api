from datetime import datetime
from dateutil.relativedelta import relativedelta
import holidays
import pandas

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
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
        contracts = crud.contract.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return contracts


@router.post("/", response_model=schemas.Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: schemas.ContractCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    user_id: str,
    nanny_id: str,
) -> Any:
    """
    Create new contract.
    """
    if (int(current_user.id) == int(user_id)) \
            or (int(current_user.id) == int(nanny_id)) \
            or bool(current_user.is_superuser):
        if crud.user.get(db, id=user_id) and crud.user.get(db, id=nanny_id):
            pass
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User not responsible")
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user_id, nanny_id=nanny_id)
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
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
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
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
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
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    contract = crud.contract.remove(db=db, id=id)
    return contract


# By contract
@router.get("/{id}/working_days", response_model=List[schemas.WorkingDay])
def read_working_days(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    year: str = Query(None, regex="^[2][0-9]{3}", min_length=4, max_length=4),
    month: str = Query(None, regex="^[01]?[0-9]", min_length=1, max_length=2),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve working_days by contract.
    """
    contract = crud.contract.get(db=db, id=id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    if year and month:
        month_date = datetime.strptime(f"{year}-{month}", "%Y-%m").date()
        next_month_date = month_date + relativedelta(months=+1, days=-1)
        working_days = crud.working_day.get_multi_by_contract_by_date(
            db=db, contract_id=id, start=month_date, end=next_month_date)
    else:
        working_days = crud.working_day.get_multi_by_contract(
            db=db, contract_id=id)
    
        
    holidays_fra = [datetime.strftime(x[0], "%Y-%m-%d") 
        for x in holidays.FRA(years=int(year)).items() 
        if x[0] >= datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
            and x[0] < datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date() + relativedelta(months=+1)
    ]
    
    workingdays_list = [x.day for x in working_days]
    weekmask = contract.weekdays

    startDay = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
    endDay = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date() + relativedelta(months=+1)
    business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask=weekmask, holidays=holidays_fra+workingdays_list).format()
    
    result = working_days + [
        schemas.WorkingDay(
            day=x,
            day_type_id=51,
            contract_id=contract.id,
            id=0,
            start=datetime.strptime(f"09:00:00", "%H:%M:%S").time(),
            end=datetime.strptime(f"18:00:00", "%H:%M:%S").time(),
        )
        for x in holidays_fra
    ] + [
        schemas.WorkingDay(
            day=x,
            day_type_id=50,
            contract_id=contract.id,
            id=0,
            start=datetime.strptime(f"09:00:00", "%H:%M:%S").time(),
            end=(datetime.strptime(f"09:00:00", "%H:%M:%S") + relativedelta(hours=+int(contract.hours))).time(),
        )
        for x in business_days_inherited_pandas
    ]
    result.sort(key=lambda x: x.day)
        
    return result
