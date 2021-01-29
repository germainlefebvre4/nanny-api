from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import holidays
import pandas
import json

from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
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
    # for contract in contracts:
    #     tmp = json.loads(contract["weekdays"])
    #     contract["weekdays"] = tmp
    return contracts


@router.post("/", response_model=schemas.Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: schemas.ContractCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    user_id: str,
    nanny_id: Optional[str] = None,
) -> Any:
    """
    Create new contract.
    """
    if (int(current_user.id) == int(user_id)) \
            or (int(current_user.id) == int(bool(nanny_id))) \
            or bool(current_user.is_superuser):
        if crud.user.get(db, id=user_id) and not nanny_id \
                or crud.user.get(db, id=user_id) and crud.user.get(db, id=nanny_id):
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
    contract_in.weekdays = json.dumps(contract_in.weekdays)
    contract = crud.contract.update(db=db, db_obj=contract, obj_in=contract_in)
    return contract


@router.put("/{id}/nanny", response_model=schemas.Contract)
async def update_contract_with_nanny_id(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    request: Request,
) -> Any:
    """
    Patch a contract with nanny user
    """
    nanny_id = int(await request.json())
    contract = crud.contract.get(db=db, id=id)
    
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    if (not crud.user.is_superuser(current_user) and
            (contract.user_id != current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    contract_patch = crud.contract.update_nanny_id(db=db, contract_id=id, nanny_id=nanny_id)
    contract = crud.contract.get(db=db, id=id)
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


@router.delete("/{id}", response_model=schemas.ContractDelete)
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
    
    hours_per_day, business_days_pandas, result = working_days_partial(working_days, contract, year, month, db)

    return result

def working_days_partial(working_days, contract, year, month, db):
    holidays_fra = [datetime.strftime(x[0], "%Y-%m-%d") 
        for x in holidays.FRA(years=int(year)).items() 
        if x[0] >= datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
            and x[0] <= datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date() + relativedelta(months=+1, days=-1)
    ]
    
    workingdays_list = [x.day for x in working_days]
    weekmask = " ".join([x for x in contract.weekdays.keys() if x != "enabled"])

    startDay = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
    endDay = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date() + relativedelta(months=+1, days=-1)
    business_days_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra).format()
    business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask=weekmask, holidays=holidays_fra+workingdays_list).format()
    hours_per_day = contract.hours/len(weekmask.split(' '))

    day_type_national_dayoff_name = "Jour férié"
    day_type_national_dayoff_id = crud.day_type.get_by_name(db, name=day_type_national_dayoff_name).id
    day_type_inherited_contract_name = "Projection du contrat"
    day_type_inherited_contract_id = crud.day_type.get_by_name(db, name=day_type_inherited_contract_name).id

    if contract.duration_mode == "daily":
        result = working_days + [
            schemas.WorkingDay(
                day=x,
                day_type_id=day_type_national_dayoff_id,
                day_type=schemas.DayType(
                    id=day_type_national_dayoff_id,
                    name=day_type_national_dayoff_name,
                ),
                contract_id=contract.id,
                id=0,
                start=datetime.strptime(f"00:00:00", "%H:%M:%S").time(),
                end=datetime.strptime(f"00:00:00", "%H:%M:%S").time(),
            )
            for x in holidays_fra
        ] + [
            schemas.WorkingDay(
                day=x,
                day_type_id=day_type_inherited_contract_id,
                day_type=schemas.DayType(
                    id=day_type_inherited_contract_id,
                    name=day_type_inherited_contract_name,
                ),
                contract_id=contract.id,
                id=0,
                start=datetime.strptime(f"08:00:00", "%H:%M:%S").time(),
                end=(datetime.strptime(f"08:00:00", "%H:%M:%S") + relativedelta(minutes=+int(hours_per_day*60))).time(),
            )
            for x in business_days_inherited_pandas
        ]
    elif contract.duration_mode == "free":
        result = working_days + [
            schemas.WorkingDay(
                day=x,
                day_type_id=day_type_national_dayoff_id,
                day_type=schemas.DayType(
                    id=day_type_national_dayoff_id,
                    name=day_type_national_dayoff_name,
                ),
                contract_id=contract.id,
                id=0,
                start=datetime.strptime(f"00:00:00", "%H:%M:%S").time(),
                end=datetime.strptime(f"00:00:00", "%H:%M:%S").time(),
            )
            for x in holidays_fra
        ]

    result.sort(key=lambda x: x.day)

    return hours_per_day, business_days_pandas, result

@router.get("/{id}/summary", response_model=Dict[Any, Any])
def read_contract_summary(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    year: str = Query(None, regex="^[2][0-9]{3}", min_length=4, max_length=4),
    month: str = Query(None, regex="^[01]?[0-9]", min_length=1, max_length=2),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve contracts summary by year and month.
    """
    if not year and not month:
        raise HTTPException(status_code=400, detail="Year and/or month not filled")
    input_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date() + relativedelta(months=+1, days=-1)
    contract = crud.contract.get(db=db, id=id)
    # contract_start = datetime.strptime(contract.year, "%Y-%m-%d")
    contract_start = contract.start
    contract_end = contract.end

    # if contract_start and contract_end:
    #     if input_date < contract_start or contract_end < input_date:
    #         raise HTTPException(status_code=400, detail="Date range not included in contract")
    # else:
    #     raise HTTPException(status_code=400, detail="Date range not included in contract")

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
    
    hours_per_day, business_days_pandas, result = working_days_partial(working_days, contract, year, month, db)

    # Flat the list from Working Days objects
    result_dict = [x.__dict__ for x in result]


    # Convert Series to DataFrame
    df = pandas.DataFrame(result_dict, columns=['day', 'start', 'end', 'id', 'contract_id', 'day_type_id', 'created_on', 'updated_on'])
    # Add column day_duration: count how many hours between start and end in the related day
    for index, row in df.iterrows():
        df.loc[index, 'day_duration_time'] = datetime.combine(date.today(), row.end) - datetime.combine(date.today(), row.start)
        df.loc[index, 'day_duration'] = (datetime.combine(date.today(), row.end) - datetime.combine(date.today(), row.start)).total_seconds()/3600
    # Add column Datime: setup pandas Datetime and set as index
    df['Datetime'] = df['day'].apply(lambda _: _)
    df = df.set_index(pandas.DatetimeIndex(df['Datetime']))
    # Add colum weekday: write day name trigramme (Mon, Tue, ...)
    df['weekday'] = df[['day']].apply(lambda x: datetime.strftime(x['day'], '%a'), axis=1)
    
    # print(df.to_string())

    # Day Types List:
    #   1 : Dayoff
    #   2 : Inherited contract
    #   3 : Presence child
    #   4 : Absence child
    #   5 : Disease child
    #   6 : Disease nanny
    #   7 : Dayoff child
    #   8 : Dayoff nanny
    business_days_count = len(business_days_pandas)
    # Working days = Business days - Disease child - Nanny disease - Child daysoff (- Dayoff)
    working_days_count = len([x for x in result if x.day_type_id not in [1, 5, 6, 7]])
    # Presence child days = Inherited presence + Forced presence
    presence_child_days_count = len([x for x in result if x.day_type_id in [2, 3]])
    absence_child_days_count = len([x for x in result if x.day_type_id in [4]])
    disease_child_days_count = len([x for x in result if x.day_type_id in [5]])
    disease_nanny_days_count = len([x for x in result if x.day_type_id in [6]])
    daysoff_child_days_count = len([x for x in result if x.day_type_id in [7]])
    daysoff_nanny_days_count = len([x for x in result if x.day_type_id in [8]])

    weekdays_duration = dict()
    if contract.duration_mode == "daily":
        for weekday in contract.weekdays:
            weekdays_duration[weekday] = contract.weekdays[weekday]["hours"]

        # Add day_duration_real column: real time spent in the day
        # df['day_duration_real'] = df[['weekday']].apply(lambda x: weekdays_duration[x['weekday']], axis=1)
        for index, row in df.iterrows():
            if df.loc[index, 'day_type_id'] not in [1,5,6,7]:
                if df.loc[index, 'weekday'] in weekdays_duration.keys():
                    df.loc[index, 'day_duration_min'] = weekdays_duration[df.loc[index, 'weekday']]
                else:
                    df.loc[index, 'day_duration_min'] = 0
            if df.loc[index, 'day_type_id'] in [4] and df.loc[index, 'day_duration'] == 0:
                df.loc[index, 'day_duration'] = float(df.loc[index, 'day_duration_min'])
        
        # Add day_duration_billed column: billed time of the day
        df['day_duration_billed'] = df[['day_duration_min', 'day_duration']].max(axis=1)
        # Evicted billed duration if 
        # df.loc[df['day_type_id name'] == 5, 'day_duration_billed'] = 0

        # Set hours and salary
        monthly_hours = 0
        monthly_salary = 0
        monthly_fees = 0

        hours_standard = 0
        hours_complementary = 0
        hours_extra = 0

        # Browse data range by week
        week_durations = df.groupby(pandas.Grouper(freq='W-SUN'))['day_duration_billed'].sum()
        for index, week_duration in week_durations.iteritems():
            week_hours_standard = min(week_duration, min(45, contract.hours))
            week_hours_complementary = min(max(0, week_duration-contract.hours), abs(45-week_duration))
            week_hours_extra = max(0, week_duration-45)

            monthly_hours += week_duration
            hours_standard += week_hours_standard
            hours_complementary += week_hours_complementary
            hours_extra += week_hours_extra

    elif contract.duration_mode == "free":
        monthly_hours =+ hours_per_day * absence_child_days_count
        monthly_salary = 0
        monthly_fees = 0

        hours_standard =+ hours_per_day * absence_child_days_count
        hours_complementary = 0
        hours_extra = 0

        # Group by week and sum for each week (date exposed is the last day of the related week)
        week_durations = df.groupby(pandas.Grouper(freq='W-SUN'))['day_duration'].sum()
        for index, day_duration in week_durations.iteritems():
            # week_duration = day_duration.total_seconds()/3600
            week_duration = day_duration
            week_hours_standard = min(week_duration, min(45, contract.hours))
            week_hours_complementary = min(max(0, week_duration-contract.hours), abs(45-week_duration))
            week_hours_extra = max(0, week_duration-45)

            monthly_hours += week_duration
            hours_standard += week_hours_standard
            hours_complementary += week_hours_complementary
            hours_extra += week_hours_extra
    
    # Salary = Hours standard * Price/hour + Hours compl. * Price/hour + Hours extra  Price/hour
    monthly_salary = hours_standard * contract.price_hour_standard + \
        hours_complementary * contract.price_hour_standard + \
        hours_extra * (contract.price_hour_extra)
    # Fees = Workings days * Price/hour
    monthly_fees = presence_child_days_count*contract.price_fees

    # Format float with 2 decimals
    hours_standard = float("{:.2f}".format(hours_standard))
    hours_complementary = float("{:.2f}".format(hours_complementary))
    hours_extra = float("{:.2f}".format(hours_extra))
    monthly_salary = float("{:.2f}".format(monthly_salary))
    monthly_fees = float("{:.2f}".format(monthly_fees))

    summary = dict(
        business_days=business_days_count,
        working_days=working_days_count,
        presence_child=presence_child_days_count,
        absence_child=absence_child_days_count,
        disease_child=disease_child_days_count,
        disease_nanny=disease_nanny_days_count,
        daysoff_child=daysoff_child_days_count,
        daysoff_nanny=daysoff_nanny_days_count,
        hours_standard=hours_standard,
        hours_complementary=hours_complementary,
        hours_extra=hours_extra,
        monthly_hours=monthly_hours,
        monthly_salary=monthly_salary,
        monthly_fees=monthly_fees,
        price_hour_standard=contract.price_hour_standard,
    )

    return summary


@router.post("/{id}/working_days", response_model=schemas.WorkingDay)
def create_working_day(
    *,
    db: Session = Depends(deps.get_db),
    working_day_in: schemas.WorkingDayCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    day_type_id: str,
    id: str,
) -> Any:
    """
    Create new working_day.
    """
    if (day_type_id in ["1", "2"]):
        raise HTTPException(status_code=400, detail="Day Type not authorized")

    contract = crud.contract.get(db, id=id)

    if (int(current_user.id) == int(contract.user_id)) \
            or (int(current_user.id) == int(contract.nanny_id)) \
            or bool(current_user.is_superuser):
        if (crud.user.get(db, id=contract.user_id)): # crud.user.get(db, id=contract.nanny_id)
            pass
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="User not responsible")
    working_day = crud.working_day.create_with_owner(
        db=db, obj_in=working_day_in,
        day_type_id=day_type_id, contract_id=id)
    return working_day
