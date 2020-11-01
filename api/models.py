from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime, Time
from sqlalchemy.orm import relationship

from .database import Base


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    value = Column(String)

class DayType(Base):
    __tablename__ = "day_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    working_days = relationship("WorkingDay", back_populates="day_type")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    is_user = Column(Boolean, default=True)
    is_nanny = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # user_contracts = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    # nanny_contracts = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    
    # contracts_user = relationship("Contract", foreign_keys=[user_contracts], back_populates="user")
    # contracts_nanny = relationship("Contract", foreign_keys=[nanny_contracts], back_populates="nanny")

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    weekdays = Column(Integer)
    weeks = Column(Integer)
    hours = Column(Float)
    price_hour_standard = Column(Float)
    price_hour_extra = Column(Float)
    price_fees = Column(Float)
    price_meals = Column(Float)
    start = Column(Date)
    end = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nanny_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    nanny = relationship("User", foreign_keys=[nanny_id])

    working_days = relationship("WorkingDay", back_populates="contract")

class WorkingDay(Base):
    __tablename__ = "working_days"
    
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date)
    start = Column(Time)
    end = Column(Time)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    contract_id = Column(Integer, ForeignKey("contracts.id"))
    day_type_id = Column(Integer, ForeignKey("day_types.id"))

    contract = relationship("Contract", back_populates="working_days")
    day_type = relationship("DayType", back_populates="working_days")
