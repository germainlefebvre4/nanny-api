from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime, Time
from sqlalchemy.orm import relationship
from app.db.base_class import Base


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
