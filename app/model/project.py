from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from sqlalchemy.orm import relationship
from .base import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    # foreign key 1 to many
    messages = relationship('Message', back_populates='project')
