from sqlalchemy import Column, Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Setting(Base):
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    # constrian
    __table_args__ = (UniqueConstraint('key'),)
