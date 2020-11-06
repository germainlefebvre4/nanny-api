from typing import List
from datetime import datetime, date, time, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import crud, models, schemas
from .database import SessionLocal, engine

# Database initialization
models.Base.metadata.create_all(bind=engine)

# App initialization
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Authentication
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
    WIP
"""
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# "clear_password": "secret"
# "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, email: str, password: str):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    db_user = crud.get_user_by_email(db, email=token_data.email)
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user







"""
    Day Type Generic
"""
@app.get("/day_types/", response_model=List[schemas.DayType], tags=["Day Types"])
async def read_day_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    day_types = crud.get_day_types(db, skip=skip, limit=limit)
    return day_types

@app.get("/day_types/{day_type_id}", response_model=schemas.DayType, tags=["Day Types"])
async def read_day_type(day_type_id: str, db: Session = Depends(get_db)):
    day_type = crud.get_day_type(db, day_type_id=day_type_id)
    if day_type is None:
        raise HTTPException(status_code=404, detail="Day Type not found")
    return day_type

@app.get("/day_types/search/", response_model=List[schemas.DayType], tags=["Day Types"])
async def read_day_type_by_name(name: str, db: Session = Depends(get_db)):
    db_day_type = crud.get_day_type_by_name(db, name=name)
    if not db_day_type:
        return []
    return [db_day_type]

@app.post("/day_types/", response_model=schemas.DayType, status_code=201, tags=["Day Types"])
async def create_day_type(day_type: schemas.DayTypeCreate, db: Session = Depends(get_db)):
    db_day_type = crud.get_day_type_by_name(db, name=day_type.name)
    if db_day_type:
        raise HTTPException(status_code=400, detail="Day Type already exists")
    return crud.create_day_type(db=db, day_type=day_type)

@app.delete("/day_types/{day_type_id}", response_model=schemas.Status, tags=["Day Types"])
async def delete_day_type(day_type_id: str, db: Session = Depends(get_db)):
    db_day_type = crud.get_day_type(db, day_type_id=day_type_id)
    if not db_day_type:
        raise HTTPException(status_code=404, detail="Day Type not found")
    crud.delete_day_type(db=db, day_type_id=day_type_id)
    return schemas.Status(message=f"Deleted Day Type {day_type_id}")


"""
    Users Generic
"""
@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=skip, limit=limit)
    return db_users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
async def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/search/", response_model=List[schemas.User], tags=["Users"])
async def read_user_by_email(email: str, firstname: str = None, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        return []
    return [db_user]

@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db=db, user=user)

@app.delete("/users/{user_id}", response_model=schemas.Status, tags=["Users"])
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return schemas.Status(message=f"Deleted User {user_id}")


"""
    Contracts Generic
"""
# GET
@app.get("/contracts/", response_model=List[schemas.Contract], tags=["Contracts"])
async def read_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contracts = crud.get_contracts(db, skip=skip, limit=limit)
    return contracts

@app.get("/contracts/{contract_id}", response_model=schemas.Contract, tags=["Contracts"])
async def read_contract(contract_id: str, db: Session = Depends(get_db)):
    contract = crud.get_contract(db, contract_id=contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.get("/contracts/search/", response_model=List[schemas.Contract], tags=["Contracts"])
async def read_contract_by_user_nanny(user_id: str, nanny_id: str, db: Session = Depends(get_db)):
    db_contract = crud.get_contracts_by_user_nanny(db, user_id=user_id, nanny_id=nanny_id)
    if not db_contract:
        return []
    return db_contract

@app.get("/contracts/search/by_date/", response_model=List[schemas.Contract], tags=["Contracts"])
async def read_contract_by_date(user_id: str, nanny_id: str, start: str, end: str, db: Session = Depends(get_db)):
    db_contract = crud.get_contracts_by_date(db, user_id=user_id, nanny_id=nanny_id, start=start, end=end)
    if not db_contract:
        return []
    return db_contract

# POST
@app.post("/contracts/", response_model=schemas.Contract, status_code=201, tags=["Contracts"])
async def create_contract(contract: schemas.ContractCreate, user_id: str = 1, nanny_id: str = 2, db: Session = Depends(get_db)):
    db_contract = crud.get_contracts_alreadyExists_by_date(db, user_id=user_id, nanny_id=nanny_id, start=contract.start, end=contract.end)
    print(db_contract)
    if db_contract:
        raise HTTPException(status_code=400, detail="Contract already exists")
    return crud.create_contract(db=db, contract=contract, user_id=user_id, nanny_id=nanny_id)

# DELETE
@app.delete("/contracts/{contract_id}", response_model=schemas.Status, tags=["Contracts"])
async def delete_contract(contract_id: str, db: Session = Depends(get_db)):
    db_contract = crud.get_contract(db, contract_id=contract_id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    crud.delete_contract(db=db, contract_id=contract_id)
    return schemas.Status(message=f"Deleted Contract {contract_id}")


"""
    Working Days Generic
"""
# GET
@app.get("/working_days/", response_model=List[schemas.WorkingDay], tags=["Working Days"])
async def read_working_days(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_working_days = crud.get_working_days(db, skip=skip, limit=limit)
    return db_working_days

@app.get("/working_days/{working_day_id}", response_model=schemas.WorkingDay, tags=["Working Days"])
async def read_working_day(working_day_id: str, db: Session = Depends(get_db)):
    db_working_day = crud.get_working_day(db, working_day_id=working_day_id)
    if db_working_day is None:
        raise HTTPException(status_code=404, detail="Working Day not found")
    return db_working_day

@app.get("/working_days/search/", response_model=List[schemas.WorkingDay], tags=["Working Days"])
async def read_working_day_by_contract_day_type(contract_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_working_days = crud.get_working_day_by_contract_day_type(db, contract_id=contract_id)
    if not db_working_days:
        return []
    return db_working_days

@app.get("/working_days/search/bydate/", response_model=List[schemas.WorkingDay], tags=["Working Days"])
async def read_working_day_by_date_range(contract_id: str, skip: int = 0, limit: int = 100, start: str = Query(date.today(), regex="^[0-9]{4}[-][0-9]{2}[-][0-9]{2}$"), end: str = Query(date.today(), regex="^[0-9]{4}[-][0-9]{2}[-][0-9]{2}$"), db: Session = Depends(get_db)):
    db_working_days = crud.get_working_days_by_date_range(db, contract_id=contract_id, start=start, end=end, skip=skip, limit=limit)
    if not db_working_days:
        return []
    return db_working_days

# POST
@app.post("/working_days/", response_model=schemas.WorkingDay, status_code=201, tags=["Working Days"])
async def create_working_day(working_day: schemas.WorkingDayCreate, contract_id: str, day_type_id: str, db: Session = Depends(get_db)):
    db_working_day = crud.get_working_day_by_date(db, contract_id=contract_id, day=working_day.day)
    if db_working_day:
        raise HTTPException(status_code=400, detail="Working Day already exists")
    db_contract = crud.get_contract(db, contract_id=contract_id)
    if not (db_contract.start <= working_day.day and working_day.day <= db_contract.end):
        raise HTTPException(status_code=400, detail="Working Day not in Contract date range")
    return crud.create_working_day(db=db, working_day=working_day, contract_id=contract_id, day_type_id=day_type_id)

# DELETE
@app.delete("/working_days/{working_day_id}", response_model=schemas.Status, tags=["Working Days"])
async def delete_working_day(working_day_id: str, db: Session = Depends(get_db)):
    db_working_day = crud.get_working_day(db, working_day_id=working_day_id)
    if not db_working_day:
        raise HTTPException(status_code=404, detail="Working Day not found")
    crud.delete_working_day(db=db, working_day_id=working_day_id)
    return schemas.Status(message=f"Deleted Working Day {working_day_id}")


"""
    Users Contracts
"""
# @app.post("/users/{user_id}/contracts/", response_model=schemas.Contract, tags=["Users", "Contracts"])
# def create_item_for_user(
#     user_id: str, item: schemas.ContractCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_contract(db=db, user_id=user_id)

# @app.post("/users/{user_id}/contracts/{contract_id}/", response_model=schemas.Contract, tags=["Users", "Contracts"])
# def create_item_for_user(
#     user_id: str, ocntract_id: str, item: schemas.ContractCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_contract(db=db, user_id=user_id, contract_id=contract_id)

"""
    Users Working Days
"""
# @app.post("/users/{user_id}/workingdays/", response_model=schemas.WorkingDay, tags=["Users", "Working Days"])
# def create_item_for_user(
#     user_id: int, item: schemas.WorkingDayCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_working_day(db=db, user_id=user_id)

# @app.post("/users/{user_id}/workingdays/{working_day_id}/", response_model=schemas.WorkingDay, tags=["Users","Working Days"])
# def create_item_for_user(
#     user_id: int, working_day_id: str, item: schemas.WorkingDayCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_working_day(db=db, user_id=user_id, working_day_id=working_day_id)

"""
    Contracts Working Days
"""



