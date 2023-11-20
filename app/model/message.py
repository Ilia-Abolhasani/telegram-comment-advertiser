from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from sqlalchemy.orm import relationship
from .base import Base


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = relationship('Project', back_populates='histories')
    text = Column(String(1028), nullable=False)
    histories = relationship('History', back_populates='message')
