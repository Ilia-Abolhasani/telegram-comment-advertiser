from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from sqlalchemy.orm import relationship
from .base import Base


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = relationship('Message', back_populates='histories')
    channel = relationship('Channel', back_populates='histories')
    post_id = Column(Integer, nullable=False)
    ping_reports = relationship('PingReport', back_populates='agent')
