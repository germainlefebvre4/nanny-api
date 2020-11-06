from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from passlib.context import CryptContext

from . import models, schemas

# Authentication Crypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
    Day Type
"""
def get_day_type(db: Session, day_type_id: int):
    return db.query(models.DayType).filter(models.DayType.id == day_type_id).first()

def get_day_type_by_name(db: Session, name: str):
    return db.query(models.DayType).filter(models.DayType.name == name).first()

def get_day_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DayType).offset(skip).limit(limit).all()

def create_day_type(db: Session, day_type: schemas.DayTypeCreate):
    db_day_type = models.DayType(name=day_type.name)
    db.add(db_day_type)
    db.commit()
    db.refresh(db_day_type)
    return db_day_type

def delete_day_type(db: Session, day_type_id: int):
    count = db.query(models.DayType).filter(models.DayType.id == day_type_id).delete()
    db.commit()
    return count


"""
    Users
"""
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str, firstname: str = None):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, firstname=user.firstname, password=hashed_password, is_user=user.is_user, is_nanny=user.is_nanny)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    count = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return count
    

"""
    Contracts
"""
def get_contract(db: Session, contract_id: int):
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()

def get_contracts_by_user_nanny(db: Session, user_id: str, nanny_id: str):
    return db.query(models.Contract).filter(and_(models.Contract.user_id == int(user_id), models.Contract.nanny_id == int(nanny_id))).all()

def get_contracts_by_date(db: Session, user_id: str, nanny_id: str, start: str, end: str):
    return db.query(models.Contract).filter(
        and_(
            models.Contract.user_id == int(user_id),
            models.Contract.nanny_id == int(nanny_id)
        )
    ).all()

def get_contracts_alreadyExists_by_date(db: Session, user_id: str, nanny_id: str, start: str, end: str):
    return db.query(models.Contract).filter(
        and_(
            models.Contract.user_id == int(user_id),
            models.Contract.nanny_id == int(nanny_id),
            or_(
                and_(
                    start <= models.Contract.end,
                    models.Contract.start <= end,
                ),
                and_(
                    start <= models.Contract.end,
                    models.Contract.end <= end,
                )
            )
        )
    ).all()

def get_contracts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contract).all()

def get_user_contracts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contract).join(models.User).offset(skip).limit(limit).all()

def create_contract(db: Session, contract: schemas.ContractCreate, user_id: str, nanny_id: str):
    created_on = datetime.now()
    db_contract = models.Contract(**contract.dict(), user_id=user_id, nanny_id=nanny_id, created_on=created_on, updated_on=None)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def delete_contract(db: Session, contract_id: int):
    count = db.query(models.Contract).filter(models.Contract.id == contract_id).delete()
    db.commit()
    return count


"""
    Working Days
"""
def get_working_day(db: Session, working_day_id: int):
    return db.query(models.WorkingDay).filter(models.WorkingDay.id == working_day_id).first()

def get_working_day_by_contract_day_type(db: Session, contract_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.WorkingDay).filter(
        models.WorkingDay.contract_id == int(contract_id)
    ).offset(skip).limit(limit).all()

def get_working_day_by_date(db: Session, contract_id: str, day: str):
    return db.query(models.WorkingDay).filter(
        and_(
            models.WorkingDay.contract_id == int(contract_id),
            models.WorkingDay.day == day
        )
    ).first()

def get_working_days_by_date_range(db: Session, contract_id: str, start: str, end: str, skip: int, limit: int):
    return db.query(models.WorkingDay).filter(
        and_(
            models.WorkingDay.contract_id == int(contract_id),
            models.WorkingDay.day >= start,
            models.WorkingDay.day <= end
        )
    ).offset(skip).limit(limit).all()

# def get_working_day_by_date(db: Session, contract_id = str, start = str, end = str):
#     return db.query(models.WorkingDay).filter(
#         and_(
#             models.WorkingDay.contract_id == int(contract_id),
#             models.WorkingDay.start > start, models.WorkingDay.end < end
#         )
#     ).all()

def get_working_days(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WorkingDay).offset(skip).limit(limit).all()

def get_user_working_days(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WorkingDay).offset(skip).limit(limit).all()

def create_working_day(db: Session, working_day: schemas.WorkingDayCreate, contract_id: str, day_type_id: str):
    created_on = datetime.now()
    db_working_day = models.WorkingDay(**working_day.dict(), contract_id=int(contract_id), day_type_id=int(day_type_id), created_on=created_on)
    db.add(db_working_day)
    db.commit()
    db.refresh(db_working_day)
    return db_working_day