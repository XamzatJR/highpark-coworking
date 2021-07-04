from datetime import date
from orm.models import Place
from typing import Optional, Type

from pydantic import BaseModel


class DatePlacesModel(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None


class PlaceModel(BaseModel):
    place: int
    price: Optional[int] = None
    start: Optional[date]
    end: Optional[date]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls: Type['PlaceModel'], obj: Place) -> 'PlaceModel':
        setattr(obj, "start", obj.date.lower)
        setattr(obj, "end", obj.date.upper)
        return super().from_orm(obj)
