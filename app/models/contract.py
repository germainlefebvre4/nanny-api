from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime, Time
from sqlalchemy.orm import relationship

from app.db.base_class import Base


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
