from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from sqlalchemy.orm import relationship
from .base import Base


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False)
    name = Column(String(128), nullable=True)
    last_id = Column(BigInteger, server_default=None, nullable=True)
    is_public = Column(Boolean, server_default='1', nullable=False)
    chat_id = Column(BigInteger, nullable=True)
    # foreign key 1 to many
    histories = relationship('History', back_populates='channel')
