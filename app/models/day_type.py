from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DayType(Base):
    __tablename__ = "day_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    working_days = relationship("WorkingDay", back_populates="day_type")
