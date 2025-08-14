from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):

    @abstractmethod
    def to_read_model(self) -> BaseModel:
        pass
