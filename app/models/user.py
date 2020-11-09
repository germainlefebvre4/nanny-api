from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime, Time
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_user = Column(Boolean, default=True)
    is_nanny = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
