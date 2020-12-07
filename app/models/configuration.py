from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    value = Column(String)
