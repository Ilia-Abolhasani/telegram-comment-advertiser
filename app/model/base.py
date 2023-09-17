from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


class CustomBase:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    def to_json(self):
        columns = [column.key for column in class_mapper(self.__class__).columns]
        return {column: getattr(self, column) for column in columns}


Base = declarative_base(cls=CustomBase)